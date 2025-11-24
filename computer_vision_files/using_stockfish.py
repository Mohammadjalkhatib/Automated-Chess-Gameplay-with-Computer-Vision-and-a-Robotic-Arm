from stockfish import Stockfish

def get_best_move(fen_string: str, stockfish_path: str) -> str:
    """
    Uses the Stockfish engine to find the best move for a given FEN position.

    Args:
        fen_string: The board position in FEN notation.
        stockfish_path: The file path to the Stockfish engine executable.

    Returns:
        The best move in UCI (Universal Chess Interface) format (e.g., 'e2e4').
        Returns None if the move cannot be determined.
    """
    try:
        # It's recommended to set the skill level and thinking time for consistent results.
        parameters = {
            "Threads": 2,
            "Minimum Thinking Time": 100,
            "Skill Level": 20, # Max skill level
        }
        stockfish = Stockfish(path=stockfish_path, parameters=parameters)

    except Exception as e:
        raise FileNotFoundError(
            f"Stockfish engine not found or failed to initialize at '{stockfish_path}'. "
            f"Please ensure the path is correct. Error: {e}"
        )

    if not stockfish.is_fen_valid(fen_string):
        raise ValueError(f"Invalid FEN string provided to Stockfish: {fen_string}")

    stockfish.set_fen_position(fen_string)

    # Give the engine 2000ms (2 seconds) to think. Adjust as needed.
    best_move = stockfish.get_best_move_time(2000)

    return best_move