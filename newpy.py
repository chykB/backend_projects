# import mysql.connector

# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "chykab",
#     password = "Useraccount82#",
#     database = "users"
# )

# # print(mydb.get_server_info())
# if mydb.is_connected():
#     print("Connected to the database")

# cursor = mydb.cursor()
# # cursor.execute("""CREATE TABLE IF NOT EXISTS books (
# #                id INT AUTO_INCREMENT PRIMARY KEY, 
# #                title VARCHAR(255), 
# #                author VARCHAR(255), 
# #                year INT)"""
# # )
# query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
# values = ("To Kill a Mockingbird", "Harper Lee", 1960)
# cursor.execute(query, values)
# mydb.commit()  # Commit the transaction
# print(f"{cursor.rowcount} record inserted.")


# query = "SELECT * FROM books"
# cursor.execute(query)
# result = cursor.fetchall()
# for row in result:
#     print(row)

# query = "UPDATE books SET year = %s WHERE title = %s"
# values = (1861, "To Kill a Mockingbird")
# cursor.execute(query, values)
# mydb.commit()
# print(f"{cursor.rowcount} record updated.")


# query = "DELETE FROM books WHERE title = %s"
# values = ("To Kill a Mockingbird",)
# cursor.execute(query, values)
# mydb.commit()
# print(f"{cursor.rowcount} record deleted.")



# query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
# values = ("To Kill a Mockingbird", "Harper Lee", 1960)
# cursor.execute(query, values)
# mydb.commit()  # Commit the transaction
# print(f"{cursor.rowcount} record inserted.")


import mysql.connector


mydb = mysql.connector.connect(
            host="localhost",
            user="chykab",
            password="Useraccount82#",
            database="users"
        )

if mydb.is_connected():
    print("Connected to the database")

cursor = mydb.cursor()

# def insert_book(title, author, year):
#     """Insert a book record into the database."""
#     query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
#     values = (title, author, year)
#     cursor = mydb.cursor()
#     cursor.execute(query, values)
#     mydb.commit()
#     print(f"{cursor.rowcount} record inserted.")
#     cursor.close()

# insert_book("Kill a Mockingbirds", "Harper Lee", 1960)

def fetch_books():
    """Fetch all book records from the database."""
    query = "SELECT * FROM books"
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()

fetch_books()

# def update_book_year(title, year):
#     """Update the year of a book record in the database."""
#     query = "UPDATE books SET year = %s WHERE title = %s"
#     values = (year, title)
#     cursor = mydb.cursor()
#     cursor.execute(query, values)
#     mydb.commit()
#     print(f"{cursor.rowcount} record updated.")
#     cursor.close()

# update_book_year("To Kill a Mockingbird", 2025)

def delete_book(title):
    """Delete a book record from the database."""
    query = "DELETE FROM books WHERE title = %s"
    values = (title,)
    cursor = mydb.cursor()
    cursor.execute(query, values)
    mydb.commit()
    print(f"{cursor.rowcount} record deleted.")
    cursor.close()
delete_book("To Kill a Mockingbirds")
    