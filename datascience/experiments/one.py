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

    #genres = ["sci-fi", "romance", "western", "horror", "animation", "war"]
    genres = ["sci-fi", "horror", "war"]

    def popularity_over_time(self, genre):
        items = self.query(SQL_QUERY_GENRE_TOTAL_MOVIES, (genre,))
        results = {}
        for item in items:
            results[item['year']] = item['count']
        return results

    def run(self):
        df = pd.DataFrame()
        for genre in self.genres:
            ratings = self.popularity_over_time(genre)
            series = pd.Series(ratings, name=genre)
            series = series.ewm(span=5).mean() # moving average smoothing
            df[genre] = series

        # show the plot
        plot = df.plot(title="Genre Popularity over Time")
