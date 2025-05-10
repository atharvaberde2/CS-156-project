#! /usr/bin/Team1_Connect_4_Agent.py 

# IMPORTS
import random
import heapq
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



# FUNCTIONS REQUIRED BY THE connect_4_main.py MODULE
def init_agent(player_symbol, board_num_rows, board_num_cols, board):
   """ Inits the agent. Should only need to be called once at the start of a game.
   NOTE NOTE NOTE: Do not expect the values you might save in variables to retain
   their values each time a function in this module is called. Therefore, you might
   want to save the variables to a file and re-read them when each function was called.
   This is not to say you should do that. Rather, just letting you know about the variables
   you might use in this module.
   NOTE NOTE NOTE NOTE: All functions called by connect_4_main.py  module will pass in all
   of the variables that you likely will need. So you can probably skip the 'NOTE NOTE NOTE'
   above. """
   num_rows = int(board_num_rows)
   num_cols = int(board_num_cols)
   game_board = board
   my_game_symbol = player_symbol
   return True

def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
   """ Decide your move, i.e., which column to drop a disk. """

   # Insert your agent code HERE to decide which column to drop/insert your disk.

   return random.randint(1, game_cols)

def a_star(board,rows,columns, my_char, opp_char):
    class Connect4State:
        def __init__(self, board, moves, cost):
            self.board = board
            self.moves = moves
            self.cost= cost 
            self.heuristic = heuristic(board, my_char, opp_char)    

        def valid_cols(board, row):
            return [col for col in range(len(board[0])) if board[0][col] == ' ']
        
        def apply_move(board, row, col, symbol):
            for r in reversed(range(rows)):
                if board[r][col] == ' ':
                    board[r][col] = symbol
                    return board
            return None
        start = Connect4State(board, [], 0)
        states = []
        heapq.heappush(states, (start.cost + start.heuristic, start))
        optimal_state = state

        while states:
            ss, curr = heapq.heappop(states)
            valid_cols = valid_cols(curr.board, rows)
            for col in valid_cols:
                board1 = apply_move(curr.board, rows, col, my_char)
                move1 = curr.moves + [col]
                cost1 = curr.cost + 1
                state1 = Connect4State(board1, move1, cost1)
                heapq.heappush(states, (state1.cost + state1.heuristic, state1))
                if state1.heuristic < start.heuristic:
                    optimal_state = state1
    return optimal_state.moves[0] + 1
            #use apply_move to make a move. if the heuristic is higher than the current optimal state, we update it.

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

    # print("The final board is") # Uncomment if you want to print the game board.
    # print(board)  # Uncomment if you want to print the game board.

    # Insert your code HERE to do whatever you like with the arguments.

    return True


#####
# MAKE SURE MODULE IS IMPORTED
if __name__ == "__main__":
   print("Team1_Connect_4_Agent.py  is intended to be imported and not executed.") 
else:
   print("Team1_Connect_4_Agent.py  has been imported.")
