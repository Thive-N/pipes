#! /usr/bin/python
import claparser
import sys
import os
import random
import time


class colors:
    reset = "\033[0m"

    colors = [
            [
                "\033[30m",
                "\033[31m",
                "\033[32m",
                "\033[33m",
                "\033[34m",
                "\033[35m",
                "\033[36m",
                "\033[37m"
                ],
            
            [
                "\033[30m",
                "\033[36m"
                ]
            
            ]


#Black: \u001b[30m
#Red: \u001b[31m
#Green: \u001b[32m
#Yellow: \u001b[33m
#Blue: \u001b[34m
#Magenta: \u001b[35m
#Cyan: \u001b[36m
#White: \u001b[37m

class VisPipe:
    def __init__(self):
        self.sets = [[
            "━", "┏", "┛", "┗", "┛", "┏", "━", "┗", "┏", "┓", "┃"]]

        # "━", "┏", "┓", "┛", "━┓", "┏", "━", "┛", "┗", "┏━","┃"]]

        self.set_trans = {
            "du": 0,
            "dr": 1,
            "dl": 2,
            "lu": 3,
            "ld": 4,
            "ur": 5,
            "ud": 6,
            "ul": 7,
            "ur": 8,
            "dr": 9,
            "ud": 0,
            "rd": 1,
            "ld": 2,
            "ul": 3,
            "dl": 4,
            "ru": 5,
            "du": 6,
            "lu": 7,
            "ru": 8,
            "rd": 9,
            "lr": 10,
            "rl": 10,

        }

    def get(self,  val):
        return self.sets[0][self.set_trans[val]]


class Terminal:
    def __init__(self):
        self.bounds = list(map(int, os.popen("stty size", "r").read().split()))

    def loc_print(self, loc, val):
        if loc[0] > self.bounds[0] or loc[1] > self.bounds[1]:
            return
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (loc[0], loc[1], val))
        sys.stdout.flush()


class Pipes:
    def __init__(self):
        self.pipes = []

    def start_pipes(self, sleepdur=0.05, numpipe=5, scarlet=5, color=0):
        for num in range(numpipe):
            pipe = Pipe(colorset = color)
            pipe.randset()
            self.pipes.append(pipe)
        
        t = time.time()
        while True:
            for pipe in self.pipes:
                pipe.advance()

            time.sleep(sleepdur)
            if time.time() - t > scarlet:
                t = time.time()
                os.system("clear")
                for pipe in self.pipes:
                    pipe.randset()
                    pipe.randcolor()
                
class Location:
    def __init__(self):
        self.bounds = list(map(int, os.popen("stty size", "r").read().split()))
        self.x = 0
        self.y = 1

    def loc(self):
        return (self.x, self.y)

    def random(self):
        self.x = random.randint(0, int(self.bounds[0]))
        self.y = random.randint(0, int(self.bounds[1]))

        self.loc()

    def up(self):
        self.y += 1
        if self.y > self.bounds[1]:
            self.y = 0

    def down(self):
        self.y -= 1
        if self.y == 0:
            self.y = self.bounds[1]

    def right(self):
        self.x += 1
        if self.x > self.bounds[0]:
            self.x = 0

    def left(self):
        self.x -= 1
        if self.x < 0:
            self.x = self.bounds[0]


class Pipe:
    def __init__(self, colorset=0):
        self.color_mutation_chance = 0.01
        self.location = Location()
        self.colorset = colorset
        self.color = random.choice(colors.colors[self.colorset])
        self.rotation = "u"
        self.term = Terminal()
        self.rotation_chance = 0.05
        self.vispipe = VisPipe()
    
    def randcolor(self):
        self.color = random.choice(colors.colors[self.colorset])
    
    def randset(self):
        self.location.random()

    def rotation_flip(self):
        if self.rotation == 'd':
            return 'u'
        if self.rotation == 'u':
            return 'd'
        if self.rotation == 'r':
            return 'l'
        if self.rotation == 'l':
            return 'r'

    def advance(self):
        #if random.random() < self.color_mutation_chance:
        #    self.color = random.choice(colors.colors)
        if random.random() < self.rotation_chance:
            self.temp = self.rotation_flip()
            if self.rotation == 'u':
                self.location.up()
            elif self.rotation == 'd':
                self.location.down()
            elif self.rotation == 'l':
                self.location.left()
            elif self.rotation == 'r':
                self.location.right()

            if self.rotation in ["u", 'd']:
                if random.random() > 0.5:
                    self.rotation = 'l'
                    self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                        self.temp+self.rotation))
                else:
                    self.rotation = 'r'
                    self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                        self.temp+self.rotation))
            else:
                if random.random() > 0.5:
                    self.rotation = 'u'
                    self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                        self.temp+self.rotation))
                else:
                    self.rotation = 'd'
                    self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                        self.temp+self.rotation))
            return

        elif self.rotation == 'u':
            self.location.up()
            self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                self.rotation_flip()+self.rotation))

        elif self.rotation == 'd':
            self.location.down()
            self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                self.rotation_flip()+self.rotation))

        elif self.rotation == 'l':
            self.location.left()
            self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                self.rotation_flip()+self.rotation))

        elif self.rotation == 'r':
            self.location.right()
            self.term.loc_print(self.location.loc(), self.color + self.vispipe.get(
                self.rotation_flip()+self.rotation))


def main():
    sleep = 0.025
    num = 5
    scarlet = 50
    color = 0
    pipes = Pipes()
    args = dict(claparser.argdict())
    if "number" in args.keys():
        num = args["number"]

    if "color" in args.keys():
        color = args["color"]

    if "speed" in args.keys():
        sleep = args["speed"]
    
    os.system("clear")
    pipes.start_pipes(sleepdur=sleep, numpipe=num, scarlet=scarlet, color = color)
if __name__ == "__main__":
    main()
