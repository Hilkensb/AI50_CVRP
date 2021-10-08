# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union
import random
import copy

# Other Library
# Library to get data from a website
import requests
# Library to create a graph
import networkx as nx
# Library to create the graph plot
import matplotlib.pyplot as plt

# Modules
from problem.cvrp.instance import Cvrp
from solution.cvrp.route import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord
import utils.mathfunctions as mathfunc
from utils.colorpallette import DEFAULT_COLOR_PALETTE


class SolutionCvrp:
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, instance: Cvrp, route: List[RouteCvrp] = []) -> SolutionCvrp:
        """
        Constructor
        
        :param instance: Instance of cvrp
        :type instance: CVRP
        :param route: List of all routes to build the solution
        :type route: List[RouteCvrp]
        :return: Itself
        :rtype: SolutionCvrp
        """
        
        # The instance of cvrp problem linked to this solution
        self.__cvrp_instance: Cvrp = instance
        # List of all route used
        self.__route: List[RouteCvrp] = route
    
    def __copy__(self) -> SolutionCvrp:
        """
        copy
        
        Create a copy of the solution
        
        :return: A copy of the solution
        :rtype: SolutionCvrp
        """
        # Copy all the route
        # So for each route we will have the same node reference
        # But the reference of  the list of those nodes will be different
        route_copy: List[RouteCvrp] = [copy.copy(route) for route in self.__route]
        # /!\ Does not copy cvrp instance to gain some time ressources
        # to also have a copy of the cvrp instance take a look at deepcopy
        
        # Create a new solution of the same cvrp instance and the new route
        # Return without put it in a variable so we gain some operation and 
        # will be time saving
        return SolutionCvrp(instance=self.__cvrp_instance, route=route_copy)

        
        return solution_copy
        
    def __deepcopy__(self) -> SolutionCvrp:
        """
        deepcopy
        
        Create a deepcopy of the solution
        
        :return: A deepcopy of the solution
        :rtype: SolutionCvrp
        """
        # Copy the cvrp instance
        instance_copy: Cvrp = copy.copy(self.__cvrp_instance)
        # Create a copy of the route with the new node references
        route_copy: List[RouteCvrp] = [
            RouteCvrp(route=[
                instance_copy.getNodeById(node.node_id)
                for node in route.customers_route
            ])
            for route in self.__route
        ]
        
        # Create a new solution of the same cvrp instance
        solution_copy: SolutionCvrp = SolutionCvrp(instance=instance_copy)
        # Set the route of the solution
        solution_copy.route(value=route_copy)
        
        return solution_copy
        
    def __str__(self) -> str:
        """
        """
        
        return "\n".join(f"Route #{index+1}: {route}" for index, route in enumerate(self.__route))
        
    def __repr__(self) -> str:
        """
        """
        return f"Solution-{self.__cvrp_instance.__repr__()}"

    def __lt__(self, other: SolutionCvrp) -> bool:
        """
        """
        
        # Compare the cost of self and the other solution
        # Will return true if this solution have a lower evaluation cost than 
        # the sol solution that we are comparing with
        return self.evaluation() < other.evaluation()
        
    def __le__(self, other: SolutionCvrp) -> bool:
        """
        """

        # Compare the cost of self and the other solution
        # Will return true if this solution have a lower or equal evaluation cost than 
        # the sol solution that we are comparing with
        return self.evaluation() <= other.evaluation()
        
    def __eq__(self, other: SolutionCvrp) -> bool:
        """
        """
        # Compare the cost of self and the other solution
        # Will return true if this solution have the same evaluation cost than 
        # the sol solution that we are comparing with
        return self.evaluation() == other.evaluation()
        
    def __ne__(self, other: SolutionCvrp) -> bool:
        """
        """
        # Compare the cost of self and the other solution
        # Will return true if this solution have a higer or equal evaluation cost than 
        # the sol solution that we are comparing with
        return self.evaluation() >= other.evaluation()
        
    def __gt__(self, other: SolutionCvrp) -> bool:
        """
        """
        # Compare the cost of self and the other solution
        # Will return true if this solution have a higher evaluation cost than 
        # the sol solution that we are comparing with
        return self.evaluation() > other.evaluation()
       
    def __len__(self) -> int:
        """
        """
        # Return the number of routes in the solution
        return len(self.__route) 
                
# --------------------------------- Methods --------------------------------- #

