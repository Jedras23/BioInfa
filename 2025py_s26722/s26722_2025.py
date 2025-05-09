# Program: Generator sekwencji  nukleotydowych w formacie FASTA
# Cel: Program generuje losową sekwencję DNA, oblicza statystyki zawartości nukleotydów,
#      wstawia imię użytkownika w losowe miejsce sekwencji i zapisuje dane w formacie FASTA.
# Kontekst zastosowania: Użyteczny w edukacji biologicznej, bioinformatyce oraz jako narzędzie pomocnicze
#      do generowania danych testowych w analizie sekwencji DNA.

import random  # Biblioteka do operacji losowych
from collections import Counter  # MODIFIED (lepsze i bardziej czytelne liczenie nukleotydów)

# Funkcja do generowania losowej sekwencji DNA o zadanej długości
def generuj_sekwencje_dna(dlugosc):
    return ''.join(random.choices('ACGT', k=dlugosc))  # Wybiera losowe nukleotydy z zestawu 'A', 'C', 'G', 'T'

# Funkcja obliczająca statystyki procentowe dla nukleotydów oraz stosunek CG do AT
def oblicz_statystyki(sekwencja):
    dl = len(sekwencja)  # Obliczenie długości sekwencji

    # ORIGINAL:
    # statystyki = {}
    # for nukleotyd in "ACGT":
    #     statystyki[nukleotyd] = round((sekwencja.count(nukleotyd) / dl) * 100, 1)
    # MODIFIED (lepsza wydajność i czytelność dzięki Counter):
    licznik = Counter(sekwencja)  # Liczy wystąpienia każdego nukleotydu
    statystyki = {
        nukleotyd: round((licznik[nukleotyd] / dl) * 100, 1) for nukleotyd in "ACGT"
    }  # Oblicza procentowy udział każdego nukleotydu

    cg = licznik['C'] + licznik['G']  # Liczba nukleotydów C i G
    at = licznik['A'] + licznik['T']  # Liczba nukleotydów A i T
    stosunek_cg_do_at = round((cg / at) * 100, 1) if at != 0 else 0  # Stosunek CG/AT jako procent
    return statystyki, stosunek_cg_do_at  # Zwraca słownik statystyk i stosunek CG/AT

# Funkcja zapisująca sekwencję do pliku FASTA, z imieniem w losowym miejscu
def zapisz_do_fasta(id_sekwencji, opis, sekwencja, imie):
    nazwa_pliku = f"{id_sekwencji}.fasta"  # Tworzy nazwę pliku na podstawie ID

    # ORIGINAL:
    # indeks = random.randint(0, len(sekwencja))
    # sekwencja_z_imieniem = sekwencja[:indeks] + imie + sekwencja[indeks:]
    # MODIFIED (dodano sprawdzenie długości, aby uniknąć błędu przy krótkich sekwencjach):
    if len(sekwencja) < len(imie):  # Sprawdzenie, czy sekwencja jest wystarczająco długa
        raise ValueError("Sekwencja jest za krótka, aby wstawić imię.")
    indeks = random.randint(0, len(sekwencja) - len(imie))  # Losowy indeks do wstawienia imienia
    sekwencja_z_imieniem = sekwencja[:indeks] + imie + sekwencja[indeks:]  # Tworzy nową sekwencję z imieniem

    with open(nazwa_pliku, 'w') as plik:  # Otwiera plik do zapisu
        plik.write(f">{id_sekwencji} {opis}\n")  # Nagłówek w formacie FASTA
        # ORIGINAL:
        # plik.write(sekwencja_z_imieniem + "\n")
        # MODIFIED (format FASTA – linie po 80 znaków):
        for i in range(0, len(sekwencja_z_imieniem), 80):  # Dzieli sekwencję na linie po 80 znaków
            plik.write(sekwencja_z_imieniem[i:i+80] + "\n")  # Zapisuje każdą linię
    return nazwa_pliku  # Zwraca nazwę utworzonego pliku

# Główna funkcja programu – pobiera dane od użytkownika, uruchamia pozostałe funkcje
def main():
    try:
        dlugosc = int(input("Podaj długość sekwencji: "))  # Pobiera długość sekwencji
    except ValueError:
        print("Błąd: długość musi być liczbą całkowitą.")  # Obsługa błędu w przypadku nieprawidłowego wejścia
        return

    id_sekwencji = input("Podaj ID sekwencji: ").strip()  # Pobiera ID sekwencji
    if not id_sekwencji:
        print("Błąd: ID sekwencji nie może być puste.")  # Sprawdza, czy ID nie jest puste
        return
    opis = input("Podaj opis sekwencji: ").strip()  # Pobiera opis sekwencji
    imie = input("Podaj imię: ").strip().lower().capitalize()  # Pobiera imię i formatuje je (pierwsza litera duża)

    if dlugosc < len(imie):  # Sprawdza, czy długość sekwencji pozwala na wstawienie imienia
        print("Błąd: długość sekwencji musi być większa niż długość imienia.")
        return

    sekwencja = generuj_sekwencje_dna(dlugosc)  # Generuje losową sekwencję DNA
    statystyki, stosunek_cg_do_at = oblicz_statystyki(sekwencja)  # Oblicza statystyki sekwencji
    nazwa_pliku = zapisz_do_fasta(id_sekwencji, opis, sekwencja, imie)  # Zapisuje sekwencję do pliku FASTA

    print(f"\nSekwencja została zapisana do pliku {nazwa_pliku}")  # Informuje o zapisanym pliku
    print("Statystyki sekwencji:")
    for nukleotyd in "ACGT":  # Wypisuje procentowy udział każdego nukleotydu
        print(f"{nukleotyd}: {statystyki[nukleotyd]}%")
    print(f"%CG: {statystyki['C'] + statystyki['G']}")  # Wypisuje łączny udział C i G w procentach

# Uruchamia program, jeśli plik jest uruchamiany bezpośrednio
if __name__ == "__main__":
    main()
