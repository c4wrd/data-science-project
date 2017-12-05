from datascience.interfaces import Experiment
import scipy.stats as stats
import numpy as np
"""
Is there a more significant correlation between a movies metascore and revenue or IMDB score and revenue?
"""

SQL_QUERY1 = """
    SELECT
        imdbScore as score,grossRevenue as revenue
    FROM
        Title
        JOIN
        Top5000Movie
        ON Title.titleId = Top5000Movie.movieId
    """

SQL_QUERY2 = """
    SELECT
        metascore as score,grossRevenue as revenue
    FROM
        TitleMetascore
        JOIN
        Top5000Movie
        ON TitleMetascore.titleId = Top5000Movie.movieId
    """

SQL_QUERY3 = """
SELECT
    A.imdbScore as imdb, B.metascore as meta, A.grossRevenue as revenue
FROM
(
		(SELECT
			imdbScore, grossRevenue, titleId
		FROM
			Title
		JOIN Top5000Movie
		ON Title.titleId = Top5000Movie.movieId
		) as A

JOIN

		(SELECT
			metascore, grossRevenue, titleId
		FROM
			TitleMetascore
		JOIN Top5000Movie
		ON TitleMetascore.titleId = Top5000Movie.movieId
        ) as B

ON A.titleId = B.titleId
)
WHERE A.grossRevenue IS NOT null
"""

class ExperimentFour(Experiment):

    # returns a 2D array containing [[score...],[grossRevenue...]]
    # if SQL_QUERY1 is passed in then score is imdb_scores
    # if SQL_QUERY2 is passed in then score is metascore
    def execute_query_pearson(self,q):
        result = self.query(q)
        xvals,yvals = [],[]
        for item in result:
            if item['revenue'] is not None:
                xvals.append(float(item['score']))
                yvals.append(float(item['revenue']))
        return [xvals,yvals]

    # returns a 2D array containing [[imdb_scores],[metascores],[revenues]]
    # SQL_QUERY3 should be passed in as the parameter.
    def execute_query_t_test(self,q = SQL_QUERY2):
        result = self.query(q)
        xvals,yvals,rev = [],[],[]
        for item in result:
            xvals.append(float(item['imdb']))
            yvals.append(int(item['meta']/10))      # scaling metascore to 1-10 like imdb
            rev.append(float(item['revenue']))
        return [xvals,yvals,rev]

    # returns the imdb peasron correlation, q1 in format [[x],[y]]
    def imdb_correlation(self,q1):
        return stats.pearsonr(q1[0],q1[1])

    # returns the metascore peasron correlation, q2in the format [[x],[y]]
    def metascore_correlation(self,q2):
        return stats.pearsonr(q2[0],q2[1])

    # selects 100 samples of imdb_scores and revenues and
    # selects 100 samples of metascores and revenues
    # returns the two sample t-test statistics of the two samples
    def t_test(self,q1,q2):
         a = np.random.choice(q1, size=100, replace=False)
         b = np.random.choice(q2, size=100, replace=False)
         return stats.ttest_ind(a,b, equal_var=False)

    def run(self):
        q1_results = self.execute_query_pearson(SQL_QUERY1)
        q2_results = self.execute_query_pearson(SQL_QUERY2)
        q3_results = self.execute_query_t_test(SQL_QUERY3)
        print("IMDB Correlation,P-val: " , self.imdb_correlation(q1_results))
        print("Meta Correlation,P-val: " , self.metascore_correlation(q2_results))
        print("T-Test: " , self.t_test(q3_results[0], q3_results[1]))
