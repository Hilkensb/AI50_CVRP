# Standard Library
from __future__ import annotations
import threading
import json
import time
import uuid
import os

# Other Library
from flask import render_template, request, session, jsonify, Response, current_app, redirect, url_for, send_file
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
from solution.metaheuristic.gwo import greyWolfSolver
from solution.multiagents.sarlcommunication import sarlSender
from utils.mailsender import sendMailFinished
from utils.pdfcreator import createPDF


# --------------------------- Controller function --------------------------- #

def index():
    """
    Controller to get the index page
    """

    # return the index.html template
    return render_template("index.html", instance_id=uuid.uuid1())

def evaluateParams(
    cvrp_id: str, TabuIteration: int = 0, TabuLength: int = 0, RunTimeTabu: int = 0
):
    """
    """
    return jsonify(messages=["All your parameters are good.", "Keep using them."])

def readInstance(instance_type: str, cvrp_id: str):
    """
    Controller that will read an instance file and give to the user the choice of algorithm to use
    
    :param instance_type: type of the instance type
    :type instance_type: str
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    """
    
    # If the method is post (posting form)
    if request.method == 'POST': 
        # If the instance come from the web
        if instance_type == "web": 
            # Get the instance type
            instance_path: str = request.form['instance']
            # Build the instance
            cvrp_instance: Cvrp = buildInstance(path=instance_path, instance_type=instance_type)
        else:
            # Get the instance type
            instance_string: str = request.files['instance'].read().decode('ascii')
            # Build the instance
            cvrp_instance: Cvrp = buildInstance(path=instance_string, instance_type="string")
            
        # Save the instance in session
        # Session object can't handle big instance of cvrp
        # session['instance'] = cvrp_instance.toJSON()
        instance_save[f'instance_{cvrp_id}'] = cvrp_instance.toJSON()
        # Html representation of the instance graph
        instance_graph: str = cvrp_instance.getHtmlFigurePlotly(full_html=False)
        # Convert it to markup to have the displayed
        # if it is not made, the string of the html code will be displayed
        html_instance_graph = Markup(instance_graph)
        
        return render_template(
            "instance_parameters.html", instance_graph=html_instance_graph,
            nb_customer=cvrp_instance.nb_customer, round=round, min=min,
            max=max, instance_id=cvrp_id
        )
    else:
        # return the index.html template
        return render_template('index.html')

def randomInstance(cvrp_id: str):
    """
    Controller that will read an instance file and give to the user the choice of algorithm to use
    
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    """
    
        # If the method is post (posting form)
    if request.method == 'POST': 
        # Build the instance
        cvrp_instance: Cvrp = Cvrp()
        # Set the param of the random instance
        cvrp_instance.randomInstance(
            nb_customer=int(request.form['nb_customer']),
            vehicule_capacity=int(request.form['vehicule_capacity']),
            customer_demand_lb=int(request.form['customer_demand_lb']),
            customer_demand_ub=int(request.form['customer_demand_ub'])
        )
            
        # Save the instance in session
        # Session object can't handle big instance of cvrp
        # session['instance'] = cvrp_instance.toJSON()
        instance_save[f'instance_{cvrp_id}'] = cvrp_instance.toJSON()
        # Html representation of the instance graph
        instance_graph: str = cvrp_instance.getHtmlFigurePlotly(full_html=False)
        # Convert it to markup to have the displayed
        # if it is not made, the string of the html code will be displayed
        html_instance_graph = Markup(instance_graph)
        
        return render_template(
            "instance_parameters.html", instance_graph=html_instance_graph,
            nb_customer=cvrp_instance.nb_customer, round=round, min=min,
            max=max, instance_id=cvrp_id
        )
    else:
        # return the index.html template
        return render_template('index.html')

