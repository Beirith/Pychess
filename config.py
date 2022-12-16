import pygame as p

p.init()
brancas = ["Pb", "Tb", "Cb", "Bb", "Qb", "Kb"]
pretas = ["Tp", "Cp", "Bp", "Qp", "Kp", "Pp"]

class Jogo():
    def __init__(self):

        self.board =[
                    ["Tp", "Cp", "Bp", "Qp", "Kp", "Bp", "Cp", "Tp"],
                    ["Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["__", "__", "__", "Pp", "__", "__", "__", "__"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["__", "__", "__", "__", "__", "__", "__", "__"],
                    ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
                    ["Tb", "Cb", "Bb", "Qb", "Kb", "Bb", "Cb", "Tb"]
                    ]

        self.rodar = True
        self.modo = 'normal'
        self.funcoes_movimento = {'P': self.getPeaoM, 'T': self.getTorreM, 'C': self.getCavaloM, 'B': self.getBispoM, 'Q': self.getRainhaM, 'K': self.getReiM}
        self.branco_move = True
        self.pecas_capturadas = []
        self.registro = []
        self.ReiBranco = (7, 4)
        self.ReiPreto = (0, 4)
         
    def mover(self, movimento):
        self.board[movimento.X_inicio][movimento.Y_inicio] = "__"
        self.board[movimento.X_fim][movimento.Y_fim] = movimento.peca_movida
        self.capturar = self.pecas_capturadas.append(movimento.peca_capturada)
        self.branco_move = not self.branco_move
        self.registrar = self.registro.append([movimento.peca_movida, movimento.peca_capturada, movimento.X_inicio, movimento.Y_inicio, movimento.X_fim, movimento.Y_fim])
        if movimento.peca_movida == 'Kb':
            self.ReiBranco = (movimento.X_fim, movimento.Y_fim)
        
        if movimento.peca_movida == 'Kp':
            self.ReiPreto = (movimento.X_fim, movimento.Y_fim)

    def retroceder(self):
        if len(self.registro) != 0:
            move = self.registro.pop()
            self.board[move[2]][move[3]] = move[0]
            self.board[move[4]][move[5]] = move[1]
            self.retornar_peca = self.pecas_capturadas.pop()
            self.branco_move = not self.branco_move

    def get_movimentos_possiveis(self):
        movimentos = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turno = self.board[i][j][1]
                if (turno == 'b' and self.branco_move) or (turno == 'p' and not self.branco_move):
                    peca = self.board[i][j][0]
                    self.funcoes_movimento[peca](i,j, movimentos)
                    
        return movimentos
    
    def getPeaoM(self, i, j, movimentos):
        if self.branco_move:
            if self.board[i-1][j] == "__":
                movimentos.append(Movimento((j,i), (j,i-1), self.board))
                if i == 6 and self.board[i-2][j] == "__":
                    movimentos.append(Movimento((j,i), (j,i-2), self.board))

            if (j-1) >= 0:
                if self.board[i-1][j-1][1] == 'p':
                    movimentos.append(Movimento((j,i), (j-1,i-1), self.board))

            if (j+1) <= 7:
                if self.board[i-1][j+1][1] == 'p':
                    movimentos.append(Movimento((j,i), (j+1,i-1), self.board))

        else:
            if self.board[i+1][j] == "__":
                movimentos.append(Movimento((j,i), (j,i+1), self.board))
                if i == 1 and self.board[i+2][j] == "__":
                    movimentos.append(Movimento((j,i), (j,i+2), self.board))

            if (j-1) >= 0:
                if self.board[i+1][j-1][1] == 'b':
                    movimentos.append(Movimento((j,i), (j-1,i+1), self.board))

            if (j+1) <= 7:
                if self.board[i+1][j+1][1] == 'b':
                    movimentos.append(Movimento((j,i), (j+1,i+1), self.board))
 
    def getTorreM(self, i, j, movimentos):
        corInimiga = 'p' if self.branco_move else 'b'
        direcoes = ((-1,0),(0,-1), (1,0), (0,1))
        for d in direcoes:
            for h in range(1,8):
                x_final = j + d[0] * h
                y_final = i + d[1] * h
                if 0 <= x_final < 8 and 0 <= y_final < 8:
                    peca_caminho = self.board[y_final][x_final]
                    if peca_caminho == '__':
                        movimentos.append(Movimento((j,i), (x_final,y_final), self.board))
                    elif peca_caminho[1] == corInimiga:
                        movimentos.append(Movimento((j,i), (x_final,y_final), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getCavaloM(self, i, j, movimentos):
        corInimiga = 'b' if self.branco_move else 'w'
        direcoes = ((-2,-1),(-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1),)
        for d in direcoes:
            x_final = j + d[0] 
            y_final = i + d[1] 
            if 0 <= x_final < 8 and 0 <= y_final < 8:
                peca_caminho = self.board[y_final][x_final]
                if peca_caminho[1] != corInimiga:
                    movimentos.append(Movimento((j,i), (x_final,y_final), self.board))

    def getBispoM(self, i, j, movimentos):
        corInimiga = 'p' if self.branco_move else 'b'
        direcoes = ((-1,1),(1,-1), (-1,-1), (1,1))
        for d in direcoes:
            for h in range(1,8):
                x_final = j + d[0] * h
                y_final = i + d[1] * h
                if 0 <= x_final < 8 and 0 <= y_final < 8:
                    peca_caminho = self.board[y_final][x_final]
                    if peca_caminho == '__':
                        movimentos.append(Movimento((j,i), (x_final,y_final), self.board))
                    elif peca_caminho[1] == corInimiga:
                        movimentos.append(Movimento((j,i), (x_final,y_final), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getRainhaM(self, i, j, movimentos):
        self.getTorreM(i, j, movimentos)
        self.getBispoM(i, j, movimentos)

    def getReiM(self, i, j, movimentos):
        corInimiga = 'b' if self.branco_move else 'w'
        direcoes = ((-1,-1),(-1,0), (-1,-1), (0,-1), (0,1), (1,-1), (1,0), (1,1),)
        for d in range(8):
            x_final = j + direcoes[d][0] 
            y_final = i + direcoes[d][1] 
            if 0 <= x_final < 8 and 0 <= y_final < 8:
                peca_caminho = self.board[y_final][x_final]
                if peca_caminho[1] != corInimiga:
                    movimentos.append(Movimento((j,i), (x_final,y_final), self.board))

class Movimento():
    def __init__(self, inicio, fim, board):
        self.X_inicio = inicio[1]
        self.Y_inicio = inicio[0]
        self.X_fim = fim[1]
        self.Y_fim = fim[0]
        self.peca_movida = board[self.X_inicio][self.Y_inicio]
        self.peca_capturada = board[self.X_fim][self.Y_fim]
        self.moveID = (self.X_inicio * 100) + (self.Y_inicio * 1000) + (self.X_fim ) + (self.Y_fim * 10)

    def __eq__(self, other):
        if isinstance(other, Movimento):
            return self.moveID == other.moveID
        return False 