'''
    By Felipe Noronha
    IME USP - 2020
'''

from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from random import shuffle
import math

# constantes usadas no codigo
INF = float('inf')
EPS = 0.0000000001

# função auxiliar que recebe 2 pontos e atualiza o melhor caso necessario
def update(a, b, best):
    '''
    a, b: pontos candidatos
    best: melhores pontos encontrados
    '''

    a_id = a.hilight(color='blue')
    b_id = b.hilight(color='blue')
    l_id = a.lineto(b, color='blue')
    control.sleep()

    d = a.distance_to(b)
    if d < EPS: d = 0
    if d < best[0][2]:

        # atualizando visualização
        control.sleep()
        if best[1][0] != None:
            best[0][0].unhilight(best[1][0])
        if best[1][1] != None:
            best[0][1].unhilight(best[1][1])
        if best[1][2] != None:
            best[0][0].remove_lineto(best[0][1], best[1][2])

        best[0][0] = a
        best[0][1] = b
        best[0][2] = d
        best[1][0] = a.hilight(color='green')
        best[1][1] = b.hilight(color='green')
        best[1][2] = a.lineto(b, color='green')
    
    a.unhilight(a_id)
    b.unhilight(b_id)
    a.remove_lineto(b, l_id)
    return d

# encontra as dimensoes (largura, altura) do retangulo que contem todos
# os pontos da coleção
def find_limits(pts):
    '''
    p: coleção de pontos
    '''
    
    min_x = max_x = pts[0].x
    min_y = max_y = pts[0].y
    for p in pts:
        x, y = p.x, p.y
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y

    return (max_x - min_x + EPS), (max_y - min_y + EPS)

# encontra o indice do quadrado em que o ponto se encontra
def index_square(p, delta):
    '''
    p: ponto
    delta: largura do quadrado
    '''
    r = math.ceil( p.x / (delta/2) )
    s = math.ceil( p.y / (delta/2) )
    return r, s

def Aleatorio(pts):

    # embaralhando os pontos
    shuffle(pts)

    if len(pts) < 2:
        return

    # melhor par encontrado ate agora, distancia entre eles e
    # id's da parte grafica
    best = [[None, None, float('inf')], [None, None, None]]

    # inicializando com dois primeiros pontos
    min_dist = update(pts[0], pts[1], best)
    delta_x, delta_y = find_limits(pts)
    # dicionario/hashtable
    h = {}

    # mais de um ponto na mesma posição
    if min_dist < EPS:
        closest = segment.Segment(best[0][0], best[0][1])
        closest.extra_info = 'Menor distancia: %.4f' %best[0][2]
        return closest

    # insere o ponto h na hashtable
    def update_hashtable(delta, p):
        r, s = index_square(p, delta)
        h[(r,s)] = p

    # constroi a hashtable de acorod com um delta e um indice
    # limite na lista de pontos, 
    def build_hashtable(delta, idx):
        h.clear()
        for i in range(idx+1):
            update_hashtable(delta, pts[i])
        return h

    build_hashtable(min_dist, 1)
    for i in range(2, len(pts)):
        pj = pts[i]
        r, s = index_square(pj, min_dist)
        new_dist = INF
        for t in range(-1, 2):
            for u in range(-1, 2):
                if (r+t, s+u) in h:
                    new_dist = update(pj, h[(r+t, s+u)], best)
        
        if new_dist + EPS < min_dist:
            min_dist = new_dist
            if min_dist < EPS: break
            build_hashtable(min_dist, i)
        else:
            update_hashtable(min_dist, pj)
        
    closest = segment.Segment(best[0][0], best[0][1])
    closest.extra_info = 'Menor distancia: %.4f' %best[0][2]
    return closest