# ______________________________ Reader Method ______________________________ #
     
    def readSolution(self, file_path: str) -> SolutionCvrp:
        """
        readSolution()
        
        Method to read solution of vrp on local machine
        
        :param file_path: Path of the file where the vrp instance is
        :type url: str
        :return: Itself
        :rtype: :class:'SolutionCvrp'
        :raises FileNotFoundError: when the file has not been found
        :raises ValueError: when the solution could not have been parsed
        
        .. warning:: Please ensure the format of the instance is correct. Exemples of the file format can be found on: http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
        
        :exemple:

        >>> cvrp_instance.readSolution(file_path=\"C:\\Users\\YourName\\Documents\\instance.sol\")
        """
        # Can raise FileNotFoundError /!\
        instance_file: file = open(file_path, "r")
        
        # Get the data stored inside the file
        instance_data: str = instance_file.read()
        # Close the file
        instance_file.close()
        
        try:
            # Parse the data to create the object
            self.__parseSol(instance_data)
        # If an exception occurs at lower level
        # It means that file could not have been parsed
        # The file must have been in a wrong format and raise a new Exception
        except Exception as e:
            raise ValueError(f"The solution could not have been parsed. Reason: {e}")
            
        # return itself
        return self

    def readSolutionWeb(self, url: str) -> SolutionCvrp:
        """
        readSolutionWeb()
        
        Method to read solution of cvrp on internet
        
        :param url: Url of the page where the vrp solution is
        :type url: str
        :return: Itself
        :rtype: :class:'Cvrp'
        :raises AssertionError: when the requests failled to get data from the url
        :raises ValueError: when the solution could not have been parsed
        
        .. warning:: If the url is incorrect raise a ValueError
        
        .. warning:: Please ensure the format of the instance is correct. Exemples of the file format can be found on: http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
        
        :exemple:

        >>> cvrp_instance.readSolutionWeb(url=\"http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol\")
        """
        # Get the data of the url
        data_request: requests.Response = requests.get(url)
        
        # Get the status code
        status_code: int = data_request.status_code
        # Check the status code
        # Should be 200 if it has worked
        # If the code isn't 200, create an AssertionError
        assert status_code == 200, f"The status code of the request is {status_code}"
        
        try:
            # Parse the data to create the object
            self.__parseSol(data_request.text)
        # If an exception occurs at lower level
        # It means that file could not have been parsed
        # The file must have been in a wrong format and raise a new Exception
        except Exception as e:
            raise ValueError(f"The solution could not have been parsed. Reason: {e}")
        
        # Return itself
        return self

# _____________________________ Writter Methods _____________________________ #

    # TODO
    def writeInstanceVrp(self, file_path: str) -> None:  
        """
        """
        pass

