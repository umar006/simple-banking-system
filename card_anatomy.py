import random
import sys
import sqlite3
from display import *
from account import *
  

def main():    
    while True:
        conn = sqlite3.connect('card.s3db')

        has_table(conn)
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
                        deposit = balance_card(conn, card) + int(deposit)
                        
                        update_balance(conn, card, deposit)
                        
                        print('Income was added!\n')
                    elif choice == '3':
                        # Transfer money
                        receiver = input('\nTransfer\nEnter card number:\n')
                        
                        check = luhn_algorithm(receiver)
                        if check:
                            if is_exist(conn, receiver):
                                money = input('Enter how much money you want to transfer:\n')
                                
                                balance = balance_card(conn, card)
                                if int(money) < balance:
                                    transfer_money(conn, receiver, money)
                                    
                                    money_sender = balance_card(conn, card) - int(money)
                                    update_balance(conn, card, money_sender)
                                    print('Success!\n')
                                else:
                                    print('Not enough money!\n')
                            else:
                                print('Such a card does not exist.\n')
                        else:
                            print('Probably you made mistake in the card number. Please try again!\n')
                    elif choice == '4':
                        # Close account
                        close_account(conn, card)
                        print('\nThe account has been closed!\n')
                        break
                    elif choice == '5':
                        print('\nYou have successfully logged out!\n')
                        break
                    elif choice == '0':
                        close()
            else:
                print('Wrong card number or PIN!\n')
        elif choice == '0':
            close()


if __name__ == "__main__":
    main()