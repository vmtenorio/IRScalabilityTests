import pyterrier as pt

import os
import time
import json

import numpy as np

from utils import plot_results, save_results, perform_tests


class TerrierTester:
    def __init__(self, index_path):
        self.index_path = index_path
        self.n_rows = 0
        self.wmodels = ["TF_IDF", "BM25", "PL2"]
        self.documents = []

    def init_indexer(self):
        # Clear the index directory to prevent indexing errors
        if len(os.listdir(self.index_path)) > 0:
            for f in os.listdir(self.index_path):
                os.remove(self.index_path + f)

        self.indexer = pt.FilesIndexer(index_path, blocks=True)
        self.indexer.verbose = True
        self.indexer.meta = {'docno': 20, 'filename': 512}
        self.indexer.meta_reverse = ['docno']

    def index(self, files):
        """
        Indexes the data into the solr instance given by global
        variable solr and returns indexing time
        """
        self.init_indexer()
        self.documents.extend(files)
        t_start = time.time()
        self.indexref = self.indexer.index(self.documents)
        t_index = time.time()-t_start
        self.n_rows = len(self.documents)
        return t_index

    def query(self, queries):
        """
        Queries the solr instance given by variable solr and return
        the time spent to make the query
        """
        times = {k:[] for k in self.wmodels}
        for q in queries:
            # print("Starting " + q)
            for wm in self.wmodels:
                t_start = time.time()
                q_result = pt.BatchRetrieve(self.indexref, metadata=["docno", "filename"], wmodel=wm).search(q)
                times[wm].append(time.time()-t_start)

        return {k:np.mean(v) for k,v in times.items()}

N_DOCS = 10000

os.environ["JAVA_HOME"]="/usr/lib/jvm/java-11-openjdk-amd64/"
os.environ["JVM_PATH"]="./lib/server/libjvm.so"

pt.init(mem="10240") # Using 10GB of mem

index_path = os.path.expanduser("~/terrier_index/")

terrier_tester = TerrierTester(index_path)

results = perform_tests(terrier_tester, N_DOCS)

save_results(results, "results_terrier")

plot_results(results, legend=True, savefig="results_terrier", show=False)
