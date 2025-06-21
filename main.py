import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz App")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Quiz data
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.quiz_started = False
        
        # Load default questions
        self.load_default_questions()
        
        # Create GUI
        self.create_widgets()
        self.show_welcome_screen()
    
    def load_default_questions(self):
        """Load default questions for the quiz"""
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": 2,
                "explanation": "Paris is the capital and largest city of France."
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1,
                "explanation": "Mars is called the Red Planet due to iron oxide on its surface."
            },
            {
                "question": "What is 2 + 2 × 3?",
                "options": ["12", "8", "10", "6"],
                "correct": 1,
                "explanation": "Following order of operations: 2 + (2 × 3) = 2 + 6 = 8"
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct": 1,
                "explanation": "William Shakespeare wrote this famous tragedy in the early part of his career."
            },
            {
                "question": "Which element has the chemical symbol 'O'?",
                "options": ["Gold", "Silver", "Oxygen", "Iron"],
                "correct": 2,
                "explanation": "Oxygen is a chemical element with symbol O and atomic number 8."
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "correct": 1,
                "explanation": "The Blue Whale is the largest animal ever known to have lived on Earth."
            },
            {
                "question": "In which year did World War II end?",
                "options": ["1944", "1945", "1946", "1947"],
                "correct": 1,
                "explanation": "World War II ended in 1945 with the surrender of Japan in September."
            },
            {
                "question": "What is the smallest prime number?",
                "options": ["0", "1", "2", "3"],
                "correct": 2,
                "explanation": "2 is the smallest prime number and the only even prime number."
            }
        ]
        self.user_answers = [None] * len(self.questions)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome screen frame
        self.welcome_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        
        # Quiz frame
        self.quiz_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        
        # Results frame
        self.results_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        
        self.create_welcome_screen()
        self.create_quiz_screen()
        self.create_results_screen()
    
    def create_welcome_screen(self):
        """Create welcome screen widgets"""
        # Title
        title_label = tk.Label(self.welcome_frame, text="🎯 Interactive Quiz App", 
                              font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=30)
        
        # Description
        desc_text = "Test your knowledge with our interactive quiz!\n\nFeatures:\n• Multiple choice questions\n• Instant feedback\n• Score tracking\n• Question navigation"
        desc_label = tk.Label(self.welcome_frame, text=desc_text, 
                             font=("Arial", 12), bg="#f0f0f0", fg="#34495e", justify=tk.CENTER)
        desc_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.welcome_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=30)
        
        # Start quiz button
        start_btn = tk.Button(buttons_frame, text="Start Quiz", 
                             command=self.start_quiz,
                             font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                             padx=30, pady=10, cursor="hand2")
        start_btn.pack(side=tk.LEFT, padx=10)
        
        # Load questions button
        load_btn = tk.Button(buttons_frame, text="Load Questions", 
                            command=self.load_questions_from_file,
                            font=("Arial", 14), bg="#2ecc71", fg="white",
                            padx=20, pady=10, cursor="hand2")
        load_btn.pack(side=tk.LEFT, padx=10)
        
        # Random order checkbox
        self.random_var = tk.BooleanVar()
        random_cb = tk.Checkbutton(self.welcome_frame, text="Randomize Question Order",
                                  variable=self.random_var, font=("Arial", 12),
                                  bg="#f0f0f0", fg="#2c3e50")
        random_cb.pack(pady=10)
    
    def create_quiz_screen(self):
        """Create quiz screen widgets"""
        # Header frame
        header_frame = tk.Frame(self.quiz_frame, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(header_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.pack(side=tk.LEFT)
        
        # Question counter
        self.question_counter = tk.Label(header_frame, text="Question 1 of 8", 
                                        font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#2c3e50")
        self.question_counter.pack(side=tk.RIGHT)
        
        # Question frame
        question_frame = tk.Frame(self.quiz_frame, bg="white", relief=tk.RAISED, bd=2)
        question_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Question text
        self.question_label = tk.Label(question_frame, text="", 
                                      font=("Arial", 16, "bold"), bg="white", fg="#2c3e50",
                                      wraplength=700, justify=tk.LEFT)
        self.question_label.pack(pady=20, padx=20)
        
        # Options frame
        self.options_frame = tk.Frame(question_frame, bg="white")
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Radio button variable
        self.selected_option = tk.IntVar()
        self.option_buttons = []
        
        # Create option buttons
        for i in range(4):
            btn = tk.Radiobutton(self.options_frame, text="", variable=self.selected_option,
                               value=i, font=("Arial", 12), bg="white", fg="#2c3e50",
                               wraplength=600, justify=tk.LEFT, anchor="w")
            btn.pack(fill=tk.X, pady=5, padx=10)
            self.option_buttons.append(btn)
        
        # Navigation frame
        nav_frame = tk.Frame(self.quiz_frame, bg="#f0f0f0")
        nav_frame.pack(fill=tk.X, pady=20)
        
        # Previous button
        self.prev_btn = tk.Button(nav_frame, text="← Previous", 
                                 command=self.previous_question,
                                 font=("Arial", 12), bg="#95a5a6", fg="white",
                                 padx=20, pady=8, cursor="hand2")
        self.prev_btn.pack(side=tk.LEFT)
        
        # Next button
        self.next_btn = tk.Button(nav_frame, text="Next →", 
                                 command=self.next_question,
                                 font=("Arial", 12), bg="#3498db", fg="white",
                                 padx=20, pady=8, cursor="hand2")
        self.next_btn.pack(side=tk.RIGHT)
        
        # Submit button
        self.submit_btn = tk.Button(nav_frame, text="Submit Quiz", 
                                   command=self.submit_quiz,
                                   font=("Arial", 12, "bold"), bg="#e74c3c", fg="white",
                                   padx=20, pady=8, cursor="hand2")
        self.submit_btn.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_results_screen(self):
        """Create results screen widgets"""
        # Title
        self.results_title = tk.Label(self.results_frame, text="🎉 Quiz Results", 
                                     font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50")
        self.results_title.pack(pady=30)
        
        # Score display
        self.score_label = tk.Label(self.results_frame, text="", 
                                   font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#27ae60")
        self.score_label.pack(pady=20)
        
        # Results text
        self.results_text = tk.Text(self.results_frame, width=80, height=15, 
                                   font=("Arial", 11), wrap=tk.WORD)
        self.results_text.pack(pady=20, padx=20)
        
        # Buttons frame
        results_buttons = tk.Frame(self.results_frame, bg="#f0f0f0")
        results_buttons.pack(pady=20)
        
        # Restart button
        restart_btn = tk.Button(results_buttons, text="Take Quiz Again", 
                               command=self.restart_quiz,
                               font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                               padx=20, pady=10, cursor="hand2")
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        # Home button
        home_btn = tk.Button(results_buttons, text="Back to Home", 
                            command=self.show_welcome_screen,
                            font=("Arial", 12), bg="#95a5a6", fg="white",
                            padx=20, pady=10, cursor="hand2")
        home_btn.pack(side=tk.LEFT, padx=10)
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        self.quiz_frame.pack_forget()
        self.results_frame.pack_forget()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_quiz_screen(self):
        """Show quiz screen"""
        self.welcome_frame.pack_forget()
        self.results_frame.pack_forget()
        self.quiz_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_results_screen(self):
        """Show results screen"""
        self.welcome_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)
    
    def start_quiz(self):
        """Start the quiz"""
        if not self.questions:
            messagebox.showerror("Error", "No questions available!")
            return
        
        # Randomize questions if selected
        if self.random_var.get():
            random.shuffle(self.questions)
        
        self.current_question = 0
        self.score = 0
        self.user_answers = [None] * len(self.questions)
        self.quiz_started = True
        
        self.show_quiz_screen()
        self.display_question()
    
    def display_question(self):
        """Display current question"""
        if self.current_question >= len(self.questions):
            return
        
        question_data = self.questions[self.current_question]
        
        # Update question counter and progress
        self.question_counter.config(text=f"Question {self.current_question + 1} of {len(self.questions)}")
        progress = ((self.current_question + 1) / len(self.questions)) * 100
        self.progress_var.set(progress)
        
        # Display question
        self.question_label.config(text=question_data["question"])
        
        # Display options
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=f"{chr(65+i)}. {option}")
        
        # Set selected option if user has answered before
        if self.user_answers[self.current_question] is not None:
            self.selected_option.set(self.user_answers[self.current_question])
        else:
            self.selected_option.set(-1)  # Clear selection
        
        # Update button states
        self.prev_btn.config(state=tk.NORMAL if self.current_question > 0 else tk.DISABLED)
        self.next_btn.config(text="Next →" if self.current_question < len(self.questions) - 1 else "Finish")
    
    def next_question(self):
        """Go to next question"""
        # Save current answer
        if self.selected_option.get() != -1:
            self.user_answers[self.current_question] = self.selected_option.get()
        
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.display_question()
        else:
            self.submit_quiz()
    
    def previous_question(self):
        """Go to previous question"""
        # Save current answer
        if self.selected_option.get() != -1:
            self.user_answers[self.current_question] = self.selected_option.get()
        
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()
    
    def submit_quiz(self):
        """Submit quiz and show results"""
        # Save current answer
        if self.selected_option.get() != -1:
            self.user_answers[self.current_question] = self.selected_option.get()
        
        # Check if all questions are answered
        unanswered = [i+1 for i, ans in enumerate(self.user_answers) if ans is None]
        if unanswered:
            if not messagebox.askyesno("Unanswered Questions", 
                                     f"You have not answered questions: {', '.join(map(str, unanswered))}.\n\nDo you want to submit anyway?"):
                return
        
        # Calculate score
        self.calculate_score()
        self.show_results()
    
    def calculate_score(self):
        """Calculate final score"""
        self.score = 0
        for i, (user_ans, question) in enumerate(zip(self.user_answers, self.questions)):
            if user_ans is not None and user_ans == question["correct"]:
                self.score += 1
    
    def show_results(self):
        """Display quiz results"""
        total_questions = len(self.questions)
        percentage = (self.score / total_questions) * 100
        
        # Update score label
        self.score_label.config(text=f"Score: {self.score}/{total_questions} ({percentage:.1f}%)")
        
        # Generate detailed results
        self.results_text.delete(1.0, tk.END)
        
        # Performance message
        if percentage >= 80:
            message = "🌟 Excellent work! You have a strong understanding of the material."
        elif percentage >= 60:
            message = "👍 Good job! You have a solid grasp of most concepts."
        elif percentage >= 40:
            message = "📚 Not bad, but there's room for improvement. Keep studying!"
        else:
            message = "💪 Don't give up! Review the material and try again."
        
        self.results_text.insert(tk.END, f"{message}\n\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "DETAILED RESULTS:\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Question by question breakdown
        for i, (question, user_ans) in enumerate(zip(self.questions, self.user_answers)):
            self.results_text.insert(tk.END, f"Question {i+1}: {question['question']}\n")
            
            # Show options with indicators
            for j, option in enumerate(question["options"]):
                prefix = ""
                if j == question["correct"]:
                    prefix = "✓ "  # Correct answer
                elif j == user_ans:
                    prefix = "✗ "  # User's wrong answer
                else:
                    prefix = "  "
                
                self.results_text.insert(tk.END, f"{prefix}{chr(65+j)}. {option}\n")
            
            # Show result
            if user_ans is None:
                self.results_text.insert(tk.END, "❌ Not answered\n")
            elif user_ans == question["correct"]:
                self.results_text.insert(tk.END, "✅ Correct!\n")
            else:
                self.results_text.insert(tk.END, "❌ Incorrect\n")
            
            # Show explanation if available
            if "explanation" in question:
                self.results_text.insert(tk.END, f"💡 Explanation: {question['explanation']}\n")
            
            self.results_text.insert(tk.END, "\n" + "-" * 50 + "\n\n")
        
        self.show_results_screen()
    
    def restart_quiz(self):
        """Restart the quiz with same questions"""
        self.start_quiz()
    
    def load_questions_from_file(self):
        """Load questions from JSON file"""
        file_path = filedialog.askopenfilename(
            title="Select Questions File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    loaded_questions = json.load(file)
                
                # Validate question format
                if self.validate_questions(loaded_questions):
                    self.questions = loaded_questions
                    self.user_answers = [None] * len(self.questions)
                    messagebox.showinfo("Success", f"Loaded {len(self.questions)} questions successfully!")
                else:
                    messagebox.showerror("Error", "Invalid question format in the file!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load questions: {str(e)}")
    
    def validate_questions(self, questions):
        """Validate question format"""
        if not isinstance(questions, list):
            return False
        
        for q in questions:
            if not isinstance(q, dict):
                return False
            if "question" not in q or "options" not in q or "correct" not in q:
                return False
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                return False
            if not isinstance(q["correct"], int) or q["correct"] not in range(4):
                return False
        
        return True

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()