# -*- coding: utf-8 -*-

from module.system.stateTitle import StateTitle
from module.field.stateCity import StateCity
from module.facility.stateWeaponShop import StateWeaponShop
from module.facility.stateArmorShop import StateArmorShop
from module.facility.stateShieldShop import StateShieldShop
from module.facility.stateHelmetShop import StateHelmetShop
#import stateBarbar
#import stateBank
#import stateSurgery
#import stateDrug
#import stateExaminations

'''
 StateStackクラス
 - Stateをスタック管理する
 - Stateのpush,popは各Stateの中で行う
'''
class StateStack():

    STATE_TITLE = "Title"
    STATE_CITY = "City"
    STATE_WEAPONSHOP = "WeaponShop"
    STATE_ARMORSHOP = "ArmorShop"
    STATE_SHIELDSHOP = "ShieldShop"
    STATE_HELMETSHOP = "HelmetShop"

    #
    # クラス初期化
    #
    def __init__(self):
        self.states = []
        self.stateDic = {
            self.STATE_TITLE : StateTitle(self),
            self.STATE_CITY : StateCity(self),
            self.STATE_WEAPONSHOP : StateWeaponShop(self),
            self.STATE_ARMORSHOP : StateArmorShop(self),
            self.STATE_SHIELDSHOP : StateShieldShop(self),
            self.STATE_HELMETSHOP : StateHelmetShop(self)
        }


    #
    # 現在先頭にあるstateのupdate処理を呼び出す
    #
    def update(self):

        state = self.states[0]
        state.update()


    #
    # 現在先頭にあるstateのrender処理を呼び出す
    # 
    def render(self, app):

        state = self.states[0]
        state.render(app)


    # 
    # stateを追加する(push)
    #
    def push(self, stateName):		

        self.states.insert(0, self.stateDic[stateName])
        self.states[0].onEnter()


    #
    # stateを削除する(pop)
    #
    def pop(self):

        self.states[0].onExit()
        self.states.pop(0)
