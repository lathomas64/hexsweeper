from hex import Hex
from random import randrange
import time
import state

class MineHex(Hex):

	def __init__(self, q,r,mine_chance=15, **kwargs):
		super().__init__(q,r, kwargs=kwargs)
		self.reset(mine_chance=mine_chance)

	def reset(self, mine_chance=15):
		if randrange(1,100) <= mine_chance:
			self.mine = True
		else:
			self.mine = False
		self.revealed = False
		self.flagged = False
		self.text = ""
		self.icon = "flag"
		self.icon.visible = False

	def update(self):
		if state.victory or state.loss:
			self.disable = True
			return
		if self.hovered:
			return
		for direction in self.directions:
			neighbor = self.getNeighbor(direction)
			if neighbor == None:
				continue
			if neighbor.hovered:
				self.model.setColorScale(self.highlight_color)
				return
		self.model.setColorScale(self.color)
	def checkNeighbors(self):
		count = 0;
		print("checkNeighbors:")
		print(self)
		for direction in self.directions:
			neighbor = self.getNeighbor(direction)
			print(neighbor)
			if neighbor == None:
				continue
			if neighbor.mine:
				count += 1
		self.text = str(count)
		if count == 0:
			for direction in self.directions:
				neighbor = self.getNeighbor(direction)
				print(neighbor)
				if neighbor == None:
					continue
				if neighbor.flagged:
					continue
				if not neighbor.revealed:
					neighbor.revealed = True
					neighbor.checkNeighbors()

	def input(self, key):
		if self.disabled or not self.model:
			return

		if key == 'right mouse up':
			if self.hovered:
				if self.flagged:
					self.flagged = False
					self.icon.visible = False
				else:
					self.flagged = True
					self.icon = "flag"
					self.icon.visible = True
		if key == 'c':
			MineHex.check_victory()

	def select(self):
		if self.flagged:
			return
		self.revealed = True
		if self.mine:
			self.text = "boom!"
			state.loss = True
		else:
			self.checkNeighbors()

	@classmethod
	def check_victory(cls):
		victory = True
		for node in cls.map.nodes.data():
			hex = node[1]["data"]
			if not hex.revealed and not hex.flagged:
				victory = False
				break
			if hex.flagged and not hex.mine:
				victory = False
				break
			if hex.mine and hex.revealed:
				victory = False
				break
		print(victory)
		return victory

	@classmethod
	def reset_map(cls, radius):
		state.reset()
		for q in range(-radius, radius+1):
			for r in range(-radius, radius+1):
				if abs(q+r) <=radius:
					hex = MineHex.getHex(q,r)
					hex.reset()
	@classmethod
	def create_map(cls, radius):
		for q in range(-radius, radius+1):
			for r in range(-radius, radius+1):
				if abs(q+r) <=radius:
					hex = MineHex(q,r)
