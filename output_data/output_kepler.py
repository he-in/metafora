import pandas as pd
import tracing as tr
import kepler_config
from geojson import LineString, Feature, FeatureCollection, dumps, dump
from keplergl import KeplerGl
from delos_caller import gen_file_command, gen_params_filename


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='#', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def extract_vehicle_movement_log(df: pd.DataFrame):
    tr.log(f"Processing delos trace for vehicle data. This may take over a minute. Please wait...")

    customer_dict = get_customer_served(df)
    customer_dict, _ = map_vehicle2customer(df, customer_dict)
    update_wait_data(customer_dict)
    customer_dropoff = update_dropoff_data(customer_dict)
    vehicle_dict = get_vehicle_movement(df)

    return {**vehicle_dict, **customer_dict, **customer_dropoff}


def extract_customer_movement_log(df: pd.DataFrame):
    tr.log(f"Processing delos trace for customer data. This may take over a minute. Please wait...")

    customer_dict = get_customer_served(df)
    customer_dict, vehicle_dict = map_vehicle2customer(df, customer_dict)
    update_wait_data(customer_dict)
    vehicle_move_dict = get_vehicle_movement2customer(df, customer_dict, vehicle_dict)
    dropoff_dict = update_dropoff_data(customer_dict)

    customer_dict = {**customer_dict, **dropoff_dict, **vehicle_move_dict}
    tr.log(f"Finished trace processing.")

    return customer_dict


def extract_customer_sharing_log(df: pd.DataFrame):
    tr.log(f"Processing delos trace for customer-sharing data. This may take over a minute. Please wait...")

    customer_dict = get_customer_served(df)
    customer_dict, vehicle_dict = map_vehicle2customer(df, customer_dict)
    sharing_dict = find_sharing_customers(vehicle_dict)
    vehicle_movement_dict = get_vehicle_movement2customer_sharing(df, customer_dict, sharing_dict)
    update_pickup_time(customer_dict, sharing_dict, vehicle_movement_dict)

    tr.log(f"Finished trace processing.")

    return vehicle_movement_dict


def update_pickup_time(customer_dict: dict, sharing_dict: dict, vehicle_movement_dict: dict):
    for k, v in vehicle_movement_dict.items():
        vehicle = v["vehicle"]
        sharing_list = sharing_dict[vehicle]

        for sharing in sharing_list:
            if k in sharing:
                first_commuter = sharing[0]
                v["show_time"] = customer_dict[first_commuter]["pickup_time"]


def get_vehicle_movement(df: pd.DataFrame):
    vehicle_dict = {}
    vehicle_state = {}

    data_length = len(df) * 3
    counter = len(df) * 2

    for row in df.itertuples():
        counter += 1
        print_progress_bar(counter, data_length)

        control = row[1]
        if control != "VehicleControl":
            continue
        data_type = row[3]
        if data_type != "MovementLog":
            continue
        vehicle = row[4]

        time = int(row[2])
        latitude = row[6]
        longitude = row[7]
        location_sub_list = [float(longitude), float(latitude), 0, time]

        status_line = row[8]
        if "ChargeDepot" in status_line:
            status = "vehicle_refuelling"
        elif "customer" in status_line:
            status = "vehicle_pickup" if "pickup" in status_line else "vehicle_dropoff"
        else:
            continue

        if vehicle not in vehicle_state.keys():
            vehicle_state[vehicle] = {"key_num": 0, "status": status}
        else:
            if vehicle_state[vehicle]["status"] != status:
                vehicle_state[vehicle]["status"] = status
                vehicle_state[vehicle]["key_num"] += 1

        key_idx = vehicle_state[vehicle]["key_num"]
        key = f"{vehicle}_{status}_{key_idx}"

        if key in vehicle_dict.keys():
            vehicle_dict[key]["location"].append(location_sub_list)
        else:
            vehicle_dict[key] = {"location": [location_sub_list], "key": key, "agent_no": vehicle, "status": status,
                                 "stroke_width": 1}

    tr.log(f"Finished trace processing.")

    return vehicle_dict


