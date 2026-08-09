#include "Arduino_LED_Matrix.h"

ArduinoLEDMatrix matrix;

// ----- Pin Configuration -----
const int M1 = 5;   // Motor A IN1
const int M2 = 6;   // Motor A IN2
const int M3 = 9;   // Motor B IN1
const int M4 = 10;  // Motor B IN2
const int LED_PIN = 13;

// ----- Serial Command Codes -----
const char CMD_FORWARD  = 'F';
const char CMD_BACKWARD = 'B';
const char CMD_LEFT     = 'L';
const char CMD_RIGHT    = 'R';
const char CMD_STOP     = 'S';

// ----- Arrow / Icon Bitmaps (8x12) -----
const uint8_t arrow_up[8][12] = {
  {0,0,0,0,1,1,1,1,0,0,0,0},
  {0,0,0,1,1,1,1,1,1,0,0,0},
  {0,0,1,0,0,1,1,0,0,1,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,1,1,1,1,0,0,0,0}
};

const uint8_t arrow_down[8][12] = {
  {0,0,0,0,1,1,1,1,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,0,0,0,1,1,0,0,0,0,0},
  {0,0,1,0,0,1,1,0,0,1,0,0},
  {0,0,0,1,1,1,1,1,1,0,0,0},
  {0,0,0,0,1,1,1,1,0,0,0,0}
};

const uint8_t arrow_left[8][12] = {
  {0,0,0,0,0,1,0,0,0,0,0,0},
  {0,0,0,0,1,1,0,0,0,0,0,0},
  {0,0,0,1,1,0,0,0,0,0,0,0},
  {0,0,1,1,1,1,1,1,1,0,0,0},
  {0,0,1,1,1,1,1,1,1,0,0,0},
  {0,0,0,1,1,0,0,0,0,0,0,0},
  {0,0,0,0,1,1,0,0,0,0,0,0},
  {0,0,0,0,0,1,0,0,0,0,0,0}
};

const uint8_t arrow_right[8][12] = {
  {0,0,0,0,0,0,1,0,0,0,0,0},
  {0,0,0,0,0,0,1,1,0,0,0,0},
  {0,0,0,0,0,0,0,1,1,0,0,0},
  {0,0,0,1,1,1,1,1,1,1,0,0},
  {0,0,0,1,1,1,1,1,1,1,0,0},
  {0,0,0,0,0,0,0,1,1,0,0,0},
  {0,0,0,0,0,0,1,1,0,0,0,0},
  {0,0,0,0,0,0,1,0,0,0,0,0}
};

const uint8_t stop_icon[8][12] = {
  {0,0,0,1,1,1,1,1,1,0,0,0},
  {0,0,1,1,0,0,0,0,1,1,0,0},
  {0,1,1,0,1,0,0,1,0,1,1,0},
  {0,1,0,0,0,1,1,0,0,0,1,0},
  {0,1,0,0,0,1,1,0,0,0,1,0},
  {0,1,1,0,1,0,0,1,0,1,1,0},
  {0,0,1,1,0,0,0,0,1,1,0,0},
  {0,0,0,1,1,1,1,1,1,0,0,0}
};

void setup() {
  Serial.begin(9600);

  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(M3, OUTPUT);
  pinMode(M4, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  matrix.begin();
  stopMotors();
  matrix.renderBitmap(stop_icon, 8, 12); // Show STOP symbol on startup
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    // Ignore newline / carriage-return / stray whitespace from Serial Monitor
    if (command == '\n' || command == '\r' || command == ' ') {
      return;
    }

    switch (command) {
      case CMD_FORWARD:
        forward();
        matrix.renderBitmap(arrow_up, 8, 12);
        blinkLED(1);
        break;

      case CMD_BACKWARD:
        backward();
        matrix.renderBitmap(arrow_down, 8, 12);
        blinkLED(2);
        break;

      case CMD_LEFT:
        left();
        matrix.renderBitmap(arrow_left, 8, 12);
        blinkLED(3);
        break;

      case CMD_RIGHT:
        right();
        matrix.renderBitmap(arrow_right, 8, 12);
        blinkLED(4);
        break;

      case CMD_STOP:
        stopMotors();
        matrix.renderBitmap(stop_icon, 8, 12);
        digitalWrite(LED_PIN, LOW); // Stop blinking
        break;

      default:
        // Unknown command received, ignore safely
        break;
    }
  }
}

// ----- Motor Control Functions -----
void forward() {
  digitalWrite(M1, HIGH); digitalWrite(M2, LOW);
  digitalWrite(M3, HIGH); digitalWrite(M4, LOW);
}

void backward() {
  digitalWrite(M1, LOW); digitalWrite(M2, HIGH);
  digitalWrite(M3, LOW); digitalWrite(M4, HIGH);
}

void left() {
  digitalWrite(M1, LOW); digitalWrite(M2, HIGH);
  digitalWrite(M3, HIGH); digitalWrite(M4, LOW);
}

void right() {
  digitalWrite(M1, HIGH); digitalWrite(M2, LOW);
  digitalWrite(M3, LOW); digitalWrite(M4, HIGH);
}

void stopMotors() {
  digitalWrite(M1, LOW); digitalWrite(M2, LOW);
  digitalWrite(M3, LOW); digitalWrite(M4, LOW);
}

// ----- LED Blink Feedback -----
void blinkLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(150);
    digitalWrite(LED_PIN, LOW);
    delay(150);
  }
}
