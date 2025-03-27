import pygame

from Classes.Level import Level
from Classes.Menu import Menu
from Const import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_OPTION


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):

        while True:
            menu = Menu(self.screen)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                level = Level(self.screen, 'JOGO')
                level_return = level.run()


