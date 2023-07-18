import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree


class TransportFinder:
    def __init__(self, reader):
        self.reader = reader
        self.df = self.__load_data()
        self.df_rad = np.radians(self.df[['NPT_Latitude', 'NPT_Longitude']])
        self.tree = BallTree(self.df_rad, metric='haversine')

    def __load_data(self):
        columns = ['ATCOCode', 'CommonName', 'ShortCommonName',
                   'Landmark', 'Street', 'Indicator', 'Bearing', 'LocalityName', 'ParentLocalityName', 'Town', 'Suburb', 'LocalityCentre',
                   'Easting', 'Northing', 'StopType', 'BusStopType', 'CreationDateTime', 'ModificationDateTime', 'RevisionNumber', 'Modification', 'Status',
                   'ETRS89GD-Lat', 'ETRS89GD-Long']

        df = self.reader.load_file(
            name='NaPTAN_stops_geodetic',
            type='csv',
            load=lambda f: pd.read_csv(f,  header=0, usecols=columns, parse_dates=[
                                       'CreationDateTime', 'ModificationDateTime'], low_memory=False)
        )
        df.rename(columns={'ETRS89GD-Lat': 'Latitude',
                  'ETRS89GD-Long': 'Longitude'}, inplace=True)

        # Drop inactive stops
        df = df[df['Status'] == 'active']

        df = df.add_prefix('NPT_')
        df.set_index('NPT_ATCOCode', inplace=True)

        return df

    def get_stops_within_radius(self, central_point, radius, types=None):
        search_radius = radius / 6371e3

        indices = self.tree.query_radius(np.radians(
            np.array(central_point)).reshape(1, -1), r=search_radius)
        nearby_stops = self.df.iloc[indices[0]]

        if types is not None:
            nearby_stops = nearby_stops[nearby_stops['NPT_StopType'].isin(
                types)]

        return nearby_stops

    def get_stop_counts(self, central_point, radius):
        all_nearby_stops = self.get_stops_within_radius(central_point, radius)

        type_map = {
            'NPT_NearbyBusStops': ['BCT', 'BCS', 'BCQ'],
            'NPT_NearbyTramMetroStops': ['PLT', 'TMU', 'MET'],
            'NPT_NearbyRailStops': ['RSE', 'RLY'],
        }

        counts = {key: all_nearby_stops[all_nearby_stops['NPT_StopType'].isin(
            types)].shape[0] for key, types in type_map.items()}
        counts['NPT_NearbyStops'] = sum(counts.values())

        return pd.DataFrame(counts, index=[0])