# ______________________________ Diplay Method ______________________________ #

    def getFigure(
        self, with_labels: bool = True, route_color: List[str] = DEFAULT_COLOR_PALETTE,
        depot_node_color: str = "#a6f68e", show_weight: bool = False,
        route_to_display: List[int] = None, fig_size: Tuple[int, int] = (5, 4)
    ) -> matplotlib.figure.Figure:
        """
        getFigure()
        
        Method to get a figure of the solution (all routes displayed on the
        cvrp graph)
        
        :param with_labels: Display or not the name of the nodes (node id), default to True (opt.)
        :type with_labels: bool
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :param route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param show_weight: True if the weight should be displayed on the edge, else False. Default to True (opt.)
        :type show_weight: bool
        :param route_to_display: Number of the routes to display on the solution (route number start at 1), default to None (opt.)
        :type route_to_display: List[int]
        :param fig_size: Size of the figure
        :type fig_size: Tuple[int, int]
        :return: The graph figure of the solution of the cvrp
        :rtype: plt.figure

        :exemple:

        >>> root = Tk.Tk()
        >>> root.wm_title("Graph embedded in TK")
        >>> root.wm_protocol('WM_DELETE_WINDOW', root.quit)
        >>> figure = sol.getFigure()
        >>> canvas = FigureCanvasTkAgg(figure, master=root)
        >>> canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        >>> Tk.mainloop()
        
        """
        # Create the plot
        figure = plt.figure(figsize=fig_size)
        subplot = figure.add_subplot(111)
        plt.axis('off')
        
        # Get the graph, the graph layout, node colors and edges colors
        graph, position_layout, node_color_map, edge_color_map, weight_map = self.__drawMatPlotLib(
            route_color=route_color, depot_node_color=depot_node_color,
            route_to_display=route_to_display
        )
        
        # Draw the graph with the layout with the position
        nx.draw(
            graph, position_layout, node_color=node_color_map,
            edge_color=edge_color_map, with_labels=with_labels, ax=subplot
        )
        
        # If the weight has to be displayed
        if show_weight:
            # Display the weight
            nx.draw_networkx_edge_labels(graph, position_layout, edge_labels=weight_map)
        
        # Set the axis
        xlim=subplot.get_xlim()
        ylim=subplot.get_ylim()
              
        # Create the legend of the graph
        figure.legend()
        figure.tight_layout()
        
        # return the result
        return figure
        
    def showFigure(
        self, with_labels: bool = True, route_color: List[str] = DEFAULT_COLOR_PALETTE,
        depot_node_color: str = "#a6f68e", show_weight: bool = False,
        route_to_display: List[int] = None
    ) -> None:
        """
        showFigure()
        
        Method to display a figure of the solution (all routes displayed on the
        cvrp graph)
        
        :param with_labels: Display or not the name of the nodes (node id), default to True (opt.)
        :type with_labels: bool
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :param route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param show_weight: True if the weight should be displayed on the edge, else False. Default to True (opt.)
        :type show_weight: bool
        :param route_to_display: Number of the routes to display on the solution (route number start at 1), default to None (opt.)
        :type route_to_display: List[int]

        :exemple:

        >>> sol.showFigure()
        """
        
        # Get the graph, the graph layout, node colors and edges colors
        graph, position_layout, node_color_map, edge_color_map, weight_map = self.__drawMatPlotLib(
            route_color=route_color, depot_node_color=depot_node_color,
            route_to_display=route_to_display
        )
        
        # Draw the graph with the layout with the position
        nx.draw(
            graph, position_layout, node_color=node_color_map,
            edge_color=edge_color_map, with_labels=with_labels
        )
        
        # If the weight has to be displayed
        if show_weight:
            # Display the weight
            nx.draw_networkx_edge_labels(graph, position_layout, edge_labels=weight_map)
              
        # Create the plot                                                                                                  
        plt.axis('off')
        # Create the legend of the graph
        plt.legend()
        plt.tight_layout()
        # Show the result
        plt.show()

    # TODO: display only given route
    def __drawMatPlotLib(
        self,  route_color: List[str] = [], depot_node_color: str = "#a6f68e",
        route_to_display: List[int] = None
    ) -> Tuple[nx.graph, nx.spring_layout, List[str], List[str], Dict[int, int]]:
        """
        drawMatPlotLib()
        
        Method to draw a figure of the solution (all routes displayed on the
        cvrp graph)
        
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :param route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param route_to_display: Number of the routes to display on the solution (route number start at 1), default to None (opt.)
        :type route_to_display: List[int]
        :return: Return a tuple containing (in that order): the graph, the layout of the graph, node color map (list of node color), edge color map (list of edge color), weight map (list of weight)
        """
        # Create an undirected graph
        graph: nx.Graph = nx.Graph()
             
        # Create a list of routes to display     
        route_display: List[RouteCvrp] = self.__route
        # Create teh route number list
        route_indices: List[int] = list(range(1, len(self.__route) + 1))
        # If the list of route display parameter is not empty,then take every route
        # to display
        # /!\ Can raise IndexError if the route number is too high  
        if route_to_display is not None and not len(route_to_display) == 0:
            # Create the updated list of route to display in the plot
            # Minus 1 because the route number starts at 1 where index in python start at 0
            route_display = [self.__route[route_index - 1] for route_index in route_to_display]
            # Update the route number list
            route_indices = route_to_display
              
        # Get the number of routes
        number_of_routes: int = len(route_display)
        # Get the number of colors passed by the user
        number_of_colors: int = len(route_color)
        # if there's not enougth color (in other words if there's more route than color)
        if number_of_routes > number_of_colors:
            # Generate random color by choosing randomly char the string
            # Create the right amount of color to color every route
            route_color += [
                "#"+''.join([
                    random.choice('0123456789abcdef') for rgb in range(6)
                ])
                for color in range(number_of_routes - number_of_colors)
            ]
        
        # Dictionnary to fix the position of nodes in the graph
        fixed_positions: Dict[int, Tuple[int, int]] = {}
              
        # Get the depot node 
        depot_node = self.__cvrp_instance.depot
        # Create the node of the depot in the graph and set his color to the color passed in argument of the function
        graph.add_node(depot_node.node_id, color=depot_node_color)
        
        # Variable to store the node of the previous node to build edege
        previous_node: NodeWithCoord = None
        
        # For every route of the solution
        for index, route in enumerate(route_display):
            # Set the previous node to the depot node, so every route start at the depot
            previous_node = depot_node
            # For every customer in the solution (excluding the depot, so excluding the first and last node of the route)
            for customer in route.customers_route[1:-1]:
                # Add the node representing the customer in the graph, with the color linked to the route
                graph.add_node(customer.node_id, color=route_color[index])
                # Set the position of the nodes in the graph
                fixed_positions[customer.node_id] = customer.getCoordinates()
                # Weight of the edge (in other word distance between the nodes)
                weight: int = round(mathfunc.euclideanDistance(previous_node, customer))
                # Add edge between the previous node and the actual node to build a route
                graph.add_edge(previous_node.node_id, customer.node_id, color=route_color[index], weights=weight)
                # Update the previous node to the actual node value for the next iteration
                previous_node = customer
                
            # Add the last edge to complete the route, from the last node to the depot
            graph.add_edge(previous_node.node_id, depot_node.node_id, color=route_color[index])
        
        
        # Get the keys of the list of position
        fixed_nodes: List[int] = fixed_positions.keys()
        # Create the layout of the graph with the position
        position_layout: nx.spring_layout = nx.spring_layout(graph, pos=fixed_positions, fixed=fixed_nodes)
        
        # Create the legend
        # For every color use in the graph (or every route - 1 since we are indexing)
        for route, color in zip(route_indices, route_color[:number_of_routes]):
            # Linked each color to a label telling the route number
            plt.plot([],color=color,label=f"Route #{route}")
          
        # Add to the legend the color of the depot
        plt.plot([],color=depot_node_color,label="Depot")

        # Create list to color node and edge
        node_color_map: List[str] = nx.get_node_attributes(graph,'color').values()
        edge_color_map: List[str] = nx.get_edge_attributes(graph,'color').values()
        weight_map: Dict[int, int] = nx.get_edge_attributes(graph,'weights')
        
        return graph, position_layout, node_color_map, edge_color_map, weight_map

