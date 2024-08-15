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

        # Load and set up the background image
        self.load_background_image()

        # Create background label
        self.bg_label = tk.Label(root)
        self.bg_label.place(relwidth=1, relheight=1)

        # Start the animation
        self.update_background()

        # Create and place widgets directly on the background
        self.problem_label = tk.Label(root, text="", font=("Helvetica", 24), bg='white')
        self.problem_label.pack(pady=20)

        self.answer_entry = tk.Entry(root, font=("Helvetica", 18))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer, font=("Helvetica", 18))
        self.submit_button.pack(pady=10)

        # Create a frame to hold the score counter
        self.side_frame = tk.Frame(root, bg='lightblue')
        self.side_frame.pack(side=tk.BOTTOM, anchor='se', padx=20, pady=20, fill=tk.X)

        self.score_label = tk.Label(self.side_frame, text=f"Score: {self.score}", font=("Helvetica", 24), bg='lightblue')
        self.score_label.pack()

        self.feedback_label = tk.Label(self.side_frame, text="", font=("Helvetica", 18), bg='lightblue')
        self.feedback_label.pack(pady=20)

        # Bind the "Enter" key to the submit button
        self.root.bind('<Return>', self.submit_on_enter)
        # Bind window resize event
        self.root.bind('<Configure>', self.on_resize)

        self.new_problem()

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
        self.num1 = random.randint(1, 20)
        self.num2 = random.randint(1, 20)
        self.operation = random.choice(['+', '-'])

        if self.operation == '+':
            self.answer = self.num1 + self.num2
            self.problem_label.config(text=f"What is {self.num1} + {self.num2}?")
        else:
            self.num1 > self.num2
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

    def submit_on_enter(self, event):
        self.check_answer()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
