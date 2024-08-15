# Milionerzy
Gra "Milionerzy" napisana w języku Python.

## Instrukcja
1. Instrukcja zakłada posiadanie pythona w wersji 3.9.13 oraz poprawną instalację i obsługę pip, venv itp.
2. Pobierz projekt, wejdź w niego, a następnie odpal wirtualne środowisko. W zależności od systemu operacyjnego odpal na nim plik setup.sh (Linux), lub setup.bat (Windows). Instalacja była testowana na Linuxie i Windowsie, ale jeśli wystąpi problem z jakąś paczką to należy ją doinstalować ręcznie.
3. Odpal main.py

## Dodatkowe informacje
1. Plik data/questions.xslx jest uzupełniony małym zestawem pytań, gra jednak wymaga do poprawnego funkcjonowania - conajmniej jedno - a najlepiej dwa pytania (w razie koła ratunkowego - zamiana pytania) dla każdego z price=[100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 40000, 75000, 125000, 250000, 500000, 1000000], a przykładowy wiersz pliku powinien wyglądać następująco:

| question | correct_answer	| answer_A | answer_B	| answer_C | answer_D | category | price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Przykladowe pytanie | A | Odp A | Odp B | Odp C | Odp D | Kategoria | 5000 |

2. Do poprawnego działania gry wymagane jest istnienie plików data/already_asked.xlsx oraz data/questions.xlsx w poprawnym formacie (tak jak są dodane na repozytorium)
3. Większość przycisków reaguje na podwójne kliknięcie - szczególnie w miejscach, w których pojedyncze kliknięcie mogłoby być przypadkowe i spowodować koniec gry. Wyjątkami są przykładowo przycisk zapisu nazwy gracza oraz przycisk wyjścia w głównym menu, w które wystarczy kliknąć raz.
4. W celu poprawnego działania programu należy odczekać kilka sekund po wyświetleniu pytania zanim zaznaczy się odpowiedź - przy zbyt szybkim klikaniu nie działa poprawnie obsługa muzyki, przez co doświadczenia związane z grą nie będą kompletne.
5. Koła ratunkowe to: Telefon do specjalisty(Członek rodziny), 50/50 - eliminujące dwie losowe niepoprawne odpowiedzi, Telefon do przyjaciela, Zamiana pytania. W przypadku kół ratunkowych związanych z dzwonieniem jest dodana funkcjonalność odmierzania czasu, który należy włączyć, kiedy zaczyna czytać się pytanie, gdy czas się skończy połączenie powinno zostać zerwane.
6. Zakłada się, że grę prowadzi osoba - a'la prowadzący teleturnieju i to ta osoba obsługuje jej interfejs, czyta pytania, obsługuje koła ratunkowe związane z telefonami itp.

### Widok menu:
![menu](https://github.com/damianstefan44/Milionerzy/assets/56561841/dbc9b97d-9e28-4bbd-ad24-fbed26605250)

### Widok pytania:
![pytanie](https://github.com/damianstefan44/Milionerzy/assets/56561841/5ae42189-564e-4883-a598-69f6dee8aca4)
