class Loader:
    @classmethod
    def load_design(cls, path):
        return cls.__open(path)

    @classmethod
    def __open(cls, path):
        with open(path, 'r') as file:
            track, *data = file.read().splitlines()
            return track, data


class DesignTrack:
    def __init__(self, track):
        self.track_string = track
        self.__parse_track(track)

    def __parse_track(self, track):
        params = {param.split('=')[0]: param.split('=')[1] for param in track.split(' ')[1:]}
        self.__dict__.update(params)


class Region:
    def __init__(self, data):
        self.chrom = data[0]
        self.chrom_start = data[1]
        self.chrom_end = data[2]
        self.ampl_name = data[3]
        self.strand = data[4]
        self.other = data[5]


class Design:
    def __init__(self, data, track, region_class=Region):
        self.track = DesignTrack(track)
        self.regions = self.__create_region_list(data, region_class)

    @staticmethod
    def __create_region_list(data, cls):
        return [cls(row.split('\t')) for row in data]
