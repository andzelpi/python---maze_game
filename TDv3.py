#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TDv3 import maze, game, enemy, turret


class Interface(object):
    def __init__(self, game):
        self.game = game

    def change_phase(self, change):
        if change == 'build':
            self.game.build()
        elif change == 'attack':
            result = self.game.attack()
            if result == 'game over':
                print "GAME OVER\n"*27
                return "Q"
            elif result == 'win':
                print "WIN\n"*3
                self.game.waves_re = 3

    def choice(self, question):
        return raw_input(question)

    def __repr__(self):
        rep = ''.join(map(str, self.game.maze))
        new_rep = "~"*60 + "\n"
        new_rep += "_"*60 + "\n"
        new_rep += "|  |" + "".join(map(str, [x for x in range(10)])) + "".join(map(str, [str(x)*10 for x in range(1,3)])) + "3"*9 + "|\n"
        new_rep += "|  |"+ " "*10 + "".join(map(str, [x for x in range(10)]))*2 + "".join(map(str, [x for x in range(9)])) + "|\n"
        new_rep += "-"*60 + "\n"
        new_rep += "| 0|" + rep[:39] + "|" + "$: " + str(self.game.coins) + "\n"
        new_rep += "| 1|" + rep[39:78] + "|\n"
        new_rep += "| 2|" + rep[78:117] +"|" + "~"*17 + "\n"
        new_rep += "| 3|" + rep[117:156] + "|" + "Enemy: " + str(self.game.wave.get_no_enemies()) + "\n"
        new_rep += "| 4|" + rep[156:195] + "|\n"
        new_rep += "| 5|" + rep[195:234] + "|\n"
        new_rep += "| 6|" + rep[234:273] + "|" + "~"*17 + "\n"
        new_rep += "| 7|" + rep[273:312] + "|\n"
        new_rep += "| 8|" + rep[312:351] + "|\n" 
        new_rep += "| 9|" + rep[351:390] + "|\n"
        new_rep += "|10|" + rep[390:429] + "|\n"
        new_rep += "|11|" + rep[429:468] + "|\n"
        new_rep += "|12|" + rep[468:507] + "|\n"
        new_rep += "~"*60 + "\n"
        new_rep += "Press: A -- add turret\t B -- start attack\t Q -- quit.\n"
        new_rep += "~"*60
        return new_rep


def main():
    print "\t\t<<<Tower defense>>>"
    play_on = True
    m = maze.Maze()
    e = enemy.WaveContainer()
    g = game.Game(260, m, e)
    interface = Interface(g)
    while play_on:
        print interface
        choice = interface.choice("What is your choice? ")
        if choice == "A":
            interface.change_phase("build")
        elif choice == "B":
            result = interface.change_phase("attack")
            if result == "Q":
                print "~"*50
                print "\t\t<<<Goodbye>>>"
                print "~"*50
                play_on = False
        elif choice == "Q":
            print "~"*50
            print "\t\t<<<Goodbye>>>"
            print "~"*50
            play_on = False
        else:
            print "Wrong choice, try again."

main()


