import requests

from design_loader import Loader, Design, Region


class DesignAnnotation(Design):
    def get_annotations(self):
        for region in self.regions:
            region.get_annotation_data(self.track.db)

    def get_gene_name(self):
        with open('gene_list.txt', 'w') as file:
            regions = set()
            for reg in self.regions:
                if reg.name2:
                    regions.update(reg.name2)
            for reg in regions:
                file.write(reg + '\n')

    def create_txt(self):
        with open(f"{self.track.name}_annotated.txt", 'w') as file:
            file.write(self.track.track_string + '\n')
            for reg in self.regions:
                file.write(
                    f"{reg.chrom}\t{reg.chrom_start}\t{reg.chrom_end}\t"
                    f"{reg.strand}\t{reg.other}\t"
                    f"{','.join(reg.name) if reg.name else None}\t"
                    f"{','.join(reg.name2) if reg.name2 else None}\t"
                    f"{','.join(reg.exon_number) if reg.exon_number else None}\n"
                )


class RegionAnnotation(Region):
    def __init__(self, data):
        super().__init__(data)
        self.name = None
        self.name2 = None
        self.exon_number = None

    def get_coord(self):
        return f"{self.chrom}:{self.chrom_start}-{self.chrom_end}"

    def get_annotation_data(self, genome):
        request = self.__get_annotation(genome)
        if request['ncbiRefSeq']:
            self.__set_name(request)
            self.__set_name2(request)
            self.__set_exon_number(request)

    def __get_annotation(self, genome):
        return requests.get(
            f"https://api.genome.ucsc.edu/getData/track?genome={genome};track=ncbiRefSeq;chrom={self.chrom};start={self.chrom_start};end={self.chrom_end}").json()

    def __set_name(self, request):
        self.name = [item['name'] for item in request['ncbiRefSeq']]

    def __set_name2(self, request):
        self.name2 = list(set([item['name2'] for item in request['ncbiRefSeq']]))

    # строгое вхождение интервала в экзон
    # def __set_exon_number(self, request):
    #     result = []
    #     for item in request['ncbiRefSeq']:
    #         exons = zip(item['exonStarts'].split(','), item['exonEnds'].split(','))
    #         n = 0
    #         for exon in exons:
    #             n += 1
    #             if self.chrom_start > exon[0] and self.chrom_end < exon[1]:
    #                 result.append(str(n))
    #     if result:
    #         self.exon_number = result

    # включает любые вхождения интервала в экзон
    def __set_exon_number(self, request):
        result = []
        for item in request['ncbiRefSeq']:
            exons = zip(item['exonStarts'].split(','), item['exonEnds'].split(','))
            n = 0
            for exon in exons:
                n += 1
                if self.chrom_end < exon[0] or self.chrom_start > exon[1]:
                    continue
                result.append(str(n))
        if result:
            self.exon_number = result


track, data = Loader.load_design(r'C:\Users\kudro\Desktop\ТЗ\parseq\IAD143293_241_Designed_short.bed')
d = DesignAnnotation(data, track, region_class=RegionAnnotation)
d.get_annotations()
d.create_txt()
d.get_gene_name()
