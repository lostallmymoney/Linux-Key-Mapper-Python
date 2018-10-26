import struct
import subprocess
import os

f = open( "/dev/input/by-id/usb-Razer_Razer_Naga_2014-if02-event-kbd", "rb" ) # Open the file in the read-binary mode.
# Change file for devices

loadedConfig = []
emptyCfg = []
cfg = 'default'

subprocess.Popen(['xinput set-int-prop 13 "Device Enabled" 8 0'], shell=True)

subprocess.Popen(["kill $(ps aux | grep inputAssigner | grep -v grep | awk '{print $2}' | grep -v "+str(os.getpid())+" )"], shell=True)



class keyEvent:
    def __init__(self, onPress, theKey, theData, run=True):
        self.runs = run
        self.onPressed = onPress
        self.key = theKey
        self.data = theData


def loadConfig(name = 'default'):

    if (os.path.exists('deviceConfig.txt')):
        config = open('deviceConfig.txt')
    else:
        config = open('deviceConfig.txt', "w+")
        print
        'Config file empty !'
        exit(0)

    if sum(1 for line in config) == 0:
        print
        'Config file empty !'
        exit(0)


    print 'config loading'
    for objects in loadedConfig:
        loadedConfig.remove(objects)
    entry = 0
    config.seek(0)
    configEnded = False

    for lines in config:
        entry += 1
        if lines.strip() == name:
            entry += 1
            for line in config:
                if (line.strip() != 'end' and not configEnded):
                    entry += 1
                    splitLine = line.split('=')

                    if (not splitLine[0].isdigit()):
                        print "Error, couldn't load entry #" + str(entry)
                        exit(0)

                    if (splitLine[1] == 'run1') or (splitLine[1] == 'run0'):
                        loadedConfig.append(keyEvent(True, splitLine[0], splitLine[2]))

                    if (splitLine[1] == 'run2') or (splitLine[1] == 'run0'):
                        loadedConfig.append(keyEvent(False, splitLine[0], splitLine[2]))

                    if (splitLine[1] == 'key0'):
                        loadedConfig.append(keyEvent(True, splitLine[0], 'xdotool keydown ' + splitLine[2]))
                        loadedConfig.append(keyEvent(False, splitLine[0], 'xdotool keyup ' + splitLine[2]))

                    if (splitLine[1] == 'cfg1'):
                        loadedConfig.append(keyEvent(True, splitLine[0], splitLine[2], False))

                    if (splitLine[1] == 'cfg2'):
                        loadedConfig.append(keyEvent(False, splitLine[0], splitLine[2], False))

                    print "Loaded entry #" + str(entry)
                else:
                    configEnded=True



def pressed(button):
    loads = False
    for cunfs in loadedConfig:
        if (cunfs.onPressed) and (int(cunfs.key) == int(button) and cunfs.runs):
            subprocess.Popen([cunfs.data], shell = True)
        else:
            if not cunfs.runs and cunfs.onPressed and int(cunfs.key) == int(button):
                loads = True
                theConfig = cunfs.data.strip()
    if loads:
        loadConfig(theConfig)


def unPressed(button):
    loads = False
    for cunfs in loadedConfig:
        if (not cunfs.onPressed) and (int(cunfs.key) == int(button) and cunfs.runs):
            subprocess.Popen([cunfs.data], shell = True)
        else:
            if not cunfs.runs and not cunfs.onPressed and int(cunfs.key) == int(button):
                loads = True
                theConfig = cunfs.data.strip()
    if loads:
        loadConfig(theConfig)

loadConfig()

while 1:
    data = f.read(24)
    readed = struct.unpack('4IHHI',data[:24])
    status = readed[6]
    key = readed[5]
    if(status < 2):
        if (key != 0):
            if(status==1):
                pressed(key-1)
            else:
                unPressed(key-1)
