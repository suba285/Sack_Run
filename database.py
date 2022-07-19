from firebase import firebase

# this is not being used because of an error, for which I see no fix

firebase = firebase.FirebaseApplication('https://database-test-82326-default-rtdb.europe-west1.firebasedatabase.app/',
                                        None)
data = {
    'nickname':'suba',
    'score':'98'
}

result = firebase.post('database-test-82326-default-rtdb/Player', data)