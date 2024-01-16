import tkinter as tk
from tkinter import font as tkfont
from tkcalendar import DateEntry

from src.components.graph import Graph

import src.util.defaults as d
import src.util.utils as util


class DataFrame(tk.Frame):
    """Frame which displays all graph and calculations data to user"""

    def _update_graph_calendar_month(self):
        self.graph.apply_calendar_month_region(self.calendar_month_selection)

    def _update_graph_custom_region(self):
        self.graph.apply_custom_region(
            self.custom_region_start_selection.get(),
            self.custom_region_end_selection.get(),
        )

    def _changed_region_selection(self, *args):
        if self.region_selection.get() == d.REGION_SELECTIONS[0]:  # Entire region
            if self.calendar_month_dropdown:
                self.calendar_month_dropdown.grid_forget()

            if (
                self.custom_region_start_picker
                and self.custom_region_end_picker
                and self.custom_region_label
            ):
                self.custom_region_start_picker.grid_forget()
                self.custom_region_end_picker.grid_forget()
                self.custom_region_label.grid_forget()

            self.graph.apply_entire_region()
        elif self.region_selection.get() == d.REGION_SELECTIONS[1]:  # Calendar month
            if (
                self.custom_region_start_picker
                and self.custom_region_end_picker
                and self.custom_region_label
            ):
                self.custom_region_start_picker.grid_forget()
                self.custom_region_end_picker.grid_forget()
                self.custom_region_label.grid_forget()

            self.calendar_month_dropdown.grid(row=2, column=1, padx=0, pady=0)
            self._update_graph_calendar_month()
        elif self.region_selection.get() == d.REGION_SELECTIONS[2]:  # Custom region
            if self.calendar_month_dropdown:
                self.calendar_month_dropdown.grid_forget()

            self.custom_region_start_picker.grid(
                row=2, column=1, padx=40, pady=0, sticky="W"
            )
            self.custom_region_label.grid(row=2, column=1, padx=0, pady=0)
            self.custom_region_end_picker.grid(
                row=2, column=1, padx=40, pady=0, sticky="E"
            )

            self._update_graph_custom_region()

    def _changed_calendar_month_selection(self, *args):
        if (
            self.region_selection.get() == d.REGION_SELECTIONS[1]
        ):  # Calender month is selected
            self._update_graph_calendar_month()

    def _changed_custom_region_selection(self, *args):
        if (
            self.region_selection.get() == d.REGION_SELECTIONS[2]
        ):  # Custom region is selected
            if (
                self.custom_region_start_selection.get() != ""
                and self.custom_region_end_selection.get() != ""
            ):
                self._update_graph_custom_region()

    def _electricity_used_updated(self, *args):
        self.final_calc.set(
            util.calculate_bill(self.block_tariff_data, self.electricity_used.get())
        )

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=8)
        self.rowconfigure(4, weight=1)

        self.block_tariff_data = None
        self.calendar_months = None

        self.load_profile_filename = tk.StringVar()
        self.block_tariff_filename = tk.StringVar()

        # Display top toolbar

        home_btn = tk.Button(
            self, text="Home", command=lambda: controller.show_frame("StartFrame")
        )
        load_profile_label = tk.Label(self, textvariable=self.load_profile_filename)
        block_tariff_label = tk.Label(self, textvariable=self.block_tariff_filename)

        home_btn.grid(row=0, column=0, padx=15, pady=5, sticky="W", columnspan=2)
        load_profile_label.grid(
            row=0, column=0, padx=80, pady=5, sticky="W", columnspan=2
        )
        block_tariff_label.grid(
            row=0, column=0, padx=15, pady=5, sticky="E", columnspan=2
        )

        # Display graph
        self.graph = Graph(self)

        # Allow user to change region selection
        self.set_region_label = tk.Label(self, text="Set region to calculate bill for:")

        self.region_selection = tk.StringVar()
        self.region_selection.set(d.REGION_SELECTIONS[0])
        self.region_selection.trace_add("write", self._changed_region_selection)

        self.region_selection_dropdown = tk.OptionMenu(
            self, self.region_selection, *d.REGION_SELECTIONS
        )

        self.set_region_label.grid(row=1, column=1, padx=10, pady=0, sticky="W")
        self.region_selection_dropdown.grid(
            row=1, column=1, padx=10, pady=0, sticky="E"
        )

        # Allow user to change calendar month
        self.calendar_month_selection = tk.StringVar()
        self.calendar_month_selection.trace_add(
            "write", self._changed_calendar_month_selection
        )
        self.calendar_month_dropdown = None

        # Allow user to change custom region
        self.custom_region_start_selection = tk.Variable()
        self.custom_region_end_selection = tk.Variable()

        self.custom_region_start_picker = None
        self.custom_region_end_picker = None

        self.custom_region_start_selection.trace_add(
            "write", self._changed_custom_region_selection
        )
        self.custom_region_end_selection.trace_add(
            "write", self._changed_custom_region_selection
        )
        self.custom_region_label = tk.Label(self, text="to")

        # Calculate electricity bill
        self.electricity_used = tk.DoubleVar()
        self.electricity_used.trace_add("write", self._electricity_used_updated)
        self.final_calc = tk.StringVar()
        self.final_calc_label_font = tkfont.Font(size=12)
        self.final_calc_label = tk.Label(
            self, textvariable=self.final_calc, font=self.final_calc_label_font
        )

    def populate_with_data(
        self,
        load_profile_filename,
        block_tariff_filename,
        block_tariff_data,
        calendar_months,
        first_reading,
        last_reading,
    ):
        """Load and display all relevant data which has to do with the load profile and block tariff files"""
        self.load_profile_filename.set(
            d.LOAD_PROFILE_LABEL + util.shorten_dir(load_profile_filename)
        )
        self.block_tariff_filename.set(
            d.BLOCK_TARIFF_LABEL + util.shorten_dir(block_tariff_filename)
        )

        self.block_tariff_data = block_tariff_data

        self.calendar_months = calendar_months
        self.calendar_month_selection.set(self.calendar_months[0])
        self.calendar_month_dropdown = tk.OptionMenu(
            self, self.calendar_month_selection, *self.calendar_months
        )

        self.custom_region_start_selection.set(first_reading)
        self.custom_region_end_selection.set(last_reading)

        self.custom_region_start_picker = DateEntry(
            self,
            selectmode="day",
            textvariable=self.custom_region_start_selection,
            mindate=first_reading,
            maxdate=last_reading,
        )
        self.custom_region_end_picker = DateEntry(
            self,
            selectmode="day",
            textvariable=self.custom_region_end_selection,
            mindate=first_reading,
            maxdate=last_reading,
        )
        self.custom_region_start_picker.set_date(first_reading)
        self.custom_region_end_picker.set_date(last_reading)

        self.graph.plot()

        self._electricity_used_updated()
        self.final_calc_label.grid(row=3, column=1, padx=0, pady=0, rowspan=2)
