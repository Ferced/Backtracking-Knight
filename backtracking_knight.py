import time
import itertools
import pygame as pg

class KnightsTour():
    def __init__(self):
        pg.init()
        pg.font.init()
        self.running=True
        self.BLACK = pg.Color('black')
        self.WHITE = pg.Color('white')
        self.screen = pg.display.set_mode((800, 800))
        self.clock = pg.time.Clock()
        self.size=[8,8]
        self.time_between_moves = 1
        self.font = pg.font.SysFont("monospace", 40)
        self.font_small = pg.font.SysFont("monospace", 13)
        self.colors = itertools.cycle((self.WHITE, self.BLACK))
        self.tile_size = 70
        self.board_width, self.board_height = self.size[1]*self.tile_size, self.size[0]*self.tile_size
        self.background = pg.Surface((self.board_width, self.board_height))

    def start_pg(self):
        board = ([[-1 for x in range(1,self.size[1]+1)] for y in range(self.size[1])])
        y_counter = 0
        for row in board:
            x_counter=0
            for column in row:
                current_position = [y_counter,x_counter]
                cicle = 1
                self.next_position_draw(board,current_position,cicle,[])
                x_counter+=1
            y_counter+=1    

    def draw_tick(self,background):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        self.screen.fill((60, 70, 90))
        self.screen.blit(background, (100, 100))
        pg.display.flip()
        self.clock.tick(30)
        if self.running == False:
            pg.quit()
    
    def draw_square(self,background,y,x,square_color):
        rect = (x, y, self.tile_size, self.tile_size)
        pg.draw.rect(background,square_color, rect)   
        return background   

    def draw_board(self,current_position,history,posible_moves):
        for y in range(0, self.board_height, self.tile_size):
            for x in range(0, self.board_width, self.tile_size):

                #DIBUJO EL CUADRADO
                tile_position=[int(y/70),int(x/70)]
                tile_counter=(self.size[0]*int(y/70) + int(x/70))
                square_color = next(self.colors)
                
                #COLOREO LOS YA MARCADOS CON ROJO
                if tile_position in history:
                    square_color = (255,0,0)

                #COLOREO LOS POSIBLES MOVIMIENTOS CON VIOLETA
                if len(posible_moves) > 0 and tile_position in posible_moves:
                    square_color = (255,0,255)

                #COLOREO LA POSICION ACTUAL CON VERDE
                if current_position == tile_position:
                    square_color = (0,255,0)

                #COLOREO LA POSICION ANTERIOR CON AMARILLO
                if len(history)> 0 and tile_position == history[len(history)-1]:
                    square_color = (255,255,0)

                self.background = self.draw_square(self.background,y,x,square_color)

                #DIBUJO EL NUMERO
                color_text= self.BLACK if square_color == self.WHITE else self.WHITE
                text = self.font.render(str(tile_counter), True, color_text)
                self.background.blit(text, (x+24, y+15)) if tile_counter < 10 else self.background.blit(text, (x+10, y+10))
            
                if len(history)> 0 :
                    if tile_position in history:
                        color_text=  self.WHITE
                        text_history = self.font_small.render("("+str(history.index(tile_position)+1)+")", True, color_text)
                        self.background.blit(text_history, (x+5, y+5)) if history.index(tile_position)+1 < 10 else self.background.blit(text_history, (x+7, y+7))
            next(self.colors)
        self.draw_tick(self.background)

    #VALIDA QUE SE PUEDA SALTAR A ESA POSICION
    def jump_validation(self,board,move):
        for index in move:
            if int(index) < 0 or int(index) > self.size[0]-1:
                return False
        if board[move[0]][move[1]] != -1:
            return False
        return True
    
    def all_permutations(self,items):
        for p in itertools.permutations(items):
            for signs in itertools.product([-1,1], repeat=len(items)):
                yield [a*sign for a,sign in zip(p,signs)]

    #DEVUELVE LAS 8 POSIBILIDADES PARA MOVERSE
    def find_posible_moves(self,board,current_position):
        posible_moves_list = []
        for x in list(self.all_permutations([1,2])):
            posible_moves_list.append([current_position[0]+x[0],current_position[1]+x[1]])
        posible_moves_list = ([x for x in posible_moves_list if self.jump_validation(board,x)])
        return(posible_moves_list)

    #PRINTEA EL TABLERO
    def print_board(self,board_):
        for line in board_:
            print (line)
            
    #CHEQUEA SI EL TABLERO ESTA COMPLETO            
    def board_finished(self,board):
        for row in board:
            if -1 in row:
                return False
        return True

    #SE MUEVE A LA PROXIMA POSICION
    def next_position_draw(self,board,current_position,cicle,history):
        posible_moves  = self.find_posible_moves(board,current_position)
        self.draw_board(current_position,history,posible_moves)
        history.append(current_position)
        time.sleep(self.time_between_moves)
        board[current_position[0]][current_position[1]] = cicle
        counter=0
        while len(posible_moves)>0:
            result =self.next_position_draw([list(row) for row in board],posible_moves[counter],cicle+1,[row for row in history])
            if result == False:
                posible_moves.pop(counter)
                counter-=1
            counter+=1
        if self.board_finished(board):
            self.print_board(board)
            input()
        #SI NO HAY MAS MOVIMIENTOS POSIBLES
        if len(posible_moves) == 0:
            self.draw_board(current_position,history,posible_moves)
            time.sleep(self.time_between_moves)
            return (False) 

def main():
    Knight = KnightsTour()
    Knight.start_pg()

if __name__ == "__main__":
    main()