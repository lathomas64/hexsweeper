'''
putzing around with clickable hexes
'''
# Next up move and limit actions to current hex.
from ursina import *
from LiSE import Engine
from LiSE.allegedb import GraphNameError
import networkx as nx
from random import randrange

class Hex(Button):
	current = None
	agents = []
	map = nx.Graph() #https://github.com/networkx/networkx/blob/main/networkx/classes/graph.py
	directions = {
		"northeast":(1,-1),
		"east" : (1,0),
		"southeast" : (0,1),
		"northwest" : (0,-1),
		"west" : (-1,0),
		"southwest" : (-1,1)
	}
	def __init__(self, q,r,scale = .125 * 3 / 5, color=color.azure, disabled=False, **kwargs):
		self.q = q
		self.r = r
		x_offset = q * scale + r * scale/2
		y_offset = r * scale
		super().__init__(x=x_offset, y=y_offset, scale=scale, color=color, disabled=disabled, kwargs=kwargs)
		self.model = Circle(6)
		self.on_click = self.select
		label = str((self.q,self.r))
		Hex.map.add_node(label, data=self)
		self.base_color = color
		self.base_scale = scale
		self.color = self.base_color

	def tick(self):
		self.color = self.base_color

	def select(self):
		if Hex.current and Hex.current != self:
			Hex.current.scale = Hex.current.base_scale
		#self.text = "clicked"
		self.scale = self.base_scale * 1.2
		Hex.current = self

	def getNeighbor(self, direction):
		direction_vector = self.directions[direction]
		targetq = self.q + direction_vector[0]
		targetr = self.r + direction_vector[1]
		return Hex.getHex(targetq, targetr)


	def __str__(self):
		result = str((self.q,self.r))
		return result

	@classmethod
	def create_map(cls, radius):
		for q in range(-radius, radius+1):
			for r in range(-radius, radius+1):
				if abs(q+r) <=radius:
					hex = Hex(q,r)
	@classmethod
	def getHex(cls, q, r):
		target = str((q,r))
		for node in cls.map.nodes.data():
			if target == node[0]:
				return node[1]['data']
		return None
