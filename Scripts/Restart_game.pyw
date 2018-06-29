import os
import sys
import time

time.sleep(2)
# Defining this projects path
project_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))
os.system("start {}\\main_game.py".format(project_path))


