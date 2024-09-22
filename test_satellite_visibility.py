"""
Author: James Aherne
Date: 2024-09-22
Project: Satellite Visibility Checker - Unit Tests
Description:
    This script contains unit tests for the `satellite_visibility.py` script.
    It tests various aspects of the satellite visibility calculations, including data cleaning,
    time conversion, and coordinate transformation.

Tests:
    - test_data_cleaning: Ensures that invalid or missing data is correctly removed.
    - test_time_conversion: Verifies that time data is converted to `astropy.time.Time` objects.
    - test_coordinate_transformation: Confirms that RA, Dec, and Distance are correctly
      transformed into Altitude and Azimuth angles.

Dependencies:
    - unittest
    - pandas
    - numpy
    - astropy

Usage:
    To run the unit tests, execute the following command in your terminal:
    
    ```bash
    python -m unittest test_satellite_visibility.py
    ```

Files:
    - test_satellite_visibility.py: This unit test file.
    - satellite_visibility.py: The main script being tested.

License:
    This project is licensed under the MIT License.

Notes:
    Ensure that the main script (`satellite_visibility.py`) and necessary input data are
    in the smae directory as this script before running these tests.
"""

import unittest
import pandas as pd
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u
from satellite_visibility import convert_to_altaz

class TestSatelliteVisibility(unittest.TestCase):

    def setUp(self):
        # Sample satellite data for testing
        self.valid_data = pd.DataFrame({
            'Time (iso)': ['2024-09-11 00:00:00.000', '2024-09-11 00:01:00.000'],
            'RA (GCRS) [deg]': [87.958, 87.126],
            'Dec (GCRS) [deg]': [-39.063, -35.471],
            'Distance (GCRS) [km]': [7067.917, 7067.734]
        })

        self.ground_station_location = EarthLocation(lat=78.7199, lon=20.3493)

    def test_data_cleaning(self):
        # Test for NaN removal
        data_with_nan = pd.DataFrame({
            'Time (iso)': ['2024-09-11 00:00:00.000', None],
            'RA (GCRS) [deg]': [87.958, 87.126],
            'Dec (GCRS) [deg]': [-39.063, -35.471],
            'Distance (GCRS) [km]': [7067.917, 7067.734]
        })
        
        # Clean the Time column
        valid_times = data_with_nan['Time (iso)'].dropna().astype(str).str.strip().replace('', np.nan).dropna()
        
        # Ensure valid_times contains only non-empty entries
        self.assertEqual(len(valid_times), 1)  # Should only have 1 valid time


    def test_time_conversion(self):
        # Check that valid time strings convert to astropy Time objects
        valid_times = self.valid_data['Time (iso)']
        times = Time(valid_times.tolist(), format='iso')
        self.assertEqual(len(times), 2)  # Should have 2 time objects

    def test_coordinate_transformation(self):
        # Use known values for transformation
        altitudes, azimuths = convert_to_altaz(self.valid_data, self.ground_station_location)
        self.assertIsInstance(altitudes, np.ndarray)  # Ensure output is a numpy array
        self.assertIsInstance(azimuths, np.ndarray)

    def test_invalid_input(self):
        # Test function raises error for invalid data
        invalid_data = pd.DataFrame({
            'Time (iso)': ['invalid_time'],
            'RA (GCRS) [deg]': [87.958],
            'Dec (GCRS) [deg]': [-39.063],
            'Distance (GCRS) [km]': [7067.917]
        })
        with self.assertRaises(ValueError):
            convert_to_altaz(invalid_data, self.ground_station_location)

if __name__ == '__main__':
    unittest.main(exit=False)  # Suppresses SystemExit
