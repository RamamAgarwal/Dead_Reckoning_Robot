#include<WiFi.h>
#include<WifiServer.h>
#include "Adafruit_VL53L0X.h"

// Motor Control Pins
#define IN1 14
#define IN2 27
#define IN3 26
#define IN4 25
#define ENA 13
#define ENB 33

// Wi-Fi credentials
const char* ssid = "DEVIL";      
const char* password = "01092005"; 

WiFiServer server(80); // Create a web server on port 80
WiFiClient client;     // Client object


// Motor speeds
float leftMotorSpeed = 0.7;
float rightMotorSpeed = 1 ;

// Initialize VL53L0X sensor
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Motor Control Functions
void moveForward()
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, (int)(leftMotorSpeed * 255));
    analogWrite(ENB, (int)(rightMotorSpeed * 255));
    Serial.println("Moving Forward");
}

void moveBackward()
{
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, (int)(leftMotorSpeed * 255));
    analogWrite(ENB, (int)(rightMotorSpeed * 255));
    Serial.println("Moving Backward");
}

void turnLeft()
{
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, (int)(leftMotorSpeed * 255));
    analogWrite(ENB, (int)(rightMotorSpeed * 255));
    Serial.println("Turning Left");
}

void turnRight()
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, (int)(leftMotorSpeed * 255));
    analogWrite(ENB, (int)(rightMotorSpeed * 255));
    Serial.println("Turning Right");
}

void stopMotors()
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);
    Serial.println("Motors Stopped");
}

void setup()
{
    Serial.begin(115200);

    // Set motor control pins as OUTPUT
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);

    // Start with motors stopped
    stopMotors();

    // Initialize VL53L0X sensor
    if (!lox.begin())
    {
        Serial.println("Failed to initialize VL53L0X!");
        while (1)
            ;
    }
    Serial.println("VL53L0X initialized.");

    // Set up Wi-Fi Access Point
    
    WiFi.softAP(ssid, password);
    server.begin(); // Start the server
    Serial.println("Server started");
    Serial.print("AP IP address: ");
    Serial.println(WiFi.softAPIP());
}


void loop()
{
    client = server.available();

    if (client)
    {
        Serial.println("Client connected.");
        while (client.connected())
        {
            if (client.available())
            {
                String command = client.readStringUntil('\n');
                command.trim();
                Serial.println("Received Command: " + command);

                // Movement Commands
                if (command == "UP")
                {
                    Serial.println("Moving UP...");
                    moveForward();
                }
                else if (command == "DOWN")
                {
                    Serial.println("Moving DOWN...");
                    moveBackward();
                }
                else if (command == "LEFT")
                {
                    Serial.println("Turning LEFT...");
                    turnLeft();
                }
                else if (command == "RIGHT")
                {
                    Serial.println("Turning RIGHT...");
                    turnRight();
                }
                else if (command == "STOP")
                {
                    Serial.println("Stopping...");
                    stopMotors();
                }
                // Sensor Command
                else if (command == "READ")
                {
                    VL53L0X_RangingMeasurementData_t measure;
                    lox.rangingTest(&measure, false);

                    String response;
                    if (measure.RangeStatus != 4)
                    {
                        response = String(measure.RangeMilliMeter);
                    }
                    else
                    {
                        response = "OUT_OF_RANGE";
                    }

                    client.println(response);
                    Serial.println("Sent Response: " + response);
                }
                // Unknown Command
                else
                {
                    client.println("INVALID_COMMAND");
                    Serial.println("Sent Response: INVALID_COMMAND");
                }
            }
        }
        client.stop();
        stopMotors();
        Serial.println("Client disconnected.");
    }
}