from brownie import network, AdvancedCollectible
from scripts.utils import get_breed, get_account, OPENSEA_URL


dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/QmWKZwFqeFAci2b22BQE7hMeVrdtYbBkJSEyRuXtBKJTr7?filename=1-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmU5DeH5zgvnp4QCnvudHcSnWSPdUkxRnbBngM5cwsQNHm?filename=2-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmNatVTjQrzV1yoteqUwpQmwuw8bheEWPkh4e5nmeCYeGH?filename=0-ST_BERNARD.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible_tokens = advanced_collectible.tokenCounter()
    print(f"You have {number_of_advanced_collectible_tokens} unique tokens")
    for token_id in range(number_of_advanced_collectible_tokens):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            # set token uri
            print(f"Setting token URI, for token id {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dict[breed])


def set_tokenURI(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Token URI has been set for token {token_id}\nYou can view it at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    return tx
