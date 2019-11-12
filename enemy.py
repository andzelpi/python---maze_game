#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Enemy(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, hp, time, typ, credit, road=None, dead=False):
        self.hp = hp
        self.time = time #w jednostkach kontrolera
        self.typ = typ #napowietrzny = True, else False
        self.credit = credit #zysk gracza za zastrzelenie
        self._road = road
        self.dead = dead

    def get_dead(self):
        return self.dead

    def set_dead(self, value):
        self.dead = value

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp

    def get_credit(self):
        return self.credit

    def get_road(self):
        return self._road

    def del_road(self):
        del self._road.enemy
        self._road = None

    def del_sp_eff(self):
        pass

    def move(self, maze):
        if self._road == None and maze[0].enemy == None and self.get_dead() == False:
            self._road = maze[0]
            maze[0].enemy = self
        elif self._road != None and self._road.get_next_road().enemy == None:
            old_road = self._road
            new_road = self._road.get_next_road()
            del old_road.enemy
            new_road.enemy = self
            self._road = new_road
        elif self._road != None and self._road.get_next_road().enemy != None:
            return
        else:
            pass
        
    def __repr__(self):
        return "{0}".format(type(self).__name__)


class FlyEnemy(Enemy):
    def __init__(self, hp, time, typ, credit):
        Enemy.__init__(self, hp, time, typ, credit, road=None, dead=False)

    def __str__(self):
        return "*"


class FastEnemy(Enemy):
    def __init__(self, hp, time, typ, credit):
        Enemy.__init__(self, hp, time, typ, credit, road=None, dead=False)
        self.stand_on = []

    def get_time(self):
        if len(self.stand_on) != 0:
            time = self.time
            for tim in self.stand_on:
                if tim[1] != 0:
                    time += tim[0]
                    tim[1] -= 1
            return time
        else:
            return self.time

    def set_stand_on(self, value, repeat):
        self.stand_on.append([value, repeat])

    def stand_on_res(self): #wyczyszczenie stand_on do następneje fali
        self.stand_on = []

    def del_sp_eff(self):
        if len(self.stand_on) != 0:
            for tim in self.stand_on:
                if tim[1] == 0:
                    self.stand_on.remove(tim)

    def __str__(self):
        return "%"


class StrongEnemy(Enemy):
    def __init__(self, hp, time, typ, credit):
        Enemy.__init__(self, hp, time, typ, credit, road=None, dead=False)
        self.arch_on = []

    def set_arch_on(self, x, y, hp, duration):
        self.arch_on.append([(x, y), hp, duration])

    def get_arch_on(self, xq, yq):
        if len(self.arch_on) != 0:
            for arch in self.arch_on:
                if arch[0] == (xq, yq) and arch[2] != 0:
                    self.hp -= arch[1]
                    arch[2] -= 1

    def arch_on_res(self): #wyczyszczenie arch_on do następnej fali
        self.arch_on = []

    def del_sp_eff(self):
        if len(self.arch_on) != 0:
            for arch in self.arch_on:
                if arch[2] == 0:
                    self.arch_on.remove(arch)

    def __str__(self):
        return "&"


class WaveContainer(object):
    total = 0
    fly_enemies = []
    enemies = []
    @classmethod
    def next_wave(cls):
        cls.total += 1
        if cls.total%3 == 0:
            cls.fly_enemies = Wave.add_enemies(cls.fly_enemies, cls.total).next()
            cls.fly_enemies
        else:
            cls.enemies = Wave.add_enemies(cls.enemies, cls.total).next()
            cls.enemies.sort(key=lambda k: k.time)

    @classmethod
    def __iter__(cls):
        if cls.total%3 == 0:
            return iter(cls.fly_enemies)
        else:
            return iter(cls.enemies)

    @classmethod
    def __getitem__(cls, index):
        if cls.total%3 == 0:
            return cls.fly_enemies[index]
        else:
            return cls.enemies[index]

    @classmethod
    def get_no_enemies(cls):
        if cls.total%3 == 0:
            return len(cls.fly_enemies)
        else:
            return len(cls.enemies)


class Wave(object):
    @staticmethod
    def add_enemies(enemies, total):
        if total%3 == 0:
            for i in range(4):
                enemies.append(FlyEnemy(8, 50, True, 5))
            yield enemies
        else:
            for i in range(3):
                enemies.append(FlyEnemy(3, 25, True, 5))
            for i in range(2):
                enemies.append(FastEnemy(4, 50, False, 10))
            for i in range(1):
                enemies.append(StrongEnemy(13, 150, False, 15))
            yield enemies


