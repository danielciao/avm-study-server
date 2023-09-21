from modules.kd_tree_finder import KDTreeFinder


class EPCFinder(KDTreeFinder):
    def __init__(self, reader, uprn_df):
        self.reader = reader

        self.df = self.reader.load_file(name='london_epc', type='parquet')
        self.df = EPCFinder.__enrich_epc_data(self.df, uprn_df)
        super().__init__(self.df, 'UPRN_LATITUDE', 'UPRN_LONGITUDE')

    @staticmethod
    def __enrich_epc_data(df, uprn_df):
        # Drop records with no UPRN
        df = df[df['EPC_UPRN'].notna()]

        # Office for National Statistics (ONS) URPN Directory with ward and borough information
        uprn_df = uprn_df[['CPO_BOROUGH', 'CPO_WARD',
                           'CPO_OA', 'CPO_MSOA', 'CPO_LSOA',
                           'UPRN_LATITUDE', 'UPRN_LONGITUDE']]

        # left join EPC and Open UPRN for geo-coordinates
        df = df.merge(uprn_df, how='left',
                      left_on='EPC_UPRN', right_index=True)
        df = df[df['UPRN_LATITUDE'].notna()]

        df_first_inspection = (df.reset_index()
                               .sort_values(by='EPC_INSPECTION_DATE')
                               .drop_duplicates('EPC_UPRN', keep='first')[['EPC_UPRN', 'EPC_INSPECTION_DATE']]
                               .rename(columns={'EPC_INSPECTION_DATE': 'EPC_FIRST_INSPECTION_DATE'})
                               .set_index('EPC_UPRN'))

        # Drop duplicates and keep the latest record but also keep the first
        # inspection date, which could be used to infer the age of the property
        # later
        df = df.sort_values(by='EPC_INSPECTION_DATE').drop_duplicates(
            'EPC_UPRN', keep='last').merge(df_first_inspection, how='left',
                                           left_on='EPC_UPRN', right_index=True)

        return df
