import os
import random
import csv
import tkinter as tk
from tkinter import PhotoImage
import time  

class MomentOfTruthApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Moment of Truth")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        top_frame = tk.Frame(self.root, bg="#F8EFE4", height=40)
        top_frame.pack(fill="x", side="top", anchor="nw")
        
        exit_button = tk.Button(
            top_frame, text="x", font=("Helvetica", 14, "bold"), bg="#e42256", fg="#ffffff", 
            command=self.root.destroy, relief="flat", bd=0
        )
        exit_button.pack(side="right", padx=5)

        minimize_button = tk.Button(
            top_frame, text="–", font=("Helvetica", 14, "bold"), bg="#00b1b0", fg="#ffffff", 
            command=self.root.iconify, relief="flat", bd=0
        )
        minimize_button.pack(side="right", padx=5)

        self.level_frame = tk.Frame(self.root, bg="#F8EFE4")
        self.level_frame.pack(fill="both", expand=True)

        self.rules_frame = tk.Frame(self.root, bg="#F8EFE4")
        self.table_frame = tk.Frame(self.root, bg="#F8EFE4")
        self.leaderboard_frame = tk.Frame(self.root, bg="#F8EFE4")

        self.games_history_folder = "games_history"
        if not os.path.exists(self.games_history_folder):
            os.makedirs(self.games_history_folder)

        self.init_level_selection()
        self.root.mainloop()

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        return "break"

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        return "break"

    def init_level_selection(self):
        for widget in self.level_frame.winfo_children():
            widget.destroy()
        self.level_frame.pack(fill="both", expand=True)
        self.table_frame.pack_forget()
        self.rules_frame.pack_forget()
        self.leaderboard_frame.pack_forget()

        logo_path = os.path.join('graphics', 'logo.png')
        logo = PhotoImage(file=logo_path)

        main_frame = tk.Frame(self.level_frame, bg="#F8EFE4")
        main_frame.place(relx=0.75, rely=0.5, anchor='center')

        button_properties = {"font": ("Helvetica", 18), "fg": "#ffffff", "relief": "flat", "bd": 0, "height": 2, "width": 15, "borderwidth": 1}

        def on_enter(e, button, hover_color):
            button.config(bg=hover_color)

        def on_leave(e, button, original_color):
            button.config(bg=original_color)

        for idx, (level, color) in enumerate([("LEADERBOARD", "#4CAF50"), ("HOW TO PLAY", "#4CAF50"), ("EASY", "#ff8370"), ("NORMAL", "#fec84d"), ("HARD", "#e42256")]):
            def button_command(level=level, color=color):
                if level == "HOW TO PLAY":
                    self.show_how_to_play()
                elif level == "LEADERBOARD":
                    self.show_leaderboard()
                else:
                    self.generate_truth_table(level, color)

            button = tk.Button(
                main_frame,
                text=level,
                command=button_command,
                **button_properties,
                bg=color
            )

            button.grid(row=idx + 1, column=0, pady=10)
            button.bind("<Enter>", lambda e, b=button, c=color: on_enter(e, b, self.darker_color(c)))
            button.bind("<Leave>", lambda e, b=button, c=color: on_leave(e, b, c))

        logo_label = tk.Label(self.level_frame, image=logo, bg="#F8EFE4")
        logo_label.image = logo  
        logo_label.place(relx=0.33, rely=0.5, anchor='center')

    def darker_color(self, color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(int(c * 0.8) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)

    def show_how_to_play(self): 
        self.level_frame.pack_forget()  
        for widget in self.rules_frame.winfo_children():
            widget.destroy()  
        self.rules_frame.pack(fill="both", expand=True)  

        self.rules_frame.config(bg="#F8EFE4")

        mechanics_image_path = os.path.join('graphics', 'mechanics.png')
        mechanics_image = PhotoImage(file=mechanics_image_path)

        bg_label = tk.Label(self.rules_frame, image=mechanics_image, bg="#F8EFE4")
        bg_label.image = mechanics_image  
        bg_label.place(relwidth=1, relheight=1)  

        back_button = tk.Button(
            self.rules_frame, 
            text="← Back", 
            font=("Helvetica", 14, "bold"), 
            bg="#00b1b0", 
            fg="#ffffff", 
            command=self.init_level_selection, 
            relief="flat", 
            bd=0
        )
        back_button.pack(anchor="nw", padx=20, pady=20)

    def show_leaderboard(self):
        self.level_frame.pack_forget()
        self.rules_frame.pack_forget()
        self.table_frame.pack_forget()

        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()

        self.leaderboard_frame.pack(fill="both", expand=True)

        back_button = tk.Button(
            self.leaderboard_frame, 
            text="← Back", 
            font=("Helvetica", 14, "bold"), 
            bg="#00b1b0", 
            fg="#ffffff", 
            command=self.init_level_selection, 
            relief="flat", 
            bd=0
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        title_label = tk.Label(
            self.leaderboard_frame, 
            text="LEADERBOARD",
            font=("Helvetica", 24, "bold"), 
            bg="#F8EFE4", 
            fg="#404040", 
            anchor="center"
        )
        title_label.pack(pady=(20, 10))

        leaderboard_container = tk.Frame(self.leaderboard_frame, bg="#F8EFE4")
        leaderboard_container.pack(padx=30, pady=20, fill="both", expand=True)  

        leaderboard_data = self.load_leaderboard_data()

        level_colors = {
            "EASY": "#ff8370",
            "NORMAL": "#fec84d",
            "HARD": "#e42256"
        }

        for i, (level, scores) in enumerate(leaderboard_data.items()):
            table_frame = tk.Frame(leaderboard_container, bg=level_colors.get(level, "#F8EFE4"), width=500)
            table_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew") 

            level_label = tk.Label(
                table_frame, 
                text=f"{level} LEVEL",  
                font=("Helvetica", 18, "bold"), 
                bg=level_colors.get(level, "#F8EFE4"), 
                fg="#ffffff", 
                anchor="center"
            )
            level_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=3)  

            header_frame = tk.Frame(table_frame, bg=level_colors.get(level, "#F8EFE4"))
            header_frame.grid(row=1, column=0, padx=5, pady=5)  

            username_header = tk.Label(header_frame, text="PLAYER", font=("Helvetica", 12, "bold"), bg=level_colors.get(level, "#F8EFE4"), fg="#ffffff", anchor="w", width=18)
            username_header.grid(row=0, column=0, padx=5)

            score_header = tk.Label(header_frame, text="SCORE", font=("Helvetica", 12, "bold"), bg=level_colors.get(level, "#F8EFE4"), fg="#ffffff", anchor="w", width=8)
            score_header.grid(row=0, column=1, padx=5)

            time_header = tk.Label(header_frame, text="TIME", font=("Helvetica", 12, "bold"), bg=level_colors.get(level, "#F8EFE4"), fg="#ffffff", anchor="w", width=18)
            time_header.grid(row=0, column=2, padx=5)

            for j, score in enumerate(scores):
                score_frame = tk.Frame(table_frame, bg=level_colors.get(level, "#F8EFE4"))
                score_frame.grid(row=j+2, column=0, padx=5, pady=5)  

                username_label = tk.Label(score_frame, text=score[0], font=("Helvetica", 12), bg=level_colors.get(level, "#F8EFE4"), fg="#404040", anchor="w", width=18)
                username_label.grid(row=j, column=0, padx=5)

                score_label = tk.Label(score_frame, text=str(score[1]), font=("Helvetica", 12), bg=level_colors.get(level, "#F8EFE4"), fg="#404040", anchor="w", width=8)
                score_label.grid(row=j, column=1, padx=5)

                minutes, seconds = divmod(score[1], 60)
                time_label = tk.Label(score_frame, text=f"{minutes:02}:{seconds:02}", font=("Helvetica", 12), bg=level_colors.get(level, "#F8EFE4"), fg="#404040", anchor="w", width=18)
                time_label.grid(row=j, column=2, padx=5)

            if i < len(leaderboard_data) - 1:
                separator = tk.Frame(leaderboard_container, bg="#404040", width=3, height=300)
                separator.grid(row=0, column=i + 1, padx=10, pady=10, sticky="nsew")  

        leaderboard_container.grid_columnconfigure(0, weight=1)
        leaderboard_container.grid_columnconfigure(1, weight=1)
        leaderboard_container.grid_columnconfigure(2, weight=1)

    def load_leaderboard_data(self):
        leaderboard_data = {"EASY": [], "NORMAL": [], "HARD": []}
        
        for level in leaderboard_data.keys():
            level_folder = os.path.join(self.games_history_folder, level.lower())
            
            if not os.path.exists(level_folder):
                print(f"Level folder {level_folder} does not exist.")
                continue
            
            for file in os.listdir(level_folder):
                if file.endswith(".csv"):
                    file_path = os.path.join(level_folder, file)
                    print(f"Reading file: {file_path}")
                    
                    with open(file_path, newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader) 
                        
                        for row in reader:
                            player_name, score, time = row
                            leaderboard_data[level].append((player_name, int(score), time))
        
        for level in leaderboard_data:
            leaderboard_data[level].sort(key=lambda x: (-x[1], x[2])) 
        
        return leaderboard_data

    def generate_truth_table(self, level, button_color):
        self.level_frame.pack_forget()
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.table_frame.pack(fill="both", expand=True)

        time_limit = {'EASY': 60, 'NORMAL': 90, 'HARD': 120}[level]

        level_folder = os.path.join('tables', level.lower())
        csv_files = [f for f in os.listdir(level_folder) if f.endswith('.csv')]
        random_csv = random.choice(csv_files)
        csv_file_path = os.path.join(level_folder, random_csv)

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            table_data = list(reader)

        control_frame = tk.Frame(self.table_frame, bg="#ffffff")
        control_frame.pack(side="top", anchor="nw", padx=10, pady=10)

        back_button = tk.Button(control_frame, text="← Back", font=("Helvetica", 14, "bold"), bg="#00b1b0", fg="#ffffff", command=self.init_level_selection, relief="flat", bd=0)
        back_button.pack(side="left", padx=5)

        main_frame = tk.Frame(self.table_frame, bg="#F8EFE4")
        main_frame.place(relx=0.5, rely=0.6, anchor='center')  

        timer_label = tk.Label(self.table_frame, text="00:00", font=("Digital-7", 60), bg="#F8EFE4", fg="#404040")
        timer_label.pack(side="top", anchor="n", pady=(20, 10))  

        table_frame = tk.Frame(main_frame, bg="#cccccc", relief="ridge", bd=2)
        table_frame.grid(row=1, column=0, pady=20, sticky="nsew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        entries = {}
        blanks = []

        exclude_columns = [0, 1, 2]

        for i, row in enumerate(table_data):
            if i == len(table_data) - 1:
                continue
            for j, cell in enumerate(row):
                if i == 0 or j in exclude_columns:
                    continue
                if random.random() < 0.5:
                    blanks.append((i, j))
                    table_data[i][j] = '__'

        for i, row in enumerate(table_data):
            for j, cell in enumerate(row):
                if i == 0:
                    bg_color = button_color
                    fg_color = "#ffffff"
                    font_style = ("Helvetica", 14, "bold")
                else:
                    bg_color = "#f9f9f9" if i % 2 == 0 else "#eeeeee"
                    fg_color = "#000000"
                    font_style = ("Helvetica", 14)

                if cell == '__':
                    entry = tk.Entry(table_frame, width=10, font=font_style, justify="center", relief="groove", bd=1)
                    entry.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                    entries[(i, j)] = entry
                else:
                    label = tk.Label(
                        table_frame,
                        text=cell,
                        width=15,
                        height=2,
                        font=font_style,
                        bg=bg_color,
                        fg=fg_color,
                        relief="ridge",
                        borderwidth=1,
                        anchor="center"
                    )
                    label.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")

                table_frame.grid_rowconfigure(i, weight=1)
                table_frame.grid_columnconfigure(j, weight=1)

        result_label = tk.Label(main_frame, text="", font=("Helvetica", 20), bg="#F8EFE4")
        result_label.grid(row=2, column=0, columnspan=6, pady=20, sticky="nsew")

        start_time = time.time()
        self.timer_running = None

        def check_answers():
            if self.timer_running:
                self.root.after_cancel(self.timer_running)

            correct_count = 0
            any_incorrect = False

            for (row_idx, col_idx), entry in entries.items():
                entry.config(bg="white")

            for (row_idx, col_idx), entry in entries.items():
                user_answer = entry.get().strip().upper()
                correct_value = table_data[row_idx + 1][col_idx].upper()

                if correct_value == '__' and user_answer in ['T', 'F']:
                    entry.config(bg="lightgreen")
                    correct_count += 1
                elif user_answer == correct_value:
                    entry.config(bg="lightgreen")
                    correct_count += 1
                else:
                    entry.config(bg="red")
                    any_incorrect = True

            result_label.config(bg="#F8EFE4", font=("Helvetica", 14), width=50, height=3)

            if any_incorrect:
                result_label.config(text="Oops! Some answers are incorrect.", fg="#e42256")
            else:
                result_label.config(text="Congratulations! All answers are correct.", fg="#00b1b0")

            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_taken = f"{minutes:02}:{seconds:02}"
            result_label.config(text=f"{result_label.cget('text')}\nTime taken: {time_taken}")

            self.show_name_entry_popup(correct_count, start_time, level)

        def countdown():
            nonlocal time_limit
            minutes, seconds = divmod(time_limit, 60)
            time_str = f"{minutes:02}:{seconds:02}"

            if time_limit > 0:
                time_limit -= 1
                timer_label.config(text=time_str)
                self.timer_running = self.root.after(1000, countdown)
            else:
                check_answers()

        countdown()

        submit_button = tk.Button(main_frame, text="Submit", command=check_answers, font=("Helvetica", 18), bg="#e42256", fg="#ffffff", relief="flat", bd=0, height=1, width=15, borderwidth=1)
        submit_button.grid(row=3, column=0, columnspan=6, pady=15)

    def show_name_entry_popup(self, score, start_time, level):
        popup = tk.Toplevel(self.root)
        popup.title("LEVEL CLEAR")
        popup.geometry("300x150")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        popup_width = 400
        popup_height = 200

        position_top = int((screen_height - popup_height) / 2)
        position_left = int((screen_width - popup_width) / 2)

        popup.geometry(f"{popup_width}x{popup_height}+{position_left}+{position_top}")
        
        popup.grab_set()

        tk.Label(popup, text="\nSEE YOU ON THE LEADERBOARD!\nPLEASE ENTER YOUR NAME:", fg="#4CAF50", font=("Helvetica", 14)).pack(pady=10)

        name_entry = tk.Entry(popup, font=("Helvetica", 20), width=20, justify="center")
        name_entry.pack(pady=5, anchor = 'center')

        def submit_name():
            player_name = name_entry.get().strip()
            if player_name:
                popup.destroy()
                self.submit_game(player_name, score, start_time, level)
                self.show_leaderboard()
            else:
                tk.Label(popup, text="Name cannot be empty!", font=("Helvetica", 10), fg="red").pack(pady=5)

        submit_button = tk.Button(popup, text="SAVE", command=submit_name, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat")
        submit_button.pack(pady=10)


    def submit_game(self, player_name, score, start_time, level):
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        time_taken = f"{minutes:02}:{seconds:02}"

        level_folder = os.path.join(self.games_history_folder, level.lower())
        
        if not os.path.exists(level_folder):
            os.makedirs(level_folder)

        file_name = f"{level}_{player_name}_{time_taken.replace(':', '-')}.csv"
        games_history_file = os.path.join(level_folder, file_name)

        if not os.path.exists(games_history_file):
            with open(games_history_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Player", "Score", "Time"])  

        with open(games_history_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([player_name, score, time_taken])  

        print(f"Game history saved: {player_name}, {score}, {time_taken}")


if __name__ == "__main__":
    app = MomentOfTruthApp()