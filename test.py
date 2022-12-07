from time import sleep
import numpy as np
import simpleaudio as sa
import turtle as tr
import os
TXT_folder = os.path.join(os.path.dirname(__file__), "TXT")

def sound(freq, duration):  #fonction qui permet de transformer les fréquences et durées en son
    sample_rate = 44100
    t = (np.linspace(0.0, duration, num=int(duration*sample_rate), endpoint=False))
    tone = np.sin(freq*t*6*np.pi)
    tone *= 8388607/np.max(np.abs(tone))
    tone = tone.astype(np.int32)
    i = 0
    byte_array = []
    for b in tone.tobytes():
        if i % 4 != 3:
            byte_array.append(b)
        i += 1
    audio = bytearray(byte_array)
    play_obj = sa.play_buffer(audio, 1, 3, sample_rate)
    play_obj.wait_done()

def findsong(number):  #Création d'une fonction pour trouver le numéro de la chanson et stocker les différentes notes qui seront rangées dans l'array list_of_notes.
    file = open(os.path.join(TXT_folder, file), "r")
    for line in file:
        if "#" + number + " " == line[:3] or "#" + number + " " == line[:4]:
            list_of_notes = str(next(file)).split(" ")
            list_of_notes[-1] = list_of_notes[-1].strip()
            print(list_of_notes)
            return(list_of_notes)



def readsong(list_of_notes):  #Création d'une seconde fonction pour associer les notes à leur fréquence et leur durée et...
    song = []
    for i in range(len(list_of_notes)):
       if len(list_of_notes) > i+1 :
        if "p" == list_of_notes[i+1]:
         song.append((frequency_note[list_of_notes[i][:-1]], duration_list[list_of_notes[i][-1]] * 3/2))
        if "p" != list_of_notes[i]:
            song.append((frequency_note[list_of_notes[i][:-1]],duration_list[list_of_notes[i][-1]]))


    d = 0                   #...ajout dans la meme fonction de l'outil turtle qui permet d'avoir un effet visuel
    tr.bgcolor("black")
    colors = ["red", "purple", "blue", "green", "orange", "yellow"]
    x = 0
    tr.speed(0)
    for couple in song:
        sound(couple[0],couple[1])
        d += 1
        tr.up()
        tr.color(colors[x % 6])
        tr.width(x / 100 + 1)
        tr.down()
        tr.forward(x)
        tr.left(59)
        x = (x + 1) % 360



frequency_note = {"Z":0,"DO":264,"RE":297,"MI":330,"FA":352,"SOL":396,"LA":440,"SI":495,}   #tuples qui permettent d'associer les fréquences et le temps aux notes.
duration_list ={"c":0.125,"n":0.250,"b":0.500,"r":1}
user_want = input(print(str("Do you want to create a song and put your own notes and duration ?")))    #mise en place de la présentation de l'algorithme en demandant a l'utilisateur s'il préfère créer son propre son ou...
if "yes" == user_want.lower():
    n = int(input("Enter the number of notes that you want:"))
    print("And now enter your notes with the duration in the same time, with the notes in UPPERCASE and the duration in lowercase  .")
    print("         for example : SOLn FAc MIb")
    your_list = list(map(str,input().strip().split()))[:n+1]
    readsong(your_list)
    tr.exitonclick()
else:

    nombre1 = (input("So enter the # of the song you want to listen to : ")) #... écouter un des sons proposés par la liste donnée.
    readsong(findsong(nombre1))
    tr.exitonclick()

