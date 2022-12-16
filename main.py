import pygame as p
import os
import json
from tkinter import *
from config import *

p.init()
p.font.init()

#Configurações da janela.
LARGURA, ALTURA = 1100, 640
janela = p.display.set_mode((LARGURA, ALTURA))
p.display.set_caption("Chess")
fonte = p.font.SysFont('Comic Sans MS', 35)
fonte2 = p.font.SysFont('Comic Sans MS', 25)

#Peças.
brancas = ["Pb", "Tb", "Cb", "Bb", "Qb", "Kb"]
pretas = ["Tp", "Cp", "Bp", "Qp", "Kp", "Pp"]

#Cores.
branco = (255, 255, 255)
marrom = (150, 75, 0)
preto = (0, 0, 0)
azul = (0, 0, 255)
amarelo_claro = (240, 220, 23)
vermelho = (255, 0, 0)
azul_claro = (135, 206, 235)
vermelho_claro = (205, 24, 56)
verde = (153, 204, 50)
verde2 = (153, 250, 100)
verde3 = (0, 255, 0)
cinza_escuro = (46, 46, 46)
cinza_barra = (97, 100, 105)
cinza =  (130, 128, 128)

botoes = []
botoes_log =  []
imagens_pecas = {}
imagens_pecas2 = {}
pecas_capturadas = []

def upload_imagens():
    img_pecas = ["Tp", "Cp", "Bp", "Qp", "Kp", "Pp", "Pb", "Tb", "Cb", "Bb", "Qb", "Kb"]
    for peca in img_pecas:
        imagens_pecas[peca] = p.image.load("imagens/" + peca + ".png")
        imagens_pecas2[peca] = p.transform.scale(p.image.load("imagens/" + peca + ".png"), (40, 40))

#Função que desenha o tabuleiro. Ela cria vários quadrados pretos e brancos, além de criar os botões e tabela de peças capturadas.
def desenhar_tabuleiro():
    if jogo.modo == 'normal':
        if jogo.branco_move:
            borda = p.draw.circle(janela, cinza_barra,[(695), (50)], 35)
            turno =  p.draw.circle(janela, branco,[(695), (50)], 30)
        else:
            borda = p.draw.circle(janela, cinza_barra,[(695), (50)], 35)
            turno =  p.draw.circle(janela, preto,[(695), (50)], 30)

    elif jogo.modo == 'sandbox':
        borda = p.draw.circle(janela, cinza_barra,[(695), (50)], 35)
        turno =  p.draw.circle(janela, cinza_escuro,[(695), (50)], 30)

    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    p.draw.rect(janela, branco,[(80*j), (80*i), 80, 80])
                else:
                    p.draw.rect(janela, preto,[(80*j), (80*i), 80, 80])
            else:
                if j % 2 == 0:
                    p.draw.rect(janela, preto,[(80*j), (80*i), 80, 80])
                else:
                    p.draw.rect(janela, branco,[(80*j), (80*i), 80, 80])

    p.draw.rect(janela, cinza_barra,[(680), (380), 375, 260])
    p.draw.line(janela, branco,[680, 380], [680, 638], )
    p.draw.line(janela, branco,[1055, 380], [1055, 638], 2)
    p.draw.line(janela, branco,[867, 420], [867, 638], 2)
    p.draw.line(janela, branco,[680, 420], [1054, 420], 2)
    p.draw.line(janela, branco,[680, 380], [1054, 380], 2)
    p.draw.line(janela, branco,[680, 638], [1055, 638], 2)
    botao_retroceder = p.draw.rect(janela, azul_claro,[(755), (300), 230, 50])
    botao_reset = p.draw.rect(janela, vermelho_claro,[(755), (30), 230, 50])
    botao_load = p.draw.rect(janela, verde,[(755), (120), 230, 50])
    botao_save = p.draw.rect(janela, amarelo_claro,[(755), (210), 230, 50])
    textoReset = fonte.render('Reset', False, (preto))
    textoLoad = fonte.render('Load', False, (preto))
    textoSave = fonte.render('Save', False, (preto))
    textoPecas = fonte2.render('Peças capturadas', False, (branco))
    textoRt = fonte.render('Undo', False, (preto))
    janela.blit(textoReset, (822, 28))
    janela.blit(textoLoad, (833, 118))
    janela.blit(textoSave, (830, 208))
    janela.blit(textoPecas, (760, 380))
    janela.blit(textoRt, (830, 298))
    botoes.append(botao_reset)
    botoes.append(botao_load)
    botoes.append(botao_save)
    botoes_log.append(botao_retroceder)

