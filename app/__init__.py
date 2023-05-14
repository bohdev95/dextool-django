# from huey import crontab
# from huey.contrib.djhuey import periodic_task, task

# import requests
# import datetime


# @task()
# def count_beans(number):
#     print('-- counted %s beans --' % number)
#     return 'Counted %s beans' % number

# api_key_eth = "HPMZ3UJMWDI7UIDHD2WJSIVZQPQJMJHSC2"
# api_key_bsc = "YSCZP3R1S3ENAU6PRJT57VQ6HH4BKAGYJ8"
# base_eth = "https://api.etherscan.io/api?"
# base_bsc = "https://api.bscscan.com/api?"
 
# dext_bsc = "0xe9320b8f09d95e63c8e37486d62843f299306293"
# dext_eth = "0xfb1b36bef010d6b073d35d40cf3069ad0d1d153a"
# burn_address = "0x0000000000000000000000000000000000000000"
# aggregator = "0x960B733FfA86EFa206E31225214d96bC217708b7"
# social_fee = "0x994ccc92858c20aed7a4c0400ce1ac0c43f3e587"


# @periodic_task(crontab(minute='*/1'))
# def every_five_mins():
#     print('Every five minutes this will be printed by the consumer')
    

# def token_amount(base,contract_address,address,api_key):
#     request = f"{base}module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={api_key}"
#     amount = int(int(requests.get(request).json()["result"])/1e18)
#     print(amount)
#     return amount

# def get_total_supply(base, contract_address, api_key):
#     request = f"{base}module=stats&action=tokensupply&contractaddress={contract_address}&apikey={api_key}"
#     amount = int(int(requests.get(request).json()["result"])/1e18)
#     print(amount)
#     return amount