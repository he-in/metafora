import pandas as pd
import time
import os

from folium import Map
from folium.plugins import HeatMap
from selenium import webdriver

import branca.colormap
from collections import defaultdict

from delos_caller import gen_file_command, gen_params_filename


def extract_emissions_log(df: pd.DataFrame):
    nox_emissions_dict = {}
    pm_emissions_dict = {}
    vehicle_dict = {}

    for row in df.itertuples():

        control = row[1]
        if control != "VehicleControl":
            continue
        data_type = row[3]
        if data_type != "MovementLog":
            continue
        vehicle = row[4]

        latitude = row[6]
        longitude = row[7]
        nox_emission = float(row[9])
        pm_emission = float(row[10])
        location_key = f"{longitude}_{latitude}"

        if vehicle not in vehicle_dict.keys():
            nox = nox_emission
            pm = pm_emission
            vehicle_dict[vehicle] = {"nox": [nox_emission], "pm": [pm_emission]}
        else:
            nox = nox_emission - vehicle_dict[vehicle]["nox"][-1]
            pm = pm_emission - vehicle_dict[vehicle]["pm"][-1]
            vehicle_dict[vehicle]["nox"].append(nox_emission)
            vehicle_dict[vehicle]["pm"].append(pm_emission)

        if location_key not in nox_emissions_dict.keys():
            nox_emissions_dict[location_key] = {}
            nox_emissions_dict[location_key]["value"] = nox
            nox_emissions_dict[location_key]["latitude"] = latitude
            nox_emissions_dict[location_key]["longitude"] = longitude
        else:
            nox_emissions_dict[location_key]["value"] += nox

        if location_key not in pm_emissions_dict.keys():
            pm_emissions_dict[location_key] = {}
            pm_emissions_dict[location_key]["latitude"] = latitude
            pm_emissions_dict[location_key]["longitude"] = longitude
            pm_emissions_dict[location_key]["value"] = pm
        else:
            pm_emissions_dict[location_key]["value"] += pm

    return nox_emissions_dict, pm_emissions_dict


def create_node_dictionary(data_dict: dict, initial_value: float = 1, value_per_point: float = 0.5):

    map_dict = {}

    for key, value in data_dict.items():
        emissions = value["value"]

        num = 0
        while emissions > initial_value + num * value_per_point:
            map_dict[f"{key}_{num}"] = {"latitude": value["latitude"], "longitude": value["longitude"]}
            num += 1

    return map_dict


def generate_html_map(data: pd.DataFrame, filename:str=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    save_at = filename
    if filename is None:
        save_at = f'{dir_path}/map.html'

    sw = [data.latitude.values.min(), data.longitude.values.min()]
    ne = [data.latitude.values.max(), data.longitude.values.max()]
    if "nox" in filename:
        captiontxt = "Relative NOx Levels"
    elif "pm" in filename:
        captiontxt = "Relative PM Levels"
    else:
        captiontxt = "Relative Levels"
    steps = 21

    # min_val = min(data.latitude.values, data.longitude.values)
    # max_val = max(data.latitude.values, data.longitude.values)
    # dif_val = max_val - min_val
    colormap = branca.colormap.LinearColormap(colors=['navy', 'blue', 'lime', 'yellow', 'red'],
                                              index=[0.1, 0.4, 0.65, 0.85, 1]).to_step(steps)
    colormap.caption = captiontxt
    # colormap = branca.colormap.ColorMap.to_step(steps)
    # colormap = branca.colormap.rainbow.scale(0, 1).to_step(steps)
    gradient_dict = defaultdict(dict)
    for i in range(steps):
        gradient_dict[1 / steps * i] = colormap.rgb_hex_str(1 / steps * i)

    hmap = Map()
    hm_wide = HeatMap(
        list(zip(data.latitude.values, data.longitude.values)),
        min_opacity=0.2,
        radius=6,
        blur=6,
        gradient=gradient_dict
    )

    hmap.add_child(hm_wide)
    colormap.add_to(hmap)

    hmap.fit_bounds([sw, ne])
    hmap.save(save_at)


def html2png(filename: str, map_type: str, html_location=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.splitext(filename)[0]
    output_ext = os.path.splitext(filename)[1]

    load_from = html_location
    if html_location is None:
        load_from = f'{dir_path}/map.html'

    browser = webdriver.Firefox()
    browser.get(fr'file:///{load_from}')
    time.sleep(1)  # Give the map tiles some time to load
    browser.save_screenshot(f'{output_path}_{map_type}{output_ext}')
    browser.quit()
    # os.remove(load_from)


def build_emissions_heatmap(trace_file, output_name):

    main_df = pd.read_csv(trace_file)
    nox_data, pm_data = extract_emissions_log(main_df)
    nox_map = create_node_dictionary(nox_data, initial_value=0.01, value_per_point=0.005)
    pm_map = create_node_dictionary(pm_data, initial_value=0.0001, value_per_point=0.00005)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.splitext(output_name)[0]
    output_ext = os.path.splitext(output_name)[1]

    for_map = pd.DataFrame.from_dict(nox_map, orient='index')
    generate_html_map(for_map, output_path + "_nox.html")

    # html2png(output_name, output_path + "_nox.html")

    for_map = pd.DataFrame.from_dict(pm_map, orient='index')
    generate_html_map(for_map, output_path + "_pm.html")
    # html2png(output_name, "pm")


def build_emission_maps(param_run: str, trace_file: str, emission_file: str, speeds=None):
    configs = (param_run[0], param_run[1])
    controls = (param_run[2], param_run[3])
    features = (param_run[4], param_run[5])
    speed_none = False
    emission_filename = None

    if speeds is None:
        speeds = [0]
        speed_none = True

    for s in speeds:
        if speed_none:
            speed_filename = ""
        else:
            speed_filename = f"sp{s}"

        for f_values in features[1]:
            features_filename = gen_params_filename(features[0], f_values)

            for c_values in controls[1]:
                controls_filename = gen_params_filename(controls[0], c_values)

                for p_values in configs[1]:
                    params_filename = gen_params_filename(configs[0], p_values)
                    trace_filename = gen_file_command(trace_file, (params_filename, controls_filename,
                                                      features_filename, speed_filename))

                    if emission_file is not None:
                        emission_filename = gen_file_command(emission_file, (params_filename, controls_filename,
                                                             features_filename, speed_filename))

                    build_emissions_heatmap(trace_filename, emission_filename)
