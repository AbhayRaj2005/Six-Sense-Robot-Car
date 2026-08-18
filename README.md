# Sixth Sense Bot

An Arduino-based robot controlled over Serial commands, with real-time visual feedback on an onboard LED Matrix and an indicator LED — driven by a webcam color-tracking controller.

**© 2026 Abhay Raj. All rights reserved.**

> **Note:** Source code for this project is private. This README documents the project for showcase purposes only.

## Overview

The bot is controlled by a webcam-based color-tracking controller running on a PC. A colored object is tracked in real time using OpenCV; depending on which on-screen zone (Up/Down/Left/Right/Middle) the object is in, a single-character command is sent over Serial to the Arduino. The Arduino then drives the motors accordingly and shows live directional feedback on its onboard LED Matrix.

## What makes this different

Color-tracking robots (webcam + OpenCV + Arduino) are a well-known concept. What sets this build apart is the **feedback system**:

- **Onboard LED Matrix directional feedback** — hand-designed 8x12 pixel bitmap icons (up/down/left/right arrows + a stop symbol) rendered live on the Arduino UNO R4's built-in LED Matrix, so the bot visually confirms every command it receives
- **Command-specific LED blink signaling** — each direction blinks the status LED a distinct number of times (1 for forward, 2 for backward, 3 for left, 4 for right), giving a second, independent feedback channel
- **Discrete 5-zone tracking logic** — object position is mapped to five on-screen zones (Up/Down/Left/Right/Middle) rather than continuous coordinate-based PID following, keeping the control logic simple and predictable

## Features

- Serial command control: `F` (forward), `B` (backward), `L` (left), `R` (right), `S` (stop)
- Live directional feedback via `Arduino_LED_Matrix` (arrow icons + stop icon)
- LED blink feedback synced to each movement command
- Simple dual-motor driver logic (2 motors, 4 direction pins)
- Webcam color-object tracking controller (Python/OpenCV) that drives the bot by moving a colored object across on-screen zones

## Hardware

| Component        | Pin |
|-------------------|-----|
| Motor A IN1        | 5   |
| Motor A IN2        | 6   |
| Motor B IN1         | 9   |
| Motor B IN2         | 10  |
| Status LED           | 13  |

Board: Arduino UNO R4 (built-in LED Matrix support required).

## How the firmware works

The board listens on Serial (9600 baud) for single-character commands. On each command it:
1. Drives the motors in the corresponding direction
2. Renders the matching arrow/stop bitmap on the LED matrix
3. Blinks the status LED a number of times unique to that command

## How the Computer Vision controller works

A Python script opens the webcam, tracks a chosen color object using HSV masking and contour detection, and sends `F`/`B`/`L`/`R`/`S` over Serial to the Arduino based on which on-screen zone the object's centroid falls into.

## License

All rights reserved © 2026 Abhay Raj — source code is private and not licensed for reuse without permission.
