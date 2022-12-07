# Menu
# This file contains all different menu screens for the GUI:

# start_screen():
# choose_file():
# choose_song():
# song_tuner(song_number):
# play_the_song(next_action):
# choose_title_new_song():
# choose_file_to_add_song_to(bg, new_song, user_title):
# write_song(user_title):
# Markov_create_song(TITLE):

# at the very bottom, we have the main loop that naviguates between the different screens

from menufunctions import *




#Different menu screens
def start_screen():
    #   Start screen, returns what next action is to be executed
    screen.blit(Main_menubg, (0, 0))
    run = True
    while run:
        write = button(screen, "Write a song", black, white, 15, 17, 10, 2)
        play = button(screen, "Play a song", black, white, 15, 12, 10, 2)
        if write:
            return "Choose title"
        if play:
            return "Choose file"
        pg.display.flip()
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"


def choose_file():
    #   Choose file screen, returns the selected file and it's filenumber
    #   This function is used when the user has to select a specific file
    run = True
    if len(textfiles) == 1:
        return textfiles[0]["filetitle"], textfiles[0]["filenumber"]

    while run:
        screen.blit(Song_playerbg, (0, 0))
        draw_text(screen, "Before playing a song,", 40, white, 15, 7)
        draw_text(screen, "select base file :", 40, white, 15, 10)
        i = 18
        # this part is to draw on screen the title of the files
        # their position depends on how many there are
        for file in textfiles:
            filebutton = text_button(screen, file["filetitle"], white, 15, i, 15, 1)
            i += 5 / len(textfiles) + 1
            if filebutton:
                return filebutton, file["filenumber"]

        if return_to_menu(screen):
            return "Start screen"
        clock.tick(FPS)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"


def choose_song():
    #   Choose song screen, returns number of song to be played, or next action to be executed
    #   depending on what the user wants to do
    sleep(0.1)

    run = True
    while run:
        screen.blit(Song_playerbg, (0, 0))
        #draw_grid()

        changefile = button(screen, "Change base file", black, less_white, 15, 5, 13, 2)
        if changefile:
            return "Choose file"

        i = 6
        for songtitle in titles_file.values():
            # the position of the titles on screen depend on the number of songs in selected file
            i += 19/len(titles_file)
            songbutton = text_button(screen, songtitle, white, 15, i, 15, 1)
            if songbutton:
                return int(get_key(songbutton, titles_file))
            if file == "File1.txt":
                maximum = 12
            else:
                maximum = textfiles[filenumber]["filelength"]/2
            # this part creates a delete button for songs added by the user
            if int(get_key(songtitle, titles_file)) > maximum:
                delete_song = img_button(screen, "del", delunpressed, delpressed, 25, i, w=2, h=2, decalage=20)
                if delete_song:
                    are_you_sure_output = are_you_sure(screen, songtitle, file)
                    if are_you_sure_output == "STOP":
                        return "STOP"
                    elif are_you_sure_output:
                        delsong(int(get_key(songtitle, titles_file)), file)
                        sleep(0.2)
                        return "Play a song"

        if return_to_menu(screen):
            return "Start screen"
        clock.tick(FPS)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"


def song_tuner(song_number):
    #   Song tuner screen, returns number of song to be played, and modifications to be aplied
    sleep(0.2)
    now = pg.time.get_ticks()

    error_transpo_notint, error_transpo_nothingthere, invert, transpose = False, False, False, False
    amount_of_transposition = ""

    run = True
    while run:
        screen.blit(Song_tunerbg, (0, 0))
        #draw_grid()

        draw_text(screen, "Inversion : ", 25, white, 10, 7.5)
        invert = switch(screen, 20, 7, 4, 2, invert, light_grey)
        draw_text(screen, "Transposition : ", 25, white, 10, 12.5)
        transpose = switch(screen, 20, 12, 4, 2, transpose, light_grey)

        if transpose:
            draw_text(screen, "Enter a value for transposition :", 25, white, 15, 17)
            text_box(screen, amount_of_transposition, 15, 19, 3, 2, now)
            if error_transpo_nothingthere:
                draw_text(screen, "You have to enter a value for transposition", 20, red, 15, 15)
            if error_transpo_notint:
                draw_text(screen, "Value has to be an integer", 20, red, 15, 15)

        play = img_button(screen, "Play", playunpressed, playpressed, 17, 22,)

        if play:
            (error_transpo_nothingthere, error_transpo_notint) = check_for_error(amount_of_transposition)
            if (error_transpo_nothingthere, error_transpo_notint) == (False, False) or not transpose:
                return (song_number, invert, transpose, amount_of_transposition)


        if return_to_menu(screen):
            return "Start screen"
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"
            if event.type == pg.KEYDOWN:
                amount_of_transposition += event.unicode
                if event.key == pg.K_BACKSPACE:
                    amount_of_transposition = amount_of_transposition[:-1]

        pg.display.flip()


