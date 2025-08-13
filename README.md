# Automated Waste Classification & Segregation (AI + Arduino)

A complete reference implementation for an automated waste segregation system that uses a **CNN model** for image-based classification (plastic, metal, paper, glass, biodegradable, etc.) and an **Arduino** (with a **KY-036 metal touch sensor**) to actuate sorting into bins.

> Built with Python (TensorFlow/Keras + OpenCV) and Arduino (C++).

![System Overview](docs/images/overview.png)

## Features
- End-to-end project: data prep → training → real-time inference → Arduino actuation.
- Uses **Garbage Classification V2 (Kaggle)** for training (or plug in your own).
- Real-time webcam inference with overlay.
- Serial bridge to send `P/M/B/...` to Arduino.
- Arduino sketch with servo-based diverters + KY-036 for metal detection.
- Clean documentation and reproducible `requirements.txt`.

## Quick Start
```bash
# 1) Setup environment
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Prepare dataset
# Download Garbage Classification V2 from Kaggle and extract to data/raw/
# Expected structure: data/raw/<class_name>/*.jpg

# 3) Train
python src/train.py --data_dir data/raw --img_size 128 --epochs 15 --model_out models/waste_classifier.h5

# 4) Test inference (webcam)
python src/infer.py --model models/waste_classifier.h5 --labels data/labels.json

# 5) Send classifications to Arduino
python src/serial_bridge.py --port COM3 --baud 9600
```

## Hardware
- **Arduino Uno/Nano**
- **KY-036 metal touch sensor** (for metal confirmation)
- SG90/MG995 servos for chute/diverters
- Optional: conveyor/DC motor + driver (L298N)
- 5V regulated supply

![Hardware Flow](docs/images/hardware_flow.png)

## Repository Layout
```
waste-segregator-ai-arduino/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── raw/                 # Place Kaggle dataset here
│   └── labels.json          # Auto-generated after training
├── models/                  # Saved models
├── notebooks/               # Optional exploration
├── src/
│   ├── train.py
│   ├── infer.py
│   ├── serial_bridge.py
│   └── utils.py
├── arduino/
│   └── WasteSorter/WasteSorter.ino
└── docs/
    ├── README.md
    ├── architecture.md
    └── images/
        ├── overview.png
        ├── pipeline.png
        ├── hardware_flow.png
        └── demo_ui.png
```

## Dataset
This repo expects the **Garbage Classification V2** dataset from Kaggle. Download and extract into `data/raw/`. You can also modify class names in `src/train.py` if using a different dataset.

## Results
- Training and validation curves are saved in `docs/images/`.
- Confusion matrix is auto-saved after evaluation.
- Example overlays in `docs/images/demo_ui.png`.

## License
[MIT](LICENSE)

## Acknowledgements
- Kaggle contributors for the dataset
- Open-source communities: TensorFlow, OpenCV, Arduino
