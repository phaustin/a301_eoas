(notebook_index)=
# code snippets by notebook

- {ref}`week3:image_zoom`

  - Finding x, y from lat, lon
  
    ```
    p_utm = CRS.from_epsg(proj_code)
    p_latlon = CRS.from_epsg(4326)
    transform = Transformer.from_crs(p_latlon, p_utm)
    ubc_lon = -123.2460 
    ubc_lat = 49.2606
    ubc_x, ubc_y = transform.transform(ubc_lat, ubc_lon)
    ubc_x,ubc_y
    ```

  - Finding row, column form x, y
  
    ```
    ubc_col, ubc_row = ~full_affine * (ubc_x, ubc_y)
    ubc_col, ubc_row = int(ubc_col), int(ubc_row)
    ```
    
  - Finding the transform from the rioxarray
  
    ```
    full_affine = hls_band5.rio.transform()
    ```

  - Finding the epsg code from a NASA download tif
  
    ```
    hls_crs = hls_band5.rio.crs.to_wkt()
    proj_crs = CRS.from_wkt(hls_crs)
    pyproj_epsg = proj_crs.to_epsg(min_confidence=60)
    ```
    
  - Creating a cartopy crs object  
    
    ```
    cartopy_crs = ccrs.epsg(pyproj_epsg)
    ```
