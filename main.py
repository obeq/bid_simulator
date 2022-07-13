from dataclasses import dataclass
from rich import print
import click
from copy import copy

@dataclass
class Bid:
    user: int
    amount: int
    max_amount: int


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
        if leader := self.leader:
            if bid.amount <= leader.amount:
                raise(ValueError(f"Illegal bid! Amount is lower than the current leader: {leader}"))
            self.bids.append(bid)
            
            higher_bids = sorted(filter(lambda x: x.max_amount > bid.amount, self.bids), key=lambda x: x.max_amount)
            
            for bid_to_raise in higher_bids[:-1]:
                auto_bid = copy(bid_to_raise)
                auto_bid.amount = auto_bid.max_amount
                self.bids.append(auto_bid)
            
            new_leader = higher_bids[-1]
            if self.bids[-1] != new_leader:
                auto_bid = copy(new_leader)
                # auto_bid.amount = self.bids[-1].amount + 1
                auto_bid.amount = min(self.bids[-1].amount + 1, auto_bid.max_amount)
                self.bids.append(auto_bid)
        else:
            self.bids.append(bid)

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


def main():
    print("Welcome to Bid Simulator 0.1!")

    user_count = click.prompt("How many bidders?", type=int)

    print(f"{user_count} bidders selected.")
    auction = Auction()

    while True:
        print(auction.bids)
        print("_______")
        user = click.prompt("Who will make the next bid?", type=int) - 1
        if user >= 0 and user < user_count:
            amount = click.prompt("How much are they bidding?", type=int)
            max_amount = click.prompt("How far are they willing to go?", default=amount)

            bid = Bid(user, amount, max_amount)

            try:
                auction.new_bid(bid)
            except ValueError as e:
                print(e)


if __name__=='__main__':
    main()