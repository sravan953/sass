import matplotlib.pyplot as plt
import numpy as np

from sass.classes import SASS


def scroll(*volumes, cmap=('gray',), scroll_dim=2):
    """
    Scroll through slices in up to 4 3D volumes simultaneously.

    Parameters
    ==========
    volumes : tuple
        One or more 3D numpy.ndarray objects.
    cmap : tuple
        Upto `volumes` number of `str` values describing the colormaps. See Matplotlib documentation for valid values.
    scroll_dim : int
        Dimension to scroll through. Default is 2 for a volume structured as `rows x columns x slices`.
    """
    if len(volumes) > 4:
        raise ValueError('sass can only display up to 4 volumes simultaneously.')

    if not np.all([isinstance(vol, np.ndarray) for vol in volumes]):  # Check if all volumes are numpy.ndarray objects
        raise ValueError(f'sass can only display numpy.ndarray volumes, you passed {type(volumes[0])}')

    if not np.all([v.shape == volumes[0].shape for v in volumes]):  # Check if all volumes have same shape
        raise ValueError('All volumes must be of same dimensions.')

    # Check if one cmap was passed or as many as volumes
    if isinstance(cmap, (list, tuple)) and len(cmap) != len(volumes):
        raise ValueError(f'Upto {len(volumes)} strings can be passed for cmap, you passed {len(cmap)}')

    nrows = 2 if len(volumes) / 2 > 1 else 1  # Number of rows of subplots
    ncols = 2 if len(volumes) % 2 == 0 else 1  # Number of columns of subplots
    fig, ax = plt.subplots(nrows, ncols)
    if isinstance(ax, np.ndarray):
        ax = ax.flatten()
    tracker = SASS(alpha=1, ax=ax, cmap=cmap, fig=fig, scroll_dim=scroll_dim, volumes=volumes)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()


def scroll_mask(volume: np.ndarray, mask: np.ndarray, alpha: float = 0.15, cmap: tuple = ('gray', 'jet'), scroll_dim=2):
    """
    Display a volume and overlay a mask of configurable opacity (see `alpha`). Scroll through slices simultaneously.

    Parameters
    ==========
    mask : numpy.ndarray
        Mask to be overlaid on `volume`.
    volume : numpy.ndarray
        One or more 3D numpy.ndarray objects.
    alpha : float, int
        Opacity of `mask` to be overlaid on `volume`. Valid values are 0 < `alpha` <=1 or 1 < `alpha` <= 100.
        Default value is `0.15`.
    cmap : list/tuple
        One or two `str` values describing the colormap(s). See Matplotlib documentation for valid values.
    scroll_dim : int
        Dimension to scroll through. Default is 2 for a volume structured as `rows x columns x slices`.
    """
    if volume.shape != mask.shape:  # Check if volume and mask have same shape
        raise ValueError(f'{volume.shape} and {mask.shape} are incompatible.')

    if 0 < alpha <= 1:  # Yay!
        pass
    elif 1 < alpha <= 100:  # Convert to %
        alpha = alpha / 100
    else:
        raise ValueError(f'Invalid alpha. Expected 0 < alpha <=1 or 1= < alpha <= 100, you passed {alpha}')

    if isinstance(cmap, (list, tuple)) and len(cmap) > 2:  # Check if a maximum of two cmaps were passed
        raise ValueError(f'Upto 2 strings can be passed for cmap, you passed {len(cmap)}')

    nrows = 1
    ncols = 1
    fig, ax = plt.subplots(nrows, ncols)
    tracker = SASS(alpha=(1, alpha), ax=ax, cmap=cmap, fig=fig, scroll_dim=scroll_dim, volumes=(volume, mask))
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()
