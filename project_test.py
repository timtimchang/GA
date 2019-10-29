from pyclustering.cluster.ga import genetic_algorithm, ga_observer
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import SIMPLE_SAMPLES
# Read input data for clustering
sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
print("SIMPLE_SAMPLES.SAMPLE_SIMPLE4)",SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
print("sample",sample)

# Create instance of observer that will collect all information:
observer_instance = ga_observer(True, True, True)
# Create genetic algorithm for clustering
ga_instance = genetic_algorithm(data=sample,
                                count_clusters=4,
                                chromosome_count=100,
                                population_count=200,
                                count_mutation_gens=1)
# Start processing
ga_instance.process()
# Obtain results
clusters = ga_instance.get_clusters()
# Print cluster to console
print("Amount of clusters: '%d'. Clusters: '%s'" % (len(clusters), clusters))
