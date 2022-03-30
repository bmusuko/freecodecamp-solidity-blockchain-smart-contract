from brownie import AdvancedCollectible, network
from scripts.utils import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible_tokens = advanced_collectible.tokenCounter()
    print(f"you have created {number_of_advanced_collectible_tokens} collectibles")
    for token_id in range(number_of_advanced_collectible_tokens):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectibe_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exist! delete it or overwrite")
        else:
            print(f"Creating new file {metadata_file_name}")
            collectibe_metadata["name"] = breed
            collectibe_metadata["description"] = f"An adroable {breed} pup!"
            image_file_name = f"./img/{breed.lower().replace('_', '-')}.png"

            image_uri = upload_to_ipfs(image_file_name)

            collectibe_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectibe_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(f"{ipfs_url}{endpoint}", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(f"image uri: {image_uri}")
        return image_uri


# {
#   "Bytes": "<int64>",
#   "Hash": "<string>",
#   "Name": "<string>",
#   "Size": "<string>"
# }
