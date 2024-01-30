import sqlite3
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping


con = sqlite3.connect('game_results.sqlite')
cursor_db = con.cursor()
cursor_db.execute('SELECT * FROM games')
data = cursor_db.fetchall()
    

dat = [[],[],[],[]]
for i, st in enumerate(data):
    dat[0].append(st[0].split(', '))
    dat[2].append(st[2].split(', '))
    dat[1].append(st[1])
    dat[3].append(st[3])


train_data = np.array([list(map(int, i)) for i in dat[0]])
train_label = np.array(dat[1]).reshape(-1,1)
test_data = np.array([list(map(int, i)) for i in dat[2]])
test_label = np.array(dat[3]).reshape(-1,1)


# 데이터 정규화
scaler = StandardScaler()
train_data_normalized = scaler.fit_transform(train_data)
test_data_normalized = scaler.transform(test_data)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=128, input_shape=(10,), activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=32, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=32, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=16, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=16, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Dropout 추가
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Early Stopping 추가
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Train the model
model.fit(np.array(train_data_normalized), np.array(train_label), 
          batch_size=100, epochs=100, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(np.array(test_data_normalized), np.array(test_label))

# Print the test loss and accuracy
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)