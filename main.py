import tkinter as tk
from tkinter import ttk
import sqlite3
from functions import create_tab1_content, create_tab2_content, create_tab3_content, create_tab4_content, display_selected_data
from functions import add_schools_and_races, add_teams, add_athletes, add_race_details
from view_data import load_athletes_listbox
from functions import create_table, display_results, load_athletes_listbox, convert_race_time, read_csv, upload_csv, update_dropdown_menu, display_top_25, calculate_and_display_team_scores, calculate_team_score

selected_data_var = None

root = tk.Tk()
root.title("Tabbed GUI")

# Connect to your SQLite database (replace 'your_database.db' with your actual database file)
with sqlite3.connect('crosscountry_match.db') as connection:
    cursor = connection.cursor()
    # Rest of your code

# Create a notebook (tabs container)
notebook = ttk.Notebook(root)

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Add to Database")
notebook.add(tab2, text="View Data")
notebook.add(tab3, text="Team Scores")
notebook.add(tab4, text="Top 25 Athletes")

# Pack the notebook to make it visible
notebook.pack(expand=True, fill="both")

# Add content to each tab initially
create_tab1_content(tab1)
create_tab2_content(tab2)
create_tab3_content(tab3)
create_tab4_content(tab4)

# Run the main loop
root.mainloop()
