#! /usr/bin/Team1_Connect_4_Agent.py 

# IMPORTS
import random
import copy
# DEFINITIONS
# board = [[' ' for _ in range(cols)] for _ in range(rows)]

# HELPER FUNCTIONS
# Print the Board
def print_board(board):
    """ Prints the connect 4 game board."""
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (len(board[0]) * 2 + 1))
    print(' ' + ' '.join(str(i+1) for i in range(len(board[0]))))
    return


def init_agent(player_symbol, board_num_rows, board_num_cols, board):
    """
    Inits the agent. Should only need to be called once at the start of a game.
    """
    # No special initialization needed for dummy agent
    return True

def check_win(bd, symbol):
    """Check if the given symbol has a winning position on the board"""
    rows, cols = len(bd), len(bd[0])
          
    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(bd[r][c + i] == symbol for i in range(4)):
                return True
                
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(bd[r + i][c] == symbol for i in range(4)):
                return True
                
    # Positive diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            diagonal = [bd[r + i][c + i] for i in range(4)]
            if all(bd[r + i][c + i] == symbol for i in range(4)):
                return True
                
    # Negative diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            diagonal = [bd[r - i][c + i] for i in range(4)]
            if all(bd[r - i][c + i] == symbol for i in range(4)):
                return True
                
    return False

def evaluate_position(bd, my_symbol, opp_symbol, depth):
    """Evaluate board position for minimax"""
    # Check if this is a winning position for either player
    if check_win(bd, my_symbol):
        return 1000 - depth  # Prefer winning sooner
    if check_win(bd, opp_symbol):
        return -1000 + depth  # Prefer losing later
        
    # Otherwise, use the heuristic to evaluate the position
    return heuristic(bd, my_symbol, opp_symbol)

def minimax_alpha_beta(bd, depth, is_maximizing, alpha, beta, my_symbol, opp_symbol, max_depth=4):
    """
    Minimax algorithm with alpha-beta pruning for Connect 4
    
    Parameters:
    - bd: Current board state
    - depth: Current depth in the search tree
    - is_maximizing: True if maximizing player's turn, False if minimizing
    - alpha: Alpha value for pruning
    - beta: Beta value for pruning
    - my_symbol: The symbol of our player ('X' or 'O')
    - opp_symbol: The symbol of the opponent
    - max_depth: Maximum depth to search
    
    Returns:
    - Score of the best move found
    """
    # Base cases: max depth reached or terminal state
    if depth == max_depth:
        return evaluate_position(bd, my_symbol, opp_symbol, depth)
        
    if check_win(bd, my_symbol):
        return 1000 - depth
        
    if check_win(bd, opp_symbol):
        return -1000 + depth
        
    # Check for draw
    if all(bd[0][c] != ' ' for c in range(len(bd[0]))):
        return 0
        
    # Maximizing player (our turn)
    if is_maximizing:
        max_eval = float('-inf')
        for col in range(len(bd[0])):
            if bd[0][col] != ' ':  # Skip full columns
                continue
                
            # Make move
            temp_board = copy.deepcopy(bd)
            for r in reversed(range(len(bd))):
                if temp_board[r][col] == ' ':
                    temp_board[r][col] = my_symbol
                    break
                    
            # Evaluate
            eval = minimax_alpha_beta(temp_board, depth + 1, False, alpha, beta, my_symbol, opp_symbol, max_depth)
            max_eval = max(max_eval, eval)
            
            # Alpha-beta pruning
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
                
        return max_eval
    
    # Minimizing player (opponent's turn)
    else:
        min_eval = float('inf')
        for col in range(len(bd[0])):
            if bd[0][col] != ' ':  # Skip full columns
                continue
                
            # Make move
            temp_board = copy.deepcopy(bd)
            for r in reversed(range(len(bd))):
                if temp_board[r][col] == ' ':
                    temp_board[r][col] = opp_symbol
                    break
                    
            # Evaluate
            eval = minimax_alpha_beta(temp_board, depth + 1, True, alpha, beta, my_symbol, opp_symbol, max_depth)
            min_eval = min(min_eval, eval)
            
            # Alpha-beta pruning
            beta = min(beta, eval)
            if beta <= alpha:
                break
                
        return min_eval

