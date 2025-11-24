import pandas as pd
import os

class RobotController:
    """
    Handles the conversion of chess moves to robot coordinates
    and simulates sending commands to the robot.
    """
    # Define a constant for the robot's home position, as seen in the notebook.
    HOME_COORDINATE = "[0.45; 0; 0.49]"

    def __init__(self, csv_path="robot_controller/Placement of pieces_csv.csv"):
        """
        Initializes the controller and loads the move mapping file.
        """
        if not os.path.exists(csv_path):
            # Attempt to construct path relative to this file if default fails
            # This makes it robust to being called from different working directories
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, "Placement of pieces_csv.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Robot coordinate mapping file not found at '{csv_path}'. "
                "Please ensure the path is correct."
            )
        
        # Clean up column names by stripping leading/trailing whitespace
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        self.df = df

    def get_move_coordinates(self, move: str):
        """
        Takes a move in UCI format (e.g., 'e2e4') and returns the
        physical pick-and-place coordinates from the CSV file.

        Args:
            move: The move to execute (e.g., 'a1b2').

        Returns:
            A tuple containing the pick coordinates and place coordinates as strings.
        """
        if len(move) < 4:
            raise ValueError(f"Invalid move format '{move}'. Expected format like 'e2e4'.")

        move_from = move[:2]
        move_to = move[2:4]

        try:
            # Get 'from' (pick) coordinates
            from_col = move_from[0]
            from_row = int(move_from[1])
            pick_coords_series = self.df.loc[(self.df['Col'] == from_col) & (self.df['Row'] == from_row)]['Pick']
            if pick_coords_series.empty:
                raise ValueError(f"Start square '{move_from}' not found in mapping file.")
            pick_coords = pick_coords_series.iloc[0]


            # Get 'to' (place) coordinates
            to_col = move_to[0]
            to_row = int(move_to[1])
            place_coords_series = self.df.loc[(self.df['Col'] == to_col) & (self.df['Row'] == to_row)]['Place']
            if place_coords_series.empty:
                raise ValueError(f"End square '{move_to}' not found in mapping file.")
            place_coords = place_coords_series.iloc[0]


        except (KeyError, IndexError):
            raise ValueError(f"Could not find coordinates for move '{move}' in the CSV file.")

        return pick_coords, place_coords

    def execute_robot_move(self, move: str):
        """
        Calculates the waypoints for the robot arm and prints the final command array.
        This simulates the final output to be sent to the Simulink controller.
        """
        try:
            pick_coords, place_coords = self.get_move_coordinates(move)

            # Construct the waypoints array as the final command for Simulink
            waypoints = [
                pick_coords,
                pick_coords,
                self.HOME_COORDINATE,
                place_coords,
                place_coords,
                self.HOME_COORDINATE
            ]

            print("\n--- Robot Control Final Command ---")
            print(f"Move: {move}")
            print("Final Waypoints Array for Simulink:")
            print(waypoints)
            print("-----------------------------------")

        except (ValueError, FileNotFoundError) as e:
            print(f"Error in robot control: {e}")

