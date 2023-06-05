import tkinter as tk
from tkinter import ttk
from tkinter import *
import sv_ttk
import os
from tkinter.messagebox import showinfo
import pygame

import touch
import rfid
import lcd
import speaker
import button
import RPi.GPIO as GPIO

numSounds = 0
soundBoard = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
def add_sound(boardDisplay):
    global numSounds
    global soundBoard
    selected_sound = soundsList.selection()[0]
    print(selected_sound)
    soundPath = soundsList.item(selected_sound)['text']
    soundName = soundsList.item(selected_sound)['values'][0]
    if numSounds < 12:
        if soundName[-4:] == '.ogg':
            for i in range(12):
                if soundBoard[i] == '0':
                    boardDisplay[i].configure(text=f'sound {str(i+1)}:\n{soundName}')
                    soundBoard[i] = selected_sound
                    numSounds += 1
                    print(soundBoard)
                    break

def add_sound_spot(boardDisplay, position):
    global numSounds
    global soundBoard
    selected_sound = soundsList.selection()[0]
    print(selected_sound)
    soundPath = soundsList.item(selected_sound)['text']
    soundName = soundsList.item(selected_sound)['values'][0]
    if soundName[-4:] == '.ogg':
        boardDisplay[position-1].configure(text=f'sound {str(position)}:\n{soundName}')
        soundBoard[position-1] = selected_sound
        print(soundBoard)
   
def clear_soundboard(boardDisplay):
    global numSounds
    for i in range(12):
        boardDisplay[i].configure(text=f'sound {i+1}:\n')
        soundBoard[i] = '0'
    numSounds = 0

def play_sound():
    selected_sound = soundsList.selection()[0]
    soundPath = soundsList.item(selected_sound)['text']
    if soundPath[-4:] == '.ogg':
        pygame.mixer.music.load(soundPath)
        pygame.mixer.music.play()
        print(f'played sound {soundPath}')

def load_onto_soundboard(playSound):
    sounds = []
    sound1 = pygame.mixer.Sound(soundsList.item(soundBoard[0])['text'])
    sound1.set_volume(1.0)
    # pygame.mixer.Channel(0).play(sound1, loops=-1)
    sounds.append(sound1)

    sound2 = pygame.mixer.Sound(soundsList.item(soundBoard[1])['text'])
    sound2.set_volume(1.0)
    # pygame.mixer.Channel(1).play(sound2, loops=-1)
    sounds.append(sound2)

    sound3 = pygame.mixer.Sound(soundsList.item(soundBoard[2])['text'])
    sound3.set_volume(1.0)
    # pygame.mixer.Channel(2).play(sound3, loops=-1)
    sounds.append(sound3)

    sound4 = pygame.mixer.Sound(soundsList.item(soundBoard[3])['text'])
    sound4.set_volume(1.0)
    # pygame.mixer.Channel(3).play(sound4, loops=-1)
    sounds.append(sound4)

    sound5 = pygame.mixer.Sound(soundsList.item(soundBoard[4])['text'])
    sound5.set_volume(1.0)
    # pygame.mixer.Channel(4).play(sound5, loops=-1)
    sounds.append(sound5)

    sound6 = pygame.mixer.Sound(soundsList.item(soundBoard[5])['text'])
    sound6.set_volume(1.0)
    # pygame.mixer.Channel(5).play(sound6, loops=-1)
    sounds.append(sound6)
    
    sound7 = pygame.mixer.Sound(soundsList.item(soundBoard[6])['text'])
    sound7.set_volume(1.0)
    # pygame.mixer.Channel(6).play(sound7, loops=-1)
    sounds.append(sound7)
    
    sound8 = pygame.mixer.Sound(soundsList.item(soundBoard[7])['text'])
    sound8.set_volume(1.0)
    # pygame.mixer.Channel(7).play(sound8, loops=-1)
    sounds.append(sound8)

    sound9 = pygame.mixer.Sound(soundsList.item(soundBoard[8])['text'])
    sound9.set_volume(1.0)
    # pygame.mixer.Channel(8).play(sound9, loops=-1)
    sounds.append(sound9)

    sound10 = pygame.mixer.Sound(soundsList.item(soundBoard[9])['text'])
    sound10.set_volume(1.0)
    # pygame.mixer.Channel(9).play(sound10, loops=-1)
    sounds.append(sound10)

    sound11 = pygame.mixer.Sound(soundsList.item(soundBoard[10])['text'])
    sound11.set_volume(1.0)
    # pygame.mixer.Channel(10).play(sound11, loops=-1)
    sounds.append(sound11)

    sound12 = pygame.mixer.Sound(soundsList.item(soundBoard[11])['text'])
    sound12.set_volume(1.0)
    # pygame.mixer.Channel(11).play(sound12, loops=-1)
    sounds.append(sound12)

    # pressed = [False, False, False, False, False, False, False, False, False, False, False, False]

    while playSound:
        touch.gui_sense(soundBoard, soundsList, sounds)
        # pressed = touch.gui_sense(soundBoard, soundsList, sounds, pressed)
        if GPIO.input(19):
            for x in sounds:
                x.stop()
            break

