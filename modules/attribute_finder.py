import modules.utils as utils
import pandas as pd
from modules.data_reader import S3DataReader
from modules.epc_finder import EPCFinder
from modules.greenspace_finder import GreenSpaceFinder
from modules.imd_finder import IMDFinder
from modules.school_finder import SchoolFinder
from modules.transport_finder import TransportFinder


class LocationAttributeFinder:
    def __init__(self):
        self.reader = S3DataReader()

        with utils.Timer() as t:
            t.log(f'Initialising attribute finders')

            onsud_uprn_df = self.reader.load_file(
                'london_onsud_uprn', 'parquet')

            self.epc_finder = EPCFinder(self.reader, onsud_uprn_df)
            self.transport_finder = TransportFinder(self.reader)
            self.school_finder = SchoolFinder(self.reader, onsud_uprn_df)
            self.space_finder = GreenSpaceFinder(self.reader, onsud_uprn_df)
            self.imd_finder = IMDFinder(self.reader, onsud_uprn_df)

            t.log(f'All attribute finders initialised!')

    def get_load_status(self):
        return {
            'epc': len(self.epc_finder.df),
            'transport': len(self.transport_finder.df),
            'schools': len(self.school_finder.df),
            'green_space': len(self.space_finder.df),
            'imd': len(self.imd_finder.df)
        }

    def find_epc(self, lat, lon, top_n):
        return self.epc_finder.get_closest_matches(central_point=(lat, lon), top_n=top_n).to_json(orient='records')

    def find_transport(self, lat, lon, radius):
        return self.transport_finder.get_stops_within_radius(central_point=(lat, lon), radius=radius).to_json(orient='records')

    def find_schools(self, lat, lon, radius):
        return self.school_finder.get_schools_within_radius(central_point=(lat, lon), radius=radius).to_json(orient='records')

    def find_green_space(self, lat, lon, top_n):
        return self.space_finder.get_closest_matches(central_point=(lat, lon), top_n=top_n).to_json(orient='records')

    def find_imd(self, lat, lon, top_n):
        return self.imd_finder.get_closest_matches(central_point=(lat, lon), top_n=top_n).to_json(orient='records')

    def find_all(self, lat, lon, radius):
        transport = self.transport_finder.get_stop_counts(
            central_point=(lat, lon), radius=radius)
        school = self.school_finder.get_school_counts(
            central_point=(lat, lon), radius=radius)
        green_space = self.space_finder.get_closest_matches(
            central_point=(lat, lon), top_n=1)
        imd = self.imd_finder.get_closest_matches(
            central_point=(lat, lon), top_n=1)

        df = pd.concat([
            transport.reset_index(drop=True),
            school.reset_index(drop=True),
            green_space.reset_index(drop=True),
            imd.reset_index(drop=True)
        ], axis=1)
        df = df.loc[:, ~df.columns.duplicated(keep='last')]  # type: ignore

        return df.to_json(orient='records')
