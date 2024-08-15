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
        self.difficulty = "Easy"  # Default difficulty
        self.time_limit = 60  # Timer duration in seconds
        self.time_left = self.time_limit

        # Create login screen
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.login_label = tk.Label(self.root, text="Login", font=("Helvetica", 24), bg='lightblue')
        self.login_label.pack(pady=20)

        self.username_entry = tk.Entry(self.root, font=("Helvetica", 18))
        self.username_entry.pack(pady=10)
        self.username_entry.insert(0, "Username")

        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 18))
        self.password_entry.pack(pady=10)
        self.password_entry.insert(0, "Password")

        self.login_button = tk.Button(self.root, text="Login", command=self.show_difficulty_options, font=("Helvetica", 18))
        self.login_button.pack(pady=20)

    def show_difficulty_options(self):
        self.clear_screen()

        self.difficulty_label = tk.Label(self.root, text="Choose Difficulty", font=("Helvetica", 24), bg='lightblue')
        self.difficulty_label.pack(pady=20)

        self.easy_button = tk.Button(self.root, text="Easy", command=lambda: self.start_game("Easy"), font=("Helvetica", 18))
        self.easy_button.pack(pady=10)

        self.hard_button = tk.Button(self.root, text="Hard", command=lambda: self.start_game("Hard"), font=("Helvetica", 18))
        self.hard_button.pack(pady=10)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.clear_screen()
        self.load_background_image()

        # Create background label
        self.bg_label = tk.Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)

        # Start the animation
        self.update_background()

        # Create and place widgets directly on the background
        self.problem_label = tk.Label(self.root, text="", font=("Helvetica", 24), bg='white')
        self.problem_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 18))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer, font=("Helvetica", 18))
        self.submit_button.pack(pady=10)

        # Place score, feedback, and timer labels directly on the background
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 24), bg='lightblue')
        self.score_label.pack(side=tk.BOTTOM, anchor='se', padx=20, pady=10)

        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 18), bg='lightblue')
        self.feedback_label.pack(side=tk.BOTTOM, anchor='se', padx=20, pady=10)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}", font=("Helvetica", 24), bg='lightblue')
        self.timer_label.pack(side=tk.BOTTOM, anchor='sw', padx=20, pady=10)

        # Bind the "Enter" key to the submit button
        self.root.bind('<Return>', self.submit_on_enter)
        # Bind window resize event
        self.root.bind('<Configure>', self.on_resize)

        self.new_problem()
        self.update_timer()

    def load_background_image(self):
        try:
            self.bg_image = Image.open("forest.gif")
            self.bg_frames = [ImageTk.PhotoImage(self.bg_image.copy().convert('RGBA').resize((self.window_width, self.window_height))) for _ in range(self.bg_image.n_frames)]
        except IOError:
            print("Error: Background image file not found.")
            self.bg_frames = []

        self.current_frame = 0

    def update_background(self):
        if self.bg_frames:
            self.bg_label.config(image=self.bg_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.root.after(200, self.update_background)  # Adjust the delay as needed

    def on_resize(self, event):
        self.window_width = event.width
        self.window_height = event.height
        self.load_background_image()
        self.update_background()

    def new_problem(self):
        if self.difficulty == "Easy":
            self.num1 = random.randint(1, 20)
            self.num2 = random.randint(1, 20)
        else:  # Hard difficulty
            self.num1 = random.randint(20, 100)
            self.num2 = random.randint(20, 100)

        self.operation = random.choice(['+', '-'])

        if self.operation == '+':
            self.answer = self.num1 + self.num2
            self.problem_label.config(text=f"What is {self.num1} + {self.num2}?")
        else:
            self.answer = self.num1 - self.num2
            self.problem_label.config(text=f"What is {self.num1} - {self.num2}?")

        # Clear feedback label
        self.feedback_label.config(text="")

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.")
            return

        if user_answer == self.answer:
            self.score += 1
            self.feedback_label.config(text="Correct! Well done!")
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer was {self.answer}.")

        # Update score label
        self.score_label.config(text=f"Score: {self.score}")

        self.answer_entry.delete(0, tk.END)
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
        self.end_label = tk.Label(self.root, text=f"Time's up! Your final score is: {self.score}", font=("Helvetica", 24), bg='lightblue')
        self.end_label.pack(pady=20)

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.create_login_screen, font=("Helvetica", 18))
        self.play_again_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Helvetica", 18))
        self.quit_button.pack(pady=10)

    def submit_on_enter(self, event):
        self.check_answer()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
