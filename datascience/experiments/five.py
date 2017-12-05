from datascience.interfaces import Experiment
import sklearn.decomposition as dec
import matplotlib.pyplot as plot
from sklearn.preprocessing import normalize as norm
from sklearn.cluster import DBSCAN as DB

"""
Is there a way to distinguishably cluster movies between those tht grossed more than their budget and those that did not?
"""

SQL_QUERY_SUCCESSES = """
SELECT *
FROM Top5000Movie
WHERE Top5000Movie.grossRevenue > Top5000Movie.budget
"""

SQL_QUERY_FLOPS = """
SELECT *
FROM Top5000Movie
WHERE Top5000Movie.grossRevenue <= Top5000Movie.budget
"""

class ExperimentFive(Experiment):

    # queries the database and extracts the feature names and values from the query
    # returns a 2D array in the shape [[keys...],[values...]]
    # in this case the values will be all movies that "flopped" (budget >= grossRevenue)
    def get_flops(self):
        results = self.query(SQL_QUERY_FLOPS)
        keys = list(results[0].keys())[2:]
        values = [list(dict.values())[2:] for dict in results if None not in list(dict.values())[2:]]
        values = [val for val in values if val.remove(val[2]) is None] # remove budgets
        #values = [val for val in values if val.remove(val[1]) is None] # remove grossReveneus
        keys.remove(keys[2]) # remove budget
        #keys.remove(keys[1]) # remove grossRevenue
        return [keys,values]

    # queries the database and extracts the feature names and values from the query
    # returns a 2D array in the shape [[keys...],[values...]]
    # in this case the values will be all movies were a "success" (budget < grossRevenue)
    def get_successes(self):
        results = self.query(SQL_QUERY_SUCCESSES)
        keys = list(results[0].keys())[2:]
        values = [list(dict.values())[2:] for dict in results if None not in list(dict.values())[2:]]
        values = [val for val in values if val.remove(val[2]) is None] # remove revenue from classification
        keys.remove(keys[2]) # remove revenue from classification
        return [keys,values]

    #
    def run_DBSCAN(self, data):
        print("Running DBSCAN...")
        print("creating DBSCAN object...")
        scan = DB(eps=0.0008,
                  min_samples=50,
                  metric='euclidean',
                  metric_params=None,
                  algorithm='auto',
                  leaf_size=30,
                  p=None,
                  n_jobs=1)
        print("finding clusters...")
        scan.fit_predict(data)
        indexes = scan.core_sample_indices_
        labels = list(scan.labels_)
        print("found %s clusters...\ndisplaying clusters..." % (len(set(labels))-1))

        cmap = plot.cm.get_cmap('hsv',len(set(labels)))
        for label in set(labels):                           # looks at all unique classes found by DBSCAN
            points = [[],[]]                                # and plots each classes corresponding PCA values
            if label != -1:                                 # while also ignoring all classes of -1
                for index in indexes:                       # due to -1 being the noise of the
                    if labels[index] == label:              # DBSCAN algorithm
                        points[0].append(data[index][0])
                        points[1].append(data[index][1])
                figDB = plot.figure('DBSCAN')
                plot.scatter(points[0],points[1],c=cmap(label), s=1)

    def run(self):
        flops = self.get_flops()
        flops[1] = norm(flops[1]).tolist()
        successes = self.get_successes()
        successes[1] = norm(successes[1]).tolist()

        # PCA AND PLOTS
        print("Converting %s dimensions to 2 dimensions..." % (len(flops[0])))
        pca = dec.PCA(n_components=2)
        new_flops = pca.fit_transform(flops[1])
        print("Conversion complete...")
        print("Explained Variance Flops: %s" % (sum(pca.explained_variance_ratio_)))
        new_successes = pca.fit_transform(successes[1])
        print("Explained Variance Successes: %s" % (sum(pca.explained_variance_ratio_)))
        nf = [[x[0] for x in new_flops],[y[1] for y in new_flops]]                          # retrieving PCA x,y for flops
        ns = [[x[0] for x in new_successes],[y[1] for y in new_successes]]                  # retrieving PCA x,y for succeesses
        fig1 = plot.figure('PCA DATA')
        plot.scatter(nf[0],nf[1], color='r', s=1)
        plot.scatter(ns[0],ns[1],color='b', s=1)

        combined_data = pca.fit_transform(flops[1]+successes[1])
        print("Combined Explained Variance: %s" % (sum(pca.explained_variance_ratio_)))
        c_data = new_flops.tolist()+new_successes.tolist()                                  # combining PCA data to plot clusters later
        self.run_DBSCAN(c_data)

        plot.show()
