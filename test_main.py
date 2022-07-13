from pytest import raises
from main import Auction, Bid

def test_equal_bid_raises():
    auction = Auction()
    auction.new_bid(Bid(1,10,10))

    with raises(ValueError):
        auction.new_bid(Bid(1,10,10))
