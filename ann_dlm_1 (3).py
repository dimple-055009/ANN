# -*- coding: utf-8 -*-
"""ANN_DLM-1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yj2hy6ToAO8tC4WjPfZt-qFI6GtO033S
"""

!pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Set Streamlit page configuration
st.set_page_config(page_title="Customer Churn Prediction", layout="wide")
st.title("Customer Churn Prediction using ANN")

# Load dataset from Git
git_file_path = "ANN/Telco_customer_churn.xlsx"
df = pd.read_excel(git_file_path)

# Preprocess categorical features
df = df.apply(lambda col: LabelEncoder().fit_transform(col.astype(str)) if col.dtype == 'object' else col)

# Define features and target
X = df.drop(columns=['Churn Label', 'Churn Value', 'Churn Score', 'CLTV', 'Churn Reason'], errors='ignore')
y = df['Churn Value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Sidebar for hyperparameter selection
st.sidebar.header("Hyperparameter Selection")
learning_rate = st.sidebar.slider("Learning Rate", 0.001, 0.1, 0.01, 0.001)
batch_size = st.sidebar.slider("Batch Size", 16, 128, 32, 16)
dense_layers = st.sidebar.radio("Number of Dense Layers", [3, 4])
epochs = st.sidebar.slider("Epochs", 10, 100, 50, 10)
dropout_rate = st.sidebar.slider("Dropout Rate", 0.0, 0.5, 0.2, 0.05)
activation_function = st.sidebar.selectbox("Activation Function", ["relu", "tanh", "sigmoid"])

def build_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(X_train.shape[1],)))
    for _ in range(dense_layers):
        model.add(tf.keras.layers.Dense(64, activation=activation_function))
        model.add(tf.keras.layers.Dropout(dropout_rate))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

# Train model
model = build_model()
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, verbose=1)

# Ensure matplotlib runs interactively
plt.switch_backend('Agg')

# Improved visualizations with vibrant aesthetics
st.write("## Training Performance")
col1, col2 = st.columns(2)

with col1:
    st.write("### Loss Over Epochs")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(x=range(1, epochs + 1), y=history.history['loss'], label='Train Loss', ax=ax, color='crimson')
    sns.lineplot(x=range(1, epochs + 1), y=history.history['val_loss'], label='Validation Loss', ax=ax, color='royalblue')
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Loss")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.write("### Accuracy Over Epochs")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(x=range(1, epochs + 1), y=history.history['accuracy'], label='Train Accuracy', ax=ax, color='darkorange')
    sns.lineplot(x=range(1, epochs + 1), y=history.history['val_accuracy'], label='Validation Accuracy', ax=ax, color='mediumseagreen')
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Accuracy")
    ax.legend()
    st.pyplot(fig)

# Churn Analysis
st.write("## Churn Distribution Analysis")
fig, ax = plt.subplots(figsize=(12, 8))
sns.histplot(y, bins=2, kde=True, ax=ax, color='deepskyblue')
ax.set_title("Churn Distribution", fontsize=16)
ax.set_xticks([0, 1])
ax.set_xticklabels(["No Churn", "Churn"], fontsize=14)
st.pyplot(fig)

st.write("## Feature Importance")
from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)
feature_importance = pd.Series(abs(lr_model.coef_[0]), index=X.columns).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x=feature_importance.values, y=feature_importance.index, ax=ax, palette="magma")
ax.set_title("Feature Importance (Approximation)", fontsize=16)
st.pyplot(fig)