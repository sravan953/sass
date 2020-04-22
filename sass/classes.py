import numpy as np


class SASS:
    def __init__(self, fig, ax, vol, cmap, alpha, scroll_dim: int = None):
        self.fig = fig

        # Move scrolling dimension to the last
        if scroll_dim > len(vol[0].shape):
            raise ValueError('Invalid scroll_dim')
        vol = [np.rollaxis(vol, axis=scroll_dim, start=3) for vol in vol]
        vol = [vol.astype(np.float64) for vol in vol]
        self.arr_vols = vol

        # Convert arr_ax to a tuple
        if not isinstance(ax, np.ndarray):
            ax = (ax,) * len(self.arr_vols)
        self.arr_ax = ax

        rows, cols, self.slices = vol[0].shape
        self.ind = self.slices // 2

        # Prepare colour map
        if not isinstance(cmap, tuple) and not isinstance(cmap, list):
            cmap = (cmap,) * len(self.arr_vols)
        self.arr_cmap = cmap

        # Prepare alpha
        if not isinstance(alpha, tuple) and not isinstance(alpha, list):
            self.alpha = (1,) * len(self.arr_vols)
        else:
            self.alpha = alpha

        # Plot
        self.im = []
        for i in range(len(self.arr_vols)):
            _im = self.arr_ax[i].imshow(self.arr_vols[i][:, :, self.ind], cmap=self.arr_cmap[i], alpha=self.alpha[i])
            self.im.append(_im)
        self.update()

    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        for i in range(len(self.arr_vols)):
            self.im[i].set_data(self.arr_vols[i][:, :, self.ind])
            self.im[i].axes.figure.canvas.draw()
        self.fig.suptitle(f'Use scroll wheel to scroll through slices\nSlice {self.ind}')
