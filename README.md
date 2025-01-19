# Porównanie metod renderingu

W ramach projektu należy stworzyć program, który będzie umożliwiał rendering różnymi metodami.

## Wymagania

W programie powinny znaleźć się m.in.:
1. Obsługa mapy środowiska
2. Interfejs konsolowy/graficzny, który umożliwi:
   - Wczytanie sceny (modele wraz z materiałami oraz ich właściwościami) z pliku
   - Podanie algorytmu renderowania wraz z parametrami
   - Wczytanie mapy środowiska
3. Implementacja algorytmu śledzenia promieni oraz mapowania fotonów
4. Statystyka na temat renderingu np. ilość wyszukiwanych przecięć, ilość wygenerowanych promieni cienia itd.

## Kryteria oceny

1. **Działanie programu** - realizacja funkcji oraz wytłumaczenie algorytmów stojących za implementacją w zrozumiały sposób (dotyczy projektów powiązanych z artykułem) (19 p.)
2. **Efekty wizualne** - prezentacja działania programu oraz kroku algorytmu w przyjemnie wizualny sposób (przygotowanie modeli, scenerii itd.) (2 p.)
3. **Jakość kodu** (3 p.)
4. **Prezentacja wykonana na wykładzie** (1 p.)

## Terminy

| Zadanie                                                 | Ostateczny termin          |
|---------------------------------------------------------|----------------------------|
| ~~Deklaracja zespołów projektowych~~                    | 10.11.2024                 |
| ~~Przydział projektów~~                                 | 12.11.2024                 |
| ~~Prezentacja projektów związanych z artykułami~~       | 26.11.2024                 |
| ~~Prezentacja projektów związanych z artykułami~~       | 3.12.2024                  |
| (!) Oddanie pierwszego etapu projektu (!)               | 13.12.2024                 |
| **Oddanie ostatecznej wersji programu**                 | **24.01.2025**             |
| **Prezentacja projektów nie związanych z artykułami**   | **28.01.2025**             |

## Wywoływanie z terminala

```bash
# Wywołanie algorytmu ray tracing z domyślnymi parametrami i sceną
python main.py --algorithm ray_tracing
```

```bash
# Wywołanie algorytmu ray tracing ze specyfikacją sceny z folderu scenes, liczbą sampli na pixek, rozdzielczością, środowiskiem i rozmyciem środowiska
python main.py --scene three_spheres --samples_per_pixel 100 --resolution 100x100 --environment lake.png --env_blur 10
```

```bash
# Wywołanie algorytmu photon mapping ze specyfikacją liczby fotonów i maksymalnej głębokości
python main.py --algorithm photon_mapping --max_depth --num_photons 1000
```
