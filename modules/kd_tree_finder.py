import pandas as pd
from scipy.spatial import KDTree


class KDTreeFinder:
    def __init__(self, df, lat_col, lon_col):
        self.df = df
        self.dtypes = self.df.dtypes
        self.tree = KDTree(self.df[[lat_col, lon_col]].values)

    def get_closest_matches(self, central_point, top_n=5):
        # Start by querying for the top_n points
        distances, indices = self.tree.query([central_point], k=top_n)

        # If there are ties at the end of the list, query for more points
        while top_n > 1 and distances[0][-1] == distances[0][-2]:
            top_n += 1
            distances, indices = self.tree.query([central_point], k=top_n)

        # Get the closest points in the DataFrame
        match = self.df.iloc[indices[0]]

        # If the result is a Series, convert it to a DataFrame so that it can be serialised to JSON
        return match if isinstance(match, pd.DataFrame) else match.to_frame().T.astype(self.dtypes)
