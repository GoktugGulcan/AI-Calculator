import re
import tkinter as tk
from tkinter import scrolledtext
import sympy as sp

def ai_calculator(question):
    question_lower = question.lower().strip()

    # General Greetings and Identification
    if any(greet in question_lower for greet in ["hi", "hello", "hey", "greetings"]):
        return "Hello! How can I assist you today?"

    if "who are you" in question_lower or "what are you" in question_lower:
        return "I am an AI assistant designed to help you with mathematical queries, general questions, and more!"

    # Arithmetic Handling
    try:
        arithmetic_match = re.search(r'(\d+\s*[\+\-\*/÷]\s*\d+(\s*[\+\-\*/÷]\s*\d+)*)', question_lower)
        if arithmetic_match:
            expression = arithmetic_match.group(1).replace('÷', '/')
            result = eval(expression)
            return f"The result is {result}"
    except Exception:
        pass

    # Handling sequence completion
    sequence_match = re.search(r'(find|calculate|determine) the (missing|next|following) term[s]? in (?:the )?(?:sequence of )?multiples? of (\d+):? (.*)', question_lower)
    if sequence_match:
        base = int(sequence_match.group(4))
        numbers = list(map(int, re.findall(r'\d+', sequence_match.group(5))))
        missing_term = numbers[-1] + base
        return f"The missing term is {missing_term}"

    # Handling prime number queries
    prime_match = re.search(r'(what is|find|calculate) the (next)? prime number (after|following)? (\d+)', question_lower)
    if prime_match:
        number = int(prime_match.group(4))
        next_prime = sp.nextprime(number)
        return f"The next prime number after {number} is {next_prime}"

    # General Mathematical Query Example: Solve 24÷8+2
    solve_match = re.search(r'(solve|calculate)\s*([\d\+\-\*/÷\s]+)', question_lower)
    if solve_match:
        expression = solve_match.group(2).replace('÷', '/')
        try:
            result = eval(expression)
            return f"The result is {result}"
        except Exception:
            return "I'm sorry, I couldn't process that calculation."

    return "I'm sorry, I couldn't understand that. Could you please rephrase your question?"

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
