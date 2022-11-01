"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
from scipy.spatial import distance_matrix


def create_data_model(distance_matrix):
    """
    Stores the data needed to solve the VRP problem.
    such as (Distance Matrix), (number of vehicles) and (starting point\s -> (depot))
    """
    data = {}
    data['distance_matrix'] = distance_matrix
    """pre-process the distance matrix to create custom routing behavior"""
    data['distance_matrix'] = process_distance_matrix(data['distance_matrix'])
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def generate_distance_matrix(points):
    """
    can be used to generate distance matrix from (x, y) list of points or (lat, long) array
    :param points:
    :return: 2D array (distance matrix)
    """
    # generate fake titles for each column in the dataframe
    ctys = ['E40'] * len(points)
    df = pd.DataFrame(points, columns=['xcord', 'ycord'], index=ctys)
    dm = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
    # make distance matrix values a bit bigger to make sure we can optimize it.
    dm = dm * 1000
    # convert our dataframe to numpy array to remove fake titles and indexing
    dm = pd.DataFrame(dm).astype(int).to_numpy()
    return dm


def process_distance_matrix(dis_matrix):
    """
    pre-process distance matrix to make sure that every vehicle go from one starting points to
    its associated exit point.

    the distance matrix is transformed in a way that makes every:
    entry point values -> all points are high except its exit.
    exit point values -> all entry points except the one it came from
    """

    # check if the current point is entry point else it is exit point
    def is_entry(index):
        return index % 2 == 0

    # distance matrix transformation logic
    for r_index, row in enumerate(dis_matrix):
        for c_index, column in enumerate(row):
            if r_index == c_index or (is_entry(r_index) and (c_index - r_index) == 1):
                pass
            elif not is_entry(r_index) and (c_index - r_index) % 2 == 1 and (c_index - r_index) != -1:
                pass
            else:
                dis_matrix[r_index][c_index] = 1e6
    return dis_matrix


def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two-dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            print(routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id), previous_index, "to", index)
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance - 1000000)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance - 1000000))


def find_best_route_for(distance_matrix):
    """
    :param distance_matrix:
    :return: the optimized ordered list of points to visit.
    """
    # Instantiate the data problem.
    data = create_data_model(distance_matrix)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        10000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_COST_INSERTION)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        routes_list = get_routes(solution, routing, manager)
        return routes_list
    else:
        print('No solution found !')
        return None
