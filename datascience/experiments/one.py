from datascience.interfaces import Experiment

"""
How has the popularity and revenue of specific genres changed over time?
"""

SQL_QUERY_GENRE_RATINGS = """
SELECT 
    AVG(averageRating) AS rating, debutYear AS year
FROM
    Title
        JOIN
    TitleGenre ON Title.titleId = TitleGenre.titleId
WHERE
    averageRating IS NOT NULL
        AND debutYear IS NOT NULL
        AND genre = %s
GROUP BY debutYear;
"""

class ExperimentOne(Experiment):

    def run(self):
        pass