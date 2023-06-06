import tkinter as tk
from tkinter import ttk
from tkinter import *
import sv_ttk
import os
import pygame

import file
import touch
import rfid
import lcd

##################### SPOTIFY API #####################
import spotipy
from spotipy.oauth2 import SpotifyOAuth

username = '21qhraopzibkwwradhzjxpjla'
clientID = '39f9ba37851448068fd71b68b88dec3b'
clientSecret = 'd9ea3a914c114f5d9781eb62db2b37bc'
redirect_uri = 'http://google.com/callback/'
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirect_uri))
##################### SPOTIFY API #####################

##################### GLOBAL VARIABLES #####################
numSounds = 0
soundBoard = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
songPlaying = False
resume_position = 0
songURI = ''
##################### GLOBAL VARIABLES #####################

# get spotify song uri
def get_songURI(songName):
    global songURI
    results = spotifyObject.search(songName, 1, 0, "track")
    songs_dict = results['tracks']
    song_items = songs_dict['items']
    songURL = song_items[0]['external_urls']['spotify']
    uri = songURL.split('/')[-1].split('?')[0]
    songURI = 'spotify:track:' + uri

# play spotify song
def play_song(songName):
    global songPlaying
    global songURI
    get_songURI(songName)
    sp.start_playback(uris=[songURI])
    songPlaying = True

# pause spotify song
def pause_song():
    global songPlaying
    global resume_position
    if songPlaying:
        sp.pause_playback()
        playback = sp.current_playback()
        if playback and 'progress_ms' in playback:
            resume_position = playback['progress_ms']
        songPlaying = False

# resume spotify song
def resume_song():
    global songPlaying
    global resume_position
    global songURI
    if not songPlaying:
        sp.start_playback(uris=[songURI], position_ms=resume_position)
        songPlaying = True

# restart spotify song
def restart_song():
    global songPlaying
    global songURI
    sp.start_playback(uris=[songURI])
    songPlaying = True

# add sound bite to soundboard sequentially
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

# add sound bit to specific spot on soundboard
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
        numSounds += 1
        print(soundBoard)

# clear specific spot on soundboard
def clear_sound_spot(boardDisplay, position):
    global numSounds
    global soundBoard
    boardDisplay[position-1].configure(text=f'sound {str(position)}:\n')
    soundBoard[position-1] = '0'
    numSounds -= 1

# clear whole soundboard 
def clear_soundboard(boardDisplay):
    global numSounds
    for i in range(12):
        boardDisplay[i].configure(text=f'sound {i+1}:\n')
        soundBoard[i] = '0'
    numSounds = 0

# play sound bite from GUI
def play_sound():
    selected_sound = soundsList.selection()[0]
    soundPath = soundsList.item(selected_sound)['text']
    if soundPath[-4:] == '.ogg':
        pygame.mixer.music.load(soundPath)
        pygame.mixer.music.play()
        print(f'played sound {soundPath}')

