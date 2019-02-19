#import random method for choose pnr
from random import randint
#import pymysql for database
import pymysql
#database connection
db =pymysql.connect('localhost','root','pri@mnit', 'mysql')

cursor=db.cursor()
#create table
'''cursor.execute('DROP TABLE IF EXISTS ticket')
#create database table
sql="""CREATE TABLE ticket (
pnr int,
route varchar(50),
name varchar(50),
age varchar(50),
gender varchar(8),
contact varchar(50),
date varchar(50),
seat varchar(50),
fare varchar(50),
time varchar(50)
)"""

cursor.execute(sql)
db.commit()'''




#method for check source
def check_source(object1):
    if (object1 in stations):
        return
    else:
        print('We do not have service in this city.')
        exit()

#method for check destination
def check_dest_city(object2):
    if(object2 in stations):
        return
    else:
        print('We do not have service in this city.')
        exit()

print('\t\t*****Welcome to RSRTC Bus Service*****')
#list of stations
stations = ['BIKANER','KOTA','JAIPUR','CHURU','BHILWARA']
#fare chart for route
fare_chart={'BIKANER to KOTA':400,'BIKANER to JAIPUR':400,'BIKANER to CHURU':400,'BIKANER to BHILWARA':400,
            'KOTA to BIKANER':500,'KOTA to JAIPUR':500,'KOTA to CHURU':500,'KOTA to BHILWARA':500,
            'JAIPUR to BIKANER':350,'JAIPUR to KOTA':350,'JAIPUR to CHURU':350,'JAIPUR to BHILWARA':350,
            'CHURU to BIKANER':450,'CHURU to KOTA':450,'CHURU to JAIPUR':450,'CHURU to BHILWARA':450,
            'BHILWARA to BIKANER':600,'BHILWARA to KOTA':600,'BHILWARA to JAIPUR':600,'BHILWARA to CHURU':600}
#departure time
Bus_timing={'BIKANER':6.00,'KOTA':6.15,'JAIPUR':7.00,'CHURU':8.00,'BHILWARA':10.00}
#available seat in bus
seat = 50

#function for search bus
def search_bus():
    print('\n*****')
    print('\nWe Have Bus Service for these Cities :')
    for i in stations:
        print(i)
    #enter source city
    source = input('\nFrom: ')
    source=source.upper()
    check_source(source)
    #enter destination city
    destination = input('\nTo: ')
    destination=destination.upper()
    check_dest_city(destination)
    journey_route = source+' to '+destination
    #function for print bus details
    def Bus_details():
        print('\nBus Details for your route is: ')
        print('From: \t',source,'\t\tTo: \t',destination)
        print('Departure Time is: ',Bus_timing[source],'P.M.')
        print('Total Fare per seat is: ',fare_chart[journey_route])
        print('Available Seat is: ',seat)
    Bus_details()
    choice2 = input('\n\nDo You Want to Book a Ticket Y/N: ')
    choice2=choice2.upper()
    if(choice2=='Y'):
        book_ticket()
    else:
        exit()

#function for book ticket
def book_ticket():
    print('\n*****Welcome to RSRTC Ticket Booking Window*****')
    source1=input('\nFrom:  ')
    source1=source1.upper()
    check_source(source1)

    destination1=input('\nTo : ')
    destination1=destination1.upper()
    check_dest_city(destination1)

    journey_route1=source1+' to '+destination1
    journey_route = ('From: ')+source1+'\tTo: '+destination1
    journey_date=(input('Enter Journey Date: '))

    seat=int(input('Choose a seat no. : '))
    #function to check that seat no. is valid or not
    def check_seat(x):
        if(x<1 or x>50):
            print('Please select a valid seat no. :')
            exit()
        else:
            return
    check_seat(seat)
    #Enter passenger details
    Pname = input('Enter Passenger Name: ') #name should be more than 3 letters
    Pname.upper()
    def check_name(x):
        if(len(x)<=2):
            print('Enter a valid name:')
            exit()
        else:
            return
    check_name(Pname)

    Page=int(input('Enter Passenger Age: ')) #age should be greater than 12
    def check_age(x):
        if(x<12):
            print('Passenger age should be between 12 to 70.')
            exit()
        else:
            return
    check_age(Page)

    Pgender = input('Enter Passenger Gender Male/Female: ')
    Pgender.upper()

    Pno = input('Enter Contact detail: ')
    def check_no(x):
        if(len(x)!=10):
            print('Mobile No. is Invalid.')
            exit()
        else:
            return
    check_no(Pno)

    pnr=randint(293843,849372)
    #print ticket details
    print('\n\n**Ticket details**')
    print('\n',journey_route)
    print('PNR NO. : ',pnr)
    print('Name: ',Pname,'\t\t\t','Date: ',journey_date,'.2018')
    print('Age: ',Page,'\t\t\t','Seat No. : ',seat)
    print('Gender: ',Pgender,'\t\t\t','Fare: ',fare_chart[journey_route1])
    print('Contact No. : ',Pno,'\t\t','Dept. Time: ',Bus_timing[source1],'P.M.')
    #insert into database
    prince='INSERT INTO ticket VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    prince1=(pnr,journey_route1,Pname,Page,Pgender,Pno,journey_date,seat,fare_chart[journey_route1],Bus_timing[source1])


    cursor.execute(prince, prince1)
    db.commit() #close the table

#check ticket status from database
def ticket_status():
    enter_pnr = int(input('Enter your PNR NO. : '))
    enter_pnr=int(enter_pnr)

    sql2='SELECT * FROM ticket WHERE pnr = %s'
    sql3=enter_pnr
    cursor.execute(sql2,sql3) #search ticket details in database
    result=cursor.fetchall()
    #loop to fetch all values from table
    for i in result:
        Ppnr = i[0]
        route = i[1]
        name = i[2]
        age = i[3]
        gender = i[4]
        no = i[5]
        date=i[6]
        seatno=i[7]
        fare=i[8]
        time=i[9]
        print('PNR = %s,\nJourney Route = %s,\nName = %s,Age = %s,Gender = %s,Phone No. = %s,\nDate of Journey = %s,Seat No. = %s,Fare = %s,Time = %s'\
              %(Ppnr,route,name,age,gender,no,date,seatno,fare,time))

#function for cancel ticket
def cancel_ticket():
    enter_pnr = input('Enter your pnr no. : ')
    sql='DELETE FROM ticket WHERE pnr = %s'
    sql2=enter_pnr
    cursor.execute(sql,sql2)
    db.commit()
    print('Your ticket is Canceled')


print('1. Search Bus')
print('2. Book Ticket')
print('3. Search Ticket Status')
print('4.Cancel Ticket')
choice = int(input('Enter your choice: '))
if(choice==1):
    search_bus()
elif(choice==2):
    book_ticket()
elif(choice==3):
    ticket_status()
elif(choice==4):
    cancel_ticket()
else:
    print('please choose a valid option ')
db.close() #close the database
