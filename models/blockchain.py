'''This module communicates with blockchains through APIs.'''

import threading
import requests

from helpers.misc import AppSettings


class BlockchainRequest:
    '''Blockchain request class.'''

    def request_update(req_type: str, data: dict,  settings: AppSettings) -> None:
        '''Make a request seperately and wait for the response without affecting the rest of the task.'''
        if req_type == 'NFT':
            threading.Thread(target=BlockchainRequest.update_nft, args=(data, settings)).start()

    def update_nft(data: dict, settings: AppSettings) -> None:
        '''Request an NFT update onto Solana blockchain.'''
        try:
            requests.post(settings.NFT.URL.UPDATE, data=data, timeout=60)
        except Exception as e:  # pylint: disable=[W0703]
            print(e)
