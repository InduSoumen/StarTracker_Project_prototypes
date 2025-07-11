import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from catalogue_query import catalogue_query
from detectstar import detectstar
from fov import calculate_fov
from nonfitstofitsandwcs import getwcsinfo
from pixeltocelestial import calculate_ra_dec_from_centroids
from starmatching import query_simbad
from plot_results import plot_centroids,plot_detectedstars,plot_detectedstars_with_catalogue,plot_matched_stars,show_plots

image_name = "astrometry_image_1.jpg"
fits_file_name = 'astrometry_image_1.fits.'
centroids,image_with_stars,image,blurred_image,thresholded_image = detectstar(image_name)
getwcsinfo(image_name,fits_file_name)
fov_width, fov_height, search_radius,ra_centre,dec_centre= calculate_fov(fits_file_name)
print(f"FoV: {fov_width:.2f}' x {fov_height:.2f}' (arcminutes) Search Radius: {search_radius:.2f} arcminutes")

ra_dec_list = calculate_ra_dec_from_centroids(centroids,fits_file_name)
ra_vals = [ra for ra, dec in ra_dec_list]
dec_vals = [dec for ra, dec in ra_dec_list]

#catalog_ra , catalog_dec = catalogue_query(ra_centre,dec_centre,search_radius)
#print(f"Catalog RA: {catalog_ra}, Catalog Dec: {catalog_dec}")
#catalog_ra = [catalog_ra]
#catalog_dec =[catalog_dec]

catalog_ra, catalog_dec ,catalog_names= query_simbad(ra_centre, dec_centre, search_radius)

# Define a matching threshold (in degrees), e.g., 1 arcsecond = 1/3600 degree
matching_threshold_deg = 5 / 3600  # 1 arcsecond

# Matching detected stars to catalog stars
detected_coords = SkyCoord(ra=ra_vals, dec=dec_vals, unit=(u.deg, u.deg), frame='icrs')
catalog_coords = SkyCoord(ra=catalog_ra, dec=catalog_dec, unit=(u.deg, u.deg), frame='icrs')

idx, d2d, _ = detected_coords.match_to_catalog_sky(catalog_coords)
matches = d2d < matching_threshold_deg * u.deg

matched_ra = detected_coords[matches].ra.deg
matched_dec = detected_coords[matches].dec.deg
matched_names = catalog_names[idx[matches]]

print(f"Number of matched stars: {np.sum(matches)}")
print("Matched stars and their names:")
for ra, dec, name in zip(matched_ra, matched_dec, matched_names):
   print(f"RA: {ra:.6f}, Dec: {dec:.6f}, Name: {name}")

# Extract matched detected stars
matched_detected_coords = detected_coords[matches]
# Extract matched catalog stars using the indices
matched_catalog_coords = catalog_coords[idx[matches]]

plot_detectedstars(image_with_stars,image,blurred_image,thresholded_image)
plot_centroids(image_with_stars,ra_vals, dec_vals)
plot_detectedstars_with_catalogue(ra_vals,dec_vals,catalog_ra,catalog_dec)
#plot_matched_stars(matched_detected_coords,matched_catalog_coords)
plot_matched_stars(matched_detected_coords,matched_catalog_coords,matched_names)
show_plots()
