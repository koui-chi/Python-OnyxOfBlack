# -*- coding: utf-8 -*-
import math
import random

import pyxel
from module.baseState import BaseState
from module.character import Character, Human, enemyParty, playerParty
from module.constant.alignment import Alignment
from module.constant.itemType import ItemType
from module.constant.state import State
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateBattle(BaseState):
    '''
    戦闘シーンのクラス/n
    BaseStateクラスを継承
    '''
    # 状態の定数
    STATE_ENCOUNT = 0
    STATE_CHOOSE_ACTION = 1
    STATE_ENEMY_ESCAPE_JUDGE = 2
    STATE_CHOOSE_TARGET = 3
    STATE_START_BATTLE = 4
    STATE_BATTLE = 5
    STATE_WIN_GETEXP = 6
    STATE_WIN_GETGOLD = 7
    STATE_JUDGE_GETITEM = 8
    STATE_LOSE = 9
    STATE_RUNAWAY_JUDGE = 10
    STATE_RUNAWAY_SUCCESS = 11
    STATE_RUNAWAY_FAILED = 12
    STATE_JUDGE_TALK = 28
    STATE_CHOOSE_TALK = 29
    STATE_TALK = 30
    STATE_TALK_FAILED = 31
    STATE_TALK_KOBOLD = 32
    STATE_CHOOSE_EQUIP = 41
    STATE_CHOOSE_ERROR = 42
    STATE_EQUIP = 43
    STATE_LEAVE = 44

    # ハンドラ用定数
    HANDLER_UPDATE = 0
    HANDLER_DRAW = 1

    # キーとインデックスの辞書
    key_to_index = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 行動順リスト
        self.turn_table = []

        # 行動順リストのインデックス
        self.turn_index = 0

        # 時間カウント用
        self.tick = 0

        # 戦闘に入ったか？
        self.isBattled = False

        # 逃走に成功したか？
        self.isRunaway = False

        # 敵は逃走したか？
        self.isEnemyEscpaed = False

        # メンバーのインデックス
        self.member_index = 0

        # メッセージリスト
        # 各リスト要素の1つ目はメッセージリスト、2つ目は表示色
        self.message = []

        # 報酬
        self.reward_exp = 0
        self.reward_gold = 0

        # ハンドラ辞書
        self.handler = {
            self.STATE_ENCOUNT: [self.update_encount, self.draw_encount],
            self.STATE_CHOOSE_ACTION: [self.update_choose_action, self.draw_choose_action],
            self.STATE_ENEMY_ESCAPE_JUDGE: [self.update_enemy_escape_judge, self.draw_enemy_escape_judge],
            self.STATE_CHOOSE_TARGET: [self.update_choose_target, self.draw_choose_target],
            self.STATE_START_BATTLE: [self.update_start_battle, self.draw_start_battle],
            self.STATE_BATTLE: [self.update_battle, self.draw_battle],
            self.STATE_WIN_GETEXP: [self.update_win_getexp, self.draw_win_getexp],
            self.STATE_WIN_GETGOLD: [self.update_win_getgold, self.draw_win_getgold],
            self.STATE_JUDGE_GETITEM: [self.update_judge_getitem, self.draw_judge_getitem],
            self.STATE_LOSE: [self.update_lose, self.draw_lose],
            self.STATE_RUNAWAY_JUDGE: [self.update_runaway_judge, self.draw_runaway_judge],
            self.STATE_RUNAWAY_FAILED: [self.update_runaway_failed, self.draw_runaway_failed],
            self.STATE_RUNAWAY_SUCCESS: [self.update_runaway_success, self.draw_runaway_success],
            self.STATE_JUDGE_TALK: [self.update_judge_talk, self.draw_judge_talk],
            self.STATE_CHOOSE_TALK: [self.update_choose_talk, self.draw_choose_talk],
            self.STATE_TALK: [self.update_talk, self.draw_talk],
            self.STATE_TALK_FAILED: [self.update_talk_failed, self.draw_talk_failed],
            self.STATE_TALK_KOBOLD: [self.update_talk_kobold, self.draw_talk_kobold],
            self.STATE_CHOOSE_EQUIP: [self.update_choose_equip, self.draw_choose_equip],
            self.STATE_CHOOSE_ERROR: [self.update_choose_error, self.draw_choose_error],
            self.STATE_EQUIP: [self.update_equip, self.draw_equip],
            self.STATE_LEAVE: [self.update_leave, self.draw_leave],
        }

        # 状態
        self.state = None

    def change_state(self, _state):
        '''
        状態変更処理
        '''
        self.state = _state
        self.tick = 0
        self.message = []

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_UPDATE]()

    def update_encount(self):
        '''
        遭遇時の処理
        ※未使用メソッド
        '''
        if self.tick == 1:
            pyxel.play(3, 1, loop=False)
        if self.tick > 80:
            self.change_state(self.STATE_CHOOSE_ACTION)

    def update_choose_action(self):
        '''
        プレイヤーパーティーの行動決定処理
        '''
        # コマンド入力
        if pyxel.btnp(pyxel.KEY_A):
            self.change_state(self.STATE_ENEMY_ESCAPE_JUDGE)
        if pyxel.btnp(pyxel.KEY_T):
            self.change_state(self.STATE_JUDGE_TALK)
        if pyxel.btnp(pyxel.KEY_R):
            self.change_state(self.STATE_RUNAWAY_JUDGE)

    def update_enemy_escape_judge(self):
        '''
        敵逃走判定処理
        '''
        if self.tick > 30:
            if self.isEnemyEscpaed:
                # 敵が逃げる場合は勝利
                self.change_state(self.STATE_WIN_GETEXP)
            else:
                # 敵が逃げない場合はプレイヤーパーティーの攻撃対象選択処理へ
                self.change_state(self.STATE_CHOOSE_TARGET)

        if self.tick == 1:
            # 敵パーティーは逃げるか？
            if enemyParty.isEscape():

                _playerMaxLevel = 0
                _playerStrength = 0
                _playerDamage = 0
                _playerSumLife = 0
                _playerSumMaxlife = 0
                for _member in playerParty.memberList:
                    if _member.level > _playerMaxLevel:
                        _playerMaxLevel = _member.level
                    _playerStrength += _member.strength
                    _playerSumLife += _member.life
                    _playerSumMaxlife += _member.maxlife
                _playerDamage = 1 - (_playerSumLife / _playerSumMaxlife)
                _playerRate = (_playerStrength * math.sqrt(_playerMaxLevel)
                               ) * _playerDamage + random.randint(1, 6)

                _enemyMaxLevel = 0
                _enemyStrength = 0
                _enemyDamage = 0
                _enemySumLife = 0
                _enemySumMaxlife = 0
                for _member in enemyParty.memberList:
                    if _member.level > _enemyMaxLevel:
                        _enemyMaxLevel = _member.level
                    _enemyStrength += _member.strength
                    _enemySumLife += _member.life
                    _enemySumMaxlife += _member.maxlife
                _enemyDamage = 1 - (_enemySumLife / _enemySumMaxlife)
                _enemyRate = (_enemyStrength * math.sqrt(_enemyMaxLevel)
                              ) * _enemyDamage + random.randint(1, 6)

                if _enemyMaxLevel >= _playerMaxLevel:
                    if _enemyDamage > 0.7 and _playerRate > _enemyRate:
                        self.isEnemyEscpaed = True
                else:
                    if _playerRate > _enemyRate:
                        self.isEnemyEscpaed = True

    def update_choose_target(self):
        '''
        プレイヤーパーティーの攻撃対象選択処理
        '''
        # 敵が1人の時は選択不要
        if len(enemyParty.memberList) == 1:
            playerParty.memberList[self.member_index].target = enemyParty.memberList[0]
            self.member_index += 1
        else:
            _idx = 0

            if pyxel.btnp(pyxel.KEY_1):
                _idx = 1
            elif pyxel.btnp(pyxel.KEY_2) and len(enemyParty.memberList) > 1:
                _idx = 2
            elif pyxel.btnp(pyxel.KEY_3) and len(enemyParty.memberList) > 2:
                _idx = 3
            elif pyxel.btnp(pyxel.KEY_4) and len(enemyParty.memberList) > 3:
                _idx = 4
            elif pyxel.btnp(pyxel.KEY_5) and len(enemyParty.memberList) > 4:
                _idx = 5

            if _idx > 0:
                playerParty.memberList[self.member_index].target = enemyParty.memberList[_idx - 1]
                self.member_index += 1

        # メンバーインデックスがプレイヤーパーティーを超えたら戦闘開始処理へ
        if self.member_index > len(playerParty.memberList) - 1:
            # プレイヤーパーティーのインデックス初期化
            self.member_index = 0
            self.change_state(self.STATE_START_BATTLE)

    def update_start_battle(self):
        '''
        戦闘開始処理
        '''
        # 敵の全てに対して、ランダムに攻撃対象を決定
        for _member in enemyParty.memberList:
            _member.target = playerParty.memberList[random.randint(
                0, len(playerParty.memberList) - 1)]

        # 行動順リスト
        self.turn_table = playerParty.memberList + enemyParty.memberList

        # イニシアチブ、攻撃値、防御値を設定
        for _member in self.turn_table:
            _member.initiative = _member.dexterity + random.randint(1, 12)

        # イニシアチブ値で降順でソート
        self.turn_table = sorted(
            self.turn_table, key=lambda k: k.initiative, reverse=True)

        # 行動順リストのインデックス初期化
        self.turn_index = 0

        # 戦闘に入った
        self.isBattled = True

        # 戦闘処理へ
        self.change_state(self.STATE_BATTLE)

    def update_battle(self):
        '''
        戦闘処理
        '''
        if self.tick > 30:
            self.tick = 0
            # 次の行動順リストへ
            self.turn_index += 1

            if self.turn_index > len(self.turn_table) - 1:
                # プレイヤーパーティーが全滅していたらプレイヤーパーティー全滅処理へ
                if len(playerParty.memberList) == 0:
                    self.change_state(self.STATE_LOSE)
                    return

                # 敵パーティーが全滅していたらプレイヤーパーティー勝利処理へ
                if len(enemyParty.memberList) == 0:
                    self.change_state(self.STATE_WIN_GETEXP)
                    return

                # どちらのパーティーも残っていたらプレイヤーパーティー行動決定処理へ
                self.state = self.STATE_CHOOSE_ACTION
                return

        if self.tick == 1:
            # 攻撃するキャラクター
            _attacker = self.turn_table[self.turn_index]

            # 攻撃の対象キャラクター
            _target = _attacker.target

            # 攻撃対象が生きていなければ抜ける
            if _target == None or _target.life < 1:
                self.tick = 31
                return

            # メッセージ初期化
            self.message = []

            # 攻撃ヒット判定
            _attacker_d = random.randint(2, 12)
            _target_d = random.randint(2, 12)
            if (_attacker.dexterity + _attacker_d < _target.dexterity + _target_d) or (_target_d == 12):
                # 避けた
                self.addMessage([""])
                self.addMessage(["*" + _target.name + " ", "KA",
                                 "D"], self.getMessageColor(_attacker))
                self.addMessage([""])
                self.addMessage(["*" + _attacker.name + " ", "WO", " ",
                                 "YO", "KE", "TA", "."], self.getMessageColor(_attacker))
            else:
                # 攻撃値算出
                _attack = _attacker.strength + random.randint(2, 12)

                # 人間のキャラクタで武器を持っている場合は補正
                if isinstance(_attacker, Human) and _attacker.weapon != None:
                    _attack = _attack + \
                        random.randint(_attacker.weapon.attack //
                                       2, _attacker.weapon.attack)

                # 防御値算出
                _defend = _target.defend + random.randint(2, 12)

                if isinstance(_target, Human):
                    # 鎧
                    if _target.armor != None:
                        _defend = _defend + \
                            random.randint(_target.armor.armor //
                                           2, _target.armor.armor)
                    # 盾
                    if _target.shield != None:
                        _defend = _defend + \
                            random.randint(_target.shield.armor //
                                           2, _target.shield.armor)
                    # 兜
                    if _target.helmet != None:
                        _defend = _defend + \
                            random.randint(_target.helmet.armor //
                                           2, _target.helmet.armor)

                # ダメージ計算
                if _attacker_d == 12:
                    self.addMessage(["**** GOOD SHOT ***"], pyxel.COLOR_YELLOW)
                    _damage = _attack
                else:
                    self.addMessage([""])
                    _damage = _attack - _defend

                if _damage < 1:
                    # 受け止めた
                    self.addMessage(
                        ["*" + _target.name + " ", "KA", "D"], self.getMessageColor(_attacker))
                    self.addMessage([""])
                    self.addMessage(["*" + _attacker.name + " ", "WO", " ", "U",
                                     "KE", "TO", "ME", "TA", "."], self.getMessageColor(_attacker))
                else:
                    _target.life = _target.life - _damage

                    # レイスの場合、一定確率でエナジードレイン攻撃をする
                    if _attacker.isPlayer == False and _attacker.name[0:6] == "WRAITH":
                        _target.maxlife = _target.maxlife - (_damage // 10 + 1)

                    if _target.life < 1:
                        # しとめた
                        self.addMessage(
                            ["*" + _attacker.name + " ", "KA", "D"], self.getMessageColor(_attacker))
                        self.addMessage([""])
                        self.addMessage(["*" + _target.name + " ", "WO", " ", "SI",
                                         "TO", "ME", "TA", "* !"], self.getMessageColor(_attacker))

                        #  行動順リストから外す
                        for _idx, _value in enumerate(self.turn_table):
                            if _value is _target:
                                del self.turn_table[_idx]
                                break

                        if _target.isPlayer:
                            # プレイヤーパーティーから外す
                            for _idx, _value in enumerate(playerParty.memberList):
                                if _value is _target:
                                    del playerParty.memberList[_idx]
                                    break
                        else:
                            # 敵パーティーから外す
                            for _idx, _value in enumerate(enemyParty.memberList):
                                if _value is _target:
                                    self.reward_exp = self.reward_exp + _target.exp
                                    self.reward_gold = self.reward_gold + _target.gold
                                    del enemyParty.memberList[_idx]
                                    break

                    else:
                        # ダメージをあたえた
                        self.addMessage(["*" + _attacker.name + " ", "KA", "D", "* " +
                                         _target.name + " ", "NI"], self.getMessageColor(_attacker))
                        self.addMessage([""])
                        self.addMessage(["*" + str(_damage) + " ", "NO", " ", "ta", "d", "me", "-", "si",
                                         "d", "WO", " ", "A", "TA", "E", "TA", "* !"], self.getMessageColor(_attacker))
                            

    def update_win_getexp(self):
        '''
        経験値獲得処理
        '''
        _member = playerParty.memberList[self.member_index]
        if self.tick == 1:
            # 経験値加算
            _member.exp = _member.exp + (self.reward_exp // _member.level)
            if _member.exp > 200:
                _member.exp = 200

            # レベルアップするか？
            if _member.exp == 200:
                # メッセージをセット
                self.message = []
                self.addMessage(["**** CONGRATULATIONS ***"], pyxel.COLOR_CYAN)
                self.addMessage([""])
                self.addMessage(["*" + playerParty.memberList[self.member_index].name + " ", "HA", " ", "re", "he", "d", "ru", "* " + str(
                    playerParty.memberList[self.member_index].level + 1) + " ", "NI", " ", "NA", "RI", "MA", "SI", "TA", "."])

        if _member.exp == 200:
            if pyxel.btnp(pyxel.KEY_SPACE):
                # レベルアップ
                _member.levelup()

                self.tick = 0
                self.member_index += 1

        else:
            self.tick = 0
            self.member_index += 1

        if self.member_index > len(playerParty.memberList) - 1:
            if self.reward_gold == 0:
                self.change_state(self.STATE_JUDGE_GETITEM)
            else:
                self.change_state(self.STATE_WIN_GETGOLD)

    def update_win_getgold(self):
        '''
        ゴールド獲得処理
        '''
        if self.tick == 1:
            # ゴールドを分配
            self.reward_gold = self.reward_gold // len(playerParty.memberList)
            # 分配した結果、0ゴールドなら戦闘終了
            if self.reward_gold == 0:
                self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_SPACE):
            # プレイヤーパーティーの各メンバーのゴールドを加算
            for _member in playerParty.memberList:
                _member.gold = _member.gold + self.reward_gold

            self.change_state(self.STATE_JUDGE_GETITEM)

    def update_judge_getitem(self):
        '''
        アイテム取得判定処理
        '''
        # アイテム入手
        if enemyParty.item != None:
            self.state = self.STATE_CHOOSE_EQUIP
        else:
            self.state = self.STATE_LEAVE

    def update_lose(self):
        '''
        プレイヤーパーティー全滅処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.stateStack.clear()
            self.stateStack.push(State.TITLE)

    def update_runaway_judge(self):
        '''
        逃走判定処理
        '''
        # クラーケンは絶対逃げられない
        if enemyParty.memberList[0].name[0:6] == "KRAKEN":
            self.change_state(self.STATE_RUNAWAY_FAILED)
            return

        _enemyDexterity = 0
        for _member in enemyParty.memberList:
            _enemyDexterity += _member.dexterity
        _enemyDexterity = (_enemyDexterity //
                           len(enemyParty.memberList)) + random.randint(0, 6)
        _playerDexterity = 0
        for _member in playerParty.memberList:
            _playerDexterity += _member.dexterity
        _playerDexterity = (
            _playerDexterity // len(playerParty.memberList)) + random.randint(0, 12)
        if _playerDexterity > _enemyDexterity:
            self.change_state(self.STATE_RUNAWAY_SUCCESS)
        else:
            self.change_state(self.STATE_RUNAWAY_FAILED)

    def update_runaway_success(self):
        '''
        逃走成功処理
        '''
        if self.tick > 30:
            playerParty.isEscaped = True
            self.tick = 0
            self.stateStack.pop()
        else:
            self.tick += 1

    def update_runaway_failed(self):
        '''
        逃走失敗処理
        '''
        if self.tick > 30:
            self.change_state(self.STATE_START_BATTLE)
            for _member in playerParty.memberList:
                _member.target = None
        else:
            self.tick += 1

    def update_judge_talk(self):
        '''
        会話判定処理
        '''
        # 敵のパーティーは人間で性格がGOOD、かつ一度も戦闘していないか？
        if isinstance(enemyParty.memberList[0], Human) and enemyParty.memberList[0].alignment == Alignment.GOOD and self.isBattled == False:
            # プレイヤーパーティーの人数 + 敵パーティーの人数 は 5以内か？
            if len(playerParty.memberList) + len(enemyParty.memberList) <= 5:
                # 会話選択へ
                self.change_state(self.STATE_CHOOSE_TALK)
            else:
                # 会話表示へ
                self.change_state(self.STATE_TALK)

        # 敵のパーティーはコボルドで、コボルド語を知っているか？
        elif enemyParty.memberList[0].name[0:6] == "KOBOLD" and playerParty.eventFlg[10] == 1:
            # 会話失敗（コボルド）へ
            self.change_state(self.STATE_TALK_KOBOLD)
        else:
            # 会話失敗へ
            self.change_state(self.STATE_TALK_FAILED)

    def update_choose_talk(self):
        '''
        会話選択処理
        '''
        if pyxel.btnp(pyxel.KEY_J):
            # 敵パーティーをプレイヤーパーティーに加える
            for _member in enemyParty.memberList:
                _member.isPlayer = True
                playerParty.memberList.append(_member)
            # 戦闘終了
            self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_G):
            # 戦闘終了
            self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_Y):
            # 戦闘へ
            self.change_state(self.STATE_ENEMY_ESCAPE_JUDGE)

    def update_talk(self):
        '''
        会話表示処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 戦闘終了
            self.stateStack.pop()

    def update_talk_failed(self):
        '''
        会話失敗処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 戦闘へ
            self.change_state(self.STATE_START_BATTLE)
            for _member in playerParty.memberList:
                _member.target = None

    def update_talk_kobold(self):
        '''
        会話失敗（コボルド）処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 戦闘へ
            self.change_state(self.STATE_START_BATTLE)
            for _member in playerParty.memberList:
                _member.target = None

        
    def update_choose_equip(self):
        '''
        装備するメンバーの選択処理
        '''
        if pyxel.btnp(pyxel.KEY_L):
            self.change_state(self.STATE_LEAVE)
            return

        _idx = 0

        if pyxel.btnp(pyxel.KEY_1):
            _idx = 1
        elif pyxel.btnp(pyxel.KEY_2) and len(playerParty.memberList) > 1:
            _idx = 2
        elif pyxel.btnp(pyxel.KEY_3) and len(playerParty.memberList) > 2:
            _idx = 3
        elif pyxel.btnp(pyxel.KEY_4) and len(playerParty.memberList) > 3:
            _idx = 4
        elif pyxel.btnp(pyxel.KEY_5) and len(playerParty.memberList) > 4:
            _idx = 5

        if _idx > 0:
            self.member_index = _idx - 1
            # 種別が武器の時で両手持ちの時は、対象キャラクターが盾を持っている場合はエラーとする
            if enemyParty.itemType == ItemType.WEAPON and enemyParty.item.isDoubleHand and playerParty.memberList[self.member_index].shield != None:
                self.change_state(self.STATE_CHOOSE_ERROR)
            else:
                self.change_state(self.STATE_EQUIP)


    def update_choose_error(self):
        '''
        装備不可エラーの処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.change_state(self.STATE_CHOOSE_EQUIP)


    def update_equip(self):
        '''
        アイテム装備処理
        '''
        if enemyParty.itemType == ItemType.WEAPON:
            playerParty.memberList[self.member_index].weapon = enemyParty.item
        elif enemyParty.itemType == ItemType.ARMOR:
            playerParty.memberList[self.member_index].armor = enemyParty.item
        else:
            pass

        self.change_state(self.STATE_LEAVE)

    def update_leave(self):
        '''
        終了処理
        '''
        self.stateStack.pop()

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        # 敵の描画
        if self.state != self.STATE_ENCOUNT:
            for _chr in enemyParty.memberList:
                super().drawCharacter(_chr, _chr.x, _chr.y)

            for _idx in range(5 if len(enemyParty.memberList) > 5 else len(enemyParty.memberList)):
                # ステータス
                _member = enemyParty.memberList[_idx]
                # 名前
                PyxelUtil.text(136,  (_idx + 1) * 16 - 2,
                               ["*" + _member.name], pyxel.COLOR_WHITE)
                # 体力最大値
                _maxlife_x = _member.maxlife if _member.maxlife <= 100 else 100
                pyxel.rect(136, (_idx + 1) * 16 + 6,
                           _maxlife_x, 3,  pyxel.COLOR_RED)
                # 体力
                _life_x = _member.life if _member.life <= 100 else 100
                pyxel.rect(136, (_idx + 1) * 16 + 6,
                           _life_x, 3,  pyxel.COLOR_DARK_BLUE)

        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_DRAW]()

    def draw_encount(self):
        '''
        遭遇時の表示処理
        ※未使用メソッド
        '''
        print("call draw encount:nanikatikaduitekita")
        PyxelUtil.text(56, 148, ["NA", "NI", "KA", " ", "TI", "KA",
                                 "TU", "D", "I", "TE", "KI", "TA", "* !"], pyxel.COLOR_RED)

    def draw_choose_action(self):
        '''
        プレイヤーパーティーの行動決定表示処理
        '''
        PyxelUtil.text(16, 140, ["TO", "D", "U", "SI",
                                 "MA", "SU", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 156, ["*     [A] ", "TA", "TA",
                                 "KA", "U"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 164, ["*     [R] ", "NI", "KE",
                                 "D", "RU"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 172, ["*     [T] ", "HA", "NA",
                                 "SU"], pyxel.COLOR_YELLOW)

    def draw_enemy_escape_judge(self):
        '''
        敵逃走判定表示処理
        '''
        if self.isEnemyEscpaed:
            PyxelUtil.text(16, 140, [
                           "NI", "KE", "D", "TE", " ", "I", "LTU", "TA", "*..."], pyxel.COLOR_WHITE)
        else:
            PyxelUtil.text(90, 148, ["** * *  BATTLE  * * *"], pyxel.COLOR_RED)

    def draw_choose_target(self):
        '''
        プレイヤーパーティーの攻撃対象選択表示処理
        '''
        if len(enemyParty.memberList) == 1:
            return

        PyxelUtil.text(16, 140, ["TO", "D", "RE", "WO", " ", "KO", "U", "KE", "D", "KI", " ", "SI", "MA",
                                 "SU", "KA", ",", "*" + playerParty.memberList[self.member_index].name, "* ?"], pyxel.COLOR_WHITE)
        for _idx in range(5 if len(enemyParty.memberList) > 5 else len(enemyParty.memberList)):
            PyxelUtil.text(24, 148 + _idx * 8,
                           "*[{:1}]".format(_idx + 1), pyxel.COLOR_YELLOW)
            PyxelUtil.text(40, 148 + _idx * 8, "*" +
                           enemyParty.memberList[_idx].name, pyxel.COLOR_LIGHT_BLUE)

    def draw_start_battle(self):
        '''
        戦闘開始表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_battle(self):
        '''
        戦闘表示処理
        '''
        if self.message != None and len(self.message) > 0:
            for idx, value in enumerate(self.message):
                PyxelUtil.text(16, 140 + idx * 8, value[0], value[1])

    def draw_win_getexp(self):
        '''
        経験値獲得表示処理
        '''
        if self.message != None and len(self.message) > 0:
            for idx, value in enumerate(self.message):
                PyxelUtil.text(16, 140 + idx * 8, value[0], value[1])
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_win_getgold(self):
        '''
        ゴールド獲得表示処理
        '''
        if self.reward_gold > 0:
            PyxelUtil.text(16, 148, ["*" + str(self.reward_gold) + " G.P. ", "TU", "D", "TU",
                                     "NO", " ", "*gold", "WO", " ", "MI", "TU", "KE", "TA", "* !"], pyxel.COLOR_WHITE)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_judge_getitem(self):
        '''
        アイテム取得判定表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_lose(self):
        '''
        プレイヤーパーティー全滅表示処理
        '''
        PyxelUtil.text(70, 156, ["*+ + ", "SE", "D", "NN", "ME", "TU",
                                 " ", "SI", "MA", "SI", "TA", "* + +"], pyxel.COLOR_RED)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_runaway_judge(self):
        '''
        逃走成功表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_runaway_success(self):
        '''
        逃走成功表示処理
        '''
        PyxelUtil.text(46, 148, ["I", "TU", "MO", " ", "U", "MA", "KU", "I", "KU", "TO", "HA",
                                 " ", "KA", "KI", "D", "RI", "MA", "SE", "NN", "YO", "*..."], pyxel.COLOR_WHITE)

    def draw_runaway_failed(self):
        '''
        逃走失敗表示処理
        '''
        PyxelUtil.text(56, 148, ["SI", "MA", "LTU", "TA", "* ! ", "NI",
                                 "KE", "D", "RA", "RE", "NA", "I", "* !"], pyxel.COLOR_RED)

    def draw_judge_talk(self):
        '''
        会話判定表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_choose_talk(self):
        '''
        会話選択表示処理
        '''
        PyxelUtil.text(16, 140, ["NA", "NI", "WO", " ", "HA", "NA",
                                 "SI", "KA", "KE", "MA", "SU", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 156, ["*     [J] JOIN US."], pyxel.COLOR_YELLOW)
        PyxelUtil.text(
            16, 164, ["*     [G] GOOD LUCK & GOOD BY."], pyxel.COLOR_YELLOW)
        PyxelUtil.text(
            16, 172, ["*     [Y] YOUR MONEY OR YOUR LIFE."], pyxel.COLOR_YELLOW)

    def draw_talk(self):
        '''
        会話表示処理
        '''
        PyxelUtil.text(16, 148, ["*ONYX", "WO", " ", "ME", "SA", "D", "SI", "TE", " ", "KA",
                                 "D", "NN", "HA", "D", "RI", "MA", "SI", "LYO", "U", "* !"], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_talk_failed(self):
        '''
        会話失敗処理
        '''
        PyxelUtil.text(16, 148, ["HA", "NA", "SI", "NI", " ", "NA",
                                 "RA", "NA", "KA", "LTU", "TA", "* !"], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_talk_kobold(self):
        '''
        会話失敗（コボルド）処理
        '''
        PyxelUtil.text(16, 148, ["u", "ma", "so", "u", "na", " ", "ni",
                                 "nn", "ke", "d", "nn", "ta", "d", "* !"], pyxel.COLOR_LIGHT_BLUE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)


    def draw_choose_equip(self):
        '''
        装備するメンバーの選択表示処理
        '''
        if enemyParty.item.name == "MAGIC MANTLE":
            PyxelUtil.text(16, 140, ["MA", "HO", "U", "NO", "ma", "nn", "to", "WO", " ", "MI", "TU", "KE", "TA", "* !"], pyxel.COLOR_WHITE)
        else:
            PyxelUtil.text(16, 140, ["SU", "HA", "D", "RA", "SI", "I",
                                    "* " + enemyParty.item.name + " ", "WO", " ", "MI", "TU", "KE", "TA", "* !"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TA", "D", "RE", "KA", "D", " ", "TU", "KA", "I", "MA", "SU", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 172, ["*     [L] ", "TU", "KA",
                                 "WA", "NA", "I"], pyxel.COLOR_YELLOW)

    def draw_choose_error(self):
        '''
        装備不可エラーの表示処理
        '''
        PyxelUtil.text(16, 140, ["*" + playerParty.memberList[self.member_index].name + " ", "HA", 
                                "* " + enemyParty.item.name + " ", "WO", " ", "MO", "TE", "NA", "I", "* !"], pyxel.COLOR_RED)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_equip(self):
        '''
        アイテム装備表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_leave(self):
        '''
        終了表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 状態を最初に設定する
        self.state = self.STATE_CHOOSE_ACTION

        # 報酬を初期化
        self.reward_exp = 0
        self.reward_gold = 0

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass

    def clearMessage(self) -> None:
        '''
        メッセージクリア
        '''
        self.message = []

    def addMessage(self, argMessage, argColor=pyxel.COLOR_WHITE) -> None:
        '''
        メッセージ追加処理\n
        引数に追加するメッセージ（リスト）と表示色（省略時は白）を指定する。
        '''
        self.message.append([argMessage, argColor])

    def getMessageColor(self, argCharacter: Character) -> int:
        '''
        メッセージ表示色を返却する。\n
        引数に与えたCharacterクラスのインスタンスがプレイヤーだった場合は白、以外は赤を返却する。
        '''
        return pyxel.COLOR_WHITE if argCharacter.isPlayer else pyxel.COLOR_RED
