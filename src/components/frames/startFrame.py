import os

import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk, Image

import src.util.defaults as d
import src.util.utils as util


class StartFrame(tk.Frame):
    """Frame displayed to the user upon startup, for choosing load profile and block tariff files"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=2)

        self.columnconfigure(0, weight=1)

        self.original_load_profile_filename = None
        self.original_block_tariff_filename = None

        self.load_profile_filename = tk.StringVar()
        self.load_profile_filename.set(
            util.normalise_dir(os.path.join(d.LOAD_PROFILE_DIR, d.LOAD_PROFILE_FILE))
        )

        self.block_tariff_filname = tk.StringVar()
        self.block_tariff_filname.set(
            util.normalise_dir(os.path.join(d.BLOCK_TARIFF_DIR, d.BLOCK_TARIFF_FILE))
        )

        # Display logo
        self.logo_img = Image.open(d.LOGO_DIR)
        self.logo_img = self.logo_img.resize(
            (int(self.logo_img.width * 0.5), int(self.logo_img.height * 0.5))
        )
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        logo_label = tk.Label(self, image=self.logo_img)
        logo_label.grid(row=0, column=0, padx=0, pady=0)

        # Choose and display load profile
        load_profile_label = tk.Label(self, text="Load profile:")
        load_profile_filename_label = tk.Label(
            self, textvariable=self.load_profile_filename, state="disabled"
        )
        load_profile_btn = tk.Button(
            self,
            text="Choose file",
            command=lambda: self._choose_file(
                [("CSV files", "*.csv")],
                d.LOAD_PROFILE_DIR,
                self.load_profile_filename,
            ),
        )

        load_profile_label.grid(row=1, column=0, padx=0, pady=0)
        load_profile_filename_label.grid(row=2, column=0, padx=0, pady=0)
        load_profile_btn.grid(row=3, column=0, padx=0, pady=0)

        # Choose and display block tariff format
        block_tariff_label = tk.Label(self, text="Block tariff format:")
        block_tariff_filename_label = tk.Label(
            self, textvariable=self.block_tariff_filname, state="disabled"
        )
        block_tariff_btn = tk.Button(
            self,
            text="Choose file",
            command=lambda: self._choose_file(
                [("JSON files", "*.json")],
                d.BLOCK_TARIFF_DIR,
                self.block_tariff_filname,
            ),
        )

        block_tariff_label.grid(row=4, column=0, padx=0, pady=0)
        block_tariff_filename_label.grid(row=5, column=0, padx=0, pady=0)
        block_tariff_btn.grid(row=6, column=0, padx=0, pady=0)

        # Button to calculate bill and open data frame
        button1 = tk.Button(
            self,
            text="Calculate bill",
            command=lambda: controller.show_data_frame(
                self.load_profile_filename.get(), self.block_tariff_filname.get()
            ),
        )

        button1.grid(row=7, column=0, padx=0, pady=0)

    def _choose_file(self, filetypes, initial_dir, var_to_update):
        filename = filedialog.askopenfilename(
            filetypes=filetypes, initialdir=initial_dir
        )
        if filename != "":
            var_to_update.set(filename)
