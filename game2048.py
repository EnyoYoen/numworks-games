from kandinsky import fill_rect,draw_string
from ion import keydown
from time import monotonic,sleep
from random import randint
from math import log2

fill_rect(0,0,320,222,(127,127,127))
fill_rect(80,31,160,160,(255,255,255))

colors=[(255,255,0),(255,170,0),(255,85,0),(255,0,0),(255,0,85),(255,0,170),(255,0,255),(85,0,255),(170,0,255),(0,0,255),(0,85,170),(0,170,85),(0,255,0)]
matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
spawnScores=[1,1,2]

def item(x,y,score):
  if score:
    fill_rect(80+x*40,31+y*40,40,40,colors[int(log2(score))])
    draw_string(str(score),95+x*40,41+y*40,(0,0,0),colors[int(log2(score))])
  else:
    fill_rect(80+x*40,31+y*40,40,40,(255,255,255))

def slide(m):
  s=False
  if m==1 or m==2:
    if m==1:
      r=range(4)
      v=0
      a=1
    else:
      r=range(3,-1,-1)
      v=3
      a=-1
    for i in range(4):
      c=v
      l=[]
      for j in r:
        if matrix[j][i]:
          if j!=v:
            if c!=v and matrix[c-a][i]==matrix[j][i]:
              f=False
              for k in l:
                if (k[0],k[1])==(c-a,i):
                  f=True
              if not(f):
                matrix[c-a][i]*=2
                matrix[j][i]=0
                l.append((c-a,i))
                item(i,j,0)
                item(i,c-a,matrix[c-a][i])
                s=True
                continue
            if j!=c:
              matrix[c][i]=matrix[j][i]
              matrix[j][i]=0
              item(i,j,0)
              item(i,c,matrix[c][i])
              s=True
          c+=a
  else:
    if m==0:
      r=range(4)
      v=0
      a=1
    else:
      r=range(3,-1,-1)
      v=3
      a=-1
    for i in range(4):
      c=v
      l=[]
      for j in r:
        if matrix[i][j]:
          if j!=v:
            if c!=v and matrix[i][c-a]==matrix[i][j]:
              f=False
              for k in l:
                if (k[0],k[1])==(i,c-a):
                  f=True
              if not(f):
                matrix[i][c-a]*=2
                matrix[i][j]=0
                l.append((i,c-a))
                item(c-a,i,matrix[i][c-a])
                item(j,i,0)
                s=True
                continue
            if j!=c:
              matrix[i][c]=matrix[i][j]
              matrix[i][j]=0
              item(j,i,0)
              iteù(c,i,matrix[i][c])
              s=True
          c+=a
  return s

def empty():
  pos=[]
  for i in range(4):
    for j in range(4):
      if matrix[i][j]==0:
        pos.append((i,j))
  return pos

def spawn(pos=None):
  s=spawnScores[randint(0,2)]
  if pos==None:
    c=(randint(0,3),randint(0,3))
  else:
    if len(pos)==0:
      return False
    c=pos[randint(0,len(pos)-1)]
  item(c[1],c[0],s)
  matrix[c[0]][c[1]]=s
  return True

def gameOver():
  fill_rect(80,31,160,160, (255,255,255))
  gameover="Game over"
  xl=115
  yl=101
  for i in range(9):
    draw_string(gameover[i],xl,yl,(255,0,0))
    xl+=10
    sleep(0.05)

spawn()
spawn()
while True:
  s=False
  if not s:sleep(0.25)
  m=None
  while True:
    if keydown(0):m=0
    elif keydown(1):m=1
    elif keydown(2):m=2
    elif keydown(3):m=3
    if m!=None:
      break

  s=slide(m)
  p=empty()
  if len(p):
    if s:
      apparition(p)
  else:
    gameOver()
