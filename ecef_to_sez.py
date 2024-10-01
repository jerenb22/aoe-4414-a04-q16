# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
# This script converts ECEF coordinates to SEZ (South-East-Zenith) coordinates.
#
# Parameters:
# o_x_km: X-coordinate of the ECEF origin (observer) in kilometers
# o_y_km: Y-coordinate of the ECEF origin (observer) in kilometers
# o_z_km: Z-coordinate of the ECEF origin (observer) in kilometers
# x_km: X-coordinate of the ECEF position in kilometers
# y_km: Y-coordinate of the ECEF position in kilometers
# z_km: Z-coordinate of the ECEF position in kilometers
#
# Output:
# Prints the corresponding SEZ coordinates in kilometers.
#
# Written by: Jeren Browder
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

import sys
import math

# Helper function to compute latitude and longitude from ECEF
def ecef_to_lat_lon(o_x_km, o_y_km, o_z_km):
    """
    Convert ECEF coordinates to latitude and longitude.

    Args:
        o_x_km (float): X-coordinate of the observer's origin in ECEF (kilometers).
        o_y_km (float): Y-coordinate of the observer's origin in ECEF (kilometers).
        o_z_km (float): Z-coordinate of the observer's origin in ECEF (kilometers).

    Returns:
        tuple: (latitude in degrees, longitude in degrees).
    """
    # Compute longitude (in radians)
    lon_rad = math.atan2(o_y_km, o_x_km)
    
    # Compute hypotenuse of x and y
    hyp = math.sqrt(o_x_km ** 2 + o_y_km ** 2)
    
    # Compute latitude (in radians)
    lat_rad = math.atan2(o_z_km, hyp)

    # Convert radians to degrees
    lat_deg = math.degrees(lat_rad)
    lon_deg = math.degrees(lon_rad)

    return lat_deg, lon_deg

# Helper function: Convert ECEF to SEZ
def ecef_to_sez(o_x_km, o_y_km, o_z_km, x_km, y_km, z_km):
    """
    Convert ECEF coordinates to SEZ coordinates.
    
    Args:
        o_x_km (float): X-coordinate of the observer's origin in ECEF (kilometers).
        o_y_km (float): Y-coordinate of the observer's origin in ECEF (kilometers).
        o_z_km (float): Z-coordinate of the observer's origin in ECEF (kilometers).
        x_km (float): X-coordinate of the point in ECEF (kilometers).
        y_km (float): Y-coordinate of the point in ECEF (kilometers).
        z_km (float): Z-coordinate of the point in ECEF (kilometers).

    Returns:
        tuple: SEZ coordinates (s, e, z) in kilometers.
    """
    # Compute latitude and longitude of the observer
    lat_deg, lon_deg = ecef_to_lat_lon(o_x_km, o_y_km, o_z_km)
    
    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(lat_deg)
    lon_rad = math.radians(lon_deg)

    # Calculate the difference between the point and the observer's origin
    dx = x_km - o_x_km
    dy = y_km - o_y_km
    dz = z_km - o_z_km

    # Rotation matrix components based on observer's latitude and longitude
    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)
    sin_lon = math.sin(lon_rad)
    cos_lon = math.cos(lon_rad)

    # Apply the rotation matrix to convert ECEF to SEZ
    s_km = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
    e_km = -sin_lon * dx + cos_lon * dy
    z_km = cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz

    return s_km, e_km, z_km

# Main function
def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 7:
        print("Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km")
        sys.exit(1)

    # Parse the input arguments
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])

    # Convert ECEF coordinates to SEZ
    s_km, e_km, z_km = ecef_to_sez(o_x_km, o_y_km, o_z_km, x_km, y_km, z_km)

    # Print the resulting SEZ coordinates
    print(s_km)
    print(e_km)
    print(z_km)

if __name__ == "__main__":
    main()