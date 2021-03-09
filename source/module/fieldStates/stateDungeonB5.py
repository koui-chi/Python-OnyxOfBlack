# -*- coding: utf-8 -*-
import pyxel
from module.character import EnemyPartyGenerator, enemyParty
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB5 import dungeonB5
from module.params.monster import monsterParams
from overrides import overrides


class StateDungeonB5(BaseFieldState):
    '''
    地下迷宮B5のクラス\n
    BaseFieldStateを継承。\n
    遭遇する敵リストとイベント処理を持つ。
    '''

    # マップ
    _map = dungeonB5.map

    # 出現するモンスターリスト
    enemy_set = (
        monsterParams["WOLF_LV2"],
        monsterParams["LION_LV2"],
        monsterParams["SLIME_LV2"],
        monsterParams["SPIDER_LV1"],
        monsterParams["GHOUL_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "10109U": self.update_encount_kraken,
            "10109D": self.draw_encount_kraken,
        }

        self.onEnter()

    def update_encount_kraken(self):
        '''
        クラーケン出現イベントの処理
        '''
        # エンカウントフラグをONにする
        self.isEncount = True

        # 敵パーティー生成
        enemyParty.memberList = EnemyPartyGenerator.generate(
            monsterParams.monsterList[monsterParams.KRAKEN])

    def draw_encount_kraken(self):
        '''
        クラーケン出現イベントの表示
        '''
        pass

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_LIGHTBLUE, pyxel.COLOR_DARKBLUE)

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()