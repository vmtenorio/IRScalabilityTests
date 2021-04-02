# Information Retrieval Scalability Tests

Repository that contains the necesary scripts to perform information retrieval over 2 different libraries: Apache Solr and Terrier. To do so, it will download a set of books from project Gutenberg webpage, and it will divide it in subsets, perform the indexing and using a set of queries to measure query time.

It contains the following scripts:
* `download_books.py`: uses `gutenberg` Python package to download books from this project and store them on disk.
* `utils.py`: contains the necesary methods to perform the tests to the libraries and store and plot the results.
* `solr_tests.py`: the main program, with the wrapper that can index and query the Solr instance and the logic to perform the necesary tests. It uses [pysolr library](https://github.com/django-haystack/pysolr).
* `terrier_tests.py`: same as `solr_tests`, but using Terrier, more precisely, [pyterrier library](https://github.com/terrier-org/pyterrier).
* `plot_results.py`: receives as argument the library that we want to use to plot the results, loads the dictionary and plots the results.