# start playing soundboard
def load_onto_soundboard(playSound):
    sounds = []
    if soundBoard[0] != '0':
        sound1 = pygame.mixer.Sound(soundsList.item(soundBoard[0])['text'])
        sound1.set_volume(1.0)
    else: 
        sound1 = ''
    sounds.append(sound1)

    if soundBoard[1] != '0':
        sound2 = pygame.mixer.Sound(soundsList.item(soundBoard[1])['text'])
        sound2.set_volume(1.0)
    else:
        sound2 = ''
    sounds.append(sound2)

    if soundBoard[2] != '0':
        sound3 = pygame.mixer.Sound(soundsList.item(soundBoard[2])['text'])
        sound3.set_volume(1.0)
    else:
        sound3 = ''
    sounds.append(sound3)

    if soundBoard[3] != '0':
        sound4 = pygame.mixer.Sound(soundsList.item(soundBoard[3])['text'])
        sound4.set_volume(1.0)
    else:
        sound4 = ''
    sounds.append(sound4)

    if soundBoard[4] != '0':
        sound5 = pygame.mixer.Sound(soundsList.item(soundBoard[4])['text'])
        sound5.set_volume(1.0)
    else:
        sound5 = ''
    sounds.append(sound5)

    if soundBoard[5] != '0':
        sound6 = pygame.mixer.Sound(soundsList.item(soundBoard[5])['text'])
        sound6.set_volume(1.0)
    else:
        sound6 = ''
    sounds.append(sound6)
    
    if soundBoard[6] != '0':
        sound7 = pygame.mixer.Sound(soundsList.item(soundBoard[6])['text'])
        sound7.set_volume(1.0)
    else:
        sound7 = ''
    sounds.append(sound7)
    
    if soundBoard[7] != '0':
        sound8 = pygame.mixer.Sound(soundsList.item(soundBoard[7])['text'])
        sound8.set_volume(1.0)
    else:
        sound8 = ''
    sounds.append(sound8)

    if soundBoard[8] != '0':
        sound9 = pygame.mixer.Sound(soundsList.item(soundBoard[8])['text'])
        sound9.set_volume(1.0)
    else:
        sound9 = ''
    sounds.append(sound9)

    if soundBoard[9] != '0':
        sound10 = pygame.mixer.Sound(soundsList.item(soundBoard[9])['text'])
        sound10.set_volume(1.0)
    else:
        sound10 = ''
    sounds.append(sound10)

    if soundBoard[10] != '0':
        sound11 = pygame.mixer.Sound(soundsList.item(soundBoard[10])['text'])
        sound11.set_volume(1.0)
    else:
        sound11 = ''
    sounds.append(sound11)

    if soundBoard[11] != '0':
        sound12 = pygame.mixer.Sound(soundsList.item(soundBoard[11])['text'])
        sound12.set_volume(1.0)
    else:
        sound12 = ''
    sounds.append(sound12)

    touch.main(sounds)

# scan RFID to load a saved soundboard
def load_in_soundBoard():
    global soundBoard
    # use rfid.read()
    soundBoard = rfid.gui_read()
    print('read')
    for i in range(12):
        if soundBoard[i] != '0':
            soundName = soundsList.item(soundBoard[i])['values'][0]
            boardDisplay[i].configure(text=f'sound {str(i+1)}:\n{soundName}')
        else:
            boardDisplay[i].configure(text=f'sound {str(i+1)}:\n')

# write soundboard onto RFID card
def save_soundBoard():
    # use rfid.write()
    rfid.gui_write(soundBoard)
    print('write')

# locally save soundboard
def local_save_soundBoard(fileName):
    if fileName == '':
        return
    else:
        filePath = 'localSave/' + fileName + '.txt'
        print(filePath)

    text = ''
    for i in range(12):
        if i < 11:
            text += soundBoard[i] + ','
        else:
            text += soundBoard[i]
    
    with open(filePath, 'w') as txtFile:
        txtFile.write(text)
    
    inputName.delete(0, END)
    reloadSaves()

# load in locally saved soundboard 
def local_load_soundBoard():
    global soundBoard
    soundBoard = []

    selected_board = localSaveList.selection()[0]
    boardPath = localSaveList.item(selected_board)['text']

    with open(boardPath, 'r') as txtFile:
        text = txtFile.read()
    print(text)
    soundBoard = text.split(',')
    soundBoard[11] = soundBoard[11].strip()
    print(soundBoard)
    for i in range(12):
        if soundBoard[i] != '0':
            soundName = soundsList.item(soundBoard[i])['values'][0]
            boardDisplay[i].configure(text=f'sound {str(i+1)}:\n{soundName}')
        else:
            boardDisplay[i].configure(text=f'sound {str(i+1)}:\n')

# refresh treeview of locally saved soundboard each time new soundboard is saved
def reloadSaves():
    localSaveList.delete(*localSaveList.get_children())
    add_saves('localSave', '')

# delete locally saved soundboard
def delete_board():
    selected_board = localSaveList.selection()[0]
    boardPath = localSaveList.item(selected_board)['text']
    localSaveList.delete(selected_board)
    os.remove(boardPath)

# initialize GUI treeview of all available sounds
def add_samples(directory, parent):
    sorted_dir = sorted(os.listdir(directory))
    for item in sorted_dir:
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if item[-4:] == '.ogg':
                soundsList.insert(parent, tk.END, iid=file.name_ID[item], value=(item,), text=str(path))
        elif os.path.isdir(path):
            folder = soundsList.insert(parent, tk.END, value=item)
            add_samples(path, folder)

