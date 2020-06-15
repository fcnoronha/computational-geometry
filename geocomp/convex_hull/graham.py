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

# para realizar a ordenação dos pontos
from functools import cmp_to_key

# constantes usadas no codigo
INF = float('inf')
EPS = 0.0000000001

class Graham:
    '''
    Classe que implementa o algoritmo de Graham para encontrar o fecho convexo
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

        # colocando ponto mais abaixo e a esquerda do conjunto na posição 0
        idx = 0
        for j in range(1, n):
            if (self.p[idx].y, self.p[idx].x) > (self.p[j].y, self.p[j].x):
                idx = j
        self.p[idx], self.p[0] = self.p[0], self.p[idx]

        # função comparadora para ordenamos a lista de pontos
        def cmp(a, b):
            return self.left_test(self.p[0], b, a)

        # ordenando os pontos de acordo com a posição polar a pivot
        self.p[1:] = sorted(self.p[1:], key=cmp_to_key(cmp))

        # 3 pontos iniciais do fecho
        hull = [0, 1, 2]
        self.p[hull[0]].hilight(color='yellow')
        self.p[hull[1]].hilight(color='yellow')
        self.p[hull[2]].hilight(color='yellow')
        self.p[hull[0]].lineto(self.p[hull[1]], color='yellow')
        self.p[hull[1]].lineto(self.p[hull[2]], color='yellow')
        control.sleep()

        def check(a, b, c):
            '''
            Checa se o ponto com indice 'c' esta a direita ou é colinear a 
            aresta a->b.
            '''
            # animacao \😆/ \😆/ \😆/ 
            #           |    |    | 
            #          / \  / \  / \
            a = self.p[a]
            b = self.p[b]
            c = self.p[c]
            id_ca = c.lineto(a, color='blue')
            id_cb = c.lineto(b, color='blue')
            control.sleep()
            c.remove_lineto(a, id=id_ca)
            c.remove_lineto(b, id=id_cb)

            return (self.left_test(a, b, c) <= 0)

        for k in range(3, n):
            self.p[k].hilight(color='yellow')
            control.sleep()

            # enquanto o novo ponto esta a direita da aresta anterior, realizo um
            # pop da mesma
            while len(hull) > 1 and check(hull[-2], hull[-1], k):
                self.p[hull[-1]].unhilight()
                self.p[hull[-2]].remove_lineto(self.p[hull[-1]])
                control.sleep()
                hull.pop()

            # incluindo novo ponto no hull
            self.p[hull[-1]].lineto(self.p[k], color='yellow')
            hull.append(k)
            control.sleep()

        # ligando ultimo no primeiro
        self.p[hull[-1]].lineto(self.p[hull[0]], color='yellow')

        # trantando o corner case em que o ultimo elemento é igual ao primeiro
        while self.p[hull[-1]] == self.p[hull[0]]:
            hull.pop()

        # fazendo com que hull seja uma lista de pontos 
        for i in range(len(hull)):
            hull[i] = self.p[hull[i]]
        return hull

    def left_test(self, s1, s2, p):
        '''
        Teste para saber se o ponto p esta a esquerda so segmento s1-s2.
        Retorna:
         1 se o ponto esta a esquerda; 
         -1 se o ponto esta a direita;
         0 caso seja colinear
        '''
        val = (s2.y-s1.y)*(p.x-s2.x) - (s2.x-s1.x)*(p.y-s2.y)
        if abs(val) < EPS:  return 0
        if val < 0:         return 1
        if val > 0:         return -1

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

    ch = Graham(points)
    ch_points = ch.find_hull()

    pol = polygon.Polygon(ch_points)
    if len(ch_points) > 2: 
        pol.extra_info = 'convex hull encontrado, possui %d pontos'%len(ch_points)
    else:
        pol.extra_info = 'não é possivel encontrar o convex hull dessa coleção'
    return pol