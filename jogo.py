import json
import pygame
from jogador import Jogador
from cobra import Cobra
from botao import Botao
from maca import Maca
import random
from config import Config  

class Jogo:
    def __init__(self, nome_jogador):
        self.nome_jogador = nome_jogador  # Salva o nome do jogador
        self.jogador = Jogador(nome_jogador)
        self.pontos = 0  # Inicializa os pontos
        self.nivel = 1  # Inicializa o nível
        self.jogando = True  # Flag para controlar o estado do jogo
        self.cobra = Cobra(300, 300)  # Inicializa a cobra na posição inicial
        self.maca = Maca() #inicializa a maca na posição inicial

    def verificar_colisao_maca(self):
        """Verifica se a cobra comeu a maçã."""
        # Verifica se a posição da cabeça da cobra coincide com a posição da maçã
        if self.cobra.lista_cobra[-1] == [self.maca.x, self.maca.y]:
            self.cobra.crescer()  # Aumenta o comprimento da cobra
            self.pontos += 1  # Incrementa os pontos
            self.maca.gerar_posicao(Config.LARGURA, Config.ALTURA, self.cobra)  # Gera uma nova posição para a maçã

    def pausar_jogo(self, tela):
        """Exibe o menu de pausa com as maiores pontuações e opções de continuar ou sair."""
        pausado = True
        fonte_titulo = pygame.font.SysFont("arial", 50)
        fonte_texto = pygame.font.SysFont("arial", 24)

        texto_pausa = fonte_titulo.render("Jogo Pausado", True, Config.PRETO)
        texto_instrucao = fonte_texto.render("Pressione ESPAÇO para continuar", True, Config.PRETO)
        texto_sair = fonte_texto.render("Pressione ESC para sair", True, Config.PRETO)

        # Carregar as maiores pontuações
        pontuacoes = self.jogador.carregar_pontuacoes()

        while pausado:
            tela.fill(Config.BRANCO)
            tela.blit(texto_pausa, (Config.LARGURA // 2 - texto_pausa.get_width() // 2, Config.ALTURA // 4))
            tela.blit(texto_instrucao, (Config.LARGURA // 2 - texto_instrucao.get_width() // 2, Config.ALTURA // 2))
            tela.blit(texto_sair, (Config.LARGURA // 2 - texto_sair.get_width() // 2, Config.ALTURA // 2 + 40))

            # Exibir as maiores pontuações
            y_offset = Config.ALTURA // 2 + 80
            for i, (nome, pontos) in enumerate(pontuacoes.items(), start=1):
                texto_pontuacao = fonte_texto.render(f"{i}º {nome}: {pontos} pontos", True, Config.PRETO)
                tela.blit(texto_pontuacao, (Config.LARGURA // 2 - texto_pontuacao.get_width() // 2, y_offset))
                y_offset += 30

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:  # Retoma o jogo ao pressionar espaço
                        pausado = False
                    elif evento.key == pygame.K_ESCAPE:  # Sai do jogo ao pressionar ESC
                        pygame.quit()
                        exit()

    def executar(self, tela):
        """Executa o jogo até o game over."""
        pygame.init()  # Pygame inicializado
        self.tela = pygame.display.set_mode((Config.LARGURA, Config.ALTURA))  # Cria a tela do jogo
        # Inicializando o relógio para controlar a taxa de atualização
        clock = pygame.time.Clock()
        tela = pygame.display.set_mode((Config.LARGURA, Config.ALTURA))  
        
        while self.jogando:
            # Trata os eventos (fechar janela, pressionar teclas, etc.)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:  # Se o jogador fechar a janela
                    self.jogando = False
                    exit()
                if evento.type == pygame.KEYDOWN:  # Verifica as teclas pressionadas
                    if evento.key == pygame.K_SPACE:  # Pausa o jogo ao pressionar espaço
                        self.pausar_jogo(tela)
                    elif evento.key == pygame.K_LEFT:
                        self.cobra.mudar_direcao(-Config.VELOCIDADE_BASE, 0)  # Move para a esquerda
                    elif evento.key == pygame.K_RIGHT:
                        self.cobra.mudar_direcao(Config.VELOCIDADE_BASE, 0)  # Move para a direita
                    elif evento.key == pygame.K_UP:
                        self.cobra.mudar_direcao(0, -Config.VELOCIDADE_BASE)  # Move para cima
                    elif evento.key == pygame.K_DOWN:
                        self.cobra.mudar_direcao(0, Config.VELOCIDADE_BASE)  # Move para baixo

            # Movimenta a cobra
            self.cobra.mover()

            # Verifica se a cobra comeu a maçã
            self.verificar_colisao_maca()

            # Verifica colisão com a parede
            if self.cobra.colisao_com_parede(Config.LARGURA, Config.ALTURA) or self.cobra.colisao_com_corpo():  
                print("Colisão detectada!")  
                self.salvar_pontuacao()
                self.exibir_game_over(tela)
                self.jogando = False 
            
            # Atualiza o nível com base na pontuação
            self.nivel = min((self.pontos // 10) + 1, len(Config.NIVEIS))  # Atualiza o nível conforme a pontuação

            # Ajusta a velocidade com base no nível
            self.velocidade = Config.NIVEIS.get(self.nivel, Config.VELOCIDADE_BASE)  # Obtém a velocidade do nível atual

            # Preenche a tela com a cor de fundo
            tela.fill(Config.BRANCO)

            # Exibe o nome do jogador, pontuação e o nível na tela
            fonte = pygame.font.SysFont(Config.FONTE, 24)
            texto_nome = fonte.render(f'Jogador: {self.nome_jogador}', True, Config.PRETO)
            texto_pontos = fonte.render(f'Pontuação: {self.pontos}', True, Config.PRETO)
            texto_nivel = fonte.render(f'Nível: {self.nivel}', True, Config.PRETO)
            tela.blit(texto_nome, (10, 10))
            tela.blit(texto_pontos, (10, 40))
            tela.blit(texto_nivel, (10, 70))

            # Desenha a cobra e a maçã
            for segmento in self.cobra.lista_cobra:
                pygame.draw.rect(tela, Config.VERDE, pygame.Rect(segmento[0], segmento[1], Config.VELOCIDADE_BASE, Config.VELOCIDADE_BASE))  
            pygame.draw.rect(tela, Config.COR_MACA, pygame.Rect(self.maca.x, self.maca.y, Config.VELOCIDADE_BASE, Config.VELOCIDADE_BASE)) 

            pygame.display.update()  # Atualiza a tela
            clock.tick(self.velocidade)  # Ajusta a velocidade do jogo com base no nível
    
    def salvar_pontuacao(self):
        """Salva a pontuação do jogador no arquivo JSON."""
        self.jogador.atualizar_pontuacao(self.pontos)
        self.jogador.salvar_pontuacoes()

    def reiniciar(self):
        """Reinicia o jogo para um novo começo."""
        self.pontos = 0
        self.nivel = 1
        self.jogando = True  # Define que o jogo está ativo novamente
        self.cobra = Cobra(Config.LARGURA // 2, Config.ALTURA // 2)  # Reinicia a cobra no centro
        self.maca = Maca()  # Reinicia a maçã
        self.maca.gerar_posicao(Config.LARGURA, Config.ALTURA, self.cobra)  # Gera uma nova posição para a maçã
        self.cobra.x_controle = 0  # Reseta o movimento horizontal da cobra
        self.cobra.y_controle = 0  # Reseta o movimento vertical da cobra
        self.cobra.movimento_inicial = False  # Reseta o estado de movimento inicial da cobra

    def exibir_game_over(self,tela):
        """Exibe a tela de Game Over e permite reiniciar ou sair."""
        tela.fill((0, 0, 0))  # Preenche a tela de preto
        fonte = pygame.font.SysFont("arial", 30)

        # Mensagem de Game Over
        texto_game_over = fonte.render(f"Você perdeu! {self.jogador.nome}: {self.jogador.pontuacao} pontos", True, (255, 0, 0))
        tela.blit(texto_game_over, (Config.LARGURA // 4, Config.ALTURA // 4))  

        # Carregar pontuações salvas e ordenadas
        pontuacoes = self.jogador.carregar_pontuacoes()

        # Exibir as pontuações na tela com colocação
        y_offset = Config.ALTURA // 2 - 50  
        for i, (nome, pontos) in enumerate(pontuacoes.items(), start=1):
            texto_pontuacao = fonte.render(f"{i}º {nome}: {pontos} pontos", True, (255, 255, 255))
            tela.blit(texto_pontuacao, (Config.LARGURA // 4, y_offset))  
            y_offset += 30

        # Criando botões para Jogar Novamente e Sair
        fonte_botao = pygame.font.SysFont("arial", 24)
        botao_jogar = fonte_botao.render("Jogar Novamente", True, (0, 255, 0))
        botao_sair = fonte_botao.render("Sair", True, (255, 0, 0))

        botao_jogar_rect = botao_jogar.get_rect(center=(Config.LARGURA // 2, Config.ALTURA - 100))  
        botao_sair_rect = botao_sair.get_rect(center=(Config.LARGURA // 2, Config.ALTURA - 50))  

        tela.blit(botao_jogar, botao_jogar_rect)
        tela.blit(botao_sair, botao_sair_rect)

        pygame.display.flip()  # Atualiza a tela

        # Loop para aguardar entrada do usuário
        esperando_resposta = True
        while esperando_resposta:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_jogar_rect.collidepoint(evento.pos):
                        self.reiniciar()  # Reinicia os valores do jogo
                        self.executar(tela)  # Chama o loop principal do jogo novamente
                    elif botao_sair_rect.collidepoint(evento.pos):
                        pygame.quit()
                        exit()
