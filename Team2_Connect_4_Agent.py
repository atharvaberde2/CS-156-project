#! /usr/bin/Team1_Connect_4_Agent.py 

# IMPORTS
import random
import heapq
import copy

# HELPER FUNCTIONS
# Print the Board
def print_board(board):
    """ Prints the connect 4 game board."""
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (len(board[0]) * 2 + 1))
    print(' ' + ' '.join(str(i+1) for i in range(len(board[0]))))
    return

# No special initialization needed for agent
def init_agent(player_symbol, board_num_rows, board_num_cols, board):
    """
    Inits the agent. Should only need to be called once at the start of a game.
    """
    return True

"""
Search Algorithm here
"""
def a_star(board, rows, columns, my_char, opp_char):
    """
        Description: Implements the A* search algorithm to determine the optimal move.
        It explores possible game states by simulating moves, using a heuristic function
        to evaluate the desirability of board configurations. A priority queue is used
        to manage states to visit, prioritizing those with a better heuristic score
        combined with the cost (depth) to reach them. The search is limited by max_depth.
        Atharva Berde: 90% Designed and implemented first version of
        the function.
        Rajiv Mohan: 10% Tweaked this function with changes to depth checking and heapq.heappush
    """
    class Connect4State:
        def __init__(self, board, moves, cost):
            self.board = board  
            self.moves = moves
            self.cost = cost
            self.heuristic = heuristic(board, my_char, opp_char)
    
        def __lt__(self, other):
            return (self.cost + self.heuristic) < (other.cost + other.heuristic)
   
    def valid_cols(board):
        """We check the columns in which a move can be made. If the topmost cell of a column is empty, 
        then a valid move can be made in that particular column. """
        return [col for col in range(columns) if board[0][col] == ' ']                

    def apply_move(board, col, symbol):
        """When making a move, user chooses a col. Then we will start from the bottom and check if the cell 
        is empty. If not, we keep on moving up until there is an empty cell. If there is no empty cell, then we 
        return None since a move can't be made in that specific column. """
        new_board = copy.deepcopy(board)
        for row in reversed(range(rows)):
            if new_board[row][col] == ' ':
                new_board[row][col] = symbol
                return new_board
        return None

    start = Connect4State(board, [], 0) 
    states = [] 
    #store each state into a priority queue.
    heapq.heappush(states, (-(start.cost + start.heuristic), start)) 
    optimal_state = start
    max_depth = 4

    while states:
        #get the f(n) value and current state(lowest state)
        f_n, curr = heapq.heappop(states)   
        if len(curr.moves) >= max_depth:
            continue
        #explore all valid columns where move can be made
        for column in valid_cols(curr.board):
            board1 = apply_move(curr.board, column, my_char)
            if board1 is None:
                continue
            move1 = curr.moves + [column]
            cost1 = curr.cost + 1
            #new state with updated board after move
            state1 = Connect4State(board1, move1, cost1)  
            #push new state and its f(n) value to queue
            heapq.heappush(states, (-(state1.cost + state1.heuristic), state1)) 
            #update opitimal state
            if state1.heuristic > optimal_state.heuristic: 
                optimal_state = state1 

    if optimal_state.moves:         
        return optimal_state.moves[0] + 1
    else:
        valid_columns = [col+1 for col in range(columns) if board[0][col] == ' ']
        return random.choice(valid_columns)
    
"""
Reasoning Scheme and Rule Based Representation here
"""    
def forward_chaining_reasoning(board, game_rows, game_cols, my_game_symbol, opp_char, check_win):
    """
    Description: Implements a rule-based reasoning system to decide a move.
    Follows a strict order of rules:
    1. If a winning move is available for the agent, take it.
    2. If the opponent has an immediate winning move, block it.
    3. If the center column is available, take it.
    If none of these rules apply, it returns None, indicating no move was found by this method.
    Rajiv Mohan: 15% wrote out basic rules using rule based representation with pseudo-code
    Jimmy Valdez: 85% Designed and implemented first version of
    the function.
    """
    center_column = game_cols // 2

    # Rule 1: Win if possible
    for column in range(game_cols):
        if board[0][column] != ' ':
            continue
        temp_board = copy.deepcopy(board)
        for row in reversed(range(game_rows)):
            if temp_board[row][column] == ' ':
                temp_board[row][column] = my_game_symbol
                break
        if check_win(temp_board, my_game_symbol):
            return column

    # Rule 2: Block opponent win
    for column in range(game_cols):
        if board[0][column] != ' ':
            continue
        temp_board = copy.deepcopy(board)
        for row in reversed(range(game_rows)):
            if temp_board[row][column] == ' ':
                temp_board[row][column] = opp_char
                break
        if check_win(temp_board, opp_char):
            return column  

    # Rule 3: Take center column
    if board[0][center_column] == ' ':
        return center_column 

    return None