def load(cvrp_id: str):
    """
    Function that will launch the algorithm choose by the user
    
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    """
    
    if request.method == 'POST':
      
        # Cvrp instance that we were asked for 
        cvrp_instance = Cvrp()
        # cvrp_instance.fromJSON(json.loads(session['instance']))
        cvrp_instance.fromJSON(json.loads(instance_save[f'instance_{cvrp_id}']))
      
        # List for algorithm function
        algo_function: List = []
        # List for algorithm name
        algo_name: List = []
        # List for algorithm kwarg
        algo_kwargs: List = []
        # Create a list to know if the solution provided contains evolution
        instance_save[f'has_evolution_{cvrp_id}']: List = []
        
        # if the clark wright should be runned
        if len(request.form.getlist("Clarck_Wright")) > 0:
            # add the algorithm
            algo_function.append(clarkWrightSavingEvolution)
            # Set the name of clark wirght
            algo_name.append("Clarck & Wright saving algorithm")
            # Set the algorithm param
            algo_kwargs.append({
                "cvrp": cvrp_instance, "publish_topic": f"{SOLUTION_TOPIC}_{cvrp_id}"
            })
            # Is there evolution in the solution
            instance_save[f'has_evolution_{cvrp_id}'].append(True)
   
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
                "max_second_run": int(request.form['RunTimeTabu']),
                "publish_topic": f"{SOLUTION_TOPIC}_{cvrp_id}"
            })
            # Is there evolution in the solution
            instance_save[f'has_evolution_{cvrp_id}'].append(True)
            
        # if the tabu search should be runned
        if len(request.form.getlist("MAS_Solver")) > 0:
            # add the algorithm
            algo_function.append(sarlSender)
            # Set the name of clark wirght
            algo_name.append("Multi-Agent System")
            # Set the algorithm param
            algo_kwargs.append({
                "topic": cvrp_id, "instance": cvrp_instance
            })
            # Is there evolution in the solution
            instance_save[f'has_evolution_{cvrp_id}'].append(False)
            
        # if the tabu search should be runned
        if len(request.form.getlist("Wolf")) > 0:
            # add the algorithm
            algo_function.append(greyWolfSolver)
            # Set the name of clark wirght
            algo_name.append("Grey Wolf Optimizer")
            # Set the algorithm param
            algo_kwargs.append({
                "iteration": int(request.form['WolfIteration']),
                "cvrp": cvrp_instance,
                "wolf_number": int(request.form['WolfNumber']),
                "topic": f"{SOLUTION_TOPIC}_{cvrp_id}",
                "max_second_run": int(request.form['RunTimeGWO'])
            })
            # Is there evolution in the solution
            instance_save[f'has_evolution_{cvrp_id}'].append(True)
        
        # Get the flask application
        flask_applaction = current_app._get_current_object()

        # Create the thread
        # It's a daemon thread, so it will run in background
        threaded_task = threading.Thread(
            target=algorithmTask,
            kwargs={
                "flask_applaction": flask_applaction,
                "cvrp_instance": cvrp_instance,
                "algorithm_list": algo_function,
                "algorithm_kargs": algo_kwargs,
                "algorithm_name": algo_name,
                "cvrp_id": cvrp_id, 
                "email": request.form['email']
            },
            daemon=True
        )

        # launch the thread  
        threaded_task.start()
        
        # return the index.html template
        return render_template('load.html', instance_id=cvrp_id)

def stream(cvrp_id):
    """
    Controller to get the message publish on the topic
    
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    
    .. note: Inspired by https://github.com/petronetto/flask-redis-realtime-chat/blob/master/app.py
    """
    return Response(event_stream(cvrp_id), mimetype="text/event-stream")
    
