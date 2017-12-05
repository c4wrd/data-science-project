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
    NCOLS = 4

    def __init__(self, config: ConfigParser):
        super().__init__(config)
        self.figure, self.axis = plt.subplots(nrows=self.NROWS, ncols=self.NCOLS, figsize=(16,20))
        self.figure.canvas.set_window_title("Keyword Occurences in Genres")

    def top_10(self, genre):
        keywords = self.keyword_totals[genre]
        sorted_top = sorted(keywords.items(), key=lambda item: item[1], reverse=True)
        return sorted_top[:7]

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
        """
        Plots the top 10 keywords of all of the genres
        into a single plot with (NROWSxNCOLS) dimensions
        """
        row = 0
        col = 0
        for genre in top_10_count.keys():
            genre_counts = top_10_count[genre]
            # create a dataframe with the genre-specific counts
            df = pd.DataFrame(genre_counts, columns=["keyword", "count"])
            # invert the dataframe to display the keywords on the y-axis
            df = df[::-1]
            ax = df.plot(yticks=df.index, kind="barh", ax=self.axis[row][col], title=genre, legend=False)
            ax.set_yticklabels(df.keyword) # set the y-axis labels to the respective keyword the bar represents
            if col == self.NCOLS - 1: # if we are in the last column, move to the next row in the plot
                col = 0
                row = row + 1
            else: # increment the column number in the plot
                col = col + 1
        plt.tight_layout()  # creates a better layout for the plot
        plt.show()

    def predict(self, keyword):
        probabilities = self.get_class_probabilities(keyword)
        return max(probabilities.items(), key=lambda k: k[1])[0]

    def classification_report(self):

        x_train = []
        y_true = []
        y_pred = []

        for genre in self.keyword_totals.keys():
            for keyword in self.keyword_totals[genre]:
                count = self.keyword_totals[genre][keyword]
                expected_class = genre
                predicted_class = self.predict(keyword)
                for i in range(count):
                    x_train.append(keyword)
                    y_true.append(expected_class)
                    y_pred.append(predicted_class)

        from sklearn.metrics import classification_report
        print(classification_report(y_true, y_pred))

    def run(self):
        print("Querying data...")
        results = self.query(SQL_QUERY_KEYWORDS_GENRE)
        print("Plotting data...")
        # compute a map containing the genre-specific keyword counts for each genre
        self.keyword_totals = {}
        for row in results:
            genre = row['genre']
            keyword = row['keyword']
            count = row['count']
            if genre not in self.keyword_totals:
                self.keyword_totals[genre] = {}
            self.keyword_totals[genre][keyword] = count

        self.classification_report()

        # create a list of the top 10 keywords and their counts
        # for each genre
        top_10_list = {}
        for genre in self.keyword_totals.keys():
            top10 = self.top_10(genre)
            if top10[0][1] != 1:
                top_10_list[genre] = top10

        # plot the genre and keyword combinations
        self.plot_genre_keywords(top_10_list)