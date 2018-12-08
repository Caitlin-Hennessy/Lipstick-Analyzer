import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LIPSTICKS = os.path.join(os.path.dirname(__file__), "data.csv")

class LipstickAnalyzer:
    # m = prior, C = confidence
    def __init__(self, path=LIPSTICKS, m=None, C=None):
        self.path = path
        self.prior = m
        self.confidence = C
        self.load()

    def load(self):
        self.data = pd.read_csv("data.csv", 
            names=("name", "avg_rating", "num_ratings"), 
            dtype={"name": str, "avg_rating": np.float64, "num_ratings": np.int32},
            usecols=[0, 1, 2])
    
    def scatter_plot(self):
        scatter_plot = this.data.plot.scatter(x="avg_rating", y="num_ratings")
        plt.show()

    def hex_plot(self):
        hex_plot = self.data.plot(x="num_ratings", y="avg_rating", kind="hexbin", 
            xscale="log", cmap="YlGnBu", gridsize=12, mincnt=1)
        plt.show()

    def bayesian_mean(self, avg_rating, num_ratings):
        return ((self.confidence * self.prior + (avg_rating * num_ratings)) /
                (self.confidence + num_ratings))

    def get_bayesian_estimates(self):
        return self.data.apply(lambda row: self.bayesian_mean(row.avg_rating, row.num_ratings), axis=1)

    
    #def get_dirichlet_estimates(self):
        # just bayesian estimate with confidence = 10 and prior = 3.0

    def top_lipsticks(self, n=10):
        self.data["bayes"] = self.get_bayesian_estimates()
        return self.data.sort_values(by=["bayes"], ascending=False).head(10)

    def __str__(self):
        return str(self.data.head())

if __name__ == "__main__":
    lipstick_analyzer = LipstickAnalyzer(LIPSTICKS, 4.0, 25)
    print lipstick_analyzer.top_lipsticks()