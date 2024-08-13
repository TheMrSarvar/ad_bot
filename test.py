from PIL import Image, ImageDraw, ImageFont

def add_number_to_image(image_path, output_path, number, position="bottom-right", font_size=200, color=(255, 255, 255)):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        
        # Load a specific font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            print("Default font loaded as the specified font was not found.")
        
        # Convert the number to a string
        text = str(number)
        
        # Get text bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Determine position
        if position == "top-right":
            x = img.width - text_width - 10
            y = 10
        elif position == "top-left":
            x = 10
            y = 10
        elif position == "bottom-right":
            x = img.width - text_width - 10
            y = img.height - text_height - 10
        elif position == "bottom-left":
            x = 10
            y = img.height - text_height - 10
        else:
            raise ValueError("Invalid position. Choose from 'top-right', 'top-left', 'bottom-right', 'bottom-left'.")

        print(f"Drawing text '{text}' at position ({x}, {y}) with color {color} and font size {font_size}.")

        # Add the number to the image
        draw.text((x, y), text, font=font, fill=color)
        
        # Save the image
        img.save(output_path)
        print(f"Number {number} added to {position} of image and saved as {output_path}")

# Example usage with increased font size and strong contrast
add_number_to_image("image.jpg", "output.jpg", 42, position="top-left", font_size=50, color=(255, 255, 255))

