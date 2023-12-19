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