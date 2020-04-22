'''
    By Felipe Noronha
    IME USP - 2020
'''

from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import point
from geocomp.common import control
from geocomp import config
from .rbtree import RBTree

# Macros usadas para tipo do evento
START = 0
END = 1
INTERSECTION = 2
VERTICAL = 3

# Algumas macros para ajudar nas comparações
EPS = 10**-9
INF = float("inf")

# Funções auxiliares
def cmp_e(sweep_line, a, b):
    '''
    Comparador para entre eventos da linha de varredura. Mantem a ordem na 
    arvore binaria que representa a lista de eventos.
    '''
    # São o mesmo segmento
    if a == b: return 0

    # Pontos de interseção com a reta l
    current_x = sweep_line.current_x
    a_y = a.y_intersection(current_x)
    b_y = b.y_intersection(current_x)
    if a_y is None: a_y = a.point[1]
    if b_y is None: b_y = b.point[1]

    # Caso esteja de acordo com a precisão, a comparação toma como base o
    # ponto de intersecção de cada segmento com a reta l do line sweep
    if abs(a_y-b_y) > EPS:
        if a_y < b_y: return -1
        else: return 1

    # Caso os coeficientes de inclinação sejam diferentes, desempatamos 
    # com eles, levando em considerção se ja processamos ou não a 
    # interseção entre essas retas
    a_slope = a.a_cof
    b_slope = b.a_cof
    if a_slope != b_slope:
        if sweep_line.before_flag:
            if a_slope > b_slope: return -1
            else:                 return 1
        else:
            if a_slope < b_slope: return -1
            else:                 return 1

    # Ultimo desempate se da com a reta que começa ou termina antes
    if (a.segment[0][0], a.segment[1][0]) < (b.segment[0][0], b.segment[1][0]): 
        return -1
    elif (a.segment[0][0], a.segment[1][0]) > (b.segment[0][0], b.segment[1][0]):
        return 1
    return 0
    
def segment_intersection(s, t):
    '''
    Checa a interseção dos eventos s e t. Se a mesma não existe, retorna
    None, caso contrario retorna o ponto p
    '''
    s_seg = s.segment
    t_seg = t.segment
    if s_seg == None or t_seg == None: return None

    # Checa se é colinear 
    if left_test(s_seg[0], s_seg[1], t_seg[0]) == 0: return t_seg[0]
    if left_test(s_seg[0], s_seg[1], t_seg[1]) == 0: return t_seg[1]
    if left_test(t_seg[0], t_seg[1], s_seg[0]) == 0: return s_seg[0]
    if left_test(t_seg[0], t_seg[1], s_seg[1]) == 0: return s_seg[1]

    # Checa se segmentos não se intersectam
    if left_test(s_seg[0], s_seg[1], t_seg[0]) == left_test(s_seg[0], s_seg[1], t_seg[1]): 
        return None
    if left_test(t_seg[0], t_seg[1], s_seg[0]) == left_test(t_seg[0], t_seg[1], s_seg[1]): 
        return None

    # Se algum dos dois for vertical, aqui, não temos mais interseção
    if s.is_vertical or t.is_vertical: return None

    # Agora sabemos que elas se intersectam e vamos achar o ponto. Para isso 
    # vamos igualar as equações de reta da forma 'y = ax + b'
    a1 = s.a_cof
    b1 = s.b_cof
    a2 = t.a_cof
    b2 = t.b_cof
        
    x = (b2-b1)/(a1-a2)
    y = a1*x + b1
    return (x, y)

def left_test(s1, s2, p):
    '''
    Teste para saber se o ponto p esta a esquerda so segmento s1-s2.
    Retorna 1 se o ponto esta a esquerda, -1 se o ponto esta a direita, 
    0 caso seja colinear
    '''
    val = (s2[1]-s1[1])*(p[0]-s2[0]) - (s2[0]-s1[0])*(p[1]-s2[1])
    if (val < 0): return 1
    if (val > 0): return -1
    return 0

