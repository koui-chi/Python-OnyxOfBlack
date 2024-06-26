# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB2 import dungeonB2
from module.params.monster import monsterParams
from overrides import overrides


class StateDungeonB2(BaseFieldState):
    '''
    地下迷宮B2のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    stateName = "DUNGEONB2"

    # マップ
    _map = dungeonB2.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(3),
        HumanGenerator.generate(4),
        monsterParams["BAT_LV2"],
        monsterParams["KOBOLD_LV2"],
        monsterParams["KOBOLD_LV2"],
        monsterParams["ZOMBIE_LV2"],
        monsterParams["ZOMBIE_LV2"],
        monsterParams["SKELETON_LV2"],
        monsterParams["SKELETON_LV2"],
        monsterParams["GOBLIN_LV2"],
        monsterParams["GOBLIN_LV2"],
        monsterParams["AZTEC_LV2"],
        monsterParams["AZTEC_LV2"],
        monsterParams["LION_LV2"],
        monsterParams["MUMMY_LV1"],
        monsterParams["ORC_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_LIGHT_BLUE, pyxel.COLOR_DARK_BLUE)

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