# ____________________________ Evaluation Method ____________________________ #

    # TODO
    def isValid(self) -> bool:
        """
        isValid()
        
        Method to know whether a solution is valid or not
        
        :return: True if the route is valid, False else
        :rtype: bool
        """
        
        customer_route: List[NodeWithCoord] = []
        
        # Verify that each route are valid
        for route in self.__route:
            # If the route is not valid
            if not route.isValid():
                return False

            # Add all customers of the route
            customer_route += route.customers_route[1:-1]
           
        # If the number of customer in the solution is different that the number
        # of customers in cvrp instance   
        if len(customer_route) != self.__cvrp_instance.nb_customer:
            return False
            
        # Create a counter (to count the number of every values)
        # Do this only for customers (exclude first and last values since they are 
        # depot
        counter_nodes: Dict[NodeWithCoord, int] = Counter(customer_route)    
            
        # Get all non valid nodes
        # Because their come multiple time
        non_valid_customers: List[NodeWithCoord] = [
            node for node in counter_nodes.keys()
            if counter_nodes[node]>1
            or not isinstance(node, CustomerCvrp)
       ]
       
       # To be a valid solution there's should none non valid nodes
        return len(non_valid_customers) == 0
            
        
    def evaluation(self) -> float:
        """
        evaluation()
        
        Method to get the cost of the solution (not rounded)
        
        :return: The cost (the sum of all distance between the nodes of the route)
        :rtype: float
        """
        
        # The evaluation of the solution
        evaluation: float = 0
        
        # We are going to evaluate each route and sum each evaluation
        # For each route
        for route in self.__route:
            # Get the cost of the route
            cost = route.evaluation()
            # Sum the cost to get an evaluation
            evaluation += cost
            
        return evaluation
        
