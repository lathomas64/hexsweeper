'''
putzing around with clickable hexes
'''
# Next up move and limit actions to current hex.
from ursina import *
from LiSE import Engine
from LiSE.allegedb import GraphNameError
import networkx as nx
from random import randrange
from minehex import MineHex
import state

#class Hex(Button):

app = Ursina()
window.color = color._20

gold = 0
counter = Text(text='Choose a starting location.', y=.4, z=-1, scale=2, origin=(0,0), background=True)
left_text = Text(text='Left Text.', y=.4, x=-.6, z=-1, scale=2, origin=(0,0), background=True)
right_text = Text(text='Right Text.', y=.4, x=.6, z=-1, scale=2, origin=(0,0), background=True)
action1 = Button(text="Gather Time", disabled=True, visible=False, y=.3, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
action2 = Button(text="Gather Space", disabled=True, visible=False, y=.245, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
left_text.visible = False
right_text.visible = False
counter.visible = False
#player_icon = 'sword'

def input(key):
    if key == "r":
        MineHex.reset_map(5)

def update():
    state.victory = MineHex.check_victory()
    if state.victory:
        counter.text = "You win!\nPress 'r' to play again!"
        counter.visible = True
    elif state.loss:
        counter.text = "You lose!\nPress 'r' to play again!"
        counter.visible = True
    else:
        counter.visible = False

MineHex.create_map(5)
map = MineHex.map
print("\n\nHex MAP!\n\n")
print(map.nodes)
print(map.nodes.data())
for node in map.nodes.data():
    if node[0] == "(1, 1)":
        print(node[0])
        print(node[1])
        print("--")
    else:
        print("...")
print(map["(0, 0)"])
print("======================")


app.run()
