import pandas as pd
from datascience.interfaces import Experiment

"""
How has the popularity and revenue of specific genres changed over time?
"""

SQL_QUERY_GENRE_TOTAL_MOVIES = """
SELECT 
    Count(*) as count, debutYear AS year
FROM
    Title
        JOIN
    TitleGenre ON Title.titleId = TitleGenre.titleId
WHERE
    averageRating IS NOT NULL
        AND debutYear IS NOT NULL
        AND genre = %s
        AND debutYear < 2018
GROUP BY debutYear
"""

class ExperimentOne(Experiment):

    genres = ["sci-fi", "romance", "western", "horror", "animation", "war"]

    def popularity_over_time(self, genre):
        """
        Computes the popularity of a specific genre (as a measure
        of the number of titles produced in a year with a specific genre)
        :param genre: The genre to query
        """
        items = self.query(SQL_QUERY_GENRE_TOTAL_MOVIES, (genre,))
        # format the results into a dictionary that is easier to work
        # with
        results = {}
        for item in items:
            results[item['year']] = item['count']
        return results

    def run(self):
        # create a dataframe to display the results
        df = pd.DataFrame()
        for genre in self.genres: # for each genre, add the series to the dataframe
            print("Querying popularity of '%s'" % genre)
            ratings = self.popularity_over_time(genre)
            series = pd.Series(ratings, name=genre)
            series = series.ewm(span=5).mean() # smooth the moving average over time
            df[genre] = series

        # show the plot
        plot = df.plot(title="Genre Popularity over Time")
        self.show()