def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
    """
    Enhanced move selection strategy with minimax principles for better performance as second player
    """
    import copy
    opp_char = 'O' if my_game_symbol == 'X' else 'X'
    
    # IMPORTANT: First prioritize blocking opponent wins
    # Check if opponent can win in one move
    for col in range(game_cols):
        if board[0][col] != ' ':  # Skip full columns
            continue
        temp_board = copy.deepcopy(board)
        # Find where the piece would land
        for r in reversed(range(game_rows)):
            if temp_board[r][col] == ' ':
                temp_board[r][col] = opp_char
                break
        # Check if opponent would win here
        if check_win(temp_board, opp_char):
            return col + 1  # 1-indexed for game

    # Then check if we can win in one move
    for col in range(game_cols):
        if board[0][col] != ' ':  # Skip full columns
            continue
        temp_board = copy.deepcopy(board)
        # Find where the piece would land
        for r in reversed(range(game_rows)):
            if temp_board[r][col] == ' ':
                temp_board[r][col] = my_game_symbol
                break
        # Check if this is a winning move
        if check_win(temp_board, my_game_symbol):
            return col + 1  # 1-indexed for game

    # Use minimax to find the best move
    best_score = float('-inf')
    best_move = -1
    
    # Count pieces to adjust search depth
    piece_count = sum(row.count(my_game_symbol) + row.count(opp_char) for row in board)
    max_search_depth = 4  # Default depth
    
    # Adjust depth based on game stage
    if piece_count < 10:
        max_search_depth = 5  # Deeper search early game
    elif piece_count > 20:
        max_search_depth = 3  # Shallower search late game
    
    for col in range(game_cols):
        if board[0][col] != ' ':  # Skip full columns
            continue
            
        # Make move
        temp_board = copy.deepcopy(board)
        for r in reversed(range(game_rows)):
            if temp_board[r][col] == ' ':
                temp_board[r][col] = my_game_symbol
                break
                
        # Evaluate with minimax
        score = minimax_alpha_beta(temp_board, 0, False, float('-inf'), float('inf'), 
                                   my_game_symbol, opp_char, max_search_depth)
        
        # Update best move
        if score > best_score or (score == best_score and col == game_cols // 2):
            best_score = score
            best_move = col
            
    # If found a good move with minimax
    if best_move != -1:
        return best_move + 1
    
    # Fallback to center control
    center_col = game_cols // 2
    if board[0][center_col] == ' ':
        return center_col + 1
    
    # Last resort: random valid move
    valid_columns = [col+1 for col in range(game_cols) if board[0][col] == ' ']
    return random.choice(valid_columns)

def window_evaluation(window, my_char, opp_char):
    score = 0
    my_count = window.count(my_char)
    opp_count = window.count(opp_char)
    empty_count = window.count(' ')

    #Win
    if my_count == 4:
        score = 10000
    elif my_count == 3 and empty_count == 1:  #One more to win
        score = 100
    elif my_count ==2 and empty_count ==2:
        score = 10
    elif opp_count ==3 and empty_count == 1:
        score = -10000
    elif opp_count ==2 and empty_count == 2:
        score = -50
    return score

def heuristic(board, my_char, opp_char):
    score = 0
    for i in range(len(board)):
        for j in range(len(board[0]) - 3):
            window = [board[i][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char)   # horizontal
    for j in range(len(board[0])):
        for i in range(len(board) - 3):
            window = [board[i+k][j] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #vertical
    for i in range(3, len(board)):
        for j in range(len(board[0]) - 3):
            window = [board[i-k][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #forward diagnol
    for i in range(len(board) - 3):
        for j in range(len(board[0]) - 3):
            window = [board[i+k][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #backward diagnol
    return score

def connect_4_result(board, winner, looser):
    """The Connect 4 manager calls this function when the game is over.
    If there is a winner, the team name of the winner and looser are the
    values of the respective argument variables. If there is a draw/tie,
    the values of winner = looser = 'Draw'."""

    # Check if a draw
    if winner == "Draw":
        print(">>> I am player TEAM1 <<<")
        print(">>> The game resulted in a draw. <<<\n")
        return True

    print(">>> I am player TEAM1 <<<")
    print("The winner is " + winner)
    if winner == "Team1":
        print("YEAH!!  :-)")
    else:
        print("BOO HOO HOO  :~(")
    print("The looser is " + looser)
    print()

    print("The final board is") # Uncomment if you want to print the game board.
    #print(board)  # Uncomment if you want to print the game board.

    # Insert your code HERE to do whatever you like with the arguments.

    return True


#####
# MAKE SURE MODULE IS IMPORTED
if __name__ == "__main__":
   print("Team1_Connect_4_Agent.py  is intended to be imported and not executed.") 
else:
   print("Team1_Connect_4_Agent.py  has been imported.")
