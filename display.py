import sys


def main_display():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def main_menu():
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')


def print_new_account(card, pin):
    print('\nYour card has been created')
    print(f'{card}')
    print('Your card PIN:')
    print(f'{pin}\n')
    
    
def close():
    print('\nBye!\n')
    sys.exit()