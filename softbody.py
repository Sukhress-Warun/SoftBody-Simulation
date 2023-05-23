import sys
import pygame,os
from pygame.locals import *
import random
from color import * 

class spring():
	def __init__(self,obj1,obj2,k,ox):
		self.k=k
		self.ox=ox
		self.obj1=obj1
		self.obj2=obj2
	def force_to_objects(self):
		dx=self.obj1.x-self.obj2.x
		dy=self.obj1.y-self.obj2.y
		length=((dx**2)+(dy**2))**0.5
		if length!=0:
			f=-1*self.k*(length-self.ox)
			dx/=length
			dy/=length
			dx*=f
			dy*=f
			self.obj1.applyforce(dx,dy)
			self.obj2.applyforce(-dx,-dy)
	def display(self):
		dx=self.obj1.x-self.obj2.x
		dy=self.obj1.y-self.obj2.y
		length=((dx**2)+(dy**2))**0.5
		c=(length/self.ox)*0.5
		if c>1:
			c=1
		pygame.draw.line(surface,cb.getcolor(c),(self.obj1.x,self.obj1.y),(self.obj2.x,self.obj2.y))

class object():
	def __init__(self,p,s,c,xv,yv=0):
		self.x=p[0]
		self.y=p[1]
		self.s=s
		self.c=c
		self.xv=xv
		self.yv=yv
	def applyforce(self,x,y):
		self.xv+=x
		self.yv+=y
	def speed(self):
		l=(self.xv**2+self.yv**2)**0.5
		if l>150:
			self.xv/=l
			self.yv/=l
			l=150
			self.xv*=l
			self.yv*=l
		if l!=0:
			self.xv/=l
			self.yv/=l
			if l>60:
				l*=0.90
			else:
				l*=0.95
			self.xv*=l
			self.yv*=l
		self.x+=self.xv
		self.y+=self.yv	
		ff=-0.99
		if(self.x>=w-self.s):
			self.xv*=ff
			self.x=w-self.s
		elif(self.x<=self.s):
			self.xv*=ff
			self.xv=self.s
		if(self.y>=h-self.s):
			self.yv*=ff
			self.y=h-self.s
		elif(self.y<=self.s):
			self.yv*=ff
			self.y=self.s
	def display(self):
		pygame.draw.circle(surface,tuple(self.c),(self.x,self.y),self.s)

def r(n,s=0):
	return random.randrange(int(s),int(n))

def ro(n,m=None):
	if m==None:
		for i in range(n):
			obj=object((r(w-w*0.25,w*0.25),r(h-h*0.35,h*0.35)),r(15,10),[r(250,100),r(250,100),r(250,100)],r(8,-7),r(8,-7))
			objl.append(obj)
	else:
		col=0.40/m
		row=0.60/n
		for i in range(n):
			for j in range(m):
				obj=object((w*(0.30+col*j),h*(0.20+row*i)),r(15,10),[r(250,100),r(250,100),r(250,100)],r(8,-7),r(8,-7))
				objl.append(obj)

def spring_objs(ind1,ind2):
	dx=objl[ind1].x-objl[ind2].x
	dy=objl[ind1].y-objl[ind2].y
	length=((dx**2)+(dy**2))**0.5
	springs.append(spring(objl[ind1],objl[ind2],0.1,length))

def in_range(i,j):
	if i>=0 and i<ROW and j>=0 and j<COL:
		return True
	else:
		return False


os.environ['SDL_VIDEO_CENTERED'] = '1' 
pygame.init()
info = pygame.display.Info()
w,h= info.current_w-100,info.current_h-100
surface = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

cb=color_band([(0,0,255),(0,0,255),(150,150,150),(255,0,0),(255,0,0)])
objl=[]
ROW,COL=(4,4)
n=ROW*COL
posi=None
hold=None
ro(ROW,COL)

springs = []
for i in range(ROW):
	for j in range(COL):
		for offx,offy in [(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-2),(0,-1),(0,1),(0,2),(1,-2),(1,-1),(1,0),(1,1),(1,2),(2,-2),(2,-1),(2,0),(2,1),(2,2)]:
			if in_range(i+offx,j+offy):
				spring_objs(i*COL+j,(offx+i)*COL+j+offy)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	if(pygame.mouse.get_pressed()[0]):
		posi=pygame.mouse.get_pos()
	else:
		posi=None
		if hold:
			hold.xv=0
			hold.yv=0
		hold=None
	
	surface.fill((0,0,0))
	for i in springs:
		i.force_to_objects()
	if posi and hold:
		hold.x=posi[0]
		hold.y=posi[1]
	for i in objl:
		if posi and not hold:
			templ=((i.x-posi[0])**2+(i.y-posi[1])**2)**0.5
			if templ<=i.s:
				hold=i
		if i==hold:
			continue
		i.applyforce(0,1)
		i.speed()
		i.display()
	for i in springs:
		i.display()
	
	pygame.display.update()
	clock.tick(60)