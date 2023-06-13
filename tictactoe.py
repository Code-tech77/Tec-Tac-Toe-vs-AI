import copy
import sys
import pygame
import random
import numpy as np

from constants import *

#IMPORT PYGAME LIBLARY settings 
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares #[squares]
        self.marked_sqrs = 0
        
    def final_state(self, show=False):

            #vertical win line
     for col in range(COLS):
             if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                 #draw wining line
                 if show:
                     color = CROSS_LINE if self.squares[0][col] == 2 else CROSS_LINE
                     iPos = (col * SQSIZE + SQSIZE // 2, 20)
                     fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                     pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

                     
                 return self.squares[0][col]
            
             #Horezintal win linw
     for row in range(ROWS):
             if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
              
              if show:
                    color = CROSS_LINE if self.squares[0][col] == 2 else CROSS_LINE
                    iPos = (20,row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2) 
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

                       
                    return self.squares[row][0]
             
        #desc digoanal
     if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                 
                  if show:
                      color = CROSS_LINE if self.squares[0][col] == 2 else CROSS_LINE
                      iPos = (20,20)
                      fPos = (WIDTH - 20, HEIGHT - 20)
                      pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                  return self.squares[1][1]
        
        #asc digoanal
     if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
             
               if show:
                      color = CROSS_LINE if self.squares[0][col] == 2 else CROSS_LINE
                      iPos = (20,HEIGHT - 20)
                      fPos = (WIDTH - 20, 20)
                      pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                      return self.squares[1][1]
        
        #No win Yet 
        
     return 0

        
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
        
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0

class AI:
   
    def __init__(self, level=1, player=2):
        self.level = level 
        self.player = player
        
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0,len(empty_sqrs))
        
        return empty_sqrs[idx] #(row, col)
    
    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
        
    #Main Eval
        
    def eval(self, main_board):
        if self.level == 0:
            # random AI choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
           eval, move = self.minimax(main_board, False)
           
        print(f'AI has Chosen to mark the square in pos {move} with an eval of: {eval}') 
        
        return move #rows and cols

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #1-cross #2-circles
        self.gamemode = 'ai' #person vs AI
        self.running = True
        self.show_lines()
        
    def make_move(self, row, col):
      self.board.mark_sqr(row, col, self.player)
      self.draw_fig(row, col)
      self.next_turn() 


    def show_lines(self):
        # Background
        screen.fill( BG_COLOR )
        #vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)


        #horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
        
    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross after wining
            # "X" right line 
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            
            # "X" left line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR  , start_asc, end_asc, CROSS_WIDTH)
        
        
        elif self.player == 2:
        #draw circle "O"
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
   
    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        if self.gamemode == 'pvp': 
            self.gamemode = 'ai'
        else: 
            self.gamemode = 'pvp'
            
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()
    
        
    def reset(self):
        self.__init__()

def main():
    #object
    game = Game()
    board = game.board
    ai = game.ai
    
    
    #mainloop
    while True:

        for event in pygame.event.get():

            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                
                #g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                    
                #restart key
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    
                #0-random choose ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                #1-random choose ai
                if event.key == pygame.K_1:
                    ai.level = 1    
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE
                    
                    #user settings
                    if board.empty_sqr(row, col) and game.running:
                       game.make_move(row, col)
                       
                       if game.isover():
                           game.running = False
                        
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #update the screen
            pygame.display.update()
            
            #AI settings
            row, col = ai.eval(board)
            game.make_move(row, col)
            
            if game.isover():
               game.running = False

                                  
        pygame.display.update()
main()