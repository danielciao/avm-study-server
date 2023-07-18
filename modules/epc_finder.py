import pandas as pd
from scipy.spatial import KDTree


class EPCFinder:
    def __init__(self, reader, uprn_df):
        self.reader = reader

        self.df = self.reader.load_file(name='london_epc', type='parquet')
        self.df = EPCFinder.__enrich_epc_data(self.df, uprn_df)
        self.dtypes = self.df.dtypes
        self.tree = KDTree(self.df[['UPRN_LATITUDE', 'UPRN_LONGITUDE']].values)

    @staticmethod
    def __enrich_epc_data(df, uprn_df):
        # # Office for National Statistics (ONS) URPN Directory with ward and borough information
        # uprn_df = uprn_df[['CPO_BOROUGH', 'CPO_WARD', 'CPO_MSOA',
        #                    'CPO_LSOA', 'UPRN_LATITUDE', 'UPRN_LONGITUDE']]

        # # Drop records with no UPRN
        # df = df[df['EPC_UPRN'].notna()]

        # # left join EPC and Open UPRN for geo-coordinates
        # df = df.merge(uprn_df, how='left',
        #               left_on='EPC_UPRN', right_index=True)
        # df = df[df['UPRN_LATITUDE'].notna()]

        # df_first_inspection = df.sort_values(
        #     by='EPC_INSPECTION_DATE').drop_duplicates('EPC_UPRN', keep='first')
        # df_first_inspection = df_first_inspection[[
        #     'EPC_UPRN', 'EPC_INSPECTION_DATE']]
        # df_first_inspection.rename(
        #     columns={'EPC_INSPECTION_DATE': 'EPC_FIRST_INSPECTION_DATE'}, inplace=True)

        # # Calculate per square meter energy consumption
        # df['EPC_ENERGY_CONSUMPTION_CURRENT_PER_SQM'] = df.apply(lambda x: utils.safe_div(
        #     x['EPC_ENERGY_CONSUMPTION_CURRENT'], x['EPC_TOTAL_FLOOR_AREA']), axis=1)
        # df['EPC_CO2_EMISSIONS_CURRENT_PER_SQM'] = df.apply(lambda x: utils.safe_div(
        #     x['EPC_CO2_EMISSIONS_CURRENT'], x['EPC_TOTAL_FLOOR_AREA']), axis=1)
        # df.drop(columns=['EPC_ENERGY_CONSUMPTION_CURRENT',
        #         'EPC_CO2_EMISSIONS_CURRENT'], inplace=True)

        # # Drop duplicates and keep the latest record but also keep the first
        # # inspection date, which could be used to infer the age of the property
        # # later
        # df = df.sort_values(by='EPC_INSPECTION_DATE').drop_duplicates(
        #     'EPC_UPRN', keep='last').merge(df_first_inspection, on='EPC_UPRN')

        return df

    def get_closest_matches(self, central_point, top_n=5):
        # Query the KDTree for the top_n closest points
        distances, indices = self.tree.query([central_point], k=top_n)

        # Get the closest points in the DataFrame
        match = self.df.iloc[indices[0]]

        # If the result is a Series, convert it to a DataFrame
        return match if ~isinstance(match, pd.DataFrame) else match.to_frame().T.astype(self.dtypes)