import tkinter as tk
from tkinter import ttk, messagebox
import string

COMMON_PASSWORDS = {
    '123456', 'password', '12345678', 'qwerty', '123456789',
    '12345', '1234', '111111', '1234567', 'dragon',
    '123123', 'baseball', 'abc123', 'football', 'monkey'
}

def validate_password(password):
    errors = []

    # Check for spaces
    if ' ' in password:
        errors.append("❌ Password must not contain spaces.")
    if password.strip() != password:
        errors.append("❌ No leading or trailing spaces allowed.")

    # Count special characters and digits
    num_digits = sum(c.isdigit() for c in password)
    num_specials = sum(c in string.punctuation for c in password)

    if num_digits > 5:
        errors.append("❌ No more than 5 digits allowed.")
    if num_specials > 5:
        errors.append("❌ No more than 5 special characters allowed.")

    return errors

def check_password_strength(password):
    suggestions = []
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("➡ Use at least 12 characters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("➡ Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("➡ Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("➡ Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        suggestions.append("➡ Add special characters.")

    if password.lower() in COMMON_PASSWORDS:
        suggestions.append("❌ This password is too common.")
        score = 0

    if score >= 6:
        return "✅ Strength: STRONG", "#28a745", []
    elif score >= 4:
        return "⚠️ Strength: MODERATE", "#ffc107", suggestions
    else:
        return "❌ Strength: WEAK", "#dc3545", suggestions

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_btn.config(text='Hide')
    else:
        password_entry.config(show='*')
        toggle_btn.config(text='Show')

def on_check():
    pwd = password_var.get()
    result_label.config(text="", fg="black")
    suggestion_box.delete(0, tk.END)

    if not pwd:
        messagebox.showerror("Input Error", "Please enter a password.")
        return

    validation_errors = validate_password(pwd)
    if validation_errors:
        result_label.config(text="🚫 INVALID PASSWORD", fg="red")
        for e in validation_errors:
            suggestion_box.insert(tk.END, e)
        return

    strength, color, suggestions = check_password_strength(pwd)
    result_label.config(text=strength, fg=color)

    for s in suggestions:
        suggestion_box.insert(tk.END, s)

# GUI Setup
root = tk.Tk()
root.title("Advanced Password Strength Checker")
root.geometry("520x500")
root.resizable(False, False)
root.configure(bg='#eef2f3')

title = tk.Label(root, text="🔐 Password Strength Checker", font=("Helvetica", 18, "bold"), bg="#eef2f3", fg="#222")
title.pack(pady=20)

frame = tk.Frame(root, bg="#eef2f3")
frame.pack(pady=10)

password_var = tk.StringVar()
password_entry = ttk.Entry(frame, textvariable=password_var, show="*", font=("Helvetica", 13), width=32)
password_entry.grid(row=0, column=0, padx=10)

toggle_btn = ttk.Button(frame, text="Show", command=toggle_password)
toggle_btn.grid(row=0, column=1)

# 3D-like Button Styling
style = ttk.Style()
style.configure("TButton", relief="raised", padding=6, font=("Helvetica", 11, "bold"))

check_btn = ttk.Button(root, text="Check Password", style="TButton", command=on_check)
check_btn.pack(pady=15)

result_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), bg="#eef2f3")
result_label.pack()

# Feedback Section with Padding
feedback_frame = tk.Frame(root, bg="#eef2f3", padx=15, pady=10)
feedback_frame.pack(pady=(10, 0), fill="x")

tk.Label(feedback_frame, text="Feedback & Suggestions:", font=("Helvetica", 12, "bold"), bg="#eef2f3").pack(anchor="w", pady=(0, 5))

suggestion_box = tk.Listbox(
    feedback_frame,
    width=65,
    height=8,
    font=("Courier", 10),
    bg="#fff",
    borderwidth=2,
    relief="groove",
    highlightthickness=0,
    selectbackground="#dbeafe"
)
suggestion_box.pack(pady=5, padx=5, fill="both")


footer = tk.Label(root, text="© 2025 SecureSoft Lab | MIT ICT932", bg="#eef2f3", font=("Arial", 9), fg="#666")
footer.pack(side="bottom", pady=10)

root.mainloop()
