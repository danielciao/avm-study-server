import pandas as pd
from scipy.spatial import KDTree


class GreenSpaceFinder:
    def __init__(self, reader, onsud_df):
        self.reader = reader

        private_space_df = self.__load_private_outdoor_space_data()
        green_space_df = self.__load_public_green_space_data()

        self.df = GreenSpaceFinder.__enrich_onsud_data(
            private_space_df, green_space_df, onsud_df
        )
        self.dtypes = self.df.dtypes
        self.tree = KDTree(self.df[['UPRN_LATITUDE', 'UPRN_LONGITUDE']].values)

    def __load_private_outdoor_space_data(self):
        df = self.reader.load_file(
            name='osprivateoutdoorspacereferencetables',
            type='xlsx',
            load=lambda f: pd.read_excel(f, header=1, sheet_name=4)
        )

        # Only keep the columns we need
        df = df.iloc[:, [6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20]]
        df.columns = ['MSOA', 'MSOAName', 'HouseWithPOS', 'HouseTotalPOS', 'HouseWithPOSPct', 'HouseAvgPOS',
                      'HouseMedPOS', 'FlatWithPOS', 'FlatTotalPOS', 'FlatPOSCount', 'FlatWithPOSPct', 'FlatAvgPOS', 'FlatPOSShare']

        df = df.add_prefix('PGN_')
        df.set_index('PGN_MSOA', inplace=True)

        return df

    def __load_public_green_space_data(self):
        df = self.reader.load_file(
            name='ospublicgreenspacereferencetables',
            type='xlsx',
            load=lambda f: pd.read_excel(f, header=0, sheet_name=7)
        )

        # Only keep the columns we need
        df = df.iloc[:, [8, 9, 12, 13, 14, 15]]
        df.columns = ['LSOA', 'LSOAName',
                      'NearestParkDistanceAvg', 'NearestParkSizeAvg',
                      '1kParkCountAvg', '1kParkSizeAvg']

        df = df.add_prefix('PGN_')
        df.set_index('PGN_LSOA', inplace=True)

        return df

    @staticmethod
    def __enrich_onsud_data(private_space_df, green_space_df, onsud_df):
        enriched_df = onsud_df[['UPRN_LATITUDE', 'UPRN_LONGITUDE',
                                'CPO_LSOA', 'CPO_MSOA']]
        enriched_df = enriched_df.merge(
            private_space_df, how='left', left_on='CPO_MSOA', right_index=True)
        enriched_df = enriched_df.merge(
            green_space_df, how='left', left_on='CPO_LSOA', right_index=True)
        return enriched_df

    def get_closest_matches(self, central_point, top_n=5):
        # Query the KDTree for the top_n closest points
        distances, indices = self.tree.query([central_point], k=top_n)

        # Get the closest points in the DataFrame
        match = self.df.iloc[indices[0]]

        # If the result is a Series, convert it to a DataFrame
        return match if isinstance(match, pd.DataFrame) else match.to_frame().T.astype(self.dtypes)
