import json

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.pontuacao = 0  

    def salvar_pontuacoes(self):
        """Salva a pontuação do jogador em um arquivo JSON."""
        try:
            with open("pontuacoes.json", "r") as arquivo:
                pontuacoes = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            pontuacoes = {}

        # Verifica se o nome do jogador já existe no arquivo e adiciona ou atualiza a pontuação
        if self.nome not in pontuacoes:
            pontuacoes[self.nome] = self.pontuacao
        else:
            # Se o jogador já existir, compara para manter a maior pontuação
            pontuacoes[self.nome] = max(pontuacoes[self.nome], self.pontuacao)

        # Salva as pontuações atualizadas de volta no arquivo
        with open("pontuacoes.json", "w") as arquivo:
            json.dump(pontuacoes, arquivo, indent=4)

    def carregar_pontuacoes(self):
        """Carrega as pontuações do arquivo JSON e retorna os 3 primeiros ordenados da maior para a menor."""
        try:
            with open("pontuacoes.json", "r") as arquivo:
                pontuacoes = json.load(arquivo)
            # Ordena as pontuações da maior para a menor e retorna os 3 primeiros
            return dict(sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)[:3])
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def atualizar_pontuacao(self, pontos):
        """Atualiza a pontuação do jogador."""
        self.pontuacao = pontos  

    def resetar_pontuacao(self):
        """Reseta a pontuação do jogador."""
        self.pontuacao = 0
