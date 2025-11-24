
import numpy as np
from ultralytics import YOLO

def image_to_fen(image_path, model_path="yolov8x_chess.pt"):
    """
    Converts an image of a chessboard into a FEN string using YOLOv8x predictions.

    Parameters:
    - image_path (str): Path to the input chessboard image.
    - model_path (str): Path to the YOLOv8 model trained for chess piece detection.

    Returns:
    - str: The generated FEN notation representing the board state.
    """
    # Load the YOLOv8 model
    model = YOLO(model_path)

    # Get detections
    results = model(image_path) 

    # Define FEN piece mapping (Black → lowercase, White → uppercase)
    fen_mapping = {
        "Black_Pawn": "p", "Black_Rook": "r", "Black_Knight": "n",
        "Black_Bishop": "b", "Black_Queen": "q", "Black_King": "k",
        "White_Pawn": "P", "White_Rook": "R", "White_Knight": "N",
        "White_Bishop": "B", "White_Queen": "Q", "White_King": "K"
    }

    # Extract board and piece detections
    chessboard = None
    pieces = []

    for i, box in enumerate(results[0].boxes.xyxy.cpu().numpy()):  # Use xyxy for bounding boxes
        x_min, y_min, x_max, y_max = box      # Extract bounding box coordinates
        label = results[0].names[int(results[0].boxes.cls[i])]  # Get class label

        if label == "Chess_Board":
            # Store chessboard coordinates (top-left x, top-left y, width, height)
            chessboard = (x_min, y_min, x_max - x_min, y_max - y_min)
        else:
            # Compute center coordinates of the detected piece
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            pieces.append((x_center, y_center, label))


    # Extract chessboard dimensions
    x_b, y_b, w_b, h_b = chessboard
    h_s = h_b / 8   # Square height
    w_s = w_b / 8   # Square width

    # Initialize empty board representation using a NumPy 2D array with 1-based indexing
    board = np.full((9, 9), "", dtype=object)  # Use (9,9) so we can use index 1-8

    # Map each detected piece to its row and column index
    for x_c, y_c, piece in pieces:
        row_index = 8 - int((y_c - y_b) / h_s)  # row_index equation in section 3.2
        col_index = int((x_c - x_b) / w_s) + 1  # column_index equation in section 3.2

        if piece in fen_mapping:
            board[row_index, col_index] = fen_mapping[piece]  # Assign correct FEN character

    # Print the board while removing the first row and first column (index 0)
    print(board[1:, 1:])
      

    # Generate FEN notation
    fen_rows = []
    for row in range(8, 0, -1):  # Start from row 8 (top) to row 1 (bottom)
        empty_count = 0
        fen_row = ""

        for col in range(1, 9):  # Columns are left to right (file 'a' to 'h')
            cell = board[row, col]
            if cell == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)

        fen_rows.append(fen_row)

    # Join rows with "/" and add game metadata (Black to move)
    fen_string = "/".join(fen_rows) + " b - - 0 1"
    
    return fen_string

# Example usage:
fen = image_to_fen(image_path, model_path)
print(fen)
