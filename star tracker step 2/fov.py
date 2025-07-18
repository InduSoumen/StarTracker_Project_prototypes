import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

def calculate_fov(fits_file_name):
    # Load the FITS file
    fits_file_name = fits_file_name
    fits_header = fits.getheader(fits_file_name)

    # Create a WCS object
    wcs = WCS(fits_header)

    # Get image dimensions (number of pixels)
    image_width = fits_header['NAXIS1']  # Number of pixels along x-axis
    image_height = fits_header['NAXIS2']  # Number of pixels along y-axis

    ra_center = fits_header['CRVAL1']  # RA at the reference pixel
    dec_center = fits_header['CRVAL2']  # Dec at the reference pixel

    print(f"Reference RA: {ra_center} degrees, Dec: {dec_center} degrees")

    # Calculate pixel scale (degrees/pixel)
    pixel_scale = wcs.pixel_scale_matrix  # A 2x2 matrix
    pixel_scale_arcsec = abs(pixel_scale[0, 0]) * 3600  # Convert degrees to arcseconds

    # Calculate field of view
    fov_width_arcmin = (image_width * pixel_scale_arcsec) / 60  # Width in arcminutes
    fov_height_arcmin = (image_height * pixel_scale_arcsec) / 60  # Height in arcminutes

    diagonal_fov = np.sqrt(fov_width_arcmin ** 2 + fov_height_arcmin ** 2)
    search_radius = diagonal_fov / 2  # Half of the diagonal, in arcminutes

    return fov_height_arcmin,fov_width_arcmin,search_radius,ra_center,dec_center


