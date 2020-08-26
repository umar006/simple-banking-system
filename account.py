import random


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

    return card, pin


def close_account(conn, card):
    cur = conn.cursor()
    cur.execute('DELETE FROM card WHERE number=?', (card,))
    conn.commit()
    
    
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


def has_table(conn):
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
    cur.execute('SELECT balance FROM card WHERE number=?', (card,))

    return cur.fetchone()[0]


def update_balance(conn, card, money):
    cur = conn.cursor()
    cur.execute('''
                UPDATE card
                SET balance=?
                WHERE number=?''', (money, card))
    conn.commit()
    
    
def transfer_money(conn, receiver, money):
    balance = balance_card(conn, receiver) + int(money)
    
    cur = conn.cursor()
    cur.execute('''
                UPDATE card
                SET balance=?
                WHERE number=?''', (str(balance), receiver))
    conn.commit()
    
    
def is_exist(conn, receiver):
    cur = conn.cursor()
    cur.execute('SELECT number FROM card WHERE number=?', (receiver,))
    
    return cur.fetchone()    # return 1 / 0