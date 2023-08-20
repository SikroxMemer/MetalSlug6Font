import sys
import random
# Prevent the generation of __pycache__ directories
sys.dont_write_bytecode = True
from main import generate_filename, generate_image_with_filename 

sys.dont_write_bytecode = True
from color import COLORS, BOLD, RESET

# Main function
def main():
    while True:
        text = input(random.choice(COLORS) + BOLD + "Enter the desired output (press Enter to quit): " + RESET)
        
        if not text:
            print(random.choice(COLORS) + BOLD + "Goodbye!" + RESET)
            break

        filename = generate_filename(text)
        img_path, error_message = generate_image_with_filename(text, filename)

        if error_message:
            print(random.choice(COLORS) + error_message + RESET)
        else:
            print(random.choice(COLORS) + BOLD + f"Image generated successfully: {img_path}" + RESET)

if __name__ == "__main__":
    main()