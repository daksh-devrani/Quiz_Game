from bs4 import BeautifulSoup
import requests
import re
import mysql.connector


def check():
    table_name = "question"

    # Query to check if the table exists
    querry = """
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = %s AND table_name = %s
    """
    mycursor.execute(querry, (mydb.database, table_name))
    result = mycursor.fetchone()
    if result[0] > 0:
        return True
    else:
        return False


# connecting to mysql database
mydb = mysql.connector.connect(host="localhost", user="root", password=input("Enter MySql Password: "), auth_plugin='mysql_native_password')

# creating cursor and database
mycursor = mydb.cursor()
mycursor.execute("create database if not exists ques_bank")
mycursor.execute("use ques_bank")
if not check():
    mycursor.execute("create table question(SR_No bigint, Ques varchar(300), Option_A varchar(100), Option_B varchar(100), Option_C varchar(100), Option_D varchar(100), Correct varchar(10))")

    # Regex pattern
    pattern = '([0-9]*). ([A-z ]*)'

    # Getting HTML Content from the website and parsing it
    content = requests.get("https://ays-pro.com/blog/free-general-knowledge-questions").content
    soup = BeautifulSoup(content, 'html.parser')

    # Finding the data needed
    ques = soup.find_all('p')
    opt = soup.find_all('ol')
    correct = soup.select('p em')
    count = 0
    lst = []

    # Scrapping the data needed
    for i in ques:
        ques_bank = []
        if i.get_text(strip=True)[0].isdigit():
            question = re.search(pattern, i.get_text(strip=True))
            ques_bank.append(question.group(1))
            ques_bank.append(question.group(2))
            options = opt[count].get_text(separator='  ', strip=True).split("  ")
            ques_bank.extend(options)
            ans = correct[count+1].get_text(strip=True)[16]
            ques_bank.append(ans)
            lst.append(ques_bank)
            count += 1
        if count == 120:
            break

    # Inserting data in the database
    a = tuple(lst)
    query = "insert into question values(%s, %s, %s, %s, %s ,%s, %s)"
    mycursor.execute(query, a)
    mydb.commit()
