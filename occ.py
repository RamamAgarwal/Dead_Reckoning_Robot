import matplotlib.pyplot as plt
import numpy as np
import socket
import keyboard
import time

ESP32_IP = "192.168.4.1"
ESP32_PORT = 80
def probability_to_log_odds(p):
    return np.log(p / (1 - p))

def log_odds_to_probability(l):
    return 1 / (1 + np.exp(-l))

class RobotMapper:
    def __init__(self):  # Corrected to __init__
        # The rest of your initialization code
        # self.grid_size = int(input("Enter grid size (number of cells): "))
        # self.cell_size = float(input("Enter cell size in cm: "))
        # self.sensor_position = float(input("Enter sensor position within the cell (0.5 for center, 1 for edge): "))
        # self.tol = float(input("Enter tolerance in cm: "))
        # self.initial_map_probability = float(input("Enter initial map probability: "))
        # # Detailed sensor model input
        # self.prob_empty = float(input("Enter probability for empty cell: "))
        # self.prob_occupied = float(input("Enter probability for occupied cell: "))
        # self.prob_unknown = float(input("Enter probability for unknown cell: "))

        self.grid_size = 5
        self.cell_size = 30
        self.sensor_position = 1
        self.tol = 5
        self.initial_map_probability = 0.5
        
        # Detailed sensor model input
        self.prob_empty = 0.2
        self.prob_occupied = 0.8
        self.prob_unknown = 0.5
        
        # Convert initial map probability to log odds
        self.initial_map_log_odds = probability_to_log_odds(self.initial_map_probability)
        
        # Get initial position and orientation
        while True:
            try:
                self.position = int(input(f"Enter initial position (1 to {self.grid_size * self.grid_size}): "))
                if not (1 <= self.position <= self.grid_size * self.grid_size):
                    print("Invalid position!")
                    continue
                    
                self.orientation = input("Enter initial orientation (right/down/left/up): ").lower()
                if self.orientation not in ['right', 'down', 'left', 'up']:
                    print("Invalid orientation!")
                    continue
                    
                break
            except ValueError:
                print("Invalid input! Please enter numbers for position.")
    
        self.grid = np.full((self.grid_size, self.grid_size), self.initial_map_log_odds)  # Initialize grid with initial map log odds
        self.cell_values = [self.initial_map_log_odds] * (self.grid_size * self.grid_size)
        self.robot_marker = None
        self.t = 0  # Initialize time index
        self.grid_states = []  # List to store grid states
        self.setup_display()
        
        # Establish socket connection
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((ESP32_IP, ESP32_PORT))
            print("[INFO] Connected to ESP32!")
        except Exception as e:
            print(f"[ERROR] Failed to connect to ESP32: {e}")
            self.client_socket = None
        
    def setup_display(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_aspect('equal')
        self.ax.grid(False)
        
        self.im = self.ax.imshow(log_odds_to_probability(self.grid), cmap='Greys', vmin=0, vmax=1, interpolation='nearest')
        
        for i in range(self.grid_size + 1):
            self.ax.axhline(y=i - 0.5, color='black', linewidth=2)
            self.ax.axvline(x=i - 0.5, color='black', linewidth=2)
            
        self.ax.set_xticks(np.arange(0, self.grid_size, 1))
        self.ax.set_yticks(np.arange(0, self.grid_size, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        
        self.update_robot_marker()
        
        plt.ion()
        plt.show()

    def update_robot_marker(self):
        if self.robot_marker:
            self.robot_marker.remove()
        
        cell_x = (self.position - 1) % self.grid_size
        cell_y = (self.position - 1) // self.grid_size
        
        # Adjust rotation angles to match grid directions
        if self.orientation == 'right':
            rotation = -90
        elif self.orientation == 'up':
            rotation = 180
        elif self.orientation == 'left':
            rotation = 90
        else:  # down
            rotation = 0
        
        self.robot_marker = plt.matplotlib.patches.RegularPolygon(
            xy=(cell_x, cell_y),
            numVertices=3,
            radius=0.3,
            orientation=np.radians(rotation),
            facecolor='red',
            edgecolor='black'
        )
        self.ax.add_patch(self.robot_marker)
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def send_command(self, command):
        """Send a command to the ESP32."""
        if self.client_socket:
            try:
                self.client_socket.sendall((command + "\n").encode('utf-8'))
                print(f"[DEBUG] Command sent: {command}")
            except Exception as e:
                print(f"[ERROR] Failed to send command: {e}")

    def receive_response(self):
        """Receive a response from the ESP32."""
        if self.client_socket:
            try:
                response = self.client_socket.recv(1024).decode('utf-8').strip()
                return response
            except Exception as e:
                print(f"[ERROR] Failed to receive response: {e}")
                return None

    def start_esp32_control(self):
        print("[INFO] Use arrow keys to control the robot, 'r' to get sensor reading, 'ESC' to exit.")
        try:
            while True:
                if keyboard.is_pressed('up'):
                    self.send_command("UP")
                    time.sleep(0.01)
                elif keyboard.is_pressed('down'):
                    self.send_command("DOWN")
                    time.sleep(0.01)
                elif keyboard.is_pressed('left'):
                    self.send_command("LEFT")
                    time.sleep(0.01)
                elif keyboard.is_pressed('right'):
                    self.send_command("RIGHT")
                    time.sleep(0.01)
                elif keyboard.is_pressed('esc'):
                    print("[INFO] Exiting...")
                    self.send_command("STOP")
                    break
                else:
                    self.send_command("STOP")
                    time.sleep(0.01)
        finally:
            print("Done")
            # if self.client_socket:
            #     self.client_socket.close()
            #     print("[INFO] Disconnected from ESP32.")

    def update_position(self):
        print(f"\nCurrent position: Cell {self.position}, Facing {self.orientation}")
        try:
            new_pos = int(input("Enter new position (1 to {}): ".format(self.grid_size * self.grid_size)))
            new_orient = input("Enter new orientation (right/down/left/up): ").lower()
            
            if 1 <= new_pos <= self.grid_size * self.grid_size and new_orient in ['right', 'down', 'left', 'up']:
                self.position = new_pos
                self.orientation = new_orient
                self.update_robot_marker()
                print("Position updated successfully!")
                
                self.t += 1  # Increment time index
            else:
                print("Invalid input!")
        except ValueError:
            print("Invalid input!")

    def process_distance(self, distance):
        current_x = (self.position - 1) % self.grid_size
        current_y = (self.position - 1) // self.grid_size
        
        # Calculate effective distance using sensor position and tolerance
        effective_distance = distance + self.cell_size * self.sensor_position
        min_distance = effective_distance - self.tol
        max_distance = effective_distance + self.tol
        
        # Calculate cells covered based on effective distance
        min_cells_to_mark = int(min_distance / self.cell_size)
        max_cells_to_mark = int(max_distance / self.cell_size)
        
        if self.orientation == 'right':
            for x in range(current_x + 1, min(current_x + max_cells_to_mark, self.grid_size)):
                cell_num = current_y * self.grid_size + x + 1
                self.update_log_odds(cell_num, self.prob_empty)  # empty space
                
            if current_x + max_cells_to_mark < self.grid_size:
                obstacle_cell = current_y * self.grid_size + current_x + max_cells_to_mark + 1
                self.update_log_odds(obstacle_cell, self.prob_occupied)  # obstacle
        
        elif self.orientation == 'down':
            for y in range(current_y + 1, min(current_y + max_cells_to_mark, self.grid_size)):
                cell_num = y * self.grid_size + current_x + 1
                self.update_log_odds(cell_num, self.prob_empty)  # empty space
                
            if current_y + max_cells_to_mark < self.grid_size:
                obstacle_cell = (current_y + max_cells_to_mark) * self.grid_size + current_x + 1
                self.update_log_odds(obstacle_cell, self.prob_occupied)  # obstacle
        
        elif self.orientation == 'left':
            for x in range(current_x - 1, max(current_x - max_cells_to_mark, -1), -1):
                cell_num = current_y * self.grid_size + x + 1
                self.update_log_odds(cell_num, self.prob_empty)  # empty space
                
            if current_x - max_cells_to_mark >= 0:
                obstacle_cell = current_y * self.grid_size + (current_x - max_cells_to_mark) + 1
                self.update_log_odds(obstacle_cell, self.prob_occupied)  # obstacle
        
        else:  # up
            for y in range(current_y - 1, max(current_y - max_cells_to_mark, -1), -1):
                cell_num = y * self.grid_size + current_x + 1
                self.update_log_odds(cell_num, self.prob_empty)  # empty space
                
            if current_y - max_cells_to_mark >= 0:
                obstacle_cell = (current_y - max_cells_to_mark) * self.grid_size + current_x + 1
                self.update_log_odds(obstacle_cell, self.prob_occupied)  # obstacle

    def update_log_odds(self, cell_num, probability):
        cell_x = (cell_num - 1) % self.grid_size
        cell_y = (cell_num - 1) // self.grid_size
        
        # Convert probability to log odds
        log_odds = probability_to_log_odds(probability)
        
        # Update log odds
        self.grid[cell_y, cell_x] += log_odds - self.initial_map_log_odds  # Corrected addition
        
        # Convert log odds to probability
        self.cell_values[cell_num - 1] = log_odds_to_probability(self.grid[cell_y, cell_x])
        
        # Update grid display
        self.im.set_array(log_odds_to_probability(self.grid))
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

        # Record grid state after update
        self.grid_states.append(self.grid.copy())
        self.t += 1

    def get_distance_measurement(self):
        self.send_command("READ")
        time.sleep(0.01)
        data = self.receive_response()
        if data and data.isdigit():
            distance_value = int(data)
            if distance_value < 3000:
                print(f"[SENSOR DATA] Distance: {distance_value / 10} cm")
                distance_cm = float(distance_value) / 10  # Convert mm to cm
                approve = input("Approve this measurement? (y/n): ").lower()
                if approve == 'y':
                    self.process_distance(distance_cm)
                elif approve == 'n':
                    print("Measurement not approved. Try again!")
                else:
                    print("Invalid input. Measurement not approved.")
            else:
                print("OUT_OF_RANGE")
        else:
            print("Invalid data received from ESP32.")

    def print_grid_states(self):
        if not self.grid_states:
            print("No grid states to display.")
            return
        
        print("\nGrid States:")
        for t, grid_state in enumerate(self.grid_states):
            print(f"\nTime {t}:")
            print("Grid State (Probabilities):")
            print(np.array2string(log_odds_to_probability(grid_state), formatter={'float_kind':lambda 
            x: f"{x:.2f}"}))
            print("Grid State (Log Odds):")
            print(np.array2string(grid_state, formatter={'float_kind':lambda 
            x: f"{x:.2f}"}))
            print(f"Orientation: {self.orientation}")

    def print_final_probabilities(self):
        print("\nFinal Probabilities for Each Cell:")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_num = i * self.grid_size + j + 1
                log_probability = self.grid[i, j]
                probability = log_odds_to_probability(self.grid[i, j])
                print(f"P(Cell) {cell_num}: {probability:.4f}")
                print(f"LP(Cell) {cell_num}: {log_probability:.4f}")

    def run(self):
        while True:
            print("\nMenu:")
            print("1. Update position and orientation")
            print("2. Start keyboard control")
            print("3. Get distance measurement from ESP32")
            print("4. Print grid states")
            print("0. Exit")
            
            choice = input("Enter your choice (0-4): ")
            
            if choice == '1':
                self.update_position()
            elif choice == '2':
                self.start_esp32_control()
            elif choice == '3':
                self.get_distance_measurement()
            elif choice == '4':
                self.print_grid_states()
            elif choice == '0':
                self.print_grid_states()
                self.print_final_probabilities()
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")

if __name__ == "__main__":
    mapper = RobotMapper()
    mapper.run()