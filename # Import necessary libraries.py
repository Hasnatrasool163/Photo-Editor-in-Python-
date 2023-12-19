# Import necessary libraries
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageTk

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

def adjust_color(image_path, output_path, hue, saturation, color_balance):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color_balance)

    img = img.convert("HSV")
    img = ImageEnhance.Color(img).enhance(saturation)
    img = img.convert("RGB")

    img = img.convert("HSV")
    img = ImageEnhance.Color(img).enhance(color_balance)
    img = img.convert("RGB")

    img = img.convert("HSV")
    img = img.point(lambda i: (i + hue) % 256)
    img = img.convert("RGB")

    img.save(output_path)
    return img

# Function to perform a rectangle or ellipse selection
def perform_selection(image_path, output_path, selection_type):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # User selects a rectangle
    if selection_type == "Rectangle Selection":
        coordinates = simpledialog.askstring("Input", "Enter coordinates (x1,y1,x2,y2):")
        coordinates = tuple(map(int, coordinates.split(',')))
        draw.rectangle(coordinates, outline="red", width=2)

    # User selects an ellipse
    elif selection_type == "Ellipse Selection":
        coordinates = simpledialog.askstring("Input", "Enter coordinates (x1,y1,x2,y2):")
        coordinates = tuple(map(int, coordinates.split(',')))
        draw.ellipse(coordinates, outline="red", width=2)

    img.save(output_path)
    return img

def draw_text(image_path, output_path, text, font, color, position):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=color)
    img.save(output_path)
    return img

