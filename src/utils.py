import os, json, numpy as np, cv2

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_labels(mapping, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)

def load_labels(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def preprocess_frame(frame, img_size):
    img = cv2.resize(frame, (img_size, img_size))
    img = img[:, :, ::-1]  # BGR->RGB
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)
