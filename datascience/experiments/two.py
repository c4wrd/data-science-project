from configparser import ConfigParser

from datascience.interfaces import Experiment
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

"""
Can the revenue produced by a movie be predicted the the movie budget, facebook likes and rating?
"""

SQL_QUERY = """
SELECT budget, numberFacebookLikes as likes, grossRevenue as revenue FROM Top5000Movie
	WHERE 
		budget IS NOT NULL
		AND
        numberFacebookLikes IS NOT NULL
        AND
        grossRevenue IS NOT NULL
"""

class ExperimentTwo(Experiment):

    def __init__(self, config: ConfigParser):
        super().__init__(config)
        self.regressor = MLPRegressor(hidden_layer_sizes=(100,100))

    def query_data(self):
        print("Querying data")
        results = self.query(SQL_QUERY)

        self.x_true = [[item['budget'], item['likes']] for item in results]
        self.y_true = [item['revenue'] for item in results]

    def fit_model(self):
        print("Constructing MLP Model")
        # fit the model
        self.regressor.fit(self.x_true, self.y_true)
        print("Finished training MLP Model")

    def report_model_stats(self):
        # create predictions from the model and
        # output the results of the model as a measure
        # of the MSE and the variance score
        y_predicted = self.regressor.predict(self.x_true)
        print("Mean Squared Error: %.4f" % mean_squared_error(self.y_true, y_predicted))
        print("r2 score: %.4f" % r2_score(self.y_true, y_predicted))

    def run(self):
        self.query_data()
        self.fit_model()
        self.report_model_stats()