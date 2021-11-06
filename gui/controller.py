# Standard Library
from __future__ import annotations
import threading
import json
import time

# Other Library
from flask import render_template, request, session, jsonify, Response, current_app, redirect
# To create markup from string
from markupsafe import Markup
# To create a pub/sub server
import redis as red
from flask_sse import sse

# Other module
from problem.cvrp.instance import Cvrp
from gui.config import *
from solution.metaheuristic.tabusearch import easyTabuSearch
from solution.constructive.clarkwrightsaving import clarkWrightSavingEvolution, clarkWrightSaving
from utils.redisutils import isRedisAvailable
from utils.runalgorithm import runAlgorithm
from utils.otherplotting import getHtmlSolutionEvolutionAnimationPlotly, getHtmlLineCostEvolution


# --------------------------- Controller function --------------------------- #

def index():
    """
    Controller to get the index page
    """

    # return the index.html template
    return render_template("index.html")

def readInstance(instance_type: str = "web"):
    """
    Controller that will read an instance file and give to the user the choice of algorithm to use
    
    :param instance_type: type of the instance type
    :type instance_type: str
    """
    
    if request.method == 'POST':  
        # Get the instance type
        instance_path: str = request.form['instance']
        # Build the instance
        cvrp_instance: Cvrp = buildInstance(path=instance_path, instance_type=instance_type)
        # Save the instance in session
        session['instance'] = cvrp_instance.toJSON()
        # Html representation of the instance graph
        instance_graph: str = cvrp_instance.getHtmlFigurePlotly(full_html=False)
        # Convert it to markup to have the displayed
        # if it is not made, the string of the html code will be displayed
        html_instance_graph = Markup(instance_graph)
        
        return render_template("instance_parameters.html", instance_graph=html_instance_graph)
    else:
        # return the index.html template
        return render_template('index.html')

def load():
    """
    Function that will launch the algorithm choose by the user
    """
    
    if request.method == 'POST':
      
        # Cvrp instance that we were asked for 
        cvrp_instance = Cvrp()
        cvrp_instance.fromJSON(json.loads(session['instance']))
      
        # List for algorithm function
        algo_function: List = []
        # List for algorithm name
        algo_name: List = []
        # List for algorithm kwarg
        algo_kwargs: List = []
        
        # if the clark wright should be runned
        if len(request.form.getlist("Clarck_Wright")) > 0:
            # add the algorithm
            algo_function.append(clarkWrightSavingEvolution)
            # Set the name of clark wirght
            algo_name.append("Clarck & Wright saving algorithm")
            # Set the algorithm param
            algo_kwargs.append({"cvrp": cvrp_instance})
          
        # TODO change the tabu search algo    
        # if the tabu search should be runned
        if len(request.form.getlist("Tabu_Search")) > 0:
            # add the algorithm
            algo_function.append(easyTabuSearch)
            # Set the name of clark wirght
            algo_name.append("Tabu Search")
            # Set the algorithm param
            algo_kwargs.append({
                "initial_solution": clarkWrightSaving(cvrp_instance),
                "number_iteration": int(request.form['TabuIteration']),
                "aspiration": request.form['TabuIteration'] == "True",
                "tabu_length": int(request.form['TabuLength']),
                "max_second_run": int(request.form['RunTimeTabu'])
            })
        
        # Get the flask application
        flask_applaction = current_app._get_current_object()

        # Create the thread
        threaded_task = threading.Thread(
            target=algorithmTask,
            kwargs={
                "flask_applaction": flask_applaction,
                "cvrp_instance": cvrp_instance,
                "algorithm_list": algo_function,
                "algorithm_kargs": algo_kwargs,
                "algorithm_name": algo_name
            },
            daemon=True
        )

        # launch the thread  
        threaded_task.start()
        
        # return the index.html template
        return render_template('load.html')

def stream():
    """
    Controller to get the message publish on the topic
    
    .. note: Inspired by https://github.com/petronetto/flask-redis-realtime-chat/blob/master/app.py
    """
    return Response(event_stream(), mimetype="text/event-stream")
    
def result():
    """
    Controller to display the result of the algorithms
    """
    
    return render_template(
        "result.html", algo_name=instance_save['algorithm_name'],
        solution_list=instance_save['algorithm_solution'],
        time_list=instance_save['algorithm_time'],
        total_time=sum(instance_save['algorithm_time']), enumerate=enumerate,
        cost_line_chart=instance_save['algorithm_solution_cost'],
        best_solution_algorithm=instance_save['algorithm_best_solution_cost'],
        algorithm_iteration=instance_save['algorithm_iteration'],
        best_overall_cost=instance_save['best_solution_cost'],
        best_algorithm=instance_save['best_algorithm'], round=round,
        number_vehicles=instance_save['minimum_vehicles']
    )


