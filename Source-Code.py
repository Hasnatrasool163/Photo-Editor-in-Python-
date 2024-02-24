####################Code-Written-by "Muhammad Hasnat Rasool"####################

# a Simple Basic Photo Editor implementation 

    # Photo editor made using python,tkinter and Pillow 
    
########## Import necessary libraries(modules)###############################################
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, StringVar
from PIL import (
    Image,
    ImageEnhance,
    ImageFilter,
    ImageOps,
    ImageDraw,
    ImageTk,
    ImageFont,
)
from customtkinter import (
    CTk,
    CTkButton,
    CTkLabel,
    set_appearance_mode,
    set_default_color_theme,
    CTkFrame,
    CTkEntry,
    CTkRadioButton,
    CTkToplevel,
)

# import time
# from threading import Thread

###################Theme+Apperance-mode##################################################

set_default_color_theme("Hades")
set_appearance_mode("dark")


# List to store the history of recent operations
recent_operations = []

zoom_factor = 3
threshold = 128


# Function to open the file dialog and return the selected file path
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    return file_path


# Function to apply blur effect to the image
def apply_blur(image_path, output_path):
    img = Image.open(image_path)
    # blurred_img = img.filter(ImageFilter.BLUR)
    blurred_img = img.filter(ImageFilter.GaussianBlur(5))  # Apply Gaussian Blur
    # return img.filter(ImageFilter.GaussianBlur(blur_intensity))

    # blurred_img.save(output_path)

    return blurred_img


def apply_sharpen(image_path, output_path, radius=2, percent=180):
    img = Image.open(image_path)
    sharpened_img = img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent))
    # sharpened_img.save(output_path)
    return sharpened_img


# Function to crop and resize the image
def crop_and_resize(image_path, output_path, dimensions):
    img = Image.open(image_path)
    cropped_resized_img = img.crop((0, 0, dimensions[0], dimensions[1])).resize(
        dimensions
    )
    # cropped_resized_img.save(output_path)
    return cropped_resized_img


# Function to apply an artistic filter to the image
def apply_artistic_filter(image_path, output_path):
    img = Image.open(image_path)
    sepia_img = ImageOps.colorize(img.convert("L"), "#704214", "#C0A080")
    # sepia_img.save(output_path)
    return sepia_img


# Function to add text overlay to the image
def add_text_overlay(image_path, output_path, text, font, color, position):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=color)
    # img.save(output_path)
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
            center_y + textbox_height // 2,
        )
        draw.rectangle(textbox_coordinates, outline=info["color"], width=info["width"])

        # Add a textbox for user input
        font_size = 12
        font = ImageFont.truetype(
            "arial.ttf", font_size
        )  # You can use a different font file
        text = info.get("text", "")
        draw.text(
            (textbox_coordinates[0] + 5, textbox_coordinates[1] + 5),
            text,
            font=font,
            fill=info["color"],
        )

    # img.save(output_path)
    return img


# Function to create a collage from multiple images
def create_collage(images, output_path):
    collage_img = Image.new("RGB", (800, 600), (255, 255, 255))

    for i, image_path in enumerate(images):
        img = Image.open(image_path)
        collage_img.paste(img, (i * 200, 0))

    # collage_img.save(output_path)
    return collage_img


