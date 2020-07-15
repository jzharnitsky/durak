# Python program to print 
# red text with green background 
  
from colorama import Fore, Back, Style 
print(Fore.RED + 'some red text') 
print(Back.GREEN + 'and with a green background') 
print(Style.DIM + 'and in dim text') 
print(Style.RESET_ALL) 
print('back to normal now')

from colorama import init
from termcolor import colored

init()
print(colored('Hello, World!', 'green', 'on_red'))
