# ===================================== #
# Author: Tran Nhat Hoang Nguyen
# Email: trannhat@ualberta.ca
# Comment: The game is designed in an OOP manner
# Technique: Using minimax tree
# ===================================== #

import os
import numpy as np

class Board:
    def __init__(self):
        '''
        Initialize a board. \n
        self.__board is an 8-bit unsigned integer matrix of shape (3,3). \n
        Note: self.__board is a private variable to avoid direct access. \n 
        '''
        
        self.__board = np.zeros(shape=(3,3), dtype='uint8') 

    def erase_board(self): 
        '''
        This function cleans the playing board. \n
        '''
        
        self.__board = np.zeros(shape=(3,3), dtype='uint8')

    def play(self, player, row_i, col_j): 
        '''
        This function allows player to make a move on the board. \n
        It also handles out-of-bound case and overwritten case. \n
        Return bool: \n
        True: Valid move \n
        False: Invalid move \n
        '''
        
        n_rows = self.__board.shape[0]
        n_cols = self.__board.shape[1]

        # Out of bound case
        if row_i < 0 or row_i > n_rows-1 or col_j < 0 or col_j > n_cols-1: 
            print('Incorrect coordinate, please try again!')
            return False
        
        # Overwritten case
        elif self.__board[row_i,col_j]: 
            print('Cannot play on this grid, please try again!')
            return False
        
        # Valid case
        else: 
            self.__board[row_i,col_j] = player
            return True 

    def check_board(self): 
        '''
        The game stops when one player win or no player win. \n
        Return int: \n
        0: The game is not over\n
        1: Player 1 win\n
        2: Player 2 win\n
        -1: No player win\n
        '''

        player_1_mask = (self.__board == 1)
        player_2_mask = (self.__board == 2)
        if self.__check(player_1_mask): # Player 1 win
            return 1
        if self.__check(player_2_mask): # Player 2 win
            return 2
        return 0 if np.any(self.__board == 0) else -1 # Game is not over or no one win

    def display_board(self):
        '''
        This function creates UI on terminal screen.
        '''

        print(' ', 0, 1, 2)
        for i in range(self.__board.shape[0]):
            print(i, end=' ')
            for j in range(self.__board.shape[1]):
                if self.__board[i,j] == 0:
                    print('+', end=' ')
                if self.__board[i,j] == 1:
                    print('o', end=' ')
                if self.__board[i,j] == 2:
                    print('x', end=' ')
            print()

    def __check(self, mask): 
        '''
        Private method \n
        When one row or column is True, it is True \n
        '''
        
        win = False
        for i in range(3):
            win |= np.all(mask[i,:]) # By row
            win |= np.all(mask[:,i]) # By col
        win |= np.all(mask.diagonal()) # Main diagonal
        win |= np.all(mask[:,::-1].diagonal()) # The other diagonal
        return win

    # --- API for an AI player ---
    def get_board(self):
        '''
        This function returns a copy of the board. \n
        Note: We cannot affect the board by modifying values on it directly. Therefore, a copy is returned. \n
        '''
        return self.__board.copy()

    def set_board(self, board):
        '''
        This function loads board states. \n
        '''
        self.__board = board 

class Agent:
    def __init__(self, player=2):
        self.player = player

    def read_board(self, board, player=2):
        '''
        Use Minimax Tree. \n
        Compute scores for every possible move. \n
        Time complexity O(8!). \n
        '''

        # Stop condition: when the game stops
        # ==================================== #
        tmp_board = Board()
        tmp_board.set_board(board)
        value = tmp_board.check_board()
        
        if value != 0: 
            if value == -1:
                score = 0
            elif value == self.player: # Agent win
                score = 1
            else: # Agent lose
                score = -1   
            return score, None

        # Recursion: Depth-first Search
        # ==================================== #
        possible_moves_row, possible_moves_col = np.where(board == 0)
        possible_moves = len(possible_moves_row)

        scores = []
        for i,j in zip(possible_moves_row, possible_moves_col):
            tmp_board = board.copy()
            tmp_board[i,j] = player
            score, _ = self.read_board(tmp_board, 1 if player==2 else 2)
            scores.append(score)

        # Maximize gain
        if self.player == player: 
            idx = np.argmax(scores)
            return np.max(scores), (possible_moves_row[idx], possible_moves_col[idx])
        # Minimize loss
        else: 
            idx = np.argmin(scores)
            return np.min(scores), (possible_moves_row[idx], possible_moves_col[idx])

if __name__ == "__main__":
    player_name = input('What is your name? ')
    print('Welcome {} to my tic-tac-toe game! Beat my A.I. if you can :-))'.format(player_name))

    ai_player = Agent()
    game = Board()

    game.display_board()
    player = 0

    while True:
        try:
            if player%2 == 0: # Human player
                row = int(input('Input row: '))
                col = int(input('Input col: '))
            else: # Agent player
                score, (row, col) = ai_player.read_board(game.get_board())
                print('A.I. move:', row, col)
            
            valid = game.play(player%2+1,row,col)

            # Only when the move is valid, switch to next player
            if valid:
                game.display_board()
                value = game.check_board()

                if value == 0:
                    player += 1
                    continue # Avoid the following commands

                elif value == -1:
                    print('No one win.')
                else:
                    print('Player {} win!!!'.format(value))

                
                answer = input('Do you want to play again? (y/n): ')
                if answer in ['y','1','yes']:
                    os.system('clear')
                    game.erase_board()
                    game.display_board()
                    player = 0
                else:
                    print('Thank you, {}, for playing. Bye bye!'.format(player_name))
                    break

        except ValueError as e:
            print('Bad input!')