def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
    """
        Description: 
        Determines the agent's next move in the Connect 4 game.
        It first attempts to find a move using the `forward_chaining_reasoning` function,
        which applies a set of predefined rules (win, block, take center).
        If the forward chaining reasoning does not give a move, the agent
        falls back to using the "a_star" search algorithm to find the best
        possible move based on a heuristic evaluation of future game states.
    
        Rajiv Mohan: 90% Designed and implemented first version of
        the function with win checking
        Jimmy Valdez: 10% Tweaked this function with addition of forward chaining reasoning
    """
    import copy
    if my_game_symbol == 'X':
        opp_char = 'O'
    else:
        opp_char = 'X'
    
    # win checking
    def check_win(bd, symbol):
        rows, cols = len(bd), len(bd[0])

        # Horizontal win check
        for row in range(rows):
            for column in range(cols - 3):
                if all(bd[row][column + i] == symbol for i in range(4)):
                    return True
        # Vertical win check
        for col in range(cols):
            for row in range(rows - 3):
                if all(bd[row + i][column] == symbol for i in range(4)):
                    return True
        # Positive diagonal win check
        for row in range(rows - 3):
            for column in range(cols - 3):
                if all(bd[row + i][column + i] == symbol for i in range(4)):
                    return True
        # Negative diagonal win check
        for row in range(3, rows):
            for column in range(cols - 3):
                if all(bd[row - i][column + i] == symbol for i in range(4)):
                    return True
        return False

    #Use forward chaining reasoning
    move = forward_chaining_reasoning(board, game_rows, game_cols, my_game_symbol, opp_char, check_win)
    if move is not None:
        return move + 1
    
    #Otherwise, use A* Search Algorithm
    return a_star(board, game_rows, game_cols, my_game_symbol, opp_char)


def window_evaluation(window, my_char, opp_char):
    """
    Description: Assesses the strategic value of a 4-cell segment (or "window") on the game board. 
    It evaluates each window by counting how many cells are occupied by the agent (my_char),
    the opponent (opp_char), and how many are empty. Based on these counts, it assigns 
    a score reflecting how favorable or dangerous the window is. For example, if the agent 
    has three pieces and one empty cell in a window, it's a strong opportunity to win and 
    receives a high positive score. If the opponent has a similar setup, it 
    receives a large negative score to prioritize blocking it. This scoring guides the agent's 
    decision-making by helping the A* algorithm estimate which future board states are most 
    beneficial or need immediate attention.
    Swan Pyae Sone Tun: 100% Designed and implemented first version of
    the function.
    """
    score = 0
    my_count = window.count(my_char)
    opponent_count  = window.count(opp_char)
    empty_count = window.count(' ')

    if my_count == 4:
        score = 100000  # Our win
    elif opponent_count == 4:
        score = -200000 # Opponent's win - IMPORTANT TO BLOCK
    elif my_count == 3 and empty_count == 1:  #One more to win for us
        score = 1000
    elif opponent_count == 3 and empty_count == 1: #One more to win for opponent
        score = -5000 #A* to block this
    elif my_count == 2 and empty_count == 2:
        score = 100
    elif opponent_count == 2 and empty_count == 2:
        score = -200
    return score


def heuristic(board, my_char, opp_char):
    """
    Description: Evaluates the current game board by assigning a score 
    based on how favorable it is for the agent. It examines all possible 
    4-cell windows (horizontal, vertical, and diagonal) and uses the window_evaluation 
    function to assess each one. The scores are summed to produce a final value that guides 
    the agent in choosing moves that maximize its chances of winning while minimizing the opponent’s 
    opportunities.

    Swan Pyae Sone Tun: 25% Designed and implemented first version of function with vertical win check
    Rajiv Mohan: 75% Designed and implemented second version of function with horizontal, forward and backward diagonal win check
    """
    score = 0
    for i in range(len(board)):
        for j in range(len(board[0]) - 3):
            window = [board[i][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) # horizontal
    for j in range(len(board[0])):
        for i in range(len(board) - 3):
            window = [board[i+k][j] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #vertical
    for i in range(3, len(board)):
        for j in range(len(board[0]) - 3):
            window = [board[i-k][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #forward diagonal
    for i in range(len(board) - 3):
        for j in range(len(board[0]) - 3):
            window = [board[i+k][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #backward diagonal
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