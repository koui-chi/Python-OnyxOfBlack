# -*- coding: utf-8 -*-
from module.baseState import BaseState

'''
 BaseFieldStateクラス
 - フィールド（街、ダンジョン）の基底クラス
 - 各フィールドで共通の処理を持つ
'''
class BaseFieldState(BaseState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(BaseFieldState, self).__init__(stateStack)
        self.stateName = "(none)"

    #
    # 各フレームの処理
    #
    def update(self):

#        print("BaseFieldState:update")

        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print("BaseFieldState:render")

        super().render()

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print("BaseFieldState:onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print("BaseFieldState:onExit")

