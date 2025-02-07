from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

from pathlib import Path
from pyproj import Transformer, CRS
import rioxarray


def rowcol2latlon(tiffile,row,col):
    """
    return the latitude and longitude of a row and column in a geotif

    Parameters
    ----------

    tiffile: Path object
        path to a clipped tiffile
    row: float
       row of the pixel
    col: float
       column of the pixel

    Returns
    -------

    (lon, lat):  (float, float)
       longitude (deg east) and latitude (deg north) on
       a WGS84 datum
    
    """
    has_file = tiffile.exists()
    if not has_file:
        raise IOError(f"can't find {filename}, something went wrong above") 
    the_band = rioxarray.open_rasterio(tif_filename,masked=True)
    epsg_code = the_band.rio.crs.to_epsg()
    p_utm = CRS.from_epsg(epsg_code)
    p_latlon = CRS.from_epsg(4326)
    affine_transform = the_band.rio.transform()
    x, y = affine_transform*(row, col)
    crs_transform = Transformer.from_crs(p_utm, p_latlon)
    lat, lon = transform.transform(x,y) 
    return (lon, lat)


def make_pal(ax = None,vmin = None, vmax = None, palette = "viridis"):
    """
    return a dictionary containing a palette and a Normalize object

    Parameters
    ----------

    vmin: minimum colorbar value (optional, defaults to minimum data value)
    vmax: maximum colorbar value (optional, defaults to maximum data value)
    palette: string (optional, defaults to "viridis")

    Returns
    -------

    out_dict: dict
      dictionary with key:values  cmap:colormap, norm:Normalize
      

    """
    the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
    pal = plt.get_cmap(palette)
    pal.set_bad("0.75")  # 75% grey for out-of-map cells
    pal.set_over("w")  # color cells > vmax white
    pal.set_under("k")  # color cells < vmin black
    out_dict=dict(cmap=pal,norm=the_norm)
    return out_dict