def load_in_soundBoard():
    global soundBoard
    # use rfid.read()
    soundBoard = rfid.gui_read()
    print('read')
    for i in range(12):
        soundName = soundsList.item(soundBoard[i])['values'][0]
        boardDisplay[i].configure(text=f'sound {str(i+1)}:\n{soundName}')

def save_soundBoard():
    # use rfid.write()
    rfid.gui_write(soundBoard)
    print('write')

soundID = 1
def add_samples(directory, parent):
    global soundID
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            soundsList.insert(parent, tk.END, iid=soundID, value=(item,), text=str(path))
            soundID += 1
        elif os.path.isdir(path):
            folder = soundsList.insert(parent, tk.END, value=item)
            add_samples(path, folder)

window = tk.Tk()
window.title('Soundboard Builder')
window.geometry('1400x650')
sv_ttk.set_theme('light')

sounds = ttk.Frame(window)
sounds.grid(row=0, column=0, sticky='nsew', padx = 10, pady=50)

soundsList = ttk.Treeview(sounds, columns='Sounds', show='headings', height=13)
soundsList.heading('Sounds', text='Sounds')
directory = 'samples'
add_samples(directory, '')

soundsList.grid(row=0, column=0, sticky='nsew', padx=3)

soundsScroll = ttk.Scrollbar(sounds, orient=tk.VERTICAL, command=soundsList.yview)
soundsList.configure(yscroll=soundsScroll.set)
soundsScroll.grid(row=0, column=1, sticky='ns')

soundBoardDisplay = ttk.Frame(window)
soundBoardDisplay.grid(row=0, column=1, sticky='nsew', padx = 20)

