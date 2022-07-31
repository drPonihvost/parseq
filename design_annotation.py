#!/usr/bin/python3
import sys
import os

try:
    import requests
except ImportError:
    print('Отсутствует библиотека requests, для установки необходимо выполнить команду: pip install requests')
    input()

from design_loader import Loader, Design, Region


class DesignAnnotation(Design):
    def get_annotations(self):
        for region in self.regions:
            print(f"Аннотирование записи {self.regions.index(region) + 1} из {len(self.regions)}")
            region.get_annotation_data(self.track.db)
            print(f"Готово {self.regions.index(region) + 1} из {len(self.regions)}")
        print('Аннотирование окончено')

    def get_gene_name(self):
        with open('gene_list.txt', 'w') as file:
            regions = set()
            for reg in self.regions:
                if reg.name2:
                    regions.update(reg.name2)
            for reg in regions:
                file.write(reg + '\n')

    def create_txt(self, output_path):
        print('Создается файл')
        with open(output_path, 'w') as file:
            file.write(self.track.track_string + '\n')
            for reg in self.regions:
                file.write(
                    f"{reg.chrom}\t{reg.chrom_start}\t{reg.chrom_end}\t"
                    f"{reg.strand}\t{reg.other}\t"
                    f"{','.join(reg.name) if reg.name else None}\t"
                    f"{','.join(reg.name2) if reg.name2 else None}\t"
                    f"{','.join(reg.exon_number) if reg.exon_number else None}\n"
                )
        print('Готово')


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
            print('Запись данных')
            self.__set_name(request)
            self.__set_name2(request)
            self.__set_exon_number(request)
        else:
            print('Аннотация отсутствует')

    def __get_annotation(self, genome):
        print(f"Получение аннотации для записи {self.get_coord()}")
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


if __name__ == '__main__':
    input_path = os.path.abspath(sys.argv[1])
    output_path = os.path.abspath(sys.argv[2])

    track, data = Loader.load_design(input_path)
    d = DesignAnnotation(data, track, region_class=RegionAnnotation)
    d.get_annotations()
    d.create_txt(output_path)
