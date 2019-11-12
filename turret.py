#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Turret(object):
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.cost = 30
        self.time = 100 #czas przeładowania w j. kont.
        self.sp_eff = None #klasa efektu spcjalnego
        self.fly_deff = True #defensywa na j. latające

    def scope(self): #zasięg rażenia
        scope = []
        for field in self.maze:
            value = abs(self.x-field.x)+abs(self.y-field.y)
            if value == 2 or value == 1:
                if field.__class__.__name__ == 'Road':
                    scope.append(field)
        return scope

    def get_cost(self):
        return self.cost

    def get_time(self):
        return self.time

    def blast(self, enemy, queue): #rażenie przeciwnika
        if self.fly_deff:
            if enemy.__class__.__name__ == 'FlyEnemy':
                enemy.hp -= 1
        else:
            if enemy.__class__.__name__ == 'FlyEnemy':
                return
            else:
                enemy.hp -= 1
                if self.sp_eff:
                    self.sp_eff(self.x, self.y, enemy, queue) #x, y - identyfikacja wieży

    def __str__(self):
        return 'T'

    def __repr__(self):
        return 'Turret({0.x!r}, {0.y!r})'.format(self)


class StandByTurret(Turret):
    def __init__(self, x, y, maze):
        super(StandByTurret, self).__init__(x, y, maze)
        self.cost = 40
        self.time = 150
        self.fly_deff = False
        self.sp_eff = SpEffSt

    def __str__(self):
        return 'S'

    def __repr__(self):
        return 'StandByTurret({0.x!r}, {0.y!r})'.format(self)


class ArcheryTurret(Turret):
    def __init__(self, x, y, maze):
        super(ArcheryTurret, self).__init__(x, y, maze)
        self.cost = 50
        self.time = 200
        self.fly_deff = False
        self.sp_eff = SpEffArch

    def __str__(self):
        return 'A'

    def __repr__(self):
        return 'ArcheryTurret({0.x!r}, {0.y!r})'.format(self)


class SpEffSt(object):
    def __init__(self, x, y, enemy, queue):
        self.add_effect(x, y, enemy, queue)

    def add_effect(self, x, y, enemy, queue):
        if enemy.__class__.__name__ == 'FastEnemy':
            enemy.set_stand_on(50, 50) #krok cz. + extra time


class SpEffArch(object):
    def __init__(self, x, y, enemy, queue):
        self.add_effect(x, y, enemy, queue)

    def add_effect(self, x, y, enemy, queue):
        if enemy.__class__.__name__ == 'StrongEnemy':
            enemy.set_arch_on(x, y, 0.40, 4) #4 razy po 0.4
            queue.append((0, enemy.get_arch_on, [x, y]))


