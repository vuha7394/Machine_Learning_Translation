import requests


def download_file_from_google_drive(file_id, destination, chunk_size=32768):
    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    params = {"id": file_id, "confirm": 1}
    response = session.get(url, params=params, stream=True)

    for i, chunk_size_ in save_response_content(response, destination, chunk_size):
        yield i, chunk_size_


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination, chunk_size):
    with open(destination, "wb") as f:
        for i, chunk in enumerate(response.iter_content(chunk_size)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                yield i, chunk_size