# ______________________________ Parse Methods ______________________________ #

    def __parseSol(self, data_to_parse: str) -> None:
        """
        parseSol()
        
        Method to parse solution file. Either web or local file,
        since the argument must be a string
        
        :param data_to_parse: The string of the data file to parse
        :type Exception: str
        
        """
        
        # split the string into lines
        solution: List[str] = data_to_parse.split("\n")
        # List that will store string representing route
        data: List[str] = []
        # Clear the route
        self.__route = []
        
        for line in solution:
            # Parse the paramter
            # The first element is the name of the parameter
            # The others elements are the data
            # In the case of a solution name will be the name of the route and
            # the data will be the route
            # In our we are only interests in route data
            thisline: List[str] = line.split(':')
            # If the of the line splitted is 2, it mean that we have a data
            # normaly a route
            # We verify that the data is a route by checking the first character
            # of the parameters name. If it starts with "Route #", it's a route
            if len(thisline) == 2 and thisline[0].startswith("Route #"):
                data.append(thisline[1].strip())
            # We are not interested in other parameters so do nothing more
            
        # For each route in the solution file    
        for route in data:
            # Build the route
            builded_route: RouteCvrp = self.__parseRoute(route_to_build=route)
            # Add the builded route to the route solution
            self.__route.append(builded_route)

    def __parseRoute(self, route_to_build: str) -> RouteCvrp:
        """
        parseRoute()
        
        Method to parse a route from solution file. The route should be a string.
        
        :param route_to_build: The string of a line of the data file representing a route
        :type Exception: str
        :return: The route object representing the route string passed as argument
        :rtype: RouteCvrp
        """
        
        # Create a list that will store the route path
        route_path: List[NodeWithCoord] = []
        
        # Split the string into a list of customers number (at this step the
        # customers number are still string)
        customers_number_list: List[str] = route_to_build.split(" ")
        
        # The route atart with the depot (the depot is never written the solution file)
        route_path.append(self.__cvrp_instance.depot)
        
        # For every customer number in the route
        for customer_number in customers_number_list:
            # Search the customer by his curstomer numer in the cvrp instance
            customer: CustomerCvrp = self.__cvrp_instance.getCustomerByCustomerNumber(customer_number_searched=int(customer_number))
            # Add the customer to the route path
            route_path.append(customer)
           
        # The route end with the depot (the depot is never written the solution file)
        route_path.append(self.__cvrp_instance.depot) 
        
        # Build the route
        route: RouteCvrp = RouteCvrp(route=route_path)
        
        return route
 
# ___________________________ Comparaison Methods ___________________________ # 

    # TODO: a tester
    def isSameSolution(self, other: SolutionCvrp) -> bool:
        """
        isSameSolution()
        
        Method to know if 2 solutions are the same
        
        :param other: The solution to compare
        :type other: SolutionCvrp
        :return: True is the 2 solution are the same, False else
        :rtype: bool
        
        """
        
        # Check that they have both the same amount of routes
        if len(self) != len(other):
            return False
            
        # Get the route of the other solution
        other_routes: List[int] = other.route
        
        # For every route in the solution
        for route in self.__route:
            # If the route is also in the other solutions routes
            if route in other_routes:
                # remove the route from other_routes to speed up next search
                other_routes.remove(route)
            # If the route is not in the other solution routes
            # it means that the solution is not the same
            else:
                return False

        # if all routes have been found in both solution can return true
        return True

