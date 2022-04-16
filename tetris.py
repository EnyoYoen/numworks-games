from ion import keydown,KEY_UP,KEY_DOWN,KEY_RIGHT,KEY_LEFT,KEY_EXE,KEY_OK
from random import randint
from kandinsky import fill_rect,get_pixel,draw_string
from time import sleep,monotonic
from math import floor

colors=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)]

tetrimino_o=[[1,1],[1,1]]
tetrimino_t=[[1,1,1],[0,1,0],[0,0,0]]
tetrimino_z=[[1,1,0],[0,1,1],[0,0,0]]
tetrimino_s=[[0,1,1],[1,1,0],[0,0,0]]
tetrimino_l=[[1,1,1],[1,0,0],[0,0,0]]
tetrimino_j=[[1,1,1],[0,0,1],[0,0,0]]
tetrimino_i=[[1,1,1,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

listTetrimino=[tetrimino_o,tetrimino_t,tetrimino_z,tetrimino_s,tetrimino_l,tetrimino_j,tetrimino_i]

xCorner=110
yCorner=10
x=150
y=10

def square(x,y,color):
  fill_rect(x,y,10,10,color)

def reset(tetrimino):
  apparition(tetrimino,True) 

def apparition(tetrimino,reset=False):
  if reset:
    color=(248,252,248)
  else:
    color=actualColor
  for i in range(len(tetrimino)):
    for j in range(len(tetrimino)):
      if tetrimino[j][i] == 1:
        square(x+10*i,y+10*j,color)

def chooseTetrimino():
  global x,y
  tetrimino=listTetrimino[randint(0,len(listTetrimino)-1)]
  x=150-(len(tetrimino)//2)*10
  y=10
  return tetrimino

def verification(tetriminoCoords,movement):
  hShift=0
  vShift=0
  if movement == "Right":
    hShift=1
  elif movement == "Left":
    hShift=-1
  elif movement == "None":
    vShift=1
  else:
    return True
  l=len(tetriminoCoords)
  if hShift:
    if hShift>0:
      r=range(l-1,-1,-1)
    else:
      r=range(l)
    for i in range(l):
      for j in r:
        if tetriminoCoords[i][j]:
          if get_pixel(x+(j+hShift)*10,y+i*10) != (248,252,248):
            return False
          break
    return True
  elif vShift:
    for i in range(l):
      for j in range(l-1,-1,-1):
        if tetriminoCoords[j][i]:
          if get_pixel(x+i*10,y+(j+1)*10) != (248,252,248):
            return False
          break
    return True

def verificationNewTetrimino(tetriminoCoords):
    for i in range(len(tetriminoCoords)):
        for j in range(len(tetriminoCoords)):
            if tetriminoCoords[i][j] == 1 and gameMatrix[(y-yCorner)//10+j][(x-xCorner)//10+i] == 1:
                return False
    return True

def newCoords(tetriminoCoords,movement):
  if movement == "Right" or movement == "Left":
    if movement == "Right":
      shift=10
    else:
      shift=-10
    global x
    x += shift
  elif movement == "Down" or movement == "Up":
    l=len(tetriminoCoords)
    if l!=2:
      temp=[[0 for j in range(l)]for i in range(l)]
      for i in range(3):
        for i in range(l):
          for j in range(l):
            temp[i][j]=tetriminoCoords[j][l-i-1]
      tetriminoCoords=temp
  elif movement == "None":
    global y
    y += 10

  return tetriminoCoords

def gameOver():
  fill_rect(110,10,100,200,(248,252,248))
  continuing=False
  gameover="Game over"
  xl=115
  yl=111
  for i in range(9):
    draw_string(gameover[i],xl,yl,(255,0,0))
    xl+=10
    sleep(0.05)

continuing=True
tInGame=False
speed=5
score=0
tStart=0
tEnd=0
actualTetrimino=None
actualColor=None
gameMatrix=[[0 for i in range(10)] for i in range(20)]

fill_rect(0,0,320,222,(127,127,127))
fill_rect(110,10,100,200,(248,252,248))

while continuing:
  t=monotonic()
  key=None
  sleep(0.5/speed)
  while True:
    if (monotonic()-t)>=1/speed-(tEnd-tStart-0.5/speed):
      break
    else:
      if keydown(KEY_RIGHT): key=KEY_RIGHT
      elif keydown(KEY_LEFT): key=KEY_LEFT
      elif keydown(KEY_UP): key=KEY_UP
      elif keydown(KEY_DOWN): key=KEY_DOWN
      elif keydown(KEY_OK): key=KEY_OK
  
  tStart=monotonic()
  if not tInGame:
    actualTetrimino=chooseTetrimino()
    if not(verificationNewTetrimino(actualTetrimino)):
      gameOver()
      continuing=False
      continue 
    actualColor=colors[randint(0,len(colors)-1)]
    for i in range(len(actualTetrimino)):
      for j in range(len(actualTetrimino)):
        if actualTetrimino[j][i]:
          square(x+i*10,y+j*10,actualColor)
    tInGame=True
    tEnd=monotonic()
    continue

  if key==KEY_RIGHT or key==KEY_LEFT or key==KEY_UP or key==KEY_DOWN or key==KEY_OK:
    if key==KEY_RIGHT:
      movement="Right"
    elif key==KEY_LEFT:
      movement="Left"
    else:
      movement="Up"
    if verification(actualTetrimino,movement):
      reset(actualTetrimino)
      actualTetrimino=newCoords(actualTetrimino,movement)
      apparition(actualTetrimino)
      tEnd=monotonic()
      continue
  if verification(actualTetrimino,"None"):
    reset(actualTetrimino)
    actualTetrimino=newCoords(actualTetrimino,"None")
    apparition(actualTetrimino)
  else:
    for i in range(len(actualTetrimino)):
      for j in range(len(actualTetrimino)):
        if actualTetrimino[i][j]:
          gameMatrix[(y-yCorner)//10+i][(x-xCorner)//10+j]=1
    tInGame=False
    
    for i in range(20):
      compteur=0
      for j in range(10):
        if gameMatrix[i][j] == 1:
          compteur += 1
        if compteur == 10:
          score += 1
          draw_string(str(score),5,5)
          for j in range(i,20-i,-1):
            for k in range(10):
              gameMatrix[j][k]=gameMatrix[j-1][k]
              square(xCorner+k*10,yCorner+j*10,get_pixel(xCorner+k*10,yCorner+(j-1)*10))
  tEnd=monotonic()
