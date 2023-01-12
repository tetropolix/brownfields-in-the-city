import base64
import json
import os
import random
import sys
import time
import requests  # type: ignore
from urllib3 import encode_multipart_formdata
from urllib3.fields import RequestField


api_url = "http://localhost:8000/brownfields/insert"
time_between_requests = 0.1  # in sec
longitude_min = 21.198261
longitude_max = 21.306751
latitude_min = 48.6819772
latitude_max = 48.7472172
min_val = 0.03
max_val = 0.11


def generate_polygon_middle(
    longitude_min: float, longitude_max: float, latitude_min: float, latitude_max: float
) -> tuple[float, float]:
    return (
        round(random.uniform(longitude_min, longitude_max), 6),
        round(random.uniform(latitude_min, latitude_max), 6),
    )


def generate_polygon_from_middle(
    middle: tuple[float, float], min: float, max: float
) -> list[tuple[float, float]]:
    polygon = []
    for _ in range(4):
        random_long = round(middle[0] + random.uniform(min_val, max_val), 6)
        random_lat = round(middle[1] + random.uniform(min_val, max_val), 6)
        polygon.append((random_long, random_lat))
    polygon.append(polygon[0])  # polygon must be closed with starting point
    return polygon


def load_mockups() -> list:
    with open("./MOCK_DATA.json") as f:
        data = json.load(f)
    for row in data:
        middle = generate_polygon_middle(
            longitude_min, longitude_max, latitude_min, latitude_max
        )
        row["polygon"] = generate_polygon_from_middle(middle, min_val, max_val)
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
    max_insert = None
    if len(sys.argv) > 1:
        max_insert = int(sys.argv[1])
    files = read_files()
    for i, row in enumerate(load_mockups()):
        if max_insert is not None and max_insert == i:
            break
        response = insert_brownfield(
            api_url,
            json.dumps(row),
            random.sample(files, random.randint(0, len(files))),
        )
        if response.status_code > 299:
            exit(1)
        print("OK - " + str(response.json()))
        time.sleep(time_between_requests)
