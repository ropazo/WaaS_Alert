import os
import sys

my_path = os.path.dirname(sys.argv[0])
print(f'my_path = {my_path}')
os.chdir(my_path)