def result(cvrp_id: str):
    """
    Controller to display the result of the algorithms
    
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    """
    
    return render_template(
        "result.html", algo_name=instance_save[f'algorithm_name_{cvrp_id}'],
        solution_list=instance_save[f'algorithm_solution_{cvrp_id}'],
        time_list=instance_save[f'algorithm_time_{cvrp_id}'],
        total_time=sum(instance_save[f'algorithm_time_{cvrp_id}']), enumerate=enumerate,
        cost_line_chart=instance_save[f'algorithm_solution_cost_{cvrp_id}'],
        best_solution_algorithm=instance_save[f'algorithm_best_solution_cost_{cvrp_id}'],
        algorithm_iteration=instance_save[f'algorithm_iteration_{cvrp_id}'],
        best_overall_cost=instance_save[f'best_solution_cost_{cvrp_id}'],
        best_algorithm=instance_save[f'best_algorithm_{cvrp_id}'], round=round,
        number_vehicles=instance_save[f'minimum_vehicles_{cvrp_id}'], instance_id=cvrp_id,
        instance_graph=instance_save[f'graph_instance_{cvrp_id}'], 
        nb_customer=instance_save[f'nb_customer_{cvrp_id}'], 
        vehicule_capacity=instance_save[f'vehicule_capacity_{cvrp_id}'],
        customer_demand=instance_save[f'demand_{cvrp_id}'],
        multiple=instance_save[f'has_evolution_{cvrp_id}']
    )

def downloadFile(cvrp_id: str):
    """
    Controller that will return the file to download (the report)
    
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    """
    # Get the current flask application
    flask_applaction = current_app._get_current_object()
    # Set the file name
    pdf_name: str = cvrp_id + ".pdf"
    
    # Get the generated pdf
    path = os.path.join(flask_applaction.config["CLIENT_PDF"], pdf_name)
    
    # Create the pdf
    createPDF(
        algorithm_name=instance_save[f'best_algorithm_{cvrp_id}'],
        min_cost=instance_save[f'best_solution_cost_{cvrp_id}'], 
        solution=instance_save[f'best_solution_{cvrp_id}'],
        name=path
    )
    
    return send_file(path, as_attachment=True)

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
 
def event_stream(cvrp_id: str) -> str:
    """
    Function to get the message publish on a topic
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    
    :return: message publish into the wanted topic
    :rtype: byte string
    
    .. note: Inspired by https://github.com/petronetto/flask-redis-realtime-chat/blob/master/app.py
    """
    # Create a publisher subscriber patern using redis
    pubsub = redis_server.pubsub(ignore_subscribe_messages=True)
    # Subscribe to the topic where the cvrp_id is
    pubsub.subscribe(f"{SOLUTION_TOPIC}_{cvrp_id}")
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

