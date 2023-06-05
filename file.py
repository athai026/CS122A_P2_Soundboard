import os
import pickle

def assignID(directory):
    global soundID
    sorted_dir = sorted(os.listdir(directory))
    for item in sorted_dir:
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if item[-4:] == '.ogg':
                if item not in files:
                    print(f'new sound bite {item} with ID {soundID}')
                    files[item] = soundID
                    soundID += 1
                else:
                    print(f'sound bite {item} already existed with ID {files[item]}')
        elif os.path.isdir(path):
            assignID(path)

files = {}
with open('files.txt', 'rb') as file:
    files = pickle.load(file)
dir = 'samples'
soundID = len(files) + 1
assignID(dir)
with open('files.txt', 'wb') as file:
    pickle.dump(files, file)
print(files)