# Football Analytic System

This project is a football analytic system that utilizes YOLOv5 and ByteTrack models to estimate player speed, distance covered, and ball control for each team.

## Demo

## Key Features

*   **Player & Ball Tracking:** Detects and tracks players and the ball throughout the video.
*   **Speed & Distance Estimation:** Calculates the real-world speed of players and the distances they cover.
*   **Ball Possession:** Determines which player is currently in possession of the ball.

## Usage

### Running the Analysis

The primary entry point for the analysis is `main.py`. It is designed to process an input video file and produce an annotated output video with all the derived analytics overlaid.

```bash
python main.py
```
*(Note: You will need to configure the input and output video paths within `main.py`.)*

## Environment
* OpenCV 4.12
* supervision 0.26
* pandas 2.3
* NumPy 2.0
* Python 3.12