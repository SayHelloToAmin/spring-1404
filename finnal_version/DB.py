from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()  # Set up rich console for colored and styled output
import sqlite3  # Import SQLite for database management

# Connect to the database (creates file if it doesn't exist)
conn = sqlite3.connect("game_data.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    name TEXT PRIMARY KEY,           
    wins INTEGER DEFAULT 0,         
    highest_score INTEGER DEFAULT 0  
)
""")
conn.commit()  # Save changes to the database

# Save or update winner's info in the database
def save_winner_to_database(name, score):
    cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
    row = cursor.fetchone()  # Check if player exists

    if row:
        # Update wins and highest score
        wins = row[1] + 1
        highest_score = max(row[2], score)
        cursor.execute("UPDATE players SET wins = ?, highest_score = ? WHERE name = ?", (wins, highest_score, name))
    else:
        # Add new player to the database
        cursor.execute("INSERT INTO players (name, wins, highest_score) VALUES (?, ?, ?)", (name, 1, score))

    conn.commit()  # Save changes

# Display the scoreboard
def display_scoreboard():
    table = Table(title="🎯 [bold yellow]Scoreboard[/bold yellow]")  # Create a table

    # Add columns
    table.add_column("Player", style="cyan", justify="left")
    table.add_column("Wins", style="green", justify="center")
    table.add_column("Highest Score", style="magenta", justify="center")

    # Get player data sorted by wins and highest score
    cursor.execute("SELECT name, wins, highest_score FROM players ORDER BY wins DESC, highest_score DESC")
    rows = cursor.fetchall()

    # Add rows to the table
    for row in rows:
        table.add_row(row[0], str(row[1]), str(row[2]))

    console.print(table)  # Print the table