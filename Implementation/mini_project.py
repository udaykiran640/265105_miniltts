import sqlite3
conn = sqlite3.connect('project.db')
c = conn.cursor()
#c.execute("""CREATE TABLE usertable (name text, mail text, mobile text PRIMARY KEY, password text)""")
#c.execute("""CREATE TABLE accounttable (accoun_balace int, mobile text)""")
"""remove the comments in above two lines if you execute without project.db file and comment the same
two lines once you execute the mini_project.py"""
conn.commit()
conn.close()

def SignUp():
    name     = input("Enter Name \n")
    gmail    = input("Enter Mail \n")
    mobile   = input("Enter Mobile \n")
    password = input("Enter Password \n")
    amount   = 1000
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    c.execute('INSERT INTO usertable VALUES (?,?,?,?)', (name, gmail, mobile, password))
    c.execute('INSERT INTO accounttable VALUES (?,?)', (amount, mobile))
    conn.commit()
    #data = c.execute('SELECT * FROM usertable')
    #print(data.fetchall())
    conn.close()
    return "success"


def Login():
    mobile    = input("\n Enter mobile \n")
    password = input("Enter password \n")
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    d = c.execute('SELECT password from usertable where mobile = ? ', (mobile,))
    pass_data = d.fetchall()
    conn.close()
    #print(pass_data)
    if pass_data :
        for i in pass_data:
            if password == i[0]:
                return 'success', mobile
            else:
                print("wrong password")
                return 'failed', 'False'
    else:
        print("Entered invalid mobile")
        return 'failed', 'False'


def Transfer(mobile):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    d = c.execute('SELECT name from usertable where mobile = ? ', (mobile,))
    v = d.fetchall()
    name = ""
    for i in v:
        name = i[0]
    print("welcome", name)
    value = int(
        input("\n Enter 0 to Check balace \n Enter 1 to Tranfer money \n Enter 2 to Add money \n Enter 3 to Exit \n"))
    # screen_clear()
    cnt = 0
    if value == 0:
        b_data = c.execute('SELECT accoun_balace from accounttable where mobile = ? ', (mobile,))
        bal_data = b_data.fetchall()
        conn.close()
        if bal_data:
            for i in bal_data:
                balance = i[0]
        print("\n" + name+"," + " " +"Your balance is INR " + str(balance) + "\n")

        Transfer(mobile)

    elif value == 1:
        sender_mobile = input("Enter receiver mobile \n")
        data = c.execute('SELECT * from usertable where mobile = ? ', (sender_mobile,))
        if data.fetchall():
            send_money = int(input("Enter amount to transfer \n"))
            b_data = c.execute('SELECT accoun_balace from accounttable where mobile = ? ', (mobile,))
            bal_data = b_data.fetchall()

            if bal_data:
                for i in bal_data:
                    balance1 = int(i[0])
            if balance1 > send_money:
                balance1 = balance1 - send_money
                c.execute('''UPDATE accounttable SET accoun_balace = ? WHERE mobile = ?''', (balance1, mobile))
                conn.commit()
                rec_data = c.execute('SELECT * from accounttable where mobile = ? ', (sender_mobile,))
                nbal = rec_data.fetchall()
                for i in nbal:
                    r_balance = int(i[0])
                r_balance = r_balance + send_money
                c.execute('''UPDATE accounttable SET accoun_balace = ? WHERE mobile = ?''', (r_balance, sender_mobile))
                conn.commit()
                print("Money transfered\n")
                Transfer(mobile)
            else:
                print("Insufficient balance\n")

                Transfer(mobile)
        else:
            print("Invalid receiver\n")

            Transfer(mobile)
    elif value == 2:
        add_money = int(input("Enter amount to add \n"))
        rec_data = c.execute('SELECT * from accounttable where mobile = ? ', (mobile,))
        old_bal = rec_data.fetchall()
        for i in old_bal:
            o_balance = int(i[0])
        o_balance = o_balance + add_money
        print("Money added successfully\n")
        c.execute('''UPDATE accounttable SET accoun_balace = ? WHERE mobile = ?''', (o_balance, mobile))
        conn.commit()

        Transfer(mobile)
    elif value == 3:
        return 0
    else:
        print("Enter valid value")

        Transfer(mobile)


def start():
    value = int(input("Enter 0 to signup or 1 to login \n"))
    if value == 0:
        val = SignUp()
        if val == 'success':
            print("Account created, please login")
            val1,mobile = Login()
            if val1 == 'success':
                Transfer(mobile)
            elif val1 == 'failed':
                print("Invalid login")
                start()
        else:
            print("Signin failed")
    elif value == 1:
        val1, mobile = Login()
        if val1 == 'success':
            Transfer(mobile)
        elif val1 == 'failed':
            print("Invalid login")
            start()

start()


