from classes import Game  # Import the Game class
from DB import *  # Import database-related functions
from rich.console import Console  # For styled console output
from rich.panel import Panel  # For creating panels
from rich.table import Table  # For creating tables

console = Console()  # Initialize the rich console

# Display the main menu and return the user's choice
def show_main_menu():
    console.print("[bold magenta]What would you like to do?[/bold magenta]")
    console.print("1. [bold cyan]Play the Game[/bold cyan]")
    console.print("2. [bold green]View Scoreboard[/bold green]")
    choice = console.input("[bold yellow]Enter your choice (1 or 2): [/bold yellow]")
    return choice

# Show a welcome message with a styled panel
def show_welcome_message():
    console.print(Panel("🎮 [bold cyan]Welcome to the Game![/bold cyan]\nGet ready for an exciting adventure!", 
                        title="[bold yellow]Game Menu[/bold yellow]",
                        subtitle="[bold magenta]Made with ❤️  by Amin[/bold magenta]",
                        border_style="bright_blue"))

# Get player names with styled prompts
def get_player_names():
    console.print("[bold magenta]Please enter player names:[/bold magenta]")
    player1 = console.input("[cyan]Player 1: [/cyan]")  # Input for Player 1
    player2 = console.input("[green]Player 2: [/green]")  # Input for Player 2

    console.print(f"\n[bold yellow]Let the game begin! Good luck to [cyan]{player1}[/cyan] and [green]{player2}[/green]![/bold yellow]")
    return player1, player2

# Display the winner and their score with a styled panel
def show_winner(name, score):
    console.print(Panel(f"[bold green]{name.upper()} is the winner![/bold green]\n[bold yellow]Final Score: {score}[/bold yellow]",
                        title="[bold magenta]Game Over[/bold magenta]",
                        border_style="bright_red"))

# Start the game
def play_game():
    # Get names of both players
    player1_name, player2_name = get_player_names()

    # Assign names to players
    Game.players[0].name = player1_name
    Game.players[1].name = player2_name

    # Initialize and run the game
    game = Game()
    game.run()

    # Determine the winner or if it's a tie
    if Game.players[0].score > Game.players[1].score:
        winner_name = Game.players[0].name
        winner_score = Game.players[0].score
    elif Game.players[1].score > Game.players[0].score:
        winner_name = Game.players[1].name
        winner_score = Game.players[1].score
    else:
        console.print("[bold magenta]It's a tie! Well played both![/bold magenta]")
        return

    # Show the winner and save their data to the database
    show_winner(winner_name, winner_score)
    save_winner_to_database(winner_name, winner_score)

# Main program execution
if __name__ == "__main__":
    show_welcome_message()  # Display the welcome message
    choice = show_main_menu()  # Show the menu and get the user's choice

    # Handle the user's choice
    if choice == "1":
        play_game()  # Start the game
    elif choice == "2":
        display_scoreboard()  # Show the scoreboard
    else:
        console.print("[bold red]Invalid choice. Please try again.[/bold red]")  # Invalid input message