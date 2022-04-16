

from time import *
from kandinsky import *
from random import *
from ion import keydown,KEY_UP,KEY_DOWN,KEY_LEFT,KEY_RIGHT

score=0
dx,dy=0,1
green,red=(0,252,0),(248,0,0)
snake=[[160,110],[150,110],[140,110]]
apple=True
pt=monotonic()
while True:
  ct=monotonic()
  dt=ct-pt
  if apple:
    fx=10*randint(0,31)
    fy=10*randint(0,21)
    apple=False
  fill_rect(fx,fy,10,10,red)
  if keydown(KEY_UP): dx,dy=0,-1
  if keydown(KEY_DOWN) : dx,dy=0,1
  if keydown(KEY_LEFT): dx,dy=-1,0
  if keydown(KEY_RIGHT): dx,dy=1,0
  if dt>0.2-0.02*v:
    pt=monotonic()
    x=snake[0][0]+10*dx
    y=snake[0][1]+10*dy
    if x<0 or x>310 or y<0 or y>210 or get_pixel(x,y)==green:
      fill_rect(x,y,10,10,rouge)
      gameover="Game over"
      fill_rect(0,0,320,222,(255,255,255))
      xl=110
      yl=105
      for i in range(9):
        draw_string(gameover[i],xl,yl,red)
        xl+=10
        sleep(0.05)
      return score
    snake.insert(0,[x,y])
    if get_pixel(x,y)!=rouge:
      q=snake.pop()
      fill_rect(q[0],q[1],10,10,(248,255,248))
    else:
      score+=1
      draw_string(str(score),5,10)
      apple=True
    fill_rect(snake[0][0],snake[0][1],10,10,vert)