def peca_capturada():
    for i in range(4):
        for j in range(4):
            p.draw.rect(janela, branco,[(685 + 45*j), (445 + 45*i), 40, 40])
            p.draw.rect(janela, preto,[(875 + 45*j), (445 + 45*i), 40, 40])
    x = 0
    y = 0
    a = 0
    b = 0
    for peca in jogo.pecas_capturadas:
        if peca != "__":
            if peca in pretas:
                pc = imagens_pecas2[peca]
                p.transform.scale(pc, (10, 10))
                if x % 4 == 0 and x != 0:
                    y += 1
                    x = 0
                janela.blit(pc, p.Rect((685 + 45*x), (445 + 45*y), 40, 40))
                x += 1
            if peca in brancas:
                pc = imagens_pecas2[peca]
                p.transform.scale(pc, (10, 10))
                if a % 4 == 0 and a != 0:
                    b += 1
                    a = 0
                janela.blit(pc, p.Rect((875 + 45*a), (445 + 45*b), 40, 40))
                a += 1

#Essa é a função que desenha as peças. Ela posiciona todas as peças em suas posições de acordo com o estado do tabuleiro.
def desenhar_pecas():
    for i in range(8):
        for j in range(8):
            peca = jogo.board[i][j]
            if peca != "__":
                janela.blit(imagens_pecas[peca], p.Rect((80*j), (80*i), 80, 80))

def load():
    caminho = r'C:\Users\zackb\OneDrive\Área de Trabalho\chess\saves'
    arquivos =  os.listdir(caminho)
    def sairF():
        janela_load.destroy()
    def loadFile():
        name = fileName.get() + '.txt'
        if name in arquivos:
            arquivo = open("saves/" + name, 'r')
            saveFile = json.load(arquivo)
            tabuleiro = saveFile[0]
            registro = saveFile[1]
            pecasCapturadasFile = saveFile[2]
            turno = saveFile[3]
            arquivo.close()
            jogo.board = tabuleiro
            jogo.registro = registro
            jogo.pecas_capturadas = pecasCapturadasFile
            jogo.branco_move = turno
            janela_load.destroy()
            p.display.update()
        else:
            label0 = Label(janela_load, text='Arquivo não encontrado!', font=("Helvetica", 11))
            label0.config(bg= 'grey')
            label0.place(x=0, y=100, height = 30, width = 400)

    janela_load = Tk()
    janela_load.title("Load")
    janela_load.configure(background= 'grey')
    janela_load.geometry("400x200")
    janela_load.resizable(False, False)
    enviar = Button(text= "Enviar", command=loadFile)
    sairB = Button(text= "Sair", command=sairF)
    fileName = Entry(janela_load)
    fileName.place(x=150, y=70,height = 20, width = 100)
    enviar.place(x=150, y=140,height = 20, width = 100)
    sairB.place(x=150, y=170, height = 20, width = 100)
    label = Label(janela_load, text='Digite o nome do arquivo desejado', font=("Helvetica", 11))
    label.place(x=0, y=20, height = 30, width = 400)
    label.config(bg= 'grey')
    janela_load.mainloop()

def save():
    caminho = r'C:\Users\zackb\OneDrive\Área de Trabalho\chess\saves'
    arquivos =  os.listdir(caminho)
    def sairS():
        janela_save.destroy()
    def saveFile():
        name = fileName.get() + '.txt'
        
        if name in arquivos:
            label0 = Label(janela_save, text='Save já existe!', font=("Helvetica", 11))
            label0.place(x=0, y=100, height = 30, width = 400)
            label0.config(bg= 'grey')
        else:
            lista = [jogo.board, jogo.registro, jogo.pecas_capturadas, jogo.branco_move]
            create_save = open(f'saves\{name}', 'x')
            create_save.close()
            save = open(f'saves\{name}', 'w')
            json.dump(lista, save)
            save.close()
            label1 = Label(janela_save, text='Arquivo Salvo!', font=("Helvetica", 11))
            label1.place(x=0, y=100, height = 30, width = 400)
            label1.config(bg= 'grey')
            janela_save.destroy()

    janela_save = Tk()
    janela_save.title("Save")
    janela_save.configure(background= 'grey')
    janela_save.geometry("400x200")
    janela_save.resizable(False, False)
    enviar = Button(text= "Salvar", command=saveFile)
    sairB = Button(text= "Sair", command=sairS)
    fileName = Entry(janela_save)
    fileName.place(x=150, y=70,height = 20, width = 100)
    enviar.place(x=150, y=140,height = 20, width = 100)
    sairB.place(x=150, y=170, height = 20, width = 100)
    label = Label(janela_save, text='Digite o nome do save desejado',  font=("Helvetica", 11))
    label.config(bg= 'grey')
    label.place(x=0, y=20, height = 30, width = 400)
    janela_save.mainloop()