def play_the_song(next_action):
    #   Play song screen, returns next action to be executed
    #   animation screen
    sleep(0.2)
    screen.blit(Song_playerbg, (0, 0))

    if next_action[1]:      #inversion
        draw_text(screen, "Inversion : ", 20, white, 5, 7)
        draw_text(screen, "ON", 20, white, 11, 7)
    if next_action[2]:      #transposition
        draw_text(screen, "Transposition : ", 20, white, 5, 8)
        draw_text(screen, "ON", 20, white, 11, 8)

    song_notes = get_song(file, str(next_action[0]))
    music_sheet = make_music_sheet(song_notes, next_action[1], next_action[2], next_action[3])

    draw_text(screen, "Playing the song :", 20, less_white, 15, 5)
    draw_text(screen, titles_file[str(next_action[0])], 20, white, 22, 6)

    index = 0
    pause = False
    while run:

        if not pause:
            (x, y) = music_sheet[index]
            piano_animation(screen, x)
            sound(x, y)
            piano_animation(screen, "Z")
            index += 1

        pg.display.flip()
        if index > len(music_sheet)-1:
            return "Play a song"

        clock.tick(FPS)
        if return_to_menu(screen):
            return "Start screen"

        for event in pg.event.get():
            if pg.key.get_pressed()[pg.K_SPACE]:
                pause = not pause
            if event.type == pg.QUIT:
                return "STOP"


def choose_title_new_song():
    # this is the choose title screen, it is used in the case of writing a new song
    # the user has to enter his title and select whether he wants to create a song by writing it
    # or by using markov chains
    now = pg.time.get_ticks()
    sleep(0.2)
    run = True
    no_title_error = False
    user_title = ""
    while run:
        screen.blit(Song_writerbg, (0, 0))
        if return_to_menu(screen):
            return "Start screen"


        draw_text(screen, "Enter a title for your new song : ", 30, white, 15, 5)
        text_box(screen, user_title, 15, 10, 4, 2, now)
        if button(screen, "Write song", black, white, 23, 20, 10, 2):
            if len(user_title) > 0:
                return (user_title, "Write song")
            else:
                no_title_error = True
        if button(screen, "Create Markov song", black, white, 9, 18, 16, 2):
            if len(user_title) > 0:
                return (user_title, "Markov song")
            else:
                no_title_error = True

        if no_title_error:
            draw_text(screen, "You have to enter a Title before creating a song", 20, red, 15, 15)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"
            if event.type == pg.KEYDOWN:
                user_title += event.unicode
                if event.key == pg.K_BACKSPACE:
                    user_title = user_title[:-1]
        clock.tick(FPS)
        pg.display.flip()


def choose_file_to_add_song_to(bg, new_song, user_title):
    # this window is when the user finished writing his new song, and has to choose to which file he wants to add it to
    # returns next action or nothing
    run2 = True
    while run2:
        screen.blit(bg, (0, 0))
        # draw_grid()
        draw_text(screen, "Choose a file to", 40, white, 15, 7)
        draw_text(screen, "add your song to :", 40, white, 15, 10)
        i = 14  # first position of filename when choosing file to add new song
        for files in textfiles:
            choosenfile = text_button(screen, files["filetitle"], white, 15, i, 15, 1)
            i += 9 / len(textfiles) + 1
            if choosenfile:
                file = choosenfile
                run2 = False

        if return_to_menu(screen):
            return "Start screen"
        clock.tick(FPS)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"

    addsong(new_song, user_title, file)
    screen.blit(Song_writerbg, (0, 0))
    draw_text(screen, "Well Done ! You have just created a song called :", 20, white, 15, 10)
    draw_text(screen, user_title, 20, white, 15, 12)
    draw_text(screen, "Go to song player to play your new song", 25, white, 15, 17)
    pg.display.flip()
    sleep(4)


