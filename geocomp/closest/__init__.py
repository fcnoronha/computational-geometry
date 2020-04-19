# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Proximo:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles seja minima

Algoritmos disponveis:
- Forca bruta
- Divide and conquer
"""
from . import brute
from . import divide_conquer

children = [
	[ 'brute', 'Brute', 'Forca Bruta' ],
	[ 'divide_conquer', 'Divide_conquer', 'Divisao e conquista' ]
]

__all__ = [a[0] for a in children]
