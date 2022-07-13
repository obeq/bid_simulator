from dataclasses import dataclass
from random import randint
from traceback import print_exc, print_stack
from rich import print
import click
from copy import copy

@dataclass
class Bid:
    user: int
    amount: int
    max_amount: int
    auto: bool = False


class Auction:
    def __init__(self):
        self.bids = []

    def sanity_check(self):
        pass

    def last_bid_highest_max(self) -> bool:
        return False

    def last_bid_higher_than_all_max(self) -> bool:
        return False

    def new_bid(self, bid: Bid):
        if bid.max_amount < bid.amount:
            raise(ValueError("Max amount can't be lower than bid amount."))
        if leader := self.leader:
            if bid.amount <= leader.amount:
                raise(ValueError(f"Illegal bid! Amount is lower than the current leader: {leader}"))
            self.bids.append(bid)
            self.auto_bid()
        else:
            self.bids.append(bid)
            
    def auto_bid(self):
        bid = self.bids[-1]
        higher_bids = sorted(filter(lambda x: x.max_amount > bid.amount, self.bids), key=lambda x: x.max_amount)
        
        for bid_to_raise in higher_bids[:-1]:
            auto_bid = copy(bid_to_raise)
            auto_bid.amount = auto_bid.max_amount
            auto_bid.auto = True
            self.bids.append(auto_bid)
        
        if higher_bids:
            new_leader = higher_bids[-1]
            if self.bids[-1] != new_leader:
                auto_bid = copy(new_leader)
                # auto_bid.amount = self.bids[-1].amount + 1
                auto_bid.amount = min(self.bids[-1].amount + 1, auto_bid.max_amount)
                auto_bid.auto = True
                self.bids.append(auto_bid)

    def get_highest_max(self):
        """Returns the bids with the highest max_amount"""
        sorted_bids = sorted(self.bids, key=lambda x: x.max_amount)
        highest_max = sorted_bids[-1]
        return highest_max
        # return list(filter(lambda x: x.max_amount >= highest_max, sorted_bids))

    @property
    def leader(self):
        if self.bids:
            return self.bids[-1]
        else:
            return None

    def __str__(self):
        if self.bids:
            return f"The leading bid is: {self.bids[-1]}!"
        return "No bids...yet!"


def check_sanity(auction):
    if len(auction.bids) > 1:
        highest_max = auction.bids[0].max_amount

        for i, bid in enumerate(auction.bids, 1):
            assert bid.amount >= auction.bids[i-1].amount
            if bid.max_amount > highest_max:
                highest_max = bid.max_amount

        assert auction.leader.max_amount == highest_max


def main(interactive = False):
    print("Welcome to Bid Simulator 0.1!")

    user_count = click.prompt("How many bidders?", type=int)

    print(f"{user_count} bidders selected.")
    auction = Auction()

    MAX_BID = 100
    MAX_INCREMENT = 10
    MAX_MAX_INCREMENT = 10
    CHAOS = True

    while True:
        print(auction.bids)
        print("_______")

        if interactive:
            user = click.prompt("Who will make the next bid?", type=int, default=randint(0, user_count))
        else:
            user = randint(0, user_count)
        
        if user >= 0 and user < user_count:
            if interactive:
                amount = click.prompt("How much are they bidding?", type=int, default=randint(0, MAX_BID))
                max_amount = click.prompt("How far are they willing to go?", default=randint(0, MAX_BID))
            else:
                amount = randint(0, MAX_BID)
                max_amount = randint(0, MAX_BID)

            bid = Bid(user, amount, max_amount)

            try:
                auction.new_bid(bid)
            except ValueError as e:
                print(e)

            try:
                check_sanity(auction=auction)
            except AssertionError as e:
                print(auction.bids)
                print_exc()
                print_stack()
                break

            if auction.leader and auction.leader.amount > 95:
                print(auction.bids)
                break


if __name__=='__main__':
    main()