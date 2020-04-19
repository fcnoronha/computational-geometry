'''
    By Felipe Noronha
    IME USP - 2020
'''

from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config

# para realizar a ordenação dos pontos
from functools import cmp_to_key

# função comparadora usada para ordenar os pontos ─ x primeiro, checa
# (a.x < b.x) or ((a.x == b.x) and (a.y < b.y))
def compare_x(a, b):
    if a[0] < b[0]:
        return -1
    elif a[0] > b[0]:
        return 1
    elif a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0

# função comparadora usada para ordenar os pontos ─ y primeiro, checa
# (a.y < b.y) or ((a.y == b.y) and (a.x < b.x))
def compare_y(a, b):
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0

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

# implementação do algoritmo de divisão e conquista para achar o pair de pontos
# mais proximos. A função abaixo é apenas um envolucro para as chamadas 
# recursivas.
def Divide_conquer(pts):

    # ordenando os pontos recebidos, O(nlogn) (leia mais no relatorio)
    pts = sorted(pts, key=cmp_to_key(compare_x))

    # melhor par encontrado ate agora, distancia entre eles e
    # id's da parte grafica
    best = [[None, None, float('inf')], [None, None, None]]

    distancia_rec_sh(pts, 0, len(pts), best)

    if best[0][2] == float('inf'):
        return

    ret = segment.Segment(best[0][0], best[0][1])
    ret.extra_info = 'Menor distancia: %.4f' %best[0][2]
    return ret

# função que realiza a recursão da divisão e conquista
def distancia_rec_sh(pts, l, r, best):
    '''
    pts: array de pontos
    l: limite esquerdo da recursão
    r: limite direito da recursão
    best: melhores pontos encontrados
    '''

    # força bruta / base da recursão
    if r-l <= 3:
        for i in range(l, r):
            for j in range(i+1, r):
                update(pts[i], pts[j], best)
        pts[l:r] = sorted(pts[l:r], key=cmp_to_key(compare_y))
        return
    
    m = int((l+r)/2)
    m_point = pts[m]
    m_line = control.plot_vert_line(m_point[0], color='red')
    
    # divisão
    distancia_rec_sh(pts, l, m, best)
    distancia_rec_sh(pts, m, r, best)
    intercala(pts, l, m, r)
    
    # conquista
    control.plot_delete(m_line)
    m_line = control.plot_vert_line(m_point[0], color='yellow')
    combine(pts, l, r, m_point, best)
    control.plot_delete(m_line)

# implementação da função intercala do mergesort, que junta dois vetores ordenados em 
# tempo linear
def intercala(pts, l, m, r):
    '''
    pts: array de pontos
    l: limite esquerdo da recursão
    m: ponto de divisão da recursão
    r: limite direito da recursão
    '''
    
    aux = []
    i, j = l, m
    while i < m and j < r: 
        if compare_y(pts[i], pts[j]) <= 0: 
            aux.append(pts[i]) 
            i += 1
        else: 
            aux.append(pts[j]) 
            j += 1
    aux = aux + pts[i:m] + pts[j:r]
    for i in range(l, r):
        pts[i] = aux[i-l]

# função que percorre a faixa do meio e compara os pontos que estão a uma distancia do 
# meio menor que a menor distancia encontrada até agora
def combine(pts, l, r, m_point, best):
    '''
    pts: array de pontos
    l: limite esquerdo da recursão
    r: limite direito da recursão
    m_point: ponto da divisão da recursão
    best: melhores pontos encontrados
    '''

    candidates = []
    for i in range(l, r):
        if m_point.distance_to(pts[i]) < best[0][2]:
            control.sleep()
            j = len(candidates)-1
            while j >= 0 and pts[i].distance_to(candidates[j]) < best[0][2]:
                update(pts[i], candidates[j], best)
                j -= 1
            candidates.append(pts[i])