def write_song(user_title):
    #This is where the user writes his new song by enterring notes one by ones
    #returns next action
    now = pg.time.get_ticks()
    sleep(0.2)
    x = 15    #where we write the new song on screen
    run = True
    error_no_song = False
    choose_note = True
    choose_duration = False
    number_of_notes_on_bottom_row = 4
    new_song = ""
    new_note = ""
    while run:
        screen.blit(Song_writerbg, (0, 0))
        #draw_grid()
        if return_to_menu(screen) != None:
            return "Start screen"

        if choose_note:
            # create notes buttons
            new_note = ""
            notes = []
            DO = button(screen, "DO", white, black, screen_width/(5*TILESIZE), 5, 3, 2)
            notes.append(DO)
            RE = button(screen, "RE", white, black, 2*screen_width/(5*TILESIZE), 5, 3, 2)
            notes.append(RE)
            MI = button(screen, "MI", white, black, 3*screen_width/(5*TILESIZE), 5, 3, 2)
            notes.append(MI)
            FA = button(screen, "FA", white, black, 4*screen_width/(5*TILESIZE), 5, 3, 2)
            notes.append(FA)
            SOL = button(screen, "SOL", white, black, screen_width/((number_of_notes_on_bottom_row+1)*TILESIZE), 10, 3, 2)
            notes.append(SOL)
            LA = button(screen, "LA", white, black, 2*screen_width/((number_of_notes_on_bottom_row+1)*TILESIZE), 10, 3, 2)
            notes.append(LA)
            SI = button(screen, "SI", white, black, 3*screen_width/((number_of_notes_on_bottom_row+1)*TILESIZE), 10, 3, 2)
            notes.append(SI)
            Z = button(screen, "Z" ,white, black, 4*screen_width/((number_of_notes_on_bottom_row+1)*TILESIZE), 10, 3, 2)
            notes.append(Z)
            if new_song:
                # only shows "p" button if the new song has a least one note
                p = button(screen, "p", white, black, 5 * screen_width / (6 * TILESIZE), 10, 3, 2)
                notes.append(p)
                number_of_notes_on_bottom_row = 5
            for note in notes:
                if note != None:
                    if note == "p":
                        new_song += "p "
                        sleep(0.2)
                    else:
                        new_note = note
                        choose_note = False
                        choose_duration = True
                        sleep(0.2)

        if choose_duration:
            durations = []
            r = button(screen, "Ronde" ,white, black, 15, 5, 6, 2)
            durations.append(r)
            b = button(screen, "Blanche" ,white, black, 15, 8, 6, 2)
            durations.append(b)
            n = button(screen, "Noire" ,white, black, 15, 11, 6, 2)
            durations.append(n)
            c = button(screen, "Croche" ,white, black, 15, 14, 6, 2)
            durations.append(c)
            for duration in durations:
                if duration != None:
                    if new_song == None:
                        new_song = ""
                    new_note += duration[0].lower()
                    choose_duration = False
                    choose_note = True
                    new_song += (new_note) + " "
                    sleep(0.2)

        delete = img_button(screen, "DEL", delpressed, delunpressed, 22, 15)
        save = img_button(screen, "Save", savepressed, saveunpressed, 13, 23)
        if delete == "DEL":
            new_song = delete_last_note(new_song)
            sleep(0.2)
        text_box(screen, new_song, x, 20, 4, 2, now)
        if text_box.text_rect.right +20 > screen_width:
            x -= 1

        if save == "Save":
            choose_file_to_add_song_to(Song_writerbg, new_song, user_title)
            return "Start screen"

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"

        pg.display.flip()
        clock.tick(FPS)


