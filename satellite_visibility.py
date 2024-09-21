import numpy as np
import pandas as pd
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.units as u

# Constants for the ground station location and visibility limits
GROUND_STATION_LAT = 78.7199  # Latitude (degrees)
GROUND_STATION_LON = 20.3493  # Longitude (degrees)
MIN_ALTITUDE = 10.0  # Minimum observable altitude (degrees)
MAX_ALTITUDE = 85.0  # Maximum observable altitude (degrees)

def load_satellite_data(file_path):
    """Load satellite data from a CSV file."""
    return pd.read_csv(file_path)

def convert_to_altaz(sat_data, ground_station_location):
    """Convert satellite positions to Altitude and Azimuth."""
    # Clean the Time column - method developed during unit testing.
    valid_times = sat_data['Time (iso)'].dropna().astype(str).str.strip().replace('', np.nan).dropna()

    # Check if valid_times is empty
    if valid_times.empty:
        raise ValueError("No valid time data available.")

    # Convert to astropy Time
    times = Time(valid_times.tolist(), format='iso')

    # Satellite coordinates (with units specified) - otherwise expects rad as default.
    satellite_coords = SkyCoord(
        ra=sat_data['RA (GCRS) [deg]'].values * u.deg, 
        dec=sat_data['Dec (GCRS) [deg]'].values * u.deg, 
        distance=sat_data['Distance (GCRS) [km]'].values * u.km,
        frame='gcrs', obstime=times
    )

    # Convert coordinates to AltAz
    altaz_coords = satellite_coords.transform_to(AltAz(obstime=times, location=ground_station_location))
    
    return altaz_coords.alt.deg, altaz_coords.az.deg


def find_visibility(sat_data, altitudes):
    """Identify visible times for the satellite."""
    visibility_mask = (altitudes >= MIN_ALTITUDE) & (altitudes <= MAX_ALTITUDE)
    return sat_data['Time (iso)'][visibility_mask]

def write_to_file(visible_times, output_file):
    """Write the visible times to a specified output file."""
    visible_times.to_csv(output_file, index=False, header=False)

def main(file_path, output_file):
    # Load satellite data and define ground station location
    sat_data = load_satellite_data(file_path)
    ground_station_location = EarthLocation(lat=GROUND_STATION_LAT * u.deg, lon=GROUND_STATION_LON * u.deg)
    
    # Convert to Altitude and Azimuth, then find visibility
    altitudes, _ = convert_to_altaz(sat_data, ground_station_location)
    visible_times = find_visibility(sat_data, altitudes)
    
    # Write results to file
    write_to_file(visible_times, output_file)
    print(f"The satellite visibility times have been written to {output_file}")

if __name__ == "__main__":
    file_path = 'satellite_positions.csv'
    output_file = 'visible_times.txt'  # Output file to store visibility times
    main(file_path, output_file)
