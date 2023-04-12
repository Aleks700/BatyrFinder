import http.client
import json


def search_images(body):
    conn = http.client.HTTPSConnection("eo.gharysh.kz")

    payload = "username=themaratovrollan%40gmail.com&password=KGSpass22"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    conn.request("POST", "/api/v2/login", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    token = json.loads(data)["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    body_json = json.dumps(body)
    conn.request("POST", "/api/v2/search/", body_json, headers)
    response = conn.getresponse()
    data_json = response.read().decode("utf-8")
    try:
        images = json.loads(data_json)["Images found:"]
    except Exception as err:
        print(err)
    if images == "No images":
        return None
    filtered_images = []
    for image in images:
        if image["source"] == "updater":
            filtered_images.append(image)
    return filtered_images if len(filtered_images) > 0 else None
