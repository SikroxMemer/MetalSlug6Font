import os
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)

ALLOWED_CHARACTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ!? ")
CHARACTER_FILES = {'?': 'Symbols/question', '!': 'Symbols/exclamation'}
SPACE_WIDTH = 20
GENERATED_IMAGE_PATH = 'result.png'

def generate_image(text):
    try:
        sanitized_text = ''.join(char for char in text if char in ALLOWED_CHARACTERS)

        img_height = None
        chars = []
        first_char = True

        for char in sanitized_text:
            if char == ' ':
                if first_char:
                    first_char = False
                    char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
                    char_width = SPACE_WIDTH
                else:
                    chars[-1] = (chars[-1][0], chars[-1][1] + SPACE_WIDTH)
                    continue
            else:
                first_char = False
                char_img_path = os.path.join('static', f"{CHARACTER_FILES.get(char, 'Alphabets/' + char)}.png")
                if not os.path.exists(char_img_path):
                    raise ValueError(f"The character '{char}' is not supported.")
                char_img = Image.open(char_img_path).convert('RGBA')
                char_size = char_img.size
                char_width = char_size[0]
                if img_height is None:
                    img_height = char_size[1]
            chars.append((char_img, char_width))

        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0
        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        img_path = os.path.join('static', GENERATED_IMAGE_PATH)
        img.save(img_path)

        return GENERATED_IMAGE_PATH, None

    except Exception as e:
        app.logger.error("An error occurred: %s", str(e))
        return None, "An error occurred. Please try again later."

@app.route('/', methods=['GET', 'POST'])
def index():
    img_path = None
    error_message = None

    if request.method == 'POST':
        text = request.form.get('text', '').upper()

        if not text:
            error_message = "Please enter text."
        else:
            img_path, error_message = generate_image(text)

    return render_template('index.html', img_path=img_path, error_message=error_message)

if __name__ == "__main__":
    app.run()
