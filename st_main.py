# import streamlit as st
# from PIL import Image
# import io
# from reportlab.pdfgen.canvas import Canvas
# import tempfile
# import base64

# # Function to convert image to dice representation
# def convert_to_dice_representation(image_path, num_dice_wide, num_dice_tall):
#     source_image = Image.open(image_path)
#     die_one = Image.open("DiceImages/DiceImages/1.png")
#     die_two = Image.open("DiceImages/DiceImages/2.png")
#     die_three = Image.open("DiceImages/DiceImages/3.png")
#     die_four = Image.open("DiceImages/DiceImages/4.png")
#     die_five = Image.open("DiceImages/DiceImages/5.png")
#     die_six = Image.open("DiceImages/DiceImages/6.png")

#     dice_image_width, dice_image_height = die_one.size
#     resized_image = source_image.resize((num_dice_wide, num_dice_tall))
#     resized_image = resized_image.convert('L')
#     pix_val = list(resized_image.getdata())

#     for i in range(len(pix_val)):
#         if pix_val[i] < 42:
#             pix_val[i] = 1
#         elif 42 <= pix_val[i] < 84:
#             pix_val[i] = 2
#         elif 84 <= pix_val[i] < 126:
#             pix_val[i] = 3
#         elif 126 <= pix_val[i] < 168:
#             pix_val[i] = 4
#         elif 168 <= pix_val[i] < 210:
#             pix_val[i] = 5
#         else:
#             pix_val[i] = 6

#     output_image_size = (dice_image_width * num_dice_wide, dice_image_height * num_dice_tall)
#     output_image = Image.new('L', output_image_size, color=0)

#     for i in range(len(pix_val)):
#         x_location = int((int(dice_image_width) * i)) % (dice_image_width * num_dice_wide)
#         y_location = int(i / num_dice_wide) * dice_image_height
#         if pix_val[i] == 1:
#             output_image.paste(die_one, (x_location, y_location))
#         elif pix_val[i] == 2:
#             output_image.paste(die_two, (x_location, y_location))
#         elif pix_val[i] == 3:
#             output_image.paste(die_three, (x_location, y_location))
#         elif pix_val[i] == 4:
#             output_image.paste(die_four, (x_location, y_location))
#         elif pix_val[i] == 5:
#             output_image.paste(die_five, (x_location, y_location))
#         elif pix_val[i] == 6:
#             output_image.paste(die_six, (x_location, y_location))

#     return output_image

# # Function to convert PIL Image to bytes
# def ImageToBytes(image):
#     img_byte_array = io.BytesIO()
#     image.save(img_byte_array, format='PNG')
#     return img_byte_array.getvalue()

# # Streamlit app
# def main():
#     st.title("Dice Image Generator")

#     # Upload image through Streamlit
#     uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:
#         num_dice_wide = st.number_input("Number of dice wide:", min_value=1, max_value=100, value=50)
#         num_dice_tall = st.number_input("Number of dice tall:", min_value=1, max_value=100, value=50)

#         st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

#         if st.button("Generate Dice Image"):
#             output_image = convert_to_dice_representation(uploaded_file, int(num_dice_wide), int(num_dice_tall))
#             st.image(output_image, caption="Generated Dice Image.", use_column_width=True)
#             st.success("Image generated successfully!")

#             # Download button for the generated image
#             image_bytes = ImageToBytes(output_image)
#             download_link_image = f'<a href="data:image/png;base64,{base64.b64encode(image_bytes).decode()}" download="generated_image.png">Download Generated Image</a>'
#             st.markdown(download_link_image, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

