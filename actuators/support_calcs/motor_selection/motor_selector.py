import json
import argparse

general = ['name', 'type']
types = ['steering', 'pedal']

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


def main(args):
    fname = args.input_json
    with open(fname) as f:
        scenarios = json.load(f)

    output_data = []
    for data in scenarios:
        for key in general:
            assert key in data, "Missing '{}' in input json".format(key)

        assert data['type'] in types, "'type' may only be {}".format(types)

        if data['type'] == "steering":
            # Data assertions
            for key in steering.keys():
                assert key in data, "Missing '{}' in input json".format(key)
                for prop_type in steering[key].keys():
                    assert prop_type in data[key], "Missing '{}:{}' in input json".format(key, prop_type)
                    for prop in steering[key][prop_type]:
                        assert prop in data[key][prop_type], "Missing '{}:{}:{}' in input json".format(key, prop_type, prop)

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
            print("Pedal calculations coming soon")
            pass

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
