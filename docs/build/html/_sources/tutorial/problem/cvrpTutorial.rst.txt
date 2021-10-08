How to create and use CVRP
==========================

In this small tutorial we will use the instance P-n16-k8_. First we will create a cvrp instance from the data file P-n16-k8. Two ways to do it:

1) Create the instance then read the data file

.. code-block:: python
   :caption: Creation and reading data file

   import problem.cvrp.instance as cvrp
   cvrp_instance = cvrp.Cvrp()
   cvrp_instance.readInstanceVrpWeb(
        url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp"
   )
   
2) Read the data file on the creation of the instance

.. code-block:: python
   :caption: Reading data file while creating the instance

   import problem.cvrp.instance as cvrp
   cvrp_instance = cvrp.Cvrp(
        file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp",
        file_type="web"
   )


Now that we have created the cvrp instance, let see what we can do with it. First, we can ensure that
the instance file has been red correctly. For this purpose, let's take a look at the distance matrix.
We will round it to the nearest integer to make the lecture of it a bit easier.

.. code-block:: python
   :caption: Getting the distance matrix

   M = cvrp_instance.distanceMatrix(round_distance=True, precision=0)

We will get the following matrix:

.. math::

        M = \begin{bmatrix}
                -1 & 14 & 21 & 33 & 22 & 23 & 12 & 22 & 32 & 32 & 21 & 28 & 30 & 29 & 31 & 30 \\
                14 & -1 & 12 & 19 & 12 & 24 & 12 & 19 & 21 & 27 &  7 & 19 & 16 & 21 & 33 & 17 \\
                21 & 12 & -1 & 15 & 22 & 16 & 11 &  9 & 12 & 15 & 11 & 29 & 19 &  9 & 24 & 23 \\
                33 & 19 & 15 & -1 & 21 & 31 & 25 & 23 &  8 & 24 & 12 & 25 &  9 & 17 & 37 & 16 \\
                22 & 12 & 22 & 21 & -1 & 36 & 24 & 30 & 26 & 37 & 12 &  7 & 13 & 30 & 44 &  9 \\
                23 & 24 & 16 & 31 & 36 & -1 & 13 &  8 & 25 & 13 & 26 & 43 & 35 & 16 &  8 & 39 \\
                12 & 12 & 11 & 25 & 24 & 13 & -1 & 10 & 23 & 20 & 16 & 31 & 26 & 17 & 21 & 28 \\
                22 & 19 &  9 & 23 & 30 &  8 & 10 & -1 & 18 & 10 & 19 & 37 & 28 &  9 & 15 & 32 \\
                32 & 21 & 12 &  8 & 26 & 25 & 23 & 18 & -1 & 17 & 15 & 32 & 17 & 10 & 31 & 23 \\
                32 & 27 & 15 & 24 & 37 & 13 & 20 & 10 & 17 & -1 & 25 & 44 & 31 &  7 & 16 & 37 \\
                21 &  7 & 11 & 12 & 12 & 26 & 16 & 19 & 15 & 25 & -1 & 19 & 10 & 18 & 34 & 13 \\
                28 & 19 & 29 & 25 &  7 & 43 & 31 & 37 & 32 & 44 & 19 & -1 & 16 & 37 & 51 & 10 \\
                30 & 16 & 19 &  9 & 13 & 35 & 26 & 28 & 17 & 31 & 10 & 16 & -1 & 24 & 43 &  6 \\
                29 & 21 &  9 & 17 & 30 & 16 & 17 &  9 & 10 &  7 & 18 & 37 & 24 & -1 & 21 & 30 \\
                31 & 33 & 24 & 37 & 44 &  8 & 21 & 15 & 31 & 16 & 34 & 51 & 43 & 21 & -1 & 47 \\
                30 & 17 & 23 & 16 &  9 & 39 & 28 & 32 & 23 & 37 & 13 & 10 &  6 & 30 & 47 & -1
            \end{bmatrix}

The above matrix represent the distance (round to the nearest integer) of the distance between each node.
The diagonal of the matrix is filled with -1 values because it's impossible to go from a node to the same node.
For exemple let's try to know the distance between the depot (node 1) and customer 1 (node 2).
To find out the distance between those 2 nodes we go at first row (distance of node 1) and second column (distance of node 2).
We see 14, it means that the distance between depot and customer 1 is 14.

.. note:: Since it's a cvrp instance, the matrix is symetric. This means that M(1,2) = M(2,1)

Now let's display a plot of the instance. For this purpose we will use the showFigure method.

.. code-block:: python
   :caption: Reading data file while creating the instance

   cvrp_instance.showFigure()

We will get the following plot generated with matplotlib and networkx.

.. figure:: /_static/tutorial/problem/cvrpInstanceFigure.png

.. _P-n16-k8: http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp
