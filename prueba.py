import random

time_to_sleep = 60*3+(random.randint(1*100, 10*100)/100)
minutes = time_to_sleep / 60
print(f'sleeping {time_to_sleep} secs ({minutes:.1f} mins)...')