def algorithmTask(
    flask_applaction: Flask, cvrp_instance: Cvrp,
    algorithm_list: List, algorithm_kargs: List[Dict], algorithm_name: List[str],
    cvrp_id: str, email: str
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
    :param cvrp_id: Instance id of the page
    :type cvrp_id: str
    """
       
    # Run the algorithm 
    algorithm_solution, cost_list, time_list = runAlgorithm(
        cvrp_instance=cvrp_instance, algorithm_list=algorithm_list,
        algorithm_kargs=algorithm_kargs, algorithm_name=algorithm_name,
        publish_topic=f"{SOLUTION_TOPIC}_{cvrp_id}"
    )
    
    # Tell to the user what is actually happening
    json_data = {
        "messages": "<b>INFO:</b> Generating the results... Please wait", "type": "info"
    }
    # Publish
    redis_server.publish(f"{SOLUTION_TOPIC}_{cvrp_id}", json.dumps(json_data))
    
    # Save the result
    instance_save[f'algorithm_name_{cvrp_id}'] = algorithm_name
    # Dictionnary to save solution linked to their solution
    solution_list: List = []
    # List to store the line graph
    solution_cost_list : List = []
    # List of numbers of iterations
    iteration_list: List[int] = []
    # dictionnary for all solution used
    for index in range(len(algorithm_name)):
        # If the solution has evolution
        if instance_save[f'has_evolution_{cvrp_id}'][index]:
            # Generate the html of the graph
            solution_representation: str = getHtmlSolutionEvolutionAnimationPlotly(
                solution_evolution=algorithm_solution[index], full_html=False, default_height="750px"
            )
            # Append the html in the list
            solution_list.append(solution_representation)
            # Generate the line chart
            cost_representation: str = getHtmlLineCostEvolution(
                cost_evolution=cost_list[index], full_html=False
            )
            # append the html of the line chart
            solution_cost_list.append(cost_representation)
            # Get the number of iteration
            iteration_number: int = len(cost_list[index])
            # append it to the list
            iteration_list.append(iteration_number)
        else:
            # Generate the html of the graph
            solution_representation: str = algorithm_solution[index][-1].getHtmlFigurePlotly(
                full_html=False, default_height="500px"
            )
            # Append the html in the list
            solution_list.append(solution_representation)
            # append the html of the line chart
            solution_cost_list.append(None)
            # append it to the list
            iteration_list.append(1)

    # Save the solution provided by the algorithm
    instance_save[f'algorithm_solution_{cvrp_id}'] = solution_list
    # Save the time took by each algorithm
    instance_save[f'algorithm_time_{cvrp_id}'] = time_list
    # Save the cost of solutions
    instance_save[f'algorithm_solution_cost_{cvrp_id}'] = solution_cost_list
    # Save the cost of solutions
    # Since it only upgrade the solution we are sure that the best solution is at the end
    instance_save[f'algorithm_best_solution_cost_{cvrp_id}'] = [cost[-1] for cost in cost_list]
    # Save th iteration number of algorithm
    instance_save[f'algorithm_iteration_{cvrp_id}'] = iteration_list
    # Find the overall min solution cost
    instance_save[f'best_solution_cost_{cvrp_id}'] = min(instance_save[f'algorithm_best_solution_cost_{cvrp_id}'])
    # Find which algorithm returned the best result
    index_best_solution = instance_save[f'algorithm_best_solution_cost_{cvrp_id}'].index(instance_save[f'best_solution_cost_{cvrp_id}'])
    # Best algorithm
    instance_save[f'best_algorithm_{cvrp_id}'] = algorithm_name[index_best_solution]
    # Best overall solution
    instance_save[f'best_solution_{cvrp_id}'] = algorithm_solution[index_best_solution][-1]
    # Minimum number of vehicles for the best solutions
    instance_save[f'minimum_vehicles_{cvrp_id}'] = len(algorithm_solution[index_best_solution][-1].route)
    # Instance graph
    instance_graph: str = cvrp_instance.getHtmlFigurePlotly(full_html=False)
    # Convert it to markup to have the displayed
    # if it is not made, the string of the html code will be displayed
    html_instance_graph = Markup(instance_graph)
    # Save the instance
    instance_save[f'graph_instance_{cvrp_id}'] = html_instance_graph
    # Save the number of customer in the instance
    instance_save[f'nb_customer_{cvrp_id}'] = cvrp_instance.nb_customer
    # Save the vehicule capacity
    instance_save[f'vehicule_capacity_{cvrp_id}'] = cvrp_instance.vehicule_capacity
    # Save the vehicule capacity
    instance_save[f'demand_{cvrp_id}'] = f"[{cvrp_instance.getMinDemand()}, {cvrp_instance.getMaxDemand()}]"
        
    # Tell to the javsscript that the algorithm as ended
    # If no subscribers receive the message
    while redis_server.publish(f"{SOLUTION_TOPIC}_{cvrp_id}", "END") != 1:
        # Wait 50ms and then resend the message
        # By doing that we are sure that every time the subscriber will receive the message
        # Because it may appear some case where python algorithm have finished
        # before the web page have finished to load. If that case arrived
        # the user will stay forever on the loading page
        time.sleep(0.05)
         
    # Send mail if requested
    if email is not None or email != "":
        # Send the notification mail
        with flask_applaction.test_request_context( '/result/'):
            # Build the url for the report
            url_link: str = f"http://{HOST}:{PORT}{url_for('result', cvrp_id=cvrp_id)}"
            # print(url_link)
            # Send the mail
            status_code: int = sendMailFinished(mail_receiver=email, mail_name=cvrp_id, link=url_link)

   
