#!/usr/bin/env python
# -*- coding: utf-8 -*-
import turret as tr
import maze as mz

class Observer(object):

    @staticmethod
    def check_alive(wave): #sprawdza czy już wszyscy przeciwnicy zginęli
        total_alive = 0
        for enemy in wave:
            if enemy.get_dead() == False:
                total_alive += 1
        if total_alive == 0:
            return False
        else:
            return True

    @staticmethod
    def reset_enemy(wave): #przywrócenie enemy do życia
        for enemy in wave:
            enemy.set_dead(False)

    @staticmethod
    def check_status(enemy):
        if enemy.get_hp() <= 0:
            enemy.set_dead(True)
            enemy.del_road() #usunięcie z mapy
            if enemy.__class__.__name__ == 'StrongEnemy':
                enemy.set_hp(13)
                enemy.arch_on_res()
            elif enemy.__class__.__name__ == 'FastEnemy':
                enemy.set_hp(4)
                enemy.stand_on_res()
            else:
                enemy.set_hp(2)

    @staticmethod
    def notify(time, queue, maze, enemy): #informuj wieże, że enemy na jego polu w scope
        if enemy.get_dead() == False:
            for field in maze:
                if str(field) == "T" or str(field) == "S" or str(field) == "A":
                    if time%field.get_turret().get_time() == 0:
                        scope = field.get_turret().scope()
                        for el in scope:
                            if repr(el) == repr(enemy.get_road()):
                                field.get_turret().blast(enemy, queue)


class TimeControler(object):
    def __init__(self):
        self.time = 0
        self.queue = []

    def add_event(self, event):
        self.queue.append(event)

    def del_events(self):
        self.queue = []

    def exec_current(self):
        for el in self.queue:
            if el[0] == 0:
                el[1](*el[2])
            elif el[0] == 1:
                el[1](*el[2])
            elif el[0] == 2:
                if self.time%el[1]() == 0:
                    el[2](*el[3])
            elif el[0] == 3:
                el[1](self.time, self.queue, *el[2])
            elif el[0] == 4:
                el[1]()

    def run(self):
        self.queue.sort(key=lambda k: k[0])
        self.exec_current()
        self.time += 1


class Game(object):
    def __init__(self, coins, maze, wave):
        self.coins = coins
        self.maze = maze
        self.wave = wave
        self.wave.next_wave()

    def attack(self):
        timecontroler = TimeControler()
        for enemy in self.wave:
            timecontroler.add_event((1, Observer.check_status, [enemy,]))
            timecontroler.add_event((2, enemy.get_time, enemy.move, [self.maze,]))
            timecontroler.add_event((3, Observer.notify, [self.maze, enemy]))
            timecontroler.add_event((4, enemy.del_sp_eff))
        while self.maze[-1].enemy == None:
            if Observer.check_alive(self.wave) == True:
                timecontroler.run()
                print self.maze
            else:
                Observer.reset_enemy(self.wave)
                for enemy in self.wave:
                    self.coins += enemy.get_credit()
                self.wave.next_wave()
                timecontroler.del_events()
                return 'win'
        if self.maze[-1].enemy != None:
            return 'game over'


    def build(self):
        try:
            x = int(raw_input("Enter the brick number from 0 to 38 (just try): "))
            if x < 0 or x > 38:    raise ValueError
            y = int(raw_input("Enter the wall number from 1 to 11 (odd): "))
            if y < 1 or y > 11:    raise ValueError
            turret = raw_input("Enter the type of turret (T-classic, S-standby, A-archery): ")
            if turret not in ['T','S','A']:    raise ValueError
        except ValueError:
            self.build()
        else:
            turrets = {'T': tr.Turret(x, y, self.maze), 'S': tr.StandByTurret(x, y, self.maze), 'A': tr.ArcheryTurret(x, y, self.maze)}
            if self.check_coins(turret):
                turret = turrets[turret]
                for el in self.maze:
                    if repr(el) == repr(mz.Brick(x, y)):
                        el.set_turret(turret)
                        self.coins -= turret.get_cost()
                    elif repr(el) == repr(turrets['T'])  or repr(el) == repr(turrets['S']) or repr(el) == repr(turrets['A']):
                        print "Turret at this position!"
                        change = raw_input("Do you want to change? Y/N: ")
                        if change == "Y":
                            self.coins += el.get_turret().get_cost()
                            el.set_turret(turret)
                            self.coins -= turret.get_cost()
                        else:
                            break
            else:
                    print "You have not enough coins!!!!"

    def check_coins(self, turret):
        if turret == 'T' and self.coins >= 30:    return True
        elif turret == 'A' and self.coins >= 50:    return True
        elif turret == 'S' and self.coins >= 40:    return True
        else:    return False


