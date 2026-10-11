from astro_tools.core.basic import circular_velocity
from astro_tools.utils.utility import open_yaml_file
from astro_tools.data.constants import G
import argparse
from pathlib import Path
from importlib.resources import files


data_path = files("astro_tools.data").joinpath("constants.yaml")
yaml_constants = open_yaml_file(data_path)
PLANET_DATA = yaml_constants["SOL_DATA"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="earth", help="The body being orbited")
    parser.add_argument("--altitude", type=float, help="Altitude above body's surface in metres")
    parser.add_argument("--sma", type=float, help="Distance from body's centre of mass in metres")

    args = parser.parse_args()
    
    if args.host == None:
        host = "earth"
    else:
        host = args.host.lower()
    
    HOST_NAME = host.capitalize()
    HOST_RAD = PLANET_DATA[host]["radius"] # radius in metres     
    HOST_MASS = PLANET_DATA[host]["mass"] # mass in kilograms
    
    if (args.altitude == None) and (args.sma == None):
        r = HOST_RAD + 3e+5 # default to 100km above the surface
    elif args.sma == None:
        r = HOST_RAD + args.altitude
    elif args.altitude == None: 
        r = args.sma
    else:
        raise ValueError("Cannot input a value for both altitude and semi-major axis")

    mu = G * HOST_MASS
    
    v_circ = circular_velocity(mu, r)
    v_circ_km = v_circ/1000
    ms_to_kmh = (1e-3) * 60 * 60
    
    SPACING = 25
    print(f"{'Host:':<{SPACING}} {HOST_NAME} \n{'Distance (Altitude):':<{SPACING}} {r/1000:,} ({(r-HOST_RAD)/1000:,}) km")
    print(f"{'Orbital Velocity:':<{SPACING}} {v_circ_km:,.3f} km/s")
    print(f"{'':<{SPACING}} {(v_circ*ms_to_kmh):,.3f} km/h")
    
    
if __name__ == "__main__":
    main()