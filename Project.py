import mysql.connector as db
con = db.connect(user='root',password='Rushi@123',host='localhost',database='bank')
cur=con.cursor()

#======================= ACCOUNT CREATION ===========================
class CreateAccount:
    def create(self):
        print('*' * 7,'REGISTERATION FOR ACCOUNT CREATION','*' * 7)
        details=[]
        
        #Account Number
        import random    
        while True:
            rand=random.randint(100000,999999)
            bank_code=str(3000)
            Account_no = bank_code + str(rand)
            cur.execute('select Account_No from users where Account_No =%s',(Account_no,))
            data=cur.fetchone()
            if data is None:
                details.append(int(Account_no))
                break
            else:
                continue
            
        #Account Holders Name
        while True:
            name = input('Full Name :')
            if all(part.isalpha() for part in name.split()) and len(name) > 3:
                details.append(name)
                break
            else:
                print('You Have entered invalid name')
                continue

        #Account Type
        while True:
            accounts=['SAVINGS','CURRENT','CREDIT']
            Account_type=input('Account Type(SAVINGS/CURRENT/CREDIT):')
            if Account_type in accounts:
                details.append(Account_type)
                break
            else:
                print("Please select a valid Account type")
                continue

        #Account Balance
        while True:
            
            Account_Balance = int(input('Deposite Amount (Min=2k) :'))
            if Account_Balance >= 2000:
                details.append(Account_Balance)
                break
            else:
                print("The minimum amount must be deposited 2000")
                continue

        #Phone Number
        import re 
        while True:
            ph_no=int(input('Phone Number :'))
            pattern='[6-9]{1}[0-9]{9}'
            cur.execute('select Phone_Number from users where Phone_Number=%s',(ph_no,))
            data=cur.fetchone()
            if re.fullmatch(pattern,str(ph_no)) and data is None :
                details.append(ph_no)
                break
            else:
                print("Invalid Phone Number ")
                continue

        #Email_Id
        import re
        while True:
            mail=input('Email Id :')
            pattern=r'^[a-z0-9]+@[a-z0-9]+\.com$'
            cur.execute('select Email_ID from users where Email_ID=%s',(mail,))
            data=cur.fetchone()
            if re.match(pattern,mail) and data is None:
                details.append(mail)
                break
            else:
                print('Your Email is Invalid / This Mail is Already Exists')
                continue

        #Pin Creation
        while True:
            pin=int(input('Set Pin :'))
            if len(str(pin))==4 and str(pin).isdigit():
                details.append(pin)
                break
            else:
                print('Your Pin must contain 4 Digits only')
                continue

        cur.execute('insert into users values(%s,%s,%s,%s,%s,%s,%s)',details)
        con.commit()
        print('Account Created Sucessfully')

        return details

cur.close()
con.close()



#=========================== USER LOGIN MODE =============================
import mysql.connector as db
con = db.connect(user='root',password='Rushi@123',host='localhost',database='bank')
cur=con.cursor()

class UserLogin:
    def login(self):
        print("\n********** USER LOGIN ***********")
        acc_no = int(input("Enter Account Number :"))
        pin = int(input("Enter Your 4-digits Pin :"))
        cur.execute('select * from users where Account_No=%s and UserPin=%s',(acc_no,pin))
        data = cur .fetchone()

        if data :
            print(f"WELCOME  {data[1]}")
            self.menu(acc_no)
        else:
            print("Invalid Account number or pin !")

    def menu(self,acc_no):
        while True:
            print("""
-------------------
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Change Pin
5. View Statement
6. Exit
-------------------
""")
            choice = int(input("Enter choice to proceed :"))
            if choice == 1:
                amt=int(input("Enter the amount to Deposit :"))
                if amt > 100:
                    cur.execute('update users set Account_Balance = Account_Balance + %s where Account_no=%s',(amt,acc_no))
                    con.commit()
                    print("Amount Deposite Sucessfull")
                else:
                    print("Please Deposit Valid Amount (Min=100)")

            elif choice ==2:
                amt = int(input('Enter the Amount to Withdraw :'))
                cur.execute('select Account_Balance from users where Account_No =%s',(acc_no,))
                balance=cur.fetchone()[0]
                if balance >= amt:
                    cur.execute('update users set Account_Balance = Account_Balance - %s where Account_no =%s',(amt,acc_no))
                    con.commit()
                    print("Amount Withdrawn Successfully")
                else:
                    print("Insufficient Balance")

            elif choice == 3:
                cur.execute('select Account_Balance from users where Account_no=%s',(acc_no,))
                balance= cur.fetchone()[0]
                print(f"Current Balance Avaliable :{balance}")

            elif choice == 4:
                self.change_pin(acc_no)

            elif choice == 5:
                self.view_statement(acc_no)

            elif choice == 6:
                print("Thank You for Banking with us!")
                break
            

            else:
                print("Invalid Choice")

    def change_pin(self, acc_no):
        old_pin = int(input("Enter Old PIN: "))
        cur.execute('select UserPin from users where Account_No=%s', (acc_no,))
        current_pin = cur.fetchone()[0]
        if old_pin == current_pin:
            new_pin = int(input("Enter New 4-Digit PIN: "))
            if len(str(new_pin)) == 4:
                cur.execute('update users set UserPin=%s where Account_No=%s', (new_pin, acc_no))
                cur.execute('insert into transactions(Account_No, Transaction_Type, Amount) values(%s,%s,%s)', (acc_no, 'PIN Change', 0))
                con.commit()
                print("PIN Changed Successfully!")
            else:
                print("PIN must be 4 digits only.")
        else:
            print("Old PIN Incorrect!")

    # ======== VIEW STATEMENT =========
    def view_statement(self, acc_no):
        print("\n---- ACCOUNT STATEMENT ----")
        cur.execute('select Transaction_Type, Amount, Date from transactions where Account_No=%s order by Date desc', (acc_no,))
        data = cur.fetchall()
        if data:
            for d in data:
                print(f"Type: {d[0]} | Amount: ₹{d[1]} | Date: {d[2]}")
        else:
            print("No transactions found.")

