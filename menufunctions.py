# This file contains all the different interface functions.
# functions:

# return_to_menu(screen):
# draw_text(screen, text, size, color, x, y, nogrid=False, midtop=True):
# draw_grid(screen):
# button(screen, text, button_color, text_color, x, y, w, h):
# text_button(screen, text, text_color, x, y, w, h):
# switch(screen, x, y, w, h, state, color):
# text_box(screen, text, x, y, w, h, time):
# img_button(screen, name, imgunpressed, imgpressed, x, y, w=0, h=0, decalage=43):
# check_for_error(amount):
# delete_last_note(string):
# piano_animation(screen, note):
# are_you_sure(screen, songtitle, file):
# draw_map(screen, matrix, x, y, w, h, list_for_axis):

from Main import *

#basic menu functions

def return_to_menu(screen):
    # This function creates a button for returning to menu,
    # returns next action if button is pressed
    restart = button(screen, "Return to menu", black, less_white, 15, 28, 13, 2)
    if restart == "Return to menu":
        return restart


def draw_text(screen, text, size, color, x, y, nogrid=False, midtop=True):
    # This function draws text on screen, and dosen't return anything
    font = pg.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)
    draw_text.text_width = text_surface.get_width()
    text_rect = text_surface.get_rect()
    if midtop:
        if not nogrid:
            text_rect.midtop = (x * TILESIZE, y * TILESIZE)
        if nogrid:
            text_rect.midtop = (x, y)
    else:
        if not nogrid:
            text_rect.topright = (x * TILESIZE, y * TILESIZE)
        if nogrid:
            text_rect.topright = (x, y)
    screen.blit(text_surface, text_rect)


def draw_grid(screen):
    # This function draws grid on screen (only used while develloping)
    for x in range(0, screen_width, TILESIZE):
        pg.draw.line(screen, light_blue, (x, 0), (x, screen_height))
    for y in range(0, screen_height, TILESIZE):
        pg.draw.line(screen, light_blue, (0, y), (screen_width, y))


def button(screen, text, button_color, text_color, x, y, w, h):
    # This function creates a button on screen
    # it returns the text of the button if it is pressed, and none otherwise
    # changes the color of box when mouse is hovering over it
    x = x*TILESIZE
    y = y*TILESIZE
    w = w*TILESIZE
    h = h*TILESIZE
    mouse = pg.mouse.get_pos()
    rect = pg.rect.Rect(0, 0, w, h)
    rect.midtop = (x, y)
    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
        button_color = grey
        pg.event.get()
        click = pg.mouse.get_pressed()
        if click[0] == 1:
            return text
    pg.draw.rect(screen, button_color, rect)
    draw_text(screen, text, 30, text_color, x, 5 + y, True)


def text_button(screen, text, text_color, x, y, w, h):
    # This function is similar to button, but does not create a box for the button,
    # it simply uses the text
    # it returns the text of the button if it is pressed, and none otherwise
    # changes the color of text when mouse is hovering over it
    mouse = pg.mouse.get_pos()
    rect = pg.rect.Rect(0, 0, w * TILESIZE, h * TILESIZE)
    rect.midtop = (x * TILESIZE, y * TILESIZE)
    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
        text_color = less_white
        pg.event.get()
        if pg.mouse.get_pressed()[0] == 1:
            return text
    draw_text(screen, text, 25, text_color, x * TILESIZE, y * TILESIZE, True)


def switch(screen, x, y, w, h, state, color):
    # this function creates a on/off switch, a bit like a radio button
    # returns the stated of the button: on or off
    # changes color when pressed
    mouse = pg.mouse.get_pos()
    rect = pg.rect.Rect(0, 0, w * TILESIZE, h * TILESIZE)
    rect.midtop = (x * TILESIZE, y * TILESIZE)
    pg.event.get()
    click = pg.mouse.get_pressed()

    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height and click[0] == 1:
        if not state:
            sleep(0.2)
            state = True
        else:
            sleep(0.2)
            state = False

    if state:
        text = "ON"
    else:
        text = "OFF"
        color = black

    pg.draw.rect(screen, color, rect)
    draw_text(screen, text, 30, white, x * TILESIZE, 5 + y * TILESIZE, True)
    return state


def text_box(screen, text, x, y, w, h, time):
    # creates a text box with inputted text
    # makes box grow as text is growing
    # creates a vertical white bar to animate a bit
    x = x*TILESIZE
    y = y*TILESIZE
    w = w*TILESIZE
    h = h*TILESIZE
    font = pg.font.Font('freesansbold.ttf', 25)
    text_surface = font.render(text, True, white)
    text_box.text_width = text_surface.get_width()
    text_box.text_rect = text_surface.get_rect()
    text_box.text_rect.midtop = (x, 5+y)

    if text_box.text_width+40 > w:
        w = 40 + text_box.text_width
    rect = pg.rect.Rect(0, 0, w, h)
    rect.midtop = (x, y)
    pg.draw.rect(screen, black, rect)
    if (pg.time.get_ticks() - time)%500 < 250:
        pg.draw.line(screen, white, (x + text_box.text_width/2, y), (x+text_box.text_width/2, y + 40), 3)
    screen.blit(text_surface, text_box.text_rect)


