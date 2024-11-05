import bcrypt
password = " "
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Store `hashed_password` securely in your Python file
print(hashed_password)  # Save this value in your file