import mysql.connector  as m
from random import randint
mydb=m.connect(host='localhost ', user='root' ,password='Ajeet@123' ,database='bankdb')
cur=mydb.cursor()


def view_all_customer():
    cur.execute("select * from customer ")
    rec=cur.fetchall()
    for r in rec:
        print("account no:",r[0])
        print("customer name:",r[1])
        print("customer mobile:",r[2])
        print("customer email:",r[3])
        print("customer aadhar no:",r[4])
        print("customer address:",r[5])
        print("account type:",r[6])
        print("="*24)
        admin_service()


def search_customer():
    print('''1.search by name:
2.search by account no:''')

    ch=int(input("enter choice:"))
    if ch==1:
        n=input("enter name:")
        q="select *from customer where c_name=%s"
        #v=(n,)
        cur.execute(q,(n,))
        records=cur.fetchall()
        if records:

            print(records)
            admin_service()
        else:
            print("Name does not found")
            search_customer()

    elif ch==2:
        ac=int(input("enter account no:"))
        q="select *from customer where acc_no=%s"
        v=(ac,)
        cur.execute(q,v)
        rec=cur.fetchone()
        print(rec)
        admin_service()
        
def  total_bank_balance():
    print("1.particular customer:\n2.overall bank balance")
    ch=int(input("enter choice:"))
    if ch==1:
        ac=int(input("enter account no:"))
        q="select balance from customer where acc_no=%s"
        v=(ac,)
        cur.execute(q,v)
        rec=cur.fetchone()
        print("total balance is:",rec)
        admin_service()

    elif ch==2:
        cur.execute("select sum(balance) from customer")
        rec=cur.fetchone()
        print("total bank balance:",rec)
        admin_service()

def delete_customer_account():
    ac=int(input("enter account no to delete:"))
    q="delete from customer where acc_no=%s"
    v=(ac,)
    cur.execute(q,v)
    print("customer account deleted successfully:")
    mydb.commit()
    admin_service()

def total_customer():
    cur.execute("select count(*) from customer")
    rec=cur.fetchall()
    print(rec)
    admin_service()

def richest_customer():
    
    cur.execute("select max(balance) from customer")
    rec=cur.fetchone()
    cur.execute("select acc_no,c_name from customer")
    r=cur.fetchone()
    print("richest customer account no and name:",r,"balance is:",rec)
    admin_service()

def log_out():
    main()
    
def admin_login():
    un=input("enter username:")
    p=int(input("enter password:"))
    q="select * from admin where ad_username=%s and ad_pass=%s"
    cur.execute(q,(un,p))
    result=cur.fetchone()
    if result:

        print("login successfully")
        print("wlecome admin:",un)
        print("=" *8)
        admin_service()
        

    else:
        print("wrong username or password")
        print("=" *8)
        admin_login()
            
           
def admin_service():
    print('''1.view all customer
2.search customer
3.total bank balance
4.delete customer account
5.total customer
6.richest customer
7.logout''')
    
    ch=int(input("enter choice:"))

    if ch==1:
        view_all_customer()

    elif ch==2:
        search_customer()

    elif ch==3:
        total_bank_balance()

    elif ch==4:
        delete_customer_account()

    elif ch==5:
        total_customer()

    elif ch==6:
        richest_customer()

    elif ch==7:
        log_out()

def create_account():
    n=input("enter name:")
    e=input("enter email:")
    m=int(input("enter mobile no:"))
    ad=int(input("enter adhar no:"))
    ads=input("enter address:")
    act=input("enter account type:")
    d=int(input("enter initial deposit:"))
    p=int(input("create pin:"))

    ac=randint(1000,9999)
    q="insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    v=(ac,n,e,m,ad,ads,act,d,p)
    cur.execute(q,v)
    print("account created successfully")
    mydb.commit()
    customer_login()
    
def deposit_money():
    ac=int(input("enter account no:"))
    amt=int(input("enter amount:"))
    q="update customer set balance=balance+%s where acc_no=%s"
    v=(amt,ac)
    cur.execute(q,v)
    a=cur.fetchone()
    print("updated balance:",a)
    mydb.commit()
    transaction(ac,'deposite',amt)
    
    
def withdraw_money():
    ac=int(input("enter account no:"))
    p=int(input("enter pin:"))
    amt=int(input("enter amount:"))
    q="update customer set balance=balance - %s where acc_no=%s and c_pin=%s"
    v=(amt,ac,p)
    cur.execute(q,v)
    print("withdraw successfull")
    mydb.commit()
    transaction(ac,'withdral',amt)

    

