import random

import pygame
import threading
import time
from pygame import Surface, Rect
from pygame.font import Font
from Entities.Player import Player

from Const import SCREEN_WIDTH


class Level:
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name
        self.image = pygame.image.load('./Assets/Roleta.png')
        self.image = pygame.transform.scale(self.image, (600, 600))
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, 750))
        self.surf = pygame.image.load('./Assets/Cover.png')
        self.rect = self.surf.get_rect()
        self.angle = 0
        self.is_rotating = False
        self.values = [100, 200, 300, 400, 500, 600, 700, 800]  # Valores das porções
        self.player1 = Player('Player1')
        self.bot = Player('Bot')
        self.vencedor = {"vencedor": ''}


    def run(self):
        while self.vencedor["vencedor"] is '':

            self.screen.blit(source=self.surf, dest=self.rect)
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.image_rect.center)
            self.screen.blit(rotated_image, rotated_rect)

            self.menu_text(30, f"{str(self.player1.score)},00", (0, 0, 0), (185, 200))

            self.menu_text(30, f"{str(self.bot.score)},00", (0, 0, 0), ((SCREEN_WIDTH - 120), 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.is_mouse_over_button(mouse_x, mouse_y):
                        if not self.is_rotating:
                            self.is_rotating = True
                            threading.Thread(target=self.rodaGirando).start()

        while True:
            self.screen.blit(source=self.surf, dest=self.rect)
            self.menu_text(60, f"{self.vencedor["vencedor"]} venceu a partida", (255, 255, 255),
                           ((SCREEN_WIDTH / 2), 250))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            time.sleep(3)

            return False




    def rodaGirando(self):
        start_time = time.time()

        rotation_time = random.uniform(5, 10)

        while time.time() - start_time < rotation_time:  # A roleta gira por 5 segundos
            if not self.is_rotating:  # Se a rotação for desativada, sai do loop
                break
            seconds = time.time() - start_time
            self.angle -= ((rotation_time*2) - (seconds * 2))  # Incrementa o ângulo (ajuste a velocidade conforme necessário)
            time.sleep(0.05)  # Controle da velocidade de rotação

        self.player1.update_score(self.valor_roleta())
        print(self.player1.get_score())

        if self.player1.score < 500:
            self.vencedor["vencedor"] = 'O bot'

        if self.player1.score >= 3000:
            self.vencedor["vencedor"] = 'Voce'

        if self.vencedor["vencedor"] != '':
            return

        time.sleep(1)

        start_time1 = time.time()

        rotation_time = random.uniform(5, 10)

        while time.time() - start_time1 < rotation_time:  # A roleta gira por 5 segundos
            if not self.is_rotating:  # Se a rotação for desativada, sai do loop
                break
            seconds = time.time() - start_time1
            self.angle -= ((rotation_time * 2) - (seconds * 2))  # Incrementa o ângulo (ajuste a velocidade conforme necessário)
            time.sleep(0.05)  # Controle da velocidade de rotação

        self.bot.update_score(self.valor_roleta())
        print(self.bot.get_score())

        if self.bot.score < 500:
            self.vencedor["vencedor"] = 'Voce'

        if self.bot.score >= 3000:
            self.vencedor["vencedor"] = 'O bot'

        if self.vencedor["vencedor"] != '':
            return

        self.is_rotating = False  # Define como falso quando a rotação parar




    def valor_roleta(self):
        # A roleta tem 360 graus e 8 porções, cada uma ocupando 45 graus.
        # Calculamos em qual faixa de 45 graus o ângulo atual se encontra.
        angle_mod = self.angle % 360  # Garantir que o ângulo esteja no intervalo [0, 360]
        portion_index = int(((angle_mod + 22.5) // 45) % len(self.values))
        value = self.values[portion_index]  # Atribui o valor correspondente à porção
        return value




    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="impact", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.screen.blit(source=text_surf, dest=text_rect)




    def is_mouse_over_button(self, mouse_x, mouse_y):
        button_x = SCREEN_WIDTH / 2
        button_y = 330
        button_width = 150
        button_height = 50

        button_rect = pygame.Rect(
            button_x - button_width / 2,
            button_y - button_height / 2,
            button_width,
            button_height
        )

        return button_rect.collidepoint(mouse_x, mouse_y)
