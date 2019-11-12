#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Field(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "{0}({1.x}, {1.y})".format(type(self).__name__, self)


class Brick(Field):
    def __init__(self, x, y):
        Field.__init__(self, x, y)
        self.turret = None

    def set_turret(self, turret):
        self.turret = turret

    def get_turret(self):
        return self.turret

    def del_turret(self):
        self.turret = None

    def __repr__(self):
        if self.turret:
            return repr(self.turret)
        else:
            return "{0}({1.x}, {1.y})".format(type(self).__name__, self)

    def __str__(self):
        if self.turret:
            return str(self.turret)
        else:
            return '#'


class Road(Field):
    def __init__(self, x, y):
        Field.__init__(self, x, y)
        self.next_road = None
        self._enemy = None

    def set_next_road(self, road):
        self.next_road = road

    def get_next_road(self):
        return self.next_road

    @property
    def enemy(self):
        return self._enemy
        
    @enemy.setter
    def enemy(self, enemy):
        if self.enemy:
            return
        self._enemy = enemy

    @enemy.deleter
    def enemy(self):
        self._enemy = None

    def __str__(self):
        if self.enemy:
            return str(self.enemy)
        else:
            return ' '


class Maze(object):
    def __init__(self):
        #mapa 38 kolumn i 8 wiersz
        maze = self.make_road()
        maze += [Brick(colum, row) for colum in range(1, 38) for row in range(1, 12, 2)]
        maze += [Brick(0, 1), Brick(0, 5), Brick(0, 9), Brick(38, 3), Brick(38, 7), Brick(38, 11)]
        maze.sort(key=lambda k: k.x)
        maze.sort(key=lambda k: k.y)
        self.maze = maze

    def make_road(self):
        road = []
        road1 = Road(0, 0)
        for row in range(0, 13, 2):
            if row%4 == 2:
                for col in reversed(range(1, 39)):
                    road2 = Road(col-1, row)
                    road1.set_next_road(road2)
                    road.append(road1)
                    road1 = road2
                for i in range(2):
                    road2 = Road(col-1, row+i+1)
                    road1.set_next_road(road2)
                    road.append(road1)
                    road1 = road2
            else:
                for col in range(1, 39):
                    road2 = Road(col, row)
                    road1.set_next_road(road2)
                    road.append(road1)
                    road1 = road2
                for i in range(2):
                    road2 = Road(col, row+i+1)
                    road1.set_next_road(road2)
                    road.append(road1)
                    road1 = road2
        road.pop()
        road[-1].set_next_road(None)
        return road

    def check_hp_enemies(self):
        fl = 0 #hp for FlyEnemies
        fa = 0 #hp for FastEnemies
        st = 0 #hp for StrongEnemies
        for field in self.maze:
            if field.__class__.__name__ == 'Road':
                if field.enemy.__class__.__name__ == 'FlyEnemy':
                    fl += field.enemy.get_hp()
                elif field.enemy.__class__.__name__ == 'FastEnemy':
                    fa += field.enemy.get_hp()
                elif field.enemy.__class__.__name__ == 'StrongEnemy':
                    st += round(field.enemy.get_hp(), 1)
        return fl, fa, st

    def __iter__(self):
        return iter(self.maze)

    def __getitem__(self, index):
        return self.maze[index]

    def __setitem__(self, index, value):
        self.maze[index] = value

    def __repr__(self):
        fl, fa, st = self.check_hp_enemies()
        rep = ''.join(map(str, self.maze))
        new_rep = "~"*45 + "\n"
        new_rep += "_"*45 + "\n"
        new_rep += "|  |" + "".join(map(str, [x for x in range(10)])) + "".join(map(str, [str(x)*10 for x in range(1,3)])) + "3"*9 + "|\n"
        new_rep += "|  |"+ " "*10 + "".join(map(str, [x for x in range(10)]))*2 + "".join(map(str, [x for x in range(9)])) + "|\n"
        new_rep += "-"*45 + "\n"
        new_rep += "| 0|" + rep[:39] + "|" + "FlyEnemies hp:" + "\n"
        new_rep += "| 1|" + rep[39:78] + "|" + str(fl) + "\n"
        new_rep += "| 2|" + rep[78:117] +"|" + "FastEnemies hp:" + "\n"
        new_rep += "| 3|" + rep[117:156] + "|" + str(fa) + "\n"
        new_rep += "| 4|" + rep[156:195] + "|" + "StrongEnemies hp:" + "\n"
        new_rep += "| 5|" + rep[195:234] + "|" + str(st) + "\n"
        new_rep += "| 6|" + rep[234:273] + "|\n" 
        new_rep += "| 7|" + rep[273:312] + "|\n"
        new_rep += "| 8|" + rep[312:351] + "|\n" 
        new_rep += "| 9|" + rep[351:390] + "|\n"
        new_rep += "|10|" + rep[390:429] + "|\n"
        new_rep += "|11|" + rep[429:468] + "|\n"
        new_rep += "|12|" + rep[468:507] + "|\n"
        new_rep += "~"*45 + "\n"
        return new_rep


