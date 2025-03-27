import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Const import SCREEN_WIDTH, MENU_OPTION


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.surf = pygame.image.load('./Assets/Cover_menu.png')
        self.rect = self.surf.get_rect()
        self.image = pygame.image.load('./Assets/Roleta.png')
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, 400))
        self.angle = 0

    def run (self):
        pygame.mixer_music.load('./Assets/soundtrack.mp3')
        pygame.mixer_music.play(-1)
        while True:
            self.screen.blit(source=self.surf, dest=self.rect)

            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.image_rect.center)
            self.screen.blit(rotated_image, rotated_rect)

            self.angle -= 1

            self.menu_text(30, MENU_OPTION[0], (255, 255, 255), ((SCREEN_WIDTH / 2), 650))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[0]

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.is_mouse_over_button(mouse_x, mouse_y):
                        return MENU_OPTION[0]




    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="impact", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.screen.blit(source=text_surf, dest=text_rect)

    def is_mouse_over_button(self, mouse_x, mouse_y):
        button_x = SCREEN_WIDTH / 2
        button_y = 650
        button_width = 150
        button_height = 50

        button_rect = pygame.Rect(
            button_x - button_width / 2,
            button_y - button_height / 2,
            button_width,
            button_height
        )

        return button_rect.collidepoint(mouse_x, mouse_y)