#============== ADMIN LOGIN MODULE ================
class Admin:
    def __init__(self):
        self.admin_id = 'Rushi'
        self.password = 'Admin@01'

    def login(self):
        print('\n--- ADMIN LOGIN ---')
        user = input('Enter Admin ID: ')
        pwd = input('Enter Password: ')
        if user == self.admin_id and pwd == self.password:
            print('Admin Login Successful!\n')
            self.menu()
        else:
            print('Invalid Admin Credentials.')

    def menu(self):
        while True:
            print("""
1. View All Users
2. View Account Details by Account No
3. View Transactions by Account No
4. View Transactions by Date
5. Logout
""")
            ch = input('Enter Choice: ')
            if ch == '1':
                self.view_all_users()
            elif ch == '2':
                self.view_account_details()
            elif ch == '3':
                self.view_transactions_user()
            elif ch == '4':
                self.view_transactions_date()
            elif ch == '5':
                print('Logging out Admin...')
                break
            else:
                print('Invalid choice!')

    def view_all_users(self):
        cur.execute('SELECT Account_No, Account_Holder, Account_Type, Account_Balance FROM users')
        data = cur.fetchall()
        print('\n--- All Users ---')
        for d in data:
            print(f"Account No: {d[0]} | Name: {d[1]} | Type: {d[2]} | Balance: ₹{d[3]}")

    def view_account_details(self):
        acc = input('Enter Account Number: ')
        cur.execute('SELECT * FROM users WHERE Account_No=%s', (acc,))
        data = cur.fetchone()
        if data:
            print(f"\nAccount No: {data[0]}\nName: {data[1]}\nType: {data[2]}\nBalance: ₹{data[3]}\nPhone: {data[4]}\nEmail: {data[5]}")
        else:
            print(' Account not found.')

    def view_transactions_user(self):
        acc = input('Enter Account Number: ')
        cur.execute('SELECT * FROM transactions WHERE Account_No=%s', (acc,))
        data = cur.fetchall()
        print('\n------- Transactions --------')
        for d in data:
            print(f"Type: {d[2]} | Amount: ₹{d[3]} | Date: {d[4]}")

    def view_transactions_date(self):
        date = input('Enter Date (YYYY-MM-DD): ')
        cur.execute('SELECT * FROM transactions WHERE DATE(Date)=%s', (date,))
        data = cur.fetchall()
        if data:
            print('\n--- Transactions on that Date ---')
            for d in data:
                print(f"Account No: {d[1]} | Type: {d[2]} | Amount: ₹{d[3]} | Date: {d[4]}")
        else:
            print('No transactions found on that date.')


# ------------------ MAIN MENU ------------------
def main_menu():
    while True:
        print("""
========== BANK MANAGEMENT SYSTEM ==========
1. Create New Account
2. User Login
3. Admin Login
4. Exit
""")
        ch = input('Enter Choice: ')
        if ch == '1':
            CreateAccount().create()
        elif ch == '2':
            UserLogin().login()
        elif ch == '3':
            Admin().login()
        elif ch == '4':
            print('Thank you for using the Bank Management System!')
            break
        else:
            print('Invalid option. Try again.')

main_menu()

cur.close()
con.close()






















