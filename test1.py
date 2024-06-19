from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2


app = FastAPI()
data = []

db_nme= "apitest"
db_user="postgres"
db_pass="root"
db_host="localhost"
db_port="5432"


conn = psycopg2.connect(database=db_nme, user=db_user, password=db_pass, host=db_host, port=db_port)
#cur = conn.cursor()

class Book(BaseModel):
    title :str
    author: str
    publisher:str

@app.post("/books")
def create_book(book:Book):
    data.append(book.dict())
    cursor = conn.cursor()
    insert_query = "INSERT INTO book (title, author, publisher) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (book.title, book.author, book.publisher))
    conn.commit()
    cursor.close()

    return book

@app.get("/{title}}")
def read_books(title:str):
    cursor = conn.cursor()
    select_query = "SELECT title, author, publisher FROM book WHERE title = %s"
    cursor.execute(select_query, (title,))
    book = cursor.fetchone()
    cursor.close()
    if book:
        return book
    else:
        return {"message": "Book not found"}

   
    
@app.put("/{title}}")
def update_book(title:str,book:Book):
    cursor = conn.cursor()
    update_query = "UPDATE book SET title = %s, author = %s, publisher = %s WHERE title = %s"
    cursor.execute(update_query, (book.title, book.author, book.publisher, title))
    conn.commit()
    cursor.close()
    
    return ({"message": "Book updated successfully"})

@app.delete("/{title}}")    
def delete_book(title:str): 
    cursor = conn.cursor()
    delete_query = "DELETE FROM book WHERE title = %s"
    cursor.execute(delete_query, (title,))
    conn.commit()
    cursor.close()

    return ({"message": "Book deleted successfully"})
    