# Function to remove red-eye effect from the image
def remove_red_eye(image_path, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.ellipse((100, 100, 150, 150), fill="black")
    # img.save(output_path)
    return img

# Function to Zoom images
def apply_zoom_in(
    image_path,
    output_path,
):
    img = Image.open(image_path)
    # img = img.resize((int(img.width * 3), int(img.height * 3)), Image.BICUBIC)
    # img.save(output_path)
    # float zoom_factor =1.25
    new_size = (int(img.size[0] * zoom_factor), int(img.size[1] * zoom_factor))
    return img.resize(new_size, Image.BICUBIC)
    # return img

# Function to Zoom images
def zoom_image(image_path):
    img = Image.open(image_path)
    # Calculate the new size (width and height) based on the zoom factor
    new_size = (int(260 * 2), int(260 * 2))

    # Resize the image to the new size
    return img.resize(new_size, Image.BICUBIC)

# Function to add invert colors effect on images
def invert_colors(image_path):
    img = Image.open(image_path)
    if img.mode == "RGBA":
        r, g, b, a = img.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        final_transposed_image = Image.merge("RGBA", (r2, g2, b2, a))
        return final_transposed_image
    else:
        return ImageOps.invert(img)

# Function to add solarize effect on images
def solarize_image(
    image_path,
):
    img = Image.open(image_path)
    if img.mode == "RGBA":
        r, g, b, a = img.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        solarized_image = ImageOps.solarize(rgb_image, threshold)
        r2, g2, b2 = solarized_image.split()
        final_transposed_image = Image.merge("RGBA", (r2, g2, b2, a))
        return final_transposed_image
    else:
        return ImageOps.solarize(img, threshold)

# Function to add posterize effect on images
def posterize_image(image_path):
    img = Image.open(image_path)
    bits = 4
    if img.mode == "RGBA":
        rgb_image = img.convert("RGB")
        alpha_channel = img.getchannel("A")
        posterized_rgb_image = ImageOps.posterize(rgb_image, bits)
        posterized_image = Image.merge(
            "RGBA", (*posterized_rgb_image.split(), alpha_channel)
        )
    else:
        # For non-RGBA images, apply posterize directly
        posterized_image = ImageOps.posterize(img, bits)

    return posterized_image

# Function to apply zoom out on the image with specified levels
def apply_zoom_out(image_path, output_path):
    img = Image.open(image_path)
    img = img.resize((int(img.width / 3), int(img.height / 3)), Image.BICUBIC)
    # img.save(output_path)
    return img

def add_text(image_path):
    img = Image.open(image_path)

    def apply_text():
        img = Image.open(image_path)

        text = text_entry.get()
        position = position_var.get()
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(img)

        text_width, text_height = draw.textsize(text, font=font)
        if position == "top":
            position = (10, 10)
        elif position == "center":
            position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

        draw.text(position, text, fill="black", font=font)
        top.destroy()
        # img.show()

    top = CTkToplevel()
    top.title("Add Text to Image")

    CTkLabel(top, text="Text:").pack()
    text_entry = CTkEntry(top)
    text_entry.pack()

    position_var = StringVar(value="top")
    CTkRadioButton(top, text="Top", variable=position_var, value="top").pack()
    CTkRadioButton(top, text="Center", variable=position_var, value="center").pack()

    CTkButton(top, text="Apply", command=apply_text).pack()

    top.mainloop()

# Function to display the history panel
def display_history_panel():
    history_text = "\n".join(recent_operations)
    messagebox.showinfo("Recent Operations", history_text)


# Function to apply grayscale effect to the image
def apply_grayscale(image_path, output_path):
    img = Image.open(image_path)
    grayscale_img = img.convert("L")
    # grayscale_img.save(output_path)
    return grayscale_img


# Function to apply sepia effect to the image
def apply_sepia(image_path, output_path):
    img = Image.open(image_path)
    sepia_img = ImageOps.colorize(img.convert("L"), "#704214", "#C0A080")
    # sepia_img.save(output_path)
    return sepia_img


# Function to adjust the brightness of the image
def adjust_brightness(image_path, output_path, factor):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(img)
    brightened_img = enhancer.enhance(factor)
    # brightened_img.save(output_path)
    return brightened_img


# Function to adjust the contrast of the image
def adjust_contrast(image_path, output_path, factor):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(img)
    contrast_img = enhancer.enhance(factor)
    # contrast_img.save(output_path)
    return contrast_img

    # def apply_emboss_filter(image_path):
    img = Image.open(image_path)

    return img.filter(ImageFilter.EMBOSS)


def apply_custom_filter(image_path):
    img = Image.open(image_path)

    kernel = [0, -1, 0, -1, 5, -1, 0, -1, 0]
    return img.filter(ImageFilter.Kernel((3, 3), kernel))


def smart_enhance(image_path):
    img = Image.open(image_path)
    # Step 1: Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Adjust the factor based on image analysis

    # Step 2: Enhance brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)  # Adjust the factor based on image analysis

    # Step 3: Apply slight sharpening
    img = img.filter(ImageFilter.SHARPEN)

    # Optional: Enhance color
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)  # Adjust the factor based on image analysis

    return img


