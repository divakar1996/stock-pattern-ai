# Define your CNN/LSTM model here
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical

def load_dataset(dataset_folder="data/datasets"):
    """
    Load preprocessed training and testing datasets.
    """
    X_train = np.load(os.path.join(dataset_folder, "X_train.npy"))
    y_train = np.load(os.path.join(dataset_folder, "y_train.npy"))
    X_test = np.load(os.path.join(dataset_folder, "X_test.npy"))
    y_test = np.load(os.path.join(dataset_folder, "y_test.npy"))

    # Reshape inputs for LSTM: (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # One-hot encode the labels
    y_train = to_categorical(y_train, num_classes=3)
    y_test = to_categorical(y_test, num_classes=3)

    return X_train, y_train, X_test, y_test

def build_model(input_shape):
    """
    Define the LSTM model architecture.
    """
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(32))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='softmax'))  # 3 classes: No pattern, Double Bottom, Double Top

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(output_folder="models"):
    """
    Train the model and save it.
    """
    os.makedirs(output_folder, exist_ok=True)

    X_train, y_train, X_test, y_test = load_dataset()

    model = build_model(input_shape=(X_train.shape[1], 1))

    checkpoint = ModelCheckpoint(
        filepath=os.path.join(output_folder, "pattern_model.h5"),
        save_best_only=True,
        monitor="val_accuracy",
        mode="max",
        verbose=1
    )

    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=30,
        batch_size=32,
        callbacks=[checkpoint]
    )

    print("✅ Training complete. Best model saved!")

if __name__ == "__main__":
    train_model()
