import tkinter as tk
from tkinter import ttk
from tkinter import *
import sv_ttk
import os
from tkinter.messagebox import showinfo

import touch
import rfid
import lcd
import speaker
import button
import RPi.GPIO as GPIO

numSounds = 0
soundBoard = ['', '', '', '', '', '', '', '', '', '', '', '']
def add_sound(boardDisplay):
    global numSounds
    global soundBoard
    selected_sound = soundsList.selection()[0]
    soundPath = soundsList.item(selected_sound)['text']
    soundName = soundsList.item(selected_sound)['values'][0]
    if numSounds < 12:
        if soundName[-4:] == '.mp3' or soundName[-4:] == '.wav':
            for i in range(12):
                if soundBoard[i] == '':
                    boardDisplay[i].configure(text=f'sound {str(i+1)}:\n{soundName}')
                    soundBoard[i] = soundPath
                    numSounds += 1
                    print(soundBoard)
                    break

def add_sound_spot(boardDisplay, position):
    global numSounds
    global soundBoard
    selected_sound = soundsList.selection()[0]
    soundPath = soundsList.item(selected_sound)['text']
    soundName = soundsList.item(selected_sound)['values'][0]
    if soundName[-4:] == '.mp3' or soundName[-4:] == '.wav':
        boardDisplay[position-1].configure(text=f'sound {str(position)}:\n{soundName}')
        soundBoard[position-1] = soundPath
        print(soundBoard)
   
def clear_soundboard(boardDisplay):
    global numSounds
    for i in range(12):
        boardDisplay[i].configure(text=f'sound {i+1}:\n')
        soundBoard[i] = ''
    numSounds = 0

def play_sound():
    selected_sound = soundsList.selection()[0]
    soundPath = soundsList.item(selected_sound)['text']
    if soundPath[-4:] == '.mp3' or soundPath[-4:] == '.wav':
        print(f'played sound {soundPath}')
        # play sound

def load_in_soundBoard():
    # use rfid.read()
    rfid.read()
    print('read')

def save_soundBoard():
    # use rfid.write()
    rfid.gui_write(soundBoard)
    print('write')

def add_samples(directory, parent):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            soundsList.insert(parent, tk.END, value=(item,), text=str(path))
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
readWrite.grid(row=1, column=1, sticky='nsew', padx = 380)

readButton= ttk.Button(readWrite, text='Read', style='Accent.TButton', command=lambda:load_in_soundBoard())
readButton.grid(row=0, column=3, sticky='nsew', padx=20, pady=3)

writeButton= ttk.Button(readWrite, text='Write', style='Accent.TButton', command=lambda:save_soundBoard())
writeButton.grid(row=0, column=4, sticky='nsew', padx=20, pady=3)

lcd.lcd_start()
lcd.lcd_string('touch ready', lcd.LCD_LINE_1)
window.mainloop()