from configparser import ConfigParser

import matplotlib.pyplot as plt
import pandas as pd

from datascience.interfaces import Experiment

"""
Can we classify the genre(s) of a movie based on the keywords of the movie?

What keywords are best associated with movies that do well?
"""

SQL_QUERY_KEYWORDS_GENRE = """
SELECT 
    genre, keyword, count(*) as count
FROM
    TitleGenre,
    Top5000MovieKeywords
WHERE
    Top5000MovieKeywords.movieId = TitleGenre.titleId
GROUP BY genre, keyword
"""

class ExperimentThree(Experiment):

    NROWS = 6
    NCOLS = 5

    def __init__(self, config: ConfigParser):
        super().__init__(config)
        self.figure, self.axis = plt.subplots(nrows=self.NROWS, ncols=self.NCOLS, figsize=(20,16))
        self.figure.canvas.set_window_title("Keyword Occurences in Genres")

    def top_10(self, genre):
        keywords = self.keyword_totals[genre]
        sorted_top = sorted(keywords.items(), key=lambda item: item[1], reverse=True)
        return sorted_top[:10]

    def get_class_probabilities(self, keyword):
        totals = []
        for genre in self.keyword_totals.keys():
            if keyword in self.keyword_totals[genre]:
                totals.append(self.keyword_totals[genre][keyword])
            else:
                totals.append(0)
        total = sum(totals)
        return_probabilities = {}
        for i, genre in zip(range(len(self.keyword_totals.keys())), self.keyword_totals.keys()):
            if total == 0:
                return_probabilities[genre] = 0
            else:
                return_probabilities[genre] = totals[i] / total
        return return_probabilities

    def plot_genre_keywords(self, top_10_count):
        row = 0
        col = 0
        for genre in self.keyword_totals.keys():
            action = top_10_count[genre]
            df = pd.DataFrame(action, columns=["keyword", "count"])
            df = df[::-1]
            ax = df.plot(yticks=df.index, kind="barh", ax=self.axis[row][col], title=genre, legend=False)
            ax.set_yticklabels(df.keyword)
            if col == self.NCOLS - 1:
                col = 0
                row = row + 1
            else:
                col = col + 1
        plt.tight_layout()
        plt.show()

    def run(self):
        print("Querying data...")
        results = self.query(SQL_QUERY_KEYWORDS_GENRE)

        print("Plotting data...")
        self.keyword_totals = {}
        for row in results:
            genre = row['genre']
            keyword = row['keyword']
            count = row['count']
            if genre not in self.keyword_totals:
                self.keyword_totals[genre] = {}
            self.keyword_totals[genre][keyword] = count

        top_10_list = {}
        for genre in self.keyword_totals.keys():
            top_10_list[genre] = self.top_10(genre)

        self.plot_genre_keywords(top_10_list)