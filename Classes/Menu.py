import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.surf = pygame.image.load('./Assets/Loading.png')
        self.rect = self.surf.get_rect()

    def run (self):
        self.screen.blit(source=self.surf, dest=self.rect)
        pygame.display.flip()
        pass