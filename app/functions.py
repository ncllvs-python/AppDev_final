from tkinter import ttk
import tkinter as tk
import pandas as pd
import csv
import sqlite3
from tkinter import filedialog, messagebox, simpledialog

# Set display options for Pandas
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Display full width

# Declare global variables
result_display = None
data_dict = {}
selected_data_var = None
file_type_menu = None

def create_table():
    connection = sqlite3.connect('crosscountry_match.db')
    cursor = connection.cursor()
    try:
        # Create the race_detail table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS race_detail (
                athlete_id INTEGER,
                race_id INTEGER,
                PRIMARY KEY (athlete_id, race_id),
                FOREIGN KEY (athlete_id) REFERENCES athletes (id),
                FOREIGN KEY (race_id) REFERENCES races (id)
            )
        ''')
        connection.commit()
        print("race_detail table created or already exists.")
    except Exception as e:
        print(f"Error creating race_detail table: {e}")
    finally:
        connection.close()

def display_results(data, action):
    global result_display  # Access the global result_display variable

    # Clear the existing Treeview
    for child in result_display.get_children():
        result_display.delete(child)

    if action == "Top_25":
        display_top_25(data)
    elif action == "Team_Scores":
        calculate_and_display_team_scores(data)
    else:
        # Set unique identifiers for Treeview columns
        col_identifiers = [f"col_{i}" for i in range(len(data.columns))]

        result_display['columns'] = col_identifiers
        result_display.heading('#0', text='Index')

        for col, col_id in zip(data.columns, col_identifiers):
            result_display.heading(col_id, text=col)
            result_display.column(col_id, anchor=tk.CENTER, width=100)

        for index, row in data.iterrows():
            result_display.insert('', tk.END, text=index, values=list(row))


def add_teams():
    # Ask user to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        try:
            # Read data from CSV file
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                teams_data = [row[" Team"] for row in csv_reader]

            # Connect to SQLite database
            conn = sqlite3.connect("crosscountry_match.db")
            cursor = conn.cursor()

            # Create Teams table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_name TEXT
                )
            ''')

            # Insert data into Teams table
            for team_name in teams_data:
                cursor.execute("INSERT INTO teams (team_name) VALUES (?)", (team_name,))

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Teams added successfully")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def add_race_details():
    connection = sqlite3.connect('crosscountry_match.db')
    cursor = connection.cursor()
    try:
        # Fetch existing athlete IDs
        cursor.execute("SELECT id FROM athletes")
        athlete_ids = [row[0] for row in cursor.fetchall()]

        # Fetch existing race IDs
        cursor.execute("SELECT id FROM races")
        race_ids = [row[0] for row in cursor.fetchall()]

        # Determine the total number of rows
        total_rows = max(len(athlete_ids), len(race_ids))

        # Insert athlete and race details in the same row
        cursor.executemany("INSERT INTO race_detail (athlete_id, race_id) VALUES (?, ?)",
                           zip(athlete_ids + [None] * (total_rows - len(athlete_ids)),
                               race_ids + [None] * (total_rows - len(race_ids))))

        connection.commit()
        print("Race details added to the database.")
    except Exception as e:
        print(f"Error adding race details: {e}")
    finally:
        connection.close()

