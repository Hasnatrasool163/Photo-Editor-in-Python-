# Function to open the file dialog and return the selected file path
def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return file_path

# Function to apply blur effect to the image
def apply_blur(image_path, output_path):
    img = Image.open(image_path)
    blurred_img = img.filter(ImageFilter.BLUR)
    blurred_img.save(output_path)
    return blurred_img


# Function to crop and resize the image
def crop_and_resize(image_path, output_path, dimensions):
    img = Image.open(image_path)
    cropped_resized_img = img.crop((0, 0, dimensions[0], dimensions[1])).resize(dimensions)
    cropped_resized_img.save(output_path)
    return cropped_resized_img

# Function to apply an artistic filter to the image
def apply_artistic_filter(image_path, output_path):
    img = Image.open(image_path)
    sepia_img = ImageOps.colorize(img.convert("L"), "#704214", "#C0A080")
    sepia_img.save(output_path)
    return sepia_img

# Function to add text overlay to the image
def add_text_overlay(image_path, output_path, text, font, color, position):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=color)
    img.save(output_path)
    return img

# Function to draw on the image
def draw_on_image_with_centered_textbox(image_path, output_path, drawing_info):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    for info in drawing_info:
        # Calculate the center coordinates for the textbox
        center_x = img.width // 2
        center_y = img.height // 2
        textbox_width = 200  # Set the width of the textbox
        textbox_height = 30  # Set the height of the textbox

        # Draw a rectangle
        textbox_coordinates = (
            center_x - textbox_width // 2,
            center_y - textbox_height // 2,
            center_x + textbox_width // 2,
            center_y + textbox_height // 2
        )
        draw.rectangle(textbox_coordinates, outline=info["color"], width=info["width"])

        # Add a textbox for user input
        font_size = 12
        font = ImageFont.truetype("arial.ttf", font_size)  # You can use a different font file
        text = info.get("text", "")
        draw.text((textbox_coordinates[0] + 5, textbox_coordinates[1] + 5), text, font=font, fill=info["color"])

    img.save(output_path)
    return img

# Function to create a collage from multiple images
def create_collage(images, output_path):
    collage_img = Image.new('RGB', (800, 600), (255, 255, 255))

    for i, image_path in enumerate(images):
        img = Image.open(image_path)
        collage_img.paste(img, (i * 200, 0))

    collage_img.save(output_path)
    return collage_img

# Function to remove red-eye effect from the image
def remove_red_eye(image_path, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.ellipse((100, 100, 150, 150), fill="black")
    img.save(output_path)
    return img

def apply_zoom_in(image_path, output_path, level):
    img = Image.open(image_path)
    img = img.resize((int(img.width * level), int(img.height * level)), Image.BICUBIC)
    img.save(output_path)
    return img

# Function to apply zoom out on the image with specified levels
def apply_zoom_out(image_path, output_path, level):
    img = Image.open(image_path)
    img = img.resize((int(img.width / level), int(img.height / level)), Image.BICUBIC)
    img.save(output_path)
    return img


# Function to display the history panel
def display_history_panel():
    history_text = "\n".join(recent_operations)
    messagebox.showinfo("Recent Operations", history_text)

# Function to apply grayscale effect to the image
def apply_grayscale(image_path, output_path):
    img = Image.open(image_path)
    grayscale_img = img.convert("L")
    grayscale_img.save(output_path)
    return grayscale_img

# Function to apply sepia effect to the image
def apply_sepia(image_path, output_path):
    img = Image.open(image_path)
    sepia_img = ImageOps.colorize(img.convert("L"), "#704214", "#C0A080")
    sepia_img.save(output_path)
    return sepia_img

# Function to adjust the brightness of the image
def adjust_brightness(image_path, output_path, factor):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(img)
    brightened_img = enhancer.enhance(factor)
    brightened_img.save(output_path)
    return brightened_img

# Function to adjust the contrast of the image
def adjust_contrast(image_path, output_path, factor):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(img)
    contrast_img = enhancer.enhance(factor)
    contrast_img.save(output_path)
    return contrast_img

# Function to rotate the image
def rotate_image(image_path, output_path, angle):
    img = Image.open(image_path)
    rotated_img = img.rotate(angle)
    rotated_img.save(output_path)
    return rotated_img

# Function to flip the image horizontally or vertically
def flip_image(image_path, output_path, direction):
    img = Image.open(image_path)
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT) if direction == 'horizontal' else img.transpose(
        Image.FLIP_TOP_BOTTOM)
    flipped_img.save(output_path)
    return flipped_img

# Function to update the image label with the modified image
def update_image_label(label, img):
    img.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo
    label.photo = img