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
EPS = 0.0000001

class Jarvis:
    '''
    Classe que implementa o algoritmo de Jarvis para encontrar o fecho convexo
    de um conjunto de pontos no plano 2D.
    '''
    def __init__(self, points):
        '''
        Constroi uma nova instancia para achar o convex hull do conjunto 
        'points'
        '''
        self.p = points

    def find_hull(self):
        '''
        Metodo que efetivamente implementa o algoritmo de Jarvis. Retorna uma 
        lista contendo os pontos do convex hull, no senti anti-horario do fecho.
        '''

        # numero de pontos na coleção
        n = len(self.p)

        # armazena os indices dos pontos no fecho, é inicializado com o indice
        # do ponto mais esquerda e baixo da colecao
        hull = [min(zip(self.p, range(n)))[1]]

        # ponto extremo do fecho
        self.p[hull[0]].hilight(color='yellow')
        control.sleep()

        while (True):
            i = (hull[-1] + 1)%n
            id_h = self.p[i].hilight(color='yellow')
            control.sleep()
            # econtrando o proximo ponto do fecho
            for j in range(n):
                if self.p[j] == self.p[hull[-1]] or self.p[j] == self.p[i]: 
                    continue
                if self.check(self.p[hull[-1]], self.p[i], self.p[j]):
                    control.plot_delete(id_h)
                    i = j
                    id_h = self.p[i].hilight(color='yellow')
            
            # poligono esta completo
            self.p[hull[-1]].lineto(self.p[i], color='yellow')
            if self.p[i] == self.p[hull[0]]: break
            hull.append(i)

        # fazendo com que hull seja uma lista de pontos 
        for i in range(len(hull)):
            hull[i] = self.p[hull[i]]
        return hull

    def left_test(self, s1, s2, p):
        '''
        Teste para saber se o ponto p esta a esquerda so segmento s1-s2.
        Retorna 1 se o ponto esta a esquerda, -1 se o ponto esta a direita, 
        0 caso seja colinear
        '''
        val = (s2.y-s1.y)*(p.x-s2.x) - (s2.x-s1.x)*(p.y-s2.y)
        if abs(val) < EPS:  return 0
        if val < 0:         return 1
        if val > 0:         return -1

    def check(self, p, q, r):
        '''
        Faz a checagem de atualização, checando se o ponto 'r' esta a 
        direita de p-q ou se 'q' esta na reta definida por q-r.
        '''
        a = p.lineto(q, color='blue')
        b = r.lineto(p, color='blue')
        c = r.lineto(q, color='blue')
        control.sleep()
        flag = False

        if self.left_test(p, q, r) == -1:
            flag = True
        
        elif self.left_test(p, q, r) == 0 and \
            min(p.x, r.x) <= q.x <= max(p.x, r.x) and \
            min(p.y, r.y) <= q.y <= max(p.y, r.y):
            flag = True
        
        for aux in [a, b, c]:
            control.plot_delete(aux)
        return flag

def find_ch(points):
    '''
    Encontra o convex hull de um conjunto de pontos usando a classe Jarvis. 
    Retorna p poligono que contem os pontos do fecho.
    points: conjunto de pontos
    '''

    if len(points) < 3:
        pol = polygon.Polygon(points)
        pol.extra_info = 'Numero de pontos da coleção deve ser maior ou igual a 3'
        return pol

    ch = Jarvis(points)
    ch_points = ch.find_hull()

    pol = polygon.Polygon(ch_points)
    if len(ch_points) > 2: 
        pol.extra_info = 'convex hull encontrado, possui %d pontos'%len(ch_points)
    else:
        pol.extra_info = 'não é possivel encontrar o convex hull dessa coleção'
    return pol