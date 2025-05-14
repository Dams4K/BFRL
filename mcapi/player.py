import requests

UUID_FROM_NAME = "https://api.mojang.com/users/profiles/minecraft/{name}"
NAME_FROM_UUID = "https://api.minecraftservices.com/minecraft/profile/lookup/{uuid}"

def get_uuid(name: str) -> str:
    response = requests.get(UUID_FROM_NAME.format(name=name))
    return response.json().get("id", "")

def get_name(uuid: str) -> str:
    response = requests.get(NAME_FROM_UUID.format(uuid=uuid.replace("-", "")))
    return response.json().get("name", "")
