from flask import Flask, request
from flask_restful import Resource, Api
from .routing.simple_vrp import find_best_route_for
import numpy as np
import math

app = Flask(__name__)


@app.route('/points', methods=['GET', 'POST'])
def points():
    """"
    https://ip/points
    takes a 2D array of points as distance matrix and return the optimized route for these points.
    """
    selected_points = str(request.data).split(',')
    selected_points[0] = selected_points[0][2:]
    selected_points[-1] = selected_points[-1].replace("'", '')
    selected_points = [float(i) for i in selected_points]
    if len(selected_points) <= 2:
        return {"routes": "Select points before routing!"}
    matrix_rows = matrix_columns = math.sqrt(len(selected_points))
    distance_matrix = np.array(selected_points, np.float64).reshape(int(matrix_rows), int(matrix_columns))
    print(distance_matrix)
    routes = find_best_route_for(distance_matrix)
    if routes:
        return {"routes": routes}
    return {
        "routes": "Found no solution!"
    }


if __name__ == '__main__':
    app.run()