def get_customer_served(df: pd.DataFrame, printbar: bool = True):
    customer_dict = {}
    data_length = len(df) * 3
    counter = 0

    for row in df.itertuples():
        counter += 1
        if printbar:
            print_progress_bar(counter, data_length)

        control = row[1]
        if control != "CustomerControl":
            continue

        aborted = row[10]
        if aborted == "TRUE" or aborted is True:
            continue

        customer_id = row[4]
        request_time = int(row[2])

        request_datetime = row[5]

        start_lat = row[6]
        start_lon = row[7]

        end_lat = row[8]
        end_lon = row[9]

        key = f"customer {customer_id}"
        status = "customer_waiting"
        pickup = [float(start_lon), float(start_lat)]
        location_sub_list = [float(start_lon), float(start_lat), 0, request_time]
        end_location = [float(end_lon), float(end_lat)]

        customer_dict[key] = {"location": [location_sub_list], "pickup_point": pickup, "dropoff_point": end_location,
                              "key": key, "agent_no": customer_id, "status": status, "request_time": request_time,
                              "request_datetime": request_datetime, "pickup_time": None, "dropoff_time": None,
                              "vehicle": None, "stroke_width": 3}
    return customer_dict


def map_vehicle2customer(df: pd.DataFrame, customer_dict: dict):
    data_length = len(df) * 3
    counter = len(df)
    vehicle_dict = {}

    for row in df.itertuples():
        counter += 1
        print_progress_bar(counter, data_length)

        control = row[1]
        if control != "VehicleControl":
            continue
        data_type = row[3]
        if data_type == "History":
            time = int(row[2])
            message = row[6]
            vehicle = row[4]
            key = vehicle

            if "StationStatus: Loading" in message:
                customer = message.split("StationStatus: Loading ")[1]
                if customer in customer_dict.keys():
                    customer_dict[customer]["pickup_time"] = time
                    customer_dict[customer]["vehicle"] = vehicle

                    if key in vehicle_dict.keys():
                        if customer in vehicle_dict[key].keys():
                            vehicle_dict[key][customer]["pickup_time"] = time
                        else:
                            vehicle_dict[key][customer] = {"pickup_time": time, "dropoff_time": None}
                    else:
                        vehicle_dict[key] = {}
                        vehicle_dict[key][customer] = {"pickup_time": time, "dropoff_time": None}

            if "StationStatus: Unloading" in message:
                customer = message.split("StationStatus: Unloading ")[1]
                if customer in customer_dict.keys():
                    customer_dict[customer]["dropoff_time"] = time
                    customer_dict[customer]["vehicle"] = vehicle

                    if key in vehicle_dict.keys():
                        if customer in vehicle_dict[key].keys():
                            vehicle_dict[key][customer]["dropoff_time"] = time
                        else:
                            vehicle_dict[key][customer] = {"dropoff_time": time, "pickup_time": None}
                    else:
                        vehicle_dict[key] = {}
                        vehicle_dict[key][customer] = {"dropoff_time": time, "pickup_time": None}

    delete_keys = []
    for key, customer in customer_dict.items():
        if customer["pickup_time"] is None or customer["dropoff_time"] is None:
            delete_keys.append(key)

    for key in delete_keys:
        del customer_dict[key]

    return customer_dict, vehicle_dict


def update_wait_data(customer_dict):
    for key in customer_dict.keys():

        customer = customer_dict[key]
        request_time = customer["request_time"]
        pickup_time = customer["pickup_time"]
        current_location = customer["location"]

        if pickup_time is None:
            continue

        location_list = add_stationary_coordinates(current_location, request_time + 1, pickup_time - 1)
        customer_dict[key]["location"] = location_list


def update_dropoff_data(customer_dict):
    customer_dropoff = {}

    for key in customer_dict.keys():

        if "travel" in key:
            continue
        main_customer = customer_dict[key]
        dropoff_location = main_customer["dropoff_point"]
        dropoff_time = main_customer["dropoff_time"]
        nkey = f"{key}_dp"

        new_location = [dropoff_location[0], dropoff_location[1], 0, dropoff_time]
        customer_dropoff[nkey] = {"location": [new_location], "key": main_customer["key"],
                                  "vehicle": main_customer["vehicle"],
                                  "agent_no": main_customer["agent_no"], "status": "customer_dropoff",
                                  "stroke_width": 3}

        if dropoff_time is None:
            continue

        location_list = add_stationary_coordinates(customer_dropoff[nkey]["location"], dropoff_time + 1,
                                                   dropoff_time + 180)
        customer_dropoff[nkey]["location"] = location_list

    return customer_dropoff


def add_stationary_coordinates(location_list, start_point, end_point):
    dirs = ['no', 'up', 'right', 'down', 'left', 'up']
    count = 0
    move = 10 ** -5
    location = location_list[-1]

    for t in range(start_point, end_point):
        count += 1
        if count >= len(dirs):
            count = 0

        if dirs[count] == "up":
            new_location = location[0] + move, location[1]
        elif dirs[count] == "right":
            new_location = location[0], location[1] + move
        elif dirs[count] == "down":
            new_location = location[0] - move, location[1]
        elif dirs[count] == "left":
            new_location = location[0], location[1] - move
        else:
            new_location = location[0], location[1]

        new_location = [new_location[0], new_location[1], 0, t]
        location_list.append(new_location)
    return location_list


