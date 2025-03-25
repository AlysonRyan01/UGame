import pygame

from Classes.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 506))

    def run(self):
        while True:
            menu = Menu(self.screen)
            menu.run()
            pass
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             quit()