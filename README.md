# Linux:

## Подготовка:
    cd <content root>

    pip install -r requirements.txt

    chmod ugo+x design_annotation.py

    chmod ugo+x check_gomology.py

## Задание №1:
    ./design_annotation.py <input_file> <output_file>

    input_file - путь к файлу дизайна в формате .bed

    output_file - путь и имя файла выходных данных

    Пример:

    philipp@philipp:~/Рабочий стол/ТЗ/parseq$ ./design_annotation.py IAD143293_241_Designed.bed IAD143293_Designed_annotated.txt

## Задание № 2
    ./check_gomology.py <input_file> <output_file> <owerlap>

    input_file - путь к файлу дизайна в формате .bed

    output_file - путь и имя файла выходных данных

    owerlap - покрытие (процент идентичности, значения выше которого будут приведены как гомологичные от 1 до 100)

    Пример:

    philipp@philipp:~/Рабочий стол/ТЗ/parseq$ ./check_gomology.py IAD143293_241_Designed.bed IAD143293_Designed_gomology.txt 100

# Windows:

## Подготовка:
    cd <content root>

    python -m venv venv

    venv\Scripts\activate

    pip install -r requirements.txt

## Задание №1:
    python ./design_annotation.py <input_file> <output_file>

    input_file - путь к файлу дизайна в формате .bed

    output_file - путь и имя файла выходных данных

    Пример:

     python .\design_annotation.py IAD143293_241_Designed.bed IAD143293_241_Designed_annotation.txt
    

## Задание № 2
    python ./check_gomology.py <input_file> <output_file> <owerlap>

    input_file - путь к файлу дизайна в формате .bed

    output_file - путь и имя файла выходных данных

    owerlap - покрытие (процент идентичности, значения выше которого будут приведены как гомологичные от 1 до 100)

    Пример:

    python .\check_gomology.py IAD143293_241_Designed.bed IAD143293_241_Designed_gomology.txt 100


