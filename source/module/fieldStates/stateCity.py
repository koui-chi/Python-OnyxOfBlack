# -*- coding: utf-8 -*-
import pyxel
from module.pyxelUtil import PyxelUtil
from module.fieldStates.baseFieldState import BaseFieldState

'''
 StateCityクラス
 - ウツロの街のクラス(BaseFiledStateを継承)
 - マップデータを保持する
 - イベントの処理を持つ
 - 各Stateへの遷移を行う
'''
class StateCity(BaseFieldState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateCity, self).__init__(stateStack)
        self.stateName = "City"

        self.count = 0

    #
    # 各フレームの処理
    #
    def update(self):

        print(self.stateName + ":update")
        '''
        if self.count == 0:
            self.stateStack.push(self.stateStack.STATE_WEAPONSHOP)
            self.count = 1
        elif self.count == 1:
            self.stateStack.push(self.stateStack.STATE_ARMORSHOP)
            self.count = 2
        elif self.count == 2:
            self.stateStack.pop()
        print(self.count)
        '''

    #
    # 各フレームの画面描画処理
    #
    def render(self):

        super().render()

#        pyxel.text(0, app.message_y, self.stateName , 7)
#        app.message_y = app.message_y + 6
        print(self.stateName + ":render")

        PyxelUtil.text(50,  60, ["u", "tu", "ro", "NO", "MA", "TI"], 7)
        PyxelUtil.text(50,  70, ["*[W]:", "HU", "D", "KI", "YA"], 7)
        PyxelUtil.text(50,  78, ["*[A]:", "YO", "RO", "I", "YA"], 7)
        PyxelUtil.text(50,  86, ["*[S]:", "TA", "TE", "YA"], 7)
        PyxelUtil.text(50,  94, ["*[H]:", "KA", "HU", "D", "TO", "YA"], 7)
        PyxelUtil.text(50, 102, ["*[B]:", "TO", "KO", "YA"], 7)

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print(self.stateName + ":onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")

