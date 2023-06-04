import tkinter as tk
from tkinter import ttk
import sv_ttk
import os
from tkinter.messagebox import showinfo

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
window.geometry('620x400')
sv_ttk.set_theme('light')

sounds = ttk.Frame(window)
sounds.grid(row=0, column=0, sticky='nsew')

soundsList = ttk.Treeview(sounds, columns='Sounds', show='headings', height=13)
soundsList.heading('Sounds', text='Sounds')
directory = 'samples'
add_samples(directory, '')

soundsList.grid(row=0, column=0, sticky='nsew')

soundsScroll = ttk.Scrollbar(sounds, orient=tk.VERTICAL, command=soundsList.yview)
soundsList.configure(yscroll=soundsScroll.set)
soundsScroll.grid(row=0, column=1, sticky='ns')

addSound = ttk.Button(sounds, text='Add Sound', style='Accent.TButton')
addSound.grid(row=1, column=0, sticky='s', pady=10)

sounds.pack(side=tk.LEFT, anchor=tk.N)
window.mainloop()