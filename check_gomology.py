#!/usr/bin/python3
import sys
import os

try:
    import requests
except ImportError:
    print('Отсутствует библиотека requests, для установки необходимо выполнить команду: pip install requests')
    input()

from design_loader import Loader, Design, Region


class DesignGomology(Design):
    def set_match(self, overlap):
        for number, region in enumerate(self.regions):
            print(f"Поиск совпадений {number} из {len(self.regions)} >= {overlap}%")
            region.set_gomology(self.track.db, overlap)
            print(f"Готово {number} из {len(self.regions)}")

    def create_txt(self, output_path):
        with open(output_path, 'w') as file:
            print('Создается файл')
            file.write('chrom\tstart\tend\tg_chrom\tg_start\tg_end\n')
            for reg in self.regions:
                if reg.gomology:
                    for g in reg.gomology:
                        file.write(
                            f"{reg.chrom}\t{reg.chrom_start}\t{reg.chrom_end}\t"
                            f"{g['chrom']}\t{g['tStart']}\t{g['tEnd']}\n"
                        )
        print('Готово')


class RegionGomology(Region):
    def __init__(self, data):
        super().__init__(data)
        self.gomology = None

    def set_gomology(self, genome, overlap):
        sequence = self.__get_sequence(genome)
        blat_data = self.__get_BLAT_data(genome, sequence)
        self.gomology = self.__match_filter(blat_data, overlap)

    def __get_sequence(self, genome):
        print(f"Получение последовательности для записи {self.get_coord()}")
        return requests.get(
            f"https://api.genome.ucsc.edu/getData/sequence?genome={genome};chrom={self.chrom};start={self.chrom_start};end={self.chrom_end}"
        ).json()['dna']

    def __get_BLAT_data(self, genome, sequence):
        print(f"Получение данных о совпадении для записи {self.get_coord()}")
        return requests.get(
            f"https://genome.ucsc.edu/cgi-bin/hgBlat?userSeq={sequence}&type=DNA&db={genome}&output=json"
        ).json()

    def __match_filter(self, blat_data, overlap):
        match_list = []
        matches = blat_data['fields'].index('matches')
        chrom = blat_data['fields'].index('tName')
        tStart = blat_data['fields'].index('tStart')
        tEnd = blat_data['fields'].index('tEnd')
        for match in blat_data['blat']:
            if int(match[matches])*100/(int(self.chrom_end) - int(self.chrom_start)) >= int(overlap):
                if int(match[tStart]) != int(self.chrom_start) and int(match[tEnd]) != int(self.chrom_end):
                    print(f"Найдено совпадение последовательности превышающее {overlap}")
                    match_list.append(
                        {
                            'chrom': match[chrom],
                            'tStart': match[tStart],
                            'tEnd': match[tEnd]
                        }
                    )
        return match_list


if __name__ == '__main__':
    input_path = os.path.abspath(sys.argv[1])
    output_path = os.path.abspath(sys.argv[2])
    overlap = sys.argv[3]

    track, data = Loader.load_design(input_path)
    d = DesignGomology(data, track, region_class=RegionGomology)
    d.set_match(overlap)
    d.create_txt(output_path)