def Markov_create_song(TITLE):
    # this screen contains multiple ones, it is where the user selects parameters to create a new song
    # using markov chains
    sleep(0.2)
    now = pg.time.get_ticks()
    run = True
    selectfile = True
    all_file = False
    selectlength = False
    choosing_file = True
    error_length_notint = False
    error_length_nothingthere = False
    new_song_length = ""
    choose_save_file = False
    while run:
        screen.blit(Song_writer_markov, (0, 0))

        # choose a file to create markov table
        if choosing_file:
            if selectfile:
                draw_text(screen, "To create a Markov song, select base file:", 28, white, 15, 7)
                draw_text(screen, "You can select the option 'whole file'", 20, white, 15, 9)
                draw_text(screen, "to base new song on all the songs of the file", 20, white, 15, 10)
            i = 15  # pos of first filename
            for files in textfiles:
                choosenfile = text_button(screen, files["filetitle"], white, 15, i, 15, 1)
                i += 7 / len(textfiles) + 1
                if choosenfile:
                    choosing_file = False
                    file = choosenfile
                    titles_file = get_all_songs_titles(file)
                    if all_file:
                        markov_map = create_markov_map_all_songs(file)
                        selectlength = True
                    sleep(0.2)
            draw_text(screen, "Whole file:", 15, white, 5, 14)
            all_file = switch(screen, 5, 15, 4, 2, all_file, light_grey)


        # choose a song in the file, if you didn't select whole file
        if not choosing_file and not all_file and not selectlength:
            i1 = 7
            draw_text(screen, "Choose a song to base your Markov table on :", 20, white, 15, 7)
            for songtitle in titles_file.values():
                i1 += 18 / len(titles_file)
                songbutton = text_button(screen, songtitle, white, 15, i1, 15, 1)
                if songbutton:
                    selectlength = True
                    markov_map = create_markov_map(get_key(songbutton, titles_file), file)

        # show markov table and select length of new song
        if selectlength:
            draw_text(screen, "Table of note successors", 15, white, 9.5, 7)
            draw_map(screen, markov_map[0], 50, 170, 300, 250, notes)
            draw_text(screen, "Table of duration successors", 15, white, 24, 9)
            draw_map(screen, markov_map[2], 400, 200, 150, 150, durations)

            draw_text(screen, "Enter a length for your song :", 25, white, 11, 22)
            text_box(screen, new_song_length, 25, 21.5, 4, 2, now)
            if error_length_nothingthere:
                draw_text(screen, "You have to enter a length for your new song", 20, red, 15, 24)
            if error_length_notint:
                draw_text(screen, "Value has to be an integer", 20, red, 15, 24)
            createsong = button(screen, "Create my new song", black, white, 15, 25, 15, 2)
            if createsong:
                (error_length_nothingthere, error_length_notint) = check_for_error(new_song_length)
                if (error_length_nothingthere, error_length_notint) == (False, False):
                    choose_save_file = True
                    selectlength = False

        # choose a file to add your song to
        if choose_save_file:
            doing = choose_file_to_add_song_to(Song_writer_markov, markov_new_song(markov_map[0], markov_map[1], markov_map[2], markov_map[3], new_song_length), TITLE)
            if doing == "STOP":
                return "STOP"
            return "Start screen"

        if return_to_menu(screen):
            return "Start screen"

        clock.tick(FPS)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"
            if event.type == pg.KEYDOWN and selectlength:
                if text_box.text_width < 150:
                    new_song_length += event.unicode
                if event.key == pg.K_BACKSPACE:
                    new_song_length = new_song_length[:-1]





# main loop
pg.init()
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption(Title)
clock = pg.time.Clock()
next_action = "Start screen"
run = True
while run:
    clock.tick(FPS)
    if next_action == "Start screen":
        next_action = start_screen()

    if next_action == "Choose file":
        next_action = choose_file()
        if type(next_action) == tuple:
            file = next_action[0]
            filenumber = next_action[1]
            next_action = "Play a song"

    if next_action == "Choose title":
        next_action = choose_title_new_song()
        if type(next_action) == tuple:
            title, next_action = next_action

    if next_action == "Play a song":
        titles_file = get_all_songs_titles(file)
        next_action = choose_song()

    if next_action == "Write song":
        next_action = write_song(title)

    if next_action == "Markov song":
        next_action = Markov_create_song(title)

    if type(next_action) is int:
        next_action = song_tuner(next_action)
        if type(next_action) != str:
            next_action = play_the_song(next_action)

    if next_action == "STOP":
        run = False