import touch
import rfid
import lcd
import speaker
import file
import button
import RPi.GPIO as GPIO
from enum import Enum
import pickle
import os
import pygame

############################## SPOTIFY API ##############################
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
############################## SPOTIFY API ##############################

############################## GLOBAL VARIABLES ##############################
numTasks = 3
period_gcd = 0.01
songPlaying = False
songURI = ''
resume_position = 0
nameToPath = file.name_path # name to path
nameToID = file.name_ID # name to ID
IDtoName = file.soundID_name # ID to name
numSounds = 0
soundBoard = []
save = []
pressed = [False, False, False, False, False, False, False, False, False, False, False, False]
############################## GLOBAL VARIABLES ##############################

############################## TASK SCHEDULER CLASS ##############################
class task:
    def __init__(self, state, period, elapsedTime, func):
        self.state = state
        self.period = period
        self.elapsedTime = elapsedTime
        self.func = func
############################## TASK SCHEDULER CLASS ##############################

############################## SPOTIFY TASK ##############################
class spotifyStates(Enum):
    startSpot = 1
    waitSearch = 2
    searchSpot = 3
    playRestart = 4
    pauseSong = 5
    resumeSong = 6
    pauseRelease = 7
    resumeRelease = 8
    waitAction = 9

spotifyState = Enum('spotifyStates', ['startSpot', 'waitSearch', 'searchSpot', 'playRestart', 'pauseSong', 'resumeSong', 'pauseRelease', 'resumeRelease', 'waitAction'])

