import pygame
import random

pygame.init()

BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW =(255,255,0)
BLUE = (0,0,128)
GREEN = (0,255,0)
WHITE = (255,255,255)




WIDTH,HEIGHT = 600,600
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH+400,HEIGHT))
screen.fill(GREY)

clock = pygame.time.Clock()

def gen(num):
   return set([(random.randrange(0,GRID_HEIGHT),random.randrange(0,GRID_WIDTH))for _ in range(num)])



def drawtext(text,Size,text_col,x,y):

   font = pygame.font.SysFont("arialblack",Size)
   img = font.render(text, True, text_col)
   screen.blit(img,(x,y))


def randomcolour():
   R = random.randrange(0,255)
   G = random.randrange(0,255)
   B = random.randrange(0,255)

   return (R,G,B)
    

def draw_grid(positions):
   for position in positions:
      col, row = position
      top_left = (col*TILE_SIZE, row*TILE_SIZE)
      pygame.draw.rect(screen, YELLOW, (*top_left,TILE_SIZE,TILE_SIZE))     

   for row in range(GRID_HEIGHT+1):
      pygame.draw.line(screen,BLACK,(0,row*TILE_SIZE),(WIDTH,(row*TILE_SIZE)))
  
   for col in range(GRID_WIDTH+1):
      pygame.draw.line(screen,BLACK,((col*TILE_SIZE),0),((col*TILE_SIZE),HEIGHT))



      
def adjust_grid(positions):
    all_neighbours = set()
    new_positions = set()

    for position in positions:
       neighbours = get_neighbours(position)
       all_neighbours.update(neighbours)

       neighbours = list(filter(lambda x: x in positions,neighbours))

       if len(neighbours) in [2,3]:
          new_positions.add(position)

    for position in all_neighbours:
       neighbours = get_neighbours(position)
       neighbours = list(filter(lambda x: x in positions,neighbours))

       if len(neighbours) == 3:
          new_positions.add(position)

    return  new_positions   



     
  
def get_neighbours(pos):
    x,y = pos
    neighbours = []
    for dx in [-1, 0, 1]:
       if x+dx < 0 or x+dx > GRID_WIDTH+1:
          continue
          
       for dy in [-1, 0, 1]:
        if y+dy < 0 or y+dy > GRID_HEIGHT+1:
          continue

        if dx == 0 and dy == 0:
             continue
          
        neighbours.append((x+dx,y+dy))

    return neighbours   


def main():	
    running = True
    playing = False
    count = 0
    gen_num = 0
    update_freq = 60

    
    

    positions = set()
    positions.add((10, 10))
    while running:
      clock.tick(FPS)

      if playing:
         count += 1

      if count >= update_freq:
         count = 0
         gen_num +=1
         positions = adjust_grid(positions)  

      pygame.display.set_caption("Conway's Game of Life" if playing else "Game-Paused")  
      

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
             running = False 
          

          if event.type == pygame.MOUSEBUTTONDOWN:
             x, y = pygame.mouse.get_pos() 
             col = x // TILE_SIZE
             row = y // TILE_SIZE
             pos = (col,row)
          
             if pos in positions:
                
                positions.remove(pos)
             elif x<600 and y<600:
                positions.add(pos) 

          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                playing = not playing

             if event.key == pygame.K_c:
                positions=set()
                playing = False
                count = 0  
                             
             if event.key == pygame.K_r:
                positions = gen(random.randrange(2,5)*GRID_HEIGHT)
      screen.fill(GREY)
      drawtext("Conway's", 40, WHITE, 700, 25)
      drawtext("Game Of Life",30,WHITE,705,75)
      drawtext("c --- clear screen",15,GREEN,650,200)
      drawtext("r --- generate random initial positions",15,GREEN,650,220)
      drawtext("Space --- Play/Pause the game",15,GREEN,650,240)
      drawtext("[goes to next generation every second]",18,WHITE,610,300)
      drawtext("",15,WHITE,650,320)      
      draw_grid(positions)
      pygame.display.update()
      
    pygame.quit()	  


if __name__ == "__main__":
   main()
