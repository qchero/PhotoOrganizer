import os

os.chdir("[library_dir]")
os.system("python -m cProfile -s cumtime [code_dir]/photo_organizer.py setup")