def balance_enquiry():
    print('''1.view balance
2.account details
3.account type''')

    ch=int(input("enter choice:"))

    if ch==1:
        ac=int(input("enter account no:"))
        p=int(input("enter pin:"))
        q="select balance from customer where acc_no=%s and c_pin=%s"
        v=(ac,p)
        cur.execute(q,v)
        a=cur.fetchone()
        print("your balance is:",a)
        
    if ch==2:
        ac=int(input("enter account no:"))
        #p=int(input("enter pin:"))
        q="select c_name,c_mobile,c_email,c_aadhar,c_address,acc_type,balance,c_pin from customer where acc_no=%s"
        v=(ac,) 
        cur.execute(q,v)
        a=cur.fetchone()
        
        print("your account detail is:",a)     
        
    if ch==3:
        ac=int(input("enter account no:"))
        p=int(input("enter pin:"))

        q="select acc_type from customer where acc_no=%s and c_pin=%s"
        v=(ac,p)
        cur.execute(q,v)
        at=cur.fetchone()
        print("your account type is:",at)
        
def fund_transfer():
    from datetime import datetime
    d=datetime.now()
    sacc=int(input("enter sender account no:"))
    racc=int(input("enter receiver account no:"))
    amt=int(input("enter amount:"))
    q="update customer set balance=balance+%s where acc_no=%s "
    v=(amt,racc)
    cur.execute(q,v)
    mydb.commit()
    q="update customer set balance=balance-%s where acc_no=%s"
    v=(amt,sacc)
    cur.execute(q,v)
    a=cur.fetchone()
    print("transfer successfull")
    print("amount:",a)
    mydb.commit()
    q="insert into transf(send_acc_no,rec_acc_no,amount,transfer_date) values(%s,%s,%s,%s)"
    v=(sacc,racc,amt,d)
    cur.execute(q,v)
    mydb.commit()
    print("transfer successfull")
    
    
def transaction(ac,tt,amt):
    from datetime import datetime
    d=datetime.now()
    cur=mydb.cursor()
    q="insert into trans(acc_no,t_type,amount,t_date) values(%s,%s,%s,%s) "
    v=(ac,tt,amt,d)
    cur.execute(q,v)
    mydb.commit()
    print('transaction suceess!')


 
def update_account():
    print('''1.update mobile
2.update email
3.update address
4.change pin''')

    ch=int(input("enter choice:"))
    if ch==1:
        ac=int(input("enter account no:"))
        m=int(input("enter new mobile no:"))

        q="update customer set c_mobile=%s where acc_no=%s"
        v=(m,ac)
        cur.execute(q,v)
        print("mobile updated successfully")
        mydb.commit()
        
    if ch==2:
        ac=int(input("enter account no:"))
        e=int(input("enter new email :"))

        q="update customer set c_email=%s where acc_no=%s"
        v=(e,ac)
        cur.execute(q,v)
        print("email updated successfully")
        mydb.commit()
        
    if ch==3:
        ac=int(input("enter account no:"))
        ads=int(input("enter new address:"))

        q="update customer set c_address=%s where acc_no=%s"
        v=(ads,ac)
        cur.execute(q,v)
        print("address updated successfully")
        mydb.commit()

    if ch==4:
        ac=int(input("enter account no:"))
        p=int(input("enter new pin:"))

        q="update customer set c_pin=%s where acc_no=%s"
        v=(p,ac)
        cur.execute(q,v)
        print("pin updated successfully")
        mydb.commit()

def delete_account():
    
    ac=int(input("enter account no:"))
    p=int(input("enter pin:"))

    q="delete from customer where acc_no=%s and c_pin=%s"
    v=(ac,p)
    cur.execute(q,v)
    print("account close successfully")
    mydb.commit()

def log_out():
    main()
   
def customer_service():
    print('''1.deposit money
2.withdraw money
3.balance enquiry
4.fund transfer
5.transaction history
6.update account
7.delete account
8.logout''')

    ch=(int(input("enter choice:")))
        
    if ch==1:
        deposit_money()
        
    elif ch==2:
        withdraw_money()
        
    elif ch==3:
        balance_enquiry()
        
    elif ch==4:
        fund_transfer()
        
    elif ch==5:
        transaction()
        
    elif ch==6:
        update_account()
        
    elif ch==7:
        delete_account()
        
    elif ch==8:
        log_out()
        
def customer_login():
    print('''1.if you have an account and pin:login
2.if you have not any account:create account''')

    ch=int(input("enter choice:"))
    if ch==1:
        
        acc=int(input("enter account no:"))
        p=int(input("enter pin:"))
        q="select c_name from customer where acc_no=%s and c_pin=%s"
        cur.execute(q,(acc,p))
        result=cur.fetchone()
        if result:
            print("login successfull")
            print("welcome:",result[0])
            customer_service()
            print("=" *7)
        else:
            print("wrong account no or password")
            customer_login()
            print("=" *5)

    elif ch==2:
        create_account()

def main():
    
    print( "=" *7,"bank management system","=" *7)
    print('''1.admin login
2.customer login
3.exit''')
    
    ch=int(input("enter choice:"))
    
    if ch==1:
        admin_login()

    elif ch==2:
        customer_login()

    elif ch==3:
        exit 
    else:
        print("wrong choice:please enter under(1-3)")
        print("="*30)
        main()
        
main()

    
def show():
    print('hello')
show()
