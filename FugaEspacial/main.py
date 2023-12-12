"""
Jogo: Fuga Espacial
Descrição: Um grupo de diplomatas escapam de uma fortaleza estelar a bordo de uma nave danificada.
   A nave precisa se desviar das ameaças e sobreviver até atingir a zona de segurança diplomática.
"""

import pygame
import time # uso da função-membro time.sleep(...) in loop
import random # uso da função-membro random.randrange (...) em loop
import os # usa função-membro os.path.isfile(...) em play_soundtrack
import sys # classe Soundtrack

class Background:
    """
    Esta classe define o Plano de Fundo do jogo
    """
    image = None
    margin_left = None
    margin_right = None

    def __init__(self):

        background_fig = pygame.image.load("Images/Images/background.png")
        background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800, 602))
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 602))
        self.margin_right = margin_right_fig

    # __init__()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        screen.blit(self.margin_left, (0, 0))  # 60 depois da primeira margem
        screen.blit(self.margin_right, (740, 0))  # 60 antes da segunda margem
    # draw()

    def draw_freedom(self, screen):
        screen.blit(self.image, (0,0))
    # draw_freedom()

    # Define posições das imagens do Plano de Fundo para criar o movimento
    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):

        for i in range(0, 2): #3 tiles
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))
    # move()
# Background:

class Player:
    """
    Esta classe define Jogador
    """
    image = None
    x = None
    y = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y
    # __init__()

    # Desenhar Player
    def draw (self, screen, x, y):
        screen.blit(self.image, (x, y))
    #draw()

    # Movimentar player
    def move(self, mudar_x):
        # Movimentação do player
        # Altera a coordenada x da nave de acordo com as mudanças do evento_handle() da class Game
        self.x += mudar_x
# Player:

class Hazard:
    """
    Esta classe define Ameaça ao Jogador
    """
    image = None
    x = None
    y = None

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y
    # __init__()

    # Desenhar Hazard
    def draw (self, screen, x, y):
        screen.blit(self.image, (x, y))
    #draw()

    def move(self, screen, velocidade_hazard):
        # adicionando movimento ao hazard
        self.y = self.y + velocidade_hazard / 4
        self.draw(screen, self.x, self.y)
        self.y += velocidade_hazard

class Soundtrack:
    soundtrack = None
    sound = None

    def __init__(self, soundtrack):
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + " not found... ignoring", file=sys.stderr)
    # __init__()

    def play(self):
        pygame.mixer.music.load(self.soundtrack)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)  # set loops to -1 to loop the music indefinitely
    # play()

    def set(self, soundtrack):
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + " not found... ignoring", file=sys.stderr)
    # set()

    def play_sound(self, sound):
        if os.path.isfile(sound):
            self.sound = sound
            pygame.mixer.music.load(self.sound)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        else:
            print(sound + " file not found... ignoring", file=sys.stderr)
    # play_sound()
# Soundtrack:

