import pyrebase

firebase_config = {
    "apiKey": "AIzaSyD5CjGek01W12xbFETXZCXq1ZPnPSfpvQg",
    "authDomain": "test-a7864.firebaseapp.com",
    "databaseURL": "https://test-a7864-default-rtdb.firebaseio.com",
    "projectId": "test-a7864",
    "storageBucket": "test-a7864.appspot.com",
    "messagingSenderId": "594427297963",
    "appId": "1:594427297963:web:c9d519dbb6228bc63b37ee",
    "measurementId": "G-Q5NWN9QS2K"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
