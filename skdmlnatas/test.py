import database

for i in range(5, 10):
    database.DeepDatabase.make_train_data(i)
    database.DeepDatabase.make_test_data(40+i)
    
    database.DataDB.insert_train_result()