#This file contains the basic functions for sound manipulation:
#   Sound(note, duration)
#   get_key(value, dictionary)
#   get_song(file, number)
#   make_music_sheet(list_notes, invert, transpos, amount_of_transposition=0)
#   get_all_songs_titles(file)
#   transpose(list_of_notes, transposition):
#   transposenote(note, transposition):
#   invert(list):
#   inverse_note(note):
#   addsong(strin, title, file):
#   delsong(numb, file):
#   create_markov_map(numb, file):
#   sum_of_maps(m1, m2):
#   create_markov_map_all_songs(file):
#   markov_new_song(markovmapnotes, total_notes, markovmapdurations, total_durations, songlength):

#   at the bottom you can find a list of tests to test these functions without running the GUI

from Settings import *
pg.mixer.init()


def sound(note, duration):      #plays a sound

    if note == "Z":
        sleep(duration)
    else:
        soundfile = pg.mixer.Sound(os.path.join(wav_folder,notesdict[note]))
        soundfile.play()
        pg.mixer.music.fadeout(0)
        sleep(duration / tempo)


def get_key(value, dictionary):        #find key for a value in a dict, returns the correct key
    for key in dictionary:
        if dictionary[key] == value:
            return key


def get_song(file, number):
    #searches for the correct song in a file returns the list of notes of the song in the form: ["SOLr", "FAb"....]
    file = open(os.path.join(TXT_folder, file), "r")
    # Finds the lines of the title of correct song
    for line in file:
        if "#" + number + " " == line[:3] or "#" + number + " " == line[:4]:
            list_of_notes = str(next(file)).split(" ")
            list_of_notes[-1] = list_of_notes[-1].strip()
            return list_of_notes


def make_music_sheet(list_notes, inver, transpos, amount_of_transposition=0):
    #This function creates partition based on a list and modification if there is one
    # ivert and transpos are booleans
    music_sheet = []
    # check if need for inversion or transposition
    if inver:
        list_notes = invert(list_notes)
    if transpos:
        list_notes = transpose(list_notes, int(amount_of_transposition))

    #finding the correct duration to play
    for index in range(len(list_notes)):
        note_and_duration = list_notes[index]
        if note_and_duration != "p":                            #find the duration if note is not a p
            duration = duration_of_notes[note_and_duration[-1]]
            if index != len(list_notes) - 1:
                if list_notes[index+1]=="p":             #Add 1/2 of the duration if next term is p
                    duration += duration / 2
            music_sheet.append((note_and_duration[:-1], duration))

    return music_sheet


def get_all_songs_titles(file):
    # This function creates a dictionnary containing as key the number of the song in the file
    # and as value the title of the song
    # It is mainly to be able to write all titles of a file in the menu
    file = open(os.path.join(TXT_folder, file), "r")
    all_titles = dict()
    for line in file:
        if line[0] == "#":
            if line[2] == " ":
                all_titles[line[1]] = line[3:].strip()
            else:
                all_titles[line[1:3]] = line[3:].strip()
    return all_titles


def transpose(list_of_notes, transposition):
    # This function transposes a list of notes with the correct amount
    # by calling the next function : transposenote
    # return the new list of notes transposed
    newline = []
    for note in list_of_notes:
        if note[:1] != "Z" and note[:1] != "p":
            newline.append(transposenote(note, transposition))
        else:
            newline.append(note)
    return newline


def transposenote(note, transposition):
    # This function transposes a note with the correct amount
    # creates a list with all notes to facilitate transposition
    list = notes[:-1]   # removes the Z of the list "notes"
    index = list.index(note[:-1]) + transposition
    while index >= 7:
        index -= 7
    note = list[index] + note[-1:]
    return note


def invert(list):
    # This function inverses a list of notes
    # by calling function inversenote
    # returns the inversed list
    inversed_list = []
    for element in list:
        if element != "p":
            inversed_list.append(inverse_note(element))
        else:
            inversed_list.append(element)
    return inversed_list


def inverse_note(note):
    #This function inverses a note and duration and returns the inversed element
    newnote = notes[(len(notes) - notes.index(note[:-1])) % len(notes)]
    newduration = durations[(len(durations) - durations.index(note[-1:])) % len(durations)]

    return newnote + newduration


def addsong(notes, title, file):
    # this function takes a song(as a list or a string seperated with spaces)
    # and adds it to the end of the inputted file with the correct title
    if type(notes) == list:     # if the song is a list, it makes it a string
        notes =" ".join(notes)
    else:
        notes = notes[:-1]       # if the function is a string, it removes space after the last note
                                # this was done because when writing the song in write player, we automatically add
                                # spaces after each note
    filesong = open(os.path.join(TXT_folder, file),"a")
    fd = open(os.path.join(TXT_folder, file), 'r')
    n = 0
    for line in fd:
        n += 1
    if n>=2:
        n=n//2
    n+=1
    filesong.write("#" + str(n) + " " + title + "\n"+notes+"\n")
    filesong.close


