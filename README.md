# Background Remover API

This project provides a FastAPI application to remove the background from images using the `rembg` library. It offers an API endpoint to upload an image and receive the processed image with its background removed, with options for adding a white or black background, and centralizing the main object.

## Features

- Remove image background.
- Add a white or black background to the processed image.
- Centralize the main object within a padded frame (5% margin).
- API Key authentication for secure access.

## Setup

### Prerequisites

- Python 3.11+
- `pip` (Python package installer)
- `uvicorn` (ASGI server for FastAPI)
- `Docker` (optional, for containerized deployment)

### Local Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/antoniocostabr/background_remover.git
    cd background_remover
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**

    Create a `.env` file in the root directory of the project and add your API key:

    ```dotenv
    API_KEY="your_strong_api_key_here"
    ```

    You can generate a strong API key using Python:

    ```bash
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    ```

### Docker Installation (Recommended)

1.  **Build the Docker image:**

    Navigate to the project root directory and run:

    ```bash
    docker build -t background-remover .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 --env API_KEY='your_strong_api_key_here' background-remover
    ```

    Replace `'your_strong_api_key_here'` with your actual API key.

## Running the Application

### Locally

Make sure your virtual environment is activated and your `.env` file is set up.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://127.0.0.1:8000`.

### With Docker

If you followed the Docker installation steps, the application should already be running after executing the `docker run` command.

## API Usage

The API provides a single endpoint for background removal.

### Endpoint

`POST /remove-background/`

### Parameters

-   **`file`** (File, required): The image file to process.
-   **`filename`** (Form, optional): The desired output filename for the processed image. Defaults to `background_removed.jpg`.
-   **`add_white_background`** (Form, optional): Boolean. If `True`, a white background is added. If `False`, the image will have a transparent background (PNG output) or a black background (JPG output). Defaults to `True`.
-   **`centralize_object`** (Form, optional): Boolean. If `True`, the main object will be centralized within a padded frame (5% margin). If `False`, the object will be pasted at the top-left corner. Defaults to `True`.

### Authentication

Include your API key in the `X-API-Key` header for all requests.

### Example Request (using `curl`)

```bash
curl -X POST "http://127.0.0.1:8000/remove-background/" \
  -H "X-API-Key: your_strong_api_key_here" \
  -F "file=@/path/to/your/image.jpg" \
  -F "filename=my_processed_image.png" \
  -F "add_white_background=false" \
  -F "centralize_object=true" \
  --output processed_image.png
```

Replace `/path/to/your/image.jpg` with the actual path to your image file and `your_strong_api_key_here` with your API key.

## Running Tests

To run the test suite, ensure your virtual environment is activated and the API is running (either locally or via Docker).

```bash
python test_api.py
```

This will send requests to the running API and save the processed images in the `images/` directory.