# sass
Scroll Across SliceS (SASS)

### What is it?
If you have a stack of images as a 3D volume and need to scroll through them, `SASS` is for you.

### Why?
Because I could not find an easy-to-use and lightweight tool to view slices in a 3D image volume.

### Examples
`SASS` can display up to four 3D volumes simultaneously!

```python
import nibabel as nb  # Use Nibabel to load a NIFTI volume
import sass

vol1 = nb.load('path/to/nifti1').get_data()
vol2 = nb.load('path/to/nifti2').get_data()
vol3 = nb.load('path/to/nifti3').get_data()
vol4 = nb.load('path/to/nifti4').get_data()

sass.scroll(vol1, vol2, vol3, vol4, cmap='gray')
```

If you want a different colormap for each volume, that's doable too.
```python
sass.scroll(vol1, vol2, vol3, vol4, cmap=['gray', 'jet', 'hot', 'cool'])
```

If your dimensions are not ordered as `rows x columns x slices`, you can specify a scrolling dimension:
```python
sass.scroll(vol1, vol2, vol3, vol4, cmap='gray', scroll_dim=0)
```

Or, `SASS` can display a volume and overlay a mask on it. With different colormaps for the volume and the mask of course!
```python
import nibabel as nb  # Use Nibabel to load a NIFTI volume
import sass

vol1 = nb.load('path/to/nifti1').get_data()
mask = nb.load('path/to/nifti2').get_data()

sass.scroll_mask(vol1, mask, alpha=0.15, cmap='gray')
```

## Contributing
Fork & PR!