rodar = True
jogo = Jogo()

movimentos_validos = jogo.get_movimentos_possiveis()
calcular_movimentos = False

player_clicks = []
clique = False
quadrado = ()

def janela_config():
    def sairS():
        jogo.rodar = False
        janelaConfig.destroy()
        
    def normal():
        jogo.modo = 'normal'
        janelaConfig.destroy()

    def sandbox():
        jogo.modo = 'sandbox'
        janelaConfig.destroy()

    janelaConfig = Tk()
    janelaConfig.title("Menu")
    janelaConfig.configure(background= 'grey')
    janelaConfig.geometry("400x200")
    janelaConfig.resizable(False, False)
    normal = Button(text= "Normal", command=normal)
    sandbox = Button(text= "Sandbox", command=sandbox)
    sairB = Button(text= "Sair", command=sairS)
    normal.place(x=75, y=90,height = 20, width = 100)
    sandbox.place(x=225, y=90,height = 20, width = 100)
    sairB.place(x=150, y=150, height = 20, width = 100)
    label = Label(janelaConfig, text='Selecione o modo de jogo',  font=("Helvetica", 11))
    label.config(bg= 'grey')
    label.place(x=0, y=20, height = 30, width = 400)
    janelaConfig.mainloop()

janela_config()

while rodar:
    clock = p.time.Clock()
    clock.tick(10)
    janela.fill(cinza_escuro)
    upload_imagens()
    desenhar_tabuleiro()
    desenhar_pecas()
    peca_capturada()
    p.display.update()

    if jogo.rodar == False:
        rodar = False

    if calcular_movimentos == True:
        movimentos_validos = jogo.get_movimentos_possiveis()
        calcular_movimentos = False

    for event in p.event.get():
        if event.type == p.QUIT:
            jogo.rodar = False
            rodar = False
  
        if event.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            x, y = p.mouse.get_pos()
            x = x//80
            y = y//80

            if x <= 8:
                if quadrado == (x, y):
                    print(quadrado)
                    quadrado = () 
                    player_clicks = []
            
                else:
                    p.draw.rect(janela, verde3,[(80*x), (80*y), 80, 80], 5)
                    p.display.update()
                    quadrado = (x, y)
                    player_clicks.append(quadrado)

                if len(player_clicks) == 2:
                    movimento_peca = Movimento(player_clicks[0], player_clicks[1], jogo.board)
                    if jogo.modo == 'normal':
                        for movimentoCALCULADO in movimentos_validos:
                            if movimento_peca.moveID == movimentoCALCULADO.moveID:
                                jogo.mover(movimento_peca)
                                calcular_movimentos = True
                                quadrado = () 
                                player_clicks = []                  

                    elif jogo.modo == 'sandbox':
                        if jogo.board[player_clicks[0][1]][player_clicks[0][0]] != "__":
                            jogo.mover(movimento_peca)
                            quadrado = () 
                            player_clicks = []
                        else:
                            quadrado = () 
                            player_clicks = []

            else:
                if botoes[0].collidepoint(pos):
                    calcular_movimentos = True
                    jogo.branco_move = True
                    player_clicks = []
                    quadrado = () 
                    jogo.pecas_capturadas = []
                    jogo.registro = []
                    p.draw.rect(janela, preto,[(750), (25), 240, 60], 7)
                    jogo.board =[
                    ["Tp", "Cp", "Bp", "Qp", "Kp", "Bp", "Cp", "Tp"],
                    ["Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
                    ["Tb", "Cb", "Bb", "Qb", "Kb", "Bb", "Cb", "Tb"]
                    ]
                    p.display.update()
                
                if botoes[1].collidepoint(pos):
                    p.draw.rect(janela, preto,[(750), (115), 240, 60], 7)
                    p.display.update()
                    load()
                    calcular_movimentos = True

                if botoes[2].collidepoint(pos):
                    p.draw.rect(janela, preto,[(750), (205), 240, 60], 7)
                    p.display.update()
                    save()

                if botoes_log[0].collidepoint(pos):
                    p.draw.rect(janela, preto,[(750), (295), 240, 60], 7)
                    p.display.update()
                    calcular_movimentos = True
                    jogo.retroceder()
