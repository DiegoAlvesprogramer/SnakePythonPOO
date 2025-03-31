from config import Config  

class Cobra:
    def __init__(self, x_inicial, y_inicial):
        """Inicializa a cobra com a posição inicial e comprimento."""
        # Alinha a posição inicial ao grid
        self.x_cobra = (x_inicial // Config.VELOCIDADE_BASE) * Config.VELOCIDADE_BASE
        self.y_cobra = (y_inicial // Config.VELOCIDADE_BASE) * Config.VELOCIDADE_BASE
        self.comprimento = 3
        self.x_controle = 0  # Começa parada até o jogador pressionar uma tecla
        self.y_controle = 0
        self.direcao_anterior = None
        self.movimento_inicial = False

        # Inicializa a cobra com 3 segmentos alinhados ao grid
        self.lista_cobra = [
            [self.x_cobra, self.y_cobra],
            [self.x_cobra - Config.VELOCIDADE_BASE, self.y_cobra],
            [self.x_cobra - 2 * Config.VELOCIDADE_BASE, self.y_cobra],
        ]

    def mover(self):
        """Move a cobra com base nos controles atuais."""
        # Verifica se a cobra recebeu um comando de movimento
        if self.x_controle == 0 and self.y_controle == 0:
            return  # Não move a cobra até que uma direção seja definida

        self.x_cobra += self.x_controle
        self.y_cobra += self.y_controle
        self.lista_cobra.append([self.x_cobra, self.y_cobra])

        if len(self.lista_cobra) > self.comprimento:
            self.lista_cobra.pop(0)

        self.movimento_inicial = True  # Marca que a cobra começou a se mover

    def mudar_direcao(self, x, y):
        """Muda a direção da cobra, evitando reversões impossíveis."""
        # Evita que a cobra inverta a direção imediatamente
        if (x, y) != (-self.x_controle, -self.y_controle):
            self.x_controle = x
            self.y_controle = y

    def colisao_com_parede(self, largura, altura):
        """Verifica se a cobra colidiu com as paredes."""
        return self.x_cobra < 0 or self.x_cobra >= largura or self.y_cobra < 0 or self.y_cobra >= altura

    def colisao_com_corpo(self):
        """Verifica se a cobra colidiu com ela mesma."""
        return self.movimento_inicial and [self.x_cobra, self.y_cobra] in self.lista_cobra[:-1]

    def crescer(self):
        """Aumenta o comprimento da cobra ao comer a maçã."""
        self.comprimento += 1