import json
import os
from getpass import getpass
from web3 import Web3
import votingABI

FuseFileStructure=True

RPC_ADDRESS = 'https://rpc.fuse.io'
dirToSearch = input("Where are you keystores?: ")
web3Fuse = Web3(Web3.HTTPProvider(votingABI.RPC_ADDRESS))
fuseVotingContract = web3Fuse.eth.contract(abi=votingABI.VOTING_ABI, address=votingABI.VOTING_ADDR)

activeBallots = fuseVotingContract.functions.activeBallots().call()

print("active Ballots: " + str(activeBallots[0]))

ballotID = input("Ballot ID: ")

choice = '0'
while (choice != '1' and choice != '2'):
    choice = input("Accept (1), reject (2): ")

hexData = fuseVotingContract.encodeABI(fn_name="vote", args=[int(ballotID),int(choice)])

for file in os.listdir(dirToSearch):
    private_key = ''
    if FuseFileStructure:
        if(os.path.isdir(dirToSearch + '/' + file+'/config')):
            with open(dirToSearch + '/' + file + '/config/address', 'r') as fileToRead:
                addr = fileToRead.read().replace('\n', '')

            with open(dirToSearch + '/' + file +'/config/pass.pwd', 'r') as fileToRead:
                keystorePassword = fileToRead.read().replace('\n', '')

            for keys in os.listdir(dirToSearch + '/' + file+'/config/keys/FuseNetwork'):
                if keys.startswith("UTC"):
                    with open(dirToSearch + '/' + file+'/config/keys/FuseNetwork/' + keys) as keyfile:
                        encrypted_key = keyfile.read()
                        private_key = web3Fuse.eth.account.decrypt(encrypted_key, keystorePassword)
    else:
        #grab the address from the keystore
        f = open(dirToSearch + '/' + file)
        data = json.load(f)
        addr=data['address']
        f.close()
        passWordString = 'What is your password for ' + addr + ' ?: '
        keystorePassword = getpass.getpass(prompt=passWordString)
        web3Fuse = Web3(Web3.HTTPProvider(RPC_ADDRESS))
        with open(dirToSearch + '/' + file) as keyfile:
            encrypted_key = keyfile.read()
            private_key = web3Fuse.eth.account.decrypt(encrypted_key, keystorePassword)

    if(private_key != ''):
        addr = Web3.toChecksumAddress(addr)

        Nonce = web3Fuse.eth.getTransactionCount(addr)

        signed_txn = web3Fuse.eth.account.signTransaction(dict(
            nonce=Nonce,
            gasPrice=web3Fuse.toWei('1', 'gwei'),
            gas=250000,
            to=votingABI.VOTING_ADDR,
            value=0,
            chainId=122,
            data=hexData
        ),
            private_key=private_key)
        try:
            txid = web3Fuse.eth.sendRawTransaction(signed_txn.rawTransaction)
            print ("Transaction sent on: " + addr + " TXID: " + web3Fuse.toHex(txid))
        except ValueError:
            print("failedToSend from " + addr)
