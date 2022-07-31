import requests

from design_loader import Loader, Design, Region


class DesignGomology(Design):
    def set_match(self):
        for region in self.regions:
            region.set_gomology(self.track.db)

    def create_txt(self):
        with open(f"{self.track.name}_gomology.txt", 'w') as file:
            file.write('chrom\tstart\tend\tg_chrom\tg_start\tg_end\n')
            for reg in self.regions:
                if reg.gomology:
                    for g in reg.gomology:
                        file.write(
                            f"{reg.chrom}\t{reg.chrom_start}\t{reg.chrom_end}\t"
                            f"{g['chrom']}\t{g['tStart']}\t{g['tEnd']}\n"
                        )


class RegionGomology(Region):
    def __init__(self, data):
        super().__init__(data)
        self.gomology = None

    def get_coord(self):
        return f"{self.chrom}:{self.chrom_start}-{self.chrom_end}"

    def set_gomology(self, genome):
        sequence = self.__get_sequence(genome)['dna']
        blat_data = self.__get_BLAT_data(genome, sequence)
        self.gomology = self.__match_filter(blat_data)

    def __get_sequence(self, genome):
        return requests.get(
            f"https://api.genome.ucsc.edu/getData/sequence?genome={genome};chrom={self.chrom};start={self.chrom_start};end={self.chrom_end}"
        ).json()

    @staticmethod
    def __get_BLAT_data(genome, sequence):
        return requests.get(
            f"https://genome.ucsc.edu/cgi-bin/hgBlat?userSeq={sequence}&type=DNA&db={genome}&output=json"
        ).json()

    def __match_filter(self, blat_data):
        match_list = []
        matches = blat_data['fields'].index('matches')
        chrom = blat_data['fields'].index('tName')
        tStart = blat_data['fields'].index('tStart')
        tEnd = blat_data['fields'].index('tEnd')
        for match in blat_data['blat']:
            if match[matches] == int(self.chrom_end) - int(self.chrom_start):
                if int(match[tStart]) != int(self.chrom_start) and int(match[tEnd]) != int(self.chrom_end):
                    match_list.append(
                        {
                            'chrom': match[chrom],
                            'tStart': match[tStart],
                            'tEnd': match[tEnd]
                        }
                    )
        return match_list




    # {
    #     "track": "blat",
    #     "genome": "hg38",
    #     "fields": [
    #         "matches",
    #         "misMatches",
    #         "repMatches",
    #         "nCount",
    #         "qNumInsert",
    #         "qBaseInsert",
    #         "tNumInsert",
    #         "tBaseInsert",
    #         "strand",
    #         "qName",
    #         "qSize",
    #         "qStart",
    #         "qEnd",
    #         "tName",
    #         "tSize",
    #         "tStart",
    #         "tEnd",
    #         "blockCount",
    #         "blockSizes",
    #         "qStarts",
    #         "tStarts"
    #     ],
    #     "blat": [
    #         [
    #             20,
    #             0,
    #             0,
    #             0,
    #             0,
    #             0,
    #             0,
    #             0,
    #             "+",
    #             "YourSeq",
    #             20,
    #             0,
    #             20,
    #             "chr21",
    #             46709983,
    #             31659745,
    #             31659765,
    #             1,
    #             "20",
    #             "0",
    #             "31659745"
    #         ]
    #     ]
    # }


    # строгое вхождение интервала в экзон
    # def __set_exon_number(self, request):
    #     result = []
    #     for item in request['ncbiRefSeq']:
    #         exons = zip(item['exonStarts'].split(','), item['exonEnds'].split(','))
    #         n = 1
    #         for exon in exons:
    #             if self.chrom_start > exon[0] and self.chrom_end < exon[1]:
    #                 result.append(str(n))
    #             n += 1
    #     if result:
    #         self.exon_number = list(set(result))

    # включает любые вхождения интервала в экзон
    # def __set_exon_number(self, request):
    #     result = set()
    #     for item in request['ncbiRefSeq']:
    #         exons = zip(item['exonStarts'].split(','), item['exonEnds'].split(','))
    #         n = 0
    #         for exon in exons:
    #             n += 1
    #             if self.chrom_end < exon[0] or self.chrom_start > exon[1]:
    #                 continue
    #             result.update(str(n))
    #     if result:
    #         self.exon_number = list(result)

track, data = Loader.load_design(r'C:\Users\kudro\Desktop\ТЗ\parseq\IAD143293_241_Designed_short.bed')
d = DesignGomology(data, track, region_class=RegionGomology)
d.set_match()
d.create_txt()
