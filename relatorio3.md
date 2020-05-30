# Geometria computacional - Projeto 3

## Algoritmo aleatorizado 
## Par de pontos mais próximos em tempo linear

### Felipe Castro de Noronha | 10737032

---

Neste terceiro projeto, implementei um algoritmo probabilístico/aleatório, que encontra o par de pontos mais próximos em tempo proporcional a _O(n)_.

Utilizando a plataforma oferecida, criei um novo algoritmo dentro do _problema_ `closest`, tal implementação se encontra em `geocomp/closest/aleatorio.py`. Utilizando a interface gráfica, basta executar `python3 tkgeocomp.py` no terminal, após isso, clique em _Par mais proximo_, selecione um conjunto de pontos a ser utilizado e clique em _Aleatorizado_ para executar minha implementação.

Em relação a animação, temos as seguintes decisões:

- As retas em **azul** representam o _grid_ de quadrados gerados com tamanho _delta/2_;
- As retas e  pontos em **verde** são os pontos mais próximos até o momento;
- O ponto em **amarelo** é o ponto sendo inserido na atual iteração do algoritmo;
- O quadrado em **amarelo** é o quadrado com distancia de no máximo 2 do ponto da iteração atual;
- A linha em **ciano** é o teste entre o ponto da iteração e o ponto do quadrado checado.