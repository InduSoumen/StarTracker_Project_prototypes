# Query SIMBAD for catalog stars
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
import astropy.units as u


def query_simbad(ra, dec, radius):
    """Query SIMBAD for stars around the given coordinates within a radius."""
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')
    result_table = Simbad.query_region(coord, radius=(radius) * u.arcminute)
    if result_table is None:
        print("No stars found in the catalog for the given region.")
        return [], []
    catalog_coords = SkyCoord(result_table['RA'], result_table['DEC'], unit=(u.hourangle, u.deg), frame='icrs')
    # Extract star names/IDs
    catalog_names = result_table['MAIN_ID']
    return catalog_coords.ra.deg, catalog_coords.dec.deg , catalog_names