import os
import sys
import cv2

try:
    from computer_vision_files.image_to_fen import image_to_fen
    from computer_vision_files.using_stockfish import get_best_move
    from robot_controller.robot_control import RobotController
except ImportError as e:
    print(f"Error: Failed to import a required module. {e}")
    print("Please ensure all subdirectories contain an '__init__.py' file and required packages are installed (run 'pip install -r requirements.txt').")
    sys.exit(1)


def capture_image(move_number: int = 1) -> str:
    """
    Captures an image from the default camera (index 0) and saves it.
    
    Args:
        move_number: The current move number, used for file naming.

    Returns:
        The file path to the captured image, or None if capture failed.
    """
    print("\nStep 1: Capturing image...")
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("  -> Error: Could not open camera.")
        return None
        
    # Read a frame
    ret, frame = cap.read()
    
    # Release the camera immediately
    cap.release()
    
    if not ret:
        print("  -> Error: Failed to capture frame.")
        return None
        
    # Ensure the directory exists
    output_dir = os.path.join("computer_vision_files", "moves_pictures")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Save the image
    image_filename = f"move_{move_number}.jpg"
    image_path = os.path.join(output_dir, image_filename)
    cv2.imwrite(image_path, frame)
    
    print(f"  -> Image captured and saved to: '{image_path}'")
    return image_path


def main():
    """
    Main function to orchestrate the chess robot pipeline.
    This function now includes a basic game loop and state management.
    """
    # --- Define and validate paths ---
    model_path = "Trained model/best.pt"
    stockfish_path = "Stockfish engine/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"

    if not os.path.exists(model_path):
        print(f"  -> Error: YOLOv8 model not found at '{model_path}'.")
        return

    # --- Initialize Game State ---
    # In a real game, this state would be loaded or initialized more dynamically.
    game_state = {
        "active_color": 'w',  # Start with white's turn
        "full_move_number": 1,
        # Castling and en-passant are complex and not handled yet
    }

    # --- Main Game Loop ---
    # This loop will run for each turn of the game. For now, we run one turn.
    while True:
        print(f"\n--- Turn {game_state['full_move_number']}: {game_state['active_color'].upper()}'s Move ---")

        # === STEP 1: CAPTURE IMAGE OF THE BOARD ===
        image_path = capture_image(move_number=game_state['full_move_number'])
        if not image_path:
            break  # Exit if no image is found

        # === STEP 2 & 3: GENERATE FEN STRING FROM IMAGE ===
        try:
            print("\nStep 2 & 3: Processing image and generating FEN string...")
            fen_string = image_to_fen(
                image_path,
                model_path,
                active_color=game_state['active_color']
            )
            print(f"  -> Generated FEN: {fen_string}")
        except ValueError as e:
            print(f"  -> Error during FEN generation: {e}")
            break
        except Exception as e:
            print(f"  -> An unexpected error occurred during image processing: {e}")
            break

        # === STEP 4: GET BEST MOVE FROM STOCKFISH ===
        if 'k' not in fen_string or 'K' not in fen_string:
            print(f"  -> Warning: FEN string '{fen_string}' is missing kings. Skipping Stockfish analysis.")
            print("  -> Possible causes: Camera captured an empty board, or model failed to detect pieces.")
            break

        try:
            print("\nStep 4: Calculating best move with Stockfish...")
            best_move = get_best_move(fen_string, stockfish_path)
            if best_move:
                print(f"  -> Best move found: {best_move}")
            else:
                print("  -> Stockfish did not return a move. Game may be over.")
                break
        except (FileNotFoundError, ValueError) as e:
            print(f"  -> Error during Stockfish analysis: {e}")
            break
        except Exception as e:
            print(f"  -> An unexpected error occurred while running Stockfish: {e}")
            break

        # === STEP 5 & 6: EXECUTE MOVE WITH ROBOT ===
        try:
            print("\nStep 5 & 6: Translating move and generating robot waypoints...")
            robot = RobotController()
            robot.execute_robot_move(best_move)
        except (FileNotFoundError, ValueError) as e:
            print(f"  -> Error during robot control step: {e}")
            break
        except Exception as e:
            print(f"  -> An unexpected error occurred during robot control: {e}")
            break

        # --- FOR NOW, WE'LL ONLY RUN ONE TURN ---
        print("\nSingle turn simulation completed successfully.")
        break

        # In a full game, you would update the game state here:
        # game_state['active_color'] = 'b' if game_state['active_color'] == 'w' else 'w'
        # if game_state['active_color'] == 'w':
        #     game_state['full_move_number'] += 1


if __name__ == "__main__":
    main()
