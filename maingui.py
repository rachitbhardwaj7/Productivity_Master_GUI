import tkinter as tk
from tkinter import messagebox, Canvas, Label, Entry, Button, Listbox
from PIL import Image, ImageTk
from datetime import datetime as dt, timedelta
import time
import os
import threading

main_root = tk.Tk()
image = Image.open("rengoku.jpg")
width, height = image.size
main_root.geometry(f"{width}x{height}")
main_root.maxsize(width, height)

class EntryPage(tk.Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Productivity App")
        image = Image.open("rengoku.jpg")
        self.width, self.height = image.size

        self.photo = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Labels
        username_label = Label(self, text="𝖀𝕾𝕰𝖱𝕹𝕬𝕸𝕰", bg="FIREBRICK")
        username_label.place(x=250, y=150)
        password_label = Label(self, text="𝕻𝕬𝖂𝕾𝕺𝕽𝕯", bg="FIREBRICK")
        password_label.place(x=250, y=200)

        # Entry fields
        self.username_entry = Entry(self, bg="firebrick")
        self.username_entry.place(x=350, y=150)
        self.password_entry = Entry(self, bg="FIREBRICK")
        self.password_entry.place(x=350, y=200)

        # Enter button
        entry_button = Button(self, text="𝕰𝕹𝕿𝕰𝕽", font=('Arial', 18), command=self.enter, bg="FIREBRICK", width=10, height=1)
        entry_button.place(x=300, y=250)

    def enter(self):
        # Destroy current widgets
        self.pack_forget()
        # Show feature page
        self.app.show_feature_page()

class FeaturePage(tk.Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        image = Image.open("download.jpg")
        self.photo = ImageTk.PhotoImage(image)
        self.width, self.height = image.size

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        feature_label = Label(self, bg="dark cyan", text="𝕱𝕰𝕬𝖀𝕿𝖀𝕽𝕰'𝕾", font="ARIAL,20")
        feature_label.place(x=300, y=0)
        self.feature1 = Button(self, bg="dark cyan", text="𝓑𝓛𝓞𝓒𝓚 𝓦𝓔𝓑𝓢𝓘𝓣𝓔", command=self.show_block_page, font="ARIAL,20", width=18, height=1)
        self.feature1.place(x=10, y=100)
        self.feature2 = Button(self, bg="dark cyan", text="𝓣𝓞-𝓓𝓞 𝓛𝓘𝓢𝓣", command=None, font="ARIAL,20", width=16, height=1)
        self.feature2.place(x=10, y=200)
        self.feature3 = Button(self, bg="dark cyan", text="𝓑𝓛𝓞𝓒𝓚 ~𝓐𝓟𝓟", command=None, font="ARIAL,20", width=14, height=1)
        self.feature3.place(x=10, y=300)
        self.feature4 = Button(self, bg="dark cyan", text="𝓐𝓘 ~ 𝓒𝓗𝓐𝓣-𝓑𝓞𝓣", command=None, font="ARIAL,20", width=18, height=1)
        self.feature4.place(x=10, y=400)

    def show(self):
        self.pack(fill="both", expand=True)

    def show_block_page(self):
        self.pack_forget()
        self.app.show_block_page()

class BlockPage(tk.Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        image = Image.open("ds.jpg")
        self.photo = ImageTk.PhotoImage(image)
        self.width, self.height = image.size

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Labels
        website_label = Label(self, text="Websites to Block (comma separated):", bg="dark cyan")
        website_label.place(x=10, y=20)
        duration_label = Label(self, text="Block Duration (minutes):", bg="dark cyan")
        duration_label.place(x=10, y=60)

        # Entry fields
        self.websites_entry = Entry(self, width=50, bg="light cyan")
        self.websites_entry.place(x=250, y=20)
        self.duration_entry = Entry(self, width=10, bg="light cyan")
        self.duration_entry.place(x=250, y=60)

        # Block button
        block_button = Button(self, text="Block", command=self.start_blocking, bg="dark cyan", width=10, height=1)
        block_button.place(x=200, y=100)

        # Listbox to show blocked websites
        self.blocked_websites_listbox = Listbox(self, width=50, height=10, bg="light cyan")
        self.blocked_websites_listbox.place(x=250, y=150)

        # Label to show remaining time
        self.remaining_time_label = Label(self, text="", bg="dark cyan")
        self.remaining_time_label.place(x=250, y=300)

        # Back button
        back_button = Button(self, text="Back", command=self.go_back, bg="dark cyan", width=10, height=1)
        back_button.place(x=300, y=500)

    def start_blocking(self):
        websites = self.websites_entry.get().strip()
        duration = self.duration_entry.get().strip()

        if not websites or not duration:
            messagebox.showerror("Error", "Please enter both websites and duration.")
            return

        try:
            duration = int(duration)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for duration.")
            return

        websites_list = [website.strip() for website in websites.split(",")]

        # Start the blocking process in a new thread
        threading.Thread(target=self.block_websites, args=(websites_list, duration)).start()
        messagebox.showinfo("Info", "Blocking started.")

    def block_websites(self, website_list, duration_minutes):
        ip_localmachine = "127.0.0.1"
        hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        start_time = "07:00:00"
        end_time = "21:00:00"

        try:
            if os.path.exists(hosts_path):
                os.chmod(hosts_path, 0o666)
            else:
                print("File not found:", hosts_path)
        except PermissionError:
            print("Permission denied: You don't have the necessary permissions to change the permissions of this file.")

        with open(hosts_path, "w") as file:
            new_content = ""
            file.write(new_content)

        now = dt.now()
        end_time_script = now + timedelta(minutes=duration_minutes)

        self.update_blocked_websites_listbox(website_list)
        self.update_remaining_time(end_time_script)

        while dt.now() < end_time_script:
            current_time = dt.now().strftime("%H:%M:%S")
            if start_time <= current_time <= end_time:
                with open(hosts_path, "r+") as file:
                    content = file.read()
                    for website in website_list:
                        if website not in content:
                            file.write(ip_localmachine + " " + website + "\n")
            else:
                with open(hosts_path, "r+") as file:
                    file.truncate(0)

            time.sleep(10)
            self.update_remaining_time(end_time_script)

        with open(hosts_path, "r+") as file:
            file.truncate(0)
        self.clear_blocked_websites_listbox()

    def update_blocked_websites_listbox(self, website_list):
        self.blocked_websites_listbox.delete(0, tk.END)
        for website in website_list:
            self.blocked_websites_listbox.insert(tk.END, website)

    def update_remaining_time(self, end_time_script):
        remaining_time = end_time_script - dt.now()
        self.remaining_time_label.config(text=f"Time left: {remaining_time}")

    def clear_blocked_websites_listbox(self):
        self.blocked_websites_listbox.delete(0, tk.END)
        self.remaining_time_label.config(text="")

    def go_back(self):
        self.pack_forget()
        self.app.show_feature_page()

    def show(self):
        self.pack(fill="both", expand=True)

class App:
    def __init__(self, root):
        self.root = root
        self.entry_page = EntryPage(master=self.root, app=self)
        self.entry_page.pack(fill="both", expand=True)

    def show_feature_page(self):
        self.entry_page.pack_forget()
        self.feature_page = FeaturePage(master=self.root, app=self)
        self.feature_page.show()

    def show_block_page(self):
        self.feature_page.pack_forget()
        self.block_page = BlockPage(master=self.root, app=self)
        self.block_page.show()

if __name__ == "__main__":
    app = App(main_root)
    main_root.mainloop()