# initialize GUI treeview of all locally saved soundboards
def add_saves(directory, parent):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if item[-4:] == '.txt':
                localSaveList.insert(parent, tk.END, value=(item,), text=str(path))
        elif os.path.isdir(path):
            folder = localSaveList.insert(parent, tk.END, value=item)
            add_samples(path, folder)


##################### GUI #####################
window = tk.Tk()
window.title('Soundboard Builder')
window.geometry('1450x750')
sv_ttk.set_theme('light')

tabControl = ttk.Notebook(window)
mainTab = ttk.Frame(tabControl)
localTab = ttk.Frame(tabControl)
spotifyTab = ttk.Frame(tabControl)
tabControl.add(mainTab, text='Build Your Soundboard')
tabControl.add(localTab, text='Save & Load Soundboard Locally')
tabControl.add(spotifyTab, text='Spotify')
tabControl.pack(expand=1, fill='both')

soundsFrame = ttk.Frame(mainTab)
soundsFrame.grid(row=0, column=0, sticky='nsew', padx = 10, pady=50)

soundsList = ttk.Treeview(soundsFrame, columns='Sounds', show='headings', height=13)
soundsList.heading('Sounds', text='Sounds')
directory = 'samples'
add_samples(directory, '')

soundsList.grid(row=0, column=0, sticky='nsew', padx=3)

soundsScroll = ttk.Scrollbar(soundsFrame, orient=tk.VERTICAL, command=soundsList.yview)
soundsList.configure(yscroll=soundsScroll.set)
soundsScroll.grid(row=0, column=1, sticky='ns')

soundBoardDisplayFrame = ttk.Frame(mainTab)
soundBoardDisplayFrame.grid(row=0, column=1, sticky='nsew', padx = 20)

sound1 = Label(soundBoardDisplayFrame, text='sound 1:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound1.grid(row=0, column=0, sticky='nsew', padx=20, pady=50)

sound2 = Label(soundBoardDisplayFrame, text='sound 2:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound2.grid(row=0, column=1, sticky='nsew', padx=20, pady=50)

sound3 = Label(soundBoardDisplayFrame, text='sound 3:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound3.grid(row=0, column=2, sticky='nsew', padx=20, pady=50)

sound4 = Label(soundBoardDisplayFrame, text='sound 4:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound4.grid(row=0, column=3, sticky='nsew', padx=20, pady=50)

sound5 = Label(soundBoardDisplayFrame, text='sound 5:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound5.grid(row=0, column=4, sticky='nsew', padx=20, pady=50)

sound6 = Label(soundBoardDisplayFrame, text='sound 6:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound6.grid(row=0, column=5, sticky='nsew', padx=20, pady=50)

sound7 = Label(soundBoardDisplayFrame, text='sound 7:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound7.grid(row=1, column=0, sticky='nsew', padx=20, pady=50)

sound8 = Label(soundBoardDisplayFrame, text='sound 8:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound8.grid(row=1, column=1, sticky='nsew', padx=20, pady=50)

sound9 = Label(soundBoardDisplayFrame, text='sound 9:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound9.grid(row=1, column=2, sticky='nsew', padx=20, pady=50)

sound10 = Label(soundBoardDisplayFrame, text='sound 10:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound10.grid(row=1, column=3, sticky='nsew', padx=20, pady=50)

sound11 = Label(soundBoardDisplayFrame, text='sound 11:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound11.grid(row=1, column=4, sticky='nsew', padx=20, pady=50)

sound12 = Label(soundBoardDisplayFrame, text='sound 12:\n', width=15, height=5, borderwidth=3, relief='ridge')
sound12.grid(row=1, column=5, sticky='nsew', padx=20, pady=50)

boardDisplay = [sound1, sound2, sound3, sound4, sound5, sound6, sound7, sound8, sound9, sound10, sound11, sound12]

addSound = ttk.Button(soundsFrame, text='Add Sound', style='Accent.TButton', command=lambda:add_sound(boardDisplay))
addSound.grid(row=2, column=0, sticky='s', pady=10)

playSound = ttk.Button(soundsFrame, text='Play Sound', style='Accent.TButton', command=lambda:play_sound())
playSound.grid(row=3, column=0, sticky='s', pady=10)

clearSound = ttk.Button(soundBoardDisplayFrame, text='Clear Soundboard', style='Accent.TButton', command=lambda:clear_soundboard(boardDisplay))
clearSound.grid(row=2, column=5, sticky='s', pady=10)

loadSound = ttk.Button(soundBoardDisplayFrame, text='Load Soundboard', style='Accent.TButton', command=lambda:load_onto_soundboard(True))
loadSound.grid(row=2, column=4, sticky='s', pady=10)

addButtonsFrame = ttk.Frame(mainTab)
addButtonsFrame.grid(row=1, column=0, sticky='nsew', padx = 10)

button1 = ttk.Button(addButtonsFrame, text='1', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 1))
button1.grid(row=0, column=0, sticky='nsew', padx=3, pady=3)

button2 = ttk.Button(addButtonsFrame, text='2', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 2))
button2.grid(row=0, column=1, sticky='nsew', padx=3, pady=3)

button3 = ttk.Button(addButtonsFrame, text='3', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 3))
button3.grid(row=0, column=2, sticky='nsew', padx=3, pady=3)

button4 = ttk.Button(addButtonsFrame, text='4', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 4))
button4.grid(row=0, column=3, sticky='nsew', padx=3, pady=3)

button5 = ttk.Button(addButtonsFrame, text='5', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 5))
button5.grid(row=0, column=4, sticky='nsew', padx=3, pady=3)

button6 = ttk.Button(addButtonsFrame, text='6', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 6))
button6.grid(row=0, column=5, sticky='nsew', padx=3, pady=3)

button7 = ttk.Button(addButtonsFrame, text='7', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 7))
button7.grid(row=1, column=0, sticky='nsew', padx=3, pady=3)

button8 = ttk.Button(addButtonsFrame, text='8', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 8))
button8.grid(row=1, column=1, sticky='nsew', padx=3, pady=3)

button9 = ttk.Button(addButtonsFrame, text='9', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 9))
button9.grid(row=1, column=2, sticky='nsew', padx=3, pady=3)

button10 = ttk.Button(addButtonsFrame, text='10', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 10))
button10.grid(row=1, column=3, sticky='nsew', padx=3, pady=3)

button11 = ttk.Button(addButtonsFrame, text='11', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 11))
button11.grid(row=1, column=4, sticky='nsew', padx=3, pady=3)

