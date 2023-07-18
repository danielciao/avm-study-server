from modules.data_reader import S3DataReader
from modules.epc_finder import EPCFinder
from modules.greenspace_finder import GreenSpaceFinder
from modules.imd_finder import IMDFinder
from modules.school_finder import SchoolFinder
from modules.transport_finder import TransportFinder


class LocationAttributeFinder:
    def __init__(self):
        # Load and prepare all the necessary data
        self.reader = S3DataReader(
            bucket_name='avm-area-data',
            region_name='eu-west-2',
            aws_access_key_id='AKIAWJUUQTPWZZXZRLE6',
            aws_secret_access_key='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',
        )

        onsud_uprn_df = self.reader.load_file('london_onsud_uprn', 'parquet')

        self.epc_finder = EPCFinder(self.reader, onsud_uprn_df)
        self.transport_finder = TransportFinder(self.reader)
        self.school_finder = SchoolFinder(self.reader, onsud_uprn_df)
        self.space_finder = GreenSpaceFinder(self.reader, onsud_uprn_df)
        self.imd_finder = IMDFinder(self.reader, onsud_uprn_df)

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
