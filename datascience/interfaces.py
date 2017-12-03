import pymysql
from configparser import ConfigParser

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
        connection_info = self.config['Database']
        connection = pymysql.connect(
            host=connection_info['host'],
            user=connection_info['user'],
            password=connection_info['password'],
            db='imdb',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def query(self, query, args=None):
        with self.get_connection() as connection:
            connection.execute(query, args)
            return connection.fetchall()

    def query_one(self, query, args=None):
        with self.get_connection() as connection:
            connection.execute(query, args)
            return connection.fetchone()