"""
Utils module.
"""

import inflect

ANSI_RESET_CODE = "\033[0m"

color_ansi_code_mapper: dict = {
    "CYAN": "\033[36m",
    "GRAY": "\033[90m",
    "GREEN": "\033[32m",
    "MAGENTA": "\033[35m",
    "RED": "\033[31m",
    "YELLOW": "\033[33m",
}

def prompt_user(message: str, color: str = "GRAY", end: str = "\n"):
    print(f"{color_ansi_code_mapper[color.upper()]}{message}{ANSI_RESET_CODE}", end=end)

def get_user_confirmation(color="GRAY"): 
    prompt_user(f"\n-> Do you want to continue? (Y/N): ", color=color, end="")

    user_input = input()

    if user_input.lower() != 'y':
        prompt_user("\nExiting...", color="RED")
        exit()

def camel_to_pascal(camel_str):
    # Capitalize the first letter and keep the rest as it is
    return camel_str[0].upper() + camel_str[1:]

def plural_to_singular(word):
    p = inflect.engine()
    return p.singular_noun(word) or word  # Returns the word if it's already singular
