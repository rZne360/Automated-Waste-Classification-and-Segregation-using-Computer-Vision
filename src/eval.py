import argparse, numpy as np, matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from src.utils import ensure_dir

def main(args):
    ensure_dir('docs/images')
    model = tf.keras.models.load_model(args.model)

    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    val = datagen.flow_from_directory(
        args.data_dir, target_size=(args.img_size, args.img_size),
        batch_size=args.batch, class_mode='categorical', subset='validation', shuffle=False
    )

    preds = model.predict(val)
    y_true = val.classes
    y_pred = np.argmax(preds, axis=1)
    labels = list(val.class_indices.keys())

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(xticks_rotation=45)
    plt.title("Validation Confusion Matrix")
    plt.tight_layout()
    plt.savefig("docs/images/confusion_matrix.png", dpi=160)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--img_size", type=int, default=224)
    ap.add_argument("--batch", type=int, default=32)
    main(ap.parse_args())
