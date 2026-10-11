from astro_tools.core.basic import circular_velocity
from astro_tools.utils.utility import open_yaml_file
from astro_tools.data.constants import G, day, year, au, earth_radius
import argparse
from pathlib import Path
from importlib.resources import files


data_path = files("astro_tools.data").joinpath("constants.yaml")
yaml_constants = open_yaml_file(data_path)
PLANET_DATA = yaml_constants["SOL_DATA"]

SPACING = 25

def present_v_circ(HOST_NAME, HOST_RAD, v_circ, r):
    v_circ_km = v_circ/1000
    ms_to_kmh = (1e-3) * 60 * 60
    
    print(f"{'Host:':<{SPACING}} {HOST_NAME} \n{'Distance (Altitude):':<{SPACING}} {r/1000:,} ({(r-HOST_RAD)/1000:,}) km")
    print(f"{'Orbital Velocity:':<{SPACING}} {v_circ_km:,.3f} km/s")
    print(f"{'':<{SPACING}} {(v_circ*ms_to_kmh):,.3f} km/h")

def present_body_data(planet):
    select_data = PLANET_DATA[planet]
    print(planet.upper())
    for key in select_data.keys():
        key_pres = key.capitalize()
        value = select_data[key]
        scale = 1
        SF = 5                            
        unit = ""
        add_text = ""
        UNIT_SPACING = 12
        
        if key == "mass":
            unit = "kg"
            scale = 1
            
        elif key == "radius":
            unit = "km"
            scale = 1e-3 # present in km
            
            unit_2 = r"R_Earth"
            scale_2 = 1/earth_radius 
            val_str = f"{value*scale_2:,.{SF}g}"
            add_text = f"{f'':<{SPACING}} {val_str:<{UNIT_SPACING}} {unit_2}"
            
        elif key == "sma":
            key_pres = "Semi-Major Axis"
            unit = "km"
            scale = 1e-3
            
            unit_2 = r"AU"
            scale_2 = 1/au 
            val_str = f"{value*scale_2:,.{SF}g}"
            add_text = f"{f'':<{SPACING}} {val_str:<{UNIT_SPACING}} {unit_2}"
 
        elif key == "period":
            unit = "yrs"
            scale = 1/year
            
        elif key == "rotation_period":
            unit = "days"
            scale = 1/day
            SF = 3
        
        val_str = f"{value*scale:,.{SF}g}"
        print(f"{f'{key_pres}:':<{SPACING}} {val_str:<{UNIT_SPACING}} {unit}")
        
        if add_text != "":
            print(add_text)


def v_circ() -> None:
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
    present_v_circ(HOST_NAME, HOST_RAD, v_circ, r)    
    
    
def info() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--planet", type=str, required=True, default="earth", help="The object of interest")
    
    args  = parser.parse_args()
    
    planet = args.planet.lower()
    
    present_body_data(planet)   

        
if __name__ == "__main__":
    info()