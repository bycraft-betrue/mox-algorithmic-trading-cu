# some network checks
# if we are running this on a test/forked network, let's give us some fake money

from boa.contracts.abi.abi_contract import ABIContract
from typing import Tuple
from moccasin.config import get_active_network, Network
import boa

STARTING_ETH_BALANCE = int(1000e18)
STARTING_USDC_BALANCE = int(100e6)
STARTING_WETH_BALANCE = int(1e18)


def _add_eth_balance():
    boa.env.set_balance(boa.env.eoa, STARTING_ETH_BALANCE)


def _add_token_balance(usdc: ABIContract, weth: ABIContract, active_network: Network):
    our_address = boa.env.eoa
    # we can use usdc contract as a proxy and pretend to be the owner
    with boa.env.prank(usdc.owner()):
        usdc.updateMasterMinter(our_address)
    usdc.configureMinter(our_address, STARTING_USDC_BALANCE)
    usdc.mint(our_address, STARTING_USDC_BALANCE)
    # because we now have the abi, we can use it to mint WETH
    weth.deposit(value=STARTING_WETH_BALANCE)


# these ABIContracts classes are to help us call contracts on blockchain when we don't know exactly the source code
def setup_script() -> Tuple[ABIContract, ABIContract, ABIContract, ABIContract]:
    print("Setting up script")

    # 1. give ourselves some ETH
    # 2. give ourselves some USDC and WETH

    active_network = get_active_network()

    usdc = active_network.manifest_named("usdc")
    weth = active_network.manifest_named("weth")

    if active_network.is_local_or_forked_network():
        _add_eth_balance()
        _add_token_balance(usdc, weth, active_network)


def moccasin_main():
    setup_script()
