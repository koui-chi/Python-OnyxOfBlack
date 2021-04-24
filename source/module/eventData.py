# -*- coding: utf-8 -*-

class eventData(object):

    # イベントデータの辞書
    events = {}

    def __init__(self) -> None:
        '''
        クラス初期化
        '''
        super().__init__()

        # イベント辞書の初期化処理を呼ぶ
        self.reset()

    def reset(self) -> None:
        '''
        イベント辞書の初期化処理
        '''
        self.events = {
            "CITY17040D": "self.draw_gate()",
            "CITY18040D": "self.draw_gate()",
            "CITY17030U": "playerParty.restoreCondition()",
            "CITY18030U": "playerParty.restoreCondition()",
            "CITY27073D": "self.draw_shieldshop()",
            "CITY26073U": "self.stateStack.push(State.SHIELDSHOP)",
            "CITY27061D": "self.draw_armorshop()",
            "CITY28061U": "self.stateStack.push(State.ARMORSHOP)",
            "CITY27081D": "self.draw_weaponshop()",
            "CITY28081U": "self.stateStack.push(State.WEAPONSHOP)",
            "CITY27101D": "self.draw_helmetshop()",
            "CITY28101U": "self.stateStack.push(State.HELMETSHOP)",
            "CITY27113D": "self.draw_barbar()",
            "CITY26113U": "self.stateStack.push(State.BARBAR)",
            "CITY08073D": "self.draw_donotenter()",
            "CITY21052D": "self.draw_inn()",
            "CITY23092D": "self.draw_physicker()",
            "CITY23100D": "self.draw_physicker_exit()",
            "CITY23103D": "self.draw_drugs()",
            "CITY22103U": "self.stateStack.push(State.DRUGS)",
            "CITY23101D": "self.draw_surgery()",
            "CITY24101U": "self.stateStack.push(State.SURGERY)",
            "CITY23111D": "self.draw_examinations()",
            "CITY24111U": "self.stateStack.push(State.EXAMINATIONS)",
            "CITY19141D": "self.draw_thewall()",
            "CITY20143D": "self.draw_thewall()",
            "CITY10102D": "self.draw_jail()",
            "CITY12193U": "self.startEvent('city_002.json')",
            "CITY18090D": "self.draw_directionmarket()",
            "CITY18092D": "self.draw_directionmarket()",
            "CITY24142D": "self.draw_cemetery()",
            "CITY24152D": "self.draw_cemetery()",
            "CITY23189U": "self.startEvent('city_003.json')",
            "CITY25179U": "self.startEvent('city_003.json')",
            "CITY25209U": "self.startEvent('city_003.json')",
            "CITY26199U": "self.startEvent('city_003.json')",
            "CITY28131D": "self.draw_temple()",
            "CITY28141D": "self.draw_temple()",
            "CITY28151D": "self.draw_temple()",
            "CITY29131U": "playerParty.restoreCondition()",
            "CITY29141U": "playerParty.restoreCondition()",
            "CITY29151U": "playerParty.restoreCondition()",
            "CITY15149U": "self.startEvent('city_001.json')",
            "CITY03069U": "self.startEvent('city_007.json')",
            "CITY16189U": "self.startEvent('city_004.json')",
            "CITY21069U": "self.startEvent('city_test.json')",

            "CEMETERY23189U": "self.startEvent('cemetery_001.json')",
            "CEMETERY25179U": "self.startEvent('cemetery_001.json')",
            "CEMETERY25209U": "self.startEvent('cemetery_001.json')",
            "CEMETERY26199U": "self.startEvent('cemetery_001.json')",
            "CEMETERY23239U": "self.update_fixed_encount_enemy()",
            "CEMETERY23259U": "self.update_fixed_encount_enemy()",
            "CEMETERY23279U": "self.update_fixed_encount_enemy()",
            "CEMETERY25269U": "self.update_fixed_encount_enemy()",
            "CEMETERY25289U": "self.update_fixed_encount_enemy()",
            "CEMETERY31319U": "self.update_fixed_encount_enemy()",
            "CEMETERY32299U": "self.update_fixed_encount_enemy()",
            "CEMETERY33319U": "self.update_fixed_encount_enemy()",
            "CEMETERY34299U": "self.update_fixed_encount_enemy()",

            "WELLB115149U": "self.startEvent('wellb1_001.json')",
            "WELLB117179U": "self.update_fixed_encount_enemy()",
            "WELLB119169U": "self.update_fixed_encount_enemy()",
            "WELLB120139U": "self.update_fixed_encount_enemy()",
            "WELLB122099U": "self.update_fixed_encount_enemy()",
            "WELLB123139U": "self.update_fixed_encount_enemy()",
            "WELLB124119U": "self.update_fixed_encount_enemy()",

            "WELLB215149U": "self.startEvent('wellb2_001.json')",

            "WELLB315149U": "self.startEvent('wellb3_001.json')",

            "WELLB415149U": "self.startEvent('wellb4_001.json')",

            "DUNGEONB103069U": "self.startEvent('dungeonb1_001.json')",
            "DUNGEONB118219U": "self.startEvent('dungeonb1_002.json')",
            "DUNGEONB117189U": "self.startEvent('dungeonb1_001.json')",
            "DUNGEONB102119U": "self.update_fixed_encount_enemy()",
            "DUNGEONB102139U": "self.update_fixed_encount_enemy()",
            "DUNGEONB104119U": "self.update_fixed_encount_enemy()",
            "DUNGEONB104139U": "self.update_fixed_encount_enemy()",
            "DUNGEONB104059U": "self.update_fixed_encount_enemy()",
            "DUNGEONB105079U": "self.update_fixed_encount_enemy()",
            "DUNGEONB106059U": "self.update_fixed_encount_enemy()",
            "DUNGEONB107079U": "self.update_fixed_encount_enemy()",
            "DUNGEONB108059U": "self.update_fixed_encount_enemy()",
            "DUNGEONB108079U": "self.update_fixed_encount_enemy()",
            "DUNGEONB109039U": "self.update_fixed_encount_enemy()",
            "DUNGEONB110029U": "self.update_fixed_encount_enemy()",
            "DUNGEONB110059U": "self.update_fixed_encount_enemy()",
            "DUNGEONB110089U": "self.update_fixed_encount_enemy()",
            "DUNGEONB111029U": "self.update_fixed_encount_enemy()",
            "DUNGEONB111069U": "self.update_fixed_encount_enemy()",

            "DUNGEONB218219U": "self.startEvent('dungeonb2_001.json')",
            "DUNGEONB216279U": "self.startEvent('dungeonb2_002.json')",
            "DUNGEONB229199U": "self.startEvent('dungeonb2_002.json')",
            "DUNGEONB226129U": "self.startEvent('dungeonb2_002.json')",
            "DUNGEONB212159U": "self.startEvent('dungeonb2_001.json')",
            "DUNGEONB217179U": "self.startEvent('dungeonb2_001.json')",
            "DUNGEONB215119U": "self.update_fixed_encount_enemy()",
            "DUNGEONB218109U": "self.update_fixed_encount_enemy()",
            "DUNGEONB219099U": "self.update_fixed_encount_enemy()",
            "DUNGEONB219279U": "self.update_fixed_encount_enemy()",
            "DUNGEONB220249U": "self.update_fixed_encount_enemy()",
            "DUNGEONB221279U": "self.update_fixed_encount_enemy()",
            "DUNGEONB222069U": "self.update_fixed_encount_enemy()",
            "DUNGEONB222289U": "self.update_fixed_encount_enemy()",
            "DUNGEONB224189U": "self.update_fixed_encount_enemy()",
            "DUNGEONB226189U": "self.update_fixed_encount_enemy()",
            "DUNGEONB232299U": "self.update_fixed_encount_enemy()",

            "DUNGEONB316289U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB306069U": "self.startEvent('dungeonb3_002.json')",
            "DUNGEONB329199U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB326129U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB303239U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB316179U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB308189U": "self.update_fixed_encount_enemy()",
            "DUNGEONB308259U": "self.update_fixed_encount_enemy()",
            "DUNGEONB309229U": "self.update_fixed_encount_enemy()",
            "DUNGEONB310279U": "self.update_fixed_encount_enemy()",
            "DUNGEONB310299U": "self.update_fixed_encount_enemy()",
            "DUNGEONB311319U": "self.update_fixed_encount_enemy()",
            "DUNGEONB311329U": "self.update_fixed_encount_enemy()",
            "DUNGEONB314289U": "self.update_fixed_encount_enemy()",
            "DUNGEONB316209U": "self.update_fixed_encount_enemy()",
            "DUNGEONB316269U": "self.update_fixed_encount_enemy()",
            "DUNGEONB318259U": "self.update_fixed_encount_enemy()",
            "DUNGEONB318289U": "self.update_fixed_encount_enemy()",
            "DUNGEONB326179U": "self.update_fixed_encount_enemy()",
            
            "DUNGEONB406069U": "self.startEvent('dungeonb4_001.json')",
            "DUNGEONB424249U": "self.startEvent('dungeonb4_002.json')",
            "DUNGEONB403109U": "self.startEvent('dungeonb4_001.json')",
            "DUNGEONB416189U": "self.startEvent('dungeonb4_001.json')",
            "DUNGEONB409079U": "self.update_fixed_encount_enemy()",
            "DUNGEONB412099U": "self.update_fixed_encount_enemy()",
            "DUNGEONB414119U": "self.update_fixed_encount_enemy()",
            "DUNGEONB414209U": "self.update_fixed_encount_enemy()",
            "DUNGEONB416079U": "self.update_fixed_encount_enemy()",
            "DUNGEONB416219U": "self.update_fixed_encount_enemy()",
            "DUNGEONB417069U": "self.update_fixed_encount_enemy()",
            "DUNGEONB417219U": "self.update_fixed_encount_enemy()",
            "DUNGEONB417239U": "self.update_fixed_encount_enemy()",
            "DUNGEONB418209U": "self.update_fixed_encount_enemy()",
            "DUNGEONB420069U": "self.update_fixed_encount_enemy()",
            "DUNGEONB423159U": "self.update_fixed_encount_enemy()",
            "DUNGEONB423179U": "self.update_fixed_encount_enemy()",
            "DUNGEONB423209U": "self.update_fixed_encount_enemy()",
            "DUNGEONB426219U": "self.update_fixed_encount_enemy()",
            "DUNGEONB428229U": "self.update_fixed_encount_enemy()",
            "DUNGEONB428269U": "self.update_fixed_encount_enemy()",
            "DUNGEONB428289U": "self.update_fixed_encount_enemy()",
            "DUNGEONB428299U": "self.update_fixed_encount_enemy()",
            "DUNGEONB428309U": "self.update_fixed_encount_enemy()",

            "DUNGEONB515149U": "self.update_encount_kraken()",
            "DUNGEONB524249U": "self.startEvent('dungeonb5_001.json')",
            "DUNGEONB518269U": "self.startEvent('dungeonb5_002.json')",
            "DUNGEONB508159U": "self.startEvent('dungeonb5_001.json')",
            "DUNGEONB517189U": "self.startEvent('dungeonb5_001.json')",
            "DUNGEONB517059D": "self.update_fixed_encount_enemy()",
            "DUNGEONB517169D": "self.update_fixed_encount_enemy()",
            "DUNGEONB520329D": "self.update_fixed_encount_enemy()",
            "DUNGEONB526139D": "self.update_fixed_encount_enemy()",
            "DUNGEONB527069D": "self.update_fixed_encount_enemy()",
            "DUNGEONB527079D": "self.update_fixed_encount_enemy()",
            "DUNGEONB527099D": "self.update_fixed_encount_enemy()",
            "DUNGEONB528139D": "self.update_fixed_encount_enemy()",
            "DUNGEONB529309D": "self.update_fixed_encount_enemy()",
            "DUNGEONB530329D": "self.update_fixed_encount_enemy()",
            "DUNGEONB531259D": "self.update_fixed_encount_enemy()",
            "DUNGEONB531309D": "self.update_fixed_encount_enemy()",
            "DUNGEONB533289D": "self.update_fixed_encount_enemy()",

            "COLORD_YELLOW18269U": "self.startEvent('colord_yellow_001.json')",
            "COLORD_YELLOW22219U": "self.startEvent('colord_yellow_002.json')",
            "COLORD_YELLOW17239U": "self.startEvent('colord_yellow_003.json')",
            "COLORD_YELLOW23309U": "self.startEvent('colord_yellow_004.json')",
            "COLORD_YELLOW13229U": "self.startEvent('colord_yellow_005.json')",
            "COLORD_YELLOW14179U": "self.startEvent('colord_yellow_006.json')",

            "COLORD_RED20179U": "self.startEvent('colord_red_001.json')",
            "COLORD_RED21219U": "self.startEvent('colord_red_002.json')",
            "COLORD_RED26219U": "self.startEvent('colord_red_003.json')",
            "COLORD_RED26259U": "self.startEvent('colord_red_004.json')",
            "COLORD_RED26319U": "self.startEvent('colord_red_005.json')",

            "COLORD_PURPLE15099U": "self.startEvent('colord_purple_001.json')",
            "COLORD_PURPLE20189U": "self.startEvent('colord_purple_002.json')",
            "COLORD_PURPLE23139U": "self.startEvent('colord_purple_003.json')",
            "COLORD_PURPLE23099U": "self.startEvent('colord_purple_004.json')",
            "COLORD_PURPLE14129U": "self.startEvent('colord_purple_005.json')",

            "COLORD_GREEN13239U": "self.startEvent('colord_green_001.json')",
            "COLORD_GREEN18239U": "self.startEvent('colord_green_002.json')",
            "COLORD_GREEN09259U": "self.startEvent('colord_green_003.json')",
            "COLORD_GREEN13309U": "self.startEvent('colord_green_004.json')",
            "COLORD_GREEN15309U": "self.startEvent('colord_green_005.json')",

            "COLORD_BLUE14229U": "self.startEvent('colord_blue_001.json')",
            "COLORD_BLUE06129U": "self.startEvent('colord_blue_002.json')",
            "COLORD_BLUE08139U": "self.startEvent('colord_blue_003.json')",
            "COLORD_BLUE09219U": "self.startEvent('colord_blue_004.json')",
            "COLORD_BLUE14239U": "self.startEvent('colord_blue_005.json')",

            "COLORD_WHITE17179U": "self.startEvent('colord_white_001.json')",
            "COLORD_WHITE14189U": "self.startEvent('colord_white_002.json')",
            "COLORD_WHITE15129U": "self.startEvent('colord_white_003.json')",
            "COLORD_WHITE07139U": "self.startEvent('colord_white_004.json')",
            "COLORD_WHITE08099U": "self.startEvent('colord_white_005.json')",
            "COLORD_WHITE12109U": "self.startEvent('colord_white_006.json')",
            "COLORD_WHITE16189U": "self.startEvent('colord_white_007.json')",

            "COLORD_BLACK17169U": "self.startEvent('colord_black_001.json')",
            "COLORD_BLACK16189U": "self.startEvent('colord_black_002.json')",
        }

# インスタンスを生成
eventdata = eventData()