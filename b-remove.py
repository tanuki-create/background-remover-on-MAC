import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
from rembg import remove

class BatchRemovalApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("640x360")
        self.root.title("Batch Background Removal Tool")

        self.setup_style()

        self.named_directory_in = tk.StringVar(value=self.load_default("default_in.txt"))
        self.named_directory_out = tk.StringVar(value=self.load_default("default_out.txt"))

        self.setup_widgets()

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # ボタンスタイル
        style.configure('TButton', font=('Helvetica', 10), background='#89CFF0')

        # ラベルスタイル
        style.configure('TLabel', font=('Helvetica', 12), background='#89CFF0')

        # プログレスバースタイル
        style.configure('Horizontal.TProgressbar', background='#89CFF0', troughcolor='white', bordercolor='gray', lightcolor='#89CFF0', darkcolor='#89CFF0')

        # GUI背景色
        self.root.configure(background='#89CFF0')

    def setup_widgets(self):
        ttk.Label(self.root, text="Batch Background Removal Tool", font=("Helvetica", 16, 'bold')).grid(row=0, column=1, pady=10)

        # Input path selection
        ttk.Button(self.root, text="Choose Input Path", command=self.get_path_in).grid(row=1, column=0, sticky="EW", padx=10, pady=10)
        ttk.Label(self.root, textvariable=self.named_directory_in, relief="sunken").grid(row=1, column=1, sticky="EW", padx=10)
        ttk.Button(self.root, text="Set as Default", command=lambda: self.set_default("default_in.txt", self.named_directory_in)).grid(row=1, column=2, padx=10)

        # Output path selection
        ttk.Button(self.root, text="Choose Output Path", command=self.get_path_out).grid(row=2, column=0, sticky="EW", padx=10, pady=10)
        ttk.Label(self.root, textvariable=self.named_directory_out, relief="sunken").grid(row=2, column=1, sticky="EW", padx=10)
        ttk.Button(self.root, text="Set as Default", command=lambda: self.set_default("default_out.txt", self.named_directory_out)).grid(row=2, column=2, padx=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(row=3, column=1, pady=10)

        # 完了ラベルの追加
        self.completion_label = ttk.Label(self.root, text="", font=("Helvetica", 10))
        self.completion_label.grid(row=4, column=1, pady=10)

        # Start and Quit buttons
        ttk.Button(self.root, text="Start Background Removal Tool", command=self.start_thread).grid(row=4, column=1, pady=10)
        ttk.Button(self.root, text="Quit", command=self.root.destroy).grid(row=5, column=1, pady=10)

    def load_default(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return file.read()
        return ""

    def set_default(self, file_name, path_variable):
        with open(file_name, "w") as file:
            file.write(path_variable.get())

    def get_path_in(self):
        self.named_directory_in.set(filedialog.askdirectory())

    def get_path_out(self):
        self.named_directory_out.set(filedialog.askdirectory())

    def start_thread(self):
        # スレッドの開始前にGUIをリセット
        self.completion_label['text'] = ""  
        self.progress_bar['value'] = 0
        threading.Thread(target=self.run_batch_removal_tool, daemon=True).start()

    def run_batch_removal_tool(self):
        pic_list = os.listdir(self.named_directory_in.get())
        total = len(pic_list)
        self.progress_bar['maximum'] = total
        save_number = 0

        for pic in pic_list:
            save_number += 1
            input_path = os.path.join(self.named_directory_in.get(), pic)
            output_path = os.path.join(self.named_directory_out.get(), f'no_bg{save_number}.png')

            if os.path.exists(output_path):
                continue

            try:
                input_image = Image.open(input_path)
                output = remove(input_image)
                output.save(output_path)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process {pic}: {e}"))
                return

            # GUIの更新（プログレスバーの進捗）
            self.root.after(0, lambda value=save_number: self.update_progress_bar(value))

        # 処理完了後のGUI更新
        self.root.after(0, self.update_completion_label)

    def update_progress_bar(self, value):
        self.progress_bar['value'] = value

    def update_completion_label(self):
        self.completion_label['text'] = "Complete"
