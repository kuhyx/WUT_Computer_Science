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
# Wywołanie algorytmu *photon mapping* ze specyfikacją liczby fotonów i maksymalnej głębokości
python main.py --algorithm photon_mapping --max_depth 4 --num_photons 1000
```

```bash
# Wywołanie algorytmu *photon mapping* wykonanego w c++
cd photonmappnig/cpp
./compile.sh
./photon_mapping
```