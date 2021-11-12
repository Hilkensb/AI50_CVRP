# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union
import random
import copy
from collections import Counter

# Other Library
# Library to get data from a website
import requests
# Library to create a graph
import networkx as nx
# Library to create the graph plot
import matplotlib.pyplot as plt
# To display plotly grah
import plotly.graph_objects as go
# To convert figure into html
from plotly.io import to_html

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
        self.__route: List[RouteCvrp] = route[:]
    
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
        
    def __hash__(self):
        """
        """
        return hash(self.__str__)
        
    def __dict__(self):
        """
        dict()
        
        Create the dictionnary of the object
        
        :return: The dictionnary with al values of the object
        :rtype: dict
        """  
        
        # Create the dictionnary
        object_dict: Dict = {}
        
        # Set every variable of it
        # Convert every route into dictionnary before putting them inside
        # the dictionnary of the solution
        # it will then be easier to generate the json string
        object_dict["route"] = [route.__dict__() for route in self.__route]
        object_dict["instance"] = self.__cvrp_instance.__dict__()
        
        return object_dict 
                
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

# ______________________________ Search Method ______________________________ #

    def getRouteOfCustomer(self, customer_id: int) -> Route:
        """
        """
        
        # for every route in the solution
        for route in self.__route:
            # Build a set by comprehension of the customers node id
            route_customer_id: Set = {customer.node_id for customer in route.customers_route}
            # If the customer is in the rouet
            if customer_id in route_customer_id:
                # Return the route found
                return route

