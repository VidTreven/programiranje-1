import re
import os
import csv



car_directory = 'Projektna_naloga'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'sob_pop.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'avti_ned.csv'


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def oglasi_v_blokih(page_content):
    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
    vrne njih seznam"""
    rx = re.compile(r'<!-- MAKE MODEL CONTAINER -->(.*?)'
                    r'<!------------ END CENA  ------------>',
                    re.DOTALL)

    ads = re.findall(rx, page_content)
    return ads

def olepsamo(oglasi):
    sez = []
    for oglas in oglasi:
        avtomobil = []
        imeR = re.compile(r'<div class="GO-Results-Naziv bg-dark px-3 py-2.*?'
                    r'font-weight-bold text-truncate text-white text-decoration-none">.*?'
                    r'<span>(.*?)</span>.*?'
                    r'</div>',
                    re.DOTALL)
        ime = re.findall(imeR, oglas)
        avtomobil.append(ime)

        kilometriR = re.compile(r'<td class="d-none d-md-block pl-3">Prevoženih</td>.*?'
                    r'<td class="pl-3">(.*?) km</td>',
                    re.DOTALL)
        kilometri = re.findall(kilometriR, oglas)
        avtomobil.append(kilometri)

        gorivoR = re.compile(r'<td class="d-none d-md-block pl-3">Gorivo</td>.*?'
                    r'<td class="pl-3">(.*?)</td>',
                    re.DOTALL)
        gorivo = re.findall(gorivoR, oglas)
        avtomobil.append(gorivo)

        menjalnikR = re.compile(r'<td class="d-none d-md-block pl-3">Menjalnik</td>.*?'
                    r'<td class="pl-3 text-truncate">(.*?)</td>',
                    re.DOTALL)
        menjalnik = re.findall(menjalnikR, oglas)
        avtomobil.append(menjalnik)

        motorR = re.compile(r'<td class="d-none d-md-block pl-3">Motor</td>.*?'
                    r'<td class="pl-3 text-truncate">\n'
                    r'\s+(.*?)\n\s+</td>',
                    re.DOTALL)
        motor = re.findall(motorR, oglas)
        avtomobil.append(motor)

        sez.append(avtomobil)
    return sez


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_car_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
    slovarjev parametra ads enaki in je seznam ads neprazen."""
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugače pa sproži napako
    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
    # produkcijskem okolju
    #assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    # write_csv('rgrgertge', ads, directory, filename)
    # return filename

    header = ['ime', 'kilometri', 'gorivo', 'menjalnik', 'motor']
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for oglas in ads:
            vrstica = [oglas[0][0], oglas[1][0], oglas[2][0], oglas[3][0], oglas[4][0]]
            writer.writerow(vrstica)






def main():
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """

    # Iz lokalne (html) datoteke preberemo podatke
    #read_file_to_string(car_directory, frontpage_filename)

    ads = oglasi_v_blokih(read_file_to_string(car_directory, frontpage_filename))
    avtucki = olepsamo(ads)
    write_car_ads_to_csv(avtucki, car_directory, csv_filename)
    return avtucki

    #page_to_ads(read_file_to_string(car_directory, frontpage_filename))
    # Podatke preberemo v lepšo obliko (seznam slovarjev)

    # Dodatno: S pomočjo parametrov funkcije main omogoči nadzor, ali se
    # celotna spletna stran ob vsakem zagon prenese (četudi že obstaja)
    # in enako za pretvorbo

