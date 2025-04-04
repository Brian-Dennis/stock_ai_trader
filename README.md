# Terminal Snake Game

A classic Snake game implementation for the terminal with enhanced graphics and smooth gameplay.

## Game Features

- Terminal-based gameplay using Python's curses library
- Colorful graphics with Unicode characters
- Score tracking and display
- Game over screen with final score
- Restart functionality
- Graceful terminal resizing handling
- Fallback ASCII graphics for terminals without Unicode support

## Controls

- **Arrow Keys** or **WASD**: Control the snake's direction
  - ↑ or W: Move up
  - ↓ or S: Move down
  - ← or A: Move left
  - → or D: Move right
- **Q**: Quit the game
- **R**: Restart after game over

## Visual Improvements

- Different characters for snake head (⚪) and body (●)
- Red apple emoji (🍎) for food
- Box drawing characters (┌─┐│└┘) for borders
- Color scheme:
  - Green: Snake
  - Red: Food and Game Over message
  - Yellow: Score
  - White: Border
- ASCII fallbacks for terminals that don't support Unicode

## Requirements

- Python 3.x
- Terminal with curses support
- For best experience: a terminal that supports Unicode characters and colors

## How to Run the Game

1. Ensure Python 3 is installed on your system
2. Open a terminal
3. Navigate to the directory containing the game
4. Run the game using:

```bash
python3 snake_game.py
```

## Game Mechanics

- The snake grows longer each time it eats food
- Game ends if the snake hits the wall or itself
- Score increases by 10 points for each food item eaten
- Food will always spawn in valid positions (not on the snake or borders)
- The snake cannot immediately reverse direction (preventing accidental self-collision)

Enjoy playing!

