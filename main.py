from logging import config
import pygame
from botao import Botao
from config import Config  
from jogo import Jogo

# Inicializando o Pygame
pygame.init()

# Configurando a tela do jogo
tela = pygame.display.set_mode((Config.LARGURA, Config.ALTURA))  
pygame.display.set_caption("Jogo da Cobra")  # Título da janela

# Variáveis globais
estado_jogo = "menu"  # Estado inicial do jogo


def desenhar_menu(tela, fonte, nome_jogador, jogar, sair, mensagem_erro):
    """Desenha os elementos do menu na tela."""
    tela.fill(Config.BRANCO)  
    jogar.desenhar(tela)  
    sair.desenhar(tela)  
 
    # Exibe o texto "Digite seu nome" na tela
    texto_nome = fonte.render(f'Nome do jogador: {nome_jogador}', True, (0, 0, 0))
    tela.blit(texto_nome, (Config.LARGURA // 2 - texto_nome.get_width() // 2, Config.ALTURA // 2 - 100))

    # Exibe mensagem de erro, se houver
    if mensagem_erro:
        texto_erro = fonte.render(mensagem_erro, True, (255, 0, 0))
        tela.blit(texto_erro, (Config.LARGURA // 2 - texto_erro.get_width() // 2, Config.ALTURA // 2 - 150))

    pygame.display.update()  # Atualiza a tela


def exibir_menu(tela):
    """Exibe o menu inicial do jogo e captura o nome do jogador."""
    global estado_jogo
    nome_jogador = ""  # Variável para armazenar o nome do jogador
    fonte = pygame.font.SysFont(Config.FONTE, 24)  
    mensagem_erro = ""  # Mensagem de erro para exibir na tela

    # Adiciona os botões "Jogar" e "Sair"
    jogar = Botao("Jogar", Config.LARGURA // 2 - 100, Config.ALTURA // 2 + 50, 200, 50, (0, 255, 0), (0, 200, 0), None)
    sair = Botao("Sair", Config.LARGURA // 2 - 100, Config.ALTURA // 2 + 150, 200, 50, (255, 0, 0), (200, 0, 0), pygame.quit)

    # Loop principal do menu
    while True:
        desenhar_menu(tela, fonte, nome_jogador, jogar, sair, mensagem_erro)

        # Loop para tratar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se o usuário clicar no "X" para fechar
                pygame.quit()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:  # Se o usuário clicar com o mouse
                if jogar.rect.collidepoint(evento.pos):  # Se o clique foi no botão "Jogar"
                    if nome_jogador.strip():  # Verifica se o nome não está vazio
                        estado_jogo = "jogo"  # Atualiza o estado global
                        jogar_acao(nome_jogador)  # Passa o nome para a função de jogar
                        return
                    else:
                        mensagem_erro = "Por favor, insira um nome válido!"  # Atualiza a mensagem de erro

                elif sair.rect.collidepoint(evento.pos):  # Se o clique foi no botão "Sair"
                    pygame.quit()
                    return

            if evento.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if evento.key == pygame.K_BACKSPACE:  # Se for BACKSPACE, remove o último caractere
                    nome_jogador = nome_jogador[:-1]
                elif evento.key == pygame.K_RETURN:  # Se for ENTER, confirma o nome e vai para o jogo
                    if nome_jogador.strip():
                        estado_jogo = "jogo"
                        jogar_acao(nome_jogador)
                        return
                    else:
                        mensagem_erro = "Por favor, insira um nome válido!"
                else:
                    nome_jogador += evento.unicode  # Adiciona o caractere digitado ao nome


def jogar_acao(nome_jogador):
    """Inicia o jogo e passa o nome do jogador."""
    print(f"Iniciando o jogo... Jogador: {nome_jogador}")
    jogo = Jogo(nome_jogador)  # Passando o nome do jogador para o jogo
    jogo.executar(tela)  # Executa o jogo


# Loop principal
while True:
    if estado_jogo == "menu":
        exibir_menu(tela)
    elif estado_jogo == "jogo":
        pass  # O jogo será executado pela classe Jogo
