@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Building the game executable...
python -m PyInstaller --onefile --windowed --name "SpaceShooter" space_shooter_game.py

echo Build complete! The executable is in the 'dist' folder.
echo You can run SpaceShooter.exe from the dist folder.
pause
