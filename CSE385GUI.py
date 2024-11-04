import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


class CustomerTable:
    def __init__(self, root):
        self.root = root
        self.root.title("City Data")

        # creating main window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # create frame for table
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # treeview for cols
        columns = ('ID', 'Name', 'Country Code', 'District', 'Population')
        self.table = ttk.Treeview(frame, columns=columns, show='headings')

        # col heading widths
        column_widths = {
            'ID': 100,
            'Name': 150,
            'Country Code': 100,
            'District': 150,
            'Population': 100
        }
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=column_widths[col])

        # scrollbars
        x_scrollbar = ttk.Scrollbar(frame, orient='horizontal', command=self.table.xview)
        y_scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.table.yview)
        self.table.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        # grid design
        self.table.grid(row=0, column=0, sticky='nsew')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')

        # frame grid weights
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # load
        self.load_data()

    def database_connection(self):
        try:
            print("Attempting to connect to database...")
            connection = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='reesewej',  # Replace with your password
                database='world'
            )
            if connection.is_connected():
                print("Successfully connected to database!")
            return connection
        except Error as e:
            print(f"Connection error: {e}")
            messagebox.showerror("Connection Error", 
                f"Error connecting to MySQL database: {e}")
            return None

    def load_data(self):
        
        
        connection = self.database_connection()
        
        if not connection:
            print("No connection available")
            return
            
        try:
            
            cursor = connection.cursor()
            
            ## select query
            cursor.execute("SELECT * FROM city;")  # First test with limit
            
            ## gets all rows
            rows = cursor.fetchall()
            
            
            # Clear existing items
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Load new data
            
            for row in rows:
                self.table.insert('', 'end', values=(
                    row[0],  # ID
                    row[1],  # Name
                    row[2],  # Country Code
                    row[3],  # District
                    f"{row[4]:,}"  # Population with comma formatting
                ))
            
           
            cursor.close()
            connection.close()
            
            
        except Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error")
        except Exception as e:
            print(f"General error: {e}")
            messagebox.showerror("Error", 
                f"An unexpected error occurred: {e}")


def main():
    root = tk.Tk()
    root.geometry("1000x600")
    app = CustomerTable(root)
    root.mainloop()

if __name__ == "__main__":
    main()
