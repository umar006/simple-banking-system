import random
import sys
import sqlite3


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


def luhn_algorithm(card):
    ori = list(card)
    last_digit = int(ori.pop())

    # Convert str to int
    ori = [i for i in map(int, ori)]

    # if i-th digit is odd (even index) multiply by 2
    multy = [ori[i] if(i % 2 == 1) else ori[i] * 2 for i in range(len(ori))]
    subtract = [i - 9 if(i > 9) else i for i in multy]
    subtract.append(last_digit)
    add = sum(subtract)

    return add % 10 == 0


def create_account(conn):
    card = ''
    pin = ''

    check = True
    while check:
        IIN = '400000'  # Issuer Identification Number (IIN)
        account_number = random.randrange(1e10)  # Customer Account Number

        card = IIN + str(account_number).zfill(10)
        pin = str(random.randrange(10e3)).zfill(4)

        check = not luhn_algorithm(card)

    cur = conn.cursor()
    cur.execute('''
    INSERT INTO card (number, pin) VALUES (?,?)
    ''', (card, pin))
    conn.commit()

    cur.execute('select * from card')
    print(cur.fetchall())

    return card, pin


def close():
    print('\nBye!\n')
    sys.exit()


def hasTable(conn):
    cur = conn.cursor()

    cur.execute(
        '''
    CREATE TABLE IF NOT EXISTS card(
        id          INTEGER             PRIMARY KEY,
        number      varchar(20),
        pin         varchar(20),
        balance     INTEGER             DEFAULT 0
    );
    ''')
    conn.commit()


def sql_fetch(conn, card, pin):
    cur = conn.cursor()

    cur.execute('''
            SELECT number, pin
            FROM card
            WHERE number=? AND pin=?;
        ''', (card, pin))

    return cur.fetchone()

def balance_card(conn, card):
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number=?', card)

    return cur.fetchone()


def add_money(conn, card, money):
    cur = conn.cursor()
    cur.execute('''
                UPDATE card
                SET balance=?
                WHERE card=?''', (card, money))
    conn.commit()
    
    
def transer_money(conn, receiver):
    cur = conn.cursor()
    cur.execute()


while True:
    conn = sqlite3.connect('card.s3db')

    hasTable(conn)
    main_display()

    choice = input()
    if choice == '1':
        new_card, new_pin = create_account(conn)
        # print card and pin
        print_new_account(new_card, new_pin)
    elif choice == '2':

        print('')
        card = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        print('')

        # get account
        if (card, pin) == sql_fetch(conn, card, pin):
            print('You have successfully logged in!\n')

            while True:
                main_menu()

                choice = input()
                if choice == '1':
                    # Check balance
                    balance = balance_card(conn, card)
                    print(f"\nBalance: {balance}\n")
                elif choice == '2':
                    # Deposit money
                    deposit = input('\nEnter income:\n')
                    add_money(conn, card, deposit)
                    
                    print('Income was added!')
                elif choice == '3':
                    # Transfer money
                    receiver = input('Transfer\nEnter card number:\n')
                    transer_money(conn, receiver)
                    
                    print('\nYou have successfully logged out!\n')
                elif choice == '4':
                    # Delete account
                    print('\nYou have successfully logged out!\n')
                elif choice == '5':
                    print('\nYou have successfully logged out!\n')
                    break
                elif choice == '0':
                    close()
        else:
            print('Wrong card number or PIN!\n')
    elif choice == '0':
        close()