def apply_cool_effect(image_path):
    # Load the image
    img = Image.open(image_path)

    # Enhance the image's color saturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(2.0)  # Increase saturation

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Slightly increase contrast

    # Apply a blur filter for a dreamy effect
    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    # Create a blue overlay to give a cool tone
    blue_overlay = Image.new("RGB", img.size, "#0036FF")
    img = Image.blend(img, blue_overlay, alpha=0.2)  # Adjust alpha for intensity

    # Optionally, apply a vignette effect
    vignette = Image.new("L", img.size, 0)
    for x in range(img.width):
        for y in range(img.height):
            # Calculate distance to center
            distance = ((x - img.width / 2) ** 2 + (y - img.height / 2) ** 2) ** 0.5
            # Normalize distance
            distance = distance / ((img.width / 2) ** 2 + (img.height / 2) ** 2) ** 0.5
            # Calculate opacity
            opacity = 255 - int(distance * 255)
            # Set pixel value
            vignette.putpixel((x, y), opacity)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=img.width / 5))
    img.paste(ImageOps.colorize(vignette, (0, 0, 0), (0, 0, 0)), (0, 0), vignette)

    return img


def apply_vintage_effect(image_path):
    img = Image.open(image_path)
    # Convert to grayscale
    grayscale = img.convert("L")
    # Apply a sepia overlay
    img = grayscale.point(lambda p: p * 0.9 + 10)
    return Image.merge(
        "RGB", (img, img.point(lambda p: p * 0.95 + 20), img.point(lambda p: p * 0.85))
    )


def apply_black_white_contrast(image_path):
    img = Image.open(image_path).convert("L")
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(
        2.0
    )  # You can adjust the factor for different levels of contrast


def apply_pencil_sketch_effect(image_path):
    img = Image.open(image_path).convert("L")
    inverted_image = ImageOps.invert(img)
    blur_image = inverted_image.filter(ImageFilter.GaussianBlur(radius=10))
    return Image.blend(img, blur_image, alpha=0.45)


def apply_emboss_effect(image_path):
    img = Image.open(image_path)
    return img.filter(ImageFilter.EMBOSS)


def apply_edge_detection(image_path):
    img = Image.open(image_path)
    return img.filter(ImageFilter.FIND_EDGES)


def apply_colorful_background(image_path, background_color="blue"):
    # Load the image
    img = Image.open(image_path).convert("RGBA")
    # Create a background image with the specified color
    background = Image.new("RGBA", img.size, background_color)
    # Composite the images
    combined = Image.alpha_composite(background, img)
    return combined.convert("RGB")  # Convert back to RGB if needed


def apply_gradient_background(image_path, color1="#FFC0CB", color2="#FFD700"):
    img = Image.open(image_path).convert("RGBA")
    background = Image.new("RGBA", img.size, "#FFFFFF")

    top_color = Image.new("RGBA", img.size, color1)
    bottom_color = Image.new("RGBA", img.size, color2)

    mask = Image.new("L", img.size)
    mask_data = []
    for y in range(img.size[1]):
        mask_data.extend([int(255 * (y / img.size[1]))] * img.size[0])
    mask.putdata(mask_data)

    background.paste(top_color, (0, 0))
    background.paste(bottom_color, (0, 0), mask=mask)
    combined = Image.alpha_composite(background, img)
    return combined.convert("RGB")


