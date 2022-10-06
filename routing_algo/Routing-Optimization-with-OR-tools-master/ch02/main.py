"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = [
        [0, 548, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
        [1000000.0, 0, 684, 1000000.0, 194, 1000000.0, 730, 1000000.0, 696, 1000000.0, 1084, 1000000.0, 480, 1000000.0,
         1016, 1000000.0, 1210],
        [1000000.0, 1000000.0, 0, 992, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
        [696, 1000000.0, 1000000.0, 0, 114, 1000000.0, 878, 1000000.0, 844, 1000000.0, 1232, 1000000.0, 628, 1000000.0,
         1164, 1000000.0, 1358],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 0, 536, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
        [274, 1000000.0, 502, 1000000.0, 1000000.0, 0, 228, 1000000.0, 194, 1000000.0, 582, 1000000.0, 662, 1000000.0,
         514, 1000000.0, 708],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 0, 536, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
        [194, 1000000.0, 810, 1000000.0, 388, 1000000.0, 1000000.0, 0, 342, 1000000.0, 730, 1000000.0, 354, 1000000.0,
         662, 1000000.0, 856],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 0, 274, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
        [194, 1000000.0, 742, 1000000.0, 776, 1000000.0, 468, 1000000.0, 1000000.0, 0, 342, 1000000.0, 422, 1000000.0,
         274, 1000000.0, 468],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         0, 878, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
        [502, 1000000.0, 1278, 1000000.0, 400, 1000000.0, 1004, 1000000.0, 810, 1000000.0, 1000000.0, 0, 114, 1000000.0,
         650, 1000000.0, 844],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 0, 194, 1000000.0, 1000000.0, 1000000.0],
        [354, 1000000.0, 1130, 1000000.0, 708, 1000000.0, 856, 1000000.0, 662, 1000000.0, 730, 1000000.0, 1000000.0, 0,
         342, 1000000.0, 536],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 0, 764, 1000000.0],
        [776, 1000000.0, 1552, 1000000.0, 674, 1000000.0, 1278, 1000000.0, 1084, 1000000.0, 1152, 1000000.0, 388,
         1000000.0, 1000000.0, 0, 798],
        [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0,
         1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 0],

    ]

    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


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
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

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
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


if __name__ == '__main__':
    main()
