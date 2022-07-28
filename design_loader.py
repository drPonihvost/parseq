import igv_notebook

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
        self.__parse_track(track)

    def __parse_track(self, track):
        params = {param.split('=')[0]: param.split('=')[1] for param in track.split(' ')[1:]}
        self.__dict__.update(params)


class Design:
    def __init__(self, data, track):
        self.regions = self.__create_region_list(data)
        self.track = DesignTrack(track)

    @staticmethod
    def __create_region_list(data):
        return [Region(row.split('\t')) for row in data]


class Region:
    def __init__(self, data):
        self.chrom = data[0]
        self.chromStart = data[1]
        self.chromEnd = data[2]
        self.name = data[3]
        self.other = data[5]

    def get_coord(self):
        return f"{self.chrom}:{self.chromStart}-{self.chromEnd}"


info, data = Loader.load_design(r'/home/philipp/Рабочий стол/ТЗ/parseq/IAD143293_241_Designed.bed')
d = Design(data, info)
print(d.regions[0].other)

igv_notebook.init()
b = igv_notebook.Browser(
    {
        "genome": d.track.db,
        "locus": d.regions[0].get_coord()
    }
)
