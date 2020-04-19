# Geometria computacional - projeto 1

## Algoritmo de divisão e conquista para par de pontos mais proximos

### Felipe Castro de Noronha | 10737032

---

Neste primeiro projeto, implementei o algoritmo de divisão e conquista para achar o par de pontos mais proximos. Utilizando a plataforma oferecida, criei um novo algoritmo dentro do _problema_ `closest`, tal implementação se encontra em `geocomp/closest/divide_conquer.py`. Utilizando a interface grafica, basta executar `python3 tkgeocomp.py` no terminal, após isso, clique em _Par mais proximo_, selecione um conjunto de pontos a ser utilizado e clique em _Divisão e conquista_ para executar minha implementação.

Para ordenar os pontos recebidos, usamos a função _built-in_ `sorted` do Python 3, que implementa o [algoritmo Timsort](https://en.wikipedia.org/wiki/Timsort). Tal algoritmo, no pior caso, tem complexidade O(nlogn). Alem disso, criei os comparadores `compare_x` e `compare_y` que tornam possivel a ordenação dos pontos pelo eixo X e pelo eixo Y, repectivamente.

Em relação a _implementação bonita_ vista em aula, fiz duas coisas diferentes:

- Ao inves de fazer com que as chamadas recursivas `distancia_rec_sh()` retornassem a menor distancia atinginda até agora, fiz com que as chamadas alterassem a lista `best`, que armazena os pontos mais proximos e a respectiva distancia;
- Na função `combine()` criamos uma lista com os pontos dentro da faixa. Tal lista é substituta do vetor `f` e é criada conforme vamos subindo no eixo vertical.

No restante da implementação, não temos nada de muito diferente da implementação visto em aula ─ a não ser, claro, as mudanças devido ao porte de pseudocodigo para python 3. A função `distancia_rec_sh` é a recursão em si, aqui temos a **divisão**, e, na base, realizamos o metodo de força bruta. A função `intercala` realiza o _merge_ de duas partes da lista que ja estão ordenadas pelo eixo Y. A função `combine` gera a faixa e a percorre, realizando a faze de **conquista**. Por ultimo, temos a função auxiliar `update`, que atualiza _best_ de acordo.

Em relação a parte grafica, as seguintes ações ocorrem:

- O par de pontos verdes, ligados por uma linha verde, é o par de pontos mais proximos encontrados até agora pelo algoritmo;
- Uma linha vertical vermelha é colocada em cada chamada da recursão, representa a posição no eixo X do ponto intermediario do intervalo _[l, r(_
- Um par de pontos azul, ligados por uma linha azul, é um par de pontos que esta sendo testado no momento;
- Quando um dado nivel da recursão esta na faze _combine_, a linha intermediaria fica amarela, ou seja, isso significa que estamos olhando a faixa.

Finalmente, para testar a corretude de meu algoritmo, executei os exemplos disponiveis em `dados/LOOSE_PTS` e comparei os resultados obtidos com aqueles obtidos no algoritmo de força bruta, e, em todos os exemplos, meu algoritmo achou o par mais proximo.