import streamlit as st
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import base64
st.set_page_config(page_title='Push Pin Art')
def floyd_steinberg_dithering(image, color_mapping):
    image = image.convert("RGB")
    width, height = image.size
    dithered_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(dithered_image)

    for y in range(1, height):
        for x in range(1, width):
            old_pixel = image.getpixel((x, y))
            new_pixel = find_closest_color(old_pixel, color_mapping)

            dithered_image.putpixel((x, y), new_pixel)

            quant_error = [old - new_ for old, new_ in zip(old_pixel, new_pixel)]

            for dx, dy, weight in [(1, 0, 7/16), (-1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_pixel = find_closest_color(image.getpixel((nx, ny)), color_mapping)
                    image.putpixel((nx, ny), tuple(map(lambda x: int(x[0] + x[1] * weight), zip(image.getpixel((nx, ny)), quant_error))))
    return dithered_image

def find_closest_color(pixel_color, color_mapping):
    closest_color = min(color_mapping, key=lambda c: sum((a - b) ** 2 for a, b in zip(pixel_color, c)))
    return closest_color

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        st.error(f"Invalid color format: {hex_color}")
        return (0, 0, 0)

def rgb_to_hex(rgb):
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def convert_image_to_pdf_with_grid(image, pdf, pdf_size, margin=0, grid_color="black", user_colors=None):
    img_width, img_height = image.size

    scale_factor_width = (pdf_size[0] - 2 * margin) / img_width
    scale_factor_height = (pdf_size[1] - 2 * margin) / img_height
    scale_factor = min(scale_factor_width, scale_factor_height)

    scaled_width = img_width * scale_factor
    scaled_height = img_height * scale_factor

    x_position = margin
    y_position = margin

    cell_size_x = scaled_width / img_width
    cell_size_y = scaled_height / img_height

    pdf.showPage()
    pdf.drawInlineImage(image, x_position, y_position, width=scaled_width, height=scaled_height)

    pdf.setStrokeColor(grid_color)

    for i in range(img_width + 1):
        x = x_position + i * cell_size_x
        pdf.line(x, y_position, x, y_position + scaled_height)

    for j in range(img_height + 1):
        y = y_position + j * cell_size_y
        pdf.line(x_position, y, x_position + scaled_width, y)

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, bytes):
        b64 = base64.b64encode(object_to_download).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def divide_push_pin_art_into_a3_pages_and_convert_to_pdf(push_pin_art_image, user_colors=None):
    push_pin_art_width, push_pin_art_height = push_pin_art_image.size

    num_pages_width, num_pages_height = calculate_a3_pages(push_pin_art_width, push_pin_art_height)

    pdf_output_path = os.path.join(os.getcwd(), "output.pdf")
    pdf = canvas.Canvas(pdf_output_path, pagesize=letter)

    max_pixels_per_page = calculate_max_pixels_per_page(push_pin_art_width, push_pin_art_height, num_pages_width, num_pages_height)

    for page_row in range(num_pages_height):
        for page_col in range(num_pages_width):
            start_col = page_col * max_pixels_per_page[0]
            end_col = (page_col + 1) * max_pixels_per_page[0]
            start_row = page_row * max_pixels_per_page[1]
            end_row = (page_row + 1) * max_pixels_per_page[1]

            page_image = push_pin_art_image.crop((start_col, start_row, end_col, end_row))

            total_pixels = page_image.width * page_image.height

            # st.write(f"Page {page_row * num_pages_width + page_col + 1}:")
            # st.write(f" - Width: {page_image.width}")
            # st.write(f" - Height: {page_image.height}")
            # st.write(f" - Total Pixels: {total_pixels}")

            convert_image_to_pdf_with_grid(page_image, pdf, pdf_size=(letter[0], letter[1]), margin=10, grid_color="black", user_colors=user_colors)

    pdf.save()

def calculate_a3_pages(image_width, image_height):
    a3_width_cm = 29.7
    a3_height_cm = 42.0

    pixels_per_cm = 1
    pixels_per_page_width = int(a3_width_cm * pixels_per_cm)
    pixels_per_page_height = int(a3_height_cm * pixels_per_cm)

    num_pages_width = image_width // pixels_per_page_width + (image_width % pixels_per_page_width > 0)
    num_pages_height = image_height // pixels_per_page_height + (image_height % pixels_per_page_height > 0)

    return num_pages_width, num_pages_height

def calculate_max_pixels_per_page(image_width, image_height, num_pages_width, num_pages_height):
    max_pixels_width = image_width // num_pages_width
    max_pixels_height = image_height // num_pages_height

    return max_pixels_width, max_pixels_height

def main():
    st.title("Push Pin Art")
    
    st.header("CENTER FOR CREATIVE LEARNING")
    st.text('Options')
    total_pixels = st.text_input("Total Pins:", "")
    input_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif"])
    
    num_colors = st.number_input("Number of Colors", min_value=1, value=1, step=1)

    color_mapping = []
    for i in range(num_colors):
        color = st.color_picker(f"Select Color {i+1}")
        color_mapping.append(hex_to_rgb(color))
    
    if st.button("Apply Dithering"):
        if not input_image:
            st.error("Please upload an image.")
            return

        if not total_pixels.isdigit():
            st.error("Invalid input. Please enter a valid integer for total pixels.")
            return

        if len(color_mapping) < 2:
            st.error("Please select at least two colors.")
            return

        total_pixels = int(total_pixels)
        input_image = Image.open(input_image)
        aspect_ratio = input_image.width / input_image.height
        new_width = int((total_pixels * aspect_ratio) ** 0.5)
        new_height = int(total_pixels / new_width)
        resized_image = input_image.resize((new_width, new_height))
        dithered_image = floyd_steinberg_dithering(resized_image, color_mapping)

        st.subheader("Original Image")
        st.image(input_image, caption="Original Image", use_column_width=True)

        st.subheader("Dithered Image")
        st.image(dithered_image, caption="Dithered Image", use_column_width=True)

        # Save the output image
        output_path_image = os.path.join(os.getcwd(), "output_image.png")
        dithered_image.save(output_path_image)

        # Save the PDF with parts and grid
        divide_push_pin_art_into_a3_pages_and_convert_to_pdf(dithered_image)

        # Display download links
        st.markdown(download_link(open(output_path_image, 'rb').read(), "output_image.png", "Download Output Image"), unsafe_allow_html=True)
        
        pdf_output_path = os.path.join(os.getcwd(), "output.pdf")
        st.markdown(download_link(open(pdf_output_path, 'rb').read(), "output.pdf", "Download Output PDF"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
