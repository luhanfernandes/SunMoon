import pygame
from pygame.locals import *
from sys import exit
from random import randint
import controles

pygame.init()

#CONFIGURAÇÃO DO TAMANHO DA TELA
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONTROLE DE FPS
relogio = pygame.time.Clock()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONTROLE DE SOM
controles.musica()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONFIGURAÇÃO DE ICON + BACKGROUND + NOME
background = pygame.image.load('Cenário/background.png').convert_alpha()
icon = pygame.image.load('Icon\SunMoon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('SunMoon')
nuvens = pygame.image.load('Cenário/nuvens.png').convert_alpha()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#FONTE
fonte = pygame.font.SysFont('arial', 20, True, False)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def reiniciar_jogo(): #REINICIAR O JOGO
    global pontos_lua, pontos_sol, velocidade_jogo_lua, velocidade_jogo_sol, timer
    pontos_lua = 0
    pontos_sol = 0
    velocidade_jogo_lua = 6
    velocidade_jogo_sol = 6
    controles.timer = 120
    personagem_lua.rect.y = personagem_lua.pos_y_inicial
    personagem_sol.rect.y = personagem_sol.pos_y_inicial

    estrela_sol.rect.x = controles.reinicia_posicao
    estrela_sol.rect.y = randint(1, 230)
    estrela_lua.rect.y = randint(310, 540)
    estrela_lua.rect.x = controles.reinicia_posicao

    arco_iris_sol.rect.x = controles.reinicia_posicao
    arco_iris_sol.rect.y = randint(1, 230)
    arco_iris_lua.rect.x = controles.reinicia_posicao
    arco_iris_lua.rect.y = randint(310, 540)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def pausar_jogo():
    global velocidade_jogo_lua, velocidade_jogo_sol
    velocidade_jogo_lua = 0
    velocidade_jogo_sol = 0
    controles.pausa = True

def despausar_jogo():
    global velocidade_jogo_sol, velocidade_jogo_lua
    velocidade_jogo_sol = controles.velocidade_atual_sol
    velocidade_jogo_lua = controles.velocidade_atual_lua
    controles.pausa = False
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#CONFIGURAÇÃO DE PERSONAGEM

#carregamento dos personagens
sprite_sheet_sol = pygame.image.load('Personagens/personagem_sol.png').convert_alpha()
sprite_sheet_lua = pygame.image.load('Personagens/personagem_lua.png').convert_alpha()

#velocidade do jogo
velocidade_jogo_sol = 6
velocidade_jogo_lua = 6

#pontuação
pontos_sol = 0
pontos_lua = 0

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONTROLADOR PERSONAGEM SOL
class Personagem_sol(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_personagem_sol = []
        for i in range(3):
            img = sprite_sheet_sol.subsurface((i * 69, 0), (69, 90))
            img = pygame.transform.scale(img, (60, 75))
            self.imagens_personagem_sol.append(img)

        self.index_lista = 0
        self.image = self.imagens_personagem_sol[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = 210 - 65 // 2
        self.rect.center = (100, self.pos_y_inicial)
        self.personagem_sol_pulo = False

    def pular(self):
        self.personagem_sol_pulo = True

    def update(self):
        if self.personagem_sol_pulo == True:
            if self.rect.y <= 15:
                self.personagem_sol_pulo = False
            self.rect.y -= 15
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 5
            else:
                self.rect.y = self.pos_y_inicial
        if controles.pausa == False:
            if self.index_lista > 2:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_personagem_sol[int(self.index_lista)]
        else:
            pass
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#controlador personagem_lua
class Personagem_lua(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_personagem_lua = []
        for i in range(3):
            img = sprite_sheet_lua.subsurface((i * 69, 0), (69, 90))
            img = pygame.transform.scale(img, (60, 75))
            self.imagens_personagem_lua.append(img)

        self.index_lista_lua = 0
        self.image = self.imagens_personagem_lua[self.index_lista_lua]
        self.rect = self.image.get_rect()
        self.pos_y_inicial = 510 - 65 // 2
        self.rect.center = (100, self.pos_y_inicial)
        self.personagem_lua_pulo = False

    def pular_lua(self):
        self.personagem_lua_pulo = True

    def update(self):
        if self.personagem_lua_pulo == True:
            if self.rect.y <= 315:
                self.personagem_lua_pulo = False
            self.rect.y -= 15
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 5
            else:
                self.rect.y = self.pos_y_inicial
        if controles.pausa == False:
            if self.index_lista_lua > 2:
                self.index_lista_lua = 0
            self.index_lista_lua += 0.25
            self.image = self.imagens_personagem_lua[int(self.index_lista_lua)]
        else:
            pass

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONFIGURAÇÃO PONTUAÇÃO
#controlador arco_iris_SOL
class Arco_iris_sol(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Capturaveis/arco_iris.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (controles.sorteio_x_arco_iris,  controles.sorteio_y_sol)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = controles.sorteio_x_arco_iris
            self.rect.y = controles.sorteio_y_sol
        self.rect.x -= velocidade_jogo_sol
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#controlador estrela_SOL
class Estrela_sol(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Capturaveis/estrela.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (controles.sorteio_x_estrela,  controles.sorteio_y_sol)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = controles.sorteio_x_estrela
            self.rect.y = controles.sorteio_y_sol
        self.rect.x -= velocidade_jogo_sol
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#controle arco_iris_LUA
class Arco_iris_lua(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Capturaveis/arco_iris.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (controles.sorteio_x_arco_iris,  controles.sorteio_y_lua)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = controles.sorteio_x_arco_iris
            self.rect.y = controles.sorteio_y_lua
        self.rect.x -= velocidade_jogo_lua
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#controlador estrela_LUA
class Estrela_lua(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Capturaveis/estrela.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (controles.sorteio_x_estrela,  controles.sorteio_y_lua)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = controles.sorteio_x_estrela
            self.rect.y = controles.sorteio_y_lua
        self.rect.x -= velocidade_jogo_lua

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Controle e adição de sprites
todas_as_sprites = pygame.sprite.Group()
personagem_sol = Personagem_sol()
personagem_lua = Personagem_lua()
arco_iris_sol = Arco_iris_sol()
estrela_sol = Estrela_sol()
arco_iris_lua = Arco_iris_lua()
estrela_lua = Estrela_lua()
todas_as_sprites.add(personagem_sol, personagem_lua, arco_iris_sol, estrela_sol, arco_iris_lua, estrela_lua)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Criação dos Group
grupo_arco_iris= pygame.sprite.Group()
grupo_estrela = pygame.sprite.Group()
#Adição dos Group
grupo_arco_iris.add(arco_iris_sol, arco_iris_lua)
grupo_estrela.add(estrela_sol, estrela_lua)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONTROLE DO CENÁRIO
chao = pygame.image.load('Cenário/chao_duplo.png').convert_alpha()

#cenario sol
arvore = pygame.image.load('Cenário/arvore_grama.png').convert_alpha()
aviao = pygame.image.load('Cenário/aviao.png').convert_alpha()
aviao = pygame.transform.scale(aviao, (64, 32))
arvore_grande = pygame.image.load('Cenário/arvore_grande.png').convert_alpha()
arbusto = pygame.image.load('Cenário/arbusto.png').convert_alpha()
tronco = pygame.image.load('Cenário/tronco.png').convert_alpha()

x_arvore = 200
x_aviao = 0
x_arvore_grande = 600
x_arbusto = 850
x_tronco = 1100

#CENÁRIO LUA

#arvore_noite
arvore_noite = pygame.image.load('Cenário/arvore_grama_noite.png').convert_alpha()
aviao_noite = pygame.image.load('Cenário/aviao_noite.png').convert_alpha()
aviao_noite = pygame.transform.scale(aviao_noite, (64, 32))
arvore_grande_noite = pygame.image.load('Cenário/arvore_grande_noite.png')
arbusto_noite = pygame.image.load('Cenário/arbusto_noite.png')
tronco_noite = pygame.image.load('Cenário/tronco_noite.png')

x_arvore_noite = 1100
x_aviao_noite = 100
x_arvore_grande_noite = 200
x_arbusto_noite = 500
x_tronco_noite = 850

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#CONTROLE DA ESTRUTURA DO JOGO

#MENU DO JOGO
start = False

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            exit()

        if e.type == KEYDOWN:
            if e.key == K_h:
                tutorial = pygame.image.load('Menu/tutorial.png')
                tutorial = pygame.transform.scale(tutorial, (800, 600))
                tela.blit(tutorial, controles.controle_de_tela)
                start = 10
                pygame.display.flip()

            if e.key == K_BACKSPACE:
                start = False

            if e.key == K_p:
                start = True

            if e.key == K_k:
                pygame.quit()
                exit()

    if start == False:
        menu = pygame.image.load('Menu/Menu.png')
        menu = pygame.transform.scale(menu, (800, 600))
        tela.blit(menu, controles.controle_de_tela)
        pygame.display.flip()

    if start == True:
        #CONTROLE FPS
        relogio.tick(30)
        #CONTROLE DE MOVIMENTAÇÃO DO CENÁRIO
        x_aviao -= velocidade_jogo_sol
        x_arvore -= velocidade_jogo_sol
        x_arvore_grande -= velocidade_jogo_sol
        x_arbusto -= velocidade_jogo_sol
        x_tronco -= velocidade_jogo_sol

        x_aviao_noite += velocidade_jogo_lua
        x_arvore_noite -= velocidade_jogo_lua
        x_arvore_grande_noite -= velocidade_jogo_lua
        x_arbusto_noite -= velocidade_jogo_lua
        x_tronco_noite -= velocidade_jogo_lua

        if x_aviao < - controles.sair_da_tela:
            x_aviao = 800
        if x_arvore < - controles.sair_da_tela:
            x_arvore = randint(1000, 1200)
        if x_arvore_grande < - controles.sair_da_tela:
             x_arvore_grande = randint(1300, 1600)
        if x_arbusto < - controles.sair_da_tela:
            x_arbusto = randint(1700, 2000)
        if x_tronco < - controles.sair_da_tela:
            x_tronco = randint(2100, 2400)

        if x_aviao_noite > controles.sair_da_tela:
            x_aviao_noite = - 800
        if x_arvore_noite < - controles.sair_da_tela:
            x_arvore_noite = randint(2100, 2400)
        if x_arvore_grande_noite < - controles.sair_da_tela:
            x_arvore_grande_noite = randint(1700, 2000)
        if x_arvore_noite < - controles.sair_da_tela:
            x_arbusto_noite = randint(1300, 1600)
        if x_tronco_noite < - controles.sair_da_tela:
            x_tronco_noite = randint(1000, 1200)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        #CONTROLE DA PONTUAÇÃO DO SOL
        mensagem_sol = f'PONTOS: {pontos_sol}'
        pontuacao_sol = fonte.render(mensagem_sol, False, (controles.preto))

        #CONTROLE DA PONTUAÇÃO DA LUA
        mensagem_lua = f'PONTOS: {pontos_lua}'
        pontuacao_lua = fonte.render(mensagem_lua, False, (controles.branco))


        #CONTROLE DO TEMPO DE JOGO
        cronometro = f'TEMPO: {controles.timer}'
        cronometro_sol = fonte.render(cronometro, False, (controles.preto))
        cronometro_lua = fonte.render(cronometro, False, (controles.branco))
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #CONTROLE DE EVENTOS NO JOGO
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        #CONTROLE DE TECLA
            if event.type == KEYDOWN:

                #CONTROLE TECLA SOL
                if event.key == K_w:
                    if personagem_sol.rect.y != personagem_sol.pos_y_inicial:
                        pass
                    else:
                        personagem_sol.pular()

                #CONTROLE TECLA LUA
                if event.key == K_UP:
                    if personagem_lua.rect.y != personagem_lua.pos_y_inicial:
                        pass
                    else:
                        personagem_lua.pular_lua()

                if event.key == K_r:
                    if controles.timer == 0:
                        reiniciar_jogo()
                    else:
                        pass

                if event.key == K_j:
                    if controles.pausa == True:
                        despausar_jogo()
                    else:
                        pausar_jogo()
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #CONTROLE DE COLISÃO
        sol_captura_arco_iris = pygame.sprite.spritecollide(personagem_sol, grupo_arco_iris, False, pygame.sprite.collide_mask)
        sol_captura_estrela = pygame.sprite.spritecollide(personagem_sol, grupo_estrela, False, pygame.sprite.collide_mask)

        lua_captura_arco_iris = pygame.sprite.spritecollide(personagem_lua, grupo_arco_iris, False, pygame.sprite.collide_mask)
        lua_captura_estrela = pygame.sprite.spritecollide(personagem_lua, grupo_estrela, False, pygame.sprite.collide_mask)

        sobreposicao_sol = pygame.sprite.spritecollide(arco_iris_sol, grupo_estrela, False, pygame.sprite.collide_mask)
        sobreposicao_lua = pygame.sprite.spritecollide(arco_iris_lua, grupo_estrela, False, pygame.sprite.collide_mask)

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #CONTROLE DE PONTUAÇÃO + VELOCIDADE DO JOGO PARA O PERSONAGEM SOL
        if sol_captura_arco_iris:
            arco_iris_sol.rect.x = randint(largura, 1100)
            arco_iris_sol.rect.y = randint(0, 240)
            pontos_sol += 1
            controles.contador_sol += 1
            if controles.contador_sol == 5:
                if velocidade_jogo_sol >= 22:
                    velocidade_jogo_sol += 0
                else:
                    velocidade_jogo_sol += 4
                    controles.contador_sol = 0
                    controles.velocidade_atual_sol = velocidade_jogo_sol
        if sol_captura_estrela:
            estrela_sol.rect.x = randint(largura, 1100)
            estrela_sol.rect.y = randint(0, 240)
            if pontos_sol == 0:
                pass
            else:
                pontos_sol -= 1
                controles.contador_sol -= 1
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        if sobreposicao_sol:
            arco_iris_sol.rect.x = randint(largura, 1100)
            arco_iris_sol.rect.y = randint(0, 240)
            estrela_sol.rect.x = randint(largura, 1100)
            estrela_sol.rect.y = randint(0, 240)

        if sobreposicao_lua:
            arco_iris_lua.rect.x = randint(largura, 1100)
            arco_iris_lua.rect.y = randint(310, 540)
            estrela_lua.rect.x = randint(largura, 1100)
            estrela_lua.rect.y = randint(310, 540)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        if lua_captura_arco_iris:
            arco_iris_lua.rect.x = randint(largura, 1100)
            arco_iris_lua.rect.y = randint(310, 540)
            if pontos_lua == 0:
                pass
            else:
                pontos_lua -= 1
                controles.contador_lua -= 1
        if lua_captura_estrela:
            estrela_lua.rect.x = randint(largura, 1100)
            estrela_lua.rect.y = randint(310, 540)
            pontos_lua += 1
            controles.contador_lua += 1
            if controles.contador_lua == 5:
                if velocidade_jogo_lua >= 22:
                    velocidade_jogo_lua += 0
                else:
                    velocidade_jogo_lua += 4
                    controles.contador_lua = 0
                    controles.velocidade_atual_lua = velocidade_jogo_lua
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        #CONTROLE DO TEMPO
        controles.cronometro()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        #APRESENTAÇÃO EM TELA DO CENÁRIO
        tela.blit(background, controles.controle_de_tela)

        #controle cenário sol
        tela.blit(aviao, (x_aviao, 10))
        tela.blit(arvore, (x_arvore, 146))
        tela.blit(arvore_grande, (x_arvore_grande, 146))
        tela.blit(arbusto, (x_arbusto, 160))
        tela.blit(tronco, (x_tronco, 238))

        #controle cenário lua
        tela.blit(aviao_noite, (x_aviao_noite, 300))
        tela.blit(arvore_noite, (x_arvore_noite, 445))
        tela.blit(arvore_grande_noite, (x_arvore_grande_noite, 445))
        tela.blit(arbusto_noite, (x_arbusto_noite, 455))
        tela.blit(tronco_noite, (x_tronco_noite, 538))

        #controle de background
        tela.blit(nuvens, controles.controle_de_tela)
        tela.blit(chao, controles.controle_de_tela)

        #APRESENTAÇÃO DE TEMPO + PONTUAÇÃO
        tela.blit(pontuacao_sol, (650, 10)), tela.blit(cronometro_sol, (300, 10))
        tela.blit(pontuacao_lua, (650, 310)), tela.blit(cronometro_lua, (300, 310))

        #APRESENTAÇÃO DE SPRITES + ATUALIZAÇÃO + DECLARAÇÃO DO VENCEDOR
        todas_as_sprites.draw(tela)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        if controles.pausa == True:
            tela.blit(controles.pausado, controles.controle_de_tela)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        if controles.timer <= 0:
            controles.stop_game()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
            if pontos_sol > pontos_lua:
                sol_vence =f'O JOGADOR SOL VENCEU COM: {pontos_sol} PONTOS!'
                ganhou_sol = pygame.image.load('Vencedor/vencedor_sol.png')
                tela.blit(ganhou_sol, controles.controle_de_tela)
                vencedor_sol = fonte.render(sol_vence, False, (controles.preto))
                tela.blit(vencedor_sol, (200, 300))

            if pontos_lua > pontos_sol:
                lua_vence = f'O JOGADOR LUA VENCEU COM: {pontos_lua} PONTOS!'
                ganhou_lua = pygame.image.load('Vencedor/vencedor_lua.png')
                tela.blit(ganhou_lua, controles.controle_de_tela)
                vencedor_lua = fonte.render(lua_vence, False, (controles.branco))
                tela.blit(vencedor_lua, (200, 300))

            if pontos_sol == pontos_lua:
                empatou = f'O JOGO TERMINOU EMPATADO EM {pontos_sol} x {pontos_lua}'
                deu_empate = pygame.image.load('Vencedor/draw.png')
                tela.blit(deu_empate, controles.controle_de_tela)
                empate = fonte.render(empatou, False, (controles.branco))
                tela.blit(empate, (200, 300))
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        else:
            todas_as_sprites.update()
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#


        pygame.display.flip()
