import numpy as np


class SASS:
    """
    Base class for displaying upto 4 volumes at once, or overlaying a mask on a single volume.

    Methods
    ==========
    onscroll : self, event
         Mouse scroll listener, updates self.ind.
    update : self
        Update method that redraws the display.
    """

    def __init__(self, alpha, ax, cmap, fig, volumes, scroll_dim: int = None):
        self.fig = fig
        flag_mask = False  # Boolean flag to identify calling method (scroll/scroll_mask)

        # Move scrolling dimension to the last
        if scroll_dim > len(volumes[0].shape):
            raise ValueError('Invalid scroll_dim')
        volumes = [np.swapaxes(vol, scroll_dim, 2) for vol in volumes]
        volumes = [vol.astype(np.float64) for vol in volumes]
        self.arr_volumes = volumes

        # Convert ax to a tuple
        if not isinstance(ax, np.ndarray):  # scroll_mask is the calling method
            ax = (ax,) * len(self.arr_volumes)
            flag_mask = True
        self.arr_ax = ax

        _, _, self.slices = volumes[0].shape  # Number of slices
        self.ind = self.slices // 2  # Center slice

        # Prepare colour map
        self.arr_cmap = (cmap,) * len(self.arr_volumes) if not isinstance(cmap, (list, tuple)) else cmap

        # Prepare alpha
        self.alpha = (1,) * len(self.arr_volumes) if not isinstance(alpha, (list, tuple)) else alpha

        # Plot
        self.im = []
        for i in range(len(self.arr_volumes)):
            _im = self.arr_ax[i].imshow(self.arr_volumes[i][:, :, self.ind], cmap=self.arr_cmap[i], alpha=self.alpha[i])
            if flag_mask and i == 1:  # If mask is overlaid: plot colorbar
                self.fig.colorbar(_im, ax=self.arr_ax[i])
            self.im.append(_im)
        self.update()

    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        for i in range(len(self.arr_volumes)):
            self.im[i].set_data(self.arr_volumes[i][:, :, self.ind])
            self.im[i].axes.figure.canvas.draw()
        self.fig.suptitle(f'Use scroll wheel to scroll through slices\nSlice {self.ind}')
