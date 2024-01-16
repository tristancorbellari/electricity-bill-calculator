import matplotlib
from matplotlib import pyplot as plt
from matplotlib import backend_bases

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from mpl_interactions import ioff
from src.tools.zoomFactory import zoom_factory

from datetime import datetime as dt
import calendar


class Graph:
    def __init__(self, parent):
        self.parent = parent

        self.load_profile_data = None

        self.original_xlim = None
        self.original_ylim = None

        with plt.ioff():
            self.fig, self.ax = plt.subplots()

        self.fig.set_size_inches(5, 4.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=0, pady=0, rowspan=3)

        # Exclude buttons for panning, zooming and subplot configuration from toolbar
        backend_bases.NavigationToolbar2.toolitems = (
            ("Home", "Reset original view", "home", "home"),
            ("Back", "Back to  previous view", "back", "back"),
            ("Forward", "Forward to next view", "forward", "forward"),
            (None, None, None, None),
            ("Save", "Save the figure", "filesave", "save_figure"),
        )
        self.toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)

        self.toolbar.pan()
        self.toolbar.update()
        self.toolbar.grid(row=4, column=0, padx=0, pady=0, sticky="W")

    def plot(self):
        """Plot the graph data and set axes"""
        self.ax.plot(
            self.load_profile_data["Time of Reading - Local"],
            self.load_profile_data["forwardActiveEnergy Value"],
        )

        plt.xlabel("Date/Time Reading")
        plt.ylabel("Electricity Used (kWh)")

        self._draw()

        self._update_lims_from_selection(self.load_profile_data)
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()

    def _draw(self):
        """Draw the graph. This is called every time the date/time region is updated"""
        self.ax.tick_params(axis="x", rotation=30)

        plt.tight_layout()

        self.parent.electricity_used.set(self.ax.get_ylim()[1] - self.ax.get_ylim()[0])

        disconnect_zoom = zoom_factory(self.ax)

        self.canvas.draw()

    def _update_lims(self, xlims, ylims):
        """Set the x and y limits of the graph"""
        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        self._draw()

    def _update_lims_from_selection(self, new_df):
        """Apply limits from a new selection to the graph"""
        xlims = (
            new_df.iloc[0]["Time of Reading - Local"],
            new_df.iloc[-1]["Time of Reading - Local"],
        )
        ylims = (
            new_df.iloc[0]["forwardActiveEnergy Value"],
            new_df.iloc[-1]["forwardActiveEnergy Value"],
        )
        self._update_lims(xlims, ylims)

    def apply_entire_region(self):
        """Apply the limits of the entire region to the graph"""
        self._update_lims(self.original_xlim, self.original_ylim)

    def apply_calendar_month_region(self, month):
        """Apply the limits of the specified calendar month to the graph"""
        new_df = self.load_profile_data[
            self.load_profile_data["Time of Reading - Local"].dt.month
            == list(calendar.month_name).index(month.get())
        ]

        self._update_lims_from_selection(new_df)

    def apply_custom_region(self, start_date, end_date):
        """Apply the limits of the specified custom region to the graph"""
        start_datetime = dt.strptime(start_date, "%m/%d/%y").replace(hour=0, minute=0)
        end_datetime = dt.strptime(end_date, "%m/%d/%y").replace(hour=23, minute=30)

        new_df = self.load_profile_data[
            self.load_profile_data["Time of Reading - Local"].between(
                start_datetime, end_datetime
            )
        ]

        self._update_lims_from_selection(new_df)
