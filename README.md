# Automated Chess Gameplay with Computer Vision and a Robotic Arm

This project integrates Computer Vision (YOLOv8), a Chess Engine (Stockfish), and a Robotic Arm Controller to play chess autonomously. It captures the board state using a camera, calculates the best move, and generates waypoints for a robot to execute the move.

## 🚀 Project Flow

1.  **Image Capture**: The system captures an image of the chessboard using a webcam. Images are saved to `computer_vision_files/moves_pictures/`.
2.  **FEN Generation**: A trained YOLOv8 model detects pieces and the board to generate a FEN (Forsyth-Edwards Notation) string representing the game state.
3.  **Move Calculation**: Stockfish analyzes the FEN string to determine the best next move.
4.  **Robot Control**: The best move (e.g., "e2e4") is translated into physical coordinates (pick and place points) using a mapping CSV. These coordinates are formatted as waypoints for a Simulink model to control the robotic arm.

## 🛠️ Prerequisites

### Hardware
- Webcam (connected to index 0)
- Robotic Arm (controlled via Simulink)
- Chessboard and pieces

### Software
- Python 3.x
- [Stockfish Engine](https://stockfishchess.org/) (included in `Stockfish engine/`)
- MATLAB/Simulink (for robot control execution)

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Mohammadjalkhatib/Automated-Chess-Gameplay-with-Computer-Vision-and-a-Robotic-Arm.git
    cd Automated-Chess-Gameplay-with-Computer-Vision-and-a-Robotic-Arm
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This installs `ultralytics`, `numpy`, `pandas`, `python-chess`, `stockfish`, and `opencv-python`.*

3.  **Git LFS**:
    This project uses Git Large File Storage (LFS) for the trained model. Ensure you have Git LFS installed and pull the large files:
    ```bash
    git lfs install
    git lfs pull
    ```

## 🎮 Usage

Run the main script to start the pipeline:

```bash
python main.py
```

The script will:
1.  Capture an image.
2.  Print the generated FEN string.
3.  Print the best move calculated by Stockfish.
4.  Output the robot waypoints array.

### ⚠️ Troubleshooting

*   **"FEN string is missing kings"**: If the camera sees an empty board or fails to detect pieces, the script will warn you and skip the Stockfish step. Ensure the board is set up and well-lit.
*   **Camera errors**: Ensure no other application is using the webcam.

## 📂 Project Structure

*   `main.py`: Main entry point orchestrating the flow.
*   `computer_vision_files/`:
    *   `image_to_fen.py`: Logic for converting images to FEN.
    *   `using_stockfish.py`: Interface with the Stockfish engine.
    *   `moves_pictures/`: Directory where captured images are stored.
*   `robot_controller/`:
    *   `robot_control.py`: Logic for coordinate mapping and waypoint generation.
    *   `Placement of pieces_csv.csv`: Mapping of board squares to physical coordinates.
*   `Trained model/`: Contains the YOLOv8 model (`best.pt`).
*   `Stockfish engine/`: Contains the Stockfish executable.