button12 = ttk.Button(addButtonsFrame, text='12', style='Accent.TButton', command=lambda:add_sound_spot(boardDisplay, 12))
button12.grid(row=1, column=5, sticky='nsew', padx=3, pady=3)

clearButtonsFrame = ttk.Frame(mainTab)
clearButtonsFrame.grid(row=2, column=0, sticky='nsew', padx = 10, pady=30)

cbutton_style = ttk.Style()
cbutton_style.configure('Custom.TButton', background='red')

cbutton1 = Button(clearButtonsFrame, text='1', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 1))
cbutton1.grid(row=0, column=0, sticky='nsew', padx=3, pady=3)

cbutton2 = Button(clearButtonsFrame, text='2', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 2))
cbutton2.grid(row=0, column=1, sticky='nsew', padx=3, pady=3)

cbutton3 = Button(clearButtonsFrame, text='3', bg='red', fg='white',  command=lambda:clear_sound_spot(boardDisplay, 3))
cbutton3.grid(row=0, column=2, sticky='nsew', padx=3, pady=3)

cbutton4 = Button(clearButtonsFrame, text='4', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 4))
cbutton4.grid(row=0, column=3, sticky='nsew', padx=3, pady=3)

cbutton5 = Button(clearButtonsFrame, text='5', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 5))
cbutton5.grid(row=0, column=4, sticky='nsew', padx=3, pady=3)

cbutton6 = Button(clearButtonsFrame, text='6', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 6))
cbutton6.grid(row=0, column=5, sticky='nsew', padx=3, pady=3)

cbutton7 = Button(clearButtonsFrame, text='7', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 7))
cbutton7.grid(row=1, column=0, sticky='nsew', padx=3, pady=3)

cbutton8 = Button(clearButtonsFrame, text='8', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 8))
cbutton8.grid(row=1, column=1, sticky='nsew', padx=3, pady=3)

cbutton9 = Button(clearButtonsFrame, text='9', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 9))
cbutton9.grid(row=1, column=2, sticky='nsew', padx=3, pady=3)

cbutton10 = Button(clearButtonsFrame, text='10', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 10))
cbutton10.grid(row=1, column=3, sticky='nsew', padx=3, pady=3)

