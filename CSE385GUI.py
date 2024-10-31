import tkinter as tk
from tkinter import ttk
import csv
from pathlib import Path


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
        self.load_csv_data()

    def load_csv_data(self):
        try:
            path = Path('assignment3.csv')

            with open(path, 'r') as file:
                # semicolon as delimeter
                csv_reader = csv.reader(file, delimiter=';', quotechar='"')
                next(csv_reader)  # skip header row
                
                # loading data
                for row in csv_reader:
                    if len(row) >= 5:
                        # remove quotes
                        cleaned_row = [field.strip('"') for field in row]
                        
                        # pop format with commas 
                        try:
                            population = f"{int(cleaned_row[4]):,}"
                        except ValueError:
                            population = cleaned_row[4]
                            
                        self.table.insert('', 'end', values=(
                            cleaned_row[0],  # ID
                            cleaned_row[1],  # Name
                            cleaned_row[2],  # Country Code
                            cleaned_row[3],  # District
                            population       # pop
                        ))
                    else:
                        print(f"Skipping invalid row: {row}")

        except FileNotFoundError:
            print("File 'assignment3.csv' not found")
        except Exception as e:
            print(f"Error loading: {e}")


def main():
    root = tk.Tk()
    root.geometry("1000x600")  
    app = CustomerTable(root)
    root.mainloop()

if __name__ == "__main__":
    main()