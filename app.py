import tkinter as tk
from tkinter import scrolledtext, messagebox
import main

def analyze_code():
    code_snippet = text_area.get("1.0", tk.END).strip()
    if not code_snippet:
        messagebox.showwarning("Warning", "Please enter some code.")
        return
    
    readability_result = main.predict_readability(code_snippet)
    bug_result = main.check_bugs(code_snippet)
    complexity_result = main.measure_complexity(code_snippet)
    output_result = main.run_code(code_snippet)  # Assuming this function executes the code and returns output
    
    result_area.config(state=tk.NORMAL)
    result_area.delete("1.0", tk.END)
    result_area.insert(tk.END, f"Readability: {readability_result}\n\nBugs: {bug_result}\n\nComplexity:\n{complexity_result}")
    result_area.config(state=tk.DISABLED)
    
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, f"Output:\n{output_result}")
    output_area.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Code Readability & Bug Checker")
root.geometry("700x550")
root.configure(bg="#2C3E50")
root.state("zoomed")  # Start in full-screen mode

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# Header Label
tk.Label(root, text="Paste Your Code Below", font=("Arial", 14, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

# Code Input Area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Courier", 12), bg="#ECF0F1", fg="#2C3E50")
text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Analyze Button
analyze_btn = tk.Button(root, text="Analyze Code", font=("Arial", 14, "bold"), bg="#3498DB", fg="white", relief=tk.RAISED, padx=20, pady=5, command=analyze_code)
analyze_btn.pack(pady=15)

# Result and Output Display Side by Side
result_output_frame = tk.Frame(root, bg="#34495E", padx=10, pady=10)
result_output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Result Frame
tk.Label(result_output_frame, text="Analysis Result:", font=("Arial", 12, "bold"), fg="white", bg="#34495E").grid(row=0, column=0, sticky="w", padx=5, pady=5)
result_area = scrolledtext.ScrolledText(result_output_frame, wrap=tk.WORD, width=40, height=10, font=("Arial", 11), bg="#ECF0F1", fg="#2C3E50", state=tk.DISABLED)
result_area.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Output Frame
tk.Label(result_output_frame, text="Execution Output:", font=("Arial", 12, "bold"), fg="white", bg="#34495E").grid(row=0, column=1, sticky="w", padx=5, pady=5)
output_area = scrolledtext.ScrolledText(result_output_frame, wrap=tk.WORD, width=40, height=10, font=("Arial", 11), bg="#ECF0F1", fg="#2C3E50", state=tk.DISABLED)
output_area.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

result_output_frame.columnconfigure(0, weight=1)
result_output_frame.columnconfigure(1, weight=1)
result_output_frame.rowconfigure(1, weight=1)

root.mainloop()