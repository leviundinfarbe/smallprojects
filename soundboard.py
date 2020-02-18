#!/usr/bin/env python3
# Webbased soundboard (using php), running on Raspberry Pi for local access only

import sys, os

dirlist = os.listdir('<path to sounds-folder>')
sounds = dict()
for idx,s in enumerate(dirlist):
    sounds[idx] = s

def playSound():
    if sound > len(sounds) - 1:
        print("Argument out of range\n")
        for key in sounds:
            print(f'{key}\t{sounds[key]}')
        exit(1)
    sound2play = sounds[sound]
    os.system(f"sudo aplay '<path to sounds-folder>/{sound2play}'")

def createPHP():
    functions = str()
    forms = "<form method='post'>"
    for s in sounds:
        if sounds[s][-4:] == '.wav':
            functions += f"""<?php if (isset($_POST['button{s}'])) {{ exec('sudo aplay "<path to sounds-folder>/{sounds[s]}"'); }} ?>\n"""
        else:
            pass
        forms += f"<button type='submit' name='button{s}'>{sounds[s][:-4]}</button>\n"""
    forms += "</form>"
    body = f"<p>\n{functions}\n{forms}\n</p>"
    with open('<php-filepath>', 'w') as stream:
        stream.write(body)

if len(sys.argv) != 2:
    sys.stderr.write('{}: One Argument needed, zero given'.format(sys.argv[0]))
    exit(1)
elif sys.argv[1] == 'php':
    createPHP() # used to create the phpfile for webinterface
else:
    try:
        sound = int(sys.argv[1]) # to play sound via commandline
        playSound()
    except:
        sys.stderr.write("{}: Argument must be integer or 'php'".format(sys.argv[0]))
        exit(1)
