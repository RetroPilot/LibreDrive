import json
import argparse

general = ['name', 'type']
types = ['steering', 'pedal','hydro']

steering = {
    'inputs': {
        'forces': ['steering_torque_Nm', 'peak_rate_deg/s'],
        'dimensions': ['drive_wheel_dia_mm', 'driven_ring_dia_mm', 'gearbox_ratio'],
        'electrical': ['voltage_V']
    },
    'outputs': {
        'forces': ['motor_torque_Nm', 'motor_velocity_RPM', 'tension_N'],
        'electrical': ['estimated_power_W', 'estimated_current_A']
    }
}

pedal = {
    'inputs': {
        'forces': ['pedal_force_N', 'peak_actuation_time_s', 'travel_distance_mm'],
        'dimensions': ['driven_pulley_dia_mm', 'gear_ratio', 'gearbox_ratio'],
        'electrical': ['voltage_V']
    },
    'outputs': {
        'forces': ['motor_torque_Nm', 'motor_velocity_RPM'],
        'electrical': ['estimated_power_W', 'estimated_current_A']
    }
}

hydro = {
    'inputs': {
        'forces': ['output_pressure_KPa', 'peak_actuation_time_s', 'travel_distance_mm'],
        'dimensions': ['gear_ratio', 'gearbox_ratio', 'cylinder_bore_mm'],
        'electrical': ['voltage_V']
    },
    'outputs': {
        'forces': ['pushrod_force_N', 'motor_torque_Nm', 'motor_velocity_RPM', 'drive_gear_velocity_RPM', 'driven_rack_velocity_mm/s'],
        'electrical': ['estimated_power_W', 'estimated_current_A']
    }
}

pi = 3.141592653589793

def assert_data_format(data, data_format):
    for key in data_format.keys():
        assert key in data, "Missing '{}' in input json".format(key)
        for prop_type in data_format[key].keys():
            assert prop_type in data[key], "Missing '{}:{}' in input json".format(key, prop_type)
            for prop in data_format[key][prop_type]:
                assert prop in data[key][prop_type], "Missing '{}:{}:{}' in input json".format(key, prop_type, prop)


