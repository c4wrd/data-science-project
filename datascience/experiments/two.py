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

    def run(self):
        # query the results from the database
        results = self.query(SQL_QUERY)
        print("Querying data")

        # construct an instance of a regressor model
        regressor = MLPRegressor(hidden_layer_sizes=(100,100))

        x_true = [[item['budget'], item['likes']] for item in results]
        y_true = [item['revenue'] for item in results]

        print("Constructing MLP Model")
        # fit the model
        regressor.fit(x_true, y_true)
        print("Finished training MLP Model")

        # create predictions from the model and
        # output the results of the model as a measure
        # of the MSE and the variance score
        y_predicted = regressor.predict(x_true)
        print("Mean Squared Error: %.4f" % mean_squared_error(y_true, y_predicted))
        print("r2 score: %.4f" % r2_score(y_true, y_predicted))