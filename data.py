# Importing necessary libraries
from bs4 import BeautifulSoup  # For parsing HTML content
import requests  # To make HTTP requests
import regex as re  # For pattern matching in text
import mysql.connector  # To interact with the MySQL database


# Function to check if the 'question' table already exists in the database
def check():
    table_name = "question"

    # SQL query to check if the table exists in the current database
    querry = """
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = %s AND table_name = %s
    """
    # Executing the query
    mycursor.execute(querry, (mydb.database, table_name))
    result = mycursor.fetchone()

    # If table exists, return True, else return False
    if result[0] > 0:
        return True
    else:
        return False


# Connecting to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='daksh',
    auth_plugin='mysql_native_password'
)

# Creating a cursor to interact with the database
mycursor = mydb.cursor()

# Creating the database if it doesn't exist
mycursor.execute("create database if not exists ques_bank")
mycursor.execute("use ques_bank")

# If the 'question' table doesn't exist, create it
if not check():
    # SQL query to create the 'question' table
    mycursor.execute("""
    create table question(
        SR_No bigint, 
        Ques varchar(300), 
        Option_A varchar(100), 
        Option_B varchar(100), 
        Option_C varchar(100), 
        Option_D varchar(100), 
        Correct varchar(10)
    )
    """)

    # Regex pattern to extract question and number
    pattern = '([0-9]*). ([A-z ]*)'

    # Fetching HTML content from the specified URL and parsing it with BeautifulSoup
    content = requests.get("https://ays-pro.com/blog/free-general-knowledge-questions").content
    soup = BeautifulSoup(content, 'html.parser')

    # Finding all the paragraph tags containing questions
    ques = soup.find_all('p')
    # Finding all ordered lists (options) on the page
    opt = soup.find_all('ol')
    # Finding all correct answers marked with <em> tags
    correct = soup.select('p em')

    count = 0  # To keep track of questions
    lst = []  # List to store all the scraped data

    # Looping through each paragraph (question)
    for i in ques:
        ques_bank = []  # Temporary list to store each question and options
        if i.get_text(strip=True)[0].isdigit():  # Check if the paragraph contains a question
            # Matching the question number and text using regex
            question = re.search(pattern, i.get_text(strip=True))
            ques_bank.append(question.group(1))  # Add question number
            ques_bank.append(question.group(2))  # Add question text
            # Getting options from the corresponding ordered list
            options = opt[count].get_text(separator='  ', strip=True).split("  ")
            ques_bank.extend(options)  # Adding options to the question data
            # Extracting the correct answer from the 'correct' list
            ans = correct[count + 1].get_text(strip=True)[16]  # Extract the correct answer
            ques_bank.append(ans)  # Add correct answer to the data
            lst.append(ques_bank)  # Add the complete question data to the list
            count += 1
        # Stop after collecting 120 questions
        if count == 120:
            break

    # Preparing data to be inserted into the database
    a = tuple(lst)
    query = "insert into question values(%s, %s, %s, %s, %s ,%s, %s)"  # SQL query to insert data
    mycursor.executemany(query, a)  # Executing the insert query for all questions
    mydb.commit()  # Committing the transaction to save changes