def apply_heart_shape(image_path, output_size=(200, 200)):
    # Load and resize the original image
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(output_size, Image.BICUBIC)

    # Create a new image with a transparent background
    heart_image = Image.new("RGBA", output_size, (0, 0, 0, 0))

    # Create a mask for the heart shape
    mask = Image.new("L", output_size, 0)
    draw = ImageDraw.Draw(mask)

    # Heart shape parameters
    width, height = output_size
    top = height // 4
    bottom = height - top
    left = width // 4
    right = width - left
    triangle = [(left, top), (right, top), (width // 2, bottom)]

    # Draw the heart shape
    draw.ellipse([0, 0, width // 2, height // 2], fill=255)
    draw.ellipse([width // 2, 0, width, height // 2], fill=255)
    draw.polygon(triangle, fill=255)

    # Apply the heart mask to the image
    return heart_image.paste(img, (0, 0), mask=mask)


# Function to rotate the image
def rotate_image(image_path, output_path, angle):
    img = Image.open(image_path)
    rotated_img = img.rotate(angle)
    # rotated_img.save(output_path)
    return rotated_img


# Function to flip the image horizontally or vertically
def flip_image(image_path, output_path, direction):
    img = Image.open(image_path)
    flipped_img = (
        img.transpose(Image.FLIP_LEFT_RIGHT)
        if direction == "horizontal"
        else img.transpose(Image.FLIP_TOP_BOTTOM)
    )
    # flipped_img.save(output_path)
    return flipped_img


# Function to update the image label with the modified image
def update_image_label(label, img):
    img.thumbnail((280, 280))
    photo = ImageTk.PhotoImage(img)
    label.configure(image=photo)
    label.image = photo
    label.photo = img


# Variable to store the original image
original_img = None


# Main function to create the GUI
def main():
    root = CTk()
    root.resizable(False, False)
    root.title("Photo Editor by Muhammad Hasnat Rasool")
    root.geometry("1200x660")

    # Label to display the original image
    original_image_label = CTkLabel(root, text="Original Image", width=280, height=280)
    original_image_label.place(x=300, y=5)

    # Label to display the modified image
    modified_image_label = CTkLabel(root, text="Modified Image", width=280, height=280)
    modified_image_label.place(x=650, y=5)

    # Variable to store the file path
    file_path_var = tk.StringVar()
    # def flash_modified_image():

    #     flash_duration = 0.1  # Time each flash lasts
    #     flash_count = 3  # Total number of flashes

    #     original_bg = modified_image_label.cget('background')  # Save original background color
    #     flash_color = "yellow"  # Flash color, choose something that stands out

    #     for _ in range(flash_count):
    #         modified_image_label.config(background=flash_color)  # Change to flash color
    #         root.update()  # Immediately update the UI
    #         time.sleep(flash_duration)
    #         modified_image_label.config(background=original_bg)
    #     root.update()
    #     time.sleep(flash_duration)
    # Function to perform image operations
    def perform_operation(operation):
        global original_img
        input_image = file_path_var.get()
        output_path = None  # Declare output_path outside of if-else block

        modified_image_label.configure(text="")

        # Undo operation
        if operation == "Undo":
            modified_img = original_img.copy()
            update_image_label(modified_image_label, modified_img)
            modified_image_label.configure(text="")

        else:
            if not input_image:
                print("No image selected. Please upload an image first.")
                messagebox.showinfo("Prompt", "Choose an image to Apply filters")
                return

            original_img = Image.open(input_image)
            output_path = input_image.replace(".", f"_{operation}.")
            modified_image_label.configure(text="")

            # Perform specific operation based on user choice
            if operation == "Blur":
                modified_img = apply_blur(input_image, output_path)

            elif operation == "Solarize":
                modified_img = solarize_image(input_image)
            elif operation == "Custom":
                modified_img = apply_custom_filter(input_image)
            elif operation == "Smart":
                modified_img = smart_enhance(input_image)
            elif operation == "Cool_effect":
                modified_img = apply_cool_effect(input_image)
            elif operation == "Vintage":
                modified_img = apply_vintage_effect(input_image)
            elif operation == "Black":
                modified_img = apply_black_white_contrast(input_image)
            elif operation == "Emboss":
                modified_img = apply_emboss_effect(input_image)
            elif operation == "Edge":
                modified_img = apply_edge_detection(input_image)
            elif operation == "Colorful":
                modified_img = apply_colorful_background(input_image)
            elif operation == "Pencil":
                modified_img = apply_pencil_sketch_effect(input_image)
            elif operation == "Gradient":
                modified_img = apply_gradient_background(input_image)
            elif operation == "Heart":
                modified_img = apply_heart_shape(input_image)
            elif operation == "Zoom":
                modified_img = zoom_image(input_image)
            elif operation == "Posteraize":
                modified_img = posterize_image(input_image)
            elif operation == "Add_Text":
                modified_img = add_text(input_image)
            elif operation == "Invert":
                modified_img = invert_colors(input_image)
            elif operation == "Sharpen":
                modified_img = apply_sharpen(
                    input_image, output_path, radius=2, percent=180
                )
            elif operation == "Grayscale":
                modified_img = apply_grayscale(input_image, output_path)
            elif operation == "Sepia":
                modified_img = apply_sepia(input_image, output_path)
            elif operation == "Brighten":
                modified_img = adjust_brightness(input_image, output_path, factor=1.9)
            elif operation == "Contrast":
                modified_img = adjust_contrast(input_image, output_path, factor=2)
            elif operation == "Rotate":
                angle = simpledialog.askfloat("Input", "Enter rotation angle:")
                modified_img = rotate_image(input_image, output_path, angle)
            elif operation == "Flip Horizontal":
                modified_img = flip_image(
                    input_image, output_path, direction="horizontal"
                )
            elif operation == "Flip Vertical":
                modified_img = flip_image(
                    input_image, output_path, direction="vertical"
                )
            elif operation == "Crop & Resize":
                dimensions = simpledialog.askstring(
                    "Input", "Enter dimensions (width,height):"
                )
                dimensions = tuple(map(int, dimensions.split(",")))
                modified_img = crop_and_resize(input_image, output_path, dimensions)
            elif operation == "Artistic Filter":
                modified_img = apply_artistic_filter(input_image, output_path)
            elif operation == "Text Overlay":
                modified_img = add_text_overlay(
                    input_image,
                    output_path,
                    "Overlay Text",
                    font=None,
                    color="black",
                    position=(50, 50),
                )
            elif operation == "Drawing":
                drawing_info = []
                initial_text = "Here is your cursor"
                drawing_info.append(
                    {"color": "black", "width": 2, "text": initial_text}
                )
                modified_img = draw_on_image_with_centered_textbox(
                    input_image, output_path, drawing_info
                )
            elif operation == "Collage Maker":
                images = [input_image] * 3
                modified_img = create_collage(images, output_path)
            elif operation == "Red-eye Removal":
                modified_img = remove_red_eye(input_image, output_path)
            elif operation.startswith("Zoom In"):
                output_path = input_image.replace(".", f"_ZoomIn_x1.")
                modified_img = apply_zoom_in(input_image)
            elif operation.startswith("Zoom Out"):
                output_path = input_image.replace(".", f"_ZoomOut_x1.")
                modified_img = apply_zoom_out(input_image, output_path)
            else:
                print("Invalid operation selected.")
                return

            # Update recent_operations
            recent_operations.append(operation)
            print(f"{operation} applied.")
            update_image_label(modified_image_label, modified_img)
            modified_image_label.configure(text="")

    # Function to save the modified image
    def save_image():
        if modified_image_label.photo:
            output_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("BMP files", "*.bmp"),
                    ("PNJ files", "*.pnj"),
                    ("All files", "*.*"),
                ],
            )
            if output_path:
                modified_image_label.photo.save(output_path)
                print(f"Modified image saved to: {output_path}")

    # Function to upload an image
    def upload_image():
        file_path = open_file_dialog()
        if file_path:
            file_path_var.set(file_path)
            print(f"Image uploaded: {file_path}")

            original_img = Image.open(file_path)
            update_image_label(original_image_label, original_img)
            original_image_label.configure(text="")

    # Button to upload an image
    upload_button = CTkButton(
        root,
        text="Upload Image",
        command=upload_image,
        fg_color="green",
        font=("consolas", 12),
    )
    # upload_button.pack(side=tk.TOP, pady=170)
    upload_button.place(x=540, y=280)

    # Button frame for the first line of buttons
    button_frame_line1 = CTkFrame(root)
    # button_frame_line1.pack(side=tk.TOP, pady=10)
    button_frame_line1.place(x=2, y=330)

    blur_button = CTkButton(
        button_frame_line1,
        text="Blur",
        command=lambda: perform_operation("Blur"),
        fg_color="red",
    )
    blur_button.pack(side=tk.LEFT, padx=5)

    grayscale_button = CTkButton(
        button_frame_line1,
        text="Emboss",
        command=lambda: perform_operation("Emboss"),
        fg_color="red",
    )
    grayscale_button.pack(side=tk.LEFT, padx=5)
    # grayscale_button = CTkButton(
    #     button_frame_line1,
    #     text="Grayscale",
    #     command=lambda: perform_operation("Grayscale"),
    #     fg_color="red",
    # )
    # grayscale_button.pack(side=tk.LEFT, padx=5)

    sepia_button = CTkButton(
        button_frame_line1,
        text="Vintage",
        command=lambda: perform_operation("Vintage"),
        fg_color="red",
    )
    sepia_button.pack(side=tk.LEFT, padx=5)
    # sepia_button = CTkButton(
    #     button_frame_line1,
    #     text="Sepia",
    #     command=lambda: perform_operation("Sepia"),
    #     fg_color="red",
    # )
    # sepia_button.pack(side=tk.LEFT, padx=5)

    brighten_button = CTkButton(
        button_frame_line1,
        text="Black",
        command=lambda: perform_operation("Black"),
        fg_color="red",
    )
    brighten_button.pack(side=tk.LEFT, padx=5)
    # brighten_button = CTkButton(
    #     button_frame_line1,
    #     text="Brighten",
    #     command=lambda: perform_operation("Brighten"),
    #     fg_color="red",
    # )
    # brighten_button.pack(side=tk.LEFT, padx=5)

    contrast_button = CTkButton(
        button_frame_line1,
        text="Contrast",
        command=lambda: perform_operation("Contrast"),
        fg_color="red",
    )
    contrast_button.pack(side=tk.LEFT, padx=5)

    rotate_button = CTkButton(
        button_frame_line1,
        text="Smart",
        command=lambda: perform_operation("Smart"),
        fg_color="red",
    )
    rotate_button.pack(side=tk.LEFT, padx=5)
    # rotate_button = CTkButton(
    #     button_frame_line1,
    #     text="Rotate",
    #     command=lambda: perform_operation("Rotate"),
    #     fg_color="red",
    # )
    # rotate_button.pack(side=tk.LEFT, padx=5)

    flip_horizontal_button = CTkButton(
        button_frame_line1,
        text="Flip Horizontal",
        command=lambda: perform_operation("Flip Horizontal"),
        fg_color="red",
    )
    flip_horizontal_button.pack(side=tk.LEFT, padx=5)
    # flip_horizontal_button = CTkButton(
    #     button_frame_line1,
    #     text="Flip Horizontal",
    #     command=lambda: perform_operation("Cool_effect"),
    #     fg_color="red",
    # )
    # flip_horizontal_button.pack(side=tk.LEFT, padx=5)

    flip_vertical_button = CTkButton(
        button_frame_line1,
        text="Flip Vertical",
        command=lambda: perform_operation("Flip Vertical"),
        fg_color="red",
    )
    flip_vertical_button.pack(side=tk.LEFT, padx=5)

    # Button frame for the second line of buttons
    button_frame_line2 = CTkFrame(root)
    # button_frame_line2.pack(side=tk.TOP, pady=10)
    button_frame_line2.place(x=2, y=390)

    crop_resize_button = CTkButton(
        button_frame_line2,
        text="Grayscale",
        command=lambda: perform_operation("Grayscale"),
        fg_color="red",
    )
    crop_resize_button.pack(side=tk.LEFT, padx=5)

    artistic_filter_button = CTkButton(
        button_frame_line2,
        text="Rotate",
        command=lambda: perform_operation("Rotate"),
        fg_color="red",
    )
    artistic_filter_button.pack(side=tk.LEFT, padx=5)

    text_overlay_button = CTkButton(
        button_frame_line2,
        text="Sepia",
        command=lambda: perform_operation("Sepia"),
        fg_color="red",
    )
    text_overlay_button.pack(side=tk.LEFT, padx=5)

    drawing_button = CTkButton(
        button_frame_line2,
        text="Brighten",
        command=lambda: perform_operation("Brighten"),
        fg_color="red",
    )
    drawing_button.pack(side=tk.LEFT, padx=5)

    collage_button = CTkButton(
        button_frame_line2,
        text="Pencil",
        command=lambda: perform_operation("Pencil"),
        fg_color="red",
    )
    collage_button.pack(side=tk.LEFT, padx=5)

    red_eye_button = CTkButton(
        button_frame_line2,
        text="Posteraize",
        command=lambda: perform_operation("Posteraize"),
        fg_color="red",
    )
    red_eye_button.pack(side=tk.LEFT, padx=5)

    sharpen_button = CTkButton(
        button_frame_line2,
        text="Sharpen",
        command=lambda: perform_operation("Sharpen"),
        fg_color="red",
    )
    sharpen_button.pack(side=tk.LEFT, padx=5)

    # batch_processing_button = CTkButton(button_frame_line2, text="Batch Processing", command=lambda: perform_operation("Batch Processing"), fg_color="red")
    # batch_processing_button.pack(side=tk.LEFT, padx=5)

    history_panel_button = CTkButton(
        button_frame_line2,
        text="History Panel",
        command=display_history_panel,
        fg_color="red",
    )
    history_panel_button.pack(side=tk.LEFT, padx=5)

    # Line for "Save" and "Undo" buttons
    button_frame_line3 = CTkFrame(root)
    # button_frame_line3.pack(side=tk.TOP, pady=10)
    button_frame_line3.place(x=200, y=440)

    zoom_in_button = CTkButton(
        button_frame_line3,
        text="Zoom In",
        command=lambda: perform_operation("Zoom"),
        fg_color="red",
    )
    zoom_in_button.pack(side=tk.LEFT, padx=5)

    zoom_out_button = CTkButton(
        button_frame_line3,
        text="Invert",
        command=lambda: perform_operation("Invert"),
        fg_color="red",
    )
    zoom_out_button.pack(side=tk.LEFT, padx=5)

    zoom_out_x1_button = CTkButton(
        button_frame_line3,
        text="Solarize",
        command=lambda: perform_operation("Solarize"),
        fg_color="red",
    )
    zoom_out_x1_button.pack(side=tk.LEFT, padx=5)

    save_button = CTkButton(
        button_frame_line3, text="Save", command=save_image, fg_color="green"
    )
    save_button.pack(side=tk.LEFT, padx=5)

    undo_button = CTkButton(
        button_frame_line3,
        text="Undo",
        command=lambda: perform_operation("Undo"),
        fg_color="blue",
    )
    undo_button.pack(side=tk.LEFT, padx=5)

    # Label to display the name
    name_label = CTkLabel(
        root, text="Muhammad Hasnat Rasool", font=("Arial", 20), fg_color="green"
    )
    name_label.place(x=560, y=590, anchor="s")
    name_label = CTkLabel(
        root,
        text="Copyright &copy; 2024 by Codingiseasy",
        font=("Arial", 20),
        fg_color="red",
    )
    name_label.place(x=560, y=650, anchor="s")
    # root.configure(fg_color="grey")
    root.mainloop()


# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
