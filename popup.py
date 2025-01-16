import tkinter as tk

def show_game_over_dialog(restart_callback, quit_callback, elapsed_time):
    """
    Display a dialog with Restart and Quit options.

    Parameters:
    - restart_callback: Function to call when "Restart" is clicked.
    - quit_callback: Function to call when "Quit" is clicked.
    """
    def restart_game():
        popup.destroy()  # Close the dialog
        restart_callback()  # Call the restart function

    def quit_game():
        popup.destroy()  # Close the dialog
        quit_callback()  # Call the quit function

    # Create the Tkinter root window
    popup = tk.Tk()
    popup.title("Game Over")
    popup.geometry("300x150")  # Set dimensions of the popup window
    popup.eval('tk::PlaceWindow . center')  # Center the popup on the screen

     # Add a message
    label = tk.Label(
        popup, 
        text=f"Game Over!\nYour time: {elapsed_time:.2f} seconds.\nWhat do you want to do?", 
        font=("Arial", 9)
    )
    label.pack(pady=20)

    # Add Restart and Quit buttons
    restart_button = tk.Button(popup, text="Restart", command=restart_game, width=10, bg="green", fg="white")
    restart_button.pack(side="left", padx=20, pady=20)

    quit_button = tk.Button(popup, text="Quit", command=quit_game, width=10, bg="red", fg="white")
    quit_button.pack(side="right", padx=20, pady=20)

    # Start the Tkinter event loop
    popup.mainloop()