def get_vehicle_movement2customer(df: pd.DataFrame, customer_dict: dict, vehicle_dict: dict):
    customer_movement = {}
    data_length = len(df) * 3
    counter = len(df) * 2

    for row in df.itertuples():
        counter += 1
        print_progress_bar(counter, data_length)

        control = row[1]
        if control != "VehicleControl":
            continue
        data_type = row[3]
        if data_type != "MovementLog":
            continue

        time = int(row[2])
        vehicle = row[4]
        latitude = row[6]
        longitude = row[7]
        location_sub_list = [float(longitude), float(latitude), 0, time]
        status = "travel"

        if vehicle in vehicle_dict:
            vehicle_info = vehicle_dict[vehicle]
        else:
            continue

        for key, value in vehicle_info.items():
            n_key = f"{key}_{status}"
            if (value["pickup_time"] is None or value["pickup_time"] < time) and \
                    (value["dropoff_time"] is None or value["dropoff_time"] > time):
                if n_key in customer_movement.keys():
                    customer_movement[n_key]["location"].append(location_sub_list)
                else:
                    wait_cust = customer_dict[key]
                    customer_movement[n_key] = {"location": [location_sub_list], "key": key,
                                                "agent_no": wait_cust["agent_no"], "status": "customer_travel",
                                                "request_time": wait_cust["request_time"],
                                                "pickup_time": wait_cust["pickup_time"],
                                                "dropoff_time": wait_cust["dropoff_time"],
                                                "vehicle": wait_cust["vehicle"],
                                                "stroke_width": 1}
    return customer_movement


def get_vehicle_movement2customer_sharing(df: pd.DataFrame, customer_dict: dict, vehicle_sharing_dict: dict):
    customer_movement = {}
    data_length = len(df) * 3
    counter = len(df) * 2

    for row in df.itertuples():
        counter += 1
        print_progress_bar(counter, data_length)

        control = row[1]
        if control != "VehicleControl":
            continue
        data_type = row[3]
        if data_type != "MovementLog":
            continue

        time = int(row[2])
        vehicle = row[4]
        latitude = row[6]
        longitude = row[7]
        location_sub_list = [float(longitude), float(latitude), 0, time]

        if vehicle in vehicle_sharing_dict:
            sharing_list = vehicle_sharing_dict[vehicle]
        else:
            continue

        for idx, customer_list in enumerate(sharing_list):
            for order, customer_key in enumerate(customer_list):
                customer = customer_dict[customer_key]
                n_key = f"{customer_key}"
                if (customer["pickup_time"] is None or customer["pickup_time"] < time) and \
                        (customer["dropoff_time"] is None or customer["dropoff_time"] > time):
                    if n_key in customer_movement.keys():
                        customer_movement[n_key]["location"].append(location_sub_list)
                    else:
                        customer_movement[n_key] = {"location": [location_sub_list],
                                                    "key": f"{customer['vehicle']}_{idx}",
                                                    "agent_no": customer["agent_no"], "status": "customer_travel",
                                                    "request_time": customer["request_time"],
                                                    "pickup_time": customer["pickup_time"],
                                                    "dropoff_time": customer["dropoff_time"],
                                                    "pickup_lat": customer["location"][0][1],
                                                    "pickup_lon": customer["location"][0][0],
                                                    "dropoff_lat": customer["dropoff_point"][1],
                                                    "dropoff_lon": customer["dropoff_point"][0],
                                                    "vehicle": customer["vehicle"],
                                                    "order": order + 1,
                                                    "stroke_width": len(customer_list)}

    for key, value in customer_movement.items():
        location = [value["dropoff_lon"], value["dropoff_lat"], 0, value["dropoff_time"]]
        customer_movement[key]["location"].append(location)

    return customer_movement


def find_sharing_customers(vehicle_dict):
    sharing_dict = {}

    for key, vehicle in vehicle_dict.items():
        dropoff_time = 0
        sharing_list = []
        customer_list = []
        for cust_key, customer in vehicle.items():
            if customer["pickup_time"] < dropoff_time:
                customer_list.append(cust_key)
            else:
                if len(customer_list) > 1:
                    sharing_list.append(customer_list)
                customer_list = [cust_key]
            dropoff_time = customer["dropoff_time"]

        if len(sharing_list) > 0:
            sharing_dict[key] = sharing_list

    return sharing_dict


