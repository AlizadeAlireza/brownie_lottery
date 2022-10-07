1. Users can enter lottery with ETH based on a USD fee
2. an admin will choose when the lottery is over 
3. The lottery will select a random winner

how do we want to test this?

1. 'mainnet-fork'
2. 'development' with mocks
3. 'testnet' 


##  lottery application
where anybody can enter and a random winner selected.


1 ) setup
mkdir and init brownie

2 ) create a qiuck readme.md to explain
3 ) main func
enter() ---> payable 
getEntranceFee()
startLottery()
endLottery()

4 ) make a test for ETH price
5 ) deleting brownie's internal built-in mainnet fork
$brownie networks delete mainnet-fork

6 ) we want make sure we're not ending the lottery before the lottery even 
starts or we're not entering a lottery when a lottery hasn't even be begun
---> using enum

7) randomness
random numbers are much harder 
each node is never going to be able to sync up  
---> base the ramndom number on some other attributes in the system
it's not actually random
is pseudorandom

8 ) to get a true random number we are going to have look outside the 
blockchain and we can't use just an api that gives a random number 
if something happens with that api is going to be down
----> what we need is a provable way to get a random number and chain-link vrf
is actually that solution ---> chainlink vrf 

key hash ---> uniquely identifies the chain link node that we're going to use 
fee ---> is how much link we're actually going to pay to the chainlink node for
delevering us this random number 

oracle Gas ---> this is to pay the oracles a fee for their services for providing
data or doing some type of external computation for a smart contract 

9 ) why didn't we pay oracle gas when working with the Chainlink Price feeds?
for price feeds somebody had actually already paid for data to be returned and if we go to chainlink 
we can actually see a list of sponsers that are paying to get this data delivered 
they're already paying the oracle gas to bring this data on chain for us  

10 ) gas estimation failed 
the reason that it's failing is because the contract doesn't have any oracle gas
we can copy deployed transaction hash and send link to it for fee

 11 ) : in one transaction we actually request some data then in a second transaction the chainlink node itself will make a function call and return 
 the data back to the smart contract ---> in this case ---> fulfill randomness
 
 11,1 ) two tx : 
 1. pay by us when we called get random number 
 2. paid by chainlink node when it called fulfill randomness 
 
 *** we can add any additional constructors from inherited smart contracts 
 
 12 ) how to do request random number?
 by saying bytes32 request id we're saying we're going to return
 
 -->this means that in this first transaction we're going to request the data 
 from the chain link oracle and chainlink goes to return the data to this contract
 into another function ---> fulfillRandomness ---> second transaction
 
 ** override keyword ---> means we're overriding the original declaration of the fulfillrandomness function
 
 12,1) we can use that mod function in our fulfill randomness with the length of
 our players
 
 13 ) lottery testing  
 - make a deploy_lottery.py 
 firs thing we need always to deploy a contract is an account 
 usually i use get_account() that we've been adding in a helpful script section
 
 $brownie account list ---> show accounts
 
 after getting id and index in get account func
 ---> now that we have an account to deploy our lottery ----> from brownie import Lottery
 
 14) see if we were on a localchain ro not 
 if we were on a local chain then we would just pull our addresses directly from our config
 if we we weren't on a localchain tough we'd deploy some mocks and use the address of those mocks 
 we're going all of this mocking and checking into a single func ---> get_contract() and add this function to our helpful script 
 
 contract_name as an argument for get_contract func
 
 15 ) contract to mock ---> create mapping here 
 
 using Contract.from_abi package
 
 add  rinkeby network to yaml
 adding vrfCoordinatorMock

what else need?  we need a link token ---> is just another smart contract 
---> get_contract()
add link token to config-yaml
in chainlink go to LinkToken contracts
add LinkToken to test folder beside mocks

what else to be need? we need a fee and a keyhash ---> they are numbers and
not actually contracts 

in yaml ---> in development set a keyhash and fee