# Function to allow user to draw on the image
def allow_drawing(image_path, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Function to handle mouse clicks for drawing
    def draw_on_click(event):
        x, y = event.x, event.y
        draw.rectangle([x - 5, y - 5, x + 5, y + 5], fill="black")  # Draw a small rectangle on click
        img_label.photo = ImageTk.PhotoImage(img)
        img_label.config(image=img_label.photo)

    # Bind the click event to the drawing function
    img_label.bind("<B1-Motion>", draw_on_click)

    # Prompt user to press a key to finish drawing
    messagebox.showinfo("Drawing", "Click and drag on the image to draw. Press any key to finish.")
    img_label.unbind("<B1-Motion>")  # Unbind the click event after drawing

    img.save(output_path)
    return img

# Function to zoom in on the image
def zoom_in(image_path, output_path):
    img = Image.open(image_path)
    img = img.resize((int(img.width * 1.2), int(img.height * 1.2)), Image.ANTIALIAS)
    img.save(output_path)
    return img

# Function to zoom out on the image
def zoom_out(image_path, output_path):
    img = Image.open(image_path)
    img = img.resize((int(img.width / 1.2), int(img.height / 1.2)), Image.ANTIALIAS)
    img.save(output_path)
    return img

# Function to adjust curves and levels
def adjust_curves_levels(image_path, output_path, curves_factor, levels_factor):
    img = Image.open(image_path)

    # Adjust curves
    img = img.point(lambda i: i * curves_factor)

    # Adjust levels
    img = img.convert("RGB")
    r, g, b = img.split()
    r = r.point(lambda i: i * levels_factor)
    g = g.point(lambda i: i * levels_factor)
    b = b.point(lambda i: i * levels_factor)
    img = Image.merge("RGB", (r, g, b))

    img.save(output_path)
    return img

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
def draw_on_image(image_path, output_path, drawing_info):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    for info in drawing_info:
        draw.rectangle(info["coordinates"], outline=info["color"], width=info["width"])

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

# Function for batch processing of images
def batch_processing(images, operation):
    processed_images = []

    for image_path in images:
        if operation == "Blur":
            processed_img = apply_blur(image_path, output_path)
        elif operation == "Grayscale":
            processed_img = apply_grayscale(image_path, output_path)
        # Add more operations as needed
        else:
            print("Invalid operation selected.")
            return

        processed_images.append(processed_img)

    return processed_images

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
                # Allow the user to draw on the image
                drawing_info = []
                while True:
                    coordinates = simpledialog.askstring("Input", "Enter coordinates (x1,y1,x2,y2):")
                    if not coordinates:
                        break
                    color = simpledialog.askstring("Input", "Enter color:")
                    width = simpledialog.askinteger("Input", "Enter width:")
                    drawing_info.append({
                        "coordinates": tuple(map(int, coordinates.split(','))),
                        "color": color,
                        "width": width
                    })
                modified_img = draw_on_image(input_image, output_path, drawing_info)
            elif operation == "Collage Maker":
                images = [input_image] * 3
                modified_img = create_collage(images, output_path)
            elif operation == "Red-eye Removal":
                modified_img = remove_red_eye(input_image, output_path)
            elif operation == "Batch Processing":
                images = [input_image] * 3
                processed_images = batch_processing(images, "Blur")
                modified_img = processed_images[0]
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

    brightness_slider = tk.Scale(root, label="Brightness", from_=0.1, to=3.0, orient="horizontal", resolution=0.1)
    brightness_slider.pack()

    contrast_slider = tk.Scale(root, label="Contrast", from_=0.1, to=3.0, orient="horizontal", resolution=0.1)
    contrast_slider.pack()

    def update_brightness_contrast(event):
        brightness_factor = brightness_slider.get()
        contrast_factor = contrast_slider.get()

        if original_img:
            modified_img = original_img.copy()

            # Adjust brightness
            modified_img = adjust_brightness(modified_img, factor=brightness_factor)

            # Adjust contrast
            modified_img = adjust_contrast(modified_img, factor=contrast_factor)

            # Update the modified image label
            update_image_label(modified_image_label, modified_img)

    brightness_slider = tk.Scale(root, label="Brightness", from_=0.1, to=3.0, orient=tk.HORIZONTAL)
    brightness_slider.pack(side=tk.TOP, pady=5)

    contrast_slider = tk.Scale(root, label="Contrast", from_=0.1, to=3.0, orient=tk.HORIZONTAL)
    contrast_slider.pack(side=tk.TOP, pady=5)

    hue_slider = tk.Scale(root, label="Hue", from_=-180, to=180, orient=tk.HORIZONTAL)
    hue_slider.pack(side=tk.TOP, pady=5)

    saturation_slider = tk.Scale(root, label="Saturation", from_=0, to=2.0, orient=tk.HORIZONTAL)
    saturation_slider.pack(side=tk.TOP, pady=5)

    color_balance_slider = tk.Scale(root, label="Color Balance", from_=0.1, to=3.0, orient=tk.HORIZONTAL)
    color_balance_slider.pack(side=tk.TOP, pady=5)

    # Dropdown menu for artistic filters
    selected_filter = tk.StringVar()
    artistic_filter_dropdown = tk.OptionMenu(root, selected_filter, "Filter 1", "Filter 2", "Filter 3", command=lambda x: perform_operation("Artistic Filter", x))
    artistic_filter_dropdown.pack(side=tk.TOP, pady=5)

    # Buttons for selection tools
    rectangle_selection_button = tk.Button(button_frame_line2, text="Rectangle Selection", command=lambda: perform_selection(file_path_var.get(), output_path, "Rectangle Selection"), fg="red")
    rectangle_selection_button.pack(side=tk.LEFT, padx=5)

    ellipse_selection_button = tk.Button(button_frame_line2, text="Ellipse Selection", command=lambda: perform_selection(file_path_var.get(), output_path, "Ellipse Selection"), fg="red")
    ellipse_selection_button.pack(side=tk.LEFT, padx=5)

    # Sliders for advanced color editing
    curves_slider = tk.Scale(root, label="Curves", from_=0.1, to=3.0, orient=tk.HORIZONTAL)
    curves_slider.pack(side=tk.TOP, pady=5)

    levels_slider = tk.Scale(root, label="Levels", from_=0.1, to=3.0, orient=tk.HORIZONTAL)
    levels_slider.pack(side=tk.TOP, pady=5)

    # Button to apply adjustments
    apply_adjustments_button = tk.Button(button_frame_line2, text="Apply Adjustments", command=lambda: perform_advanced_operation("Adjust Color", brightness_slider.get(), contrast_slider.get(), hue_slider.get(), saturation_slider.get(), color_balance_slider.get()))
    apply_adjustments_button.pack(side=tk.LEFT, padx=5)

    # Button to apply curves and levels adjustments
    apply_curves_levels_button = tk.Button(button_frame_line2, text="Apply Curves & Levels", command=lambda: perform_advanced_operation("Adjust Curves & Levels", curves_slider.get(), levels_slider.get()))
    apply_curves_levels_button.pack(side=tk.LEFT, padx=5)
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
    
    draw_button = tk.Button(button_frame_line2, text="Draw", command=lambda: perform_drawing(file_path_var.get(), output_path), fg="red")
    draw_button.pack(side=tk.LEFT, padx=5)

    # Buttons for zooming in and out
    zoom_in_button = tk.Button(button_frame_line3, text="Zoom In", command=lambda: perform_operation("Zoom In"), fg="purple")
    zoom_in_button.pack(side=tk.LEFT, padx=5)

    zoom_out_button = tk.Button(button_frame_line3, text="Zoom Out", command=lambda: perform_operation("Zoom Out"), fg="purple")
    zoom_out_button.pack(side=tk.LEFT, padx=5)
    save_button = tk.Button(button_frame_line3, text="Save", command=save_image,fg="green")
    save_button.pack(side=tk.LEFT, padx=5)

    undo_button = tk.Button(button_frame_line3, text="Undo", command=lambda: perform_operation("Undo"),fg="blue")
    undo_button.pack(side=tk.LEFT, padx=5)

    # Label to display the name
    name_label = tk.Label(root, text="Muhammad Hasnat Rasool", font=("Arial", 20), fg="green")
    name_label.place(relx=1, rely=1, anchor="se")

    # Start the main event loop
    root.mainloop()

# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
