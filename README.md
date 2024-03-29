# Pychess - jogo de xadrez feito a partir do módulo pygame

--------------------------------------------------------------------------------------------------------------------------
### Sobre o projeto

O apliativo foi criado incialmente como trabalho final da disciplina de programação orientada a objetos 2, da Universidade Federal de Santa Catarina. 

A lógica de jogo implementada foi baseada no projeto "Chess Engine in Python", de Eddie Sharick.

O conteúdo do projeto de Eddie está disponível em:
https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick .

--------------------------------------------------------------------------------------------------------------------------
### Configurações necessárias

Para o fucnionamento correto do programa, é necessária a instalação da biblioteca "Pygame", e para instalar tal biblioteca, é necessário possuir o pacote Pip, que é o sistema gerenciador de pacotes python.

Para instalar o Pip: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/

Para instalar o Pygame: https://www.geeksforgeeks.org/how-to-install-pygame-in-windows/

Além da instalação destes pacotes, é necessária a alteração de um valor no código. Nas linhas 139 e 181 do arquivo main é preciso identificar o caminho da pasta 'saves' do programa. A identificação precisa ser do tipo r'caminho', como por exemplo r'E:\Users\user\Desktop\chess\saves'.

--------------------------------------------------------------------------------------------------------------------------
### Modo de uso

O programa possui dois tipos de inicialização, normal e sandbox. 

No modo normal, o jogo funciona como um jogo de xadrez padrão, com os turno de jogada estipulados (brancas e pretas) e com todas as regras de movimentação das peças.

No modo sandbox, não há limitação de turnos, ambas as peças pretas e brancas podem se movimentar a qualquer momento e também não há lógica de movimentação das peças, sendo possível a realização de qualquer movimento.

A lógica de cheque e chque mate ainda não foi implementada, então é possível realizar alguns movimentos inválidos no modo de jogo normal em situações onde o rei está ameaçado.

--------------------------------------------------------------------------------------------------------------------------
