import tkinter as tk
from tkinter import scrolledtext
import sympy as sp
from transformers import pipeline
import os

# Set up environment variables to manage warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Define a custom cache directory for transformers
cache_dir = "./model_cache"

# Initialize the NLP pipeline (cached locally)
nlp = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", cache_dir=cache_dir, device=0)

def ai_calculator(question):
    try:
        # First, attempt to evaluate the expression directly
        result = eval(question)
        return result
    except:
        # If eval fails, fall back to the previous logic
        if "plus" in question or "minus" in question or "times" in question or "divided by" in question:
            expression = question.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
            try:
                result = eval(expression)
                return result
            except:
                return "Invalid input for arithmetic operation."

        if "square root" in question:
            number_str = ''.join(filter(str.isdigit, question))
            if number_str:
                number = int(number_str)
                return sp.sqrt(number)
            else:
                return "Invalid input for square root."

        elif "factorial" in question:
            number_str = ''.join(filter(str.isdigit, question))
            if number_str:
                number = int(number_str)
                return sp.factorial(number)
            else:
                return "Invalid input for factorial."

        elif "to the power of" in question:
            parts = question.split()
            base_str = ''.join(filter(str.isdigit, parts[0]))
            exp_str = ''.join(filter(str.isdigit, parts[-1]))
            if base_str and exp_str:
                base = int(base_str)
                exponent = int(exp_str)
                return sp.Pow(base, exponent)
            else:
                return "Invalid input for power calculation."

        return "Sorry, I can't understand the question."

def send_message():
    user_message = entry_field.get()
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_message + "\n")
    entry_field.delete(0, tk.END)
    
    # Get AI response
    ai_response = ai_calculator(user_message)
    chat_window.insert(tk.END, "AI: " + str(ai_response) + "\n\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)  # Scroll to the bottom

# Setting up the GUI window
window = tk.Tk()
window.title("AI Chat Interface")
window.geometry("600x500")

# Chat window
chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20, font=("Arial", 12))
chat_window.config(state=tk.DISABLED)
chat_window.pack(pady=10)

# Entry field for user input
entry_field = tk.Entry(window, width=70, font=("Arial", 14))
entry_field.pack(pady=10)

# Send button
send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 14))
send_button.pack(pady=10)

# Bind Enter key to send message
window.bind('<Return>', lambda event: send_message())

# Run the GUI loop
window.mainloop()
