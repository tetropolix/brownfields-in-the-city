import base64
import json
import os
import random
import requests  # type: ignore
from urllib3 import encode_multipart_formdata
from urllib3.fields import RequestField


api_url = "http://localhost:8000/brownfields/insert"


def load_mockups() -> list:
    with open("./MOCK_DATA.json") as f:
        data = json.load(f)
    return data


def read_files() -> list:
    files = []
    for f in os.listdir("./images"):
        with open("./images/" + f, "rb") as file:
            files.append(("files", (f, file.read(), "image/jpg")))
    return files


def insert_brownfield(api_url, data: str, files: list):
    fields = [("data", data)] + files
    body, header = encode_multipart_formdata(fields)
    response = requests.post(api_url, headers={"Content-Type": header}, data=body)
    if response.status_code > 299:
        exit(1)
    print("OK - " + str(response.json()))


if __name__ == "__main__":
    files = read_files()
    print(len(files))
    for row in load_mockups():
        insert_brownfield(
            api_url,
            json.dumps(row),
            random.sample(files, random.randint(0, len(files))),
        )
        exit(0)
