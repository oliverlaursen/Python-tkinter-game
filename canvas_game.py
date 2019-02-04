#fileencoding=UTF-8

"""
	Canvas GAME
"""

import tkinter as tk
import time
from random import *
from math import sqrt

class Game:
	def __init__(self):
		self.root=tk.Tk()

		tk.Label(text='Aim Trainer v1.0',font=('Arial Black',20)).pack()

		self.canvas=tk.Canvas(width=500,height=500)
		self.canvas.pack()
		self.player=self.canvas.create_oval(200,200,250,250,fill='orange')
		self.shot=self.canvas.create_line(0,0,0,0)

		trumpimg=tk.PhotoImage(r"images\trump.gif")
		self.root.trumpimg=trumpimg
		self.trump=self.canvas.create_image((200,200),image=trumpimg,anchor='nw')

		self.root.bind('a', lambda event: self.player_movement(event,'left'))
		self.root.bind('s', lambda event: self.player_movement(event,'down'))
		self.root.bind('d', lambda event: self.player_movement(event,'right'))
		self.root.bind('w', lambda event: self.player_movement(event,'up'))
		self.root.bind('<ButtonPress-1>', lambda event: self.shoot(event,self.enemy1))

		self.enemy1=self.create_enemy(100,100)
		self.wall1=self.create_wall(300,300)
		

		self.points=tk.IntVar()
		point_text=tk.Label(text='POINTS: ',font=("Courier",16)).pack(side=tk.LEFT)
		point_score=tk.Label(textvariable=self.points,font=("Courier",22)).pack(side=tk.LEFT)

		self.highscore=tk.IntVar()
		highscore_label=tk.Label(textvariable=self.highscore,font=("Courier",16)).pack(side=tk.RIGHT)
		highscore_text=tk.Label(text='Highscore: ',font=(("Courier"),16)).pack(side=tk.RIGHT)




		self.enemy_bot()

	def player_movement(self,event,direction):
		a = self.canvas.bbox(self.player)
		b= self.canvas.bbox(self.wall1)
		wallmidx=(b[0]+b[2])/2
		stuck=False

		#Check for collision, otherwise move player
		if not(a[0]>b[2] or b[0]>a[2] or a[1]>b[3] or b[1]>a[3]):
			stuck=True


		if(stuck==False):
			if(direction=='left'):
				self.canvas.move(self.player,-10,0)
			elif(direction=='up'):
				self.canvas.move(self.player,0,-10)
			elif(direction=='down'):
				self.canvas.move(self.player,0,10)
			elif(direction=='right'):
				self.canvas.move(self.player,10,0)
		else:
			if (abs(a[0]-wallmidx)>abs(a[2]-wallmidx)): #Check if collision happened on left side
				self.canvas.move(self.player,-10,0)
			elif abs(a[2]-wallmidx)>abs(a[0]-wallmidx): #Check if collision happened on right side
				self.canvas.move(self.player,10,0)




	def shoot(self,event,target):
		length=1000
		enemy_center=((self.canvas.coords(self.enemy1)[0]+self.canvas.coords(self.enemy1)[2])/2,(self.canvas.coords(self.enemy1)[1]+self.canvas.coords(self.enemy1)[3])/2)
		player_center=((self.canvas.coords(self.player)[0]+self.canvas.coords(self.player)[2])/2,(self.canvas.coords(self.player)[1]+self.canvas.coords(self.player)[3])/2)

		if(target==self.player):
			B=enemy_center
			A=(event[0],event[1])
		else:
			A=(event.x,event.y)
			B=(player_center)

		ran1=randint(0,400)
		ran2=randint(0,400)

		if(B[0]-A[0])==0:
			B[0]+=0.5 		#fix division with zero fejl som kan forekomme
		a=(B[1]-A[1])/(B[0]-A[0])
		b=A[1]-a*A[0]

		if(A[0]<B[0]):
			length=-length

		self.shot=self.canvas.create_line(B,length,a*length+b, fill='red')
		self.canvas.update()
		for i in range(50):
			if (self.canvas.coords(target)[0])<i*10<self.canvas.coords(target)[2] and self.canvas.coords(target)[1]<a*i*10+b<self.canvas.coords(target)[3]: #CHECK FOR ENEMY ER RAMT MED STRÅLE VED BRUG AF LINEÆR ALGEBRA
				
				
	
				if(target==self.player):
					if(self.points.get()>0):
						self.points.set(self.points.get()-1)
				else:
					self.canvas.coords(target,ran1,ran2,ran1+50,ran2+50)
					self.points.set(self.points.get()+1)
					if(self.highscore.get()<self.points.get()):
						self.highscore.set(self.points.get())
				break

		self.root.after(100,self.canvas.coords,self.shot,0,0,0,0)

	def enemy_bot(self):
		delay=2000/(self.points.get()+1)*1.5
		self.root.after(int(delay),self.enemy_bot)
		aimx, aimy = ((self.canvas.coords(self.player)[0]+self.canvas.coords(self.player)[2])/2,(self.canvas.coords(self.player)[1]+self.canvas.coords(self.player)[3])/2)
		
		if(self.points.get()!=0):
			self.root.after(int(delay),self.shoot,(aimx,aimy),self.player)
			
		
		

	def create_enemy(self,x,y):
		return self.canvas.create_rectangle(x-25,y-25,x+25,y+25,fill='black')

	def create_wall(self,x,y):
		return self.canvas.create_rectangle(x-10,y-70,x+10,y+70,fill='brown')

if __name__ == '__main__':
	g1=Game()
	g1.root.mainloop()