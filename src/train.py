import argparse, os, json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from src.utils import ensure_dir, save_labels

def build_model(img_size, num_classes, freeze_layers):
    base = tf.keras.applications.MobileNetV2(
        include_top=False, input_shape=(img_size, img_size, 3), weights='imagenet', pooling='avg'
    )
    for i, layer in enumerate(base.layers):
        layer.trainable = (i >= freeze_layers)
    x = layers.Dropout(0.2)(base.output)
    out = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(inputs=base.input, outputs=out)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main(args):
    ensure_dir('artifacts'); ensure_dir('docs/images')

    datagen = ImageDataGenerator(
        rescale=1./255, validation_split=0.2,
        rotation_range=25, width_shift_range=0.1, height_shift_range=0.1,
        zoom_range=0.15, horizontal_flip=True
    )
    train = datagen.flow_from_directory(
        args.data_dir, target_size=(args.img_size, args.img_size),
        batch_size=args.batch, class_mode='categorical', subset='training'
    )
    val = datagen.flow_from_directory(
        args.data_dir, target_size=(args.img_size, args.img_size),
        batch_size=args.batch, class_mode='categorical', subset='validation', shuffle=False
    )

    model = build_model(args.img_size, train.num_classes, args.freeze)
    cb = [tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss', restore_best_weights=True)]
    hist = model.fit(train, validation_data=val, epochs=args.epochs, callbacks=cb)

    # Save model + labels
    model.save(args.model_out)
    inv = {v:k for k,v in train.class_indices.items()}
    save_labels(inv, 'artifacts/labels.json')

    # Curves
    plt.figure(); plt.plot(hist.history['loss']); plt.plot(hist.history['val_loss']); plt.title('Loss'); plt.legend(['train','val']); plt.savefig('docs/images/loss.png', dpi=160)
    plt.figure(); plt.plot(hist.history['accuracy']); plt.plot(hist.history['val_accuracy']); plt.title('Accuracy'); plt.legend(['train','val']); plt.savefig('docs/images/acc.png', dpi=160)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--img_size", type=int, default=224)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--freeze", type=int, default=100, help="freeze first N layers")
    ap.add_argument("--model_out", default="artifacts/model.h5")
    main(ap.parse_args())
