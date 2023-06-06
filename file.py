import os
import pickle

def assignID(directory):
    global soundID
    sorted_dir = sorted(os.listdir(directory))
    for item in sorted_dir:
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if item[-4:] == '.ogg':
                if item not in name_ID:
                    print(f'new sound bite {item} with ID {soundID}')
                    name_ID[item] = soundID
                    name_path[item] = path
                    soundID_name[soundID] = item
                    soundID += 1
                else:
                    print(f'sound bite {item} already existed with ID {name_ID[item]}')
        elif os.path.isdir(path):
            assignID(path)

name_ID = {}
name_path = {}
soundID_name = {}
with open('nameID.txt', 'rb') as file:
    name_ID = pickle.load(file)
with open('namePath.txt', 'rb') as file:
    name_path = pickle.load(file)
with open('IDName.txt', 'rb') as file:
    soundID_name = pickle.load(file)

dir = 'samples'
soundID = len(name_ID) + 1
assignID(dir)
with open('nameID.txt', 'wb') as file:
    pickle.dump(name_ID, file)
with open('namePath.txt', 'wb') as file:
    pickle.dump(name_path, file)
with open('IDName.txt', 'wb') as file:
    pickle.dump(soundID_name, file)
print(name_ID)

# files.txt: sound name to unit ID (starting at 1)
# names.text: sound name to path
# soundIDs.txt: ID to name