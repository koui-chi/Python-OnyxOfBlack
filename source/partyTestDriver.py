# -*- coding: utf-8 -*-
from module.character import HumanPartyGenerator
from module.character import PlayerParty
from module.character import Human

if __name__ == "__main__":
    party = HumanPartyGenerator.generate()
    for human in party.getMemberList():
        print(human.name)
        print(human.life)
        print(human.exp)

