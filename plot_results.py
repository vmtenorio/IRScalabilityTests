from utils import load_results, plot_results
import sys

if len(sys.argv) < 2 or sys.argv[1] not in ["solr", "terrier"]:
    raise ValueError("Need to enter one argument, either 'solr' or 'terrier', to plot the results")

results = load_results("results_" + sys.argv[1])

plot_results(results, legend=sys.argv[1]=="terrier", savefig="results_" + sys.argv[1], show=True)
