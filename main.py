import tkinter as tk
from tkinter import ttk
import sqlite3
from app.functions import create_tab1_content, create_tab4_content, display_selected_data
from app.functions import add_schools_and_races, add_teams, add_athletes, add_race_details
from app.view_data import load_athletes_listbox
from app.functions import create_table, display_results, load_athletes_listbox, convert_race_time, read_csv, upload_csv, update_dropdown_menu, display_top_25, calculate_and_display_team_scores, calculate_team_score

selected_data_var = None

def main():
    root = tk.Tk()
    root.title("Middle School State XC Calculator")
    root.geometry("800x600")

    # Connect to your SQLite database (replace 'your_database.db' with your actual database file)
    with sqlite3.connect('crosscountry_match.db') as connection:
        cursor = connection.cursor()

    # Create a notebook (tabs container)
    notebook = ttk.Notebook(root)

    # Create tabs
    tab1 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)

    # Add tabs to the notebook
    notebook.add(tab1, text="Add to Database")
    notebook.add(tab4, text="Race Data & Scores")

    # Pack the notebook to make it visible
    notebook.pack(expand=True, fill="both")

    # Add content to each tab initially
    create_tab1_content(tab1)
    create_tab4_content(tab4)

    # Run the main loop
    root.mainloop()

# Call the main function if this script is executed
if __name__ == "__main__":
    main()