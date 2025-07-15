# Background Remover API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful and easy-to-use FastAPI application for removing backgrounds from images. This API leverages the `rembg` library to provide high-quality background removal, with options to add a solid background color and center the main object.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Docker (Recommended)](#docker-recommended)
  - [Local Setup](#local-setup)
- [Running the Application](#running-the-application)
  - [With Docker](#with-docker)
  - [Locally](#locally)
- [API Usage](#api-usage)
  - [Endpoint](#endpoint)
  - [Authentication](#authentication)
  - [Parameters](#parameters)
  - [Example with `curl`](#example-with-curl)
  - [Example with Python `requests`](#example-with-python-requests)
- [Testing](#testing)
- [License](#license)

## Features

-   **High-Quality Background Removal**: Utilizes `rembg` for seamless background removal.
-   **Customizable Backgrounds**: Option to add a white or black background to the processed image.
-   **Object Centering**: Automatically centralizes the main object within a padded frame (5% margin).
-   **API Key Authentication**: Secure your API endpoint with API key authentication.
-   **Dockerized**: Comes with a `Dockerfile` and `Makefile` for easy containerization and deployment.

## Project Structure

```
/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── LICENSE
├── main.py
├── Makefile
├── README.md
├── requirements.txt
├── temp/
└── tests/
    ├── test_api.py
    ├── input/
    └── output/
```

## Getting Started

Follow these instructions to get the application up and running.

### Prerequisites

-   Python 3.11+
-   `pip` and `venv`
-   `make` (optional, for using Makefile shortcuts)
-   `Docker` (optional, for containerized deployment)

### Docker (Recommended)

This is the easiest way to get the application running.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/antoniocostabr/background_remover.git
    cd background_remover
    ```

2.  **Set up your API Key:**
    Create a `.env` file in the root directory. This file will store your API key.
    ```bash
    # Generate a secure API key
    python -c "import secrets; print(f'API_KEY={secrets.token_urlsafe(32)}')" > .env
    ```
    Your `.env` file should now contain a line like `API_KEY="your_strong_api_key_here"`.

3.  **Build and Run with Makefile:**
    Use the provided `Makefile` to build and run the Docker container in one step:
    ```bash
    make build-run-docker
    ```
    Alternatively, you can run the steps separately:
    ```bash
    # Build the image
    make build-docker

    # Run the container
    make run-docker
    ```

### Local Setup

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
    Create a `.env` file as described in the Docker setup section.

## Running the Application

### With Docker

If you followed the Docker setup, the application should already be running and accessible at `http://localhost:8000`.

### Locally

Ensure your virtual environment is activated and the `.env` file is present.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://127.0.0.1:8000`.

## API Usage

The API provides a single endpoint for background removal.

### Endpoint

`POST /remove-background/`

### Authentication

You must include your API key in the `X-API-Key` header for all requests.

### Parameters

| Parameter              | Type    | Description                                                                                                                            | Default                  |
| ---------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `file`                 | File    | **Required.** The image file to process.                                                                                               | N/A                      |
| `filename`             | String  | The desired output filename. The extension determines the output format (e.g., `.png`, `.jpg`).                                        | `background_removed.jpg` |
| `add_white_background` | Boolean | If `True`, adds a white background. If `False`, the background is transparent (for PNGs) or black (for JPEGs).                           | `True`                   |
| `centralize_object`    | Boolean | If `True`, centralizes the object with a 5% margin. If `False`, the object is placed at the top-left.                                    | `True`                   |
| `foreground_thresh`    | Integer | A value from 0 to 255 to threshold the foreground matte.                                                                                | `240`                    |
| `background_thresh`    | Integer | A value from 0 to 255 to threshold the background matte.                                                                                | `10`                     |

### Example with `curl`

```bash
curl -X POST "http://127.0.0.1:8000/remove-background/" \
  -H "X-API-Key: your_strong_api_key_here" \
  -F "file=@/path/to/your/image.jpg" \
  -F "filename=my_processed_image.png" \
  -F "add_white_background=false" \
  -F "centralize_object=true" \
  --output processed_image.png
```

### Example with Python `requests`

```python
import requests
import os

# It's recommended to load the API key from environment variables
api_key = os.getenv("API_KEY", "your_strong_api_key_here")
api_url = "http://127.0.0.1:8000/remove-background/"
image_path = "/path/to/your/image.jpg"

headers = {"X-API-Key": api_key}
files = {"file": (os.path.basename(image_path), open(image_path, "rb"), "image/jpeg")}
data = {
    "filename": "my_processed_image.png",
    "add_white_background": "false",
    "centralize_object": "true",
}

response = requests.post(api_url, headers=headers, files=files, data=data)

if response.status_code == 200:
    with open("processed_image.png", "wb") as f:
        f.write(response.content)
    print("Image processed successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Testing

The project includes an integration test script that calls the running API to verify its functionality.

1.  **Ensure the application is running** (either locally or with Docker).
2.  **Make sure your `.env` file is configured**, as the test script uses the `API_KEY` from it.
3.  **Run the test script:**
    ```bash
    python tests/test_api.py
    ```

The script will send several requests with different parameters to the API. The processed images will be saved in the `tests/output/` directory. You can inspect these files to verify the results.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
