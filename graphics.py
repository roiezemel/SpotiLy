import tkinter as tk
from tkinter import ttk
import threading
from langdetect import detect


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, **kwargs)
        canvas = tk.Canvas(self, width=600, height=700)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollbar.focus()


class ScrollWindow:
    def __init__(self):
        self.root = None
        self.labelvar = None

    def start(self, on_thread):
        self.root = tk.Tk()

        frame = ScrollableFrame(self.root)
        self.labelvar = tk.StringVar()

        ttk.Label(frame.scrollable_frame,
                  textvariable=self.labelvar, font=("Arial", 16)).pack(padx=10, pady=10)

        frame.pack()

        threading.Thread(target=on_thread).start()

        self.root.mainloop()

    def set_lines(self, song_name, lines):
        self.root.title(song_name)
        self.labelvar.set('\n'.join(lines))


class ScrollWindow2:
    def __init__(self):
        self.root = None
        self.textbox = None

    def start(self, on_thread):
        self.root = tk.Tk()

        # self.root.geometry("600x700")
        self.root.configure(bg='pink')

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.configure(bg='black')

        self.textbox = tk.Text(self.root, font=("Ariel", 16), width=50, height=30, borderwidth=0)
        self.textbox.pack(fill=tk.Y, padx=10, pady=10)
        self.textbox.configure(bg='pink', fg='black')

        self.textbox.tag_configure('english', justify='left')
        self.textbox.tag_configure('hebrew', justify='right')

        self.textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.textbox.yview)

        threading.Thread(target=on_thread).start()

        self.root.mainloop()

    def set_lines(self, song_name, lines):
        self.root.title(song_name)
        self.textbox.delete("1.0", tk.END)
        lang = 'hebrew' if detect(song_name) == 'he' else 'english'
        for line in lines:
            self.textbox.insert(tk.END, line + '\n')
        self.textbox.tag_add(lang, "1.0", "end")
