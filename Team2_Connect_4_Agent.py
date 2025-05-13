#! /usr/bin/Team2_Connect_4_Agent.py 

# IMPORTS
import random
import heapq
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


def init_agent(player_symbol, board_num_rows, board_num_cols, board):
    """
    Inits the agent. Should only need to be called once at the start of a game.
    """
    # No special initialization needed for dummy agent
    return True

def a_star(board, rows, columns, my_char, opp_char):
    class Connect4State:
        def __init__(self, board, moves, cost):
            self.board = board
            self.moves = moves
            self.cost = cost
            self.heuristic = heuristic(board, my_char, opp_char)
        def __compare__(self, other):
            return (self.cost + self.heuristic) < (other.cost + other.heuristic)
     

    def valid_cols(board):
        return [col for col in range(columns) if board[0][col] == ' ']

    def apply_move(board, col, symbol):
        new_board = copy.deepcopy(board)
        for r in reversed(range(rows)):
            if new_board[r][col] == ' ':
                new_board[r][col] = symbol
                return new_board
        return None

    start = Connect4State(board, [], 0)
    states = []
    heapq.heappush(states, (start.cost + start.heuristic, start))
    optimal_state = start
    max_depth = 3

    while states:
        _, curr = heapq.heappop(states)
        if len(curr.moves) >= max_depth:
            continue
        for col in valid_cols(curr.board):
            board1 = apply_move(curr.board, col, my_char)
            if board1 is None:
                continue
            move1 = curr.moves + [col]
            cost1 = curr.cost + 1
            state1 = Connect4State(board1, move1, cost1)
            heapq.heappush(states, (state1.cost + state1.heuristic, state1))
            if state1.heuristic > optimal_state.heuristic:
                optimal_state = state1

    if optimal_state.moves:
        return optimal_state.moves[0] + 1
    else:
        valid_columns = [col+1 for col in range(columns) if board[0][col] == ' ']
        return random.choice(valid_columns)

def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
    import copy
    opp_char = 'O' if my_game_symbol == 'X' else 'X'

    # Inline win check
    def check_win(bd, symbol):
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
        # Positive diagonal
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(bd[r + i][c + i] == symbol for i in range(4)):
                    return True
        # Negative diagonal
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(bd[r - i][c + i] == symbol for i in range(4)):
                    return True
        return False

    # 1. Rule: Win if possible
    for col in range(game_cols):
        if board[0][col] != ' ':
            continue
        temp_board = copy.deepcopy(board)
        for r in reversed(range(game_rows)):
            if temp_board[r][col] == ' ':
                temp_board[r][col] = my_game_symbol
                break
        if check_win(temp_board, my_game_symbol):
            return col + 1

    # 2. Rule: Block opponent's win
    for col in range(game_cols):
        if board[0][col] != ' ':
            continue
        temp_board = copy.deepcopy(board)
        for r in reversed(range(game_rows)):
            if temp_board[r][col] == ' ':
                temp_board[r][col] = opp_char
                break
        if check_win(temp_board, opp_char):
            return col + 1

    # 3. Otherwise, use A*
    return a_star(board, game_rows, game_cols, my_game_symbol, opp_char)



def connect_4_result(board, winner, looser):
    """The Connect 4 manager calls this function when the game is over.
    If there is a winner, the team name of the winner and looser are the
    values of the respective argument variables. If there is a draw/tie,
    the values of winner = looser = 'Draw'."""

    # Check if a draw
    if winner == "Draw":
        print(">>> I am player TEAM2 <<<")
        print(">>> The game resulted in a draw. <<<\n")
        return True

    print(">>> I am player TEAM2 <<<")
    print("The winner is " + winner)
    if winner == "Team2":
        print("YEAH!!  :-)")
    else:
        print("BOO HOO HOO  :~(")
    print("The looser is " + looser)
    print()

    print("The final board is")   # Uncomment if you want to print the game board.
    # print(board)  # Uncomment if you want to print the game board.

    # Insert your code HERE to do whatever you like with the arguments.

    return True

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
            score += window_evaluation(window, my_char, opp_char) #forward diagonal
    for i in range(len(board) - 3):
        for j in range(len(board[0]) - 3):
            window = [board[i+k][j+k] for k in range(4)]
            score += window_evaluation(window, my_char, opp_char) #backward diagonal
    return score

#####
# MAKE SURE MODULE IS IMPORTED
if __name__ == "__main__":
   print("Team2_Connect_4_Agent.py  is intended to be imported and not executed.") 
else:
   print("Team2_Connect_4_Agent.py  has been imported.")
