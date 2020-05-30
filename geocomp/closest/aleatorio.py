'''
    By Felipe Noronha
    IME USP - 2020
'''

from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import polygon
from geocomp.common import point
from geocomp.common import control
from geocomp import config
from random import shuffle
import math

# constantes usadas no codigo
INF = float('inf')
EPS = 0.0000000001

class Closest:  
    '''
    classe que implementa as funcoes necessarias para se encotrar o par de
    pontos mais proximos de maneira aleatorizada.
    '''
    def __init__(self, pts):
        '''
        metodo construtor
        '''
        # melhor par encontrado ate agora, distancia entre eles e
        # id's da parte grafica
        self.best = [[None, None, INF], [None, None, None]]
        self.pts = pts
        self.delta = INF
        self.h = {} # dicionario/hashtable
        self.id_lines = [] # lista de ids usados na animacao

    def update(self, a, b):
        '''
        função auxiliar que recebe 2 pontos e atualiza o melhor caso necessario
        a, b: pontos candidatos
        '''

        a_id = a.hilight(color='cyan')
        b_id = b.hilight(color='cyan')
        l_id = a.lineto(b, color='cyan')
        control.sleep()
        d = a.distance_to(b)
        if d < EPS: d = 0
        if d < self.best[0][2]:

            # atualizando visualização
            control.sleep()
            if self.best[1][0] != None:
                self.best[0][0].unhilight(self.best[1][0])
            if self.best[1][1] != None:
                self.best[0][1].unhilight(self.best[1][1])
            if self.best[1][2] != None:
                self.best[0][0].remove_lineto(self.best[0][1], self.best[1][2])

            self.best[0][0] = a
            self.best[0][1] = b
            self.best[0][2] = d
            self.best[1][0] = a.hilight(color='green')
            self.best[1][1] = b.hilight(color='green')
            self.best[1][2] = a.lineto(b, color='green')
        
        a.unhilight(a_id)
        b.unhilight(b_id)
        a.remove_lineto(b, l_id)
        return d

    def find_limits(self):
        '''
        encontra o ponto superior direito e o inferior esquerdo do retangulo
        que contem todos os pontos da coleção, com um aumento de 20% no
        comprimento e largura
        p: coleção de pontos
        '''
        
        self.ur = [self.pts[0].x, self.pts[0].x]
        self.bl = [self.pts[0].x, self.pts[0].y]
        for p in self.pts:
            x, y = p.x, p.y
            if x < self.bl[0]: self.bl[0] = x
            if x > self.ur[0]: self.ur[0] = x
            if y < self.bl[1]: self.bl[1] = y
            if y > self.ur[1]: self.ur[1] = y

        # 10 porcento a mais em cada dimensao
        delta_x = (self.ur[0] - self.bl[0])/10.0
        delta_y = (self.ur[1] - self.bl[1])/10.0
        self.ur[0] += delta_x
        self.ur[1] += delta_y
        self.bl[0] -= delta_x
        self.bl[1] -= delta_y

    def index_square(self, p):
        '''
        encotra os indices do quadrado em que o ponto se encontra, 
        coluna e linha. 
        p: ponto
        '''
        r = math.floor( (p.x - self.bl[0]) / (self.delta/2.0) )
        s = math.floor( (p.y - self.bl[1]) / (self.delta/2.0) )
        return r, s

    def build_ans(self):
        '''
        constroi o segmento de resposta
        '''
        closest = segment.Segment(self.best[0][0], self.best[0][1])
        closest.extra_info = 'Menor distancia: %.4f' %self.best[0][2]
        return closest

    def build_animation_lines(self):
        '''
        controi as linhas imaginarias que dividem o plano em quadrados
        '''
        delta = self.delta/2.0
        for il in self.id_lines:
            control.plot_delete(il)
        self.id_lines.clear()
        r = self.bl[1]
        c = self.bl[0]
        while r < self.ur[1]:
            self.id_lines.append( control.plot_horiz_line(r, color='blue') )
            r += delta
        while c < self.ur[0]:
            self.id_lines.append( control.plot_vert_line(c, color='blue') )
            c += delta
        control.sleep()

    def build_square(self, c, r):
        '''
        constroi um quadrado usado para marcar qual ponto do plano estamos 
        usando para comparar com um ponto atual
        c: indice da coluna
        r: indice da linha
        '''
        sbl = [(c)*(self.delta/2.0) + self.bl[0], (r)*(self.delta/2.0) + self.bl[1]]
        sur = [sbl[0] + (self.delta/2.0), sbl[1] + (self.delta/2.0)]
        
        tl = point.Point(sbl[0], sur[1])
        tr = point.Point(sur[0], sur[1])
        dr = point.Point(sur[0], sbl[1])
        dl = point.Point(sbl[0], sbl[1])
        sqr = polygon.Polygon([tl, tr, dr, dl])
        sqr.plot(color='yellow')
        control.sleep()
        return sqr

    def update_hashtable(self, p):
        '''
        insere o ponto p na hashtable
        '''
        r, s = self.index_square(p)
        self.h[(r,s)] = p

    def build_hashtable(self, idx):
        '''
        constroi a hashtable
        idx: index maximo, inclusivo, dos pontos que devem ser considerados
        '''
        self.build_animation_lines()
        self.h.clear()
        for i in range(idx+1):
            self.update_hashtable(self.pts[i])

    def find_closest(self):
        
        # embaralhando os pontos
        shuffle(self.pts)

        if len(self.pts) < 2: return self.build_ans()
        self.find_limits()

        # inicializando com dois primeiros pontos
        self.delta = self.update(self.pts[0], self.pts[1])

        # mais de um ponto na mesma posição
        if self.delta < EPS: return self.build_ans()

        self.build_hashtable(1)
        for i in range(2, len(self.pts)):
            pj = self.pts[i]
            r, s = self.index_square(pj)
            new_dist = INF
            for t in range(-2, 3):
                for u in range(-2, 3):
                    id_pt = pj.hilight(color='yellow')
                    sqr = self.build_square(r+t, s+u)
                    if (r+t, s+u) in self.h:
                        new_dist = self.update(pj, self.h[(r+t, s+u)])
                    sqr.hide()
                    control.plot_delete(id_pt)
                    
            if new_dist + EPS < self.delta:
                self.delta = new_dist
                if self.delta < EPS: break
                self.build_hashtable(i)
            else:
                self.update_hashtable(pj)
        
        return self.build_ans()

def Aleatorio(pts):
    '''
    função principal que calcula o par de pontos mais proximos usando um
    algoritmo aleatorizado, obtendo tempo esperado linear.
    pts: conjunto de pontos da colecao
    '''

    c = Closest(pts)
    return c.find_closest()

