import pyautogui
import chess
import chess.engine
import tkinter as tk
import threading

from utils import find_chessboard, cut_squares, load_piece_templates, save_piece_templates, identify_all_pieces, get_fen_from_pieces

def save_template():
    screenshot = pyautogui.screenshot()
    chessboard, chessboard_coords = find_chessboard(screenshot)
    if chessboard is not None:
        squares, board_coordinates = cut_squares(chessboard, chessboard_coords)
        save_piece_templates(squares)
        return("Template saved")
    else:
        print("Chessboard not found")
        return None


def analyze_chessboard(is_black = False):
    try:
        screenshot = pyautogui.screenshot()
        chessboard, chessboard_coords= find_chessboard(screenshot)
        
        if chessboard is not None:
            squares, board_coordinates = cut_squares(chessboard, chessboard_coords)
            piece_templates = load_piece_templates()
            pieces_on_board = identify_all_pieces(squares, piece_templates)
            
            board_array = []
            row_pieces = []
            for i, piece in enumerate(pieces_on_board):
                row = i // 8
                col = i % 8 
                row_pieces.append(piece) 
                if col == 7:
                    board_array.append(row_pieces)
                    row_pieces = []
            
            FEN = get_fen_from_pieces(board_array, is_black)
            print(f"FEN: {FEN}")
            board = chess.Board(FEN)
            engine = chess.engine.SimpleEngine.popen_uci("Online Chess Analysis Application/stockfish/stockfish-windows-x86-64-avx2.exe")
            result = engine.play(board, chess.engine.Limit(time=2.0))
            print(f"Best move: {result.move}")
            make_move(result.move, board_coordinates)
            engine.quit()
            return result.move
        else:
            print("Chessboard not found")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
def on_key_press(event):
    if not loading:
        if event.char == 'b': 
            set_loading(True)
            threading.Thread(target=start_analysis, args=(True,)).start()
        elif event.char == 'w':
            set_loading(True)
            threading.Thread(target=start_analysis, args=(False,)).start()
        elif event.char == '`':
            set_loading(True)
            threading.Thread(target=start_save).start()

def start_analysis(is_black):
    move = analyze_chessboard(is_black)
    if move:
        result_label.config(text=f"Best Move for {'Black' if is_black else 'White'}: {move}")
    else:
        result_label.config(text="Chessboard not found or error occurred")
    set_loading(False)
    root.focus_force()

def start_save():
    result = save_template()
    if result:
        result_label.config(text=result)
    else:
        result_label.config(text="Chessboard not found or error occurred")
    set_loading(False)

def set_loading(is_loading):
    global loading
    loading = is_loading
    if is_loading:
        result_label.config(text="Loading, please wait...")
        root.unbind('<KeyPress>')
    else:
        root.bind('<KeyPress>', on_key_press)
        root.focus_force()

def make_move(move, board_coordinates):
    start_square = chess.square_name(move.from_square)
    end_square = chess.square_name(move.to_square)
    start_coords = board_coordinates[start_square]
    end_coords = board_coordinates[end_square]
    pyautogui.moveTo(start_coords[0], start_coords[1], duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(end_coords[0], end_coords[1], duration=0.5)
    pyautogui.click()

root = tk.Tk()
root.title("Chess Analyzer")

loading = False

root.attributes('-topmost', True)

root.geometry('400x60')
root.resizable(False, False)

result_label = tk.Label(root, text="Press 'b' for Black or 'w' for White", font=("Helvetica", 14))
result_label.pack(pady=20)

root.bind('<KeyPress>', on_key_press)

root.mainloop()