# ______________________________ Diplay Method ______________________________ #

    def getFigure(
        self, with_labels: bool = True, route_color: List[str] = DEFAULT_COLOR_PALETTE,
        depot_node_color: str = "#a6f68e", show_weight: bool = False,
        route_to_display: List[int] = None, fig_size: Tuple[int, int] = (5, 4),
        node_size: int = 300, auto_node_size: bool= False
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
        :param node_size: Size of the nodes
        :type node_size: int
        :param auto_node_size: Set the size of the node automatically
        :type auto_node_size: bool
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
        graph, position_layout, node_color_map, edge_color_map, weight_map, node_size = self.drawMatPlotLib(
            route_color=route_color, depot_node_color=depot_node_color,
            route_to_display=route_to_display, node_size=node_size,
            auto_node_size=auto_node_size
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
        route_to_display: List[int] = None, node_size: int = 300,
        auto_node_size: bool= False
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
        :param node_size: Size of the nodes
        :type node_size: int
        :param auto_node_size: Set the size of the node automatically
        :type auto_node_size: bool

        :exemple:

        >>> sol.showFigure()
        """
        
        # Get the graph, the graph layout, node colors and edges colors
        graph, position_layout, node_color_map, edge_color_map, weight_map, node_size = self.drawMatPlotLib(
            route_color=route_color, depot_node_color=depot_node_color,
            route_to_display=route_to_display, node_size=node_size,
            auto_node_size=auto_node_size
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


    def getFigurePlotly(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: List[str] = DEFAULT_COLOR_PALETTE, show_legend_edge: bool = True,
        show_legend_node: bool = False
    ) -> str:
        """
        getHtmlFigurePlotly()

        Method to display the graph with plotly library

        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :tyoe route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :param full_html: If True, produce a string containing a complete HTML document starting with an <html> tag. If False, produce a string containing a single <div> element. Default to True (opt.)
        :type full_html: bool
        :param default_width: he default figure width/height to use if the provided figure does not specify its own layout.width/layout.height property. May be specified in pixels as an integer (e.g. 500), or as a css width style string (e.g. ‘500px’, ‘100%’). Default to \"100%\" (opt.)
        :type default_width: str
        :param default_height: The default figure width/height to use if the provided figure does not specify its own layout.width/layout.height property. May be specified in pixels as an integer (e.g. 500), or as a css width style string (e.g. ‘500px’, ‘100%’). Default to \"100%\" (opt.)
        """  
      
        # Get variable to draw a graph on plotly
        node_scatter_list, edge_scatter_list = self.drawPlotly(
            depot_node_color=depot_node_color, node_size=node_size, 
            route_color=route_color, show_legend_edge=show_legend_edge,
            show_legend_node=show_legend_node
        )
        
        # Create the firgure
        fig = go.Figure(
            data=[*node_scatter_list, *edge_scatter_list],
            layout=go.Layout(
                title=self.__repr__(),
                titlefont_size=16,
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        
        return fig

    def showFigurePlotly(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: List[str] = DEFAULT_COLOR_PALETTE, show_legend_edge: bool = True,
        show_legend_node: bool = False
    ) -> str:
        """
        getHtmlFigurePlotly()

        Method to display the graph with plotly library

        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :tyoe route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :param full_html: If True, produce a string containing a complete HTML document starting with an <html> tag. If False, produce a string containing a single <div> element. Default to True (opt.)
        :type full_html: bool
        :param default_width: he default figure width/height to use if the provided figure does not specify its own layout.width/layout.height property. May be specified in pixels as an integer (e.g. 500), or as a css width style string (e.g. ‘500px’, ‘100%’). Default to \"100%\" (opt.)
        :type default_width: str
        :param default_height: The default figure width/height to use if the provided figure does not specify its own layout.width/layout.height property. May be specified in pixels as an integer (e.g. 500), or as a css width style string (e.g. ‘500px’, ‘100%’). Default to \"100%\" (opt.)
        """  
      
        # Get variable to draw a graph on plotly
        fig = self.getFigurePlotly(
            depot_node_color=depot_node_color, node_size=node_size,
            route_color=route_color, show_legend_edge=show_legend_edge,
            show_legend_node=show_legend_node
        )
        
        fig.show()

    def getHtmlFigurePlotly(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: List[str] = DEFAULT_COLOR_PALETTE, show_legend_edge: bool = True,
        show_legend_node: bool = False, full_html: bool = True,
        default_width: str = '100%', default_height: str = '100%'
    ) -> str:
        """
        getHtmlFigurePlotly()

        Method to get the html code of the graph

        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :tyoe route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :param full_html: If True, produce a string containing a complete HTML document starting with an <html> tag. If False, produce a string containing a single <div> element. Default to True (opt.)
        :type full_html: bool
        :param default_width: he default figure width/height to use if the provided figure does not specify its own layout.width/layout.height property. May be specified in pixels as an integer (e.g. 500), or as a css width style string (e.g. ‘500px’, ‘100%’). Default to \"100%\" (opt.)
        :type default_width: str
        :param default_height: The default figure width/height to use if the provided figure does not specify its own layout.width/layout.height property. May be specified in pixels as an integer (e.g. 500), or as a css width style string (e.g. ‘500px’, ‘100%’). Default to \"100%\" (opt.)
        :return: a html string
        :rtype: str
        """  
      
        # Get variable to draw a graph on plotly
        fig = self.getFigurePlotly(
            depot_node_color=depot_node_color, node_size=node_size,
            route_color=route_color, show_legend_edge=show_legend_edge,
            show_legend_node=show_legend_node
        )
        
        # Return the html string
        return to_html(
                fig=fig, full_html=full_html,
                default_width=default_width, default_height=default_height
        )

    def drawMatPlotLib(
        self,  route_color: List[str] = [], depot_node_color: str = "#a6f68e",
        route_to_display: List[int] = None, node_size: int = 300,
        auto_node_size: bool= False
    ) -> Tuple[nx.graph, nx.spring_layout, List[str], List[str], Dict[int, int]]:
        """
        drawMatPlotLib()
        
        Method to draw a figure of the solution (all routes displayed on the
        cvrp graph)
        
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :type route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param route_to_display: Number of the routes to display on the solution (route number start at 1), default to None (opt.)
        :type route_to_display: List[int]
        :param node_size: Size of the nodes
        :type node_size: int
        :param auto_node_size: Set the size of the node automatically
        :type auto_node_size: bool
        :return: Return a tuple containing (in that order): the graph, the layout of the graph, node color map (list of node color), edge color map (list of edge color), weight map (list of weight), node size (an integer to represent the node size)
        :raises IndexError: If a route to display does exists
        """
        # Create an undirected graph
        graph: nx.Graph = nx.Graph()
         
        # Check if we need to set the size of the nodes
        if auto_node_size:
            # Set the node to be visible and the less has possible overlapping
            node_size = 300 - round((max(self.__cvrp_instance.nb_customer,  50) - 50) / 2)
             
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
        # Fix the position of the depot
        fixed_positions[depot_node.node_id] = depot_node.getCoordinates()
        
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
        
        return graph, position_layout, node_color_map, edge_color_map, weight_map, node_size

    def drawPlotly(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: List[str] = DEFAULT_COLOR_PALETTE, show_legend_edge: bool = True,
        show_legend_node: bool = False
    ) -> Tuple(List[Scatter], List[Scatter]):
        """
        drawPlotly()
        
        Method to create the scatter that compose the graph made with plotly
        
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :tyoe route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :return: Two lists of scatters, one of nodes and one of edges
        :rtype: Tuple(List[Scatter], List[Scatter])
        """
        
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
        
        # Get the depot node 
        depot_node = self.__cvrp_instance.depot
        
        # List of scatter plot 
        # List of the nodes
        node_scatter_list: List[Scatter] = [None] * (self.__cvrp_instance.nb_customer + 1)
        # List of edges
        edge_scatter_list: List[Scatter] = []
        
        # List of edges
        edge_x = []
        edge_y = []
        # List of nodes
        node_x = []
        node_y = []
        # Text when hovered
        node_text: List[str] = []
        # Dictionnary of nodes color
        node_route_index: Dict[int, int] = {}

        # For every route of the solution
        for index, route in enumerate(self.__route):
        
            # Reset the list
            # List of edges
            edge_x = []
            edge_y = []
            # List of nodes
            node_x = []
            node_y = []
            # Name of the nodes
            node_text = []
        
            # Set the previous node to the depot node, so every route start at the depot
            previous_node = depot_node
            x1, y1 = depot_node.getCoordinates()
            # For every customer in the solution (excluding the depot, so excluding the first and last node of the route)
            for customer in route.customers_route[1:-1]:
                # Get the x and y position of the departure of the route
                x0, y0 = x1, y1
                # Get the x and y position of the arrival of the route
                x1, y1 = customer.getCoordinates()
                
                # Set the coloration of the node
                node_route_index[customer.node_id] = index
                
                # Set the positions of the ege
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)
                
                # Set the node
                # Set is position
                node_x = [x1]
                node_y = [y1]
                # Set his name
                node_text = [f"Customer: {customer.node_id}<br>Demand: {customer.demand}"]
      
                # Node of the trace
                node_trace: Scatter = go.Scatter(
                    x=node_x, y=node_y,
                    showlegend=show_legend_node,
                    mode='markers',
                    hoverinfo='text',
                    marker=dict(
                        color=route_color[node_route_index[customer.node_id]],
                        size=node_size,
                        line_width=0.5
                    ),
                    name=f"Customers in route #{node_route_index[customer.node_id] + 1}",
                    text = node_text
                )
                # Add the node scatter 
                # Garrentee that each node will be in the same oreder
                node_scatter_list[customer.node_id - 1] = node_trace
                                
                # Update the previous node to the actual node value for the next iteration
                previous_node = customer

            # Set the returning edge to the depot
            # Get the x and y position of last customer
            x0, y0 = x1, y1
            # Get the x and y position of the depot
            x1, y1 = depot_node.getCoordinates()
            # Set the positions of the ege
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

            # Edge of the trace
            edge_trace: Scatter = go.Scatter(
                x=edge_x, y=edge_y,
                showlegend=show_legend_edge,
                line=dict(width=0.5, color=route_color[index]),
                hoverinfo='none',
                mode='lines',
                name=f"Route #{index + 1}"
            )
            # Add the edge scatter
            edge_scatter_list.append(edge_trace)
            
        # Create the node of the depot
        depot_trace: Scatter = go.Scatter(
            x=[depot_node.x], y=[depot_node.y],
            showlegend=show_legend_node,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                color=depot_node_color,
                size=node_size,
                line_width=0.5
            ),
            name=f"Depot",
            text = [f"{depot_node.node_id} (Depot)"]
        )
        # Add the depot scatter 
        node_scatter_list[depot_node.node_id - 1] = depot_trace

        return node_scatter_list, edge_scatter_list

    def drawPlotlyJSON(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: List[str] = DEFAULT_COLOR_PALETTE, show_legend_edge: bool = True,
        show_legend_node: bool = False
    ) -> Dict:
        """
        drawPlotly()
        
        Method to create the scatter that compose the graph made with plotly
        
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :tyoe route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :return: List of dictionnary to draw scatters
        :rtype: 
        """
        
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
        
        # Get the depot node 
        depot_node = self.__cvrp_instance.depot
        
        # List of scatter plot 
        # List of the nodes
        scatter_list_json: List[Scatter] = []
        
        # List of edges
        edge_x = []
        edge_y = []
        # List of nodes
        node_x = []
        node_y = []
        # Text when hovered
        node_text: List[str] = []
        # Dictionnary of nodes color
        node_route_index: Dict[int, int] = {}

        # For every route of the solution
        for index, route in enumerate(self.__route):
        
            # Reset the list
            # List of edges
            edge_x = []
            edge_y = []
            # List of nodes
            node_x = []
            node_y = []
            # Name of the nodes
            node_text = []
        
            # Set the previous node to the depot node, so every route start at the depot
            previous_node = depot_node
            # For every customer in the solution (excluding the depot, so excluding the first and last node of the route)
            for customer in route.customers_route[1:-1]:
                # Get the x and y position of the departure of the route
                x0, y0 = previous_node.getCoordinates()
                # Get the x and y position of the arrival of the route
                x1, y1 = customer.getCoordinates()
                
                # Set the coloration of the node
                node_route_index[customer.node_id] = index
                
                # Set the positions of the ege
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)
                
                # Update the previous node to the actual node value for the next iteration
                previous_node = customer

            # Set the returning edge to the depot
            # Get the x and y position of last customer
            x0, y0 = previous_node.getCoordinates()
            # Get the x and y position of the depot
            x1, y1 = depot_node.getCoordinates()
            # Set the positions of the ege
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

            # Edge of the trace
            edge_trace: Dict = {
                "x":edge_x, "y":edge_y,
                "showlegend":show_legend_edge,
                "line":{"width":0.5, "color":route_color[index]},
                "hoverinfo":"none",
                "mode":"lines",
                "name":f"Route #{index + 1}"
            }
            # Add the edge scatter
            scatter_list_json.append(edge_trace)
         
         # We create separatly the customer to garentee that all the time
         # The customers will be in the same order
         # It is necessary to build animation then
         # For every customer in cvrp
         # do it in another loop to keep the same order all the time of customers
        for customer in self.__cvrp_instance.customers:
            # Get the coordinates
            x1, y1 = customer.getCoordinates()
        
            # Set the node
            # Set is position
            node_x = [x1]
            node_y = [y1]
            # Set his name
            node_text = [f"{customer.node_id}<br>Demand: {customer.demand}"]
  
            # Node of the trace
            node_trace: Dict = {
                "x":node_x, "y":node_y,
                "showlegend":show_legend_node,
                "mode":"markers",
                "hoverinfo":"text",
                "marker":{
                    "color":route_color[node_route_index[customer.node_id]],
                    "size":node_size,
                    "line_width":0.5
                },
                "name":f"Customers in route #{node_route_index[customer.node_id] + 1}",
                "text":node_text
            }
            # Add the node scatter 
            scatter_list_json.append(node_trace)
            
        # Create the node of the depot
        depot_trace: Dict = {
            "x":[depot_node.x], "y":[depot_node.y],
            "showlegend":show_legend_node,
            "mode":"markers",
            "hoverinfo":"text",
            "marker":{
                "color":depot_node_color,
                "size":node_size,
                "line_width":0.5
            },
            "name":f"Depot",
            "text":[f"{depot_node.node_id} (Depot)"]
        }
        # Add the depot scatter 
        scatter_list_json.append(depot_trace)

        return scatter_list_json


# ____________________________ Evaluation Method ____________________________ #

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
              
            # If the vehicule supplied more than it can    
            if route.demandSupplied() > self.__cvrp_instance.vehicule_capacity:
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
                
    def getAllRouteSwapNeighbours(self, total_cost: float = None) -> List[Tuple[SolutionCvrp, int]]:
        """
        getAllRouteSwapNeighbours()
        
        Method to get all swaps possible of customers in a single route. Do this for each route of the solution.
                
        :param total_cost: Total cost of the route (so it has not to be calculated again), default to None (opt.)
        :type total_cost: float
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []
        
        # If there's not the evaluation
        if total_cost is None:
            # Get the cost of the actual solution
            total_cost: float = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution
        for index, route in enumerate(self.__route):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
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
                new_route[index] = neighbours[0]
                # Create the new solution that is a neighbour of our actual solution
                new_solution: Solution = Solution(instance=self.__cvrp_instance, route=new_route)
                # Calcul the cost by looking at the cost without the route and add the route cost
                # Since neighbours is a tuple, 1 is the cost of the route
                new_solution_cost: int = solution_cost + neighbours[1]
                
                # Tuple with the solution and it's cost
                solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost)
                
        return neighborhood
        
    def getRouteSwapNeighbours(self, proximity_swaps: int = 1, total_cost: float = None) -> List[Tuple[SolutionCvrp, int, str]]:
        """
        getRouteSwapNeighbours()
        
        Method to get a single swap for each customer in a single route. The swap is made between customers that are separated by proximity_swaps - 1 customers. Do this for each route of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap in the route, default to 1 (opt.)
        :type proximity_swaps: int
        :param total_cost: Total cost of the route (so it has not to be calculated again), default to None (opt.)
        :type total_cost: float
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []
        
        # If there's not the evaluation
        if total_cost is None:
            # Get the cost of the actual solution
            total_cost: float = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution
        for index, route in enumerate(self.__route):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            solution_cost: int = total_cost - route_cost
            # For every neighbours of the route
            for neighbours in route.getNeighboursSwap(proximity_swaps=proximity_swaps, route_cost=route_cost):
                # Create a copy of the list to then add the route to the solution
                new_route: List[RouteCvrp] = updates_route[:]
                # Add the route to the route list of the future solution
                # Since neighbours is a tuple, 0 is the route
                new_route[index] = neighbours[0]
                # Create the new solution that is a neighbour of our actual solution
                new_solution: SolutionCvrp = SolutionCvrp(instance=self.__cvrp_instance, route=new_route)
                # Calcul the cost by looking at the cost without the route and add the route cost
                # Since neighbours is a tuple, 1 is the cost of the route
                new_solution_cost: int = solution_cost + neighbours[1]
                # Swap realized
                swap_realized: str = neighbours[2]
                
                # Tuple with the solution and it's cost
                solution_costs_tuple: Tuple[SolutionCvrp, int, str] = (new_solution, new_solution_cost, swap_realized)
                # Add the solution to the neighborhood to be returned
                neighborhood.append(solution_costs_tuple)
            
        return neighborhood
        
    def getPermutationNeighbours(self, proximity_swaps: int = 1, total_cost: float = None) -> List[Tuple[SolutionCvrp, int, str]]:
        """
        getPermutationNeighbours()
        
        Method to build new solution by swapping a customer between 2 route. The position difference between the customer in route1 and route2 is defined by proximity_swaps. Swaps between each routes of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap between the route, default to 1 (opt.)
        :type proximity_swaps: int
        :param total_cost: Total cost of the route (so it has not to be calculated again), default to None (opt.)
        :type total_cost: float
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []

        # If there's not the evaluation
        if total_cost is None:
            # Get the cost of the actual solution
            total_cost: float = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution except the last
        for index, route in enumerate(self.__route[:-1]):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            route_removed_cost: int = total_cost - route_cost
            # for every route after the one selected
            for index2, second_route in enumerate(self.__route[index+1:]):
                # Create a copy (just change reference) of the updated route list
                # (the route list without the route of the first for loop)
                final_route: List[RouteCvrp] = updates_route[:]
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
                    first_index: int = index
                    second_index: int = index2 + index + 1
                else:
                    base_route: RouteCvrp = second_route
                    other_route: RouteCvrp = route
                    first_index: int = index2 + index + 1
                    second_index: int = index
                 
                # Get list of neighbours 
                neighboors_list: List[Route]= base_route.getNeighboursRouteSwap(
                    other_route=other_route,
                    vehicule_capacity=self.__cvrp_instance.vehicule_capacity,
                    proximity_swaps=proximity_swaps
                 )
                    
                # look for every neighboors
                for neighbours in neighboors_list:
                    # Create a copy of the list to then add the route to the solution
                    new_route: List[RouteCvrp] = final_route[:]
                    # Add the route to the route list of the future solution
                    # Since neighbours is a tuple, 0 is the route
                    new_route[first_index] = neighbours[0]
                    new_route[second_index] = neighbours[1]
                    # Create the new solution that is a neighbour of our actual solution
                    new_solution: SolutionCvrp = SolutionCvrp(instance=self.__cvrp_instance, route=new_route)
                    # Calcul the cost by looking at the cost without the route and add the route cost
                    # Since neighbours is a tuple, 1 is the cost of the route
                    new_solution_cost: int = solution_cost + neighbours[2]
                    # Swap realized
                    swap_realized: str = neighbours[3]
                    
                    # Tuple with the solution and it's cost
                    solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost, swap_realized)
                    
                    # Add the new solution to the neighborhood
                    neighborhood.append(solution_costs_tuple)
                
        return neighborhood
        
        
    def getClosestPermutationNeighbours(self, proximity_swaps: int = 1, total_cost: float = None) -> List[Tuple[SolutionCvrp, int, str]]:
        """
        getClosestPermutationNeighbours()
        
        Method to build new solution by swapping a customer between 2 adjacent route. The position difference between the customer in route1 and route2 is defined by proximity_swaps. Swaps between each routes of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap between the route, default to 1 (opt.)
        :type proximity_swaps: int
        :param total_cost: Total cost of the solution (so it has not to be calculated again), default to None (opt.)
        :type total_cost: float
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []

        # If there's not the evaluation
        if total_cost is None:
            # Get the cost of the actual solution
            total_cost: float = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution except the last
        for index, route in enumerate(self.__route):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            route_removed_cost: int = total_cost - route_cost
            # for every route after the one selected
            second_route = self.__route[(index+1) % len(self.__route)]
            # Create a copy (just change reference) of the updated route list
            # (the route list without the route of the first for loop)
            final_route: List[RouteCvrp] = updates_route[:]
            # Get the route cost
            second_route_cost: int = second_route.evaluation()
            # Cost with the route removed
            solution_cost: int = route_removed_cost - second_route_cost
            # Choose the base route and the other route
            # because route1.getNeighboursRouteSwap(route2) !=
            # route2.getNeighboursRouteSwap(route1)
            # The base route should the one with the most node in it
            if len(route) >= len(second_route):
                base_route: RouteCvrp = route
                other_route: RouteCvrp = second_route
                first_index: int = index
                second_index: int = (index+1) % len(self.__route)
                self_route_cost: float = route_cost
                other_route_cost: float = second_route_cost
            else:
                base_route: RouteCvrp = second_route
                other_route: RouteCvrp = route
                first_index: int = (index+1) % len(self.__route)
                second_index: int = index
                self_route_cost: float = second_route_cost
                other_route_cost: float = route_cost
             
            # Get list of neighbours 
            neighboors_list: List[Route]= base_route.getNeighboursRouteSwap(
                other_route=other_route,
                vehicule_capacity=self.__cvrp_instance.vehicule_capacity,
                proximity_swaps=proximity_swaps
             )
                
            # look for every neighboors
            for neighbours in neighboors_list:
                # Create a copy of the list to then add the route to the solution
                new_route: List[RouteCvrp] = final_route[:]
                # Add the route to the route list of the future solution
                # Since neighbours is a tuple, 0 is the route
                new_route[first_index] = neighbours[0]
                new_route[second_index] = neighbours[1]
                # Create the new solution that is a neighbour of our actual solution
                new_solution: SolutionCvrp = SolutionCvrp(instance=self.__cvrp_instance, route=new_route)
                # Calcul the cost by looking at the cost without the route and add the route cost
                # Since neighbours is a tuple, 1 is the cost of the route
                new_solution_cost: int = solution_cost + neighbours[2]
                # Swap realized
                swap_realized: str = neighbours[3]
                
                # Tuple with the solution and it's cost
                solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost, swap_realized)
                
                # Add the new solution to the neighborhood
                neighborhood.append(solution_costs_tuple)
                
        return neighborhood

    def getInsertionNeighbours(self, proximity_swaps: int = 1, total_cost: float  = None) -> List[Tuple[SolutionCvrp, int, str]]:
        """
        getInsertionNeighbours()
        
        Method to build new solution by insertinh a customer between in a route. The position difference between the customer in route1 and route2 is defined by proximity_swaps. Swaps between each routes of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap between the route, default to 1 (opt.)
        :type proximity_swaps: int
        :param total_cost: Total cost of the solution (so it has not to be calculated again), default to None (opt.)
        :type total_cost: float
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []

        # If there's not the evaluation
        if total_cost is None:
            # Get the cost of the actual solution
            total_cost: float = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution except the last
        for index, route in enumerate(self.__route[:-1]):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            route_removed_cost: int = total_cost - route_cost
            # for every route after the one selected
            for index2, second_route in enumerate(self.__route[index+1:]):
                # Create a copy (just change reference) of the updated route list
                # (the route list without the route of the first for loop)
                final_route: List[RouteCvrp] = updates_route[:]
                # Get the route cost
                second_route_cost: int = second_route.evaluation()
                # Cost with the route removed
                solution_cost: int = route_removed_cost - route_cost
                # Choose the base route and the other route
                # because route1.getNeighboursRouteInsertion(route2) !=
                # route2.getNeighboursRouteInsertion(route1)
                # The base route should the one with the last fullfilment demand
                if route.demandSupplied() <= second_route.demandSupplied():
                    base_route: RouteCvrp = route
                    other_route: RouteCvrp = second_route
                    first_index: int = index
                    second_index: int = index2 + index + 1
                    self_route_cost: float = route_cost
                    other_route_cost: float = second_route_cost
                else:
                    base_route: RouteCvrp = second_route
                    other_route: RouteCvrp = route
                    first_index: int = index2 + index + 1
                    second_index: int = index
                    self_route_cost: float = second_route_cost
                    other_route_cost: float = route_cost

                 
                # Get list of neighbours 
                neighboors_list: List[Route]= base_route.getNeighboursRouteInsertion(
                    other_route=other_route,
                    vehicule_capacity=self.__cvrp_instance.vehicule_capacity,
                    proximity_swaps=proximity_swaps, self_route_cost=self_route_cost, 
                    other_route_cost=other_route_cost
                 )
                    
                # look for every neighboors
                for neighbours in neighboors_list:
                    # Create a copy of the list to then add the route to the solution
                    new_route: List[RouteCvrp] = final_route[:]
                    # Add the route to the route list of the future solution
                    # Since neighbours is a tuple, 0 is the route
                    new_route[first_index] = neighbours[0]
                    new_route[second_index] = neighbours[1]
                    # Create the new solution that is a neighbour of our actual solution
                    new_solution: SolutionCvrp = SolutionCvrp(instance=self.__cvrp_instance, route=new_route)
                    # Calcul the cost by looking at the cost without the route and add the route cost
                    # Since neighbours is a tuple, 1 is the cost of the route
                    new_solution_cost: int = solution_cost + neighbours[2]
                    # Swap realized
                    swap_realized: str = neighbours[3]
                    
                    # Tuple with the solution and it's cost
                    solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost, swap_realized)
                    
                    # Add the new solution to the neighborhood
                    neighborhood.append(solution_costs_tuple)
                
        return neighborhood
        
    def getClosestInsertionNeighbours(
        self, proximity_swaps: int = 1, total_cost: float = None
    ) -> List[Tuple[SolutionCvrp, int, str]]:
        """
        getClosestInsertionNeighbours()
        
        Method to build new solution by swapping a customer between 2 adjacent route. The position difference between the customer in route1 and route2 is defined by proximity_swaps. Swaps between each routes of the solution.
        
        :param proximity_swaps: Number of customer between to customer to swap between the route, default to 1 (opt.)
        :type proximity_swaps: int
        :param total_cost: Total cost of the route (so it has not to be calculated again), default to None (opt.)
        :type total_cost: float
        :return: A list containing the new solutions with the customers swaps in a single route, and their cost
        :rtype: List[Tuple[SolutionCvrp, int]]
        """
        
        # Create a list to store all neighbours
        neighborhood: List[Tuple[SolutionCvrp, int]] = []

        # If there's not the evaluation
        if total_cost is None:
            # Get the cost of the actual solution
            total_cost: float = self.evaluation()
        # List all route of the solution
        route_list: List[RouteCvrp] = copy.copy(self.__route)
        
        # For every route in the solution except the last
        for index, route in enumerate(self.__route):
            # Create a copy (just change reference) of the route's list
            updates_route: List[RouteCvrp] = route_list[:]
            # Get the route cost
            route_cost: int = route.evaluation()
            # Cost with the route removed
            route_removed_cost: int = total_cost - route_cost
            # for every route after the one selected
            second_route = self.__route[(index+1) % len(self.__route)]
            # Create a copy (just change reference) of the updated route list
            # (the route list without the route of the first for loop)
            final_route: List[RouteCvrp] = updates_route[:]
            # Get the route cost
            second_route_cost: int = second_route.evaluation()
            # Cost with the route removed
            solution_cost: int = route_removed_cost - second_route_cost
            # Choose the base route and the other route
            # because route1.getNeighboursRouteInsertion(route2) !=
            # route2.getNeighboursRouteInsertion(route1)
            # The base route should the one with the last fullfilment demand
            if route.demandSupplied() <= second_route.demandSupplied():
                base_route: RouteCvrp = route
                other_route: RouteCvrp = second_route
                first_index: int = index
                second_index: int = ((index+1) % len(self.__route))
                self_route_cost: float = route_cost
                other_route_cost: float = second_route_cost
            else:
                base_route: RouteCvrp = second_route
                other_route: RouteCvrp = route
                first_index: int = ((index+1) % len(self.__route))
                second_index: int = index
                self_route_cost: float = second_route_cost
                other_route_cost: float = route_cost
             
            # Get list of neighbours 
            neighboors_list: List[Route]= base_route.getNeighboursRouteInsertion(
                other_route=other_route,
                vehicule_capacity=self.__cvrp_instance.vehicule_capacity,
                proximity_swaps=proximity_swaps, self_route_cost=self_route_cost, 
                other_route_cost=other_route_cost
             )
                
            # look for every neighboors
            for neighbours in neighboors_list:
                # Create a copy of the list to then add the route to the solution
                new_route: List[RouteCvrp] = final_route[:]
                # Add the route to the route list of the future solution
                # Since neighbours is a tuple, 0 is the route
                new_route[first_index] = neighbours[0]
                new_route[second_index] = neighbours[1]
                # Create the new solution that is a neighbour of our actual solution
                new_solution: SolutionCvrp = SolutionCvrp(instance=self.__cvrp_instance, route=new_route)
                # Calcul the cost by looking at the cost without the route and add the route cost
                # Since neighbours is a tuple, 1 is the cost of the route
                new_solution_cost: int = solution_cost + neighbours[2]
                # Swap realized
                swap_realized: str = neighbours[3]
                
                # Tuple with the solution and it's cost
                solution_costs_tuple: Tuple[SolutionCvrp, int] = (new_solution, new_solution_cost, swap_realized)
                
                # Add the new solution to the neighborhood
                neighborhood.append(solution_costs_tuple)
                
        return neighborhood

# _____________________________ Extract Methods _____________________________ #

    def toJSON(self) -> str:
        """
        toJSON()
        
        Method to get the JSON value of the class
        """
    
        return json.dumps(self.__dict__())
        
    def fromJSON(self, json: dict) -> None:
        """
        fromJSON()
        
        Method to transform a JSON into an object
        
        :param json: Json data of the object
        :type json: dict
        :raises: KeyValueError if the json is incomplete
        """
    
        # Create a list of routes
        route_list: List[RouteCvrp] = []
        # Iterate through the json data
        for route_json in object_dict["route"]:
            # Create a new route
            route: RouteCvrp = RouteCvrp(route=[])
            # Update the route with the json data
            route.fromJSON(json=route_json)
            # add it to the list
            route_list.append(route)
        
        # Set the attribute
        self.__route = route_list
        
        # Create the cvrp instance
        instance: Cvrp = Cvrp()
        # Read the json data and update the object
        instance.fromJSON(json=object_dict["instance"])
        self.__cvrp_instance = instance

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

