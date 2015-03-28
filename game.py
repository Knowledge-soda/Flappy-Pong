#! python3

import pygame
import Mind
import random
from src import player


class fake_menu(Mind.Imagination.Main_menu):

    def blit(self):
        self.keyboard.update()


class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.init()

        self.screen_x, self.screen_y = self.screen.get_size()

        self.places = [Mind.Imagination.PLACE(True)] +\
        [Mind.Imagination.PLACE() for x in range(2)]

        self.Game = Mind.Imagination.Game(self.places[0])

        self.Main_menu = Mind.Imagination.Main_menu(self.places[0], 250)
        self.Main_menu.set_game(self.Game)
        self.keyboard = self.Main_menu.get_keyboard()
        self.keyboard.extend([(pygame.K_TAB, "switch"), (pygame.K_ESCAPE,
        "quit"), (pygame.K_g, "p1"), (pygame.K_k, "p2")])

        self.font = pygame.font.SysFont("Arial", 77)
        self.colors = [tuple([random.randrange(256) for i in range(3)])
        for x in range(7)]
        self.Main_menu.add_option(Mind.Imagination.text_option(self.font,
        "Start", (self.colors[0]), self.Main_menu, Mind.Imagination.link
        (self.places[1]), pos_do=Mind.Imagination.ch_color((0, 0, 0)),
        anti_pos_do=Mind.Imagination.ch_color(self.colors[0])), True)
        self.Main_menu.add_option(Mind.Imagination.text_option(self.font,
        "Options", (self.colors[1]), self.Main_menu,
        pos_do=Mind.Imagination.ch_color((0, 0, 0)),
        anti_pos_do=Mind.Imagination.ch_color(self.colors[1])))
        self.Main_menu.add_option(Mind.Imagination.text_option(self.font,
        "Quit", (self.colors[2]), self.Main_menu, Mind.Imagination.Quit,
        pos_do=Mind.Imagination.ch_color((0, 0, 0)),
        anti_pos_do=Mind.Imagination.ch_color(self.colors[2])))
        self.Main_menu.set_options()

        self.in_game = fake_menu(self.places[1], 0, keyboard=self.keyboard)
        self.in_game.set_game(self.Game)

        self.Map = Mind.Orientation.MAP(self.screen_x, self.screen_y)

        self.paddles = [player.paddle(i, self.screen, self.Map) for i in
        range(2)]
        self.player = player.player(self.screen_x / 2, self.screen_y / 2,
        random.randrange(2), self.Map, self.screen)

        self.mid = self.screen_x / 2
        self.t1 = self.screen_y * 0.9
        self.t2 = self.screen_y * 0.1

        self.w_menu = Mind.Imagination.Main_menu(self.places[2], 250,
        off=(0, 250 / 2), keyboard=self.keyboard)
        self.ag1 = [Mind.Imagination.link(self.places[1]),
        self.player.reset]
        self.ag2 = [Mind.Imagination.link(self.places[0]),
        self.Main_menu.reset]
        self.w_menu.add_option(Mind.Imagination.text_option(self.font,
        "Again", self.colors[4], self.Main_menu, Mind.Imagination.joined
        (self.ag1), pos_do=Mind.Imagination.ch_color((0, 0, 0)),
        anti_pos_do=Mind.Imagination.ch_color(self.colors[4])), True)
        self.w_menu.add_option(Mind.Imagination.text_option(self.font,
        "Back", self.colors[5], self.Main_menu, Mind.Imagination.joined
        (self.ag2), pos_do=Mind.Imagination.ch_color((0, 0, 0)),
        anti_pos_do=Mind.Imagination.ch_color(self.colors[5])))
        self.w_menu.set_options()
        self.w_menu.set_game(self.Game)

        self.Clock = pygame.time.Clock()

    def main(self):
        while self.Game.run():
            if self.keyboard["switch"] == 1:
                self.colors[3] = tuple([random.randrange(256) for i in
                range(3)])
            elif self.keyboard["quit"]:
                self.Game.kill()

            self.screen.fill(self.colors[3])

            self.Game.blit()

            if self.places[1]:
                pygame.draw.line(self.screen, self.colors[0],
                (self.mid, 0), (self.mid, self.screen_y))
                pygame.draw.line(self.screen, self.colors[1],
                (0, self.t1), (self.screen_x, self.t1))
                pygame.draw.line(self.screen, self.colors[2],
                (0, self.t2), (self.screen_x, self.t2))
                self.player.blit()
                for x in self.paddles:
                    x.blit()
                if self.player.Z:
                    if self.keyboard["p2"] == 1:
                        self.player.s_push()
                    elif self.keyboard["p2"] == 2:
                        self.player.push()
                    elif self.keyboard["p2"] == 3:
                        self.player.f_push()
                else:
                    if self.keyboard["p1"] == 1:
                        self.player.s_push()
                    elif self.keyboard["p1"] == 2:
                        self.player.push()
                    elif self.keyboard["p1"] == 3:
                        self.player.f_push()
                if not self.player.run():
                    self.Game.change(self.places[2])
                    self.w_menu.reset()
                    if self.player.Z:
                        self.T = "Player 1 won!"
                    else:
                        self.T = "Player 2 won!"
                    self.o = self.font.render(self.T, True, self.colors[6])
                    self.o_width, self.o_height = self.o.get_size()
                    self.o_x = self.screen_x / 2 - self.o_width / 2
                    self.o_y = self.screen_y / 2 - 250 - self.o_height / 2

            if self.places[2]:
                self.screen.blit(self.o, (self.o_x, self.o_y))

            pygame.display.flip()
            self.Clock.tick(60)

Game = game()
Game.main()

pygame.display.quit()
