import random
import pygame
from cobra import Cobra
from config import Config  

class Maca:
    def __init__(self):
        """Inicializa a maçã com uma posição aleatória."""
        self.x = 0
        self.y = 0
        self.gerar_posicao(Config.LARGURA, Config.ALTURA, None)  

    def gerar_posicao(self, largura, altura, cobra):
        """Gera uma nova posição aleatória para a maçã dentro do grid correto."""
        while True:
            self.x = random.randint(0, (largura // Config.VELOCIDADE_BASE) - 1) * Config.VELOCIDADE_BASE
            self.y = random.randint(0, (altura // Config.VELOCIDADE_BASE) - 1) * Config.VELOCIDADE_BASE
            # Verifica se a posição gerada não está ocupada pela cobra
            if not cobra or [self.x, self.y] not in cobra.lista_cobra:
                break

    def desenhar(self, tela):
        """Desenha a maçã na tela."""
        pygame.draw.rect(tela, Config.COR_MACA, pygame.Rect(self.x, self.y, Config.VELOCIDADE_BASE, Config.VELOCIDADE_BASE))  

