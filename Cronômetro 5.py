import tkinter as tk
from tkinter import filedialog
import time

class CronometroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronômetro")
        self.root.geometry("400x500")
        self.root.configure(bg="#add8e6")

        # Variáveis do cronômetro
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.laps = []
        
        # Display do cronômetro
        self.time_label = tk.Label(root, text="00:00:00", font=("Arial", 30), bg="#add8e6")
        self.time_label.pack(pady=20)

        # Caixa de texto para registrar voltas
        self.text_area = tk.Text(root, width=40, height=10, state="disabled", bg="#f0f8ff")
        self.text_area.pack(pady=10)

        # Botões
        self.btn_iniciar = tk.Button(root, text="Iniciar", command=self.iniciar, bg="#32cd32", width=10)
        self.btn_iniciar.pack(pady=5)
        
        self.btn_parar = tk.Button(root, text="Parar", command=self.parar, bg="#ff4500", width=10)
        self.btn_parar.pack(pady=5)

        self.btn_reset = tk.Button(root, text="Reset", command=self.reset, bg="#ffa500", width=10)
        self.btn_reset.pack(pady=5)

        self.btn_volta = tk.Button(root, text="Volta", command=self.volta, bg="#1e90ff", width=10)
        self.btn_volta.pack(pady=5)

        self.btn_salvar = tk.Button(root, text="Salvar", command=self.salvar, bg="#9370db", width=10)
        self.btn_salvar.pack(pady=5)

        self.btn_sair = tk.Button(root, text="Sair", command=root.quit, bg="#dc143c", width=10)
        self.btn_sair.pack(pady=5)
        
        self.update_clock()

    def format_time(self, time_in_seconds):
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        centiseconds = int((time_in_seconds - int(time_in_seconds)) * 100)
        return f"{minutes:02}:{seconds:02}:{centiseconds:02}"

    def iniciar(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def parar(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.laps = []
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.configure(state="disabled")
        self.update_clock()

    def volta(self):
        if self.running:
            current_time = time.time() - self.start_time
            lap_time = current_time - sum(self.laps) if self.laps else current_time
            self.laps.append(lap_time)
            formatted_lap = self.format_time(lap_time)
            self.text_area.configure(state="normal")
            self.text_area.insert(tk.END, f"{formatted_lap}\n")
            self.text_area.configure(state="disabled")

    def salvar(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Arquivo de Texto", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.writelines(self.text_area.get("1.0", tk.END))

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        formatted_time = self.format_time(self.elapsed_time)
        self.time_label.config(text=formatted_time)
        self.root.after(10, self.update_clock)

# Inicializar a aplicação
root = tk.Tk()
app = CronometroApp(root)
root.mainloop()
