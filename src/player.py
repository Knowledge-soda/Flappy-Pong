#! python3

import pygame
from Mind import Orientation
import random


class player:
    def __init__(self, x, y, d, level, screen):
        self.pos = self.s_x, self.s_y = self.x, self.y = x, y
        self.d = d

        self.level = level
        self.screen = screen
        self.screen_x, self.screen_y = self.screen.get_size()
        self.mid = self.screen_x / 2
        self.t1 = self.screen_y * 0.9
        self.t2 = self.screen_y * 0.1

        self.alive = True
        self.Z = self.d

        self.f = 2
        self.pushing = False

        self.image = pygame.image.load("images/player.png")
        self.width, self.height = self.image.get_size()
        self.font = pygame.font.SysFont("Arial", 22)

        self.x -= self.width / 2
        self.y -= self.height / 2
        self.D = Orientation.direction(Orientation.point(self.x, self.y, self.level, quiet=True), 20, self.level)

        self.rect = Orientation.rect(self.x, self.y, self.width, self.height, self.level, "ball")

        self.paddles = []
        for obj in self.level.objects:
            if type(obj) == Orientation.ext_obj:
                if obj.obj.description == "paddle":
                    self.paddles.append(obj)

    def blit(self):
        self.screen.blit(self.image, self.pos)

        self.alive = self.zone()
        if self.Z != (self.x + self.width / 2 > self.mid):
            self.alive -= 1

        if self.alive > 0:
            self.Z = self.x + self.width / 2 > self.mid

        if self.pushing:
            self.screen.blit(self.h, (self.x + self.width / 2 - self.f_width / 2, self.y - self.f_height))

        self.D.move(self.f)
        self.pos = self.x, self.y = self.rect.x, self.rect.y = self.D.point.get_xy()

        self.C = self.rect.collide(self.paddles[self.d].obj)
        if self.C[(not self.d) * 2]:
            self.d = not self.d
            self.paddles[not self.d].prop1[0].randomize()
            self.D.set_angle(360 - self.D.get_angle())
            self.cD = None
            if self.height / 2 > self.C[1]:
                self.a = 90 - (self.height / 2 - self.C[1]) / (self.height / 2) * 90
                if self.d:
                    self.cD = Orientation.direction(self.D.get_pos(self.f), 180 + self.a, self.level, quiet=True)
                else:
                    self.cD = Orientation.direction(self.D.get_pos(self.f), 180 - self.a, self.level, quiet=True)
            elif self.height / 2 > self.C[3]:
                self.a = 90 - (self.height / 2 - self.C[3]) / (self.height / 2) * 90
                if self.d:
                    self.cD = Orientation.direction(self.D.get_pos(self.f), self.a, self.level, quiet=True)
                else:
                    self.cD = Orientation.direction(self.D.get_pos(self.f), 360 - self.a, self.level, quiet=True)
            if self.cD:
                self.N = self.cD.get_pos(self.f)
                self.nx, self.ny = self.N.get_xy()

                self.L = Orientation.line((self.D.get_pos(0), self.N), self.level, quiet=True)

                self.angle = self.L.get_angle()
                if self.y < self.ny:
                    if self.d:
                        self.angle = 180 - self.angle
                    else:
                        self.angle += 180
                elif not self.d:
                    self.angle = 360 - self.angle

                self.D.set_angle(self.angle)

        self.G = Orientation.direction(self.D.get_pos(self.f), 180, self.level, quiet=True)
        self.N = self.G.get_pos(0.1)
        self.nx, self.ny = self.N.get_xy()

        self.L = Orientation.line((self.D.get_pos(0), self.N), self.level, quiet=True)

        self.angle = self.L.get_angle()
        if self.y < self.ny:
            if self.d:
                self.angle = 180 - self.angle
            else:
                self.angle += 180
        elif not self.d:
            self.angle = 360 - self.angle

        self.D.set_angle(self.angle)

        self.f = self.D.get_pos(0).distance(self.N)

    def s_push(self):
        if self.d:
            self.p_angle = 0
        else:
            self.p_angle = 360
        self.pushing = True
        self.push()

    def push(self):
        if self.d:
            self.p_angle += 2
            self.p_angle %= 180
            self.h = self.font.render(str(self.p_angle), True, (0, 0, 0))
        else:
            self.p_angle -= 2
            if self.p_angle < 180:
                self.p_angle = 358
            self.h = self.font.render(str(360 - self.p_angle), True, (0, 0, 0))
        self.f_width, self.f_height = self.h.get_size()

    def f_push(self):
        self.D.set_angle(self.p_angle)
        self.f = 5
        self.pushing = False

    def zone(self):
        if (self.screen_y > self.y + self.height > self.y > 0) and (self.screen_x > self.x + self.width > self.x > 0):
            if self.t2 < self.y < self.y + self.height < self.t1:
                return 2
            return 1
        return 0

    def run(self):
        return self.alive

    def reset(self, *some):
        self.__init__(self.s_x, self.s_y, random.randrange(2), self.level, self.screen)


class paddle:
    def __init__(self, side, screen, level):
        self.side = side
        self.screen = screen
        self.width = 20
        self.height = 140
        if self.side:
            self.x = self.screen.get_size()[0] - 30
        else:
            self.x = 30
        self.up = 0
        self.down = self.screen.get_size()[1]
        self._randomize()
        self.y = self.Y
        self.level = level
        self.rect = Orientation.ext_obj(Orientation.rect(self.x, self.y, self.width, self.height, self.level, "paddle", quiet=False), self)
        self.move = 0

    def _randomize(self):
        self.Y = random.randrange(self.down - self.height)

    def randomize(self):
        self._randomize()
        self.move = random.randint(4, 6)
        if self.Y < self.y:
            self.move = -self.move

    def blit(self):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height))
        self.y += self.move
        if abs(self.Y - self.y) < abs(self.move):
            self.y = self.Y
            self.move = 0
        self.rect.obj.y = self.y
