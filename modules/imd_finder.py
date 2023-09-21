import pandas as pd
from modules.kd_tree_finder import KDTreeFinder


class IMDFinder(KDTreeFinder):
    def __init__(self, reader, onsud_df):
        self.reader = reader

        self.df = self.__load_data()
        self.df = IMDFinder.__enrich_onsud_data(
            self.df, onsud_df
        )
        super().__init__(self.df, 'UPRN_LATITUDE', 'UPRN_LONGITUDE')

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
