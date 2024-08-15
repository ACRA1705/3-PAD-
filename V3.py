import tkinter as tk
import random
from PIL import Image, ImageTk

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Game")

        # Initialize window size variables
        self.window_width = 1280
        self.window_height = 720
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.score = 0
        self.difficulty = "Easy"  # Default difficulty level
        self.mode = "Addition"  # Default mode
        self.time_limit = 60  # Timer duration in seconds
        self.time_left = self.time_limit

        # Create login screen
        self.create_login_screen()

    def load_background_image(self):
        try:
            self.bg_image = Image.open("Space.jpg")
        except IOError:
            print("Error: Background image file not found.")
            self.bg_image = Image.new('RGB', (self.window_width, self.window_height), color='black')
            
    def create_login_screen(self):
        self.clear_screen()

        self.login_label = tk.Label(self.root, text="Login", font=("Helvetica", 24))
        self.login_label.pack(pady=20)

        self.username_entry = tk.Entry(self.root, font=("Helvetica", 18))
        self.username_entry.pack(pady=10)
        # No default text inserted

        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 18))
        self.password_entry.pack(pady=10)
        # No default text inserted

        self.login_button = tk.Button(self.root, text="Login", command=self.show_mode_selection_screen, font=("Helvetica", 18), width=15)
        self.login_button.pack(pady=20)

    def show_mode_selection_screen(self):
        self.clear_screen()

        self.mode_label = tk.Label(self.root, text="Choose Mode", font=("Helvetica", 24))
        self.mode_label.pack(pady=20)

        self.addition_button = tk.Button(self.root, text="Addition", command=lambda: self.show_difficulty_options("Addition"), font=("Helvetica", 18), width=20)
        self.addition_button.pack(pady=10)

        self.subtraction_button = tk.Button(self.root, text="Subtraction", command=lambda: self.show_difficulty_options("Subtraction"), font=("Helvetica", 18), width=20)
        self.subtraction_button.pack(pady=10)

        self.multiplication_button = tk.Button(self.root, text="Multiplication", command=lambda: self.show_difficulty_options("Multiplication"), font=("Helvetica", 18), width=20)
        self.multiplication_button.pack(pady=10)

        self.division_button = tk.Button(self.root, text="Division", command=lambda: self.show_difficulty_options("Division"), font=("Helvetica", 18), width=20)
        self.division_button.pack(pady=10)

    def show_difficulty_options(self, mode):
        self.mode = mode
        self.clear_screen()

        self.difficulty_label = tk.Label(self.root, text="Choose Difficulty", font=("Helvetica", 24))
        self.difficulty_label.pack(pady=20)

        self.easy_button = tk.Button(self.root, text="Easy", command=lambda: self.start_game("Easy"), font=("Helvetica", 18), width=15)
        self.easy_button.pack(pady=10)

        self.hard_button = tk.Button(self.root, text="Hard", command=lambda: self.start_game("Hard"), font=("Helvetica", 18), width=15)
        self.hard_button.pack(pady=10)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.clear_screen()
        self.load_background_image()

        # Create background label
        self.bg_label = tk.Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)

        # Set the background image
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((self.window_width, self.window_height)))
        self.bg_label.config(image=self.bg_photo)

        # Score and timer labels
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 24), bg='lightblue')
        self.score_label.place(x=self.window_width - 150, y=10, anchor='ne')  # Top right

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}", font=("Helvetica", 24), bg='lightblue')
        self.timer_label.place(x=10, y=10, anchor='nw')  # Top left

        # Problem label
        self.problem_label = tk.Label(self.root, text="", font=("Helvetica", 24), bg='white')
        self.problem_label.place(relx=0.5, rely=0.3, anchor='center')

        # Create and place answer buttons in the four corners at the bottom
        self.create_answer_buttons()

        # Feedback label
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 18), bg='lightblue')
        self.feedback_label.place(relx=0.5, rely=0.7, anchor='center')

        # Bind window resize event
        self.root.bind('<Configure>', self.on_resize)

        self.new_problem()
        self.update_timer()

    def on_resize(self, event):
        self.window_width = event.width
        self.window_height = event.height
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((self.window_width, self.window_height)))
        self.bg_label.config(image=self.bg_photo)

        # Update position of score and timer labels on resize
        self.score_label.place(x=self.window_width - 150, y=10, anchor='ne')
        self.timer_label.place(x=10, y=10, anchor='nw')

    def create_answer_buttons(self):
        self.answer_buttons_frame = tk.Frame(self.root)
        self.answer_buttons_frame.place(relx=0.5, rely=0.9, anchor='center')

        # Create a grid layout for buttons within the frame
        self.answer_buttons_frame.grid_columnconfigure(0, weight=1)
        self.answer_buttons_frame.grid_columnconfigure(1, weight=1)
        self.answer_buttons_frame.grid_rowconfigure(0, weight=1)
        self.answer_buttons_frame.grid_rowconfigure(1, weight=1)

        self.answer_buttons = []
        button_width = 20
        button_height = 2

        # Create and place answer buttons
        button_positions = [
            (0, 1),  # Bottom left
            (1, 1),  # Bottom right
            (0, 0),  # Top left
            (1, 0)   # Top right
        ]

        for i, (col, row) in enumerate(button_positions):
            button = tk.Button(self.answer_buttons_frame, text="", font=("Helvetica", 18), width=button_width, height=button_height, relief=tk.RAISED, bd=3, command=lambda b=i: self.check_answer(b))
            button.grid(column=col, row=row, padx=10, pady=10, sticky='nsew')
            self.answer_buttons.append(button)

    def new_problem(self):
        if self.difficulty == "Easy":
            self.num1 = random.randint(1, 20)
            self.num2 = random.randint(1, 20)
        else:  # Hard difficulty
            self.num1 = random.randint(20, 100)
            self.num2 = random.randint(20, 100)

        if self.mode == "Addition":
            self.answer = self.num1 + self.num2
            self.problem_label.config(text=f"What is {self.num1} + {self.num2}?", bg='lightblue')

        elif self.mode == "Subtraction":
            self.num1 = max(self.num1, self.num2)  # Ensure positive results for subtraction
            self.num2 = min(self.num1, self.num2)
            self.answer = self.num1 - self.num2
            self.problem_label.config(text=f"What is {self.num1} - {self.num2}?", bg='lightblue')

        elif self.mode == "Multiplication":
            self.answer = self.num1 * self.num2
            self.problem_label.config(text=f"What is {self.num1} × {self.num2}?", bg='lightblue')

        elif self.mode == "Division":
            self.num2 = random.randint(1, 12)
            self.answer = random.randint(1, 12) * self.num2
            self.problem_label.config(text=f"What is {self.answer} ÷ {self.num2}?", bg='lightblue')

        # Generate and shuffle answer options
        options = [self.answer]
        while len(options) < 4:
            wrong_answer = random.randint(self.answer - 10, self.answer + 10)
            if wrong_answer != self.answer and wrong_answer not in options:
                options.append(wrong_answer)

        random.shuffle(options)
        self.correct_answer_index = options.index(self.answer)

        for i, button in enumerate(self.answer_buttons):
            button.config(text=str(options[i]), bg='lightblue')

    def check_answer(self, selected_index):
        if selected_index == self.correct_answer_index:
            self.score += 1
            self.feedback_label.config(text="Correct! Well done!", bg='lightblue')
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer was {self.answer}.")
            if self.score > 0:
                self.score -= 1

        # Update score label
        self.score_label.config(text=f"Score: {self.score}")
        self.new_problem()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        self.clear_screen()

        self.end_label = tk.Label(self.root, text=f"Time's up! Your final score is {self.score}.", font=("Helvetica", 24))
        self.end_label.pack(pady=20)

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.show_mode_selection_screen, font=("Helvetica", 18), width=15)
        self.play_again_button.pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
