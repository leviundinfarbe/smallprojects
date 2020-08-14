#!/usr/bin/env python3
import sys, os
from tkinter import *
import tkinter.font as font

window = Tk()
window.configure(bg='black')
myFont = font.Font(size=20)
window.title("Soundboard")
sounds = os.popen('ls <sounds directory>').read().split('\n')

button = list()
c = 1
r = 0
for i in range(len(sounds)):
    if sounds[i][-4:] == '.wav':
        button.append(Button(window, text={sounds[i][:-4]}, bg='black', fg='white', command=lambda k=i: os.system("""aplay "<sounds directory>/{}" &""".format(sounds[k].replace(' ', '\ ')))))
        button[-1]['font'] = myFont
        button[-1].config(height=1,width=16)
        button[-1].grid(row=r, column=c-1, padx=5, pady=5)
        c += 1
        if c % 5 == 0:
            r += 1
            c = 1

button.append(Button(window, text="Stop", bg='black', fg='white', command=lambda: os.system("killall aplay")))
button[-1]['font'] = myFont
button[-1].grid(row=r+1, column=3, padx=20, pady=20)
window.mainloop()