* now our deploy lottery --> we can't just grab this directly from a brawning
config because we're always going to have this default keyhash and fee
so----> config["network"][network.show_active()]["fee"],
and same this for keyhash
and last move ---> {"from":account}
if we want to published this ---> 
published_source=config["networks"][network.show_active()].get("verify", False)


* add vrf and linktoken to deploy mock
get vrf in his constractor in sol document

16) python lottery scripts/Functions

start the lottery ---> start_lottery
enter_lottery()
we need to pick some value to send when we call the enter function
because we need to send that entranceFee with it 

end_lottery()---> before we actually end this lottery we're going to need some
link token in this contract because this func call request randomness
and we can only request some randomness if our contract has some chainlink token

funding our contracts with the link token is going to be a pretty common function that we use ---> add it to helpful script 
we can also use the interfaces 

16,1 ) waiting for callback
when we call endlottery func we're going to make a request to a chainlink node 
and that chainlink node is going to be respond by calling this fulfill randomness
function ---> so we actually have to wait for that chainlink node to finish
---> time.sleep(60)
then we can see who that recent winner is 

16,2 ) well, there's no chain-link nodes watching our local ganache so we add
end_lottery

***unit test ---> a way of testing the smallest piece of code in an isolated instance

integration testing ---> a way of testing across multiple complex systems that 
run on a actual chain

first test ---> test_get_entrance_fee
second test ---> test_cant_enter_unless_started
third ---> test_can_start_and_enter_lottery
fourth ---> test_can_end_lottery

to actually end the lottery we do need to send this some link calling request 
randomness
we use our fund with link script 

how do we actually know that this is being called correctly
in Lottery when we call end lottery we don't we're not really doing
check to see if our calculating winner state is different

fifth test ---> test_can_pick_winner_correctly()
in our lottery test actually calling this fulfill randomness function and 
testing everything in here 
we're going to need to call fulfillRandomness() in Lottery

in vrfCoordinatorMock we have callBackWithRandomness() ---> this is the func
that actually calls this rawfullfilrandomness.selector

when this contract actually entered the calculating winner state is we want to 
do what's called emmiting an event 

** event ---> are pieces of data executed in the blockchain stored in the blockchain but are not accessible by any smart contracts

smart contracts cant access events 
events are much more gas efficient than using a storage variable

in the transaction details---logs section witch also includes all the different 
events now there's a lot of information here so we're actually going to do an
event ourself just so that we can see what this really looks like

RandomnessRequest that spitout by the vercoordinator that is inhereted
some data that's already been decoded
one those pieces of data is request id 

in Lottery.sol --->     event RequestedRandomness(bytes32 requestId);

this events is already really helpful  for many reasons like:
upgrading our smart contract 
understanding when a mappinng is updated

pretended to be the chainlink node and use this callback func in VRF
to duumy getting a random number back from the chainlink node


17 ) integration test
we're going to use rinkeby

this is going to be the opposite of our unit test 
unit test ---> only on our local blockchain we're going to skip if it's not on 
our local blockchains 

in our unit test we pretended that were the vrf coordinator and called the 
callback with randommness and on a chain-link node

here, we're on an actual network so going wait for that chainlink node to respond
brownie test -k test_can_pick_winner --network rinkeby -s
-s ---> will print whatever brownie is going to be printingF


### lottery solidity:

function enter(): ---> payable
	
	- keep track all of the players,
	every body signs up for this lottery.
	
function getEntranceFee(): --> view
 	- we have to store somewhere this minimum entrance fee,
 	and we can declare a variable and set in constructor.
 	
 	we're going to need to pull from the price feed convert $5
 	to $5 in the eth.
 	
 	usdEntryFee has 18 decimals but it cancled out with our priceFeed.
 	
 	we want to make sure that we're not ending the lottery before the 
 	lottery even starts/

when we initialize our contract here we're going to want to set our lottery state
to being closed.


endLottery():

	this is here we choose a random winner here
	
	we're converting everything here to being a uint256,
	because we want to pick a random number based off of an index.
	
startLottery():
	
	it must be closed at first.
	when we make sure that is closed we can start it.
	and when it's start, we can enter in because the enter situation
	is that the lottery must opened.
	
