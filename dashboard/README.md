# intall before opening

```bash
pip install -r requirements.txt
python app.py
```

## the app opens <http://127.0.0.1:8050>.

## Pages

| Path        | Module                | What it shows                                   |
| ----------- | --------------------- | ----------------------------------------------- |
| `/`         | `pages/home.py`       | Overview, live snapshot KPIs, navigation cards. |
| `/monitor`  | `pages/monitor.py`    | Real-time BPM/IBI from simulation or ESP32.     |
| `/analise`  | `pages/analysis.py`   | Historical CSV analysis with filters + export.  |
| `/gabriel`  | `pages/gabriel.py`    | Patient Gabriel record (200-beat reference set).|

## Data sources

- **Simulacao** replays `data/gabriel_data.csv` beat-by-beat through the
  same `PPGAnalyzer` used by the production pipeline.
- **ESP32 (serial)** expects newline-delimited JSON on the COM port,
  e.g. `{"bpm": 75.3, "ibi": 820, "ts_ms": 12345}`. Firmware reference
  lives in `esp32/esp32_max30100.ino`.

Live beats are appended to `data/cardiac_data.csv` (auto-saved unless
disabled on the control rail).

## Layout

```
cardiac_dashboard_dash/
  app.py                # Dash entry, topbar, nav, routing
  pages/                # auto-registered via dash.register_page
  assets/
    style.css           # HUD theme (squared, clinical, grid backdrop)
    alert.wav           # audible arrhythmia alert
  utils/
    analysis.py         # PPG math (unchanged from original)
    storage.py          # CSV helpers
    serial_reader.py    # ESP32 JSON stream reader
    theme.py            # tokens + UI primitives + plotly layout helpers
  data/
    gabriel_data.csv    # reference dataset
    cardiac_data.csv    # auto-generated at runtime
  esp32/
    esp32_max30100.ino  # firmware sketch
```
