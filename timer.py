import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import winsound  # Для звукового оповещения

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Timer")
        self.root.geometry("700x550")
        self.root.configure(bg="#2e3f4f")

        # Создание меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить состояние", command=self.save_state)
        file_menu.add_command(label="Загрузить состояние", command=self.load_state)
        menubar.add_cascade(label="Файл", menu=file_menu)

        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Темная тема", command=self.set_dark_theme)
        theme_menu.add_command(label="Светлая тема", command=self.set_light_theme)
        menubar.add_cascade(label="Тема", menu=theme_menu)

        # Стилизация
        self.style = ttk.Style()
        self.set_dark_theme()  # Установить темную тему по умолчанию

        # Метка времени
        self.time_label = ttk.Label(root, text="00:00:00")
        self.time_label.pack(pady=20)

        # Метка текущего времени
        self.current_time_label = ttk.Label(root, text="")
        self.current_time_label.pack(pady=5)
        self.update_current_time()

        # Поле ввода для настраиваемого времени
        self.entry = ttk.Entry(root, justify='center')
        self.entry.pack(pady=10)

        # Кнопки управления
        self.start_button = ttk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.pause_button = ttk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(pady=5)

        self.reset_button = ttk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=5)

        # Инициализация переменных состояния
        self.running = False
        self.paused = False
        self.start_time = None
        self.end_time = None
        self.elapsed_time = timedelta()

    def set_dark_theme(self):
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#2e3f4f", foreground="#ffffff", font=('Helvetica', 48))
        self.style.configure("TButton", font=('Helvetica', 24), background="#4e5d6c", foreground="#ffffff")
        self.style.configure("TEntry", font=('Helvetica', 24))
        self.root.configure(bg="#2e3f4f")

    def set_light_theme(self):
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#ffffff", foreground="#000000", font=('Helvetica', 48))
        self.style.configure("TButton", font=('Helvetica', 24), background="#ffffff", foreground="#000000")
        self.style.configure("TEntry", font=('Helvetica', 24))
        self.root.configure(bg="#ffffff")

    def update_current_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {now}")
        self.root.after(1000, self.update_current_time)

    def start_timer(self):
        if not self.running:
            if self.paused:
                self.start_time = datetime.now() - self.elapsed_time
            else:
                try:
                    minutes = int(self.entry.get())
                    self.end_time = datetime.now() + timedelta(minutes=minutes)
                except ValueError:
                    self.time_label.config(text="Invalid input!")
                    return
                self.start_time = datetime.now()
            self.running = True
            self.paused = False
            self.update_timer()

    def pause_timer(self):
        if self.running:
            self.elapsed_time = datetime.now() - self.start_time
            self.running = False
            self.paused = True

    def stop_timer(self):
        if self.running or self.paused:
            self.elapsed_time = datetime.now() - self.start_time
            self.running = False
            self.paused = False
            self.show_completion_message()

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.start_time = None
        self.end_time = None
        self.elapsed_time = timedelta()
        self.time_label.config(text="00:00:00")

    def update_timer(self):
        if self.running:
            now = datetime.now()
            if self.end_time:
                remaining_time = self.end_time - now
                if remaining_time.total_seconds() > 0:
                    self.time_label.config(text=str(remaining_time).split('.')[0])
                else:
                    self.time_label.config(text="00:00:00")
                    self.running = False
                    self.show_completion_message()
                    self.play_sound()
                    return
            else:
                elapsed_time = now - self.start_time
                self.time_label.config(text=str(elapsed_time).split('.')[0])
            self.root.after(1000, self.update_timer)

    def show_completion_message(self):
        messagebox.showinfo("Timer", "Time's up!")

    def play_sound(self):
        winsound.Beep(1000, 1000)  # Частота 1000 Гц, длительность 1000 мс

    def save_state(self):
        state = {
            'running': self.running,
            'paused': self.paused,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'elapsed_time': str(self.elapsed_time),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None
        }
        with open('timer_state.json', 'w') as f:
            json.dump(state, f)
        messagebox.showinfo("Timer", "State saved successfully!")

    def load_state(self):
        try:
            with open('timer_state.json', 'r') as f:
                state = json.load(f)
            self.running = state['running']
            self.paused = state['paused']
            self.start_time = datetime.strptime(state['start_time'], '%Y-%m-%d %H:%M:%S') if state['start_time'] else None
            self.elapsed_time = timedelta(seconds=float(state['elapsed_time'].split(':')[2]))
            self.end_time = datetime.strptime(state['end_time'], '%Y-%m-%d %H:%M:%S') if state['end_time'] else None
            if self.running:
                self.update_timer()
            messagebox.showinfo("Timer", "State loaded successfully!")
        except Exception as e:
            messagebox.showerror("Timer", f"Failed to load state: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
