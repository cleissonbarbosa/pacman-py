# Pac-Man Python

Este projeto implementa uma versão do clássico Pac-Man utilizando Python e a biblioteca Pygame.

## Visão Geral

- **Jogo**: Controle o Pac-Man para coletar pontos e evitar fantasmas.
- **Fases**: O jogo consiste em um labirinto onde você deve coletar todos os pontos e power pellets para vencer.
- **Fantasmas**: Quatro fantasmas com comportamentos simples patrulham o labirinto. Quando Pac-Man coleta um power pellet, os fantasmas ficam assustados e podem ser comidos.

## Imagens do Jogo

https://github.com/user-attachments/assets/9a2c5738-874a-4b65-a3ba-b39d994d772b

![Durante o Jogo](/assets/1.2025-02-24%2020-44-59.png)

## Como Jogar

1. **Instalação**: 
   - Certifique-se de ter o Python instalado.
   - Instale o Pygame com o comando: `pip install pygame`

2. **Executar o Jogo**:
   - Navegue até a pasta do projeto e execute:
     ```bash
     python src/main.py
     ```

3. **Controles**:
   - Use as setas do teclado para movimentar o Pac-Man.
   - Quando o jogo acabar (vitória ou derrota), pressione a tecla R para reiniciar.

## Estrutura do Projeto

```
pacman-py/
├── src/
│   ├── game.py         # Lógica principal do jogo
│   ├── ghost.py        # Comportamento dos fantasmas
│   ├── main.py         # Ponto de entrada do jogo
│   ├── maze.py         # Criação e desenho do labirinto e pontos
│   ├── player.py       # Lógica do Pac-Man
│   └── settings.py     # Configurações do jogo (cores, velocidade, etc.)
└── README.md           # Este arquivo de documentação
```

## Desenvolvimento

- **Refatoração**: A lógica principal foi separada da função `main()` para a classe `Game` em `game.py`, melhorando a organização do código.
- **Modularização**: Cada aspecto do jogo (jogador, fantasmas, labirinto) está em seu próprio módulo para facilitar manutenção e expansão.

## Contribuindo

Fique à vontade para contribuir com melhorias, correções e novas funcionalidades.

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Envie suas alterações com commit (`git commit -m 'Adiciona nova funcionalidade'`)
4. Envie um pull request

## Licença

Este projeto é open-source e livre para uso. Veja o arquivo LICENSE para mais detalhes.
