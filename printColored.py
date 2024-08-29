from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def printColored(text, color):
    """
    Prints the given text in the specified color.

    Parameters:
    text (str): The text to print.
    color (str): The color to print the text in. Supported colors are:
                 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
    """
    color_dict = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    
    # Get the color from the dictionary, default to white if not found
    color_code = color_dict.get(color.lower(), Fore.WHITE)
    
    # Print the text in the specified color
    print(f"{color_code}{text}{Style.RESET_ALL}")