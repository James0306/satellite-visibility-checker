"""
Author: James Aherne
Date: 2024-09-22
Project: Satellite Visibility Checker
Description:
    This script calculates the visibility of a satellite from a specified ground station.
    It reads satellite position data from a CSV file, converts celestial coordinates
    (RA, Dec, Distance) into Altitude and Azimuth using the ground station's location,
    and returns the Altitude and Azimuth angles for further analysis.
    For more information, please refer to the README.md file provided.

Dependencies:
    - astropy
    - numpy
    - pandas

Files:
    - satellite_visibility.py: Main script for calculating satellite visibility.
    - test_satellite_visibility.py: Unit tests to ensure the correctness of the script.
    - satellite_positions.csv: Provides satellite positional data.
    - visibility_results.csv: Provides dates and times when the satellite is visible
      from the ground station within the provided paraemters.

Notes:
    Ensure that the CSV file follows the specified format with columns:
    'Time (iso)', 'RA (GCRS) [deg]', 'Dec (GCRS) [deg]', 'Distance (GCRS) [km]'.
"""

import numpy as np
import pandas as pd
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.units as u

# Constants for the file input and outputs
INPUT_FILE = "satellite_positions.csv"
OUTPUT_FILE = "visibility_results.csv"

# Constants for the ground station location and visibility limits
GROUND_STATION_LAT = 78.7199  # Latitude (degrees)
GROUND_STATION_LON = 20.3493  # Longitude (degrees)
MIN_ALTITUDE = 10.0  # Minimum observable altitude (degrees)
MAX_ALTITUDE = 85.0  # Maximum observable altitude (degrees)

def load_satellite_data(file_path):
    """Load satellite data from a CSV file."""
    return pd.read_csv(file_path)

def clean_time_column(sat_data):
    """Clean the Time column and convert it to a list of valid times."""
    valid_times = sat_data['Time (iso)'].dropna().astype(str).str.strip().replace('', np.nan).dropna()

    # Check if valid_times is empty
    if valid_times.empty:
        raise ValueError("No valid time data available.")
    
    # Convert the cleaned times to astropy Time objects
    return Time(valid_times.tolist(), format='iso')

def convert_to_altaz(sat_data, times, ground_station_location):
    """Convert satellite positions to Altitude and Azimuth using cleaned times."""
    # Satellite coordinates (with units specified)
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
    
    # Clean the time data
    times = clean_time_column(sat_data)
    
    # Convert to Altitude and Azimuth using cleaned times, then find visibility
    altitudes, _ = convert_to_altaz(sat_data, times, ground_station_location)
    visible_times = find_visibility(sat_data, altitudes)
    
    # Write results to file
    write_to_file(visible_times, output_file)
    print(f"The satellite visibility times have been written to {output_file}")

if __name__ == "__main__":
    main(INPUT_FILE, OUTPUT_FILE)
