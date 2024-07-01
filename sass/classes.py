from typing import Sequence

import numpy as np


class SASS:
    """
    Base class for displaying upto 4 volumes at once, or overlaying a mask on a single volume.

    Methods
    ==========
    onscroll(self, event)
         Mouse scroll listener, updates self.ind.
    update(self)
        Update method that redraws the display.
    """

    def __init__(self, alpha: Sequence, ax: Sequence, cmap: Sequence, labels: list, fig, volumes: Sequence,
                 flag_mask: bool = False, scroll_dim: int = None):
        self.fig = fig
        self.flag_mask = flag_mask  # Boolean flag to identify calling method (scroll/scroll_mask)
        self.labels = labels

        # Move scrolling dimension to the last
        volumes = [np.moveaxis(vol, scroll_dim, 2) for vol in volumes]
        self.arr_volumes = volumes

        # Prepare ax
        self.arr_ax = ax.flatten() if isinstance(ax, np.ndarray) else (ax,) * len(self.arr_volumes)

        _, _, self.slices = volumes[0].shape  # Number of slices
        self.ind = int(self.slices / 2)  # Center slice

        self.arr_alpha = alpha
        self.arr_cmap = cmap

        # Plot
        self.im = []
        for i in range(len(self.arr_volumes)):
            _alpha = self.arr_alpha[i]
            if isinstance(_alpha, np.ndarray):
                _alpha = _alpha[:, :, self.ind]
            _im = self.arr_ax[i].imshow(self.arr_volumes[i][:, :, self.ind], cmap=self.arr_cmap[i], alpha=_alpha)
            if self.flag_mask and i == 1 and not isinstance(_alpha, np.ndarray):  # If mask is overlaid: plot colorbar
                self.fig.colorbar(_im, ax=self.arr_ax[i])
            self.im.append(_im)
        self.update()

    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        elif event.button == 'down':
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        for i in range(len(self.arr_volumes)):
            self.im[i].set_data(self.arr_volumes[i][:, :, self.ind])
            self.im[i].axes.figure.canvas.draw()

            if len(self.labels) != 0:
                self.im[i].axes.set_title(self.labels[i][self.ind])
        text = f'Use scroll wheel to scroll through slices\nSlice {self.ind + 1}'
        self.fig.suptitle(text)