class Game:
    screen = None
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None
    player = None
    hazard = []
    soundtrack = None

    # movimento do Player
    mudar_x = 0.0

    def __init__(self, size, fullscreen):

        """
        Função que inicializa o pygame, define a resolução da tela,
        caption, e desabilita o mouse.
        """

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))  # tamanho da tela
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Fuga Espacial')

    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            # se clicar em qualquer tecla, entra no if
            if event.type == pygame.KEYDOWN:
                # se clicar na seta da esquerda, anda 3 para a esquerda no eixo x
                if event.key == pygame.K_LEFT:
                    self.mudar_x = -3
                # se clicar na seta da direita, anda 3 para a direita no eixo x
                if event.key == pygame.K_RIGHT:
                    self.mudar_x = 3

            # se soltar qualquer tecla, não faz nada
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.mudar_x = 0
    # handle_events()

    def write_message(self, message, R, G, B, x, y):
        my_font1 = pygame.font.Font('Fonts/Fonts/Fonte4.ttf', 100)
        # Mensagens para o jogador
        render_text = my_font1.render(message, False, (R, G, B)) # (texto, opaco/transparente)
        # desenha
        self.screen.blit(render_text, (x, y))


    def elements_draw(self):
        self.background.draw(self.screen)
    # elements_draw()

    # Informa a quantidade de hazard que passaram e a Pontuação
    def score_card(self, screen, h_passou, score):
        font = pygame.font.SysFont(None, 35)
        passou = font.render("Passou: " + str(h_passou), True, (255, 255, 128))
        score = font.render("Score: " + str(score), True, (253, 231, 32))
        screen.blit(passou, (0, 50))
        screen.blit(score, (0, 100))
    #score_card()

    def draw_explosion(self, screen, x, y):
        explosion_fig = pygame.image.load("Images/explosion.png")
        explosion_fig.convert()
        explosion_fig = pygame.transform.scale(explosion_fig, (150,150))
        screen.blit(explosion_fig, (x,y))

    def loop(self):
        """
        Esta função contém o laço principal
        """
        score = 0
        h_passou = 0

        # variáveis para movimento de Plano de Fundo/Background e para Hazards
        velocidade_background = 10
        velocidade_hazard = 10

        hzrd = 0
        h_x = random.randrange(125, 660)
        h_y = -500


        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        # Criar o Plano de fundo
        self.background = Background()

        # Posição do Player
        x = (self.width - 56) / 2
        y = self.height - 125

        # Criar o Player
        self.player = Player(x, y)

        # Criar os Hazards
        self.hazard.append(Hazard("Images/Images/satelite.png", h_x, h_y))
        self.hazard.append(Hazard("Images/Images/nave.png", h_x, h_y))
        self.hazard.append(Hazard("Images/Images/cometaVermelho.png", h_x, h_y))
        self.hazard.append(Hazard("Images/Images/meteoros.png", h_x, h_y))
        self.hazard.append(Hazard("Images/Images/buracoNegro.png", h_x, h_y))

        # Criar trilha sonora
        self.soundtrack = Soundtrack('Sounds/Sounds/song.wav')
        self.soundtrack.play()
        # Inicializamos o relogio e o dt que vai limitar o valor de FPS
        # frames por segundo do jogo
        clock = pygame.time.Clock()
        dt = 16

        # Início do laço principal do programa
        while self.run:
            clock.tick(1000 / dt)

            # Handle Input Events
            self.handle_events()

            # Desenha o background buffer
            self.elements_draw()

            # adiciona movimento ao background
            self.background.move(self.screen, self.height, movL_x, movL_y, movR_x, movR_y)
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            #se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600

            # Movimentação do Player
            # Altera a coordenada x da nave de acordo comas mudanças no event_handle() para ela se mover
            self.player.move(self.mudar_x)

            # Desenha o Player
            self.player.draw(self.screen, self.player.x, self.player.y)

            # Mostrar score
            self.score_card(self.screen, h_passou, score)

            # Restrições do movimento do Player
            # Se o Player bate na lateral não é Game Over
            if self.player.x > 760 - 92 or self.player.x < 40 + 5:

                # Som da colisão nas margens
                self.soundtrack.play_sound('Sounds/jump2.wav')

                # Exibe mensagem
                self.write_message("VOCÊ BATEU!", 255, 255, 255, 80, 200) # fonte branca
                pygame.display.update()  # atualizar a tela
                time.sleep(3)
                self.loop()
                self.run = False

            # Vitória do jogador
            if score == 100: # se atingir score de 100, vence o jogo

                # Música da vitória
                self.soundtrack.play_sound('Sounds/Sounds/racetheme.mp3')

                # Desenha área diplomática
                self.background.draw_freedom(self.screen)

                # Escreve mensagens de vitória
                self.write_message("100 PONTOS!", 255, 117, 24, 90, 100) # laranja
                self.write_message("VOCÊ VENCEU!", 255, 117, 24, 2, 300)  # laranja

                pygame.display.update()
                time.sleep(4)
                self.run = False

            # adicionando movimento ao hazard
            self.hazard[hzrd].move(self.screen, velocidade_hazard)

            # definindo onde hazard vai aparecer, recomeçando a posição do obstaculo e da faixa
            if self.hazard[hzrd].y > self.height:
                self.hazard[hzrd].y = 0 - self.hazard[hzrd].image.get_height()
                self.hazard[hzrd].x = random.randrange(125, 650 - self.hazard[hzrd].image.get.height())
                hzrd = random.randint(0, 4)
                # determinando quantos hazard passaram e a pontuação
                h_passou = h_passou + 1
                score = h_passou * 10

            # Aumenta a velocidade de score == 60
            if score == 60:
                velocidade_hazard += 0.1

            # Colisão e game over
            player_rect = self.player.image.get_rect()
            player_rect.topleft = (self.player.x, self.player.y)
            hazard_rect = self.hazard[hzrd].image.get_rect()
            hazard_rect.topleft = (self.hazard[hzrd].x, self.hazard[hzrd].y)

            if hazard_rect.colliderect(player_rect):
                # Emite som da colisão
                self.soundtrack.play_sound('Sounds/crash.wav')

                # Exibe a imagem da explosão
                self.draw_explosion(self.screen, self.player.x - (self.player.image.get.width() / 2),
                                    self.player.y - (self.player.image.get_height() / 2))

                # Exibe mensagem de Game Over
                self.write_message("GAME OVER!", 255, 0, 0, 80, 200) #vermelha
                pygame.display.update()
                time.sleep(3)
                self.run = False

            # Atualiza a tela
            pygame.display.update()
            clock.tick(1000 / dt)

        # while self.run
    # loop()
# Game:

# Cria o objeto game e chama o loop básico
game = Game("resolution", "fullscreen")
game.loop()