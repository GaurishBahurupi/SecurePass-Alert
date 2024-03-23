import tkinter as tk
from tkinter import messagebox
import hashlib

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Checker")
        self.root.geometry("300x200")

        self.title_label = tk.Label(root, text="Made by Gaurish", font=("Helvetica", 14, "bold"))
        self.title_label.pack(pady=10)

        self.password_label = tk.Label(root, text="Enter your password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.check_button = tk.Button(root, text="Check Password", command=self.check_password)
        self.check_button.pack()

    def check_password(self):
        password = self.password_entry.get()

        # Calculate SHA-1 hash of the password
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()

        # Fetch the first 5 characters of the hash
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        # Make request to Pwned Passwords API
        response = self.check_pwned_passwords(prefix)

        # Check if the suffix exists in the response
        if suffix in response:
            count = int(response[suffix])
            if count > 0:
                messagebox.showwarning("Password Check", f"This password has been found {count} times in data breaches. Please choose a different password.")
            else:
                messagebox.showinfo("Password Check", "This password has not been found in data breaches. You're good to go!")
        else:
            messagebox.showinfo("Password Check", "This password has not been found in data breaches. You're good to go!")

    def check_pwned_passwords(self, prefix):
        import requests
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code == 200:
            response_text = response.text
            passwords = response_text.split('\n')
            password_dict = {p.split(':')[0]: p.split(':')[1] for p in passwords if p}
            return password_dict
        else:
            messagebox.showerror("Error", "Could not connect to the Pwned Passwords service.")
            return {}

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()
