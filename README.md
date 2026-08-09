# Sixth Sense Bot

An Arduino-based robot controlled over Serial commands, with real-time visual feedback on an onboard LED Matrix and an indicator LED — driven by a webcam color-tracking controller.

## Project Structure

```
sixth_sense_bot/          Arduino sketch (firmware)
color_tracker/            Python webcam controller (sends Serial commands)
```

## Features

- Serial command control: `F` (forward), `B` (backward), `L` (left), `R` (right), `S` (stop)
- Live directional feedback via `Arduino_LED_Matrix` (arrow icons + stop icon)
- LED blink feedback synced to each movement command
- Simple dual-motor driver logic (2 motors, 4 direction pins)
- Webcam color-object tracking controller (Python) that drives the bot by moving a colored object across on-screen zones

## Hardware

| Component        | Pin |
|-------------------|-----|
| Motor A IN1        | 5   |
| Motor A IN2        | 6   |
| Motor B IN1         | 9   |
| Motor B IN2         | 10  |
| Status LED           | 13  |

Board: Arduino with built-in LED Matrix support (e.g. Arduino UNO R4 WiFi).

## How the firmware works

The board listens on Serial (9600 baud) for single-character commands. On each command it:
1. Drives the motors in the corresponding direction
2. Renders the matching arrow/stop bitmap on the LED matrix
3. Blinks the status LED a number of times unique to that command

## Firmware setup (Arduino)

1. Open `sixth_sense_bot/sixth_sense_bot.ino` in the Arduino IDE (or VS Code with the Arduino extension)
2. Select your board and port
3. Upload the sketch

## Computer Vision controller (Python)

`color_tracker/color_tracker.py` opens your webcam, tracks a chosen color object, and sends `F`/`B`/`L`/`R`/`S` over Serial to the Arduino based on which on-screen zone the object is in.

1. Install dependencies:
   ```
   pip install -r color_tracker/requirements.txt
   ```
2. Open `color_tracker/color_tracker.py` and set `SERIAL_PORT` to your Arduino's port
   (Windows: `COM3`, `COM4`... / Mac-Linux: `/dev/ttyUSB0` or `/dev/ttyACM0`)
3. Run it:
   ```
   python color_tracker/color_tracker.py
   ```
4. Pick a color from the menu, hold up a matching colored object in front of the webcam, and move it across the on-screen zones (up/down/left/right/middle) to drive the bot. Press `ESC` to quit.

## License

MIT