def main(args):
    fname = args.input_json
    with open(fname) as f:
        scenarios = json.load(f)

    output_data = []
    for data in scenarios:
        for key in general:
            assert key in data, "Missing '{}' in input json".format(key)

        assert data['type'] in types, "'type' may only be {}".format(types)

        if data['type'] == 'steering':
            # Data assertions
            assert_data_format(data, steering)

            # inputs
            steering_torque_Nm = data['inputs']['forces']['steering_torque_Nm']
            peak_rate_dps = data['inputs']['forces']['peak_rate_deg/s']
            drive_wheel_dia_mm = data['inputs']['dimensions']['drive_wheel_dia_mm']
            driven_ring_dia_mm = data['inputs']['dimensions']['driven_ring_dia_mm']
            gearbox_ratio = data['inputs']['dimensions']['gearbox_ratio']
            voltage_V = data['inputs']['electrical']['voltage_V']

            # outputs
            precision = args.precision
            tension_N = steering_torque_Nm / (driven_ring_dia_mm/1000/2)
            motor_torque_Nm = tension_N * (drive_wheel_dia_mm/1000/2)/gearbox_ratio
            motor_velocity_RPM = peak_rate_dps/360*gearbox_ratio*(driven_ring_dia_mm/drive_wheel_dia_mm)*60
            estimated_power_W = motor_torque_Nm*motor_velocity_RPM/9.5488
            estimated_current_A = estimated_power_W/voltage_V

            data['outputs']['forces']['tension_N'] = round(tension_N, precision)
            data['outputs']['forces']['motor_torque_Nm'] = round(motor_torque_Nm, precision)
            data['outputs']['forces']['motor_velocity_RPM'] = round(motor_velocity_RPM, precision)

            data['outputs']['electrical']['estimated_power_W'] = round(estimated_power_W, precision)
            data['outputs']['electrical']['estimated_current_A'] = round(estimated_current_A, precision)

        elif data['type'] == "pedal":
            # Data assertions
            assert_data_format(data, pedal)

            # inputs
            pedal_force_N = data['inputs']['forces']['pedal_force_N']
            peak_actuation_time_s = data['inputs']['forces']['peak_actuation_time_s']
            travel_distance_mm = data['inputs']['forces']['travel_distance_mm']
            driven_pulley_dia_mm = data['inputs']['dimensions']['driven_pulley_dia_mm']
            gear_ratio = data['inputs']['dimensions']['gear_ratio']
            gearbox_ratio = data['inputs']['dimensions']['gearbox_ratio']
            voltage_V = data['inputs']['electrical']['voltage_V']

            # outputs
            precision = args.precision
            pulley_velocity_rps = travel_distance_mm/peak_actuation_time_s / (pi*driven_pulley_dia_mm)
            pulley_torque_Nm = pedal_force_N * (driven_pulley_dia_mm/2)/1000
            gearbox_torque_Nm = pulley_torque_Nm / gear_ratio
            motor_torque_Nm = gearbox_torque_Nm / gearbox_ratio
            motor_velocity_RPM = pulley_velocity_rps * gear_ratio * gearbox_ratio * 60
            estimated_power_W = motor_torque_Nm * motor_velocity_RPM / 9.5488
            estimated_current_A = estimated_power_W / voltage_V

            data['outputs']['forces']['motor_torque_Nm'] = round(motor_torque_Nm, precision)
            data['outputs']['forces']['motor_velocity_RPM'] = round(motor_velocity_RPM, precision)

            data['outputs']['electrical']['estimated_power_W'] = round(estimated_power_W, precision)
            data['outputs']['electrical']['estimated_current_A'] = round(estimated_current_A, precision)

        elif data['type'] == 'hydro':
            # Data assertions
            assert_data_format(data, hydro)

            # inputs
            output_pressure_KPa = data['inputs']['forces']['output_pressure_KPa']
            peak_actuation_time_s = data['inputs']['forces']['peak_actuation_time_s']
            travel_distance_mm = data['inputs']['forces']['travel_distance_mm']
            drive_gear_dia_mm = data['inputs']['dimensions']['drive_gear_dia_mm']
            cylinder_bore_mm = data['inputs']['dimensions']['cylinder_bore_mm']
            pedal_ratio = data['inputs']['dimensions']['pedal_ratio']
            gear_ratio = data['inputs']['dimensions']['gear_ratio']
            gearbox_ratio = data['inputs']['dimensions']['gearbox_ratio']
            voltage_V = data['inputs']['electrical']['voltage_V']

            # outputs
            precision = args.precision
            bore_area_m2 = pi*(cylinder_bore_mm/1000/2)**2
            pushrod_force_N = output_pressure_KPa * 1000 * bore_area_m2
            effective_pedal_force_N = pushrod_force_N / pedal_ratio
            motor_torque_Nm = pushrod_force_N * (drive_gear_dia_mm/1000/2) / (gear_ratio * gearbox_ratio)
            drive_gear_RPS = travel_distance_mm/peak_actuation_time_s / (pi*drive_gear_dia_mm)
            driven_rack_velocity_mmps = drive_gear_dia_mm * pi * drive_gear_RPS
            drive_gear_velocity_RPM = drive_gear_RPS * 60
            motor_velocity_RPM = drive_gear_velocity_RPM * gear_ratio * gearbox_ratio
            estimated_power_W = motor_torque_Nm * motor_velocity_RPM / 9.5488
            estimated_current_A = estimated_power_W / voltage_V

            data['outputs']['forces']['pushrod_force_N'] = round(pushrod_force_N, precision)
            data['outputs']['forces']['effective_pedal_force_N'] = round(effective_pedal_force_N, precision)
            data['outputs']['forces']['motor_torque_Nm'] = round(motor_torque_Nm, precision)
            data['outputs']['forces']['motor_velocity_RPM'] = round(motor_velocity_RPM, precision)
            data['outputs']['forces']['drive_gear_velocity_RPM'] = round(drive_gear_velocity_RPM, precision)
            data['outputs']['forces']['driven_rack_velocity_mm/s'] = round(driven_rack_velocity_mmps, precision)

            data['outputs']['electrical']['estimated_power_W'] = round(estimated_power_W, precision)
            data['outputs']['electrical']['estimated_current_A'] = round(estimated_current_A, precision)

        output_data.append(data)

    with open(fname, 'w') as f:
        json.dump(output_data, f, indent=4)

    if args.verbose:
        print(json.dumps(output_data, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_json', default='scenarios.json', help='json file to compute values')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='set to print values')
    parser.add_argument('-p', '--precision', default=4, type=int, help='number of digits to return')

    args = parser.parse_args()
    main(args)
