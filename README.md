# AI50_CVRP

AI50 project to modelize **C**apacited **V**ehicle **R**outing **P**roblem (**CVRP**) and find solutions using Multi-Agents Systems, metaheuristics and Machine Learning.

## Requirements

This project requires a 3.8+ python version and multiple library to be runned. Before running it for the first time please ensure that you have every python library required by running the following command:

```shell
pip install requirements.txt
```

## Launching the web application

To launch the web application, run the main.py file. You can add one or more of the followings arguments:

| Argument               | Explanation                                   |
| ---------------------- | --------------------------------------------- |
| -h or --help           | Display the help message                      |
| -t or --unittest       | Run unit test before running the application  |
| -s or --show_evolution | Display the current solution on the load page |

The web application runned by default on http://localhost:8080/. To be runned the application needs [Redis](https://redis.io/ 'redis.io') server available (version for windows and linux are present in the redis folder).

## Implemented Algorithm

### Multi-Agents Systems (MAS)

The algorithm is based on the scientific article [Agents toward Vehicle Routing Problem](https://www.semanticscholar.org/paper/Agents-towards-vehicle-routing-problems-Vokr%C3%ADnek-Komenda/1d486f85f0810331c8feb203ac126a7c192d00e1 'SemanticScholar page'). It is written in [sarl](http://www.sarl.io/ 'sarl programming language') and bridged to python using py4J library.

### Metaheuristcis

Two metaheuristics have been implemented:

- Tabu search
- Genetic Algorithm

Both metaheuristics start from a solution provided by the Clark & Wright saving algorithm and try to improve it. Here's a small example of the result provided by the tabu search algorithm.

![](./misc/tabu_search.gif)

