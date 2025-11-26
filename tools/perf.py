import os

os.chdir("E:/OneDrive/Photo Library")
os.system("python -m cProfile -s cumtime E:/Code/PhotoOrganizer/photo_organizer.py setup")
