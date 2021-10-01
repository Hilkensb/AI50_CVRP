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
from solution.cvrp.route import Route
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import nodeWithCoord


class SolutionCvrp:
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, instance: Cvrp, route: List[Route] = []) -> SolutionCvrp:
        """
        """
        
        # The instance of cvrp problem linked to this solution
        self.__cvrp_instance: Cvrp = instance
        # List of all route used
        # TODO Utiliser un set pour augmenter la vitesse de comparaison ? Mais perte en insertion !
        self.__route: List[Route] = route
    
    def __copy__(self) -> SolutionCvrp:
        """
        """
        # Copy all the route
        # So for each route we will have the same node reference
        # But the reference of  the list of those nodes will be different
        route_copy: List[Route] = [copy.copy(route) for route in self.__route]
        # /!\ Does not copy cvrp instance to gain some time ressources
        # to also have a copy of the cvrp instance take a look at deepcopy
        
        # Create a new solution of the same cvrp instance and the new route
        # Return without put it in a variable so we gain some operation and 
        # will be time saving
        return SolutionCvrp(instance=self.__cvrp_instance, route=route_copy)

        
        return solution_copy
        
    def __deepcopy__(self) -> SolutionCvrp:
        """
        """
        # Copy the cvrp instance
        instance_copy: Cvrp = copy.copy(self.__cvrp_instance)
        # Create a copy of the route with the new node references
        route_copy: List[Route] = [
            Route(route=[
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
        readSolution
        
        Method to read solution of vrp on local machine
        
        :param file_path: Path of the file where the vrp instance is
        :type url: str
        :return: Itself
        :rtype: :class:'SolutionCvrp'
        :raises FileNotFoundError: when the file has not been found
        :raises ValueError: when the solution could not have been parsed
        
        .. warning:: Please ensure the format of the instance is correct.
        Exemples of the file format can be found on: http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
        
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
        readSolutionWeb
        
        Method to read solution of cvrp on internet
        
        :param url: Url of the page where the vrp solution is
        :type url: str
        :return: Itself
        :rtype: :class:'Cvrp'
        :raises AssertionError: when the requests failled to get data from the url
        :raises ValueError: when the solution could not have been parsed
        
        .. warning:: If the url is incorrect raise a ValueError
        
        .. warning:: Please ensure the format of the instance is correct.
        Exemples of the file format can be found on: http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
        
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
        self, with_labels: bool = True, route_color: List[str] = [], depot_node_color: str = "#a6f68e"
    ) -> matplotlib.figure.Figure:
        """
        """
        pass
        
    def showFigure(
        self, with_labels: bool = True, route_color: List[str] = [], depot_node_color: str = "#a6f68e"
    ) -> None:
        """
        """
        
        # Create an undirected graph
        graph: nx.Graph = nx.Graph()
              
        # Get the number of routes
        number_of_routes: int = len(self.__route)
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
        
        # Variable to store the node id of the previous node to build edege
        previous_node: int = 0
        
        # For every route of the solution
        for index, route in enumerate(self.__route):
            # Set the previous node to the depot node, so every route start at the depot
            previous_node = depot_node.node_id
            # For every customer in the solution (excluding the depot, so excluding the first and last node of the route)
            for customer in route.customers_route[1:-1]:
                # Add the node representing the customer in the graph, with the color linked to the route
                graph.add_node(customer.node_id, color=route_color[index])
                # Set the position of the nodes in the graph
                fixed_positions[customer.node_id] = customer.getCoordinates()
                # Add edge between the previous node and the actual node to build a route
                graph.add_edge(previous_node, customer.node_id, color=route_color[index])
                # Update the previous node to the actual node value for the next iteration
                previous_node = customer.node_id
                
            # Add the last edge to complete the route, from the last node to the depot
            graph.add_edge(previous_node, depot_node.node_id, color=route_color[index])
        
        
        # Get the keys of the list of position
        fixed_nodes: List[int] = fixed_positions.keys()
        # Create the layout of the graph with the position
        position_layout: nx.spring_layout = nx.spring_layout(graph, pos=fixed_positions, fixed=fixed_nodes)
        
        # Using a figure to use it as a parameter when calling nx.draw_networkx
        figure = plt.figure(1)
        # Create a sub plot to create the legend
        ax = figure.add_subplot(1,1,1)
        # Create the legend
        # For every color use in the graph (or every route - 1 since we are indexing)
        for route, color in enumerate(route_color[:number_of_routes-1]):
            # Linked each color to a label telling the route number
            ax.plot([0],[0],color=color,label=f"Route #{route+1}")
          
        # Add to the legend the color of the depot
        ax.plot([0],[0],color=depot_node_color,label="Depot")

        # Create list to color node and edge
        node_color_map: List[str] = nx.get_node_attributes(graph,'color').values()
        edge_color_map: List[str] = nx.get_edge_attributes(graph,'color').values()
        
        # Draw the graph with the layout with the position
        nx.draw(graph, position_layout, node_color=node_color_map, edge_color=edge_color_map, with_labels=with_labels, ax=ax)
              
        # Create the plot                                                                                                      
        plt.axis('off')
        figure.set_facecolor('w')
        plt.legend()
        figure.tight_layout()
        plt.show()

# ____________________________ Evaluation Method ____________________________ #

    # TODO
    def isValid(self) -> bool:
        """
        """
        pass
        
    def evaluation(self) -> float:
        """
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
            builded_route: Route = self.__parseRoute(route_to_build=route)
            # Add the builded route to the route solution
            self.__route.append(builded_route)

    def __parseRoute(self, route_to_build: str) -> Route:
        """
        """
        
        # Create a list that will store the route path
        route_path: List[nodeWithCoord] = []
        
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
        route: Route = Route(route=route_path)
        
        return route
 
# ___________________________ Comparaison Methods ___________________________ # 

    # TODO: a tester
    def isSameSolution(self, other: SolutionCvrp) -> bool:
        """
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
                
    def getNeighbours(self) -> SolutionCvrp:
        """
        """
        pass
                
# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def cvrp_instance(self) -> Cvrp:
        return self.__cvrp_instance
        
    @cvrp_instance.setter
    def cvrp_instance(self, value: Cvrp) -> None:
        self.__cvrp_instance = value

    @property 
    def route(self) -> List[Route]:
        return self.__route
        
    @route.setter
    def route(self, value: List[Route]) -> None:
        self.__route = value

