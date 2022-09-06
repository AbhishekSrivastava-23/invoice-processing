#Beginning of program

#Importing modules
import mysql.connector
from math import floor, ceil

#Establishing connection
connect = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234', database = 'INVOICES')
cursor = connect.cursor()

#Function definitions

def spacing(invoice): #For arranging data in form of table
    print(' ', '-'*16, '-'*26, '-'*26, '-'*12, '-'*25, '', sep = '+')
    print('', 'INVOICE NUMBER', '     CUSTOMER NAME      ', '        ADDRESS         ', '   DATE   ', '     INVOICE TOTAL     ', '', sep = ' | ')
    print(' ', '-'*16, '-'*26, '-'*26, '-'*12, '-'*25, '', sep = '+')
    for c in invoice:
        print('', ' '*floor(7-len(str(c[0]))/2) + str(c[0]) + ' '*ceil(7-len(str(c[0]))/2), ' '*floor(12-len(c[1])/2) + c[1] + ' '*ceil(12-len(c[1])/2), ' '*floor(12-len(c[2])/2) + c[2] + ' '*ceil(12-len(c[2])/2), str(c[3]), ' '*floor(11.5-len(str(c[4]))/2) + str(c[4]) + ' '*ceil(11.5-len(str(c[4]))/2), '', sep = ' | ')
    print(' ', '-'*16, '-'*26, '-'*26, '-'*12, '-'*25, '', sep = '+')
    
def date_input(): #Taking date from user
    d = input('Enter date(DD): ')
    while int(d) < 1 or int(d) > 31: 
        print('Invalid date. Enter again')
        d = input('Enter date(DD): ')
    m = input('Enter month number(MM): ')
    while int(m) < 1 or int(m) > 12:
        print('Invalid month. Enter again')
        m = input('Enter month number(MM): ')
    y = input('Enter year(YYYY): ')
    if len(d) != 2:
        d = '0' + d[0]
    if len(m) != 2:
        m = '0' + m[0]
    while len(y) != 4 or int(y) < 1000:
        print('Invalid year. Enter again')
        y = input('Enter correct year(YYYY): ')
    req_date = y + '-' + m + '-' +d
    return req_date

def display(invoice): #Displaying particular customer
    if len(invoice) == 0:
        print('\nNo matching record found')
    else:
        spacing(invoice)
        