cbutton11 = Button(clearButtonsFrame, text='11', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 11))
cbutton11.grid(row=1, column=4, sticky='nsew', padx=3, pady=3)

cbutton12 = Button(clearButtonsFrame, text='12', bg='red', fg='white', command=lambda:clear_sound_spot(boardDisplay, 12))
cbutton12.grid(row=1, column=5, sticky='nsew', padx=3, pady=3)


read_writeFrame = ttk.Frame(mainTab)
read_writeFrame.grid(row=1, column=1, sticky='nsew', padx=400)

readButton = ttk.Button(read_writeFrame, text='Scan RFID Tag', style='Accent.TButton', command=lambda:load_in_soundBoard())
readButton.grid(row=0, column=3, sticky='nsew', padx=20, pady=3)

writeButton = ttk.Button(read_writeFrame, text='Write to RFID Tag', style='Accent.TButton', command=lambda:save_soundBoard())
writeButton.grid(row=0, column=4, sticky='nsew', padx=20, pady=3)

localFrame = ttk.Frame(localTab)
localFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

localSaveFrame = ttk.Frame(localFrame)
localSaveFrame.grid(row=0, column=0, sticky='nsew', padx=10)

prompt = Label(localSaveFrame, text='Enter a name for your soundboard:')
prompt.grid(row=0, column=0)

inputName = Entry(localSaveFrame)
inputName.grid(row=1, column=0, padx=10)

localSaveButton = ttk.Button(localSaveFrame, text='Save', style='Accent.TButton', command=lambda:local_save_soundBoard(inputName.get()))
localSaveButton.grid(row=2, column=0, pady=10)

localLoadFrame = ttk.Frame(localFrame)
localLoadFrame.grid(row=0, column=1, sticky='nsew', padx = 10)

localSaveList = ttk.Treeview(localLoadFrame, columns='Local_Saves', show='headings', height=13)
localSaveList.heading('Local_Saves', text='Local Saves')
directory = 'localSave'
add_saves(directory, '')

localSaveList.grid(row=0, column=0, sticky='nsew', padx=3)

localSaveScroll = ttk.Scrollbar(localLoadFrame, orient=tk.VERTICAL, command=localSaveList.yview)
localSaveList.configure(yscroll=localSaveScroll.set)
localSaveScroll.grid(row=0, column=1, sticky='ns')

loadBoard = ttk.Button(localLoadFrame, text='Load in Soundboard', style='Accent.TButton', command=lambda:local_load_soundBoard())
loadBoard.grid(row=2, column=0, sticky='s', pady=10)

deleteBoard = ttk.Button(localLoadFrame, text='Delete Soundboard', style='Accent.TButton', command=lambda:delete_board())
deleteBoard.grid(row=3, column=0, sticky='s', pady=10)

spotifyFrame = ttk.Frame(spotifyTab)
spotifyFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

searchPromptFrame = ttk.Frame(spotifyFrame)
searchPromptFrame.grid(row=0, column=0, padx=10, pady=10)

spotifyPrompt = Label(searchPromptFrame, text='Enter a song name:')
spotifyPrompt.grid(row=0, column=0)

searchSong = Entry(searchPromptFrame, highlightbackground='#1D8954')
searchSong.grid(row=1, column=0, padx=10)

spotifyButtonsFrame = ttk.Frame(spotifyFrame)
spotifyButtonsFrame.grid(row=1, column=0, padx=10, pady=10)

playSongButton = Button(spotifyButtonsFrame, text='Play', bg='#1D8954', fg='white', command=lambda:play_song(searchSong.get()))
playSongButton.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

pauseSongButton = Button(spotifyButtonsFrame, text='Pause', bg='#1D8954', fg='white', command=lambda:pause_song())
pauseSongButton.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

resumeSongButton = Button(spotifyButtonsFrame, text='Resume', bg='#1D8954', fg='white', command=lambda:resume_song())
resumeSongButton.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

restartSongButton = Button(spotifyButtonsFrame, text='Restart', bg='#1D8954', fg='white', command=lambda:restart_song())
restartSongButton.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)


lcd.lcd_start()
lcd.lcd_string('touch ready', lcd.LCD_LINE_1)
pygame.mixer.init()
pygame.mixer.set_num_channels(12)
window.mainloop()
sp.pause_playback()