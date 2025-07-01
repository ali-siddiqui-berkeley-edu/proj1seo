
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyBf53CUWRRNthllOeQYHLa3oTnqc1FEvac",
    "authDomain": "seoproj1.firebaseapp.com",
    "databaseURL": "https://seoproj1.firebaseio.com",
    "storageBucket": "seoproj1.firebasestorage.app"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()


def login():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Logged in successfully into Firebase Firestore API.")
        return user
    except Exception as e:
        print("Login failed:", e)
        return None

def main():
  

    user = login()

    if user:
        print("User is logged in.")

        ##### now add code for DogAPI here (inside this block of code!) thx
        ####
        ####
        #####
        import requests
        url= 'https://api.thedogapi.com/v1/images/search'
        headers= {'x-api-key':'live_lYvNHFVb44Md9LN8D7kNtzPWtOdZrfhqrLG15u3gdZwgG0JOOb3V7ZNK6srMwZnS'}
        response= requests.get (url, headers)
        data=response.json()
        print (data)

    
    else:
        print("Not logged in. Sorry no dog pics until you log in!")

if __name__ == "__main__":
    main()
