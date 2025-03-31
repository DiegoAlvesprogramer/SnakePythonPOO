import pygame
import time
from config import Config 

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor_normal, cor_hover, acao=None):
        self.texto = texto
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.acao = acao
        self.rect = pygame.Rect(x, y, largura, altura)
        self.tempo_ultimo_clique = 0  # Controle do tempo do último clique

    def desenhar(self, tela):
        """Desenha o botão na tela com a cor apropriada e o texto centralizado."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(tela, self.cor_hover, self.rect)  # Cor quando o mouse passa sobre o botão
        else:
            pygame.draw.rect(tela, self.cor_normal, self.rect)  # Cor normal

        # Renderiza o texto e o centraliza no botão
        fonte = pygame.font.SysFont(Config.FONTE, 24)  
        texto = fonte.render(self.texto, True, Config.BRANCO)  
        tela.blit(texto, (self.x + (self.largura - texto.get_width()) // 2, self.y + (self.altura - texto.get_height()) // 2))

    def verificar_clique(self, evento):
        """Verifica se o botão foi clicado e executa a ação associada."""
        if evento.type == pygame.MOUSEBUTTONDOWN:  # Verifica se houve um clique
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):  # Verifica se o clique foi dentro do botão
                if pygame.time.get_ticks() - self.tempo_ultimo_clique > 200:  # Evita múltiplos cliques rápidos
                    self.tempo_ultimo_clique = pygame.time.get_ticks()  # Atualiza o tempo do último clique
                    if self.acao:  # Executa a ação associada ao botão
                        self.acao()
