#!/usr/bin/env python3
import numpy as np
import re, colorama, os

colorama.init()
def move_curser(x,y):
    print("\x1b[{};{}H".format(y+1,x+1))

print("\n" * 200)
move_curser(10,0)

m = np.array([[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']])
print("\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\n\n".format(' \033[104m  \033[0m '.join([m[0,0],m[0,1],m[0,2]]), ' \033[104m  \033[0m '.join([m[1,0],m[1,1],m[1,2]]), ' \033[104m  \033[0m '.join([m[2,0],m[2,1],m[2,2]])))

def move(xo):
    t = False
    while t == False:
        n = False
        while n == False:
            row = input(f'\t\t{xo}-row: ')
            if row == 'q':
                print('\t\tExit')
                exit(1)
            else:
                try:
                    row = int(row) - 1
                    if row <= 2 and row >= 0:
                        n = True
                except:
                    print('\t\tonly between 1 and 3, try again!')
                    n = False

        n = False
        while n == False:
            col = input(f'\t\t{xo}-col: ')
            if col == 'q':
                print('\t\tExit')
                exit(1)
            else:
                try:
                    col = int(col) - 1
                    if col <= 2 and col >= 0:
                        n = True
                except:
                    print('\t\tonly between 1 and 3, try again!')
                    n = False

        if m[row,col] == ' ':
            m[row,col] = xo
            t = True
        else:
            print('\t\tfield obstructed, pick another')
    if str(m[row]) == f"['{xo}' '{xo}' '{xo}']" or str(m[0:,col]) == f"['{xo}' '{xo}' '{xo}']" or f"['{m[0,0]}' '{m[1,1]}' '{m[2,2]}']" == f"['{xo}' '{xo}' '{xo}']" or f"['{m[0,2]}' '{m[1,1]}' '{m[2,0]}']" == f"['{xo}' '{xo}' '{xo}']":
        move_curser(10,0)
        print("\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\n\n".format(' \033[104m  \033[0m '.join([m[0,0],m[0,1],m[0,2]]), ' \033[104m  \033[0m '.join([m[1,0],m[1,1],m[1,2]]), ' \033[104m  \033[0m '.join([m[2,0],m[2,1],m[2,2]])))
        return f'\t\t{xo} won!'
    else:
        return ''

for i in range(0,9):
    if i%2==0:
        a = move('x')
    else:
        a = move('o')
    
    move_curser(10,0)
    print("\n" * 200)
    move_curser(10,0)
    print("\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\n\n".format(' \033[104m  \033[0m '.join([m[0,0],m[0,1],m[0,2]]), ' \033[104m  \033[0m '.join([m[1,0],m[1,1],m[1,2]]), ' \033[104m  \033[0m '.join([m[2,0],m[2,1],m[2,2]])))
    if re.search(r'won', a):
        os.system('clear')
        print("\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\n\n".format(' \033[104m  \033[0m '.join([m[0,0],m[0,1],m[0,2]]), ' \033[104m  \033[0m '.join([m[1,0],m[1,1],m[1,2]]), ' \033[104m  \033[0m '.join([m[2,0],m[2,1],m[2,2]])))
        print(a)
        break
    if i == 8:
        os.system('clear')
        print("\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t\033[104m             \033[0m\n\t\t {}\n\t\t   \033[104m  \033[0m   \033[104m  \033[0m\n\n\n".format(' \033[104m  \033[0m '.join([m[0,0],m[0,1],m[0,2]]), ' \033[104m  \033[0m '.join([m[1,0],m[1,1],m[1,2]]), ' \033[104m  \033[0m '.join([m[2,0],m[2,1],m[2,2]])))
        print('\t\tno winner')
