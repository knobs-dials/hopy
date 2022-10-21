#!/usr/bin/python3
import time, hopy

hopi = hopy.Hopi(verbose=False) # defaults to look for CH340s

while True:
    hopi.read_all()
    print( '\t'.join(['%.1f'%time.time()]+list('%.4f'%reg for reg in hopi.regs) ) )
    time.sleep(0.95)