def Spotify(state):
    global songPlaying
    global songURI
    global resume_position

    # transitions
    if state == spotifyState.startSpot:
        state = spotifyState.waitSearch
    elif state == spotifyState.waitSearch:
        if GPIO.input(13):
            state = spotifyState.searchSpot
        else:
            state = spotifyState.waitSearch
    elif state == spotifyState.searchSpot:
        if GPIO.input(6):
            state = spotifyState.playRestart
        else:
            state = spotifyState.waitAction
    elif state == spotifyState.playRestart:
        state = spotifyState.waitAction
    elif state == spotifyState.pauseSong:
        if GPIO.input(5):
            state = spotifyState.pauseRelease
        else:
            state = spotifyState.waitAction
    elif state == spotifyState.resumeSong:
        if GPIO.input(5):
            state = spotifyState.resumeRelease
        else:
            state = spotifyState.waitAction
    elif state == spotifyState.pauseRelease:
        if not GPIO.input(5):
            state = spotifyState.waitAction
        else:
            state = spotifyState.pauseRelease
    elif state == spotifyState.resumeRelease:
        if not GPIO.input(5):
            state = spotifyState.waitAction
        else:
            state = spotifyState.resumeRelease
    elif state == spotifyState.waitAction:
        if GPIO.input(6): 
            state = spotifyState.playRestart
        elif GPIO.input(5):
            if songPlaying:
                state = spotifyState.pauseSong
            else:
                state = spotifyState.resumeSong
        elif GPIO.input(13):
            state = spotifyState.searchSpot
    else:
        state = spotifyState.startSpot

    # state actions
    if state == spotifyState.startSpot:
        state = spotifyState.waitSearch
    elif state == spotifyState.searchSpot:
        songName = input('Enter song name: ')
        results = spotifyObject.search(songName, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        songURL = song_items[0]['external_urls']['spotify']
        uri = songURL.split('/')[-1].split('?')[0]
        songURI = 'spotify:track:' + uri
    elif state == spotifyState.playRestart:
        sp.start_playback(uris=[songURI])
        songPlaying = True
    elif state == spotifyState.pauseSong:
        if songPlaying:
            sp.pause_playback()
            playback = sp.current_playback()
            if playback and 'progress_ms' in playback:
                resume_position = playback['progress_ms']
        songPlaying = False
    elif state == spotifyState.resumeSong:
        if not songPlaying:
            sp.start_playback(uris=[songURI], position_ms=resume_position)
            songPlaying = True

    return state
############################## SPOTIFY TASK ##############################

############################# TOUCH TASK ##############################
class touchStates(Enum):
    startTouch = 1
    senseTouch = 2

touchState = Enum('touchStates', ['startTouch', 'senseTouch'])


def Touch(state):
    global pressed
    global soundBoard

    # transitions
    if state == touchState.startTouch:
        state = touchState.senseTouch
    elif state == touchState.senseTouch:
            state = touchState.senseTouch

    # state actions
    if state == touchState.senseTouch:
        for i in range(12):
            if touch.mpr121[i].value:
                print("Input {} touched!".format(i+1))
                lcd.lcd_string("Sound {} touched".format(i+1), lcd.LCD_LINE_1)
                lcd.lcd_string('', lcd.LCD_LINE_2)
                if soundBoard[i]:
                    if not pressed[i]:
                        pygame.mixer.Channel(i).play(soundBoard[i])
                        pressed[i] = True
            else:
                pressed[i] = False

    
    return state
############################# TOUCH TASK ##############################

############################## SAVE/LOAD FUNCTION ##############################
class saveLoadStates(Enum):
    start = 1
    waitAction = 2
    saveLocal = 3
    saveLocalRelease = 4
    loadLocal = 5
    loadLocalRelease = 6
    saveRFID = 7
    saveRFIDRelease = 8
    loadRFID = 9
    loadRFIDRelease = 10
    newBoard = 11
    newBoardRelease = 12

saveLoadState = Enum('saveLoadStates', ['start', 'waitAction', 'saveLocal', 'saveLocalRelease', 'loadLocal', 'loadLocalRelease', 'saveRFID', 'saveRFIDRelease', 'loadRFID', 'loadRFIDRelease', 'newBoard', 'newBoardRelease'])

def SaveLoad(state):
    global soundBoard
    global save
    global IDtoName

    # transitions
    if state == saveLoadState.start:
        state = saveLoadState.waitAction
    elif state == saveLoadState.waitAction:
        if GPIO.input(20):
            state = saveLoadState.saveLocal
        elif GPIO.input(21):
            state = saveLoadState.loadLocal
        elif GPIO.input(12):
            state = saveLoadState.saveRFID
        elif GPIO.input(16):
            state = saveLoadState.loadRFID
        elif GPIO.input(22):
            state = saveLoadState.newBoard
        else:
            state = saveLoadState.waitAction
    elif state == saveLoadState.saveLocal:
        if GPIO.input(20):
            state = saveLoadState.saveLocalRelease
        else:
            state = saveLoadState.waitAction
    elif state == saveLoadState.saveLocalRelease:
        if not GPIO.input(20):
            state = saveLoadState.waitAction
        else:
            state = saveLoadState.saveLocalRelease
    elif state == saveLoadState.loadLocal:
        if GPIO.input(21):
            state = saveLoadState.loadLocalRelease
        else:
            state = saveLoadState.waitAction
    elif state == saveLoadState.loadLocalRelease:
        if not GPIO.input(21):
            state = saveLoadState.waitAction
        else:
            state = saveLoadState.loadLocalRelease
    elif state == saveLoadState.saveRFID:
        if GPIO.input(12):
            state = saveLoadState.saveRFIDRelease
        else:
            state = saveLoadState.waitAction
    elif state == saveLoadState.saveRFIDRelease:
        if not GPIO.input(12):
            state = saveLoadState.waitAction
        else:
            state = saveLoadState.saveRDIFRelease
    elif state == saveLoadState.loadRFID:
        if GPIO.input(16):
            state = saveLoadState.loadRFIDRelease
        else:
            state = saveLoadState.waitAction
    elif state == saveLoadState.loadRFIDRelease:
        if not GPIO.input(16):
            state = saveLoadState.waitAction
        else:
            state = saveLoadState.loadRFIDRelease
    elif state == saveLoadState.newBoard:
        if GPIO.input(22):
            state = saveLoadState.newBoardRelease
        else:
            state = saveLoadState.waitAction
    elif state == saveLoadState.newBoardRelease:
        if not GPIO.input(22):
            state = saveLoadState.waitAction
        else:
            state = saveLoadState.newBoardRelease
    else:
        state = saveLoadState.start

    # state actions
    if state == saveLoadState.saveLocal:
        validName = False
        while not validName:
            saveName = input('Enter a name for your soundboard: ')
            if saveName:
                validName = True
            else:
                print('file name cannot be empty string')
        filePath = f'localSave/{saveName}.txt'
        text = ''
        for i in range(12):
            if i < 11:
                text += str(save[i]) + ','
            else:
                text += str(save[i])
        
        with open(filePath, 'w') as txtFile:
            txtFile.write(text)
        print('saved')
    elif state == saveLoadState.loadLocal:
        validFile = False
        while not validFile:
            fileName = input('Enter name of saved soundboard (without .txt): ')
            filePath = f'localSave/{fileName}.txt'
            if os.path.isfile(filePath):
                with open(filePath, 'r') as txtFile:
                    text = txtFile.read()
                print(text)
                save = text.split(',')
                save[11] = save[11].strip()
                validFile = True
            else:
                print('Not a valid file')
        soundBoard = []
        for i in range(12):
            if save[i] != '0':
                tempSound = pygame.mixer.Sound(nameToPath[IDtoName[save[i]]])
                tempSound.set_volume(1.0)
            else: 
                tempSound = ''
            soundBoard.append(tempSound)
        print('loaded')
    elif state == saveLoadState.saveRFID:
        text = ''
        for i in range(12):
            if i < 11:
                text += str(save[i]) + ','
            else:
                text += str(save[i])
        rfid.write(text)
        print('saved')
    elif state == saveLoadState.loadRFID:
        text = rfid.read()
        save = text.split(',')
        save[11] = save[11].strip()
        soundBoard = []
        for i in range(12):
            if save[i] != '0':
                tempSound = pygame.mixer.Sound(nameToPath[IDtoName[save[i]]])
                tempSound.set_volume(1.0)
            else: 
                tempSound = ''
            soundBoard.append(tempSound)
        print('loaded')
    elif state == saveLoadState.newBoard:
        make_soundboard()
    
    return state
############################## SAVE/LOAD FUNCTION ##############################

############################## HELPER FUNCTION ##############################
def make_soundboard():
    global nameToPath
    global nameToID
    global soundBoard
    global save

    soundBoard = []
    save = []

    validSound = False
    print('Press \'Enter\' to leave sound position empty')
   
    while not validSound:
        pos1 = input('Enter name of sound in position 1 (without .ogg): ')
        pos1 += '.ogg'
        if pos1 == '.ogg':
            break
        if pos1 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos1 != '.ogg':
        sound1 = pygame.mixer.Sound(nameToPath[pos1])
        sound1.set_volume(1.0)
        id1 = nameToID[pos1]
    else: 
        sound1 = ''
        id1 = '0'
    soundBoard.append(sound1)
    save.append(id1)

    while not validSound:
        pos2 = input('Enter name of sound in position 2 (without .ogg): ')
        pos2 += '.ogg'
        if pos2 == '.ogg':
            break
        if pos2 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos2 != '.ogg':
        sound2 = pygame.mixer.Sound(nameToPath[pos2])
        sound2.set_volume(1.0)
        id2 = nameToID[pos2]
    else: 
        sound2 = ''
        id2 = '0'
    soundBoard.append(sound2)
    save.append(id2)

    while not validSound:
        pos3 = input('Enter name of sound in position 3 (without .ogg): ')
        pos3 += '.ogg'
        if pos3 == '.ogg':
            break
        if pos3 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos3 != '.ogg':
        sound3 = pygame.mixer.Sound(nameToPath[pos3])
        sound3.set_volume(1.0)
        id3 = nameToID[pos3]
    else: 
        sound3 = ''
        id3 = '0'
    soundBoard.append(sound3)
    save.append(id3)

    while not validSound:
        pos4 = input('Enter name of sound in position 4 (without .ogg): ')
        pos4 += '.ogg'
        if pos4 == '.ogg':
            break
        if pos4 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos4 != '.ogg':
        sound4 = pygame.mixer.Sound(nameToPath[pos4])
        sound4.set_volume(1.0)
        id4 = nameToID[pos4]
    else: 
        sound4 = ''
        id4 = '0'
    soundBoard.append(sound4)
    save.append(id4)

    while not validSound:
        pos5 = input('Enter name of sound in position 5 (without .ogg): ')
        pos5 += '.ogg'
        if pos5 == '.ogg':
            break
        if pos5 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos5 != '.ogg':
        sound5 = pygame.mixer.Sound(nameToPath[pos5])
        sound5.set_volume(1.0)
        id5 = nameToID[pos5]
    else: 
        sound5 = ''
        id5 = '0'
    soundBoard.append(sound5)
    save.append(id5)

    while not validSound:
        pos6 = input('Enter name of sound in position 6 (without .ogg): ')
        pos6 += '.ogg'
        if pos6 == '.ogg':
            break
        if pos6 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos6 != '.ogg':
        sound6 = pygame.mixer.Sound(nameToPath[pos6])
        sound6.set_volume(1.0)
        id6 = nameToID[pos6]
    else: 
        sound6 = ''
        id6 = '0'
    soundBoard.append(sound6)
    save.append(id6)

    while not validSound:
        pos7 = input('Enter name of sound in position 7 (without .ogg): ')
        pos7 += '.ogg'
        if pos7 == '.ogg':
            break
        if pos7 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos7 != '.ogg':
        sound7 = pygame.mixer.Sound(nameToPath[pos7])
        sound7.set_volume(1.0)
        id7 = nameToID[pos7]
    else: 
        sound7 = ''
        id7 = '0'
    soundBoard.append(sound7)
    save.append(id7)

    while not validSound:
        pos8 = input('Enter name of sound in position 8 (without .ogg): ')
        pos8 += '.ogg'
        if pos8 == '.ogg':
            break
        if pos8 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos8 != '.ogg':
        sound8 = pygame.mixer.Sound(nameToPath[pos8])
        sound8.set_volume(1.0)
        id8 = nameToID[pos8]
    else: 
        sound8 = ''
        id8 = '0'
    soundBoard.append(sound8)
    save.append(id8)

    while not validSound:
        pos9 = input('Enter name of sound in position 9 (without .ogg): ')
        pos9 += '.ogg'
        if pos9 == '.ogg':
            break
        if pos9 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos9 != '.ogg':
        sound9 = pygame.mixer.Sound(nameToPath[pos9])
        sound9.set_volume(1.0)
        id9 = nameToID[pos9]
    else: 
        sound9 = ''
        id9 = '0'
    soundBoard.append(sound9)
    save.append(id9)

    while not validSound:
        pos10 = input('Enter name of sound in position 10 (without .ogg): ')
        pos10 += '.ogg'
        if pos10 == '.ogg':
            break
        if pos10 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos10 != '.ogg':
        sound10 = pygame.mixer.Sound(nameToPath[pos10])
        sound10.set_volume(1.0)
        id10 = nameToID[pos10]
    else: 
        sound10 = ''
        id10 = '0'
    soundBoard.append(sound10)
    save.append(id10)

    while not validSound:
        pos11 = input('Enter name of sound in position 11 (without .ogg): ')
        pos11 += '.ogg'
        if pos11 == '.ogg':
            break
        if pos11 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos11 != '.ogg':
        sound11 = pygame.mixer.Sound(nameToPath[pos11])
        sound11.set_volume(1.0)
        id11 = nameToID[pos11]
    else: 
        sound11 = ''
        id11 = '0'
    soundBoard.append(sound11)
    save.append(id11)

    while not validSound:
        pos12 = input('Enter name of sound in position 12 (without .ogg): ')
        pos12 += '.ogg'
        if pos12 == '.ogg':
            break
        if pos12 in nameToPath:
            validSound = True
        else:
            print('Not a valid sound')
    validSound = False
    if pos12 != '.ogg':
        sound12 = pygame.mixer.Sound(nameToPath[pos12])
        sound12.set_volume(1.0)
        id12 = nameToID[pos12]
    else: 
        sound12 = ''
        id12 = '0'
    soundBoard.append(sound12)
    save.append(id12)

def add_samples(directory):
    global nameToPath
    global numSounds
    global IDtoName

    sorted_dir = sorted(os.listdir(directory))
    for item in sorted_dir:
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if item[-4:] == '.ogg':
                nameToPath[item] = path
                nameToID[item] = numSounds
                IDtoName[str(numSounds)] = item
                numSounds += 1
        elif os.path.isdir(path):
            add_samples(path)
    IDtoName['0'] = ''
############################## HELPER FUNCTION ##############################

def main():
    global numTasks
    global nameToPath
    lcd.lcd_start()
    lcd.lcd_string('touch ready', lcd.LCD_LINE_1)

    pygame.mixer.init()
    pygame.mixer.set_num_channels(12)

    add_samples('samples')
    print(nameToPath)
    make_soundboard()

    task1 = task(saveLoadState.start, period_gcd, 0, SaveLoad)
    task2 = task(touchState.startTouch, period_gcd, 0, Touch)
    task3 = task(spotifyState.startSpot, period_gcd, 0, Spotify)

    tasks = [task1, task2, task3]

    while True:
        for i in range(numTasks):
            if(tasks[i].elapsedTime >= tasks[i].period):
                tasks[i].state = tasks[i].func(tasks[i].state)
                tasks[i].elapsedTime = 0
            tasks[i].elapsedTime += period_gcd

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x01, lcd.LCD_CMD)
        lcd.lcd_string("Goodbye!", lcd.LCD_LINE_1)
        speaker.p.stop()
        sp.pause_playback()