import cv2
import numpy as np
import pyautogui
import os
import chess
import chess.engine

def is_square(contour, epsilon=0.02, min_side_length=30, side_length_tolerance=0.1):
    approx = cv2.approxPolyDP(contour, epsilon * cv2.arcLength(contour, True), True)

    if len(approx) == 4:
        side_lengths = []
        for i in range(4):
            side = np.linalg.norm(approx[i][0] - approx[(i+1) % 4][0])
            side_lengths.append(side)

        avg_side_length = np.mean(side_lengths)
        if all(abs(side - avg_side_length) <= side_length_tolerance * avg_side_length for side in side_lengths):
            if avg_side_length >= min_side_length:
                return True
    return False

def find_chessboard(pil_image, min_side_length=100):
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresh, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    largest_square_contour = None
    largest_area = 0
    for contour in contours:
        if is_square(contour, min_side_length=min_side_length):
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_square_contour = contour

    if largest_square_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_square_contour)
        chessboard = image[y:y+h, x:x+w]
        return remove_background(chessboard)

def cut_squares(chessboard):
    height, width = chessboard.shape[:2]

    square_width = width // 8
    square_height = height // 8

    squares = []

    for row in range(8):
        for col in range(8):
            x_start = col * square_width
            y_start = row * square_height
            x_end = x_start + square_width
            y_end = y_start + square_height

            square = chessboard[y_start:y_end, x_start:x_end]
            squares.append(square)

    return squares

def save_piece_templates(squares, output_dir="piece_templates"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cv2.imwrite(os.path.join(output_dir, 'white_pawn.jpg'), squares[55])
    cv2.imwrite(os.path.join(output_dir, 'black_pawn.jpg'), squares[9])
    cv2.imwrite(os.path.join(output_dir, 'white_knight.jpg'), squares[62])
    cv2.imwrite(os.path.join(output_dir, 'black_knight.jpg'), squares[1])
    cv2.imwrite(os.path.join(output_dir, 'white_bishop.jpg'), squares[61])
    cv2.imwrite(os.path.join(output_dir, 'black_bishop.jpg'), squares[2])
    cv2.imwrite(os.path.join(output_dir, 'white_rook.jpg'), squares[63])
    cv2.imwrite(os.path.join(output_dir, 'black_rook.jpg'), squares[0])
    cv2.imwrite(os.path.join(output_dir, 'white_queen.jpg'), squares[59])
    cv2.imwrite(os.path.join(output_dir, 'black_queen.jpg'), squares[3])
    cv2.imwrite(os.path.join(output_dir, 'white_king.jpg'), squares[60])
    cv2.imwrite(os.path.join(output_dir, 'black_king.jpg'), squares[4])

def load_piece_templates():
    template_directory = 'piece_templates/'
    piece_templates = {
        'P': cv2.imread(template_directory + 'white_pawn.jpg'),
        'p': cv2.imread(template_directory + 'black_pawn.jpg'),
        'N': cv2.imread(template_directory + 'white_knight.jpg'),
        'n': cv2.imread(template_directory + 'black_knight.jpg'),
        'B': cv2.imread(template_directory + 'white_bishop.jpg'),
        'b': cv2.imread(template_directory + 'black_bishop.jpg'),
        'R': cv2.imread(template_directory + 'white_rook.jpg'),
        'r': cv2.imread(template_directory + 'black_rook.jpg'),
        'Q': cv2.imread(template_directory + 'white_queen.jpg'),
        'q': cv2.imread(template_directory + 'black_queen.jpg'),
        'K': cv2.imread(template_directory + 'white_king.jpg'),
        'k': cv2.imread(template_directory + 'black_king.jpg'),
    }
    return piece_templates

def identify_piece(square, piece_templates, threshold=0.8):
    
    for piece_name, template in piece_templates.items():
        resized_template = cv2.resize(template, (square.shape[1], square.shape[0]))
        result = cv2.matchTemplate(square, resized_template, cv2.TM_CCOEFF_NORMED)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            return piece_name

    return None

def identify_all_pieces(squares, piece_templates):
    pieces_on_board = []
    for i, square in enumerate(squares):
        piece_name = identify_piece(square, piece_templates)
        pieces_on_board.append(piece_name if piece_name else "empty")

    return pieces_on_board

def remove_background(myimage):
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
    
    ret,baseline = cv2.threshold(myimage_grey,127,255,cv2.THRESH_TRUNC)

    ret,background = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY)

    ret,foreground = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY_INV)

    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)

    finalimage = background + foreground
    
    return finalimage

def get_fen_from_pieces(pieces, black = False):
    fen_rows = []
    for row in pieces:
        fen_row = ''
        empty_count = 0
        for square in row:
            if square == 'empty':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += square
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    if black:
        return '/'.join(fen_rows) + " b"
    return '/'.join(fen_rows)

screenshot = pyautogui.screenshot()
chessboard = find_chessboard(screenshot)
if chessboard is not None:
    squares = cut_squares(chessboard)
    #save_piece_templates(squares)
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
    FEN = get_fen_from_pieces(board_array)
    print(FEN)
    engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-windows-x86-64-avx2.exe")
    board = chess.Board(FEN)
    result = engine.play(board, chess.engine.Limit(time=2.0))
    print(f"Best move: {result.move}")
    engine.quit()
else:
    print("Chessboard not found")