def invoice_display(no): #Displaying invoice
    cursor.execute('SELECT * FROM INVOICE_%s' %(no,))
    invoice = cursor.fetchall()
    cursor.execute('SELECT * FROM INVOICES_LIST WHERE INVOICE_NO = %s' %(no,))
    display = cursor.fetchall()
    display = display[0]
    date = display[3]
    name = display[1]
    address = display[2]
    total = display[4]
    print('\nInvoice date  : ', date)
    print('Invoice number: ', no)
    print('\nCustomer name: ', name, '\tAddress: ', address, '\n')
    print(' ', '-'*26, '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
    print('', ' '*10 + 'ITEM' + ' '*10, ' QUANTITY  ', '     RATE/ITEM(Rs)     ', 'TAX%', '     TAX VALUE(Rs)     ', '       TOTAL(Rs)       ', '', sep = ' | ')
    print(' ', '-'*26, '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
    for i in invoice:
        print('', ' '*floor(12-len((i[0]))/2) + i[0] + ' '*ceil(12-len((i[0]))/2), ' '*floor(5.5-len(str(i[1]))/2) + str(i[1]) + ' '*ceil(5.5-len(str(i[1]))/2), ' '*floor(11.5-len(str(i[2]))/2) + str(i[2]) + ' '*ceil(11.5-len(str(i[2]))/2), str(i[3]) + ' '*(4-len(str(i[3]))), ' '*floor(11.5-len(str(i[4]))/2) + str(i[4]) + ' '*ceil(11.5-len(str(i[4]))/2), ' '*floor(11.5-len(str(i[5]))/2) + str(i[5]) + ' '*ceil(11.5-len(str(i[5]))/2), '', sep = ' | ')
    print(' ', '-'*26, '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
    print('\nINVOICE TOTAL: Rs', total, '\n')
    print('DELHIVERY EXPRESS CORPORATION, Tamil Nadu\n')
    
def all(): #Displaying all customers
    cursor.execute('SELECT * FROM INVOICES_LIST')
    invoice = cursor.fetchall()
    if len(invoice) == 0:
        print('No existing record')
    else:
        spacing(invoice)
        
def date(): #Displaying customers by date
    given_date = date_input()
    cursor.execute("SELECT * FROM INVOICES_LIST WHERE DATE = '%s'" %(given_date,))
    invoice = cursor.fetchall()
    display(invoice)
    
def total(): #Displaying customers by total
    lower = float(input('Enter lower limit of total(Rs): '))
    upper = float(input('Enter upper limit of total(Rs): '))
    while lower > upper:
        print('Wrong limits. Enter again')
        lower = float(input('Enter lower limit of total(Rs): '))
        upper = float(input('Enter upper limit of total(Rs): '))
    while lower < 0 or lower > 99999999999999999999999:
        print('Wrong or too large lower limit. Enter again')
        lower = float(input('Enter lower limit of total(Rs): '))
    while upper < 0 or upper > 99999999999999999999999:
        print('Wrong or too large upper limit. Enter again')
        upper = float(input('Enter upper limit of total(Rs): '))
    cursor.execute('SELECT * FROM INVOICES_LIST WHERE INVOICE_TOTAL BETWEEN %s AND %s' %(lower, upper))
    invoice = cursor.fetchall()
    display(invoice)
    
def invoice_by_no(): #Displaying invoice by no.
    no = int(input('Enter invoice no. whose invoice is to be displayed: '))
    cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
    invoices = cursor.fetchall()
    if (no,) not in invoices:
        print('\nInvoice does not exist.')
    else:
        invoice_display(no)
        
def all_invoices(): #Displaying all invoices
    cursor.execute('SELECT * FROM INVOICES_LIST')
    invoices_list = cursor.fetchall()
    if len(invoices_list) == 0:
        print('No existing invoice')
    for i in invoices_list:
        invoice_display(i[0])
        print()
        
def new_items(no): #Entering new items in invoice
    while True:
        item = input('Enter item name: ').capitalize()
        if len(item) > 24:
            item = item[:24]
        quantity = int(input('Enter quantity: '))
        while quantity > 999999999:
            print('Quantity too large. 999999999 is being taken')
            quantity = input('If you want to change, enter new quantity. Else, press enter: ')
            if len(quantity) == 0:
                quantity = 999999999
            else:
                quantity = int(quantity)
        rate = float(input('Enter rate/item(Rs): '))
        rate = round(rate,2)
        tax = input('Enter tax %, if applicable. If not, press enter: ')
        if len(tax) == 0:
            tax = 0
        while float(tax) < 0 or float(tax) > 100:
            print('Invalid Tax%. Enter again')
            tax = input('Enter tax %, if applicable. If not, press enter: ')
        tax = round(float(tax), 1)
        tax_value = rate*quantity*tax/100
        total = rate*quantity + tax_value
        total = round(total, 2)
        cursor.execute("INSERT INTO INVOICE_%s VALUES('%s', %s, %s, %s, %s, %s)" %(no, item, quantity, rate, tax, tax_value, total))
        more = ''
        more = input('Do you want to enter more items? If not, press Enter: ')
        if len(more) == 0 or more[0].upper() != 'Y':
            break
    cursor.execute('SELECT SUM(TOTAL) FROM INVOICE_%s' %(no,))
    total = cursor.fetchall()
    total = total[0][0]
    total = round(total,2)
    return total

def new(): #Making new invoice
    date = date_input()
    no = int(input('Enter invoice no.: '))
    cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
    invoices = cursor.fetchall()
    while (no,) in invoices:
        print('Invoice already exists. Use another invoice number')
        no = int(input('Enter invoice no.: '))
    while len(str(no)) > 11:
        print('Invoice no. too large!')
        no = int(input('Please enter smaller: '))
    global name
    name = input('Enter customer name: ').title()
    if len(name) > 24:
        name = name[:24]
    address = input('Enter customer address: ').title()
    if len(address) > 24:
        address = address[:24]
    cursor.execute('CREATE TABLE INVOICE_%s (ITEM VARCHAR(24), QUANTITY INT, RATE FLOAT, TAX FLOAT, TAX_VALUE FLOAT, TOTAL FLOAT)' %(no,))
    sum_total = new_items(no)
    cursor.execute("INSERT INTO INVOICES_LIST VALUES(%s, '%s', '%s', '%s', %s)" %(no, name, address, date, sum_total))
    connect.commit()
    invoice_display(no)
    
def edit_invoice(): #Editing invoice
    no = int(input('Enter invoice no. whose invoice is to be edited: '))
    cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
    invoices = cursor.fetchall()
    if (no,) not in invoices:
        print('Invoice does not exist.')
    else:
        print('\nCURRENT INVOICE:')
        invoice_display(no)
        print('What do you want to edit?')
        print('1 Date')
        print('2 Customer name')
        print('3 Customer address')
        print('4 Delete item')
        print('5 Enter new items')
        print('6 Edit item')
        choice3 = int(input('Enter choice: 1/2/3/4/5/6: '))
        print()
        if choice3 == 1: #Editing date
            date = date_input()
            cursor.execute("UPDATE INVOICES_LIST SET DATE = '%s' WHERE INVOICE_NO = %s" %(date,no))
        elif choice3 == 2: #Editing customer name
            name = input('Enter customer name: ').title()
            if len(name) > 24:
                name = name[:24]
            cursor.execute("UPDATE INVOICES_LIST SET CUSTOMER_NAME = '%s' WHERE INVOICE_NO = %s" %(name,no))
        elif choice3 == 3: #Editing customer address
            address = input('Enter customer address: ').title()
            if len(address) > 24:
                address = address[:24]
            cursor.execute("UPDATE INVOICES_LIST SET ADDRESS = '%s' WHERE INVOICE_NO = %s" %(address,no))
        elif choice3 == 4: #Deleting item
            item = input('Enter name of item to be deleted: ').capitalize()
            cursor.execute('SELECT ITEM FROM INVOICE_%s' %(no,))
            items = cursor.fetchall()
            while (item,) not in items:
                print('Item does not exist. Enter again')
                item = input('Enter name of item to be deleted: ').capitalize()
            cursor.execute("DELETE FROM INVOICE_%s WHERE ITEM = '%s'" %(no, item))
            cursor.execute('SELECT SUM(TOTAL) FROM INVOICE_%s' %(no,))
            total = cursor.fetchall()
            total = total[0][0]
            cursor.execute('UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s' %(total, no))
        elif choice3 == 5: #Entering new item
            sum_total = new_items(no)
            cursor.execute('UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s' %(sum_total, no))
        elif choice3 == 6: #Editing item
            item = input("Which item's details do you want to change?: ").capitalize()
            cursor.execute('SELECT ITEM FROM INVOICE_%s' %(no,))
            items = cursor.fetchall()
            while (item,) not in items:
                print('Item does not exist. Enter again')
                item = input("Which item's details do you want to change?: ").capitalize()
            print('\nCURRENT DETAILS')
            cursor.execute("SELECT * FROM INVOICE_%s WHERE ITEM = '%s'" %(no, item))
            invoice = cursor.fetchall()
            print(' ', '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
            print('', ' QUANTITY  ', '     RATE/ITEM(Rs)     ', 'TAX%', '     TAX VALUE(Rs)     ', '       TOTAL(Rs)       ', '', sep = ' | ')
            print(' ', '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
            for i in invoice:
                quantity = i[1]
                rate = i[2]
                tax = i[3]
                print('', ' '*floor(5.5-len(str(i[1]))/2) + str(i[1]) + ' '*ceil(5.5-len(str(i[1]))/2), ' '*floor(11.5-len(str(i[2]))/2) + str(i[2]) + ' '*ceil(11.5-len(str(i[2]))/2), str(i[3]) + ' '*(4-len(str(i[3]))), ' '*floor(11.5-len(str(i[4]))/2) + str(i[4]) + ' '*ceil(11.5-len(str(i[4]))/2), ' '*floor(11.5-len(str(i[5]))/2) + str(i[5]) + ' '*ceil(11.5-len(str(i[5]))/2), '', sep = ' | ')
            print(' ', '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
            print('What do you want to change?')
            print('1 Item Name')
            print('2 Quantity')
            print('3 Rate/Item')
            print('4 Tax%')
            choice4 = int(input('Enter choice: 1/2/3/4: '))
            print()
            if choice4 == 1: #Changing item name
                new_item = input('Enter new item name: ')
                if len(new_item) > 24:
                    new_item = new_item[:24]
                cursor.execute("UPDATE INVOICE_%s SET ITEM = '%s' WHERE ITEM = '%s'" %(no, new_item, item))
            elif choice4 == 2: #Changing quantity
                quantity = int(input('Enter new quantity: '))
                while quantity > 999999999:
                    print('Quantity too large. 999999999 is being taken')
                    quantity = input('If you want to change, enter new quantity. Else, press enter: ')
                    if len(quantity) == 0:
                        quantity = 999999999
                    else:
                        quantity = int(quantity)
                tax_value = rate*quantity*tax/100
                total = rate*quantity + tax_value
                total = round(total, 2)
                cursor.execute("UPDATE INVOICE_%s SET QUANTITY = %s, TOTAL = %s WHERE ITEM = '%s'" %(no, quantity, total, item))
            elif choice4 == 3: #Changing rate/item
                rate = float(input('Enter new rate/item(Rs): '))
                tax_value = rate*quantity*tax/100
                total = rate*quantity + tax_value
                total = round(total, 2)
                cursor.execute("UPDATE INVOICE_%s SET RATE = %s, TOTAL = %s WHERE ITEM = '%s'" %(no, rate, total, item))
            elif choice4 == 4: #Changing tax%
                tax = input('Enter new tax %, if applicable. If not, press enter: ')
                if len(tax) == 0:
                    tax = 0
                while float(tax) < 0 or float(tax) > 100:
                    print('Invalid Tax%. Enter again')
                    tax = input('Enter tax %, if applicable. If not, press enter: ')                
                tax = round(float(tax), 1)
                tax_value = rate*quantity*tax/100
                total = rate*quantity + tax_value
                cursor.execute("UPDATE INVOICE_%s SET TAX = %s, TAX_VALUE = %s, TOTAL = %s WHERE ITEM = '%s'" %(no, tax, tax_value,total, item))
            else:
                print('Wrong input')
            cursor.execute('SELECT SUM(TOTAL) FROM INVOICE_%s' %(no,))
            total = cursor.fetchall()
            total = total[0][0]
            cursor.execute('UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s' %(total,no))
        else:
            print('Wrong input')
        if 0 < choice3 < 6 or (choice3 == 6 and 0 < choice4 < 5):
            connect.commit()
            print('\nINVOICE UPDATED')
            invoice_display(no)
            
def delete(): #Deleting invoice
    no = int(input('Enter invoice number, whose invoice is to be deleted: '))
    cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
    invoices = cursor.fetchall()
    if (no,) not in invoices:
        print('Invoice does not exist.')
    else:
        cursor.execute('DROP TABLE INVOICE_%s' %(no,))
        cursor.execute('DELETE FROM INVOICES_LIST WHERE INVOICE_NO = %s' %(no,))
        connect.commit()
        print('INVOICE DELETED')
        
#Main program

print('WELCOME!')
print('DELHIVERY EXPRESS CORPORATION')
print('GSTIN: 33AAICM7545C1ZK')
print('State: Tamil Nadu')
print('PAN  : AAICM7545C')
while True:
    print('\nWhat do you want to do?')
    print('1 DISPLAY DATA')
    print('2 EDIT DATA')
    print('3 EXIT\n')
    choice1 = int(input('Enter choice: 1/2/3: '))
    if choice1 == 1:
        print('1 Display all customers')
        print('2 Display customers who ordered on given date')
        print('3 Display customers whose invoice total is between given range')
        print('4 Display the invoice of a customer')
        print('5 Display all invoices')
        print('6 Exit to main menu\n')
        choice2 = int(input('Enter choice: 1/2/3/4/5/6: '))
        if choice2 != 6:
            print()
        if choice2 == 1:
            all()
        elif choice2 == 2:
            date()
        elif choice2 == 3:
            total()
        elif choice2 == 4:
            invoice_by_no()
        elif choice2 == 5:
            all_invoices()
        elif choice2 == 6:
            pass
        else:
            print('Wrong input')
    elif choice1 == 2:
        print('1 Make new  invoice')
        print('2 Edit existing invoice')
        print('3 Delete existing invoice')
        print('4 Exit to main menu\n')
        choice2 = int(input('Enter choice: 1/2/3/4: '))
        if choice2 != 4:
            print()
        if choice2 == 1:
            new()
        elif choice2 == 2:
            edit_invoice()
        elif choice2 == 3:
            delete()
        elif choice2 == 4:
            pass
        else:
            print('Wrong input')
    elif choice1 == 3:
        print('THANK YOU!')
        break
    else:
        print('Wrong input')
#End of program
