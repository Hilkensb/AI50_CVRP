Installation
============

Python Version
--------------

Please note that this project is working with **python 3.8+**. If you have a lower
version you should upgrade your python to use this project.

Dependancies
------------

List of python dependancies
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You will find all the dependancies of the project in the following table (This table
does not include dependancies of dependancies):

+-------------------+----------+----------------------+
| Dependancy name   | Version  | Link to documentation|
+===================+==========+======================+
| matplotlib        | 3.4.3    | matplotlib_          |
+-------------------+----------+----------------------+
| more-itertools    | 8.10.0   | more-itertools_      |
+-------------------+----------+----------------------+
| networkx          | 2.6.3    | networkx_            |
+-------------------+----------+----------------------+
| numpy             | 1.21.2   | numpy_               |
+-------------------+----------+----------------------+
| panda             | 1.3.3    | panda_               |
+-------------------+----------+----------------------+
| requests          | 2.26.0   | requests_            |
+-------------------+----------+----------------------+
| sphinx            | 4.2.0    | sphinx_              |
+-------------------+----------+----------------------+

List of needed software
~~~~~~~~~~~~~~~~~~~~~~~

The project can be runned using any version of python_ higher than the 3.8 version
(tested for python version 3.8, 3.9 and 3.10).


In order to use the application you will also need redis_ (version for windows and linux
may be found in the redis folder).


Finally to run the multiagent system you will need sarl_ programming language. You should then
run the sarl maven projet in sarl folder to use the algorithm made in sarl.

Install dependancies
~~~~~~~~~~~~~~~~~~~~

To install all the dependancies, use the following command in the root directory of the prject:

.. code-block:: sh

    pip install -r requirements.txt

.. _matplotlib: http://https://matplotlib.org/
.. _more-itertools: https://more-itertools.readthedocs.io/en/stable/
.. _networkx: https://networkx.org/
.. _numpy: https://numpy.org/
.. _panda: https://pandas.pydata.org/
.. _requests: https://fr.python-requests.org/en/latest/
.. _sphinx: https://www.sphinx-doc.org/en/master/
.. _python: https://www.python.org/
.. _redis: https://redis.io/
.. _sarl: http://www.sarl.io/
