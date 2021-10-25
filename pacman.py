import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()
tela = pygame.display.set_mode((800, 600), 0)

fonte = pygame.font.SysFont("arial", 24, True, False)

VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0 )
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)
CIANO = (0, 255, 255)
LARANJA = (255, 140, 0)
ROSA = (255, 20, 192)

ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass
    
    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass
    
class Cenario(ElementoJogo):
    def __init__(self, tamanho, pacman):
        self.pacman = pacman
        self.moviveis = []
        self.tamanho = tamanho 
        self.pontos = 0
        self.vidas = 5

        #estados possiveis 0-jogando 1-pausado 2-gameOver 3-Win
        self.estado = 0

        #aqui está o código para o cenário, cada 2 é a parede, 0 é o fundo negro, e o 1 é a bolinha
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def pintar_hue(self, tela):
        pontos_x = 30 * self.tamanho
        img_vidas = fonte.render(f"Vidas: {self.vidas}", True, AMARELO)
        img_pontos = fonte.render(f"Pontos: {self.pontos}", True, AMARELO)
        fonte_info = pygame.font.SysFont("arial", 16, True, False)
        img_pausar = fonte_info.render("Aperte 'P' para pausar", True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 50))
        tela.blit(img_vidas, (pontos_x, 100))
        tela.blit(img_pausar, (pontos_x, (tela.get_height() - 50)))

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar(self, tela):
        if self.estado == 0:
            self.pintar_jogando(tela)
        elif self.estado == 1:
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == 2:
            self.pintar_jogando(tela)
            self.pintar_gameOver(tela)
        elif self.estado == 3:
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto):
        img_texto = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - img_texto.get_width()) // 2
        texto_y = (tela.get_height() - img_texto.get_height()) // 2
        tela.blit(img_texto, (texto_x, texto_y))

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D O")
    
    def pintar_gameOver(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")
    
    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "P A R A B E N S,  V O C E  V E N C E U !!!!")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_hue(tela)

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho 

            # regra de negocio para pintar 0 o fundo e 2 a parede
            cor = AZUL if coluna == 2 else PRETO 
            metade_tamanho = self.tamanho // 2
            pygame.draw.rect(tela, cor,(x, y, self.tamanho, self.tamanho), 0)

            #pinta as bolinhas
            if coluna == 1: pygame.draw.circle(tela, AMARELO, (x + metade_tamanho, y + metade_tamanho), self.tamanho//10, 0) 

    def calcular_regras(self):
        if self.estado == 0:
            self.calcular_regras_jogando()
        if self.estado == 1:
            self.calcular_regras_pausado()
        elif self.estado == 2:
            self.calcular_regras_gameOver()

    def calcular_regras_pausado(self):
        pass
    
    def calcular_regras_gameOver(self):
        pass

    def calcular_regras_jogando(self):
       for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
               movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) \
                            and movivel.linha == self.pacman.linha \
                            and movivel.coluna == self.pacman.coluna:
                    self.vidas -= 1
                    if self.vidas <= 0:
                        self.estado = 2
                        return
                    else:
                        self.pacman.linha = 1
                        self.pacman.coluna = 1
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                    self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 307:
                            self.estado = 3
                else:
                    movivel.recusar_movimento(direcoes)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)

        return direcoes

    def processar_eventos(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    else:
                        self.estado = 0

class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):

        self.coluna = 1
        self.linha = 1

        self.centroX = 400
        self.centroY = 300
        self.tamanho = tamanho
        self.raio = self.tamanho//2
        self.abertura = 0
        self.velocidade_abertura = 1

        self.velocidade_geral = 1
        self.velX = 0
        self.velY = 0

        self.coluna_intençao = self.coluna
        self.linha_intencao = self.linha

    def pintar(self, tela):
        #desenha o corpo do pacman
        pygame.draw.circle(tela, AMARELO, (self.centroX, self.centroY), self.raio, 0)
        
        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio:
            self.velocidade_abertura = -1
        if self.abertura <= 0:
            self.velocidade_abertura = 1

        #desenho da boca
        canto_boca = (self.centroX, self.centroY)
        labio_superior = (self.centroX + self.raio, self.centroY - self.abertura)
        labio_inferior = (self.centroX + self.raio, self.centroY + self.abertura)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        #olho do pacman
        olhoX = int(self.centroX + self.raio/3)
        olhoY = int(self.centroY - self.raio * 0.70)
        olho_raio = int(self.raio/10)
        pygame.draw.circle(tela, PRETO, (olhoX, olhoY), olho_raio, 0)

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.velX
        self.linha_intencao = self.linha + self.velY
        self.centroX = int(self.coluna * self.tamanho + self.raio)
        self.centroY = int(self.linha * self.tamanho + self.raio)

    def processar_eventos(self, eventos):

        self.padroes = {pygame.K_RIGHT: self.velocidade_geral,
                        pygame.K_LEFT: -self.velocidade_geral,
                        pygame.K_UP: -self.velocidade_geral,
                        pygame.K_DOWN: self.velocidade_geral}
        
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    self.velX = self.padroes[e.key]
                if e.key in (pygame.K_UP,pygame.K_DOWN):
                    self.velY = self.padroes[e.key]
            if e.type == pygame.KEYUP:
                self.velX = 0
                self.velY = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
    
    def esquina(self, direcoes):
        pass

class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = ABAIXO
        self.tamanho = tamanho
        self.cor = cor
        

    def pintar(self, tela):
        #O CORPO DO FANTASMINHA HEHE
        fatia = self.tamanho // 8
        pX = int(self.coluna * self.tamanho)
        pY = int(self.linha * self.tamanho)
        contorno = [(pX, pY + self.tamanho), 
                    (pX + fatia * 1, pY + fatia * 2),
                    (pX + fatia * 3, pY + fatia // 2),
                    (pX + fatia * 3, pY),
                    (pX + fatia * 5, pY),
                    (pX + fatia * 6, pY + fatia // 2),
                    (pX + fatia * 7, pY + fatia * 2),
                    (pX + self.tamanho, pY + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        #O OLHO DELE HEHE
        olho_rext = fatia
        olho_rint = fatia // 2
        olho_EX = int(pX + fatia * 2.5)
        olho_EY = int(pY + fatia * 2.5)
        olho_DX = int(pX + fatia * 5.5)
        olho_DY = int(pY + fatia * 2.5)
        #olho esquerdo
        pygame.draw.circle(tela, BRANCO, (olho_EX, olho_EY), olho_rext, 0)
        pygame.draw.circle(tela, PRETO, (olho_EX, olho_EY), olho_rint, 0)
        #olho direito
        pygame.draw.circle(tela, BRANCO, (olho_DX, olho_DY), olho_rext, 0)
        pygame.draw.circle(tela, PRETO, (olho_DX, olho_DY), olho_rint, 0)
        

    def calcular_regras(self):
        if self.direcao == ACIMA: 
            self.linha_intencao -= self.velocidade
        if self.direcao == ABAIXO: 
            self.linha_intencao += self.velocidade
        if self.direcao == ESQUERDA: 
            self.coluna_intencao -= self.velocidade
        if self.direcao == DIREITA: 
            self.coluna_intencao += self.velocidade

    def mudar_direcoes(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
         self.mudar_direcoes(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao
    
    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcoes(direcoes)

    def processar_eventos(self, eventos):
        pass

if __name__ == "__main__":

    pacman = Pacman(600 // 30)

    blinky = Fantasma(VERMELHO, 600 // 30)
    inky = Fantasma(CIANO, 600 // 30)
    clyde = Fantasma(LARANJA, 600 // 30)
    pinky = Fantasma(ROSA, 600 // 30)

    cenario = Cenario(600 // 30,  pacman=pacman)

    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        #calcular as regras
        pacman.calcular_regras()
        cenario.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()

        #pintar a tela
        tela.fill(PRETO)
        cenario.pintar(tela)
        pacman.pintar(tela=tela)
        blinky.pintar(tela)
        blinky.pintar(tela)
        inky.pintar(tela)
        clyde.pintar(tela)
        pinky.pintar(tela)
        pygame.display.update()
        pygame.time.delay(90)
        
        #captura os eventos
        eventos = pygame.event.get()
        cenario.processar_eventos(eventos)
        pacman.processar_eventos(eventos)

        