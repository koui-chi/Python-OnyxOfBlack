# -*- coding: utf-8 -*-
import pyxel

from ..character import HumanGenerator, playerParty
from ..map.wellB2 import wellB2
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil
from .baseFieldState import BaseFieldState


class StateWellB2(BaseFieldState):
    '''
    井戸B2のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    # マップ
    _map = wellB2.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(2),
        monsterParams.monsterList[monsterParams.BAT_LV1],
        monsterParams.monsterList[monsterParams.SKELTON_LV1],
        monsterParams.monsterList[monsterParams.WOLF],
        monsterParams.monsterList[monsterParams.COBOLD_LV1],
    )

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "WellB2"

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "10109U": self.update_to_upanddown,
            "10109D": self.draw_to_upanddown,
        }

        self.onEnter()

    def update_to_upanddown(self):
        '''
        抜け穴のイベント
        '''
        if pyxel.btnp(pyxel.KEY_U):
            playerParty.x = 10
            playerParty.y = 10
            # 井戸B1へ戻る
            self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_D):
            playerParty.x = 10
            playerParty.y = 10
            # 井戸B3へ
            self.stateStack.push(self.stateStack.STATE_WELLB3)

    def draw_to_upanddown(self):
        '''
        天井の抜け穴の表示
        '''
        PyxelUtil.text(16, 140, ["U", "E", "TO", "SI", "TA", "NI", " ", "NU",
                                 "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_LIGHTBLUE, pyxel.COLOR_DARKBLUE)

    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
