from main import *
"""
Welcome to my game! I have explored the use of Prim's Maze algorithm combined with a DDA algorithm, and
perspective based pseudo-3D rendering (that's alot of words).

Aim of the game is to find the Green square in the maze as Fast as possible! (simple right?!)

Keys:
SECRETS:
B       -> boss key
Z       -> 4x speed 
ESC     -> Pause
m   -> Show Map 
= -> dev_mode
- -> uber cheat (will you get lucky?)


A,S,D,W -> forward, back, strafe left, strafe right

Q,E     -> Rotate anticlockwise / clockwise


references i used: 
http://www.playfuljs.com/a-first-person-engine-in-265-lines/ - first person engine theory from playfulJS
https://www.youtube.com/watch?v=NbSee-XM7WA - Useful Video of Fast DDA from javidx9 (28/02,2021)
https://lodev.org/cgtutor/raycasting.html - referenced by javidx9
https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm - Prims Algorithm Explanation by Jamis Buck


"""

if __name__ == '__main__':
    g = Game()
    g.run_menu()
