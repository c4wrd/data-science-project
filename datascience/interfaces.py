import pymysql
from configparser import ConfigParser
from matplotlib.pyplot import show

class Experiment:
    """
    A class that will be subclassed by each individual experiment.
    Each experiment must implement the 'run' method below.
    """
    def __init__(self, config: ConfigParser):
        self.config = config

    def run(self):
        raise NotImplementedError()

    def get_connection(self):
        """
        Retrieves the MySQL connection
        :return: mysql connection object
        """
        connection_info = self.config['Database']
        connection = pymysql.connect(
            host=connection_info['host'],
            user=connection_info['username'],
            password=connection_info['password'],
            db='imdb',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def query(self, query, args=None):
        """
        Performs a query against the dataset, and
        returns a list of dictionary objects where the
        key in each dictionary object is the respective column name,
        and the value is the value of the respective column
        :param query: The query to run
        :param args: Any arguments that should be part of the query
        :return: [list]
        """
        with self.get_connection() as connection:
            connection.execute(query, args)
            return connection.fetchall()

    def query_one(self, query, args=None):
        """
        Performs a query against the dataset and returns
        a single result
        :param query: The query to run
        :param args: Any arguments for the query
        :return: dict
        """
        with self.get_connection() as connection:
            connection.execute(query, args)
            return connection.fetchone()

    def show(self):
        """
        Shows any pending matplotlib plots on the screen
        """
        show()