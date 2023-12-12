import tkinter as tk
import pandas as pd
import csv
import sqlite3
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime

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