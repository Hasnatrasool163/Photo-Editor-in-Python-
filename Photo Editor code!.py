# Import necessary libraries
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageTk,ImageFont

# List to store the history of recent operations
recent_operations = []

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

# Variable to store the original image
original_img = None

# Main function to create the GUI
def main():
    root = tk.Tk()
    root.title("Photo Editor")
    root.geometry("800x500")

    # Label to display the original image
    original_image_label = tk.Label(root, text="Original Image")
    original_image_label.pack(pady=10)

    # Label to display the modified image
    modified_image_label = tk.Label(root, text="Modified Image")
    modified_image_label.pack(pady=10)

    # Variable to store the file path
    file_path_var = tk.StringVar()

    # Function to perform image operations
    def perform_operation(operation):
        global original_img
        input_image = file_path_var.get()
        output_path = None  # Declare output_path outside of if-else block

        # Undo operation
        if operation == "Undo":
            modified_img = original_img.copy()
            update_image_label(modified_image_label, modified_img)
        else:
            if not input_image:
                print("No image selected. Please upload an image first.")
                return

            original_img = Image.open(input_image)
            output_path = input_image.replace(".", f"_{operation}.")

            # Perform specific operation based on user choice
            if operation == "Blur":
                modified_img = apply_blur(input_image, output_path)
            elif operation == "Grayscale":
                modified_img = apply_grayscale(input_image, output_path)
            elif operation == "Sepia":
                modified_img = apply_sepia(input_image, output_path)
            elif operation == "Brighten":
                modified_img = adjust_brightness(input_image, output_path, factor=1.5)
            elif operation == "Contrast":
                modified_img = adjust_contrast(input_image, output_path, factor=1.5)
            elif operation == "Rotate":
                angle = simpledialog.askfloat("Input", "Enter rotation angle:")
                modified_img = rotate_image(input_image, output_path, angle)
            elif operation == "Flip Horizontal":
                modified_img = flip_image(input_image, output_path, direction='horizontal')
            elif operation == "Flip Vertical":
                modified_img = flip_image(input_image, output_path, direction='vertical')
            elif operation == "Crop & Resize":
                dimensions = simpledialog.askstring("Input", "Enter dimensions (width,height):")
                dimensions = tuple(map(int, dimensions.split(',')))
                modified_img = crop_and_resize(input_image, output_path, dimensions)
            elif operation == "Artistic Filter":
                modified_img = apply_artistic_filter(input_image, output_path)
            elif operation == "Text Overlay":
                modified_img = add_text_overlay(input_image, output_path, "Overlay Text", font=None, color="black", position=(50, 50))
            elif operation == "Drawing":
                drawing_info = []
                initial_text = "Type here"
                drawing_info.append({"color": "black",  "width": 2,  "text": initial_text})
                modified_img = draw_on_image_with_centered_textbox(input_image, output_path, drawing_info)
            elif operation == "Collage Maker":
                images = [input_image] * 3
                modified_img = create_collage(images, output_path)
            elif operation == "Red-eye Removal":
                modified_img = remove_red_eye(input_image, output_path)
            elif operation.startswith("Zoom In"):
                level_str = operation.split(" ")[-1][1:]  # Extract the numeric part from the operation
                level = int(level_str)
                output_path = input_image.replace(".", f"_ZoomIn_x{level}.")
                modified_img = apply_zoom_in(input_image, output_path, level)
            elif operation.startswith("Zoom Out"):
                level_str = operation.split(" ")[-1][1:]  # Extract the numeric part from the operation
                level = int(level_str)
                output_path = input_image.replace(".", f"_ZoomOut_x{level}.")
                modified_img = apply_zoom_out(input_image, output_path, level)
            else:
                print("Invalid operation selected.")
                return

            # Update recent_operations
            recent_operations.append(operation)
            print(f"{operation} applied.")
            update_image_label(modified_image_label, modified_img)

    # Function to save the modified image
    def save_image():
        if modified_image_label.photo:
            output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                                    ("All files", "*.*")])
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


    # Button to upload an image
    upload_button = tk.Button(root, text="Upload Image", command=upload_image)
    upload_button.pack(side=tk.TOP, pady=10)

    # Button frame for the first line of buttons
    button_frame_line1 = tk.Frame(root)
    button_frame_line1.pack(side=tk.TOP, pady=10)

    blur_button = tk.Button(button_frame_line1, text="Blur", command=lambda: perform_operation("Blur"), fg="red")
    blur_button.pack(side=tk.LEFT, padx=5)

    grayscale_button = tk.Button(button_frame_line1, text="Grayscale", command=lambda: perform_operation("Grayscale"), fg="red")
    grayscale_button.pack(side=tk.LEFT, padx=5)

    sepia_button = tk.Button(button_frame_line1, text="Sepia", command=lambda: perform_operation("Sepia"), fg="red")
    sepia_button.pack(side=tk.LEFT, padx=5)

    brighten_button = tk.Button(button_frame_line1, text="Brighten", command=lambda: perform_operation("Brighten"), fg="red")
    brighten_button.pack(side=tk.LEFT, padx=5)

    contrast_button = tk.Button(button_frame_line1, text="Contrast", command=lambda: perform_operation("Contrast"), fg="red")
    contrast_button.pack(side=tk.LEFT, padx=5)

    rotate_button = tk.Button(button_frame_line1, text="Rotate", command=lambda: perform_operation("Rotate"), fg="red")
    rotate_button.pack(side=tk.LEFT, padx=5)

    flip_horizontal_button = tk.Button(button_frame_line1, text="Flip Horizontal", command=lambda: perform_operation("Flip Horizontal"), fg="red")
    flip_horizontal_button.pack(side=tk.LEFT, padx=5)

    flip_vertical_button = tk.Button(button_frame_line1, text="Flip Vertical", command=lambda: perform_operation("Flip Vertical"), fg="red")
    flip_vertical_button.pack(side=tk.LEFT, padx=5)

   # Button frame for the second line of buttons
    button_frame_line2 = tk.Frame(root)
    button_frame_line2.pack(side=tk.TOP, pady=10)

    crop_resize_button = tk.Button(button_frame_line2, text="Crop & Resize", command=lambda: perform_operation("Crop & Resize"), fg="red")
    crop_resize_button.pack(side=tk.LEFT, padx=5)

    artistic_filter_button = tk.Button(button_frame_line2, text="Artistic Filter", command=lambda: perform_operation("Artistic Filter"), fg="red")
    artistic_filter_button.pack(side=tk.LEFT, padx=5)

    text_overlay_button = tk.Button(button_frame_line2, text="Text Overlay", command=lambda: perform_operation("Text Overlay"), fg="red")
    text_overlay_button.pack(side=tk.LEFT, padx=5)

    drawing_button = tk.Button(button_frame_line2, text="Drawing", command=lambda: perform_operation("Drawing"), fg="red")
    drawing_button.pack(side=tk.LEFT, padx=5)

    collage_button = tk.Button(button_frame_line2, text="Collage Maker", command=lambda: perform_operation("Collage Maker"), fg="red")
    collage_button.pack(side=tk.LEFT, padx=5)

    red_eye_button = tk.Button(button_frame_line2, text="Red-eye Removal", command=lambda: perform_operation("Red-eye Removal"), fg="red")
    red_eye_button.pack(side=tk.LEFT, padx=5)

    batch_processing_button = tk.Button(button_frame_line2, text="Batch Processing", command=lambda: perform_operation("Batch Processing"), fg="red")
    batch_processing_button.pack(side=tk.LEFT, padx=5)

    history_panel_button = tk.Button(button_frame_line2, text="History Panel", command=display_history_panel, fg="red")
    history_panel_button.pack(side=tk.LEFT, padx=5)

    # Line for "Save" and "Undo" buttons
    button_frame_line3 = tk.Frame(root)
    button_frame_line3.pack(side=tk.TOP, pady=10)
    
    zoom_in_button = tk.Button(button_frame_line3, text="Zoom In x2", command=lambda: perform_operation("Zoom In x2"), fg="red")
    zoom_in_button.pack(side=tk.LEFT, padx=5)

    zoom_out_button = tk.Button(button_frame_line3, text="Zoom Out x2", command=lambda: perform_operation("Zoom Out x2"), fg="red")
    zoom_out_button.pack(side=tk.LEFT, padx=5)

    zoom_out_x1_button = tk.Button(button_frame_line3, text="Zoom Out x1", command=lambda: perform_operation("Zoom Out x1"), fg="red")
    zoom_out_x1_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame_line3, text="Save", command=save_image,fg="green")
    save_button.pack(side=tk.LEFT, padx=5)

    undo_button = tk.Button(button_frame_line3, text="Undo", command=lambda: perform_operation("Undo"),fg="blue")
    undo_button.pack(side=tk.LEFT, padx=5)

    # Label to display the name
    name_label = tk.Label(root, text="Muhammad Hasnat Rasool", font=("Arial", 20), fg="green")
    name_label.place(relx=1, rely=1, anchor="se")

    root.mainloop()

# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
