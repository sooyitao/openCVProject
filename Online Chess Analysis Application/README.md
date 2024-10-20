# Chess Analysis Application

A Python application that analyzes a chessboard using image processing and chess engine integration. This tool identifies chess pieces on a board, recognizes legal moves, and supports special moves like castling while preventing move repetition.

## Features

- **Chessboard Recognition**: Captures a screenshot and identifies the chessboard.
- **Piece Identification**: Recognizes and categorizes chess pieces using pre-defined templates.
- **FEN Generation**: Converts the identified pieces into a FEN (Forsyth-Edwards Notation) string to represent the board state.
- **Move Analysis**: Utilizes a chess engine to determine the best move based on the current board position.
- **Auto Move**: Utilizes pyautogui to move pieces.

## Requirements

- Python 3.x
- `pyautogui` for screenshot functionality
- `opencv-python` for image processing
- `python-chess` for chess logic and engine interaction
- A compatible chess engine (e.g., Stockfish)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sooyitao/openCVProject
   cd Online Chess Analysis Application

2. Install the required packages:

    ```bash
    pip install -r requirement.txt

## Usage

1. Run the application:
    ```bash
    python main.py
2. Ensure the chessboard is visible on your screen.
3. Press 'b' to analyze from the black perspective or 'w' for white.
4. The application will capture the chessboard, identify pieces, generate FEN, and move the best move.
