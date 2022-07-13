from pytest import raises
from main import Auction, Bid

def test_bid_equality():
    assert Bid(1,10,10) == Bid(1,10,10)

def test_equal_bid_raises():
    auction = Auction()
    auction.new_bid(Bid(1,10,10))

    with raises(ValueError):
        auction.new_bid(Bid(1,10,10))

def test_right_highest_max():
    auction = Auction()
    auction.bids = [
        Bid(1,10,20),
        Bid(1,10,10),
        Bid(1,10,30),
        Bid(1,10,15),
    ]

    assert auction.get_highest_max() == Bid(1,10,30)

def test_auto_raise_first_bidder_should_win():
    auction = Auction()
    auction.new_bid(Bid(1,10,20))

    auction.new_bid(Bid(2,11,15))

    assert auction.leader == Bid(1,16,20)


def test_auto_raise_seconde_bidder_should_win():
    auction = Auction()
    auction.new_bid(Bid(1,16,20))

    auction.new_bid(Bid(2,17,23))

    print(auction.bids)
    assert auction.leader == Bid(2,21,23)


def test_auto_raise_should_never_result_in_exceeded_max():
    auction = Auction()

    bids = [
        Bid(user=2, amount=21, max_amount=25),
        Bid(user=1, amount=22, max_amount=25),
    ]

    for bid in bids:
        auction.new_bid(bid)

    for bid in auction.bids:
        assert bid.amount <= bid.max_amount