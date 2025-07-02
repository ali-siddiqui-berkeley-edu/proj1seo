import sqlite3
import requests
import random



def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



def create_account():
    email = input("Choose your email: ").strip()
    password = input("Choose your password: ").strip()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        print("Account created successfully! Logged in!")
        loggedIn()
    except sqlite3.IntegrityError:
        print("An account with that email already exists.")
    finally:
        conn.close()


def login():
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchone()

    conn.close()

    if result:
        loggedIn()

    else:
        print("Invalid email or password. Please run the program again.")


def loggedIn():
    print("Login successful!")
    # Call Dog API

    url = "https://api.thedogapi.com/v1/images/search"
    headers = {
        'x-api-key': 'live_lYvNHFVb44Md9LN8D7kNtzPWtOdZrfhqrLG15u3gdZwgG0JOOb3V7ZNK6srMwZnS'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            dog_image_url = data[0]['url']
            print(f"Click here for your dog image: {dog_image_url}")
        else:
            print("No dog image found.")
    else:
        print("Failed to fetch dog image.")



CLIENT_ID = "BK09a99NhuhirWVIbgR3Svy20vdWyKEvsMRW237GtqatDkUvPe"
CLIENT_SECRET = "IRpnquDucc1o8dkaJwZzVvQYcixJ6OY9S2O9JtWV"

def get_access_token():
    url = "https://api.petfinder.com/v2/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def find_local_dog(location="10001", distance=50):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "type": "dog",
        "location": location,
        "distance": distance,
        "limit": 10,
        "sort": "random"
    }

    url = "https://api.petfinder.com/v2/animals"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    dogs = response.json().get("animals", [])

    if not dogs:
        print("No dogs found nearby.")
        return

    dog = random.choice(dogs)  # pick one random dog
    name = dog.get("name", "Unknown")
    desc = dog.get("description", "No description available.")
    link = dog.get("url", "No link provided.")

    print(f"\nWe found you a dog in your area! Meet {name}!\n")
    print(f"---{desc}\n")
    print(f"---Learn more: {link}")



def main():
    setup_db()

    print("Welcome! Please choose an option:")
    print("1. Log in")
    print("2. Create a new account")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        login()
        zipCode = input("Enter your zip code to find dogs in your area!: ")
        find_local_dog(zipCode)
    elif choice == "2":
        create_account()
    else:
        print("Invalid choice. Please run the program again.")


if __name__ == "__main__":
    main()


