'''This module communicates with blockchains through APIs.'''

import threading
# import requests


class BlockchainRequest:
    '''Blockchain request class.'''

    def request_update(req_type: str, data: dict) -> None:
        '''Make a request seperately and wait for the response without affecting the rest of the task.'''
        if req_type == 'NFT':
            threading.Thread(target=BlockchainRequest.update_nft, args=(data,)).start()

    def update_nft(data: dict) -> None:
        '''Request an NFT update onto Solana blockchain.'''
        url = 'WAITING FOR URL'  # TODO: add url when it's ready
        # requests.post(url, data=data, timeout=10)
        print(url)