# ___________________________ Other Useful Method ___________________________ # 
                
    def getAllRouteSwapNeighbours(self) -> List[Tuple[SolutionCvrp, int]]:
        """
        getAllRouteSwapNeighbours()
        
        Method to get all swaps possible of customers in a single route. Do this for each route of the solution.
        
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []
        
        # Get the cost of the actual solution
        total_cost: int = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution
        for route in self.__route:
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Remove the actual route
            updates_route.remove(route)
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            solution_cost: int = total_cost - route_cost
            # For every neighbours of the route
            for neighbours in route.getAllNeighboursSwap():
                # Create a copy of the list to then add the route to the solution
                new_route: List[RouteCvrp] = updates_route[:]
                # Add the route to the route list of the future solution
                # Since neighbours is a tuple, 0 is the route
                new_route.append(neighbours[0])
                # Create the new solution that is a neighbour of our actual solution
                new_solution: Solution = Solution(instance=self.__cvrp_instance, route=new_route)
                # Calcul the cost by looking at the cost without the route and add the route cost
                # Since neighbours is a tuple, 1 is the cost of the route
                new_solution_cost: int = solution_cost + neighbours[1]
                
                # Tuple with the solution and it's cost
                solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost)
                
        return neighborhood
        
    def getRouteSwapNeighbours(self, proximity_swaps: int = 1) -> List[Tuple[SolutionCvrp, int]]:
        """
        getRouteSwapNeighbours()
        
        Method to get a single swap for each customer in a single route. The swap is made between customers that are separated by proximity_swaps - 1 customers. Do this for each route of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap in the route, default to 1 (opt.)
        :type proximity_swaps: int
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []
        
        # Get the cost of the actual solution
        total_cost: int = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution
        for route in self.__route:
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Remove the actual route
            updates_route.remove(route)
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            solution_cost: int = total_cost - route_cost
            # For every neighbours of the route
            for neighbours in route.getNeighboursSwap(proximity_swaps=proximity_swaps):
                # Create a copy of the list to then add the route to the solution
                new_route: List[RouteCvrp] = updates_route[:]
                # Add the route to the route list of the future solution
                # Since neighbours is a tuple, 0 is the route
                new_route.append(neighbours[0])
                # Create the new solution that is a neighbour of our actual solution
                new_solution: Solution = Solution(instance=self.__cvrp_instance, route=new_route)
                # Calcul the cost by looking at the cost without the route and add the route cost
                # Since neighbours is a tuple, 1 is the cost of the route
                new_solution_cost: int = solution_cost + neighbours[1]
                
                # Tuple with the solution and it's cost
                solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost)
                
        return neighborhood
        
    def getPermutationNeighbours(self, proximity_swaps: int = 1) -> List[Tuple[SolutionCvrp, int]]:
        """
        getPermutationNeighbours()
        
        Method to build new solution by swapping a customer between 2 route. The position difference between the customer in route1 and route2 is defined by proximity_swaps. Swaps between each routes of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap between the route, default to 1 (opt.)
        :type proximity_swaps: int
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []
        # Get the cost of the actual solution
        total_cost: int = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution except the last
        for index, route in enumerate(self.__route[:-1]):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Remove the actual route
            updates_route.remove(route)
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            route_removed_cost: int = total_cost - route_cost
            # for every route after the one selected
            for second_route in self.__route[index:]:
                # Create a copy (just change reference) of the updated route list
                # (the route list without the route of the first for loop)
                final_route: List[RouteCvrp] = updates_route[:]
                # Remove the second route
                final_route.remove(second_route)
                # Get the route cost
                route_cost: int = second_route.evaluation()
                # Cost with the route removed
                solution_cost: int = route_removed_cost - route_cost
                # Choose the base route and the other route
                # because route1.getNeighboursRouteSwap(route2) !=
                # route2.getNeighboursRouteSwap(route1)
                # The base route should the one with the most node in it
                if len(route) >= len(second_route):
                    base_route: RouteCvrp = route
                    other_route: RouteCvrp = second_route
                else:
                    base_route: RouteCvrp = second_route
                    other_route: RouteCvrp = route
                    
                # look for every neighboors
                for neighbours in base_route.getNeighboursSwap(other_route=other_route, proximity_swaps=proximity_swaps):
                    # Create a copy of the list to then add the route to the solution
                    new_route: List[RouteCvrp] = final_route[:]
                    # Add the route to the route list of the future solution
                    # Since neighbours is a tuple, 0 is the route
                    new_route.append(neighbours[0])
                    new_route.append(neighbours[1])
                    # Create the new solution that is a neighbour of our actual solution
                    new_solution: Solution = Solution(instance=self.__cvrp_instance, route=new_route)
                    # Calcul the cost by looking at the cost without the route and add the route cost
                    # Since neighbours is a tuple, 1 is the cost of the route
                    new_solution_cost: int = solution_cost + neighbours[2]
                    
                    # Tuple with the solution and it's cost
                    solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost)
                
        return neighborhood

# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def cvrp_instance(self) -> Cvrp:
        return self.__cvrp_instance
        
    @cvrp_instance.setter
    def cvrp_instance(self, value: Cvrp) -> None:
        self.__cvrp_instance = value

    @property 
    def route(self) -> List[RouteCvrp]:
        return self.__route
        
    @route.setter
    def route(self, value: List[RouteCvrp]) -> None:
        self.__route = value

