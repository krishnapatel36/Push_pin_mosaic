
# Push Pin Art

This Streamlit application allows users to upload an image, apply Floyd-Steinberg dithering to it, and then convert the processed image into a PDF with a grid overlay. The app also lets users choose color mappings for dithering and view the resulting image and color counts.

## Overview

The application consists of several key functions:

1. **Floyd-Steinberg Dithering**: Applies dithering to the uploaded image to simulate a reduced color palette.
2. **Color Conversion**: Functions to convert between hex and RGB color formats.
3. **PDF Generation**: Converts the dithered image into a PDF with a grid overlay, dividing the image into multiple A3-sized pages if necessary.
4. **Streamlit Interface**: Provides a user-friendly interface to upload images, select colors, and download the processed results.

## Code Breakdown

### Floyd-Steinberg Dithering

```python
def floyd_steinberg_dithering(image, color_mapping):
    ...
```

This function applies Floyd-Steinberg dithering to an image using a specified color mapping. It converts the image to RGB, processes each pixel, and applies dithering errors to neighboring pixels.

### Color Conversion Functions

```python
def hex_to_rgb(hex_color):
    ...
def rgb_to_hex(rgb):
    ...
```

These functions convert colors between hex and RGB formats, ensuring the colors are correctly interpreted and used in dithering.

### PDF Conversion

```python
def convert_image_to_pdf_with_grid(image, pdf, pdf_size, margin=0, grid_color="black", user_colors=None, page_label=None):
    ...
def divide_push_pin_art_into_a3_pages_and_convert_to_pdf(push_pin_art_image, user_colors=None):
    ...
```

These functions convert the dithered image into a PDF format. The `convert_image_to_pdf_with_grid` function handles scaling and drawing the grid, while `divide_push_pin_art_into_a3_pages_and_convert_to_pdf` divides the image into A3-sized pages and adds them to the PDF.

### Streamlit Interface

```python
def main():
    st.title("Push Pin Art")
    ...
```

The `main` function creates the Streamlit app interface. It allows users to:
- Upload an image.
- Specify the number of colors and select colors for dithering.
- Apply dithering to the image.
- View the original and dithered images.
- Download the processed image and the resulting PDF.

## Usage

1. **Upload Image**: Upload an image file (PNG, JPG, JPEG, or GIF).
2. **Specify Number of Colors**: Choose the number of colors for dithering and select the colors.
3. **Apply Dithering**: Click the "Apply Dithering" button to process the image.
4. **View Results**: Check the original and dithered images, along with color counts.
5. **Download Results**: Download the processed image and PDF with the grid overlay.

## Installation

To run this application, make sure you have the following Python packages installed:

- `streamlit`
- `PIL` (Pillow)
- `reportlab`
- `base64`

You can install these packages using pip:

```bash
pip install streamlit pillow reportlab
```

## Running the Application

To run the Streamlit app, execute the following command in your terminal:

```bash
streamlit run your_script_name.py
```

Replace `your_script_name.py` with the name of your Python file containing the above code.
