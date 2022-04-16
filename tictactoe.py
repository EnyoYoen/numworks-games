from kandinsky import *
from ion import *
from time import sleep

def case(column,row,color):  
  x=85+column*50+1
  y=30+row*50+1
  fill_rect(x,y,48,1,color)
  fill_rect(x,y,1,48,color)
  fill_rect(x+48,y,1,48+1,color)
  fill_rect(x,y+48,48,1,color)

def circle(c,r):
  px=85+c*50+25
  py=30+r*50+25
  color=(0,0,0)
  for x in range(1-23,23):
    h=int((23**2-x**2)**0.5)
    for y in range(1-h,h):
      set_pixel(px+x,py+y,color)
  color=(255,255,255)
  for x in range(1-21,21):
    h=int((21**2-x**2)**0.5)
    for y in range(1-h,h):
      set_pixel(px+x,py+y,color)

def cross(c,r):
  x=85+c*50+3
  y=30+r*50+3
  color=(0,0,0)
  for i in range(44):
    set_pixel(x+i,y+i,color)
    set_pixel(x+i+1,y+i,color)
    set_pixel(x+i+2,y+i,color)
    set_pixel(x+44-i,y+i,color)
    set_pixel(x+44-i+1,y+i,color)
    set_pixel(x+44-i+2,y+i,color)

def display():
  x=85
  y=30
  for i in range(2):
    fill_rect(x+50*(i+1),y+1,1,149,(0,0,0))
  for i in range(2):
    fill_rect(x+1,y+50*(i+1),149,1,(0,0,0))

def play(player):
  case(0,0,(0,0,255))
  column=0
  row=0
  while True:
    keyPressed=False
    oldColumn=column
    oldRow=row
    if keydown(KEY_RIGHT):
      column+=1
      column%=3
      keyPressed=True
    elif keydown(KEY_LEFT):
      column-=1
      column%=3
      keyPressed=True
    elif keydown(KEY_DOWN):
      row+=1
      row%=3
      keyPressed=True
    elif keydown(KEY_UP):
      row-=1
      row%=3
      keyPressed=True
    elif keydown(KEY_OK) or keydown(KEY_EXE):
      if gameMatrix[row][column]==0:
        gameMatrix[row][column]=player
        case(column,row,(255,255,255))
        if player==2:
          cross(column,row)
        else:
          circle(column,row)
        break

    if keyPressed:      
      case(column,row,(0,0,255))
      case(oldColumn,oldRow,(255,255,255))
    sleep(0.1)

def verification(player):
  symbole=player
  for i in range(3):
    if gameMatrix[i]==[symbole,symbole,symbole]:
      return True
  for i in range(3):
    if gameMatrix[0][i]==gameMatrix[1][i]==gameMatrix[2][i]==symbole:
      return True
  if gameMatrix[0][0]==gameMatrix[1][1]==gameMatrix[2][2]==symbole or gameMatrix[0][2]==gameMatrix[1][1]==gameMatrix[2][0]==symbole:
    return True
  return False

gameMatrix=[[0,0,0],[0,0,0],[0,0,0]]
end=False
display()
while not end:
  for i in [1,2]:
    play(i)
    
    full=True
    for i in range(3):
      for j in range(3):
        if gameMatrix[i][j]==0:
          full=False
          break
        
    if verification(i) or full:
      if full:
        draw_string("Equality",125,5)
      else:
        draw_string("The player "+str(i)+" won!",60,5)
      sleep(1)
      draw_string("Press OK or EXE to",30,178)
      draw_string("continue or BACK to quit.",5,203)
      backPressed=False
      while True:
        if keydown(KEY_BACK):
          backPressed=True
          break
        elif keydown(KEY_EXE) or keydown(KEY_OK):
          break
      if backPressed:
        end=True
        break
      gameMatrix=[[0,0,0],[0,0,0],[0,0,0]]
      fill_rect(60,8,200,20,(255,255,255))
      fill_rect(85,30,149,149,(255,255,255))
      fill_rect(5,178,315,45,(255,255,255))
      display()
    sleep(1)
