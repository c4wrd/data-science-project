from datascience.interfaces import Experiment
import sklearn.decomposition as dec
import matplotlib.pyplot as plot
from sklearn.preprocessing import normalize as norm
from sklearn.cluster import DBSCAN as DB

"""
Is there a correlation between the lifespan in years for a TV show, and the average rating of the TV show?
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

    def get_flops(self):
        results = self.query(SQL_QUERY_FLOPS)
        keys = list(results[0].keys())[2:]
        values = [list(dict.values())[2:] for dict in results if None not in list(dict.values())[2:]]
        values = [val for val in values if val.remove(val[2]) is None] # remove budgets
        #values = [val for val in values if val.remove(val[1]) is None] # remove grossReveneus
        keys.remove(keys[2]) # remove budget
        #keys.remove(keys[1]) # remove grossRevenue
        return [keys,values]

    def get_successes(self):
        results = self.query(SQL_QUERY_SUCCESSES)
        keys = list(results[0].keys())[2:]
        values = [list(dict.values())[2:] for dict in results if None not in list(dict.values())[2:]]
        values = [val for val in values if val.remove(val[2]) is None] # remove budgets
        #values = [val for val in values if val.remove(val[1]) is None] # remove grossReveneus
        keys.remove(keys[2]) # remove budget
        #keys.remove(keys[1]) # remove grossRevenue
        return [keys,values]

    def run_DBSCAN(self, data):
        print("Running DBSCAN...")
        print("creating DBSCAN object...")
        scan = DB(eps=0.0008, #.0005 for 2 clear clusters
                  min_samples=50, # 30 for 2 clear clusters
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
        for label in set(labels):
            points = [[],[]]
            if label != -1:
                for index in indexes:
                    if labels[index] == label:
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
        print("Explained Variance: %s" % (sum(pca.explained_variance_ratio_)))
        new_successes = pca.fit_transform(successes[1])
        nf = [[x[0] for x in new_flops],[y[1] for y in new_flops]]
        ns = [[x[0] for x in new_successes],[y[1] for y in new_successes]]
        fig1 = plot.figure('PCA DATA')
        plot.scatter(nf[0],nf[1], color='r', s=1)
        plot.scatter(ns[0],ns[1],color='b', s=1)

        c_data = new_flops.tolist()+new_successes.tolist()
        self.run_DBSCAN(c_data)

        plot.show()
