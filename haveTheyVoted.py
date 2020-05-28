import json
import os
from getpass import getpass
from web3 import Web3
import votingABI
import contractABI
import time

FuseFileStructure=True

RPC_ADDRESS = 'https://rpc.fuse.io'
web3Fuse = Web3(Web3.HTTPProvider(votingABI.RPC_ADDRESS))
fuseVotingContract = web3Fuse.eth.contract(abi=votingABI.VOTING_ABI, address=votingABI.VOTING_ADDR)
fuseConsensusContract = web3Fuse.eth.contract(abi=contractABI.CONSENSUS_ABI, address=contractABI.CONSENSUS_ADDRESS)

activeBallots = fuseVotingContract.functions.activeBallots().call()

print("active Ballots: " + str(activeBallots[0]))

ballotID = input("Ballot ID: ")

activeValidator = fuseConsensusContract.functions.getValidators().call()

forVote = 0
againstVote = 0
abstained = 0

totalValidators = len(activeValidator)

for address in activeValidator:
    voted = fuseVotingContract.functions.getVoterChoice(int(ballotID), address).call()
    if voted == 0:
        abstained+=1
    elif voted == 1:
        forVote+=1
    elif voted == 2:
        againstVote+=1

    print(address + " Voted for choice = " + str(voted))

print("total Validators = " + str(totalValidators) + " For = " + str(forVote) + " (" + str((forVote/totalValidators)*100) +
       '%) , Against = ' + str(againstVote) + " (" + str((againstVote/totalValidators)*100) + '%) , Abstained = '+ str(abstained) + " (" + str((abstained/totalValidators)*100) + '%)')