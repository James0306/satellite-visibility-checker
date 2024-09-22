"""
Author: James Aherne
Date: 2024-09-22
Project: Satellite Visibility Checker - Unit Tests
Description:
    This script contains unit tests for the `satellite_visibility.py` script.
    It tests various aspects of the satellite visibility calculations, including data cleaning,
    time conversion, and coordinate transformation.

Tests:
    - test_clean_time_column: Ensures that invalid or missing time data is correctly removed.
    - test_time_conversion: Verifies that time data is converted to `astropy.time.Time` objects.
    - test_coordinate_transformation: Confirms that RA, Dec, and Distance are correctly
      transformed into Altitude and Azimuth angles.

Dependencies:
    - unittest
    - pandas
    - numpy
    - astropy

Notes:
    Ensure that the main script (`satellite_visibility.py`) and necessary input data are
    in the same directory as this script before running these tests.
"""

##########################################IMPORTS##########################################

import unittest
import pandas as pd
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u
from satellite_visibility import clean_time_column, convert_to_altaz

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

    def test_clean_time_column(self):
        # Test for NaN removal and cleaning of time data
        data_with_nan = pd.DataFrame({
            'Time (iso)': ['2024-09-11 00:00:00.000', None, ' '],
            'RA (GCRS) [deg]': [87.958, 87.126, 87.500],
            'Dec (GCRS) [deg]': [-39.063, -35.471, -36.000],
            'Distance (GCRS) [km]': [7067.917, 7067.734, 7070.000]
        })
        
        # Clean the Time column using the new clean_time_column function
        cleaned_times = clean_time_column(data_with_nan)
        
        # Ensure only valid times are returned
        self.assertEqual(len(cleaned_times), 1)  # Should only have 1 valid time
        self.assertEqual(cleaned_times.isot[0], '2024-09-11T00:00:00.000')  # Ensure correct time remains

    def test_time_conversion(self):
        # Check that valid time strings convert to astropy Time objects
        times = clean_time_column(self.valid_data)
        self.assertEqual(len(times), 2)  # Should have 2 time objects
        self.assertIsInstance(times, Time)

    def test_coordinate_transformation(self):
            # Check altitude values
            altitudes = convert_to_altaz(self.valid_data, Time(self.valid_data['Time (iso)'].tolist(), format='iso'), self.ground_station_location)
            self.assertIsInstance(altitudes, np.ndarray)  # Ensure output is a numpy array
            self.assertEqual(len(altitudes), len(self.valid_data))  # Should have the same number of altitude values as input data

    def test_invalid_input(self):
        # Test function raises error for invalid data
        invalid_data = pd.DataFrame({
            'Time (iso)': ['invalid_time'],
            'RA (GCRS) [deg]': [87.958],
            'Dec (GCRS) [deg]': [-39.063],
            'Distance (GCRS) [km]': [7067.917]
        })
        with self.assertRaises(ValueError):
            times = clean_time_column(invalid_data)
            convert_to_altaz(invalid_data, times, self.ground_station_location)

if __name__ == '__main__':
    unittest.main(exit=False)  # Suppresses SystemExit
