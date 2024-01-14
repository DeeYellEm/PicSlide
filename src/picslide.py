import pyglet
from pyglet import image
#from pyglet.gl import *

from files import thing, load, resources
from collections import namedtuple
import random
import os
import glob

# Set up a window
myWindow = namedtuple('myWindow', ['X', 'Y'])
myWin = myWindow(800, 600)
game_window = pyglet.window.Window(myWin.X, myWin.Y, visible=True, resizable=False)
main_batch = pyglet.graphics.Batch()

myTile = namedtuple('myTile', ['X', 'Y'])
myTileSize = myTile(100, 75)

# Set up the two top labels
#score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Testing - PicSlide!", x=400, y=575, anchor_x='center', batch=main_batch)

counter = pyglet.window.FPSDisplay(window=game_window)

all_pics = []
pic_tiles = []
DLMcount = 0

def init():
    global num_things
    reset_level()


def reset_level():
    global DLMcount, num_things, all_pics, pic_tiles

    DLMcount += 1
    num_things = int(myWin.X/myTileSize.X * myWin.Y/myTileSize.Y)
    print('DLM: num_things: '+str(num_things))

    # list to store filename present in current directory
    files = []
    relevant_path = "../resources"
    #print("DLM: relevant_path: "+str(relevant_path))
    included_prefix = ['deeyellem']
    files = [fn for fn in os.listdir(relevant_path)
              if any(fn.startswith(ext) for ext in included_prefix)]
    #    if os.path.isfile(os.path.join('../resources', file_path)):
    #        files.append(str('../resources/'+file_path))
            #print("DLM: Adding file_path: "+str(file_path))
    for file in files:
        print('DLM: resource images: '+str(file))

    img_path = relevant_path+'/'+random.choice(files)
    print("DLM: Random Image: "+img_path)
    img = pyglet.image.load(img_path)

    # Load up the tiles
    pic_tiles = load.things(num_things, myWin, main_batch)

    i, j = 0,0
    for tile in pic_tiles:
        picTile = img.get_region(x=(i*myTileSize.X), y=(j*myTileSize.Y), width=myTileSize.X, height=myTileSize.Y)
        tile.image = picTile
        tile.x = i*myTileSize.X
        tile.y = j*myTileSize.Y
        i += 1
        if i == 8:
            j += 1
            i = 0

    game_objects = pic_tiles

    # Things to do on the game_ojects before kickoff
    for obj in game_objects:
        obj.vx = 0
        obj.vy = 0




#def timerFunc (dt):
#    globalVx = random.randrange(20, 80)
#    if (random.random() < 0.5):
#        globalVx = -1*globalVx
    #print('DLM: timerFunc():globalVx: '+str(globalVx))
#    for obj in game_objects:
#        obj.vx = (0.4/obj.scale) * globalVx
#        #print('DLM: timerFunc: obj.scale: '+str(obj.scale)+' obj.vx:'+str(obj.vx))


@game_window.event
def on_draw():
    game_window.clear()

    #bgpicSprite.draw()

    main_batch.draw()

    #fgpicSprite.draw()

    counter.draw()

def update(dt):
    global DLMcount

    DLMcount += 1



if __name__ == "__main__":
    # Start it up!
    init()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
