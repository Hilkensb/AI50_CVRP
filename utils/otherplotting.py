#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set

# Other library
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
# To display plotly grah
import plotly.graph_objects as go
# To convert figure into html
from plotly.io import to_html

# Modules
from solution.cvrp.solution import SolutionCvrp
from utils.colorpallette import DEFAULT_COLOR_PALETTE


def __updateSolutionEvolutionAnimation(
    frame_num: int, solution_evolution: List[SolutionCvrp], ax: AxesSubplot,
    with_labels: bool = True, route_color: List[str] = DEFAULT_COLOR_PALETTE,
    depot_node_color: str = "#a6f68e", show_weight: bool = False,
    route_to_display: List[int] = None, node_size: int = 300,
    auto_node_size: bool= False
) -> None:
    """
    updateSolutionEvolutionAnimation()
    
    Function to create an animation of best solution evolution
    
    :param frame_num: The number of the frame in the animation
    :type frame_num: number of the frame
    :param ax: Axes of the animation
    :type ax: AxesSubplot
    :param solution_evolution: List of solution evolution
    :type solution_evolution: List[SolutionCvrp]
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
    """
    ax.clear()
    
    # Get the solutio to display
    sol: SolutionCvrp = solution_evolution[frame_num]

    # Get the graph, the graph layout, node colors and edges colors
    graph, position_layout, node_color_map, edge_color_map, weight_map, node_size = sol.drawMatPlotLib(
        route_color=route_color, depot_node_color=depot_node_color,
        route_to_display=route_to_display, node_size=node_size,
        auto_node_size=auto_node_size
    )
    
    # Draw the graph with the layout with the position
    nx.draw(
        graph, position_layout, node_color=node_color_map,
        edge_color=edge_color_map, with_labels=with_labels, node_size=node_size,
        ax=ax
    )

    # Set the title
    ax.set_title(f"Iteration {frame_num}")

def showSolutionEvolutionAnimationMatplotlib(
    solution_evolution: List[SolutionCvrp], with_labels: bool = True,
    route_color: List[str] = DEFAULT_COLOR_PALETTE,
    depot_node_color: str = "#a6f68e", show_weight: bool = False,
    route_to_display: List[int] = None, node_size: int = 300,
    auto_node_size: bool= False
) -> None:
    """
    showSolutionEvolutionAnimation()
    
    Function to create an animation of best solution evolution
    
    :param solution_evolution: List of solution evolution
    :type solution_evolution: List[SolutionCvrp]
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
    """
    
    # Build plot
    fig, ax = plt.subplots(figsize=(6,4))
    
    # Create the animation
    ani = animation.FuncAnimation(
        fig, __updateSolutionEvolutionAnimation, frames=len(solution_evolution),
        fargs=(solution_evolution, ax, with_labels, route_color, depot_node_color,
                show_weight, route_to_display, node_size, auto_node_size)
    )
    
    # Show the result
    plt.show()
    
    
def getSolutionEvolutionAnimationPlotly(
    solution_evolution: List[SolutionCvrp],depot_node_color: str = "#a6f68e",
    node_size: int = 15, route_color: List[str] = DEFAULT_COLOR_PALETTE,
    show_legend_edge: bool = True, show_legend_node: bool = False
) -> Figure:
    """
    getSolutionEvolutionAnimationPlotly()
    
    Function to create animation figure of solution evolution
    
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
    :return: Animation Figure of the solution evolution
    :rtype: Figure
    """
    
    # List of all iterations number
    # + 1 Because we want to start the iteration number at 1
    iterations = [str(iteration) for iteration in range(1, len(solution_evolution) + 1)]

    # make figure properties to build it then
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # Hover mode of the animation
    fig_dict["layout"]["hovermode"] = "closest"
    # Button menu of the animation
    # Create the play and pause button
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    # Create the slider
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Iteration #",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    
    
    # Get the node and edge scatter
    node_scatter_list, edge_scatter_list = solution_evolution[0].drawPlotly(
        depot_node_color=depot_node_color, node_size=node_size, 
        route_color=route_color, show_legend_edge=show_legend_edge,
        show_legend_node=show_legend_node
    )
    
    # Create the first frame
    for scatter in [*node_scatter_list, *edge_scatter_list]:
        fig_dict["data"].append(scatter)
    
    # Make the frame
    # For every iterations
    for index, iteration in enumerate(range(len(solution_evolution))):
        # Create the frame
        frame = {"data": [], "name": str(iteration)}
        
        # Get the node and edge scatter
        node_scatter_list, edge_scatter_list = solution_evolution[index].drawPlotly(
            depot_node_color=depot_node_color, node_size=node_size, 
            route_color=route_color, show_legend_edge=show_legend_edge,
            show_legend_node=show_legend_node
        )
        
        # for every scatter 
        # each scatter represent either node of a route or edges of a route
        for route in [*node_scatter_list, *edge_scatter_list]:
            # Add each scatter to the frame
            frame["data"].append(route)

        # Create the frame
        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [iteration],
            {"frame": {"duration": 300, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": iteration,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    # Add the slider
    fig_dict["layout"]["sliders"] = [sliders_dict]
    # Build the figure
    fig = go.Figure(fig_dict)
    
    # return the figure
    return fig

def getHtmlSolutionEvolutionAnimationPlotly(
    solution_evolution: List[SolutionCvrp],depot_node_color: str = "#a6f68e",
    node_size: int = 15, route_color: List[str] = DEFAULT_COLOR_PALETTE,
    show_legend_edge: bool = True, show_legend_node: bool = False,
    full_html: bool = True, default_width: str = '100%',
    default_height: str = '100%'
):
    """
    getHtmlSolutionEvolutionAnimationPlotly()
    
    Function to create animation figure of solution evolution
    
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
    :return: Html code of the animation figure
    :rtype: str
    """

    fig = getSolutionEvolutionAnimationPlotly(
        solution_evolution=solution_evolution,depot_node_color=depot_node_color,
        node_size=node_size, route_color=route_color,
        show_legend_edge=show_legend_edge, show_legend_node=show_legend_node
    )

    # Return the html string
    return to_html(
            fig=fig, full_html=full_html,
            default_width=default_width, default_height=default_height
    )