class Event:
    '''
    Classe usada para representar eventos do line sweep. Podemos ter os 
    seguintes tipos:

    START: marca o inicio de um segmento, o mesmo deve ser colocado na arvore
    END: marca o fim de um segmento, o mesmo deve ser retirado da arvore
    INTERSECTION: marca uma intersecação entre segmentos
    VERTICAL: marca a ocorrencia de um segmento vertical
    '''
    def __init__(self, t, p, s):
        '''
        Metodo construtor de um evento.
        '''
        self.type = t
        self.point = p
        self.segment = s

        if s != None:
            x1, y1 = s[0][0], s[0][1]
            x2, y2 = s[1][0], s[1][1]
            self.is_vertical = (x1-x2 == 0.0)
            # Coeficientes da reta ax + b = y
            if not self.is_vertical:
                self.a_cof = (y1-y2)/(x1-x2)
                self.b_cof = y1 - self.a_cof*x1
            else:
                if y1 < y2: self.a_cof = INF
                else:       self.a_cof = -INF

    def __hash__(self):
        '''
        Definindo um hash para o evento, baseado no ponto.
        '''
        return hash(self.point)

    def y_intersection(self, x):
        '''
        Dado um ponto x, retorna a y-coordenada do ponto (x, y), tal que 
        o mesmo pertence ao segmento. Se x esta fora dos limites do segmento,
        retorna o y mais proximo
        '''
        if x <= self.segment[0][0]: return self.segment[0][1]
        elif x >= self.segment[1][0]: return self.segment[1][1]

        a = self.a_cof
        b = self.b_cof
        y = a*x + b
        return y

class SweepLine:
    '''
    Classe que implementa a linha de varruda. Contem todas as principais 
    funções executadas para a execução do algoritmo e é responsavel por manter
    as estruturas de dados que fazem possivel o funcionamento do algoritmo.
    '''
    def __init__(self, bag):
        '''
        Metodo construtor da linha de varredura.

        - intersections: dicionario que mapeia pontos de interseção para uma
        lista que contem todas as retas participantes;
        - current_x: guarda a posição em que a linha de varredura esta;
        - events_list: lista de eventos, ABBB;
        - bag: bag ordenas dos eventos que vão ser processados;
        - before_flag: flag usada na comparação para manutenção de ordem quando
        estamos na iminencia de processar uma interseção.
        '''
        self.intersections = {}
        self.current_x = None 
        self.events_list = RBTree(cmp=cmp_e, cmp_data=self) 
        self.bag = bag 
        self.before_flag = True 

    def get_intersections(self):
        '''
        Retorna lista com pontos de interseção, nossa resposta.
        '''
        inter_points = []
        for i in self.intersections: inter_points.append(i)
        return inter_points

    def insert(self, event):
        '''
        Insere um evento na lista de eventos.
        '''
        self.events_list.insert(event, None)

    def remove(self, event):
        '''
        Remove um evento da lista de eventos.
        '''
        if not event in self.events_list: return False
        self.events_list.remove(event)
        return True

    def above(self, event):
        '''
        Recebe um evento do tipo segmento e retorna o segmento acima dele na
        lista de eventos.
        '''
        return self.events_list.succ_key(event, None)

    def below(self, event):
        '''
        Recebe um evento do tipo segmento e retorna o segmento abaixo dele na
        lista de eventos.
        '''
        return self.events_list.prev_key(event, None)

    def all_above(self, event):
        '''
        Recebe um evento do tipo segmento e retorna todos os seguimetos acima
        dele na lista de eventos.
        '''
        return self.events_list.key_slice(event, None, reverse=False)

    def process_intersection(self, a, b):
        '''
        Usada para processar a interseção entre dois eventos. 
        '''
        if a == None or b == None or a == b: return 
        if a.type == INTERSECTION or b.type == INTERSECTION: return

        a_line = a.segment.plot(cor='blue')
        b_line = b.segment.plot(cor='blue')
        control.sleep()
        control.plot_delete(a_line)
        control.plot_delete(b_line)

        # Ponto de interseção            
        p = segment_intersection(a, b)
        if p == None: return
        # Ponto ja foi processado, adiciono possiveis novos segmentos a inter
        if p in self.intersections: 
            self.intersections[p].add(a)
            self.intersections[p].add(b)
            return 

        p_plot = point.Point(p[0], p[1])
        p_plot.plot('white')

        # Cria conjunto com os segmentos que compõem aquela interseção
        self.intersections[p] = {a, b}
        # Adiciono a interseção na fila de eventos se ela esta a direita
        if p[0] >= self.current_x:
            new_event = Event(INTERSECTION, p, None)
            self.bag.insert(p, new_event)

    def process_event(self, event):
        '''
        Processa um evento.
        '''
        e_type = event.type
        if e_type == START:
            self.before_flag = False
            self.insert(event)
            e_above = self.above(event)
            e_below = self.below(event)
            self.process_intersection(event, e_above)
            self.process_intersection(event, e_below)

        if e_type == END:
            self.before_flag = True
            e_above = self.above(event)
            e_below = self.below(event)
            self.remove(event)
            self.process_intersection(e_above, e_below)

        if e_type == INTERSECTION:
            self.before_flag = True
            # Segmentos que participam da interseção
            segments_set = self.intersections[event.point]
            # Segmentos que devem ser recolocados na lista de eventos
            to_go_back = []
            for e in segments_set:
                if self.remove(e): 
                    to_go_back.append(e)

            p_plot = point.Point(event.point[0], event.point[1])
            p_plot.plot('green', 5)
            control.sleep()

            self.before_flag = False
            for e in reversed(to_go_back):
                self.insert(e)
                e_above = self.above(e)
                e_below = self.below(e)
                self.process_intersection(e, e_above)
                self.process_intersection(e, e_below)

        if e_type == VERTICAL:
            y_high = event.segment[1][1]
            for e_above in self.all_above(event):
                y_above = e_above.y_intersection(self.current_x)
                if y_above == None: continue
                if y_above > y_high: break
                self.process_intersection(event, e_above)

