import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Define the API endpoint
url = "http://127.0.0.1:8000/remove-background/"

# Define the image to be processed
image_path = "images/MSSADDLOCS03112024DA-01.jpg"
#image_path = "images/MSSADDLOCS03112024DA-05.jpg"
#image_path = "images/pessoa.jpeg"
#image_path = "images/caneca.jpeg"

API_KEY = os.getenv("API_KEY")

def test_background_removal(api_key: str, add_white_background: bool, output_filename: str, centralize_object: bool = True):
    output_path = os.path.join("images", output_filename)

    # Open the image file
    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
        data = {"filename": output_filename, "add_white_background": str(add_white_background), "centralize_object": str(centralize_object)}
        headers = {"X-API-Key": api_key}

        # Make the request
        response = requests.post(url, files=files, data=data, headers=headers)

    # Check the response
    if response.status_code == 200:
        # Save the result
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Successfully removed background and saved image to {output_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Test with correct API key and white background (JPG)
print("\n--- Testing with CORRECT API Key (JPG, white background) ---")
test_background_removal(API_KEY, True, "removed_background_white_jpg.jpg", True)


# Test with correct API key and transparent background (PNG)
print("\n--- Testing with CORRECT API Key (PNG, transparent background) ---")
test_background_removal(API_KEY, False, "removed_background_transparent_png.png", True)

# Test with correct API key and white background (PNG)
print("\n--- Testing with CORRECT API Key (PNG, white background) ---")
test_background_removal(API_KEY, True, "removed_background_white_png.png", True)

# Test with correct API key and transparent background (JPG - will be black)
print("\n--- Testing with CORRECT API Key (JPG, transparent background - will be black) ---")
test_background_removal(API_KEY, False, "removed_background_black_jpg.jpg", True)

# Test with incorrect API key
print("\n--- Testing with INCORRECT API Key ---")
test_background_removal("WRONG_API_KEY", True, "removed_background_white_incorrect_key.jpg", True)

# Test with correct API key and white background (JPG) without centralization
print("\n--- Testing with CORRECT API Key (JPG, white background) without centralization ---")
test_background_removal(API_KEY, True, "removed_background_white_no_centralization_jpg.jpg", False)
