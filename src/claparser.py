#! /usr/bin/python
import sys
def argdict():
    x = sys.argv[1:]

    print(x)
    x = iter(x)
    while 1:
        try:
            arg = next(x)
            if arg == "-n":
                
                value = next(x)
                try:
                    yield "number", int(value)
                except ValueError:
                    print("-n ",value,":not an integer")
            
            elif arg == "-c":
                
                value = next(x)
                try:
                    yield "color", int(value)
                except ValueError:
                    print("-c ",value,":not an integer")
       
            elif arg == "-s":
                
                value = next(x)
                try:
                    yield "speed", float(value)
                except ValueError: 
                    print("-c ",value,":not an float")
        except StopIteration:
           break
