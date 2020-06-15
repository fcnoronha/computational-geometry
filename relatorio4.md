# Geometria computacional - Projeto 4

## Algoritmos de Jarvis e Graham
## Convex hull 2D

### Felipe Castro de Noronha | 10737032

---

Neste quarto projeto implementei o algoritmo de Jarvis e o algoritmo de Graham, ambos buscam encontrar o **convex hull** (fecho convexo) de um conjunto de pontos no plano.

Utilizando a plataforma oferecida, criei os novos algoritmos dentro do _problema_ `convex_hull`, as implementação se encontram em `geocomp/convex_hull/jarvis.py` e `geocomp/convex_hull/graham.py`. Utilizando a interface gráfica, basta executar `python3 tkgeocomp.py` no terminal, após isso, clique em _Fecho convexo_, selecione um conjunto de pontos a ser utilizado e clique em _Graham_ ou _Jarvis_ para executar o algoritmo desejado.

O algoritmo de Jarvis tem complexidade de tempo definida por _O(nh)_, ou seja, seu consumo de tempo é proporcional ao produto do numero de pontos no plano e ao numero de pontos no convex hull final.

O algoritmo de Graham tem complexidade de tempo definida por _O(nlogn)_, isto é, seu consumo de tempo é linear-logaritmicamente ao numero de pontos no conjunto.

Em relação a animação, temos as seguintes decisões:

- As retas em pontos em **amarelo** definem o convex hull definido até o momento;
- As retas em **azul** definem os triângulos (teste esquerda) que estão sendo realizados a partir de um ponto.
