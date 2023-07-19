import pandas as pd
from scipy.spatial import KDTree


class IMDFinder:
    def __init__(self, reader, onsud_df):
        self.reader = reader

        self.df = self.__load_data()
        self.df = IMDFinder.__enrich_onsud_data(
            self.df, onsud_df
        )
        self.dtypes = self.df.dtypes
        self.tree = KDTree(self.df[['UPRN_LATITUDE', 'UPRN_LONGITUDE']].values)

    def __load_data(self):
        df = self.reader.load_file(
            name='File_2_-_IoD2019_Domains_of_Deprivation',
            type='xlsx',
            load=lambda f: pd.read_excel(f, header=1, sheet_name=1)
        )

        # Only keep the columns we need
        df = df.iloc[:, [0, 1, 5, 7, 9, 11, 13, 15, 17]]
        df.columns = ['LSOA', 'LSOAName', 'IMDDecile', 'IncDecile',
                      'EmpDecile', 'EduDecile',  'CrmDecile', 'HouseBarDecile', 'EnvDecile']

        df = df.add_prefix('IMD_')
        df.set_index('IMD_LSOA', inplace=True)

        return df

    @staticmethod
    def __enrich_onsud_data(df, onsud_df):
        enriched_df = onsud_df[['UPRN_LATITUDE', 'UPRN_LONGITUDE', 'CPO_LSOA']]
        enriched_df = enriched_df.merge(
            df, how='left', left_on='CPO_LSOA', right_index=True)
        enriched_df.drop(columns=['CPO_LSOA'], inplace=True)
        return enriched_df

    def get_closest_matches(self, central_point, top_n=5):
        # Start by querying for the top_n points
        distances, indices = self.tree.query([central_point], k=top_n)

        # If there are ties at the end of the list, query for more points
        while top_n > 1 and distances[0][-1] == distances[0][-2]:
            top_n += 1
            distances, indices = self.tree.query([central_point], k=top_n)

         # Get the closest points in the DataFrame
        match = self.df.iloc[indices[0]]

        # If the result is a Series, convert it to a DataFrame
        return match if isinstance(match, pd.DataFrame) else match.to_frame().T.astype(self.dtypes)