def add_schools_and_races():
    # Ask user to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        try:
            # Read data from CSV file
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                data = list(csv_reader)

            # Connect to SQLite database
            conn = sqlite3.connect("crosscountry_match.db")
            cursor = conn.cursor()

            # Create Schools table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_name TEXT
                )
            ''')

            # Create Races table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS races (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    race_name TEXT
                )
            ''')

            # Insert data into Schools and Races tables
            for row in data:
                school_name = row.get("School Name")
                race_name = row.get(" Race Name")

                if school_name:
                    cursor.execute("INSERT INTO schools (school_name) VALUES (?)", (school_name,))

                if race_name:
                    cursor.execute("INSERT INTO races (race_name) VALUES (?)", (race_name,))

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Schools and Races added successfully")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def add_athletes():
    # Ask user to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        try:
            # Read data from CSV file
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                athletes_data = list(csv_reader)

            # Connect to SQLite database
            conn = sqlite3.connect("crosscountry_match.db")
            cursor = conn.cursor()

            # Prompt user for gender
            gender = simpledialog.askstring("Gender", "Enter gender (Male/Female):").capitalize()

            # Create Athletes table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS athletes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    team_id INTEGER,
                    gender TEXT,
                    FOREIGN KEY (team_id) REFERENCES teams (id)
                )
            ''')

            # Insert data into Athletes table
            for athlete in athletes_data:
                # Get team_id based on team_name
                cursor.execute("SELECT id FROM teams WHERE team_name = ?", (athlete[" Team"],))
                team_id = cursor.fetchone()

                if team_id:
                    team_id = team_id[0]

                    # Insert athlete data into Athletes table
                    cursor.execute("""
                        INSERT INTO athletes (first_name, last_name, team_id, gender)
                        VALUES (?, ?, ?, ?)
                    """, (athlete[" First Name"], athlete["Last Name"], team_id, gender))
                else:
                    messagebox.showwarning("Warning", f"Team '{athlete[' Team']}' not found in the database.")

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Athletes added successfully")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def create_tab1_content(tab1):
    # Create a frame for the content of Tab 1
    tab1_frame = ttk.Frame(tab1)
    tab1_frame.pack(expand=True, fill="both")

    # Add Teams Button
    add_teams_button = tk.Button(tab1_frame, text="Add Teams", command=add_teams)
    add_teams_button.pack(pady=10)

    # Add Race Detail Button with create_table function
    add_race_detail_button = tk.Button(tab1_frame, text="Add Race Detail",
                                       command=lambda: [create_table(), add_race_details()])
    add_race_detail_button.pack(pady=10)

    # Add Schools and Races Button
    add_schools_and_races_button = tk.Button(tab1_frame, text="Add Schools and Races", command=add_schools_and_races)
    add_schools_and_races_button.pack(pady=10)

    # Add Athletes Button
    add_athletes_button = tk.Button(tab1_frame, text="Add Athletes", command=add_athletes)
    add_athletes_button.pack(pady=10)



def create_tab4_content(tab4):
    # Create a frame for the content of Tab 4
    tab4_frame = ttk.Frame(tab4)
    tab4_frame.pack(expand=True, fill="both")

    # Upload CSV Button
    upload_button = tk.Button(tab4_frame, text="Upload CSV", command=upload_csv)
    upload_button.pack(pady=10)

    # Initialize selected_data_var as a global variable
    global selected_data_var
    selected_data_var = tk.StringVar(tab4_frame)
    selected_data_var.set("Select Data")  # Default selection

    # File Type Menu
    global file_type_menu
    file_type_menu = tk.OptionMenu(tab4_frame, selected_data_var, "Select Data")
    file_type_menu.pack(pady=10)

    # Update Dropdown Menu
    update_dropdown_menu()  # Initialize the dropdown menu

    # Display Data Button
    display_button = tk.Button(tab4_frame, text="Display Data",
                               command=lambda tab=tab4_frame: display_selected_data(tab))
    display_button.pack(pady=10)

    # Include result_display in the Top 25 tab
    global result_display
    result_display = ttk.Treeview(tab4_frame)
    result_display.pack(pady=10)

    # Top 25 Finishers Button
    top_25_button = tk.Button(tab4_frame, text="Top 25 Finishers", command=lambda: display_results(data_dict[selected_data_var.get()], "Top_25"))
    top_25_button.pack(pady=10)

    # Team Scores Button
    team_scores_button = tk.Button(tab4_frame, text="Team Scores",
                                   command=lambda: display_results(data_dict[selected_data_var.get()], "Team_Scores"))
    team_scores_button.pack(pady=10)


def load_athletes_listbox(listbox):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("crosscountry_match.db")
        cursor = conn.cursor()

        # Fetch athletes from the database
        cursor.execute("""
            SELECT athlete_id, first_name, last_name, team_id, gender
            FROM athletes
        """)
        athletes_data = cursor.fetchall()

        # Clear the existing items in the listbox
        listbox.delete(0, tk.END)

        # Populate the listbox with athlete information
        for athlete in athletes_data:
            listbox.insert(tk.END, f"{athlete[1]} {athlete[2]}, Team: {athlete[3]}, Gender: {athlete[4]}")

        # Close the connection
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert_race_time(race_time):
    """
    Convert race time from 'mm:ss.s' format to seconds.

    Parameters:
    - race_time: Race time in 'mm:ss.s' format.

    Returns:
    - Time in seconds.
    """
    minutes, seconds = map(float, race_time.split(':'))
    return minutes * 60 + seconds

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_name = file_path.split("/")[-1].split(".")[0]  # Extract file name without extension
        data_dict[file_name] = read_csv(file_path)
        print(f"Uploaded {file_name}.csv")

        # Update the dropdown menu with the new data
        update_dropdown_menu()


def display_results(data, action):
    global result_display  # Access the global result_display variable

    # Clear the existing Treeview
    for child in result_display.get_children():
        result_display.delete(child)

    if action == "Top_25":
        display_top_25(data)
    elif action == "Team_Scores":
        calculate_and_display_team_scores(data)
    else:
        # Set unique identifiers for Treeview columns
        col_identifiers = [f"col_{i}" for i in range(len(data.columns))]

        result_display['columns'] = col_identifiers
        result_display.heading('#0', text='Index')

        for col, col_id in zip(data.columns, col_identifiers):
            result_display.heading(col_id, text=col)
            result_display.column(col_id, anchor=tk.CENTER, width=100)

        for index, row in data.iterrows():
            result_display.insert('', tk.END, text=index, values=list(row))


def display_top_25(data):
    # Assuming 'Race Time (Seconds)' is a valid column
    data['Race Time (Seconds)'] = data[' Race Time'].apply(convert_race_time)
    top_25_data = data.sort_values(by='Race Time (Seconds)').head(25)

    # Set unique identifiers for Treeview columns
    col_identifiers = [f"col_{i}" for i in range(len(top_25_data.columns))]

    result_display['columns'] = col_identifiers
    result_display.heading('#0', text='Index')

    for col, col_id in zip(top_25_data.columns, col_identifiers):
        result_display.heading(col_id, text=col)
        result_display.column(col_id, anchor=tk.CENTER, width=100)

    for index, row in top_25_data.iterrows():
        result_display.insert('', tk.END, text=index, values=list(row))

def calculate_and_display_team_scores(data):
    # Assuming 'Team' is a valid column
    data['Team'] = data[' Team']
    team_scores = data.groupby('Team').apply(calculate_team_score).reset_index(drop=True)
    team_scores = team_scores.sort_values(by='Total Points')

    # Set unique identifiers for Treeview columns
    col_identifiers = [f"col_{i}" for i in range(len(team_scores.columns))]

    result_display['columns'] = col_identifiers
    result_display.heading('#0', text='Index')

    for col, col_id in zip(team_scores.columns, col_identifiers):
        result_display.heading(col_id, text=col)
        result_display.column(col_id, anchor=tk.CENTER, width=100)

    for index, row in team_scores.iterrows():
        result_display.insert('', tk.END, text=index, values=list(row))


def calculate_team_score(team_data):
    # Assuming 'Race Time (Seconds)' is a valid column
    team_data['Race Time (Seconds)'] = team_data[' Race Time'].apply(convert_race_time)
    team_data = team_data.sort_values(by='Race Time (Seconds)').head(5)

    total_points = team_data['Race Time (Seconds)'].rank().sum()
    return pd.DataFrame({
        'Team': [team_data['Team'].iloc[0]],
        'Total Points': [total_points],
    })

def display_selected_data(*args):
    selected_data = selected_data_var.get()
    if selected_data in data_dict:
        display_results(data_dict[selected_data], selected_data)
    else:
        print(f"Error: {selected_data} data not found.")

def update_dropdown_menu():
    menu = file_type_menu["menu"]
    menu.delete(0, "end")

    for data_key in data_dict.keys():
        menu.add_command(label=data_key, command=tk._setit(selected_data_var, data_key))
