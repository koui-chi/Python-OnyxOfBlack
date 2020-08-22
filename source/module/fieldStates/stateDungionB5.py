# -*- coding: utf-8 -*-
import pyxel

from ..character import HumanGenerator, playerParty, EnemyPartyGenerator, enemyParty
from ..fieldStates.baseFieldState import BaseFieldState
from ..map.dungionB5 import dungionB5
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil

class StateDungionB5(BaseFieldState):
    '''
    地下迷宮B5のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "dungionB5"

        # 変数定義
        self.tick = 0
        self.isEncount = False

        # マップ
        self.map = dungionB5.map

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "10109U": self.update_encount_kraken,
            "10109D": self.draw_encount_kraken,
        }

        # 出現するモンスターリスト
        self.enemy_set = (
            HumanGenerator.generate(2),
            monsterParams.monsterList[monsterParams.BAT_LV1],
            monsterParams.monsterList[monsterParams.SKELTON_LV1],
            monsterParams.monsterList[monsterParams.WOLF],
            monsterParams.monsterList[monsterParams.COBOLD_LV1],
        )

    def update_encount_kraken(self):
        '''
        クラーケン出現イベントの処理
        '''
        # 敵パーティー生成
        self.isEncount = True
        enemyParty.memberList = EnemyPartyGenerator.generate(monsterParams.monsterList[monsterParams.KRAKEN])

    def draw_encount_kraken(self):
        '''
        クラーケン出現イベントの表示
        '''
#        PyxelUtil.text(16, 140, ["U", "E", "TO", "SI", "TA", "NI", " ", "NU",
#                                 "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

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

        pass