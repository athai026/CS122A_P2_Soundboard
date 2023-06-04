import tkinter as tk
from tkinter import ttk
from tkinter import *
import sv_ttk
import os
from tkinter.messagebox import showinfo

numSounds = 0
def change_label(soundBoard):
    global numSounds
    if numSounds < 12:
        soundBoard[numSounds].configure(text=f'new text: {numSounds}')
        numSounds += 1

def clear_soundboard(soundBoard):
    global numSounds
    for i in range(12):
        soundBoard[i].configure(text=f'sound {i+1}:\n')
    numSounds = 0

def add_samples(directory, parent):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            soundsList.insert(parent, tk.END, value=item)
        elif os.path.isdir(path):
            folder = soundsList.insert(parent, tk.END, value=item)
            add_samples(path, folder)

window = tk.Tk()
window.title('Soundboard Builder')
window.geometry('1200x480')
sv_ttk.set_theme('light')

sounds = ttk.Frame(window)
sounds.grid(row=0, column=0, sticky='nsew', pady=50)

soundsList = ttk.Treeview(sounds, columns='Sounds', show='headings', height=13)
soundsList.heading('Sounds', text='Sounds')
directory = 'samples'
add_samples(directory, '')

soundsList.grid(row=0, column=0, sticky='nsew')

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

soundBoard = [sound1, sound2, sound3, sound4, sound5, sound6, sound7, sound8, sound9, sound10, sound11, sound12]

addSound = ttk.Button(sounds, text='Add Sound', style='Accent.TButton', command=lambda:change_label(soundBoard))
addSound.grid(row=1, column=0, sticky='s', pady=10)

clearSound = ttk.Button(soundBoardDisplay, text='Clear Soundboard', style='Accent.TButton', command=lambda:clear_soundboard(soundBoard))
clearSound.grid(row=2, column=5, sticky='s', pady=10)

window.mainloop()