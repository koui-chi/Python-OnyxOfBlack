# -*- coding: utf-8 -*-
import pyxel

from ..character import HumanGenerator, playerParty
from ..fieldStates.baseFieldState import BaseFieldState
from ..map.cemeteryB1 import cemeteryB1
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil


class StateCemetery(BaseFieldState):
    '''
    墓地の地下のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "Cemetery"

        # 変数定義
        self.tick = 0
        self.isEncount = False

        # マップ
        self.map = cemeteryB1.map

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "09069U": self.update_to_city,
            "10069U": self.update_to_city,
            "09079U": self.update_to_city,
            "10079U": self.update_to_city,
            "09069D": self.draw_to_city,
            "10069D": self.draw_to_city,
            "09079D": self.draw_to_city,
            "10079D": self.draw_to_city,
        }

        # 出現するモンスターリスト
        self.enemy_set = (
            HumanGenerator.generate(2),
            monsterParams.monsterList[monsterParams.BAT_LV1],
            monsterParams.monsterList[monsterParams.SKELTON_LV1],
            monsterParams.monsterList[monsterParams.WOLF],
            monsterParams.monsterList[monsterParams.ZOMBIE_LV1],
            monsterParams.monsterList[monsterParams.COBOLD_LV1],
            monsterParams.monsterList[monsterParams.MUMMY],
        )

    def update(self):
        '''
        各フレームの処理
        '''
        super().update()

    def update_to_city(self):
        '''
        天井の抜け穴のイベント
        '''
        if pyxel.btn(pyxel.KEY_U):
            if playerParty.x == 9 and playerParty.y == 6:
                playerParty.x = 25
                playerParty.y = 19
            if playerParty.x == 10 and playerParty.y == 6:
                playerParty.x = 26
                playerParty.y = 19
            if playerParty.x == 9 and playerParty.y == 7:
                playerParty.x = 25
                playerParty.y = 20
            if playerParty.x == 10 and playerParty.y == 7:
                playerParty.x = 26
                playerParty.y = 20
            # 町へ戻る
            self.stateStack.pop()

    def draw_to_city(self):
        '''
        天井の抜け穴の表示
        '''
        PyxelUtil.text(16, 140, ["TE", "NN", "SI", "D", "LYO", "U", "NI", " ", "NU",
                                 "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        self.tick = 0
        self.isEncount = False

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_RED, pyxel.COLOR_PURPLE)

    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()

        pass