def small_movement_check(longitude, latitude, location):
    return abs(float(longitude) - location[-1][0]) < 0.05 and abs(float(latitude) - location[-1][1]) < 0.05


def dictionary2geojson(vehicle_data: dict, properties: list = ["agent_no", "status", "key", "stroke_width"],
                       savefile=None):
    features = []
    for x in vehicle_data.keys():
        route = LineString(vehicle_data[x]["location"])

        props = {}
        for p in properties:
            props[p] = vehicle_data[x][p]

        features.append(Feature(geometry=route, properties=props))
    feature_collection = FeatureCollection(features)

    if savefile is not None:
        with open(savefile, 'w') as f:
            dump(feature_collection, f)

    return dumps(feature_collection)


def get_config_parameters(customer_data: dict):
    centre_point = [0, 0]
    counter = 0
    start_time = float("inf")

    for key in customer_data.keys():

        if "_dp" in key or "travel" in key:
            continue

        customer = customer_data[key]
        start_coords = customer["location"][0]
        end_coords = customer["dropoff_point"]

        if start_time > customer["request_time"]:
            start_time = customer["request_time"]

        counter += 2
        centre_point[0] += start_coords[0] + end_coords[0]
        centre_point[1] += start_coords[1] + end_coords[1]

    centre_point[0] = centre_point[0] / counter
    centre_point[1] = centre_point[1] / counter

    return centre_point, start_time


def build_kepler_map(delos_trace: str, kepler_file: str, json_file: str, readonly: bool = True):
    import os

    tr.log("Loading trace file.")
    main_df = pd.read_csv(delos_trace)
    vehicle_data = extract_vehicle_movement_log(main_df)
    customer_data = extract_customer_movement_log(main_df)
    sharing_data = extract_customer_sharing_log(main_df)

    if json_file is None:
        vehicle_json = None
        customer_json = None
        sharing_json = None
    else:
        geo_path, geo_ext = os.path.splitext(json_file)[0], os.path.splitext(json_file)[1]
        vehicle_json = f"{geo_path}_veh{geo_ext}"
        customer_json = f"{geo_path}_cus{geo_ext}"
        sharing_json = f"{geo_path}_shr{geo_ext}"

    veh_gjson = dictionary2geojson(vehicle_data, savefile=vehicle_json)
    cus_gjson = dictionary2geojson(customer_data, ["agent_no", "status", "key", "vehicle", "stroke_width"],
                                   savefile=customer_json)
    shr_gjson = dictionary2geojson(sharing_data, ["agent_no", "key", "vehicle", "pickup_time", "dropoff_time",
                                                  "show_time", "pickup_lat", "pickup_lon", "dropoff_lat", "dropoff_lon",
                                                  "order", "stroke_width"],
                                   savefile=sharing_json)

    if kepler_file is None:
        return

    map_centre, map_starttime = get_config_parameters(customer_data)
    kep_path, kep_ext = os.path.splitext(kepler_file)[0], os.path.splitext(kepler_file)[1]

    # create kepler map
    map_1 = KeplerGl()
    map_1.add_data(data=veh_gjson, name='geojson')
    map_1.save_to_html(data={'geojson': veh_gjson}, config=kepler_config.get_vehicle_config(map_centre, map_starttime),
                       file_name=f"{kep_path}_veh{kep_ext}", read_only=readonly)

    map_2 = KeplerGl()
    map_2.add_data(data=cus_gjson, name='geojson')
    map_2.save_to_html(data={'geojson': cus_gjson}, config=kepler_config.get_customer_config(map_centre, map_starttime),
                       file_name=f"{kep_path}_cus{kep_ext}", read_only=readonly)

    map_3 = KeplerGl()
    map_3.add_data(data=shr_gjson, name='geojson')
    map_3.save_to_html(data={'geojson': shr_gjson}, config=kepler_config.get_sharing_config(map_centre, map_starttime),
                       file_name=f"{kep_path}_shr{kep_ext}", read_only=readonly)


def build_kepler_maps(param_run: str, trace_file: str, kepler_file: str, geojson_file: str, speeds=None):
    configs = (param_run[0], param_run[1])
    controls = (param_run[2], param_run[3])
    features = (param_run[4], param_run[5])
    speed_none = False
    kepler_filename = None
    geojson_filename = None

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

                    if kepler_file is not None:
                        kepler_filename = gen_file_command(kepler_file, (params_filename, controls_filename,
                                                                         features_filename, speed_filename))
                    if geojson_file is not None:
                        geojson_filename = gen_file_command(geojson_file, (params_filename, controls_filename,
                                                                           features_filename, speed_filename))

                    build_kepler_map(trace_filename, kepler_filename, geojson_filename)
