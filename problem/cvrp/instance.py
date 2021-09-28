#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
import random as rand
from typing import List, Dict, Tuple, Union
import logging as log
import copy as copy

# Other Library
# Library for array, matrix, ...
import numpy as np
# Library to create a graph
import networkx as nx
# Library to get data from a website
import requests
# Library to create the graph plot
import matplotlib.pyplot as plt
# Library to generate html graph plot
import plotly.graph_objs as go
from plotly.offline import plot
# Library pandas from dataframe
import pandas as pd

# Modules
from problem.vrp_interface import VehiculeRootingProblem
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
import utils.mathfunctions as mathfunc


class Cvrp(VehiculeRootingProblem):
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, file_path: str = None, file_type: str = "local") -> Cvrp:
        """
        Constructor of Cvrp class

        :param file_path: Path to the instance file, defaults to None (opt.)
        :type file_path: str
        :param file_type: Type of the instance file. Should be either \"local\" or \"web\", defaults to \"local\" (opt.)
        :type file_type: str
        :return: Itself (implicitly as constructor)
        :rtype: :class:'Cvrp'
        :raises ValueError: when file_type is not either \"local\" or \"web\"
        :raises AssertionError: when file_type is \"web\" and the requests failled to get data from the url
        
        .. note:: If no arguments are passed, it will create a random instance
        
        .. warning:: If the parameter file_type is not either \"local\" or \"web\" raise a ValueError
        
        :exemple:

        >>> cvrp_instance = Cvrp()
        """
        
        # Customers variables
        # Number of customer
        self.__nb_customer: int = None
        # list of Customer
        self.__customers: List[CustomerCvrp] = []
        
        # Depot variables
        self.__depot: DepotCvrp = None
        
        # Vehicules variables
        # Capactiy of each vehicules
        self.__vehicule_capacity: int = None
        
        # if a path to file have been specified create the instance of data
        # stored in the given file
        if file_path is not None:
            # If the instance file is in local
            if file_type == "local":
                self.readInstanceFile(file_path=file_path)
            # If the instance file is on internet  
            elif file_type == "web":
                self.readInstanceVrpWeb(url=file_path)
            else:
                raise ValueError(f"The parameter file_type should be either \"local\" or \"web\", not \"{file_type}\"")
        # If no file have been passed, then create a random instance
        else:
            self.randomInstance()

    def __copy__(self) -> Cvrp:
        """
        copy
        
        Create a copy of the cvrp instance
        
        :return: A copy of the cvrp instance
        :rtype: :class:'Cvrp'
        
        :exemple:

        >>> import copy
        >>> cvrp_copy = copy.copy(cvrp_instance)
        """
        
        # Copy every customer
        customers_copy: List[CustomerCvrp] = [copy.copy(customer) for customer in self.__customers]
        # Copy the depot
        depot_copy: DepotCvrp = copy.copy(self.__depot)
        
        # Create a new cvrp object
        cvrp_copy: Cvrp = Cvrp()
        # Set the customers of this new instance
        cvrp_copy.customers = customers_copy
        # Set the depot of this new instance
        cvrp_copy.depot = depot_copy
        # Set the vehicule_capacity of this new instance
        cvrp_copy.vehicule_capacity = self.__vehicule_capacity
        
        # Return the copy
        return cvrp_copy
        

    def __repr__(self) -> str:
        """
        repr
        
        Method to get the representation of the CVRP problem
        
        :return: The name of the instance
        :rtype: str
        """
        return f"CVRP-n{self.__nb_customer + 1}-k{self.min_vehicule_number()}"
      
    def __str__(self) -> str:
        """
        """
        
        # Get the matrix of the instance
        # Round the distance and put them in int
        distance_matrix: np.matrix = self.distanceMatrix(round_distance=True, precision=0)
        
        # Get the id of nodes to put it then as column and row name
        # At first only the node id of customers
        nodes_id: List[int] = [customer.node_id for customer in self.__customers]
        # Add finaly the node id of the depot
        nodes_id.append(self.__depot.node_id)
        # Sort the list
        nodes_id.sort()
        
        # Create a pandas dataframe to show column name and row name of the matrix
        matrix_data_frame = pd.DataFrame(distance_matrix, columns=nodes_id, index=nodes_id)
        
        # Return the string value of the dataframe
        return str(matrix_data_frame)
        