class EventBag:  
    '''
    Classe que funciona como uma bag de eventos, porem, essa bag esta em ordem.
    Assim, ela nos fornece, em ordem, o proximo evento que devera ser
    precessado pela linha de varredura.
    '''
    def __init__(self, segments):
        '''
        Recebe os segmentos e um objeto do tipo sweep line e cria/popula a 
        lista de eventos com os segmentos passados.
        '''
        self.event_bag = RBTree()
        for s in segments:
            if s[0][0] == s[1][0]:
                e_start = Event(VERTICAL, s[0], s)
                self.insert(s[0], e_start)
            else:
                e_start = Event(START, s[0], s)
                e_end   = Event(END, s[1], s)
                self.insert(s[0], e_start)
                self.insert(s[1], e_end)

    def insert(self, p, e):
        '''
        Adiciona o evento 'e' a chave 'p' na bag de eventos, criando o 
        respectivo valor caso ele ainda não exista.
        Aqui, cada chave 'p' pode corresponder a mais de um evento, por isso
        criamos uma tupla com 4 posições para cada ponto 'p', cada posição dessa
        tupla é uma lista que contem todos os eventos daquele certo tipo. 
        '''
        tp = (p[0],p[1])
        e_get = self.event_bag.get(tp, False)
        if not e_get:
            new_e = ([], [], [], [])
            self.event_bag.insert(tp, new_e)
            e_get = self.event_bag.get(tp)

        e_get[e.type].append(e) 

    def next_events(self):
        '''
        Retorna o proximo ponto a ser retirado da bag, isto é, a proxima tupla
        de eventos a ser processada.
        '''
        p, events_current = self.event_bag.pop_min()
        return p, events_current

def Bent_ott (segments):
    '''
    Rotina principal de execução do algoritmo de Bentley and Ottmman.
    '''
    # Ordenando os pontos do segmento
    for s in segments:
        if s[0] > s[1]:
            s.to, s.init = s.init, s.to
        s.plot()
    
    bag = EventBag(segments)
    sweep_line = SweepLine(bag)
    line = None
    while not bag.event_bag.is_empty():
        p, e_tuple = bag.next_events()
        # Andando com a linha de varredura
        if line: control.plot_delete(line)
        sweep_line.current_x = p[0]
        line = control.plot_vert_line(p[0], color='yellow')
        control.sleep()
        # Processando cada tupla de eventos do mesmo tipo
        for t in [END, INTERSECTION, START, VERTICAL]:
            for e in e_tuple[t]: 
                sweep_line.process_event(e)

    intersections = sweep_line.get_intersections()
    print("Numero de interseções: " + str(len(intersections)))