""" Solr indexing and querying time tester
Scripts to test the Apache Solr library in terms of indexing and querying time. It call
the methods of the utils library

For this script to work, there should be a Solr instance up and running, listening
to requests in port 8984 and with a core called 'gutenberg' created.
"""
import pysolr

import os
import time
import json

import numpy as np

from utils import plot_results, save_results, perform_tests


class SolrTester:
    """
    This class is an interface for indexing and querying to the Solr instance
    given by the argument solr of the constructor.
    """
    def __init__(self, solr):
        self.solr = solr
        self.docs = []
        self.n_rows = 0

    def index(self, files):
        """
        Indexes the data into the solr instance given by attribute
        solr and returns indexing time
        """
        docs = []
        global N_CHARS

        # Reset the database to measure complete indexing time
        solr.delete(q='*:*', commit=True)

        for elem in files:
            with open(elem, 'r') as f:
                file_text = f.read()
            doc_id = int(elem.split('.')[0].split('/')[-1])
            self.docs.append({
                "id": doc_id,
                "text": file_text[:N_CHARS]
            })
        resp = self.solr.add(self.docs, commit=True)
        self.n_rows += len(files)
        return json.loads(resp)['responseHeader']['QTime'] / 1000

    def query(self, queries):
        """
        Queries the solr instance given by attribute solr and return
        the time spent to make the query
        """
        times = []
        for q in queries:
            # print("Starting " + q)
            t_start = time.time()
            self.solr.search("text:" + q, rows=self.n_rows)
            times.append(time.time()-t_start)
        return {"times_query": np.mean(times)}


N_DOCS = 10000
N_CHARS = 100000

solr = pysolr.Solr("http://127.0.0.1:8984/solr/gutenberg")

if json.loads(solr.ping())["status"] != "OK":
    raise RuntimeError("Solr server is not up")

# Reset the database
solr.delete(q='*:*', commit=True)

solr_tester = SolrTester(solr)

results = perform_tests(solr_tester, N_DOCS)

save_results(results, "results_solr")

plot_results(results, savefig="results_solr", show=False)