sound1 = Label(soundBoardDisplay, text='sound 1:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound1.grid(row=0, column=0, sticky='nsew', padx=20, pady=50)

sound2 = Label(soundBoardDisplay, text='sound 2:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound2.grid(row=0, column=1, sticky='nsew', padx=20, pady=50)

sound3 = Label(soundBoardDisplay, text='sound 3:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound3.grid(row=0, column=2, sticky='nsew', padx=20, pady=50)

sound4 = Label(soundBoardDisplay, text='sound 4:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound4.grid(row=0, column=3, sticky='nsew', padx=20, pady=50)

sound5 = Label(soundBoardDisplay, text='sound 5:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound5.grid(row=0, column=4, sticky='nsew', padx=20, pady=50)

sound6 = Label(soundBoardDisplay, text='sound 6:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound6.grid(row=0, column=5, sticky='nsew', padx=20, pady=50)

sound7 = Label(soundBoardDisplay, text='sound 7:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound7.grid(row=1, column=0, sticky='nsew', padx=20, pady=50)

sound8 = Label(soundBoardDisplay, text='sound 8:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound8.grid(row=1, column=1, sticky='nsew', padx=20, pady=50)

sound9 = Label(soundBoardDisplay, text='sound 9:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound9.grid(row=1, column=2, sticky='nsew', padx=20, pady=50)

sound10 = Label(soundBoardDisplay, text='sound 10:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound10.grid(row=1, column=3, sticky='nsew', padx=20, pady=50)

sound11 = Label(soundBoardDisplay, text='sound 11:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound11.grid(row=1, column=4, sticky='nsew', padx=20, pady=50)

sound12 = Label(soundBoardDisplay, text='sound 12:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound12.grid(row=1, column=5, sticky='nsew', padx=20, pady=50)

boardDisplay = [sound1, sound2, sound3, sound4, sound5, sound6, sound7, sound8, sound9, sound10, sound11, sound12]

addSound = ttk.Button(sounds, text='Add Sound', style='Accent.TButton', command=lambda:add_sound(boardDisplay))
addSound.grid(row=2, column=0, sticky='s', pady=10)

playSound = ttk.Button(sounds, text='Play Sound', style='Accent.TButton', command=lambda:play_sound())
playSound.grid(row=3, column=0, sticky='s', pady=10)

clearSound = ttk.Button(soundBoardDisplay, text='Clear Soundboard', style='Accent.TButton', command=lambda:clear_soundboard(boardDisplay))
clearSound.grid(row=2, column=5, sticky='s', pady=10)

loadSound = ttk.Button(soundBoardDisplay, text='Load Soundboard', style='Accent.TButton', command=lambda:load_onto_soundboard(True))
loadSound.grid(row=3, column=4, sticky='s', pady=10)

stopSound = ttk.Button(soundBoardDisplay, text='Stop Soundboard', style='Accent.TButton', command=lambda:load_onto_soundboard(False))
stopSound.grid(row=3, column=5, sticky='s', pady=10)

addButtons = ttk.Frame(window)
addButtons.grid(row=1, column=0, sticky='nsew', padx = 10)

button1 = ttk.Button(addButtons, text='1', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 1))
button1.grid(row=0, column=0, sticky='nsew', padx=3, pady=3)

button2 = ttk.Button(addButtons, text='2', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 2))
button2.grid(row=0, column=1, sticky='nsew', padx=3, pady=3)

button3 = ttk.Button(addButtons, text='3', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 3))
button3.grid(row=0, column=2, sticky='nsew', padx=3, pady=3)

button4 = ttk.Button(addButtons, text='4', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 4))
button4.grid(row=0, column=3, sticky='nsew', padx=3, pady=3)

button5 = ttk.Button(addButtons, text='5', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 5))
button5.grid(row=0, column=4, sticky='nsew', padx=3, pady=3)

button6 = ttk.Button(addButtons, text='6', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 6))
button6.grid(row=0, column=5, sticky='nsew', padx=3, pady=3)

button7 = ttk.Button(addButtons, text='7', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 7))
button7.grid(row=1, column=0, sticky='nsew', padx=3, pady=3)

button8 = ttk.Button(addButtons, text='8', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 8))
button8.grid(row=1, column=1, sticky='nsew', padx=3, pady=3)

button9 = ttk.Button(addButtons, text='9', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 9))
button9.grid(row=1, column=2, sticky='nsew', padx=3, pady=3)

button10 = ttk.Button(addButtons, text='10', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 10))
button10.grid(row=1, column=3, sticky='nsew', padx=3, pady=3)

button11 = ttk.Button(addButtons, text='11', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 11))
button11.grid(row=1, column=4, sticky='nsew', padx=3, pady=3)

button12 = ttk.Button(addButtons, text='12', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 12))
button12.grid(row=1, column=5, sticky='nsew', padx=3, pady=3)

readWrite = ttk.Frame(window)
readWrite.grid(row=1, column=1, sticky='nsew', padx = 470)

readButton = ttk.Button(readWrite, text='Read', style='Accent.TButton', command=lambda:load_in_soundBoard())
readButton.grid(row=0, column=3, sticky='nsew', padx=20, pady=3)

writeButton = ttk.Button(readWrite, text='Write', style='Accent.TButton', command=lambda:save_soundBoard())
writeButton.grid(row=0, column=4, sticky='nsew', padx=20, pady=3)

lcd.lcd_start()
lcd.lcd_string('touch ready', lcd.LCD_LINE_1)
pygame.mixer.init()
pygame.mixer.set_num_channels(12)  # default is 8
window.mainloop()