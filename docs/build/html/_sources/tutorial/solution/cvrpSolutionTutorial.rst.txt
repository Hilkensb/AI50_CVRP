How to create a Solution for CVRP
=================================

In this small tutorial we will use the instance P-n16-k8_ that we created in the previous page and build it's solution Sol-P-n16-k8_. First we will create a cvrp solution from the Cvrp instance object of P-n16-k8:

.. code-block:: python
   :caption: Creation of the solution

   import problem.cvrp.instance as cvrp
   import solution.cvrp.solution as sol
   # We assume that the cvrp instance has been created has showed
   # in the previous page tutorial
   sol_cvrp = sol.SolutionCvrp(cvrp_instance)
   
Now that we have the solution object linked to the cvrp instance, we need to give it the route to build the solution. We can either do it by hand (by building and giving a list of route) or more simply by giving it a solution file (either on local or on web). 

If the solution file is on internet we can get the solution with the following:

.. code-block:: python
   :caption: Read a solution

   sol_cvrp.readSolutionWeb(url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol")

Else if you have the solution file on local you can use the readSolution method. You will need to precise the path of the file you want to read.
Now let's try to display the solution on a matplotlib window.

.. note:: We will use the default parameters but many argument can change how the plot looks like.

.. code-block:: python
   :caption: Plotting the solution

   sol_cvrp.showFigure()

We will get the following plot generated with matplotlib and networkx.

.. figure:: /_static/tutorial/solution/cvrpSolutionFigure.png

Finally there's many more method that can be use for specific purpose. You can create other solutions from a solution object, get the total cost of the solution (sum of all routes cost of the solution), check that the solution is verifying all constraints, ...

Please refer to the object details to see all of these methods and their arguments.

.. _P-n16-k8: http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp

.. _Sol-P-n16-k8: http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol
