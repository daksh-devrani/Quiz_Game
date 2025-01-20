from data import *
import random

def level(level_no):
    if level_no == 1:
        return 10
    elif level_no == 2:
        return 25
    elif level_no == 3:
        return 50


def draw_box(content):
    """Draws a box around the provided content."""
    lines = content.split('\n')
    max_length = max(len(line) for line in lines)
    border = "+" + "-" * (max_length + 2) + "+"

    print(border)
    for line in lines:
        print(f"| {line.ljust(max_length)} |")
    print(border)

def display_question_with_hangman(question, hangman_stage):
    """Displays the question and hangman in the same box."""
    question_lines = question.split('\n')
    hangman_lines = hangman_stage.split('\n')

    # Calculate box dimensions
    max_question_length = max(len(line) for line in question_lines)
    max_hangman_length = max(len(line) for line in hangman_lines)
    max_length = max(max_question_length, max_hangman_length)

    border = "+" + "-" * (max_length + 4) + "+"

    print(border)
    for q_line, h_line in zip(question_lines, hangman_lines):
        print(f"| {q_line.ljust(max_length)} | {h_line.ljust(max_length)} |")
    print(border)



def get_hangman_stage(wrong_attempts):
    """Returns the hangman stage based on the number of wrong attempts."""
    stages = [
        "\n\n\n\n\n\n_____",
        '''\n |
         |
         |
         |
         |
        _____''',
                '''  _______
         |
         |
         |
         |
         |
        _____''',
                '''  _______
         |       |
         |
         |
         |
         |
        _____''',
                '''  _______
         |       |
         |       O
         |
         |
         |
        _____''',
                '''  _______
         |       |
         |       O
         |       |
         |
         |
        _____''',
                '''  _______
         |       |
         |       O
         |      /|\\
         |
         |
        _____''',
                '''  _______
         |       |
         |       O
         |      /|\\
         |      / 
        _____''',
                '''  _______
         |       |
         |       O
         |      /|\\
         |      / \\
        _____'''
            ]
    return stages[wrong_attempts]

points = 0
wrong_attempts = 0
max_attempts = 8
ques_asked = []
max_ques = level(int(input('1. easy\n2. normal\n3. hard\nChoose your level:   ')))
while wrong_attempts < max_attempts and len(ques_asked) != max_ques:
    ques = random.randint(1, 120)
    if ques not in ques_asked:
        ques_asked.append(ques)
        query = "select * from question where SR_No = " + str(ques) + ""
        mycursor.execute(query)
        ask = mycursor.fetchone()

        question_text = f"{ask[1]}\nA. {ask[2]}\nB. {ask[3]}\nC. {ask[4]}\nD. {ask[5]}"
        hangman_stage = get_hangman_stage(wrong_attempts)
        display_question_with_hangman(question_text, hangman_stage)

        ans = input("Enter your choice: ")
        if ans.lower() == ask[6]:
            points += 1
        else:
            wrong_attempts += 1

if wrong_attempts == max_attempts:
    print("Game Over! The hangman is complete.")
    print(get_hangman_stage(wrong_attempts))
    print(f"You scored {points} points!")
else:
    print(f"You scored {points} points!")
