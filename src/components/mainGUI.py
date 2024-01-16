import tkinter as tk
from ctypes import windll

from src.components.frames import startFrame
from src.components.frames import dataFrame

from src.tools import dataRetriever

import src.util.defaults as d


class MainGUI(tk.Tk):
    def _set_screen_properties(self):
        """Set the size of the application and centre it on screen"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (d.APP_WIDTH / 2)
        y = (screen_height / 2) - (d.APP_HEIGHT / 2)

        self.geometry("%dx%d+%d+%d" % (d.APP_WIDTH, d.APP_HEIGHT, x, y))

    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(
            1
        )  # Fixes an issue with tkinter applications being quite blurry

        super().__init__()

        self.title(d.APP_TITLE)
        self._set_screen_properties()

        self.iconbitmap(d.ICON_DIR)

        self._create_frames()

    def _create_frames(self):
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (startFrame.StartFrame, dataFrame.DataFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def _has_chosen_new_files(self, load_profile_filename, block_tariff_filename):
        """Determines if the user has selected new files from the last calculation.
        If they haven't, and are still selecting the same files, we don't need to reload/recalculate everything.
        """
        return (
            load_profile_filename
            != self.frames["StartFrame"].original_load_profile_filename
        ) or (
            block_tariff_filename
            != self.frames["StartFrame"].original_block_tariff_filename
        )
        # return (os.path.abspath(load_profile_filename) != os.path.abspath(self.frames["StartFrame"].original_load_profile_filename)) or (os.path.abspath(block_tariff_filename) != os.path.abspath(self.frames["StartFrame"].original_block_tariff_filename))

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def show_data_frame(self, load_profile_filename, block_tariff_filename):
        """Retrieve the load profile and block tariff data, then display on data frame"""
        if self._has_chosen_new_files(load_profile_filename, block_tariff_filename):
            (
                load_profile_data,
                block_tariff_data,
                calendar_months,
            ) = dataRetriever.get_data_from_files(
                load_profile_filename, block_tariff_filename
            )

            self.frames["DataFrame"].graph.load_profile_data = load_profile_data

            first_reading = load_profile_data["Time of Reading - Local"].iloc[0]
            last_reading = load_profile_data["Time of Reading - Local"].iloc[-1]

            self.frames["DataFrame"].populate_with_data(
                load_profile_filename,
                block_tariff_filename,
                block_tariff_data,
                calendar_months,
                first_reading,
                last_reading,
            )

            self.frames[
                "StartFrame"
            ].original_load_profile_filename = load_profile_filename
            self.frames[
                "StartFrame"
            ].original_block_tariff_filename = block_tariff_filename

        self.show_frame("DataFrame")
