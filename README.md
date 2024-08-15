# Milionerzy
Gra "Milionerzy" napisana w języku Python (3.9) głównie w tkinterze oraz z pomocą pygame.

## Instrukcja
1. Zainstaluj wszystkie potrzebne biblioteki opisane w requirements.txt
2. Plik data/questions.xslx uzupełnij pytaniami - conajmniej jednym dla każdego z price=[100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 40000, 75000, 125000, 250000, 500000, 1000000], a przykładowy wiersz pliku powinien wyglądać następująco:

| question | correct_answer	| answer_A | answer_B	| answer_C | answer_D | category | price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Przykladowe pytanie | A | Odp A | Odp B | Odp C | Odp D | Kategoria | 5000 |

3. Do odpalenia gry wymagane jest istnienie plików data/already_asked.xlsx oraz data/questions.xlsx w poprawnym formacie (tak jak są dodane na repozytorium)
4. Odpal main.py

### Widok menu:
![menu](https://github.com/damianstefan44/Milionerzy/assets/56561841/dbc9b97d-9e28-4bbd-ad24-fbed26605250)

### Widok pytania:
![pytanie](https://github.com/damianstefan44/Milionerzy/assets/56561841/5ae42189-564e-4883-a598-69f6dee8aca4)
