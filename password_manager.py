import mysql.connector
from getpass import getpass
from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
def generate_key():
    return Fernet.generate_key()

# Function to encrypt the password
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Function to decrypt the password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="khusmysql77Aa$%",
        database="password_manager"
    )

# Function to add a new password entry
def add_password(service, username, password, notes):
    key = generate_key()
    encrypted_password = encrypt_password(password, key)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password, notes, encryption_key) VALUES (%s, %s, %s, %s, %s)", 
                   (service, username, encrypted_password, notes, key))
    conn.commit()
    cursor.close()
    conn.close()
    print("Password added successfully!")

# Function to retrieve passwords
def retrieve_passwords():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords")
    for (id, service, username, encrypted_password, notes, key) in cursor.fetchall():
        decrypted_password = decrypt_password(encrypted_password, key)
        print(f"Service: {service}, Username: {username}, Password: {decrypted_password}, Notes: {notes}")
    cursor.close()
    conn.close()

# Function to update a password entry
def update_password(id, new_password):
    key = generate_key()
    encrypted_password = encrypt_password(new_password, key)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET password = %s, encryption_key = %s WHERE id = %s", (encrypted_password, key, id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Password updated successfully!")

# Function to delete a password entry
def delete_password(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Password deleted successfully!")

# Main function to interact with the user
def main():
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Passwords")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            service = input("Service Name: ")
            username = input("Username: ")
            password = getpass("Password: ")
            notes = input("Notes (optional): ")
            add_password(service, username, password, notes)
        
        elif choice == "2":
            retrieve_passwords()
        
        elif choice == "3":
            id = input("Enter the ID of the password to update: ")
            new_password = getpass("New Password: ")
            update_password(id, new_password)
        
        elif choice == "4":
            id = input("Enter the ID of the password to delete: ")
            delete_password(id)
        
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
