# Automated Chess Gameplay with Computer Vision and a Robotic Arm

## 1. Project Overview
This project implements a fully autonomous chess-playing system that integrates computer vision, artificial intelligence, and robotics. The system perceives the physical board state, calculates optimal moves using a chess engine, and physically executes those moves using a robotic manipulator. It bridges the gap between digital chess logic and physical interaction.

## 2. Replication Requirements
To recreate the results of this study and ensure the system functions correctly, the following specific setup is required:

*   **Chess Set:** You must use the exact same chess pieces as used in the study.
*   **Camera Setup:** A top-down camera angle is strictly required, matching the perspective in the training data.
*   **Dataset:** Refer to the [Chess TopView Dataset](https://app.roboflow.com/mohammadjalkhatib/chess_dataset_topview/) on Roboflow for reference images and training data.
*   **Robotic Hardware:** A **Quanser QArm** (4-DOF robotic manipulator) and the associated Simulink control file are required to execute the physical moves.

## 3. System Architecture
The system is built on a modular architecture consisting of three core components:
* **Perception (Computer Vision):** Uses a fine-tuned **YOLOv8x** deep learning model to detect chess pieces and board coordinates from a top-down camera feed.
* **Decision Making (Game Logic):** Utilizes **Stockfish**, a high-performance open-source chess engine, to calculate the best strategic move based on the board state.
* **Actuation (Robotics):** Employs a **Quanser QArm** (4-DOF robotic manipulator) to execute pick-and-place operations.

## 4. Technical Implementation

### Vision Pipeline
* **Model:** YOLOv8x (86M parameters) fine-tuned on a custom dataset of 173 annotated chessboard images (augmented to 363 samples).
* **Logic:** The system converts detected bounding boxes into **Forsyth-Edwards Notation (FEN)** to represent the game state.
* **Mapping:** Pixel coordinates are mapped to the 8x8 chess grid using calculated row/column indices based on board dimensions.

### Robotic Control
* **Hardware:** Quanser QArm with a tendon-based 2-finger gripper.
* **Software:** Controlled via **MATLAB Simulink** using a "Pick and Place" model.
* **Movement Logic:** Uses waypoint navigation with cubic spline interpolation for smooth trajectories.
* **Sequence:** Home -> Pick (Waypoint 1 & 2) -> Home -> Place (Waypoint 1 & 2) -> Home.
* **Gripper Configuration:** Optimal grip found at 80% closure to prevent knocking over pieces.

### Hardware Setup
* **Camera:** Smartphone camera mounted in a fixed top-down position.
* **Computers:** A dual-setup with a laptop running Vision/Stockfish and a desktop running Simulink for robot control.
* **Board:** Standard 35cm x 35cm chessboard.

## 5. Performance Metrics

### Computer Vision
* **Training Results:** Precision: 0.972, Recall: 0.984, mAP@50: 0.985.
* **Real-World Testing:** Average accuracy of 85.8% under operational conditions. The "White Pawn" class achieved the highest accuracy (96%).

### Robotic Actuation
* **Success Rate:** 87% of moves successful on the first attempt; 97% successful by the second attempt.

## 6. Deployment Recommendations & Lessons Learned
* **Lighting:** Use daylight-balanced LED panels with diffusers to minimize glare and shadows, which are critical for FEN generation accuracy.
* **Calibration:** Rigidly mount the board and camera; use a laser distance meter for precise height calibration.
* **Gripping:** Adjust gripper saturation limits (0.8 to 0.95) to handle variable piece geometries without toppling them.

## 7. Datasets & Resources
* **Dataset:** The "Chess TopView Dataset" used for training is available via Roboflow/Universe.
* **Model:** The fine-tuned YOLOv8 model is available on Hugging Face (`Mohammadjalkhatib/chess_yolo`).

## 8. Project Flow

1.  **Image Capture**: The system captures an image of the chessboard using a webcam. Images are saved to `computer_vision_files/moves_pictures/`.
2.  **FEN Generation**: A trained YOLOv8 model detects pieces and the board to generate a FEN (Forsyth-Edwards Notation) string representing the game state.
3.  **Move Calculation**: Stockfish analyzes the FEN string to determine the best next move.
4.  **Robot Control**: The best move (e.g., "e2e4") is translated into physical coordinates (pick and place points) using a mapping CSV. These coordinates are formatted as waypoints for a Simulink model to control the robotic arm.

## 9. Chess Engine Details

The project uses **Stockfish**, a powerful open-source chess engine.

*   **Version**: [Stockfish 16.1](https://stockfishchess.org/blog/2024/stockfish-16-1/) (Windows x86-64 AVX2 build)
*   **Location**: `Stockfish engine/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe`
*   **Input**: A **FEN (Forsyth-Edwards Notation)** string representing the current board state.
    *   *Example*: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`
*   **Output**: The **Best Move** in UCI (Universal Chess Interface) format.
    *   *Example*: `e2e4` (Move piece from e2 to e4)

## 9. Prerequisites

### Hardware
- Webcam (connected to index 0)
- Robotic Arm (controlled via Simulink)
- Chessboard and pieces

### Software
- Python 3.x
- [Stockfish Engine](https://stockfishchess.org/) (included in `Stockfish engine/`)
- MATLAB/Simulink (for robot control execution)

## 10. Installation

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

## 11. Usage

Run the main script to start the pipeline:

```bash
python main.py
```

The script will:
1.  Capture an image.
2.  Print the generated FEN string.
3.  Print the best move calculated by Stockfish.
4.  Output the robot waypoints array.

### Troubleshooting

*   **"FEN string is missing kings"**: If the camera sees an empty board or fails to detect pieces, the script will warn you and skip the Stockfish step. Ensure the board is set up and well-lit.
*   **Camera errors**: Ensure no other application is using the webcam.

## 12. Project Structure

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
