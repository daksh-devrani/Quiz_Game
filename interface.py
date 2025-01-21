import tkinter as tk  # Importing tkinter library for GUI creation
from tkinter import messagebox  # Importing messagebox for pop-up alerts
from quiz import QuizLogic, level  # Importing QuizLogic and level function from the quiz module


class QuizGame:
    def __init__(self, root):
        self.root = root  # Store reference to the root window
        self.root.title("Hangman Quiz Game")  # Set the window title
        self.root.geometry("900x700")  # Set window size
        self.root.configure(bg="#1a1a2e")  # Set background color of the window

        self.logic = QuizLogic()  # Create an instance of the QuizLogic class to handle game logic
        self.max_ques = 0  # Variable to store maximum number of questions based on difficulty level

        self.create_start_screen()  # Call method to display the start screen

    def clear_widgets(self):
        """Helper function to clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_label(self, text, font_size=18, font_weight="normal", fg="#f5f5f5", bg="#1a1a2e", pady=10, padx=20, anchor="nw"):
        """Helper function to create a label."""
        label = tk.Label(self.root, text=text, font=("Helvetica", font_size, font_weight), fg=fg, bg=bg)
        label.pack(pady=pady, padx=padx, anchor=anchor)
        return label

    def create_button(self, text, font_size=16, command=None, bg="#0f3460", fg="white", pady=10):
        """Helper function to create a button."""
        button = tk.Button(self.root, text=text, font=("Helvetica", font_size), bg=bg, fg=fg, command=command)
        button.pack(pady=pady)
        return button

    def create_start_screen(self):
        """Creates the initial start screen where the user selects difficulty."""
        self.clear_widgets()  # Remove all previous widgets from the window

        # Title Label
        self.create_label("Hangman Quiz Game", 36, "bold", "#e94560", "#1a1a2e", pady=40)

        # Difficulty Selection Label
        self.create_label("Select Difficulty Level:", 20, "", "#f5f5f5", "#1a1a2e", pady=20)

        # Difficulty Level Buttons
        self.create_button("Easy", 16, lambda: self.start_game(1))
        self.create_button("Normal", 16, lambda: self.start_game(2))
        self.create_button("Hard", 16, lambda: self.start_game(3))

    def start_game(self, level_no):
        """Start the game with the selected difficulty level."""
        self.logic.points = 0  # Reset points to 0
        self.logic.wrong_attempts = 0  # Reset wrong attempts
        self.logic.ques_asked = []  # Clear the list of asked questions
        self.max_ques = level(level_no)  # Set the maximum number of questions based on selected difficulty
        self.load_question()  # Start loading questions

    def load_question(self):
        """Load a question and handle end game scenarios."""
        question_text, answer, correct_answer, end_game = self.logic.load_question(self.max_ques)

        if end_game is True:
            self.end_game(True)  # End game if all questions have been asked
        elif end_game is False:
            self.end_game(False)  # End game if wrong attempts exceed limit
        else:
            self.show_question(question_text, answer, correct_answer)  # Show current question

    def draw_hangman(self, canvas):
        """Draws the hangman image based on the number of wrong attempts."""
        canvas.delete("all")  # Clear previous drawing

        # Draw the components of the hangman (base, pole, beam, rope)
        canvas.create_line(50, 300, 150, 300, width=5, fill="#f5f5f5")
        canvas.create_line(100, 300, 100, 50, width=5, fill="#f5f5f5")
        canvas.create_line(100, 50, 200, 50, width=5, fill="#f5f5f5")
        canvas.create_line(200, 50, 200, 100, width=3, fill="#f5f5f5")

        # Define steps to draw hangman parts based on wrong attempts
        steps = [
            lambda: canvas.create_oval(175, 100, 225, 150, width=3, outline="#f5f5f5"),  # Head
            lambda: canvas.create_line(200, 150, 200, 220, width=3, fill="#f5f5f5"),  # Body
            lambda: canvas.create_line(200, 170, 180, 200, width=3, fill="#f5f5f5"),  # Left Arm
            lambda: canvas.create_line(200, 170, 220, 200, width=3, fill="#f5f5f5"),  # Right Arm
            lambda: canvas.create_line(200, 220, 180, 260, width=3, fill="#f5f5f5"),  # Left Leg
            lambda: canvas.create_line(200, 220, 220, 260, width=3, fill="#f5f5f5"),  # Right Leg
        ]

        # Draw the hangman progressively based on wrong attempts
        for i in range(self.logic.wrong_attempts):
            if i < len(steps):
                steps[i]()  # Execute each step (drawing part)

    def show_question(self, question_text, answers, correct_answer):
        """Displays the current question and possible answers."""
        self.clear_widgets()  # Remove all previous widgets

        # Display current score and remaining lives
        self.create_label(f"Points: {self.logic.points}", 18, "", "#f5f5f5", "#1a1a2e", pady=20, padx=20)
        self.create_label(f"Remaining Lives: {8 - self.logic.wrong_attempts}", 18, "", "#f5f5f5", "#1a1a2e", pady=10, padx=20)

        # Create a canvas for drawing the hangman
        canvas = tk.Canvas(self.root, width=400, height=300, bg="#16213e")
        canvas.pack(pady=20)
        self.draw_hangman(canvas)  # Draw hangman

        # Create a frame for the question box
        question_box = tk.Frame(self.root, bg="#0f3460", bd=5, relief="ridge")
        question_box.pack(pady=20, padx=20, fill="x")

        # Display the question text
        tk.Label(question_box, text=question_text, font=("Helvetica", 18), fg="#f5f5f5", bg="#0f3460", wraplength=750, justify="left").pack(pady=20, padx=10)

        # Create a frame for displaying the answer options
        answer_box = tk.Frame(self.root, bg="#1a1a2e", bd=5, relief="ridge")
        answer_box.pack(pady=7, padx=20, fill="x")

        # Create buttons for each answer option
        answer_frame = tk.Frame(answer_box, bg="#1a1a2e")
        answer_frame.pack(pady=10)
        row = 0
        col = 0
        for key, opt in zip(['A', 'B', 'C', 'D'], answers):
            tk.Button(answer_frame, text=opt, font=("Helvetica", 18), bg="#0f3460", fg="white", width=40, height=2,
                      command=lambda key=key: self.check_answer(key, correct_answer)).grid(row=row, column=col, padx=20, pady=10)

            col += 1
            if col > 1:
                col = 0
                row += 1

    def check_answer(self, answer, correct_answer):
        """Checks if the selected answer is correct and updates the score."""
        if answer.lower() == correct_answer.lower():
            self.logic.points += 1  # Correct answer, increase score
        else:
            self.logic.wrong_attempts += 1  # Incorrect answer, increase wrong attempts

        self.load_question()  # Load next question

    def end_game(self, won):
        """Ends the game and shows the result."""
        self.clear_widgets()  # Remove all widgets

        # Display game over or win message
        message = f"Congratulations! You won the game with {self.logic.points} points." if won else f"Game Over! You scored {self.logic.points} points."
        self.create_label(message, 20, "", "#f5f5f5", "#1a1a2e", pady=40)

        # If game is lost, show full hangman
        if not won:
            canvas = tk.Canvas(self.root, width=400, height=300, bg="#16213e")
            canvas.pack(pady=20)
            self.logic.wrong_attempts = 6  # Ensure the full hangman is drawn
            self.draw_hangman(canvas)

        # Buttons for playing again or exiting
        self.create_button("Play Again", 16, self.create_start_screen)
        self.create_button("Exit", 16, self.root.quit)


# Initialize the game
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    game = QuizGame(root)  # Create an instance of the QuizGame class
    root.mainloop()  # Start the Tkinter event loop
