# Space Shooter Game 🚀

An exciting space shooter game built with Python and Pygame!

## Features

- **Smooth gameplay** with 60 FPS
- **Multiple enemy types** including bosses
- **Power-ups** (health restoration, rapid fire)
- **Particle effects** for explosions and damage
- **Progressive difficulty** with waves
- **Beautiful graphics** with animated stars background
- **Health bars** for player and enemies
- **Score system** with different point values for enemies

## Controls

- **WASD** or **Arrow Keys**: Move your ship
- **SPACE**: Shoot
- **ESC**: Pause/Resume game
- **R**: Restart (when game over)
- **Q**: Quit (when game over)

## How to Play

1. **Survive the waves** of incoming enemies
2. **Collect power-ups** to restore health or improve your shooting
3. **Defeat different enemy types**:
   - Red squares: Basic enemies (10 points)
   - Purple circles: Stronger enemies that shoot back (25 points)
   - Orange bosses: Tough enemies with lots of health (100 points)
4. **Each wave gets harder** with more enemies
5. **Don't let your health reach zero!**

## Installation & Running

### Option 1: Run from Source
```bash
pip install -r requirements.txt
python space_shooter_game.py
```

### Option 2: Build Executable
```bash
# Run the build script
build_game.bat

# Or manually:
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "SpaceShooter" space_shooter_game.py
```

The executable will be created in the `dist` folder as `SpaceShooter.exe`.

## Game Mechanics

- **Health System**: Start with 100 health, lose health from enemy contact or bullets
- **Scoring**: Earn points by destroying enemies
- **Waves**: Complete waves by destroying all enemies
- **Power-ups**: 10% chance to drop from destroyed enemies
- **Collision Detection**: Precise collision detection for all game objects
- **Visual Effects**: Particle explosions and smooth animations

## Technical Details

- Built with **Python 3.x** and **Pygame**
- **Object-oriented design** with separate classes for game entities
- **Efficient collision detection** and game loop
- **Compiled to standalone .exe** using PyInstaller

Enjoy the game! 🎮
