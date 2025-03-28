import sys
import os
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
        self.image = pygame.image.load(self.resource_path('./Assets/Roleta.png'))
        self.seta_roleta = pygame.image.load(self.resource_path('./Assets/seta.png'))
        self.rosto_normal = pygame.image.load(self.resource_path('./Assets/rosto_normal.png'))
        self.rosto_feliz1 = pygame.image.load(self.resource_path('./Assets/rosto_feliz1.png'))
        self.rosto_feliz2 = pygame.image.load(self.resource_path('./Assets/rosto_feliz2.png'))
        self.rosto_feliz3 = pygame.image.load(self.resource_path('./Assets/rosto_feliz3.png'))
        self.rosto_feliz4 = pygame.image.load(self.resource_path('./Assets/rosto_feliz4.png'))
        self.rosto_triste1 = pygame.image.load(self.resource_path('./Assets/rosto_triste1.png'))
        self.rosto_triste2 = pygame.image.load(self.resource_path('./Assets/rosto_triste2.png'))
        self.rosto_triste3 = pygame.image.load(self.resource_path('./Assets/rosto_triste3.png'))
        self.rosto_triste4 = pygame.image.load(self.resource_path('./Assets/rosto_triste4.png'))
        self.rostos_tristes_list = [self.rosto_triste1, self.rosto_triste2, self.rosto_triste3, self.rosto_triste4]
        self.rostos_felizes_list = [self.rosto_feliz1, self.rosto_feliz2, self.rosto_feliz3, self.rosto_feliz4]
        self.image = pygame.transform.scale(self.image, (600, 600))
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, 750))
        self.rosto_player = self.rosto_normal.get_rect(center=(195, 400))
        self.rosto_bot = self.rosto_normal.get_rect(center=(1080, 400))
        self.seta = self.seta_roleta.get_rect(center=((SCREEN_WIDTH / 2), 505))
        self.rosto_1 = self.rosto_normal
        self.rosto_2 = self.rosto_normal
        self.surf = pygame.image.load('./Assets/Cover.png')
        self.rect = self.surf.get_rect()
        self.angle = 0
        self.is_rotating = False
        self.values = [100, 200, 300, 400, 500, 600, 700, 800]
        self.player1 = Player('Player1')
        self.bot = Player('Bot')
        self.vencedor = {"vencedor": ''}


        self.current_message = None
        self.message_expire_time = 0
        self.current_bot_message = None
        self.bot_message_expire_time = 0

    def run(self):
        while self.vencedor["vencedor"] == '':
            self.screen.blit(source=self.surf, dest=self.rect)
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.image_rect.center)
            self.screen.blit(rotated_image, rotated_rect)

            self.screen.blit(self.rosto_1, self.rosto_player)
            self.screen.blit(self.rosto_2, self.rosto_bot)
            self.screen.blit(self.seta_roleta, self.seta)

            self.menu_text(30, f"{str(self.player1.score)},00", (0, 0, 0), (195, 200))
            self.menu_text(30, f"{str(self.bot.score)},00", (0, 0, 0), ((SCREEN_WIDTH - 110), 200))


            if self.current_message and time.time() < self.message_expire_time:
                text, color, pos = self.current_message
                self.menu_text(20, text, color, pos)

            if self.current_bot_message and time.time() < self.bot_message_expire_time:
                text, color, pos = self.current_bot_message
                self.menu_text(20, text, color, pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.is_mouse_over_button(mouse_x, mouse_y):
                        if not self.is_rotating:
                            self.is_rotating = True
                            threading.Thread(target=self.roda_girando).start()


        while True:
            self.screen.fill((0, 0, 0))
            self.menu_text(60, f"{self.vencedor['vencedor']} venceu a partida", (255, 255, 255),
                           (SCREEN_WIDTH / 2, 250))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            time.sleep(3)
            return False

    def roda_girando(self):

        start_time = time.time()
        rotation_time = random.uniform(5, 10)

        while time.time() - start_time < rotation_time:
            self.current_message = ('Você está girando a roleta', (0, 0, 0), (185, 650))
            self.message_expire_time = time.time() + 0.1
            if not self.is_rotating:
                break
            seconds = time.time() - start_time
            self.angle -= ((rotation_time * 2) - (seconds * 2))
            time.sleep(0.05)

        valor = self.valor_roleta()
        self.player1.update_score(valor)
        print(f"Jogador: {self.player1.get_score()}")

        if valor < 400:
            self.rosto_1 = random.choice(self.rostos_tristes_list)
            self.current_message = (f'Você perdeu R${valor - 400},00!', (0, 0, 0), (185, 650))
            self.message_expire_time = time.time() + 2
        elif valor == 400:
            self.rosto_1 = self.rosto_triste3
            self.current_message = ('Você não ganhou e nem perdeu!', (0, 0, 0), (185, 650))
            self.message_expire_time = time.time() + 2
        elif valor > 400:
            self.rosto_1 = random.choice(self.rostos_felizes_list)
            self.current_message = (f'Você ganhou R${valor - 400},00!', (0, 0, 0), (185, 650))
            self.message_expire_time = time.time() + 2

        if self.player1.score < 400:
            self.vencedor["vencedor"] = 'O bot'
            return

        if self.player1.score >= 2500:
            self.vencedor["vencedor"] = 'Você'
            return

        time.sleep(2)


        start_time = time.time()
        rotation_time = random.uniform(5, 10)

        while time.time() - start_time < rotation_time:
            self.current_bot_message = ('O bot está girando a roleta', (0, 0, 0), (1100, 650))
            self.bot_message_expire_time = time.time() + 0.1
            if not self.is_rotating:
                break
            seconds = time.time() - start_time
            self.angle -= ((rotation_time * 2) - (seconds * 2))
            time.sleep(0.05)

        valor = self.valor_roleta()
        self.bot.update_score(valor)
        print(f"Bot: {self.bot.get_score()}")

        if valor < 400:
            self.rosto_2 = random.choice(self.rostos_tristes_list)
            self.current_bot_message = (f'O bot perdeu R${valor - 400},00', (0, 0, 0), (1100, 650))
            self.bot_message_expire_time = time.time() + 2
        elif valor == 400:
            self.rosto_2 = self.rosto_triste3
            self.current_bot_message = ('O bot não ganhou e nem perdeu', (0, 0, 0), (1100, 650))
            self.bot_message_expire_time = time.time() + 2
        elif valor > 400:
            self.rosto_2 = random.choice(self.rostos_felizes_list)
            self.current_bot_message = (f'O bot ganhou R${valor - 400},00', (0, 0, 0), (1100, 650))
            self.bot_message_expire_time = time.time() + 2

        time.sleep(2)

        self.rosto_1 = self.rosto_normal
        self.rosto_2 = self.rosto_normal

        if self.bot.score < 400:
            self.vencedor["vencedor"] = 'Você'
            return

        if self.bot.score >= 2500:
            self.vencedor["vencedor"] = 'O bot'
            return

        self.is_rotating = False

    def valor_roleta(self):
        angle_mod = self.angle % 360
        portion_index = int(((angle_mod + 22.5) // 45) % len(self.values))
        return self.values[portion_index]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="arial", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.screen.blit(source=text_surf, dest=text_rect)


    def is_mouse_over_button(self, mouse_x, mouse_y):
        button_x = SCREEN_WIDTH / 2
        button_y = 330
        button_width = 180
        button_height = 80

        button_rect = pygame.Rect(
            button_x - button_width / 2,
            button_y - button_height / 2,
            button_width,
            button_height
        )

        return button_rect.collidepoint(mouse_x, mouse_y)

    def resource_path(self, relative_path):
        try:
            # Para o PyInstaller
            base_path = sys._MEIPASS
        except Exception:
            # Para ambiente de desenvolvimento
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)