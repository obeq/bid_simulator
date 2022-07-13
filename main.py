from dataclasses import dataclass
from rich import print
import click

@dataclass
class Bid:
    user: int
    amount: int
    max_amount: int


class Auction:
    def __init__(self):
        self.bids = []

    def new_bid(self, bid: Bid):
        if leader := self.leader:
            if bid.amount < leader.amount:
                print(f"Illegal bid! Amount is lower than the current leader: {leader}")
                return
            self.bids.append(bid)
        else:
            self.bids.append(bid)

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
        print(auction)
        user = click.prompt("Who will make the next bid?", type=int) - 1
        if user >= 0 and user < user_count:
            amount = click.prompt("How much are they bidding?", type=int)
            max_amount = click.prompt("How far are they willing to go?", default=amount)

            bid = Bid(user, amount, max_amount)
            auction.new_bid(bid)


if __name__=='__main__':
    main()