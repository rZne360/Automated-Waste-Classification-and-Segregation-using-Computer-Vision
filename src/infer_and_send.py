import argparse, json, time, cv2, serial, numpy as np, tensorflow as tf
from src.utils import preprocess_frame

CODE_MAP = {"paper":"1", "plastic":"2", "metal":"3"}

def main(args):
    model = tf.keras.models.load_model(args.model)
    with open(args.labels, "r") as f:
        labels = json.load(f)
    labels = {int(k): v for k, v in labels.items()}

    ser = serial.Serial(args.port, args.baud, timeout=0.1)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No camera found"); return

    last_code = "0"
    next_send_time = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret: break

            X = preprocess_frame(frame, args.img_size)
            probs = model.predict(X, verbose=0)[0]
            idx = int(np.argmax(probs))
            label = labels[idx]
            conf = float(np.max(probs))
            code = CODE_MAP.get(label, "0")

            # Overlay
            cv2.putText(frame, f"{label} ({conf:.2f}) -> code {code}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
            cv2.imshow("Waste Classifier (press q to quit)", frame)

            t = time.time()
            if t >= next_send_time and code != last_code:
                ser.write((code + "\n").encode())
                last_code = code
                next_send_time = t + args.interval

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release(); cv2.destroyAllWindows(); ser.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--port", required=True)
    ap.add_argument("--baud", type=int, default=9600)
    ap.add_argument("--img_size", type=int, default=224)
    ap.add_argument("--interval", type=float, default=2.0)
    main(ap.parse_args())
