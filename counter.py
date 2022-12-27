#!/usr/bin/python3
from time import sleep

class colors:
    FONT = {
        'black':      '\x1b[30m',
        'red':        '\x1b[31m',
        'green':      '\x1b[32m',
        'brown':      '\x1b[33m',
        'blue':       '\x1b[34m',
        'purple':     '\x1b[35m',
        'cyan':       '\x1b[36m',
        'lightgray':  '\x1b[37m'}
    BACKGROUND = {
        'black':      '\x1b[40m',
        'red':        '\x1b[41m',
        'green':      '\x1b[42m',
        'brown':      '\x1b[43m',
        'blue':       '\x1b[44m',
        'purple':     '\x1b[45m',
        'cyan':       '\x1b[46m',
        'lightgray':  '\x1b[47m'}
    STYLE = {
        'bold'        : '\x1b[1m' ,
        'faint'       : '\x1b[2m' ,
        'standout'    : '\x1b[3m' ,
        'uderlined'   : '\x1b[4m' ,
        'blink'       : '\x1b[5m' ,
        'reverse'     : '\x1b[7m' ,
        'hidden'      : '\x1b[8m' ,
        '_standout'   : '\x1b[23m',
        '_underlined' : '\x1b[24m',
        '_blink'      : '\x1b[25m',
        '_reverse'    : '\x1b[27m',
        }
    END = '\x1b[0m'


class Counter:
    CURSOR_UP_ONE = '\x1b[1A'
    CURSOR_DO_ONE = '\x1b[1B'
    ERASE_LINE = '\x1b[2K'
    def __init__(self,limit=-1,PREFIX='',SUFFIX='',position=1):
        self.limit   = limit
        self.counter = 0
        self.PREFIX  = PREFIX+colors.FONT['red']+colors.STYLE['bold']
        self.SUFFIX  = colors.END+SUFFIX
        self.UP      = ''
        self.DO      = ''
        self.position= position

    def iterate_position(self,n=1):
        for i in range(n):
            self.UP += self.CURSOR_UP_ONE
        for i in range(n):
            self.DO += self.CURSOR_DO_ONE

    def initiate(self):
        for i in range(self.position):
            self.UP += self.CURSOR_UP_ONE
        for i in range(self.position-1):
            self.DO += self.CURSOR_DO_ONE
        if self.limit > 0:
            print(self.PREFIX+str(self.counter)+"/"+str(self.limit)+self.SUFFIX)
        else:
            print(self.PREFIX+str(self.counter)+self.SUFFIX)

    def update(self,counter=None,step=1):
        if counter is None:
            self.counter += step
        else:
            self.counter = counter
        print(self.UP + self.ERASE_LINE,end='')
        if self.limit > 0:
            print(self.PREFIX+str(self.counter)+"/"+str(self.limit)+self.SUFFIX)
        else:
            print(self.PREFIX+str(self.counter)+self.SUFFIX)
        print(self.DO,end='')