# ----------------------------- Other functions ----------------------------- #

def buildInstance(path: str, instance_type: str) -> Cvrp:
    """
    Function to build the cvrp instance
    
    :param path: Path of the instance
    :type path: str
    :param instance_type: type of the instance
    :type instance_type: Type of the instance file
    """
    return Cvrp(file_path=path, file_type=instance_type)
 
def event_stream() -> str:
    """
    Function to get the message publish on a topic
    
    :return: message publish into the wanted topic
    :rtype: byte string
    
    .. note: Inspired by https://github.com/petronetto/flask-redis-realtime-chat/blob/master/app.py
    """
    pubsub = redis_server.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(SOLUTION_TOPIC)
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

def algorithmTask(
    flask_applaction: Flask, cvrp_instance: Cvrp,
    algorithm_list: List, algorithm_kargs: List[Dict], algorithm_name: List[str]
) -> None:
    """
    Function to run the algorithm selected by the user
    
    :param flask_applaction: Flask application
    :type flask_applaction: Flask
    :param cvrp_instance: Instance of the cvrp
    :type cvrp_instance: Cvrp
    :param algorithm_list: List of algorithm
    :type algorithm_list: List of  function
    :param algorithm_kargs: arguments of functions
    :type algorithm_kargs: list of dictionnary
    :param algorithm_name: List of the algorithm name
    :type algorithm_name: List of strings
    """
       
    # Run the algorithm 
    algorithm_solution, cost_list, time_list = runAlgorithm(
        cvrp_instance=cvrp_instance, algorithm_list=algorithm_list,
        algorithm_kargs=algorithm_kargs, algorithm_name=algorithm_name
    )
    
    #with flask_applaction.test_request_context( '/result/'):
    #    session['algorithm_name'] = algorithm_name
    #    session['algorithm_solution'] = algorithm_solution
    
    # Tell to the user what is actually happening
    json_data = {
        "messages": "Generating the results... Please wait", "type": "info"
    }
    # Publish
    redis_server.publish(SOLUTION_TOPIC, json.dumps(json_data))
    
    # Save the result
    instance_save['algorithm_name'] = algorithm_name
    # Dictionnary to save solution linked to their solution
    solution_list: List = []
    # List to store the line graph
    solution_cost_list : List = []
    # List of numbers of iterations
    iteration_list: List[int] = []
    # dictionnary for all solution used
    for index in range(len(algorithm_name)):
        # Generate the html of the graph
        solution_representation: str = getHtmlSolutionEvolutionAnimationPlotly(
            solution_evolution=algorithm_solution[index], full_html=True, default_height="750px"
        )
        # Append the html in the list
        solution_list.append(solution_representation)
        # Generate the line chart
        cost_representation: str = getHtmlLineCostEvolution(
            cost_evolution=cost_list[index], full_html=True
        )
        # append the html of the line chart
        solution_cost_list.append(cost_representation)
        # Get the number of iteration
        iteration_number: int = len(cost_list[index])
        # append it to the list
        iteration_list.append(iteration_number)

    # Save the solution provided by the algorithm
    instance_save['algorithm_solution'] = solution_list
    # Save the time took by each algorithm
    instance_save['algorithm_time'] = time_list
    # Save the cost of solutions
    instance_save['algorithm_solution_cost'] = solution_cost_list
    # Save the cost of solutions
    # Since it only upgrade the solution we are sure that the best solution is at the end
    instance_save['algorithm_best_solution_cost'] = [cost[-1] for cost in cost_list]
    # Save th iteration number of algorithm
    instance_save['algorithm_iteration'] = iteration_list
    # Find the overall min solution cost
    instance_save['best_solution_cost'] = min(instance_save['algorithm_best_solution_cost'])
    # Find which algorithm returned the best result
    index_best_solution = instance_save['algorithm_best_solution_cost'].index(instance_save['best_solution_cost'])
    # Best algorithm
    instance_save['best_algorithm'] = algorithm_name[index_best_solution]
    # Minimum number of vehicles for the best solutions
    instance_save['minimum_vehicles'] = len(algorithm_solution[index_best_solution][-1].route)
        
    # Tell to the javsscript that the algorithm as ended
    redis_server.publish(SOLUTION_TOPIC, "END")
   
