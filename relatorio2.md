# Geometria computacional - projeto 2

## Algoritmo de Bentley e Ottmman
## Line sweep para encontrar interseção de segmentos

### Felipe Castro de Noronha | 10737032

---

Neste segundo projeto, implementei o [algoritmo de Bentley e Ottmman](https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm) que, usando uma linha de verredura, encotra todas as _k_ interseções de _n_ segmentos em tempo proporcional a _O((n+k)lgn)_.

Utilizando a plataforma oferecida, criei um novo algoritmo dentro do _problema_ `lineintersections`, tal implementação se encontra em `geocomp/lineintersections/bent_ott.py`. Utilizando a interface grafica, basta executar `python3 tkgeocomp.py` no terminal, após isso, clique em _Interseções de segmentos_, selecione um conjunto de segmentos a ser utilizado e clique em _Bentley and Ottmman_ para executar minha implementação.

Gostaria de fazer duas importantissimas ressalvas sobre minha implementação:

- Tive muita dificuldade em implementar uma função comparadora que me permitisse manter uma ordem relativa dos seguimentos na minha ABBB, logo, busquei inspiração [nesta implementação](https://github.com/ideasman42/isect_segments-bentley_ottmann) pois, acho que tal implementação é muito elegante e enchuta. Com isso, consegui fazer com que minha implementação fosse muito legivel e ao mesmo tempo perfomatica.
- Usando a mesma adaptção proposta pela implementação citada, utilizei a [RBTree da biblioteca Pypi](https://pypi.org/project/bintrees/) que pode ter sua [implementação encontrada aqui](https://github.com/mozman/bintrees). Essa foi a minha escolha de arvore de busca binaria balanceada, e para ter a comparação necessaria temos a adaptação dela em `geocomp/lineintersections/rbtree.py`.

Em relação a animação, temos as seguintes decisões:

- A linha de varredura _l_ é representada por uma linha vertical amarela.
- Dois segmentos ficam azuis quando se esta checando se ha interseção entre os mesmos.
- Um ponto de interseção é marcado em branco quando o mesmo é colocado na lista de eventos.
- Um ponto de interseção é marcado em verde quando o mesmo é processado pela linha de varredura.

Finalmente, notei que no exemplo _segments2.txt__a contagem de interseções impressa esta incorreta. Isso se deve ao erro de precisão de pontos gerados. Não consegui achar uma maneira satisfatoria de corrigir tal problema, dado que a minha abordagem de truncar o ponto flutuante afetava fortemente a contagem de interseções no exemplo _segments1.txt_.
