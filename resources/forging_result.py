# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from connect import security


class ForgingResultResource(Resource):

    @security.http(
        # params=MyNFTsRequestSchema(),
        # response=MyNFTsResponseSchema()
    )
    def get(self):
        # _query = request.args.to_dict()

        return {
            "name": "SHIBA INU",
            "description": "Now you can forge SHIBA INU. This NFT will not be available on minting. Only on forging, which make it very rare.",
            "image": "https://s3-alpha-sig.figma.com/img/3653/965d/23802b9a698995d84fe3d589a0086525?Expires=1684713600&Signature=SLp3d~PfC8TGRM9Ly2qRMKx6RQ7NRpz9vuXQMOBs4aASNlah7Ho5riX6I5QZECTEvKwQAary00T5rmKZMIsDf6Y3-W42yUPr2W6UbVfb4dz1z32Z0-wUhjR-Goxz9DMrGW1SMMP2hJj2Q2ZCE-vFt17hMFyy7NXX3dD5RvAQ9eV-HWF7c2jKwu99qJyZEEaxVPHOpILgwh47nKD1XOBCBm~7aK7RGWtbtuJ2uoZNiVMWFilJBCPSpWcIlYinLwDEdnIpQ3tLKyOK-Kc~RBSaIzTtc7w7kcLUuMohYR0SqIIppYD6sm90883e-DcN8woxZk55C2E1ixOtxz~dNKh54g__&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4",
            "metadata": [
                {
                    "name": "Skin Rarity",
                    "value": "MYTHICAL"
                },
                {
                    "name": "Hero Rarity",
                    "value": "COMMON"
                },
                {
                    "name": "Hero Class",
                    "value": "MARSKMAN"
                },
            ],
            "requirements": [
                {
                    "name": "2D NFT",
                    "value": 2
                },
                {
                    "name": "3D NFT",
                    "value": 1
                },
                {
                    "name": "KATA token",
                    "value": 15000
                }
            ]
        }
