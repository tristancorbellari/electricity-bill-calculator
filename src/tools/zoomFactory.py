# This is basically matplotlib's zoom factory function, which allows to zoom in a graph with the scroll wheel.
# Had to change one minor thing to not allow the user to zoom out from the initial bounds.
def zoom_factory(ax, base_scale=1.1):
    """
    Add ability to zoom with the scroll wheel.

    Parameters
    ----------
    ax : matplotlib axes object
        axis on which to implement scroll to zoom
    base_scale : float
        how much zoom on each tick of scroll wheel

    Returns
    -------
    disconnect_zoom : function
        call this to disconnect the scroll listener
    """

    def limits_to_range(lim):
        return lim[1] - lim[0]

    fig = ax.get_figure()  # get the figure of interest
    fig.canvas.capture_scroll = True
    has_toolbar = hasattr(fig.canvas, "toolbar") and fig.canvas.toolbar is not None
    if has_toolbar:
        # it might be possible to have an interactive backend without
        # a toolbar. I'm not sure so being safe here
        toolbar = fig.canvas.toolbar
        toolbar.push_current()
    orig_xlim = ax.get_xlim()
    orig_ylim = ax.get_ylim()
    orig_yrange = limits_to_range(orig_ylim)
    orig_xrange = limits_to_range(orig_xlim)
    orig_center = ((orig_xlim[0] + orig_xlim[1]) / 2, (orig_ylim[0] + orig_ylim[1]) / 2)

    def zoom_fun(event):
        if event.inaxes is not ax:
            return
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        # set the range
        (cur_xlim[1] - cur_xlim[0]) * 0.5
        (cur_ylim[1] - cur_ylim[0]) * 0.5
        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location
        if event.button == "up":
            # deal with zoom in
            scale_factor = base_scale
        elif event.button == "down":
            # deal with zoom out
            scale_factor = 1 / base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
        # set new limits
        new_xlim = [
            xdata - (xdata - cur_xlim[0]) / scale_factor,
            xdata + (cur_xlim[1] - xdata) / scale_factor,
        ]
        new_ylim = [
            ydata - (ydata - cur_ylim[0]) / scale_factor,
            ydata + (cur_ylim[1] - ydata) / scale_factor,
        ]
        new_yrange = limits_to_range(new_ylim)
        new_xrange = limits_to_range(new_xlim)

        # NOTE: This is the changed section of code
        if abs(new_yrange) > abs(orig_yrange):
            new_ylim = orig_ylim
        if abs(new_xrange) > abs(orig_xrange):
            new_xlim = orig_xlim

        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)

        if has_toolbar:
            toolbar.push_current()
        ax.figure.canvas.draw_idle()  # force re-draw

    # attach the call back
    cid = fig.canvas.mpl_connect("scroll_event", zoom_fun)

    def disconnect_zoom():
        fig.canvas.mpl_disconnect(cid)

    # return the disconnect function
    return disconnect_zoom
