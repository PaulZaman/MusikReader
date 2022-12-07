import os
import pygame as pg
import numpy
from time import sleep
import random

duration_of_notes = {"r":1, "b":0.5, "n":0.250, "c":0.125}
durations = ["r", "b", "n", "c"]
notes = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI", "Z"]

tempo = 1

#colors
darkmagenta = (139,0,139)
black = (0,0,0)
red = (255,0,0)
light_grey = (100, 100, 100)
grey = (50,50,50)
dark_grey = (20, 20, 20)
blue = (0,0,255)
light_blue = (100, 100, 255)
white = (255, 255, 255)
less_white = (160, 160, 160)

#window settings
screen_width = 600
screen_height = 600
TILESIZE = 20
# screen is 30*30 grid wise
GRIDWIDTH = screen_width / TILESIZE
GRIDHEIGHT = screen_height / TILESIZE
Title = 'The Music App'
FPS = 60


#load text files
TXT_folder = os.path.join(os.path.dirname(__file__), "TXT")
textfiles = []
i=0
for txt_file in os.listdir(TXT_folder):
    filesong = open(os.path.join(TXT_folder, txt_file), "r")
    lines = filesong.readlines()
    d = {"filenumber":i, "filetitle":txt_file, "filelength":len(lines)}
    textfiles.append(d)
    i += 1


#load piano sounds
wav_folder = os.path.join(os.path.dirname(__file__), "wav_files")
notesdict={}
i=0
for file in sorted(os.listdir(wav_folder)):
    notesdict[file[1:-4]] = file
    i+=1


#load images
img_folder = os.path.join(os.path.dirname(__file__), "img_folder")

#buttons
playunpressed = pg.image.load(os.path.join(img_folder, "PLAY_unpressed.png"))
playpressed = pg.image.load(os.path.join(img_folder, "Play_pressed.png"))
delunpressed = pg.image.load(os.path.join(img_folder, "DEL_unpressed.png"))
delpressed = pg.image.load(os.path.join(img_folder, "DEL_pressed.png"))
saveunpressed = pg.image.load(os.path.join(img_folder, "SAVE_unpressed.png"))
savepressed = pg.image.load(os.path.join(img_folder, "SAVE_pressed.png"))

#menu bg
Main_menubg = pg.image.load(os.path.join(img_folder, "Main_menu.jpg"))
Song_playerbg = pg.image.load(os.path.join(img_folder, "Song_player.jpg"))
Song_tunerbg = pg.image.load(os.path.join(img_folder, "Song_tuner.jpg"))
Song_writerbg = pg.image.load(os.path.join(img_folder, "Song_writer.jpg"))
Song_writer_markov = pg.image.load(os.path.join(img_folder, "Song_writer_Markov.jpg"))