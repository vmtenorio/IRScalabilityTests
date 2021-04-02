""" Utils for testing IR libraries
This script includes both constants and methods used to test the indexing and 
querying using IR libraries.

This file can be imported as a module and contains the following
functions:

    * get_partitions - returns the list of partitions. To be called internally
    * perform_tests - perform the indexing and querying tests
    * save_results - save the results dict in a json file
    * load_results - loads the results dict from a json file
    * plot_results - plots the results in a matplotlib figure
"""
import os
import json
import random
import matplotlib.pyplot as plt


# Set of queries to send to the IR systems
QUERIES = [
    "lion",
    "Spain",
    "whale",
    "part",
    "the",
    "bird",
    "nightmare",
    "country",
    "mountain",
    "Alice",
    "master",
    "with",
    "main",
    "event",
    "red",
    # Queries en español por los libros en español encontrados
    "perro",
    "casa",
    "caballo",
    "molinos",
    "ascendencia"
]

DATA_PATH = os.path.expanduser("~/gutenberg_data/")
N_PARTITIONS = 20
SEED = 42

def get_partitions(n_docs=0):
    """
    Reads the path given by DATA_PATH and returns a list that contains the partitions.
    Each partition contains the path of each element in the data folder. 
    The elements of each partition are random.

    Parameters
    ----------
    n_docs : int
        The number of docs to be used for the tests

    Returns
    -------
    list of lists
        a list of the partitions, where each partition is a list of paths to files
    """
    global DATA_PATH, N_PARTITIONS, SEED
    elements = os.listdir(DATA_PATH)
    elem_path = [DATA_PATH + elem for elem in elements if os.path.isfile(DATA_PATH + elem)]
    random.seed(SEED)
    random.shuffle(elem_path)
    if n_docs != 0:
        elem_path = elem_path[:n_docs]
    n_elements = len(elem_path)
    n_elem_part = n_elements // N_PARTITIONS
    partitions = [elem_path[n_elem_part*i:(i+1)*n_elem_part] for i in range(N_PARTITIONS)]
    return partitions

def perform_tests(indexer, n_docs=0):
    """
    This method is used to perform the indexing and querying tests to each of
    the libraries used. It receives as argument an indexer, that is, an object
    with access to the methods 'index' and 'query', who make the underlying
    calculations and return indexing and querying time, respectively, so it is
    agnostic with respect to the underlying library that the indexer uses.

    It returns a dictionary with the information of the times, as well as the
    number of documents in each step (given by the attribute 'n_rows' of the
    indexer, that should be available as well).

    Parameters
    ----------
    indexer : custom
        The object with the index and query methods to be used.

    n_docs : int
        The number of docs to be used for the tests

    Returns
    -------
    dict
        a dictionary with the results of the tests
    """
    partitions = get_partitions(n_docs)

    results = {
        "index_times": [],
        "n_docs": []
    }

    for i, part in enumerate(partitions):
        print("Starting partition: {} - INDEXING - ".format(str(i+1)), flush=True, end="")
        results["index_times"].append(indexer.index(part))
        print("QUERYING - ", flush=True, end="")
        queries_result = indexer.query(QUERIES)
        for k, v in queries_result.items():
            if k in results:
                results[k].append(v)
            else:
                results[k] = [v]
        print("DONE - N Docs: {}".format(indexer.n_rows), flush=True)
        results["n_docs"].append(indexer.n_rows)

    return results


def save_results(results, path):
    """
    Save results dictionary coming as argument as a json file in the path specified

    Parameters
    ----------
    results : dict
        The dict containing the results to be saved

    path : str
        The path where to save the results file
    """
    with open("results/" + path + ".json", 'w') as f:
        json.dump(results, f, indent=4)

def load_results(path):
    """
    Load a results dictionary from a json file in the path specified

    Parameters
    ----------
    path : str
        The path from where to load the results file
    """
    with open("results/" + path + ".json", 'r') as f:
        results = json.load(f)
    return results

def plot_results(results, legend=True, savefig=None, show=False):
    """
    Plot the index times and all the query times in a matplotlib figure with 2 subplots

    Parameters
    ----------
    results : dict
        The results dict, with at least the keys 'n_docs' and 'index_times'

    legend : bool, optional
        Whether or not to plot the legend in the figure

    savefig : str, optional
        if set, it has to contain the path to store the figure

    show : bool, optional
        if true, it will show the plot
    """
    f, ax = plt.subplots(2, figsize=(8,10))

    ax[0].plot(results['n_docs'], results['index_times'])
    ax[0].set_title("Indexing times", fontsize=20)
    ax[0].set_ylabel("Time (s)")

    for i, k in enumerate(results.keys()):
        if k == 'n_docs' or k == 'index_times':
            continue
        ax[1].plot(results['n_docs'], results[k], label=k)

    if legend:
        ax[1].legend()

    ax[1].set_title("Query time", fontsize=20)
    ax[1].set_ylabel("Time (s)")
    ax[1].set_xlabel("Number of documents", fontsize=14)

    if savefig:
        plt.savefig(savefig, bbox_inches='tight')
    if show:
        plt.show()