def delsong(numb, file):
    # this function deletes a song contained in a file with the file number
    filesong = open(os.path.join(TXT_folder, file),"r")
    lines=filesong.readlines()
    numb=(numb-1)*2     #finds line number to delete
    del lines[numb]
    del lines[numb]
    filesong.close
    editfile=open(os.path.join(TXT_folder, file),"w")

    # this part is a sort of security
    # when deleting a song that is not the last one of the file,
    # it changes the number of other songs to have them in the ascending order
    number_of_before = 0
    for line in lines:
        if line[0] == "#":
            if number_of_before + 1 != int(line[1:3]):
                editfile.write("#" + str(int(number_of_before)+1) + line[3:])
            else:
                editfile.write(line)
            number_of_before += 1
        else:
            editfile.write(line)
    editfile.close


def create_markov_map(numb, file):
    # this function creates 2 markov maps for a song
    # one for the notes, and another one for duration
    # it returns 4 elements, the 2 markov maps and the 2 lists containing the number of occurences of each note
    songlist = get_song(file, numb)

    list_of_notes = list(filter(lambda note: note != "p", songlist))    #remove "p"

    # calculate the total number of durations
    total_durations = [0, 0, 0, 0]
    for note in list_of_notes:
        total_durations[durations.index(note[-1:])] += 1

    # fill lines of matrix for duration with 0
    markovmap_durations = []
    for i in range(4):
        markovmap_durations.append([0, 0, 0, 0])

    # count sucessors of each duration
    for i in range(len(list_of_notes) - 1):
        if i > 0:
            before_duration = list_of_notes[i - 1][-1:]
            markovmap_durations[durations.index(before_duration)][durations.index(list_of_notes[i][-1:])] += 1

    #remove durations
    for i in range(len(list_of_notes)):
        list_of_notes[i] = list_of_notes[i][:-1]

    #calculate total number of notes notes:
    total_notes = [0 ,0 ,0, 0, 0, 0, 0, 0]
    for note in list_of_notes:
        total_notes[notes.index(note)] += 1

    #create matrix of successors for each note
    markovmap_notes = []
    for i in range(8):
        markovmap_notes.append([0, 0, 0, 0, 0, 0, 0, 0])

    #count sucessors of each note
    for i in range(len(list_of_notes)-1):
        if i>0:
            before_note = list_of_notes[i-1]
            markovmap_notes[notes.index(before_note)][notes.index(list_of_notes[i])] += 1

    return markovmap_notes, total_notes, markovmap_durations, total_durations


def sum_of_maps(m1, m2):
    # this functions adds two matrixes using numpy, it the returns the sum of both matrixes as a normal matrix
    m1 = numpy.array(m1)
    m2 = numpy.array(m2)
    new_map = numpy.sum([m1, m2], axis=0)
    return new_map.tolist()


def create_markov_map_all_songs(file):
    # this function uses the function "create_markov_map" to create a markov map of a whole file,
    # it returns 4 elements, the 2 markov maps(notes and duration)
    # and the 2 lists containing the number of occurences of each note and each duration
    song_titles = get_all_songs_titles(file)

    #create all 4 maps and lists, and fill them with zeros
    markov_map_notes_all_songs = []
    for i in range(8):
        markov_map_notes_all_songs.append([0, 0, 0, 0, 0, 0, 0, 0])
    markov_map_durations_all_songs = []
    for i in range(4):
        markov_map_durations_all_songs.append([0, 0, 0, 0])
    total_notes = [0, 0, 0, 0, 0, 0, 0, 0]
    total_durations = [0, 0, 0, 0]


    for song in song_titles:        # adds all the maps and lists to obtain the sum of all 4 lists and maps
        markov_map_notes, all_notes, markov_map_durations, all_durations = create_markov_map(song, file)
        # sums markov map for the notes
        markov_map_notes_all_songs = sum_of_maps(markov_map_notes_all_songs, markov_map_notes)
        # sums markov map for the durations
        markov_map_durations_all_songs = sum_of_maps(markov_map_durations_all_songs, markov_map_durations)
        # sums lists of number of occurences of each note and each duration
        total_notes = sum_of_maps(total_notes, all_notes)
        total_durations = sum_of_maps(total_durations, all_durations)

    return markov_map_notes_all_songs, total_notes, markov_map_durations_all_songs, total_durations