def img_button(screen, name, imgunpressed, imgpressed, x, y, w=0, h=0, decalage=43):
    # This function creates a button on screen with an image
    # it returns the text of the button if it is pressed
    # changes the image when mouse is hovering over it
    x = x*TILESIZE
    y = y*TILESIZE
    w = w*TILESIZE
    h = h*TILESIZE
    mouse = pg.mouse.get_pos()
    if w!= 0 and h!=0:
        imgpressed = pg.transform.scale(imgpressed, (w, h))
        imgunpressed = pg.transform.scale(imgunpressed, (w, h))

    rect = imgunpressed.get_rect()
    rect.midtop = (x + decalage, y)
    #pg.draw.rect(screen, red, rect)

    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
        screen.blit(imgpressed,  (x, y))
        pg.event.get()
        click = pg.mouse.get_pressed()
        if click[0] == 1:
            return name
    else:
        screen.blit(imgunpressed, (x, y))


def check_for_error(amount):
    # this function checks for 2 errors for an amount
    # returns a tuple of booleans
    # error 1: if amount is none
    # error 2: if amount is a string and not a number
    if len(amount) == 0:
        return (True, False)
    for caracter in amount:
        if "0"<=caracter<="9":
           pass
        else:
            return (False, True)
    return (False, False)


def delete_last_note(string):
    # this functions deletes the last note of a song under the form of a string
    # the string when calling this function has a space at the end, so it starts by removing the space:
    if string != None:
        string = string[:-1]
        for c in reversed(string):  #remove all caracters until the next space
            if c != " ":
                string = string[:-1]
            else:
                return string


def piano_animation(screen, note):
    # this function displays on screen the image corresponding to the note that is played
    note = note.lower()
    img = pg.image.load(os.path.join(img_folder, note + ".png"))
    screen.blit(img, (40, 60))
    pg.display.flip()


def are_you_sure(screen, songtitle, file):
    # this function displays a message to make sure the user wants to delete a song
    # we added this to make sure the user does not delete a song unpurposely
    rect = pg.rect.Rect(100, 225, 400, 150)
    run = True
    while run:
        screen.blit(Song_playerbg, (0, 0))
        pg.draw.rect(screen, darkmagenta, rect)
        draw_text(screen, "Do you want to delete the song", 20, black, rect.x + rect.w/2, rect.y+10, nogrid=True)
        draw_text(screen, "'"+songtitle+"'", 20, black, rect.x + rect.w/2, rect.y+35, nogrid=True)
        draw_text(screen, "from "+ file +" ?", 20, black, rect.x + rect.w / 2, rect.y + 65, nogrid=True)
        no = button(screen, "NO", white, black, rect.x/TILESIZE + 5, rect.y/TILESIZE+5, 3, 2)
        yes = button(screen, "YES", white, black, rect.x/TILESIZE + 15, rect.y/TILESIZE + 5, 3, 2)
        if yes == "YES":
            return True
        if no == "NO":
            sleep(0.2)
            return False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "STOP"
        if return_to_menu(screen):
            return "Start screen"
        pg.display.flip()


def draw_map(screen, matrix, x, y, w, h, list_for_axis):
    # this function draws on screen a table

    minisquare_width = w // (len(list_for_axis)+1)
    w = minisquare_width*(len(list_for_axis)+1)
    minisquare_height = h // (len(list_for_axis)+1)
    h = minisquare_height*(len(list_for_axis)+1)

    #create grid
    for i in range(x, x+w+minisquare_width, minisquare_width):      #vertical
        pg.draw.line(screen, white, (i, y), (i, h+y))
    for i in range(y, y+h+minisquare_height, minisquare_height):    #horizontal
        pg.draw.line(screen, white, (x, i), (x+w, i))

    # draw DO RE MI FA SOL LA SI Z
    text_pos_x = x + (3*minisquare_width/2)
    for i in range(len(list_for_axis)):
        draw_text(screen, list_for_axis[i], 15, blue, text_pos_x, y+minisquare_height/4, nogrid=True)
        text_pos_x += minisquare_width
    text_pos_y = y + 5*minisquare_height/4
    for i in range(len(list_for_axis)):
        draw_text(screen, list_for_axis[i], 15, blue, x+minisquare_width/2, text_pos_y, nogrid=True)
        text_pos_y += minisquare_height


    text_pos_y = y + 5*minisquare_height/4
    for line in range(len(matrix)):
        text_pos_x = x + (3 * minisquare_width / 2)
        for col in range(len(matrix[line])):
            draw_text(screen, str(matrix[line][col]), 15, white, text_pos_x, text_pos_y, nogrid=True)
            text_pos_x += minisquare_width
        text_pos_y += minisquare_height