# ---------------------------- Inhereted Methods ---------------------------- #
    
    def distanceMatrix(self, round_distance: bool = False, precision: int = 2) -> np.matrix:   
        """
        distanceMatrix
        
        Method to get the distance matrix of the cvrp instance (node are sorted
        by their node_id)
        
        :param round_distance: If the distance between nodes should rounded or not, default to False (opt.)
        :type round_distance: bool
        :param precision: Precision of the round, default to 2 (opt.)
        :type precision: int
        :return: The distance matrix of the instance
        :rtype: :class:'numpy.matrix'
        
        .. note:: All the distance are round to the nearest int
        
        .. note:: The diagonal of the matrix is filled with -1
        
        :exemple:

        >>> dm = cvrp_instance.distanceMatrix()
        """
        # List all nodes (customers + depot)
        node_list: List[Union[CustomerCvrp, DepotCvrp]] = self.__customers[:]
        node_list.append(self.__depot)
        
        # Sort the list by the node id
        node_list.sort(key=lambda node: node.node_id)
        
        # Create the distance matrix
        # Round the distance to the nearest integer
        distance_matrix: np.matrix = np.matrix([
            [
                round(mathfunc.euclideanDistance(node1, node2), precision)
                if round_distance else mathfunc.euclideanDistance(node1, node2)
                for node2 in node_list
            ] for node1 in node_list
        ])
             
        # fill the diagonal of the distance matrix with -1
        np.fill_diagonal(distance_matrix, -1)
        
        return distance_matrix
        
    def graph(self) -> nx.Graph:
        """
        graph
        
        Method to get the graph (complete graph) generated with networkx
        
        :return: The graph of the cvrp instance
        :rtype: :class:'nx.Graph'
        
        .. note:: All the distance are round to the nearest int
        
        :exemple:

        >>> g = cvrp_instance.graph()
        """
        # Create an undirected graph
        graph: nx.Graph = nx.Graph()
        
        # Create a list of node id (for all the customers)
        node_id_list: List[int] = [customer.node_id for customer in self.__customers]
        # Add the depot to the node id list
        node_id_list.append(self.__depot.node_id)
        # Sort the list by id
        node_id_list.sort()
        # Create edges from the list of node id
        graph.add_nodes_from(node_id_list)
        
        # List of weighted edge
        weighted_edge_list = []
        # For each node get the index and node_id of the list
        for index_1, node_id_1 in enumerate(node_id_list[:-1]):
            # For each node_id from the node_1 index + 1 to the last node
            for node_id_2 in node_id_list[index_1 + 1:]:
                # Get the node (either CustomerCvrp or DepotCvrp) with the node_id_1
                node_1: Union[CustomerCvrp, DepotCvrp] = self.getNodeById(id_searched=node_id_1)
                # Get the node (either CustomerCvrp or DepotCvrp) with the node_id_2
                node_2: Union[CustomerCvrp, DepotCvrp] = self.getNodeById(id_searched=node_id_2)
                # Calcul the distance between the node_1 and the node_2
                distance: int = round(mathfunc.euclideanDistance(node_1, node_2))
                # Create a tuple composed (in that order) of first node, second node, weight
                weighted_edge: Tuple[int, int, int] = (node_id_1, node_id_2, distance)
                # Add the tuple representing the edge to the list of weighted edge
                weighted_edge_list.append(weighted_edge)
        
        # Pass the list of weighted list to build the edges
        # At the end, the graph will be a complete and weighted graph        
        graph.add_weighted_edges_from(weighted_edge_list)
        
        # Return the graph build
        return graph

    def readInstanceVrp(self, file_path: str) -> Cvrp:
        """
        readInstanceVrp
        
        Method to read instance of vrp on local machine
        
        :param file_path: Path of the file where the vrp instance is
        :type url: str
        :return: Itself
        :rtype: :class:'Cvrp'
        :raises FileNotFoundError: when the file has not been found
        :raises ValueError: when the instance could not have been parsed
        
        .. warning:: Please ensure the format of the instance is correct.
        Exemples of the file format can be found on: http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
        
        :exemple:

        >>> cvrp_instance.readInstanceVrp(file_path=\"C:\\Users\\YourName\\Documents\\instance.vrp\")
        """
        
        # Can raise FileNotFoundError /!\
        instance_file: file = open(file_path, "r")
        
        # Get the data stored inside the file
        instance_data: str = instance_file.read()
        # Close the file
        instance_file.close()
        
        try:
            # Parse the data to create the object
            self.__parseVrp(instance_data)
        # If an exception occurs at lower level
        # It means that file could not have been parsed
        # The file must have been in a wrong format and raise a new Exception
        except Exception as e:
            raise ValueError(f"The instance could not have been parsed. Reason: {e}")

    def readInstanceVrpWeb(self, url: str) -> Cvrp:
        """
        readInstanceVrpWeb
        
        Method to read instance of vrp on internet
        
        :param url: Url of the page where the vrp instance is
        :type url: str
        :return: Itself
        :rtype: :class:'Cvrp'
        :raises AssertionError: when the requests failled to get data from the url
        :raises ValueError: when the instance could not have been parsed
        
        .. warning:: If the url is incorrect raise a ValueError
        
        .. warning:: Please ensure the format of the instance is correct.
        Exemples of the file format can be found on: http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
        
        :exemple:

        >>> cvrp_instance.readInstanceVrpWeb(url=\"http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp\")
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
            self.__parseVrp(data_request.text)
        # If an exception occurs at lower level
        # It means that file could not have been parsed
        # The file must have been in a wrong format and raise a new Exception
        except Exception as e:
            raise ValueError(f"The instance could not have been parsed. Reason: {e}")
        
        # Return itself
        return self

    # TODO
    def writeInstanceVrp(self, file_path: str) -> None:  
        """
        """
        pass
        
    def randomInstance(
        self, nb_customer: int = 30, vehicule_capacity: int = 100,
        customer_demand_lb: int = 1, customer_demand_ub: int = 20,
        grid_size: int = 100
    ) -> Cvrp:
        """
        randomInstance
        
        Method to create a random instance of cvrp
        
        :param nb_customer: The number of customers in the instance, default to 30 (opt.)
        :type nb_customer: int
        :param vehicule_capacity: The capacity of the vehicule's fleet, default to 100 (opt.)
        :type vehicule_capacity: int
        :param customer_demand_lb: Lowerbound of the customer demand which will be distributed randomly and uniformely, default to 1 (opt.)
        :type customer_demand_lb: int
        :param customer_demand_ub: Upperbound of the customer demand which will be distributed randomly and uniformely, default to 20 (opt.)
        :type customer_demand_ub: int
        :param grid_size: The size of the grid in other word the maximum value
        """
        
        # Set the parameters passed as argments
        self.__nb_customer = nb_customer
        self.__vehicule_capacity = vehicule_capacity
        # Clear the list (in case something was generated previously)
        self.__customers = []
        
        # Create ever customer
        for customer_number in range(1, self.__nb_customer + 1):
            # Create the CustomerCvrp object that is storing curstomer information
            # Generate randomly value for each information of the customer
            customer: CustomerCvrp = CustomerCvrp(
                node_id=customer_number, x=rand.randint(0, grid_size),
                y=rand.randint(0, grid_size),
                demand=rand.randint(customer_demand_lb, customer_demand_ub)
            )
            
            # Create the informations about the customer
            self.__customers.append(customer)

        # Create the depot
        self.__depot = DepotCvrp(
            node_id=self.__nb_customer + 1, x=rand.randint(0, grid_size),
            y=rand.randint(0, grid_size)
        )
        
        return self

    def min_vehicule_number(self) -> int:
        """
        """
        
        # Get all the customers demand into a list
        # To do so iterate throw all customers (only the customers node)
        # and get their demand
        customers_demand: List[int] = [customer.demand for customer in self.__customers]
        
        # Sort the demand (in decreasing order)
        customers_demand.sort(reverse=True)
        
        # Calcul the number minimum of vehicule to solve this problem
        # Counter of the number min of vehicule
        nb_vehicule: int = 0
        # To calculate the number of vehicule we need to have a variable that will
        # be decreasing for every customer demand and which start from the 
        # vehicule capacity 
        actual_vehicule_capacity: int = self.__vehicule_capacity

        # Check if a solution exists or not
        # If the highest demand is higher than the vehicule capacity,
        # it means that this customer (may be others too ?) cannot be delivered by
        # vehicule with this capacity
        # There will no feasible solution for this problem (since at least one
        # customer can't be delivered).
        # Since there will be no solution, the minimum vehicule to solve the problem
        # is none
        if customers_demand[0] > self.__vehicule_capacity:
            # Raise a RuntimeError to show that there's no feasible solution
            raise RuntimeError(f"The highest customer demand is higher than the vehicule capacity ({customers_demand[0]} > {self.__vehicule_capacity}). At least one (or more) customer(s) can't be deliver by a vehicule. No feasible solution for this problem!") 

        # while the customers_demand has values in it, run the while loop
        while customers_demand:
            # Reset the actual vehicule capacity (we start from a new vehicule,
            # because the previous had his maximum capacity)
            actual_vehicule_capacity = self.__vehicule_capacity
            # Increase the number of vehicule by 1, because the previous cannot
            # be filled more
            nb_vehicule += 1
            # Customers demand that have not been delivered by the previous vehicules
            # Create a copy of the customer_demand
            # Since we are using after a for loop, we can't pop element of the list
            # we are iterating throw in the for loop
            # We need 2 list, one we iterate throw and another one where we pop
            # demand that have been delivered by the vehicule
            # Update the customers demand
            actual_customer_demand = customers_demand[:]
            
            # for every demand (sorted in decreasing order)
            for demand in actual_customer_demand:
                # Check if the demand can be delivered by the vehicule
                if demand <= actual_vehicule_capacity:
                    # Add the demand in the vehicule
                    # So remove the demand space free in the vehicule
                    actual_vehicule_capacity -= demand
                    # The customer demand have been solved
                    # We can remove it from the list of demand
                    customers_demand.remove(demand)
              
        # Return the number minimum of vehicule to solve the problem            
        return nb_vehicule
                    

# --------------------------------- Methods --------------------------------- #

# ______________________________ Diplay Method ______________________________ #

    def showConsole(self) -> None:
        """
        """
        
        # Print the depot node id
        print(f"Depot node id: {self.__depot.node_id}")
        # Print the string value of the instance
        print(self.__str__())

    def showMathPlotLib(
        self, show_edge: bool = False, customer_node_color: str = "#8eaaf6",
        depot_node_color: str = "#a6f68e", with_labels: bool = True
    ) -> None:
        """
        """
        
        # Get the graph, layout and node color ready to be draw
        graph, position_layout, color_map = self.__drawMathPlotLib(
            show_edge=show_edge, customer_node_color=customer_node_color,
            depot_node_color=depot_node_color
        )
        
        # Draw the graph with the layout with the position
        nx.draw(graph, position_layout, node_color=color_map, with_labels=with_labels)
        # Display the graph
        plt.show()
        
    def getFigureMathPlotLib(
        self, show_edge: bool = False, customer_node_color: str = "#8eaaf6",
        depot_node_color: str = "#a6f68e", with_labels: bool = True,
        fig_size: Tuple[int, int] = (5, 4)
    ) -> matplotlib.figure.Figure:
        """
        """
        
        # Create the plot
        figure = plt.figure(figsize=fig_size)
        subplot = figure.add_subplot(111)
        plt.axis('off')
        
        # Get the graph, layout and node color ready to be draw
        graph, position_layout, color_map = self.__drawMathPlotLib(
            show_edge=show_edge, customer_node_color=customer_node_color,
            depot_node_color=depot_node_color
        )
        
        # Draw the graph with the layout with the position
        nx.draw_networkx(graph, pos=position_layout, ax=subplot, node_color=color_map, with_labels=with_labels)
        # Set the axis
        xlim=subplot.get_xlim()
        ylim=subplot.get_ylim()
        
        return figure
      
    # TODO: Size of the nodes depending of their demand    
    def __drawMathPlotLib(
        self, show_edge: bool = False, customer_node_color: str = "#8eaaf6",
        depot_node_color: str = "#a6f68e"
    ) -> Tuple[nx.graph, nx.spring_layout, List[str]]:
        """
        """
        
        # Get the graph
        graph: nx.Graph = self.graph()
        
        # If we don't want to show the edges of the graph
        if not show_edge:
            # Create a list containing all the edges of the graph to then remove them
            edges: List[nx.classes.reportviews.EdgeView] = list(graph.edges)
            # remove the edges
            graph.remove_edges_from(edges)
        
        # Set the position of the nodes
        # Dict with two of the positions set
        fixed_positions: Dict[int, Tuple[int, int]] = {}
        # For every customer
        for customer in self.__customers:
            # Set his position
            fixed_positions[customer.node_id] = customer.getCoordinates()
        
        # Set the position of the depot
        fixed_positions[self.__depot.node_id] = self.__depot.getCoordinates()
        
        # Create a color map to color each customer with a color and the depot with another one
        # the color has to be in str
        color_map: List[str] = []
        # For every node set his color
        for node in graph:
            # If the node is representing the depot
            if node == self.__depot.node_id:
                color_map.append(depot_node_color)
            # If it's not a depot, it means that the node is representing a customer
            # So we have to color it with the customer color
            else:
                color_map.append(customer_node_color)
        
        # Get the keys of the list of position
        fixed_nodes: List[int] = fixed_positions.keys()
        # Create the layout of the graph with the position
        position_layout: nx.spring_layout = nx.spring_layout(graph, pos=fixed_positions, fixed = fixed_nodes)
        
        return graph, position_layout, color_map
        
    def showPlotly(self, folderPath: str, name: str) -> None:
        """
        """

        # Get the graph
        graph: nx.graph = self.graph()

        # Looks for the graph's communities (get a list of connected node)
        nodes: List[int] = list(graph.nodes)

        # Generates the layout of the graph
        layout_graph: nx.spring_layout = nx.spring_layout(graph, dim=2)
        # x-coordinates of nodes
        Xn = [self.getNodeById(int(node)).x for node in nodes]
        # y-coordinates
        Yn = [self.getNodeById(int(node)).y for node in nodes]  

        # Create a scatter plot with the edge
        traceEdges = go.Scatter(  x=[],
                              y=[],
                              mode='lines',
                              line=dict(color='rgb(90, 90, 90)', width=1),
                              hoverinfo='none'
                            )

        # Create a scatter plot with the nodes
        traceNodes = go.Scatter(  x=Xn,
                              y=Yn,
                              mode='markers+text',
                              name='Nodes',
                              marker=dict(symbol='circle',
                                          size=8,
                                          color="#006699",
                                          colorscale='Viridis',
                                          line=dict(color='rgb(255,255,255)', width=1)
                                          ),
                              text=nodes,
                              textposition='top center',
                              hoverinfo='none'
                              )

        # Build the axis (and their layout)
        xaxis = dict(
                    backgroundcolor="rgb(200, 200, 230)",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    zerolinecolor="rgb(255, 255, 255)"
                    )
        yaxis = dict(
                    backgroundcolor="rgb(230, 200,230)",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    zerolinecolor="rgb(255, 255, 255)"
                    )

        # Create the layout of the plot
        layout = go.Layout(
            title=name,
            width=700,
            height=700,
            showlegend=False,
            plot_bgcolor="rgb(230, 230, 200)",
            scene=dict(
                xaxis=dict(xaxis),
                yaxis=dict(yaxis)
            ),
            margin=dict(
                t=100
            ),
            hovermode='closest'
            , )
            
        # Set the data to display
        data = [traceEdges, traceNodes]
        fig = go.Figure(data=data, layout=layout)
        
        # Write the html file
        plotDir = folderPath + "/"
        plot(fig, filename=plotDir + name + ".html")

# ______________________________ Parse Methods ______________________________ #

    def __parseVrp(self, data_to_parse: str) -> None:
        """
        Inspired by : https://github.com/scespinoza/CVRP-Formulations/blob/master/cvrp.py
        """
        
        # split the string into lines
        cvrp: List[str] = data_to_parse.split("\n")
        # Get the value of the parameter of the cvrp
        header: Dict[str, str] = {}
        # The other data (nodes, demands, ...)
        data: List[str] = []
        
        # Clear the customer array
        self.__customers = []
        
        # For each line in the cvrp input data
        for line in cvrp:
            # Parse the paramter
            # The first element is the name of the parameter
            # The others elements are the data
            thisline: List[str] = line.split(':')
            # If the array has more than one element it means that there's 
            # the parameter name and data
            if len(thisline) > 1:
                header[thisline[0].strip()] = ';'.join(thisline[1:]).strip()
            # If there's only one element in the array split of the line
            # It means there's either only data or only parameter name
            else:
                data.append(line.strip())
       
        # Get the number of customer
        # The DIMENSION is the number of node so customer + 1 depot
        # So the number of customer is the DIMENSION - 1
        self.__nb_customer = int(header['DIMENSION']) - 1
        # Get the vehicule capacity
        self.__vehicule_capacity = int(header['CAPACITY'])
        
        # Parse the node section
        # The 1st element is the node id
        # The 2nd element is the x coordinate
        # The 3rd element is the y coordinate
        # At first we search the line of NODE_COORD_SECTION
        start_nodes: int = data.index('NODE_COORD_SECTION')
        # Then read every line from the first line of the section + 1
        # (The first line is the name of the section)
        # Read the number of customer + 1 (read every customer + 1 depot)
        nodes_raw_data: List[str] = data[start_nodes + 1:start_nodes + self.__nb_customer + 2]
        # Finaly create a list of node
        # each node is represented by a tuple composed (in this order) of
        # node id, x coordinate, y coordinate
        nodes_raw_list: List[Tuple[int, int, int]] = [
            (
                int(node.split(" ")[0]),  int(node.split(" ")[1]),
                int(node.split(" ")[2])
            )
            for node in nodes_raw_data
        ]

        # Parse the demand section
        # The 1st element is the node id
        # The 2nd element is the demand of the customer
        # At first we search the line of DEMAND_SECTION
        start_demand: int = data.index('DEMAND_SECTION')
        # Then read every line from the first line of the section + 1
        # (The first line is the name of the section)
        # Read the number of customer + 1 (read every customer + 1 depot)
        demands_raw_data: List[str] = data[start_demand + 1: start_demand + self.__nb_customer + 2]
        # Finaly create a list of node
        # each node is represented by a tuple composed (in this order) of
        # node id, demand of customer
        demands_raw_list: List[Tuple[int, int]] = np.array([
            (
                int(demand.split(" ")[0]), int(demand.split(" ")[1])
            )
            for demand in demands_raw_data
        ])

        # Parse the demand section
        # This section contains the node id of the depot
        # At first we search the line of DEMAND_SECTION
        start_depot: int = data.index('DEPOT_SECTION')
        # Since we are in classical CVRP, there is only one depot
        # So we have only one line to read and to convert, no need of lists here
        depot_node_id: int = int(data[start_depot+1])
        
        # For each node in the node list
        for node in nodes_raw_list:
            # get the data stored in the tuple representing the node
            # Get the node id 
            node_id: int = node[0]
            # Get the node x coordinate
            node_x: int = node[1]
            # Get the node y coordinate
            node_y: int = node[2]
            
            # If the node has the same id as the depot
            # Create a depot instead of a customer
            if node_id == depot_node_id:
                # Create the depot
                self.__depot = DepotCvrp(node_id=node_id, x=node_x, y=node_y)
                # Go to the next node
                continue

            # Get the demand
            # Create a filter to get the demand linked with the node id
            # Then when the filter have been applied convert it to a list
            # Since the id must be unique, the list should be composed of one element
            # if more it means that the id was not unique in instance file
            # if 0 elmeent it means that the node has no demand linked to it
            # in both case it's not NORMAL
            # /!\ if 0 element it will raise a keyError /!\
            # Then we know that the node id is the first element of the tuple
            # and the demand is the second
            # So we just have to get the second element (the demand) 
            node_demand: int = list(filter(lambda demand: demand[0] == node_id, demands_raw_list))[0][1]
            
            # Create the customer
            customer: CustomerCvrp = CustomerCvrp(
                node_id=node_id, x=node_x, y=node_y, demand=node_demand
            )
            
            # Add the customer
            self.__customers.append(customer)

# ____________________________ Searching Methods ____________________________ #

    def getCustomerById(self, id_searched: int) -> CustomerCvrp:
        """
        """
        
        # Filter all customer with their id
        # The result a list of customer
        customer_matches: List[CustomerCvrp] = list(filter(lambda customer: customer.node_id == id_searched, self.__customers))

        # Initialize the customer found variable
        # This variable will be the one return
        customer_found: CustomerCvrp = None
        # If zero customer have been found with the given id, it will trigger
        # no if condition and will stay None
        # If one customer have been found the elif condition will trigger,
        # which will get the only element found and put it in customer_found
        # If more than one customer have been found with the given id, it will
        # raise an KeyError Exception
        if len(customer_matches) > 1:
            # Raise the exception because of multiple customer with the same id,
            # in the same vrp instance
            raise KeyError(f"Multiple customer with the id {id_searched}")
        elif len(customer_matches) == 1:
            # Get the only customer found with the given id
            customer_found = customer_matches[0]

        # Return the result
        return customer_found
        
    def getCustomerByCustomerNumber(self, customer_number_searched: int) -> CustomerCvrp:
        """
        """
        
        # Get a copy (NOT a deepcopy) of the customers list
        customers_list: List[CustomerCvrp] = self.__customers[:]

        # Sort the list by node id
        customers_list.sort(key=lambda customer: customer.node_id)
        
        # Get the customer
        # /!\ can raise a ValueError if the node_id is not in the list
        # We then need to add 1 because indexing in python start at 0, but
        # the customer number start at 1
        customer: CustomerCvrp = customers_list[customer_number_searched - 1]
        
        return customer
        
    def getNodeById(self, id_searched: int) -> Union[CustomerCvrp, DepotCvrp]:
        """
        """
        
        # List all nodes (customers + depot)
        node_list: List[Union[CustomerCvrp, DepotCvrp]] = self.__customers[:]
        node_list.append(self.__depot)
        
        # Filter all customer with their id
        # The result a list of customer
        node_matches: List[Union[CustomerCvrp, DepotCvrp]] = list(filter(
            lambda customer: customer.node_id == id_searched, node_list
        ))

        # Initialize the node found variable
        # This variable will be the one return
        node_found: Union[CustomerCvrp, DepotCvrp] = None
        # If zero node have been found with the given id, it will trigger
        # no if condition and will stay None
        # If one node have been found the elif condition will trigger,
        # which will get the only element found and put it in node_found
        # If more than one node have been found with the given id, it will
        # raise an KeyError Exception
        if len(node_matches) > 1:
            # Raise the exception because of multiple node with the same id,
            # in the same vrp instance
            raise KeyError(f"Multiple customer with the id {id_searched}")
        elif len(node_matches) == 1:
            # Get the only node found with the given id
            node_found = node_matches[0]

        # Return the result
        return node_found

    def getCustomerNumberByNodeId(self, node_id: int) -> int:
        """
        getCustomerNumberByNodeId
        
        Method to get the customer number (used in solution of vrp) to node id
        (used in instance of vrp). It only sort customers by their node id and then
        return the index of the node id searched.
        
        :param node_id: The node id that we are surching for
        :type node_id: int
        :return: The customer number of the node searched
        :rtype: int
        :raises ValueError: when the node id either does not exists or is the node id of the depot
        
        .. warning: The node id must be linked to a customer. If the node id
        is linked to the depot an error will be raised
        
        :example:
            
        >>> customer_num = cvrp_instance.getCustomerNumberByNodeId(node_id=6)
        >>> customer_num
        5
        """

        # Create a list of customer node id (for all the customers in the cvrp instance)
        customer_id_list: List[int] = [customer.node_id for customer in self.__customers]
        # Sort the list by id
        customer_id_list.sort()
        # Get the customer number
        # /!\ can raise a ValueError if the node_id is not in the list
        # We then need to add 1 because indexing in python start at 0, but
        # the customer number start at 1
        customer_number: int = customer_id_list.index(node_id) + 1
        
        return customer_number
        
    def getNodeIdByCustomerNumber(self, customer_number: int) -> int:
        """
        getNodeIdByCustomerNumber
        
        Method to get the customer node id (used in instance of vrp)
        to customer number (used in solution of vrp).
        It only sort customers by their node id and then
        return the value indexed at customer_number value
        
        :param customer_number: The customer number that we are surching for
        :type customer_number: int
        :return: The node id of the customer searched
        :rtype: int
        :raises IndexError: when the customer number does not exists 
        
        :example:
        
        >>> node_id = cvrp_instance.getNodeIdByCustomerNumber(node_id=5)
        >>> node_id
        6
        """
        
        # Create a list of customer node id (for all the customers in the cvrp instance)
        customer_id_list: List[int] = [customer.node_id for customer in self.__customers]
        # Sort the list by id
        customer_id_list.sort()
        # Get the customer number
        # /!\ can raise a IndexError if the customer number is higher than the number of customers in the instance
        # We ten need to minus 1 because indexing in python start at 0, but
        # the customer number start at 1 -> So we will have the real index
        customer_id: int = customer_id_list[customer_number - 1]

        return customer_id

# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def nb_customer(self) -> int:
        return self.__nb_customer
        
        
    @property 
    def customers(self) -> List[CustomerCvrp]:
        return self.__customers
        
    @customers.setter
    def customers(self, value: List[CustomerCvrp]) -> None:  
        self.__customers = value
        # Also set the number of customer depending of the length of the
        # customer's list
        self.__nb_customer = len(value)


    @property 
    def depot(self) -> DepotCvrp:
        return self.__depot
        
    @depot.setter
    def depot(self, value: DepotCvrp) -> None:  
        self.__depot = value

    @property 
    def vehicule_capacity(self) -> int:
        return self.__vehicule_capacity
        
    @vehicule_capacity.setter
    def vehicule_capacity(self, value: int) -> None:  
        self.__vehicule_capacity = value