def markov_new_song(markovmapnotes, total_notes, markovmapdurations, total_durations, songlength):
    # This function creates a new song using the markov map technique
    # it returns the partition created
    new_song = []

    # create a list of lists of all successors for each note
    succesors_matrix_notes = []
    for line in markovmapnotes:
        succesors_matrix_line = []
        for i in range(len(line)):
            for j in range(line[i]):
                succesors_matrix_line.append(notes[i])
        succesors_matrix_notes.append(succesors_matrix_line)

    # take the most played note in song and set it as first note
    firstnote = notes[total_notes.index(max(total_notes))]
    new_song.append(firstnote)

    # create new partition only composed of notes by randomly choosing in lists of all successors
    for i in range(1, int(songlength)):
        beforenote = new_song[i-1]
        new_song.append(random.choice(succesors_matrix_notes[notes.index(beforenote)]))

    # create a list of lists of all successors for each duration
    succesors_matrix_durations = []
    for line in markovmapdurations:
        succesors_matrix_line = []
        for i in range(len(line)):
            for j in range(line[i]):
                succesors_matrix_line.append(durations[i])
        succesors_matrix_durations.append(succesors_matrix_line)

    # take the most played duration in song and add it to the first note
    firstduration = durations[total_durations.index(max(total_durations))]
    new_song[0] += firstduration

    # add to new partition durations by randomly choosing in lists of all duration successors
    for i in range(1, int(songlength)):
        beforeduration = new_song[i-1][-1:]
        new_song[i] += (random.choice(succesors_matrix_durations[durations.index(beforeduration)]))

    return new_song



#   TESTS
# You can find here a series of test to test these function with the GUI
# feel free to change the variables or add in a few print statements to test them how you wish


#               TEST 1
"""#   This first test is to get the list of notes from the second song from the file 1
# you can change the variables as you wish to test different songs
song_number = "2"
file = "File1.txt"
song = get_song(file, song_number)
print(song)"""


#               TEST 2
"""#   This second test is to transpose the second song from the file 1 of three notes
# you can change the variables as you wish to test different songs
# normally, when running the GUI, this is done automatically with the function make_music_sheet
# as you can test in test 4
# first we need to get the song list, and then send it to transpose function
song_number = "2"
file = "File1.txt"
transposition_amount = 3
song = get_song(file, song_number)
transposed_song = transpose(song, transposition_amount)
print(song)
print(transposed_song)
# you can now compare the two songs to see that transposotion worked correctly
# here is a list of the notes to help you if you want to compare:
print(notes[:-1])"""



#               TEST 3
"""#   This thrid test is to invert the second song from the file 1
# you can change the variables as you wish to test different songs
# normally, when running the GUI, this is done automatically with the function make_music_sheet
# as you can test in test 4
# first we need to get the song list, and then send it to invert function
song_number = "2"
file = "File1.txt"
song = get_song(file, song_number)
inverted_song = invert(song)
print(song)
print(inverted_song)
# you can now compare the two songs to see that inversion worked correctly
# here is the list we use for inversion to help you if you want to compare:
print(notes)"""



#               TEST 4
"""#   This fourth test is to play the second song from the file 1
# you can change the variables as you wish to test different songs, different files or apply modifications
song_number = "2"
file = "File1.txt"
inversion = False
transposition = False
amount = 2
partition = make_music_sheet(get_song(file, song_number), inversion, transposition, amount_of_transposition=amount)
print(partition)
# you can send this partition to the sound function with a simple while loop:
for note in partition:
    sound(note[0], note[1])"""



#               TEST 5
"""#   This fifth test creates a markov song for song 2 of file1
#you can change the variables as you wish to test different songs
song_number = "2"
file = "File1.txt"
map = create_markov_map(song_number, file)
#map contains a list of 4 elements :
#   the successors table for notes
#   a list of the total repetions for each note
#   the successors table for durations
#   a list of the total repetitons for each duration
#if desired you can send these elements to markov_new_song to create a new partition:
newsonglength = 10
new_song =markov_new_song(map[0], map[1], map[2], map[3], newsonglength)
# now lets send this new song to the sound function by using same method than in test 1
inversion = False
transposition = False
amount = 2
new_parition = make_music_sheet(new_song, inversion, transposition, amount)
for note in new_parition:
    sound(note[0], note[1])
sleep(1)    #this line is added because this program is not in a while loop
            #so as soon as the for loop is finished it stops, thus cutting of the last note and 
            #not letting it fade away
"""


#               TEST 6
"""#   This sixth test creates a markov song for file1
#you can change the variables as you wish to test different files
file = "File1.txt"
map = create_markov_map_all_songs(file)
#map contains a list of 4 elements :
#   the successors table for notes
#   a list of the total repetions for each note
#   the successors table for durations
#   a list of the total repetitons for each duration
#if desired you can send these elements to markov_new_song to create a new partition:
newsonglength = 10
new_song =markov_new_song(map[0], map[1], map[2], map[3], newsonglength)
# now lets send this new song to the sound function by using same method than in test 1
inversion = False
transposition = False
amount = 2
new_parition = make_music_sheet(new_song, inversion, transposition, amount)
for note in new_parition:
    sound(note[0], note[1])
sleep(1)"""

