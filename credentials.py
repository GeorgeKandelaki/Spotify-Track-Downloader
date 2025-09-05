import os


def save_credentials(
    config_file_name="spotidownload",
    client_secret="",
    client_id="",
):
    home = os.path.expanduser("~")
    path = f"{home}/.config/spotidownload"

    if not os.path.exists(path):
        os.mkdir(path, mode=0o777)

    with open(f"{path}/{config_file_name}.py", "w") as file:
        file.write(
            f"""client_id = '{client_id}'
client_secret = '{client_secret}'"""
        )

    return None


def get_credentials(path):
    client_secret = ""
    client_id = ""

    if not os.path.exists(path):
        return None

    with open(path, "r") as file:
        for line in file.readlines():
            arr = line.strip().split("'")

            if "client_id" in arr[0]:
                client_id = arr[len(arr) - 2]

            if "client_secret" in arr[0]:
                client_secret = arr[len(arr) - 2]

    return {"client_secret": client_secret, "client_id": client_id}
