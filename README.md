# Pac-Man Python

This project implements a version of the classic Pac-Man using Python and the Pygame library.

## Overview

- **Game**: Control Pac-Man to collect dots and avoid ghosts.
- **Levels**: The game takes place in a maze where you must collect all the dots and power pellets to win.
- **Ghosts**: Four ghosts with simple behaviors patrol the maze. When Pac-Man collects a power pellet, the ghosts become scared and can be eaten.

## Game Images

https://github.com/user-attachments/assets/9a2c5738-874a-4b65-a3ba-b39d994d772b

![In Game](/assets/1.2025-02-24%2020-44-59.png)

## How to Play

1. **Installation**:
   - Make sure you have Python installed.
   - Install Pygame using the command: `pip install pygame`

2. **Run the Game**:
   - Navigate to the project folder and run:
     ```bash
     python src/main.py
     ```

3. **Controls**:
   - Use the arrow keys to move Pac-Man.
   - When the game is over (win or lose), press the R key to restart.

## Project Structure

```
pacman-py/
├── src/
│   ├── game.py         # Main game logic
│   ├── ghost.py        # Ghost behavior
│   ├── main.py         # Game entry point
│   ├── maze.py         # Maze creation and dot drawing
│   ├── player.py       # Pac-Man logic
│   └── settings.py     # Game settings (colors, speed, etc.)
└── README.md           # This documentation file
```

## Contributing

Feel free to contribute improvements, fixes, and new features.

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Adds new feature'`)
4. Submit a pull request

## License

This project is open-source and free to use. See the LICENSE file for more details.
