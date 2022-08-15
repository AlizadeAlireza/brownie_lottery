from brownie import (
    network,
    config,
    accounts,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    interface,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")

    # if index passed
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    # we're going to pull directly from our config ---> default
    # to grab right from our config

    return accounts.add(config["wallets"]["from_key"])


# any time you see fusd price feed that's going be ]
# a mock V3 aggregator if we need to deploy a mock
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """this func will grab the contract addresses from the brownie config
    if defined, otherwise it will deploy a mock version of that contract and
    return that mock contract

        Args:
            contract_name (string):
        Returns:
            Contract ---> brownie.network.contract.ProjectContract:the most recently
            deployed version of this contract.
            MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]
    # let's check if we're on a local blockchain
    # and we'll skip the forked local env because
    # again we don't need to deploy a mock price feed address
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # check to see if one of these contracts has already been deployed
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


# first we'll to have a contract address
# we'll want to know who we're going to fund with link
# so we set a default account and same with the link token
# say if you want to use a specific link token you can othewise we'll just grab it ourselves
# set a default amount
def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 Link
    # if somebody send it and second account is exist
    account = account if account else get_account()
    # same thing with the link token
    link_token = link_token if link_token else get_contract("link_token")
    # now we can just call the functions on this linktoken
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
