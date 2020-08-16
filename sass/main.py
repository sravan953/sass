from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np

from sass.classes import SASS


def scroll(*volumes: np.ndarray, cmap: List[str] = ('gray',), scroll_dim: int = 2):
    """
    Scroll through slices in up to 4 3D volumes simultaneously.

    Parameters
    ==========
    *volumes : numpy.ndarray
        One or more 3D numpy.ndarray objects.
    cmap : list[str, ...]
        Upto `volumes` number of `str` values describing the colormaps. See Matplotlib documentation for valid values.
    scroll_dim : int
        Dimension to scroll through. Default is 2 for a volume structured as `rows x columns x slices`.
    """
    # Check volumes
    if len(volumes) > 4:  # Check number of volumes passed
        raise ValueError(f'sass can only display up to 4 volumes simultaneously. You passed {len(volumes)}')
    elif not np.all([isinstance(v, np.ndarray) for v in volumes]):  # Check if all volumes are numpy.ndarray objects
        raise TypeError(f'sass can only display numpy.ndarray volumes')
    elif not np.all([v.shape == volumes[0].shape for v in volumes]):  # Check if all volumes have same shape
        raise ValueError('Shapes are incompatible.')

    # Check cmap
    if not isinstance(cmap, (list, tuple)):  # cmap was neither a list nor a tuple
        raise TypeError(f'cmap must be a list[str, ...] or a tuple[str, ...]. You passed {type(cmap)}')
    elif len(cmap) > len(volumes):  # cmap > volumes
        raise TypeError(f'Upto {len(volumes)} strings can be passed for cmap. You passed {len(cmap)}')
    elif len(cmap) != len(volumes):
        if len(cmap) > 1:  # cmap > 1 but not as many as volumes
            raise TypeError(f'cmap must have a single value, or as many as volumes. You passed {len(cmap)}')
        _len = len(volumes) - len(cmap)
        cmap = cmap * _len

    # Check scrolling dimension
    if scroll_dim > len(volumes[0].shape):
        raise ValueError('Invalid scroll_dim')

    alpha = [1] * len(volumes)  # Prepare alpha

    nrows = 2 if len(volumes) / 2 > 1 else 1  # Number of rows of subplots
    ncols = 2 if len(volumes) % 2 == 0 else 1  # Number of columns of subplots
    fig, ax = plt.subplots(nrows, ncols)
    tracker = SASS(alpha=alpha, ax=ax, cmap=cmap, fig=fig, scroll_dim=scroll_dim, volumes=volumes)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()


def scroll_mask(volume: np.ndarray, mask: np.ndarray, alpha: Union[int, float, np.ndarray] = 0.15,
                cmap: List[str] = ('gray', 'jet'), scroll_dim: int = 2):
    """
    Display a volume and overlay a mask of configurable opacity (see `alpha`). Scroll through slices simultaneously.

    Parameters
    ==========
    volume : numpy.ndarray
        3D numpy.ndarray object.
    mask : numpy.ndarray
        Mask to be overlaid on `volume`.
    alpha : float, int, np.ndarray
        Opacity of `mask` to be overlaid on `volume`. Valid values are 0 < `alpha` <=1 or 1 < `alpha` <= 100. `alpha`
        must be of the same shape as `mask` and `volume` if it is a np.ndarray. Default value is `0.15`.
    cmap : list[str, str]
        Upto two `str` values describing the colormap(s). See Matplotlib documentation for valid values.
    scroll_dim : int
        Dimension to scroll through. Default is 2 for a volume structured as `rows x columns x slices`.
    """
    # Check volume and mask
    if volume.shape != mask.shape:
        raise ValueError(f'volume ({volume.shape}) and mask ({mask.shape}) are incompatible.')
    # Check if volume and mask are np.ndarray objects
    elif not isinstance(volume, np.ndarray) or not isinstance(mask, np.ndarray):
        raise TypeError(f'sass can only display numpy.ndarray volumes')

    # Check alpha
    if isinstance(alpha, int):  # alpha is int
        if not 0 <= alpha <= 100:
            raise ValueError(f'0 <= alpha <= 100. You passed {alpha}')
        alpha = alpha / 100  # Convert to %
    elif isinstance(alpha, float):  # alpha is float
        if not 0 <= alpha <= 1:
            raise ValueError(f'0 <= alpha <=1. You passed {alpha}')
    elif isinstance(alpha, np.ndarray):  # alpha is np.ndarray
        if alpha.shape != volume.shape:
            raise ValueError(f'alpha ({alpha.shape}) and volume ({volume.shape}) are incompatible.')
    else:
        raise TypeError(f'alpha can be float, int or numpy.ndarray. You passed {type(alpha)}')
    alpha = (1, alpha)

    # Check cmap
    if isinstance(cmap, (list, tuple)) and len(cmap) > 2:  # Check if a maximum of two cmaps were passed
        raise ValueError(f'scroll_mask accepts upto 2 strings for cmap. You passed {len(cmap)}')
    elif not isinstance(cmap, (list, tuple, str)):
        raise TypeError(f'cmap must be a list[str, ...] or a tuple[str, ...]. You passed {type(cmap)}')

    # Check scroll_dim
    if scroll_dim > len(volume[0].shape):
        raise ValueError('Invalid scroll_dim')

    nrows = 1
    ncols = 1
    fig, ax = plt.subplots(nrows, ncols)
    tracker = SASS(alpha=alpha, ax=ax, cmap=cmap, fig=fig, flag_mask=True, scroll_dim=scroll_dim,
                   volumes=(volume, mask))
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()
