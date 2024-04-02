from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

# Your chart data mapped to the corresponding launch angles
chart_data = {
    75: [44, 79, 131, 180, 205, 218, 242, 254, 256],
    80: [46, 86, 145, 202, 229, 243, 268, 280, 280],
    85: [48, 93, 161, 224, 254, 269, 295, 306, 305],
    90: [50, 100, 177, 248, 280, 323, 333, 329],
    92: [51, 103, 183, 258, 291, 307, 334, 343, 338],
    95: [52, 107, 194, 273, 307, 324, 351, 359, 352],
    100: [54, 114, 211, 298, 335, 351, 379, 385, 376],
    105: [55, 122, 229, 325, 364, 382, 408, 412, 399]
}
# Angles provided in the chart, corresponding to the distance values
angles = [0, 5, 10, 15, 18, 20, 25, 30, 35]

# Function to lookup distance based on exit speed and launch angle
def lookup_distance(exit_speed, launch_angle):
    # Find the closest speeds in the chart
    speeds = sorted(chart_data.keys())
    lower_speed = max([s for s in speeds if s <= exit_speed])
    upper_speed = min([s for s in speeds if s >= exit_speed], default=lower_speed)
    
    # Interpolate distance for the closest speeds
    lower_distance = np.interp(launch_angle, angles, chart_data[lower_speed])
    upper_distance = np.interp(launch_angle, angles, chart_data[upper_speed])
    
    # Now interpolate between the two speeds
    if lower_speed == upper_speed:
        return lower_distance
    else:
        final_distance = lower_distance + (upper_distance - lower_distance) * ((exit_speed - lower_speed) / (upper_speed - lower_speed))
        return final_distance

# API endpoint to calculate distance
@app.route('/calculate_distance', methods=['GET'])
def api_calculate_distance():
    try:
        # Assuming the exit speed is provided in mph, we convert it to m/s by multiplying by 0.44704
        velocity_mph = float(request.args.get('velocity'))
        velocity_mps = velocity_mph * 0.44704
        angle = float(request.args.get('angle'))
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    
    distance = lookup_distance(velocity_mph, angle)
    return jsonify({"exit_speed_mph": velocity_mph, "launch_angle_degrees": angle, "projected_distance_feet": distance})

if __name__ == '__main__':
    app.run(debug=True)
