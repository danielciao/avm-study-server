import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree


class SchoolFinder:
    def __init__(self, reader, uprn_df):
        self.reader = reader
        self.df = self.__load_data()
        self.df = self.__enrich_school_data(self.df, uprn_df)
        self.df_rad = np.radians(self.df[['UPRN_LATITUDE', 'UPRN_LONGITUDE']])
        self.tree = BallTree(self.df_rad, metric='haversine')

    def __load_data(self):
        column_map = {
            'URN': 'URN',
            'EstablishmentName': 'NAME',
            'TypeOfEstablishment (name)': 'TYPE',
            'EstablishmentTypeGroup (name)': 'MINORGROUP',
            'EstablishmentStatus (name)': 'STATUS',
            'PhaseOfEducation (name)': 'PHASE',
            'Boarders (name)': 'BOARDING',
            'NurseryProvision (name)': 'NURSERY',
            'Gender (name)': 'GENDER',
            'ReligiousCharacter (name)': 'RELCHAR',
            'NumberOfPupils': 'TOTALPUPILS',
            'OfstedRating (name)': 'OFSTEDRATING',
            'HeadTitle (name)': 'HeadTitle',
            'HeadFirstName': 'HeadFirstName',
            'HeadLastName': 'HeadLastName',
            'HeadPreferredJobTitle': 'HeadPreferredJobTitle',
            'Easting': 'Easting',
            'Northing': 'Northing',
            'UPRN': 'UPRN'
        }

        df = self.reader.load_file(
            name='national_school_edubasealldata20230402',
            type='csv',
            load=lambda f: pd.read_csv(f, header=0, usecols=list(
                column_map.keys()), encoding='ISO-8859-1', low_memory=False)
        )
        df.rename(columns=column_map, inplace=True)

        df = df[df['STATUS'] == 'Open']
        df['OFSTEDRATING'] = df['OFSTEDRATING'].apply(
            lambda x: SchoolFinder.__map_ofsted_rating(x))
        df = df.add_prefix('SCH_')

        df.set_index('SCH_URN', inplace=True)

        return df

    @staticmethod
    def __map_ofsted_rating(rating):
        if rating == 'Outstanding':
            return 6
        elif rating == 'Good':
            return 5
        elif rating == 'Requires improvement':
            return 4
        elif rating == 'Inadequate':
            return 3
        else:
            return None if pd.isnull(rating) else 1

    @staticmethod
    def __enrich_school_data(df, uprn_df):
        # left join SCH and UPRN dataset
        location_df = uprn_df[['UPRN_LATITUDE', 'UPRN_LONGITUDE']]
        df = df.merge(location_df, how='left',
                      left_on='SCH_UPRN', right_index=True)

        # Drop records that have not been matched - they are not in London
        print('Matched school count:', len(df[df['UPRN_LATITUDE'].notna()]))
        df = df[df['UPRN_LATITUDE'].notna()]

        return df

    def get_schools_within_radius(self, central_point, radius, minor_group=None, ofsted_rating=None):
        search_radius = radius / 6371e3

        indices = self.tree.query_radius(np.radians(
            np.array(central_point)).reshape(1, -1), r=search_radius)
        nearby_schools = self.df.iloc[indices[0]]

        if minor_group is not None:
            nearby_schools = nearby_schools[nearby_schools['SCH_MINORGROUP'].str.lower(
            ) == minor_group.lower()]

        if ofsted_rating is not None:
            nearby_schools = nearby_schools[nearby_schools['SCH_OFSTEDRATING']
                                            >= ofsted_rating]

        return nearby_schools

    def get_school_counts(self, central_point, radius):
        all_nearby_schools = self.get_schools_within_radius(
            central_point, radius)

        conditions = {
            'SCH_NearbyAcademies': all_nearby_schools['SCH_MINORGROUP'].str.lower() == 'academies',
            'SCH_NearbyIndependentSchools': all_nearby_schools['SCH_MINORGROUP'].str.lower() == 'independent schools',
            'SCH_NearbyNurserySchools': (all_nearby_schools['SCH_PHASE'].str.lower() == 'nursery') | (all_nearby_schools['SCH_NURSERY'].str.lower() == 'has nursery classes'),
            'SCH_NearbyPrimarySchools': all_nearby_schools['SCH_PHASE'].str.lower().isin(['primary', 'middle deemed primary', 'all-through']),
            'SCH_NearbySecondarySchools': all_nearby_schools['SCH_PHASE'].str.lower().isin(['secondary', 'middle deemed secondary', 'all-through']),
            'SCH_NearbyOutstandingSchools': all_nearby_schools['SCH_OFSTEDRATING'] >= 6,
            'SCH_NearbyGoodSchools': all_nearby_schools['SCH_OFSTEDRATING'] >= 5,
            'SCH_NearbyInadequateSchools': all_nearby_schools['SCH_OFSTEDRATING'] <= 3,
        }

        counts = {key: all_nearby_schools[cond].shape[0]
                  for key, cond in conditions.items()}
        counts['SCH_NearbySchools'] = all_nearby_schools.shape[0]

        return pd.DataFrame(counts, index=[0])
