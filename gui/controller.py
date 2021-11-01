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
from solution.metaheuristic.tabusearch import tabuSearch
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from utils.redisutils import isRedisAvailable
from utils.runalgorithm import runAlgorithm


# --------------------------- Controller function --------------------------- #

def index():
    """
    """

    # return the index.html template
    return render_template("index.html")

def readInstance(instance_type: str = "web"):
    """
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
            algo_function.append(clarkWrightSaving)
            # Set the name of clark wirght
            algo_name.append("Clarck & Wright saving algorithm")
            # Set the algorithm param
            algo_kwargs.append({"cvrp": cvrp_instance})
          
        # TODO change the tabu search algo    
        # if the tabu search should be runned
        if len(request.form.getlist("Tabu_Search")) > 0:
            # add the algorithm
            algo_function.append(tabuSearch)
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
    """
    return Response(event_stream(), mimetype="text/event-stream")


# ----------------------------- Other functions ----------------------------- #

def buildInstance(path: str, instance_type: str):
    """
    """
    return Cvrp(file_path=path, file_type=instance_type)
 
def event_stream():
    pubsub = redis_server.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(SOLUTION_TOPIC)
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

def algorithmTask(
    flask_applaction: Flask, cvrp_instance: Cvrp,
    algorithm_list: List, algorithm_kargs: List, algorithm_name: List
):
    """
    """
       
    # Run the algorithm 
    runAlgorithm(
        cvrp_instance=cvrp_instance, algorithm_list=algorithm_list,
        algorithm_kargs=algorithm_kargs, algorithm_name=algorithm_name
    )
    
    with flask_applaction.test_request_context( '/load/'):
        pass
        
    redis_server.publish(SOLUTION_TOPIC, "END")
   
