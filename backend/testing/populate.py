import base64
import json
import os
import random
import time
import requests  # type: ignore
from urllib3 import encode_multipart_formdata
from urllib3.fields import RequestField


api_url = "http://localhost:8000/brownfields/insert"
time_between_requests = 0.1 #in sec


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
    return requests.post(api_url, headers={"Content-Type": header}, data=body)


if __name__ == "__main__":
    files = read_files()
    for row in load_mockups():
        response = insert_brownfield(
            api_url,
            json.dumps(row),
            random.sample(files, random.randint(0, len(files))),
        )
        if response.status_code > 299:
            exit(1)
        print("OK - " + str(response.json()))
        time.sleep(time_between_requests)
