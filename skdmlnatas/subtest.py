import sqlite3
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


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

def vectorize_sequences(sequences, dimention = 163):
    results = np.zeros((len(sequences), dimention))
    for i, sequences in enumerate(sequences):
        for j in sequences:
            results[i, j] = 1.
    return results


train_data = [list(map(int, i)) for i in dat[0]]
train_label = dat[1]
test_data = [list(map(int, i)) for i in dat[2]]
test_label = dat[3]

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)
y_train = np.asarray(train_label).astype("float32")
y_test = np.asarray(test_label).astype("float32")


model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=32, activation='relu', input_shape=(163,)),
    tf.keras.layers.Dense(units=16, activation='relu'),
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

x_val = x_train[:500]
partial_x_train = x_train[500:]
y_val = y_train[:500]
partial_y_train = y_train[500:]

history = model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=256, validation_batch_size=(x_val, y_val))

history_dict = history.history
loss_values = history_dict["loss"]
val_loss_values=history_dict["val_loss"]
epochs = range(1, len(loss_values) + 1)
plt.plot(epochs, loss_values, "bo", label="Traning loss")
plt.plot(epochs, val_loss_values, 'b', label = "Validatioin loss")
plt.title("Training and validation loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()