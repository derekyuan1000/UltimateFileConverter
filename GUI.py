import tkinter as tk
from tkinter import ttk
import sv_ttk
import Conversions as info

class GUI:
    def __init__(self, ROOT) -> None:
        self.ROOT = ROOT
        self.ROOT.title("Ultimate File Converter")
        self.ROOT.geometry("700x800")
        self.ROOT.resizable(True, True)

        sv_ttk.set_theme("dark")

        MAIN_FRAME = ttk.Frame(self.ROOT, padding=20)
        MAIN_FRAME.pack(fill="both", expand=True)

        SINGLE_FRAME = ttk.LabelFrame(MAIN_FRAME, text="Single File Conversion", padding=20)
        SINGLE_FRAME.pack(fill="both", expand=True, pady=(0, 20))

        SINGLE_DESC = ttk.Label(
            SINGLE_FRAME,
            text="Convert a single file from one format to another. Select the source format, choose your file, select the target format, and click Convert.",
            wraplength=600,
            justify="left"
        )
        SINGLE_DESC.pack(anchor="w", pady=(0, 10), fill="x")

        SINGLE_FILE_ROW = ttk.Frame(SINGLE_FRAME)
        SINGLE_FILE_ROW.pack(fill="x", pady=5)
        self.chosen_files = tk.StringVar(value="")
        self.file_paths = []
        ttk.Label(SINGLE_FILE_ROW, text="Files:", width=15, anchor="w").pack(side="left")
        ttk.Entry(SINGLE_FILE_ROW, textvariable=self.chosen_files, state="readonly", width=40).pack(side="left", padx=(0, 10), fill="x", expand=True)
        ttk.Button(SINGLE_FILE_ROW, text="Browse...", command=lambda: self.controller.update_chosen_files()).pack(side="left")

        SINGLE_OUTPUT_ROW = ttk.Frame(SINGLE_FRAME)
        SINGLE_OUTPUT_ROW.pack(fill="x", pady=5)
        self.output_folder = tk.StringVar(value="")
        ttk.Label(SINGLE_OUTPUT_ROW, text="Output Folder:", width=15, anchor="w").pack(side="left")
        ttk.Entry(SINGLE_OUTPUT_ROW, textvariable=self.output_folder, state="readonly", width=40).pack(side="left", padx=(0, 10), fill="x", expand=True)
        ttk.Button(SINGLE_OUTPUT_ROW, text="Browse...", command=lambda: self.controller.update_output_folder()).pack(side="left")

        SINGLE_FROM_ROW = ttk.Frame(SINGLE_FRAME)
        SINGLE_FROM_ROW.pack(fill="x", pady=5)
        ttk.Label(SINGLE_FROM_ROW, text="From Format:", width=15, anchor="w").pack(side="left")
        self.SINGLE_FORMAT_FROM_BOX = ttk.Combobox(SINGLE_FROM_ROW, values=info.file_formats, state="readonly", width=20)
        self.SINGLE_FORMAT_FROM_BOX.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.SINGLE_FORMAT_FROM_BOX.bind('<<ComboboxSelected>>', lambda x: self.controller.update_to_format())

        SINGLE_TO_ROW = ttk.Frame(SINGLE_FRAME)
        SINGLE_TO_ROW.pack(fill="x", pady=5)
        ttk.Label(SINGLE_TO_ROW, text="To Format:", width=15, anchor="w").pack(side="left")
        self.SINGLE_FORMAT_TO_BOX = ttk.Combobox(SINGLE_TO_ROW, state="readonly", width=20)
        self.SINGLE_FORMAT_TO_BOX.pack(side="left", padx=(0, 10), fill="x", expand=True)

        SINGLE_PROGRESS_ROW = ttk.Frame(SINGLE_FRAME)
        SINGLE_PROGRESS_ROW.pack(fill="x", pady=10)
        ttk.Label(SINGLE_PROGRESS_ROW, text="Progress:", width=15, anchor="w").pack(side="left")
        self.SINGLE_FORMAT_PROGRESS_BAR = ttk.Progressbar(SINGLE_PROGRESS_ROW, orient="horizontal", length=300, mode="determinate")
        self.SINGLE_FORMAT_PROGRESS_BAR.pack(side="left", padx=(0, 10), fill="x", expand=True)

        SINGLE_BUTTON_ROW = ttk.Frame(SINGLE_FRAME)
        SINGLE_BUTTON_ROW.pack(fill="x", pady=(10, 0))
        ttk.Button(SINGLE_BUTTON_ROW, text="Convert", width=15,
                   command=lambda: self.controller.convert_single_files(self.file_paths)).pack(side="right")

        BATCH_FRAME = ttk.LabelFrame(MAIN_FRAME, text="Batch File Conversion", padding=20)
        BATCH_FRAME.pack(fill="both", expand=True, pady=(0, 20), ipadx=40)

        BATCH_DESC = ttk.Label(
            BATCH_FRAME,
            text="Convert multiple files of the same format and output as a folder with all your converted files.",
            wraplength=600,
            justify="left"
        )
        BATCH_DESC.pack(anchor="w", pady=(0, 10), fill="x")

        BATCH_FILE_ROW = ttk.Frame(BATCH_FRAME)
        BATCH_FILE_ROW.pack(fill="x", pady=5)
        self.batch_chosen_files = tk.StringVar(value="")
        self.batch_file_paths = []
        ttk.Label(BATCH_FILE_ROW, text="Files:", width=15, anchor="w").pack(side="left")
        ttk.Entry(BATCH_FILE_ROW, textvariable=self.batch_chosen_files, state="readonly", width=40).pack(side="left", padx=(0, 10), fill="x", expand=True)
        ttk.Button(BATCH_FILE_ROW, text="Browse...", command=lambda: self.controller.update_batch_chosen_files()).pack(side="left")

        BATCH_OUTPUT_ROW = ttk.Frame(BATCH_FRAME)
        BATCH_OUTPUT_ROW.pack(fill="x", pady=5)
        self.batch_output_folder = tk.StringVar(value="")
        ttk.Label(BATCH_OUTPUT_ROW, text="Output Folder:", width=15, anchor="w").pack(side="left")
        ttk.Entry(BATCH_OUTPUT_ROW, textvariable=self.batch_output_folder, state="readonly", width=40).pack(side="left", padx=(0, 10), fill="x", expand=True)
        ttk.Button(BATCH_OUTPUT_ROW, text="Browse...", command=lambda: self.controller.update_batch_output_folder()).pack(side="left")

        BATCH_FROM_ROW = ttk.Frame(BATCH_FRAME)
        BATCH_FROM_ROW.pack(fill="x", pady=5)
        ttk.Label(BATCH_FROM_ROW, text="From Format:", width=15, anchor="w").pack(side="left")
        self.BATCH_FORMAT_FROM_BOX = ttk.Combobox(BATCH_FROM_ROW, values=info.file_formats, state="readonly", width=20)
        self.BATCH_FORMAT_FROM_BOX.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.BATCH_FORMAT_FROM_BOX.bind('<<ComboboxSelected>>', lambda x: self.controller.update_batch_to_format())

        BATCH_TO_ROW = ttk.Frame(BATCH_FRAME)
        BATCH_TO_ROW.pack(fill="x", pady=5)
        ttk.Label(BATCH_TO_ROW, text="To Format:", width=15, anchor="w").pack(side="left")
        self.BATCH_FORMAT_TO_BOX = ttk.Combobox(BATCH_TO_ROW, state="readonly", width=20)
        self.BATCH_FORMAT_TO_BOX.pack(side="left", padx=(0, 10), fill="x", expand=True)

        BATCH_PROGRESS_ROW = ttk.Frame(BATCH_FRAME)
        BATCH_PROGRESS_ROW.pack(fill="x", pady=10)
        ttk.Label(BATCH_PROGRESS_ROW, text="Progress:", width=15, anchor="w").pack(side="left")
        self.BATCH_FORMAT_PROGRESS_BAR = ttk.Progressbar(BATCH_PROGRESS_ROW, orient="horizontal", length=300, mode="determinate")
        self.BATCH_FORMAT_PROGRESS_BAR.pack(side="left", padx=(0, 10), fill="x", expand=True)

        BATCH_BUTTON_ROW = ttk.Frame(BATCH_FRAME)
        BATCH_BUTTON_ROW.pack(fill="x", pady=(10, 0))
        ttk.Button(BATCH_BUTTON_ROW, text="Batch Convert", width=15,
                   command=lambda: self.controller.convert_batch_files(self.batch_file_paths)).pack(side="right")

        self.ROOT.bind("<F11>", self.toggle_fullscreen)
        self.ROOT.bind("<Escape>", self.exit_fullscreen)
        self.fullscreen = False

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.ROOT.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.ROOT.attributes("-fullscreen", False)

    def set_controller(self, controller):
        self.controller = controller

    def lock_from_format(self):
        self.SINGLE_FORMAT_FROM_BOX.config(state="disabled")

    def unlock_from_format(self):
        self.SINGLE_FORMAT_FROM_BOX.config(state="readonly")

    def lock_batch_from_format(self):
        self.BATCH_FORMAT_FROM_BOX.config(state="disabled")

    def unlock_batch_from_format(self):
        self.BATCH_FORMAT_FROM_BOX.config(state="readonly")
