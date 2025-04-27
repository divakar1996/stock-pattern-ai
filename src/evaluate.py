import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

def load_dataset(dataset_folder="data/datasets"):
    """
    Load preprocessed datasets.
    """
    X_test = np.load(os.path.join(dataset_folder, "X_test.npy"))
    y_test = np.load(os.path.join(dataset_folder, "y_test.npy"))

    # Reshape the input for LSTM model (samples, timesteps, features)
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # One-hot encode the labels for evaluation
    y_test = to_categorical(y_test, num_classes=3)

    return X_test, y_test

def evaluate_model(model_path="models/pattern_model.h5"):
    """
    Evaluate the model on test data and print classification metrics.
    """
    # Load the saved model
    model = load_model(model_path)

    # Load the test dataset
    X_test, y_test = load_dataset()

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"Model Loss: {loss:.4f}")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Predict on test data
    y_pred = model.predict(X_test)

    # Get the predicted labels by taking the index of the max probability (argmax)
    y_pred_labels = np.argmax(y_pred, axis=1)
    y_true_labels = np.argmax(y_test, axis=1)

    # Print Classification Report only if there are multiple classes predicted
    unique_classes = np.unique(y_pred_labels)
    if len(unique_classes) > 1:
        print("\nClassification Report:")
        print(classification_report(y_true_labels, y_pred_labels, target_names=["No Pattern", "Double Bottom", "Double Top"]))
    else:
        print("\nWarning: Only one class was predicted. Classification report not applicable.")

    # Plot Confusion Matrix
    cm = confusion_matrix(y_true_labels, y_pred_labels)
    plot_confusion_matrix(cm)

def plot_confusion_matrix(cm, labels=["No Pattern", "Double Bottom", "Double Top"]):
    """
    Plot confusion matrix.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(cm, cmap='Blues')
    fig.colorbar(cax)
    
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')

    for i in range(len(cm)):
        for j in range(len(cm[i])):
            ax.text(j, i, str(cm[i][j]), va='center', ha='center', color="red")

    plt.show()

if __name__ == "__main__":
    evaluate_model()
