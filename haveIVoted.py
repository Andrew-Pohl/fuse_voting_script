import json
import os
from getpass import getpass
from web3 import Web3
import votingABI
import time

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

addrList = []

for file in os.listdir(dirToSearch):
    private_key = ''
    addr=''
    if FuseFileStructure:
        if(os.path.isdir(dirToSearch + '/' + file+'/config')):
            with open(dirToSearch + '/' + file + '/config/address', 'r') as fileToRead:
                addr = fileToRead.read().replace('\n', '')
    else:
        #grab the address from the keystore
        f = open(dirToSearch + '/' + file)
        data = json.load(f)
        addr=data['address']
        f.close()

    if addr != '':
        addr = Web3.toChecksumAddress(addr)
        addrList.append(addr)

for address in addrList:
    voted = fuseVotingContract.functions.getVoterChoice(int(ballotID), address).call()
    if voted != int(choice):
        print("Failed to vote for addr: " + address)
    else:
        print(address + " Voted correctly choice = " + str(voted))