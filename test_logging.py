from logging import getLogger
import MyLogger


print('Test init')
MyLogger.start()
my_log = getLogger(__name__)
print('\nPrinted message #1')
my_log.error('Logged message #1')

MyLogger.start()
my_log = getLogger(__name__)
print('\nPrinted message #2')
my_log.error('Logged message #2')

print('\nTest end - There should be 2 logged messages')
