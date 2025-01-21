import random  # Importing the random module to generate random numbers
from Quiz_Game.data import \
    mycursor  # Importing the database cursor from the 'data' module to interact with the database


# Function to select the difficulty level and return the corresponding maximum number of questions
def level(level_no):
    if level_no == 1:
        return 10  # Easy level, 10 questions
    elif level_no == 2:
        return 25  # Normal level, 25 questions
    elif level_no == 3:
        return 50  # Hard level, 50 questions


# Class to handle the main quiz logic
class QuizLogic:
    def __init__(self):
        self.points = 0  # Initialize the points to 0
        self.wrong_attempts = 0  # Initialize wrong attempts to 0
        self.ques_asked = []  # List to store the questions that have already been asked to avoid repetition

    def load_question(self, max_ques):
        """Load a question from the database based on difficulty level"""

        # End the game if the player has already made 8 wrong attempts
        if self.wrong_attempts >= 8:
            return None, None, None, False  # No question, game over

        # End the game if the maximum number of questions for this level has been asked
        if len(self.ques_asked) >= max_ques:
            return None, None, None, True  # No question, game complete

        # Select a random question number (between 1 and 120) that has not been asked already
        ques = random.randint(1, 120)
        while ques in self.ques_asked:
            ques = random.randint(1, 120)  # Keep selecting a new question number until it's unique

        self.ques_asked.append(ques)  # Add the question to the list of asked questions to prevent repeat questions

        # Create the SQL query to fetch the question data from the database
        query = "SELECT * FROM question WHERE SR_No = " + str(ques)
        mycursor.execute(query)  # Execute the query
        ask = mycursor.fetchone()  # Fetch the first result of the query (a single question)

        if ask:
            # If a question is found, extract the question text and its possible answers from the database row
            question_text = f"{ask[1]}"  # Assuming ask[1] contains the question text
            answers = [ask[2], ask[3], ask[4], ask[5]]  # The possible answers are assumed to be in ask[2] to ask[5]
            return question_text, answers, ask[
                6], None  # Return the question, answer options, and the correct answer (ask[6])

        # Return None if no valid question is found
        return None, None, None, None
