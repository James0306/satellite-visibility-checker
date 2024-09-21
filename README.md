This project contains a Python script that calculates the visibility of a satellite from a specified ground station location using satellite position data. The project also includes unit tests to ensure the correctness of the main functionality.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage-of-satellite-visibility-analysis)
- [Unit Tests](#unit-tests-for-satellite-visibility-analysis)
  - [Test Coverage](#test-coverage)
  - [Running the Tests](#running-the-tests)


# Installation

To run this project, you need to have Python installed on your system. This project has been developed using Python 3.11.

## To Install:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/satellite_visibility.git
   cd satellite_visibility
   ```

# Usage of Satellite Visibility Analysis

This section outlines how to use the Satellite Visibility Analysis script to determine the visibility of a satellite from a specified ground station.

## Running the Main Script

To analyze satellite visibility, follow these steps:

1. **Prepare Your Input Data**:
   Ensure you have a CSV file containing satellite position data in the specified format. The CSV should include the following columns:
   - `Time (iso)`: ISO formatted timestamps (e.g., `2024-09-11T00:00:00Z`)
   - `RA (GCRS) [deg]`: Right Ascension in degrees (e.g., `87.958413`)
   - `Dec (GCRS) [deg]`: Declination in degrees (e.g., `-39.063465`)
   - `Distance (GCRS) [km]`: Distance from the center of the Earth in kilometers (e.g., `7067.917061`)

2. **Run the Script**:
   Open your Command Prompt (cmd), navigate to the project directory, and execute the main script using the following commands:
   ```bash
   cd "C:\Users\jtahe\Documents\Python Projects\Blue Skies Space"
   python satellite_visibility.py
   ```


This section outlines how to use the Satellite Visibility Analysis script to determine the visibility of a satellite from a specified ground station.

# Unit Tests for Satellite Visibility Analysis

This section provides information on how to run unit tests for the Satellite Visibility Analysis project. The unit tests ensure that the main functionality of the project works as expected.

## Test Coverage

The unit tests cover the following scenarios:

1. **Data Cleaning:** Ensures that the `Time (iso)` column is correctly processed, and any missing or invalid data is removed.
2. **Time Conversion:** Verifies that the `Time (iso)` values are correctly converted to `astropy.time.Time` objects.
3. **Coordinate Transformation:** Confirms that the satellite's RA, Dec, and Distance are transformed into Altitude and Azimuth using the ground station's location.

To ensure full coverage of the code, consider adding additional tests for edge cases, including handling of malformed CSV data or boundary conditions for elevation.

## Running the Tests

To run the unit tests, use the following command in your terminal:

```bash
python -m unittest test_satellite_visibility.py
```

