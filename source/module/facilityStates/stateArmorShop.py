# -*- coding: utf-8 -*-
import os

import pyxel
from module.character import playerParty
from module.facilityStates.baseShopState import BaseShopState
from module.params.armor import armorParams
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateArmorShop(BaseShopState):
    '''
    鎧屋のクラス\n
    BaseFacilityStateクラスを継承。
    選択した商品の購入、キャラクターへの装備を行う。
    '''

    # この店で使うアイテムリスト
    itemList = armorParams

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 店員の初期データ
        self.saleParson.name = "Blick"
        self.saleParson.head = 13
        self.saleParson.body = 4

        # 画像をロード
        pyxel.image(0).load(0, 205, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../assets/armorshop.png")))

    @overrides
    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()
        playerParty.memberList[self.equipMember].armor = self.item

    @overrides
    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.armor = self.item

    @overrides
    def draw_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["YO", "U", "KO", "SO", " ", "I", "RA",
                                 "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["WA", "TA", "SI", "HA", "* Blick Armstrong ",
                                 "TO", " ", "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
