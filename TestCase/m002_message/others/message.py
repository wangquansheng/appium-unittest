import time

from selenium.common.exceptions import TimeoutException

import preconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def if_exists_multiple_enterprises_share_card():
        """选择团队联系人时存在多个团队时返回获取当前团队名，再分享名片"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            cdp = ContactDetailsPage()
            cp = ContactsPage()
            shc.click_back()
            time.sleep(1)
            # scg.wait_for_page_load()
            scg.click_back()
            time.sleep(1)
            # cdp.wait_for_page_load()
            cdp.click_back_icon()
            time.sleep(1)
            # cp.wait_for_page_load()
            cdp.click_back_by_android()
            time.sleep(1)
            cp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_contacts_page()
            cp.wait_for_page_load()
            card_name = "名片消息测试"
            cp.click_tel_contacts_631()
            time.sleep(1)
            cp.select_contacts_by_name(card_name)
            cdp.wait_for_page_load()
            cdp.click_share_business_card()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)

    @staticmethod
    def if_exists_multiple_enterprises_send_card(name):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入单聊发送名片"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            slc = SelectLocalContactsPage()
            scp = SingleChatPage()
            wbp = WorkbenchPage()
            shc.click_back()
            slc.wait_for_page_load()
            slc.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            Preconditions.enter_single_chat_page(name)
            scp.click_more()
            time.sleep(1)
            scp.click_profile()
            slc.wait_for_page_load()
            slc.click_text("选择团队联系人")
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def get_into_enterprise_group_chat_page():
        """进入企业群聊天会话页面 返回群名"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个企业群
        name = sog.select_one_enterprise_group()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        return name

    @staticmethod
    def enter_label_grouping_chat_page():
        """进入标签分组会话页面"""

        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()
        label_grouping = LabelGroupingPage()
        label_grouping.wait_for_page_load()
        # 不存在标签分组则创建
        group_name = Preconditions.get_label_grouping_name()
        group_names = label_grouping.get_label_grouping_names()
        time.sleep(1)
        if not group_names:
            label_grouping.click_new_create_group()
            label_grouping.wait_for_create_label_grouping_page_load()
            label_grouping.input_label_grouping_name(group_name)
            label_grouping.click_sure()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
            label_grouping.wait_for_page_load()
            label_grouping.select_group(group_name)
        else:
            # 选择一个标签分组
            label_grouping.select_group(group_names[0])
        lgdp = LableGroupDetailPage()
        time.sleep(1)
        # 标签分组成员小于2人，需要添加成员
        members_name = lgdp.get_members_names()
        if lgdp.is_text_present("该标签分组内暂无成员") or len(members_name) < 2:
            lgdp.click_add_members()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
        # 点击群发信息
        lgdp.click_send_group_info()
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()

    @staticmethod
    def get_label_grouping_name():
        """获取标签分组群名"""

        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "alg" + phone_number[-4:]
        return group_name

    @staticmethod
    def delete_record_group_chat():
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # if not gcsp.is_toast_exist("聊天记录清除成功"):
            #     raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e


class MessageScanTest(TestCase):
    """消息 - 扫一扫"""

    @classmethod
    def setUpClass(cls):
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 2:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                for name, number in required_contacts:
                    conts.open_contacts_page()
                    if conts.is_text_present("显示"):
                        conts.click_text("不显示")
                    conts.create_contacts_if_not_exits_new(name, number)
                # 创建群
                # required_group_chats = dataproviders.get_preset_group_chats()
                #
                # conts.open_group_chat_list()
                # group_list = GroupListPage()
                # for group_name, members in required_group_chats:
                #     group_list.wait_for_page_load()
                #     group_list.create_group_chats_if_not_exits(group_name, members)
                # group_list.click_back()
                # conts.open_message_page()
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    def default_setUp(self):
        pass

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_A_0014(self):
        """网络异常使用扫一扫"""
        message_page = MessagePage()
        message_page.click_add_icon()
        message_page.click_take_a_scan()
        time.sleep(8)

        scan_page = Scan1Page()
        # scan_page.wait_for_page_load()
        scan_page.assert_network_disconnect_img_is_display()

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0014():
        """
        1.网络异常
        2.已登录客户端
        3.当前在消息列表界面
        4.使用扫一扫功能
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        current_mobile().set_network_status(0)
        current_mobile().activate_app()

    @staticmethod
    def tearDown_test_msg_xiaoliping_A_0014():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().set_network_status(6)
        scan_page = Scan1Page()
        scan_page.click_back()
        current_mobile().activate_app()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_A_0026(self):
        """进入我的二维码页面"""
        message_page = MessagePage()
        message_page.click_add_icon()
        message_page.click_take_a_scan()

        scan_page = ScanPage()
        scan_page.wait_for_page_load()
        time.sleep(2)
        scan_page.open_my_qr_code_page()
        time.sleep(2)

        qr_code_page = MyQRCodePage()
        qr_code_page.wait_for_loading_animation_end()

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0026():
        """
        1.网络正常
        2.已登录客户端
        3.当前在消息列表界面
        4.使用扫一扫功能
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @staticmethod
    def tearDown_test_msg_xiaoliping_A_0026():
        qr_code_page = MyQRCodePage()
        qr_code_page.click_back()
        scan_page = ScanPage()
        scan_page.click_back()

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0008():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        current_mobile().activate_app()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_A_0008(self):
        """扫描普通群无效二维码，分享二维码的人已离开该群"""
        # 1、进入消息列表标题栏“+”
        # 2、点击扫一扫
        # 3、扫描群聊二维码
        message_page = MessagePage()
        message_page.click_add_icon()
        time.sleep(3)
        message_page.click_take_a_scan()
        time.sleep(3)
        message_page.click_back_by_android()
        message_page.wait_for_page_load()


class MessageSearchTest(TestCase):
    """消息-全局搜索"""
    @classmethod
    def setUpClass(cls):
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                conts.open_contacts_page()
                if conts.is_text_present("发现SIM卡联系人"):
                    conts.click_text("显示")
                for name, number in required_contacts:
                    conts.create_contacts_if_not_exits_new(name, number)

                # 创建群
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                return
            except:
                fail_time += 1

    def default_setUp(self):
        """确保每个用例运行前在通讯录页面"""
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', "CMCC1")
    def test_msg_huangcaizui_E_0001(self):
        """消息-消息列表界面搜索框显示"""
        message = MessagePage()
        message.assert_search_box_is_display(8)

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0001():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['IOS-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0002(self):
        """搜索框正常弹起和收起"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        search_page.assert_keyboard_is_display(5)
        search_page.hide_keyboard()
        search_page.assert_keyboard_is_hided()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0002():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0003(self):
        """搜索联系人"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '茻'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 联系人数量
        contact_count = 0
        # 群聊数量
        group_chat_count = 0
        # 聊天记录数量
        chat_count = 0
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if category == 0:
                if now_go_to == '联系人':
                    contact_count += 1
                elif now_go_to == '群聊':
                    group_chat_count += 1
                elif now_go_to == '聊天记录':
                    chat_count += 1
                else:
                    pass
        self.assertGreater(contact_count, 0, '检查点：搜索匹配到的全部有关“{}”的联系'.format(search_key))
        self.assertEqual(chat_count, 0, '检查点：聊天记录为空')
        self.assertEqual(group_chat_count, 0, '检查点：群聊为空')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0003():
        """
        1、联网正常
        2、首次登录客户端，没有群聊和聊天记录
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0004(self):
        """搜索关键字-精准搜索"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '给个红包'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 联系人数量
        contact_count = 0
        # 群聊数量
        group_chat_count = 0
        # 聊天记录数量
        chat_count = 0
        # 列表顺序【联系人】-【群聊】-【聊天记录】板块顺序
        order_map = {
            '联系人': 1,
            '群聊': 2,
            '聊天记录': 3,
            '公众号': 4,
        }
        value_map = {
            1: '联系人',
            2: '群聊',
            3: '聊天记录',
            4: '公众号',
        }
        list_order = []
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
                list_order.append(order_map.get(category))
                # if category in ['联系人', '群聊', '聊天记录']:
                #     list_order.append(category)
            if category == 0:
                if now_go_to == '联系人':
                    contact_count += 1
                elif now_go_to == '群聊':
                    group_chat_count += 1
                elif now_go_to == '聊天记录':
                    chat_count += 1
                else:
                    pass
        self.assertLessEqual(contact_count, 3, '检查点：联系人版块各显示不超过三条')
        self.assertLessEqual(chat_count, 3, '检查点：聊天记录版块各显示不超过三条')
        self.assertLessEqual(group_chat_count, 3, '检查点：群聊版块各显示不超过三条')

        sorted_order = list_order.copy()
        sorted_order.sort()
        self.assertEqual(list_order, sorted_order, '排序"{}"'.format([value_map[i] for i in list_order]))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0004():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0005(self):
        """会话窗口点击后退"""
        # 消息-点击搜索框
        message_page = MessagePage()
        message_page.click_search()
        # 输入关键字进行搜索
        search_page = SearchPage()
        search_key = "给个红包1"
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard()
        # 选择联系人
        contact_search = ContactListSearchPage()
        contact_search.click_contact(search_key)
        # 详情页-点击消息
        detail_page = ContactDetailsPage()
        detail_page.wait_for_page_load()
        detail_page.click_message_icon()
        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        # 检查搜索关键字
        search_page.wait_for_page_load()
        search_page.assert_current_search_keyword_is(search_key)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0006(self):
        """搜索关键字-精准搜索"""
        # 消息页
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = "给个红包1"
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        search_page.assert_current_search_keyword_is(search_key)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0007(self):
        """搜索关键字-中文模糊搜索"""
        contact_name = '给个红包1'
        message_content = '巴适得板'
        message_page = MessagePage()
        message_page.click_search()
        # 查询联系人后，选择联系人
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(contact_name)
        contact_search.hide_keyboard()
        time.sleep(3)
        contact_search.click_contact(contact_name)
        time.sleep(2)
        # 进入"消息"
        detail_page = ContactDetailsPage()
        detail_page.click_message_icon()
        time.sleep(2)
        # 进入聊天界面，发送消息
        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        chat.send_message(message_content)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        contact_search.input_search_keyword("巴适得")
        contact_search.hide_keyboard()
        time.sleep(3)
        exsit = contact_search.is_text_present("巴适得板") or contact_search.is_text_present("相关聊天记录")
        self.assertEqual(exsit, True)

    def setUp_test_msg_huangcaizui_E_0008(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()
        # 创建联系人
        self.contact_name = '给个红包1'
        self.search_keyword = 'abcDEFghijklmnopqrstuvwxyz'
        self.message_content = '其他字符' + self.search_keyword + '其他字符'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_contact(uid)
                detail_page.click_message_icon()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(self.message_content)
                chat.click_back_by_android()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0008(self):
        """搜索关键字-英文模糊搜索"""
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()
        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        # 用消息内容作为关键字搜索
        search_key = self.search_keyword.lower()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to == '联系人' and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    def setUp_test_msg_huangcaizui_E_0009(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.search_keyword = '1234567890'
        self.message_content = '其他字符' + self.search_keyword + '其他字符'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_contact(uid)
                detail_page.click_message_icon()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(self.message_content)
                chat.click_back_by_android()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0009(self):
        """搜索关键字-数字模糊搜索"""
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = self.search_keyword
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['联系人', '群聊', '聊天记录', '公众号'] and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    def setUp_test_msg_huangcaizui_E_0010(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.search_keyword = '#@￥%'
        self.message_content = '其他字符' + self.search_keyword + '其他字符'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_contact(uid)
                detail_page.click_message_icon()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(self.message_content)
                chat.click_back_by_android()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0010(self):
        """搜索关键字-特殊字符模糊搜索"""

        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = self.search_keyword
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['联系人', '群聊', '聊天记录', '公众号'] and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0011(self):
        """搜索不存在的关键字"""
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        time.sleep(2)
        message_page.scroll_to_top()
        time.sleep(2)
        message_page.click_search()
        time.sleep(2)

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = '奇货可居'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        time.sleep(3)
        # 检查无结果提示是否显示
        result = search_page.is_text_present("无搜索结果")
        self.assertTrue(result)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0012(self):
        """搜索聊天记录版块不存在的关键字"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        contact_results = search_page.get_contact_count()
        self.assertEqual(contact_results, 3, '搜索结果中，联系人数量不正确')
        time.sleep(2)
        scp = SelectContactsPage()
        scp.page_up()
        time.sleep(2)
        group_chat_results = search_page.get_group_count()
        self.assertEqual(group_chat_results, 3, '搜索结果中，群聊数量不正确')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0012():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = [key_message + '1', key_message + '2', key_message + '3', key_message + '4']
        for group_name in groups:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))

        group_list.click_back()

        # 创建联系人
        names = [key_message + '1', key_message + '2', key_message + '3', key_message + '4']
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(names))

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0013(self):
        """搜索群聊版块不存在的关键字"""
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        # contact_results = []
        # chat_history = []
        # for result in search_page.search_list_iterator():
        #     category = search_page.determine_list_item_type(result)
        #     if category in ['联系人', '群聊', '聊天记录', '公众号']:
        #         self.assertNotEqual(category, '群聊', '检查点："群聊"板块不展示')
        #         now_go_to = category
        #     if now_go_to in ['联系人'] and category == 0:
        #         # 检查搜索结果是否包含关键字
        #         contact_results.append(result)
        #     if now_go_to in ['聊天记录'] and category == 0:
        #         # 检查搜索结果是否包含关键字
        #         chat_history.append(result)
        time.sleep(1)
        contact_results = search_page.get_contact_count()
        self.assertEqual(contact_results, 3, '检查点：联系人最多显示3条')
        search_page.page_down()
        time.sleep(3)
        chat_history = search_page.get_chat_history_count()
        self.assertEqual(chat_history, 3, '检查点：聊天记录最多显示3条')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0013():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = ['群聊1', '群聊2', '群聊3', '群聊4']
        for group_name in groups:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                time.sleep(1)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back_by_android()
                time.sleep(2)
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))

        group_list.click_back()

        # 创建联系人
        names = [key_message + '1', key_message + '2', key_message + '3', key_message + '4']
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(names))

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0014(self):
        """搜索联系人排序"""
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        time.sleep(2)
        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
            time.sleep(1)
        results = search_page.get_meslist_contacts()
        flag = search_page.is_contains_element(results, "大佬2")
        self.assertEqual(flag, True, '检查点：搜索结果中联系人版块排序是：最近生成消息的联系人')
        flag = search_page.is_contains_element(results, "大佬1")
        self.assertEqual(flag, True, '检查点：聊天记录最多显示3条')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0014():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()
        # 创建联系人
        names = [key_message + '1', key_message + '2']
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_contact(uid)
                detail_page.click_message_icon()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message('新消息')
                chat.click_back_by_android()
                time.sleep(2)
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(names))

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0015(self):
        """搜索群聊排序"""

        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        time.sleep(1)
        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        # search_key = '群聊'
        # search_page.input_search_keyword(search_key)
        # search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        # results = []
        # for result in search_page.search_list_iterator():
        #     category = search_page.determine_list_item_type(result)
        #     if category in ['联系人', '群聊', '聊天记录', '公众号']:
        #         now_go_to = category
        #     if now_go_to in ['群聊'] and category == 0:
        #         # 检查搜索结果是否包含关键字
        #         name = search_page.get_contact_name(result)
        #         results.append(name)
        results = search_page.get_meslist_contacts()
        flag = search_page.is_contains_element(results,"群聊2")
        self.assertEqual(flag, True, '检查点：搜索结果中群聊排序是：最近生成消息的群聊（按时间排序）')
        flag = search_page.is_contains_element(results, "群聊1")
        self.assertEqual(flag, True, '检查点：搜索结果中群聊排序是：最近生成消息的群聊（按时间排序）')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0015():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = ['群聊1', '群聊2']
        for group_name in groups:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back_by_android()
                time.sleep(2)
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))
        group_list.click_back()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0016(self):
        """搜索聊天记录排序"""
        key_message = '新消息'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.set_top_for_message('群聊1')
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                results.append(name)
        self.assertEqual('群聊2', results[0], '检查点：搜索结果中聊天记录排序是： 按时间排序')
        self.assertEqual('群聊1', results[1], '检查点：搜索结果中聊天记录排序是： 按时间排序')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0016():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        key_message = '新消息'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = ['群聊1', '群聊2']
        for group_name in groups:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back_by_android()
                time.sleep(2)
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))
        group_list.click_back()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0017(self):
        """查看更多联系人"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        # results = []
        # for result in search_page.search_list_iterator():
        #     category = search_page.determine_list_item_type(result)
        #     if category in ['联系人', '群聊', '聊天记录', '公众号']:
        #         now_go_to = category
        #     if now_go_to in ['联系人'] and category == 0:
        #         # 检查搜索结果是否包含关键字
        #         name = search_page.get_contact_name(result)
        #         self.assertIn(search_key, name)
        #         results.append(name)
        results = search_page.get_contact_count()
        self.assertEqual(3, results, '检查点：搜索结果显示相应匹配的联系人信息')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '手机联系人':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        time.sleep(2)
        search_page.click_show_more(searching)

        show_more = GlobalSearchContactPage()
        try:
            time.sleep(4)
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0018(self):
        """清空搜索条件"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        search_page.input_search_keyword('关键字')
        search_page.click_clear_keyword_button()
        # 检查点: 置灰语：搜索
        search_page.assert_current_search_keyword_is('输入关键词快速搜索')
        search_page.click_back_button()
        message_page.assert_search_box_text_is('搜索')

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0019(self):
        """更改搜索关键字"""
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = '测试'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 更换关键字
        search_key = '给个红包'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示

        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0020(self):
        """查看更多群聊"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['手机联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['群聊'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                search_page.assert_search_result_match_keyword(result, search_key)
                self.assertIn(search_key, name)
                results.append(name)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关匹配的群聊名称；')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '群聊':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)

        show_more = GlobalSearchGroupPage()
        try:
            time.sleep(2)
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0021(self):
        """查看更多群聊"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['手机联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['群聊'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                search_page.assert_search_result_match_keyword(result, search_key)
                self.assertIn(search_key, name)
                results.append(name)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关匹配的群聊名称；')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '群聊':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)

        show_more = GlobalSearchGroupPage()
        try:
            time.sleep(3)
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')
        # show_more.clear_search_keyword()
        search_key = key_message + '1'
        show_more.search2(search_key)
        show_more.hide_keyboard_if_display()
        # show_more.assert_list_contains_group(search_key)
        search_page.is_exist__contact_name(search_key)

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0022(self):
        """查看更多聊天记录"""
        key_message = '聊'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, search_key)
                results.append(result)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关聊天记录的联系人名称或群聊名称')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '聊天记录':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)
        show_more = GlobalSearchMessagePage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0022():
        """
        1、联网正常
        2、已登录客户端
        3、当前群聊搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.click_contacts()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1', group_name + '2', group_name + '3', group_name + '4']
        for group_name in group_names:
            chat_message = '聊天记录搜索测试{}'.format(group_names.index(group_name))
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(chat_message)
                chat.click_back_by_android()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))
        group_list.click_back()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0023(self):
        """查看更多聊天记录"""
        key_message = '聊'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, search_key)
                results.append(result)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关聊天记录的联系人名称或群聊名称')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '聊天记录':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)
        show_more = GlobalSearchMessagePage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')
        show_more.clear_search_keyword()
        search_key = '聊天记录搜索测试' + '1'
        show_more.search(search_key)
        show_more.hide_keyboard_if_display()
        show_more.assert_list_contains_message(search_key)

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0023():
        """
        1、联网正常
        2、已登录客户端
        3、当前群聊搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1', group_name + '2', group_name + '3', group_name + '4']
        for group_name in group_names:
            chat_message = '聊天记录搜索测试{}'.format(group_names.index(group_name))
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(chat_message)
                chat.click_back_by_android()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0024(self):
        """查看更多聊天记录"""
        key_message = '测试相同聊天记录大于一条'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, "2条相关聊天记录")
                results.append(result)
        self.assertEqual(1, len(results), '检查点：搜索结果显示相关聊天记录的联系人名称或群聊名称')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0024():
        """
        1、联网正常
        2、已登录客户端
        3、当前聊天页面搜索页面
        4、同一个群或联系人有多条相同的聊天记录
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1']
        for group_name in group_names:
            chat_message = '测试相同聊天记录大于一条'
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                # 发第一次
                chat.send_message(chat_message)
                # 发第二次
                chat.send_message(chat_message)
                chat.click_back_by_android()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0025(self):
        """查看更多聊天记录"""
        key_message = '测试相同聊天记录大于一条'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, "2条相关聊天记录")
                result.click()

        message_search = MessageSearchPage()
        message_search.wait_for_page_load()
        message_search.assert_list_data_match_statistic_bar()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0025():
        """
        1、联网正常
        2、已登录客户端
        3、当前聊天页面搜索页面
        4、同一个群或联系人有多条相同的聊天记录
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1']
        for group_name in group_names:
            chat_message = '测试相同聊天记录大于一条'
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                # 发第一次
                chat.send_message(chat_message)
                # 发第二次
                chat.send_message(chat_message)
                chat.click_back_by_android()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0026(self):
        """网络异常全局搜索"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '给个红包'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 联系人数量
        contact_count = 0
        # 群聊数量
        group_chat_count = 0
        # 聊天记录数量
        chat_count = 0
        # 列表顺序【联系人】-【群聊】-【聊天记录】板块顺序
        order_map = {
            '联系人': 1,
            '群聊': 2,
            '聊天记录': 3,
            '公众号': 4,
        }
        value_map = {
            1: '联系人',
            2: '群聊',
            3: '聊天记录',
            4: '公众号',
        }
        list_order = []
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
                list_order.append(order_map.get(category))
            if category == 0:
                if now_go_to == '联系人':
                    contact_count += 1
                elif now_go_to == '群聊':
                    group_chat_count += 1
                elif now_go_to == '聊天记录':
                    chat_count += 1
                else:
                    pass
        self.assertLessEqual(contact_count, 3, '匹配到有关“{}”的联系人信息'.format(search_key))
        self.assertLessEqual(chat_count, 3, '聊天记录不为空')
        self.assertLessEqual(group_chat_count, 3, '群聊记录群聊记录不为空')

        sorted_order = list_order.copy()
        sorted_order.sort()
        self.assertEqual(list_order, sorted_order, '排序"{}"'.format([value_map[i] for i in list_order]))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0026():
        """
        1、网络异常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        current_mobile().set_network_status(0)
        current_mobile().activate_app()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0026():
        current_mobile().set_network_status(6)
        current_mobile().activate_app()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC-EMAIL")
    def test_msg_huangcaizui_E_0027(self):
        """搜索关键字"""
        key_message = '1'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 正确的顺序
        expected_order = ['搜索和通讯录联系人', '联系人', '群聊', '功能', '聊天记录', '公众号']
        # 实际顺序
        actual_order = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category != 0:
                if category == 1:
                    category = '搜索和通讯录联系人'
                actual_order.append(category)
        self.assertEqual(
            expected_order,
            actual_order,
            "检查点：排序规则为：搜索和通讯录联系人>本地联系人>群聊>功能>聊天记录>公众号"
        )

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0027():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面

        测试方案：
            1.号码有1的联系人：不用在这里创建，前面的用例已经导入包含“1”的号码
            2.名称有1的群聊：使用“群聊1”
            3.内容有1的聊天记录：群聊1中发送消息“1”
            4.名字包含“1”的功能：发送邮件到登录号码的139邮箱触发“139邮箱助手”
            5.名字包含“1”的公众号：不需要制造，中国移动10886
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        login_num = preconditions.make_already_in_message_page(reset_required=True)

        # 先发邮件，否则无法搜索到功能“139邮箱”
        from library.core.utils.email_helper import send_email
        send_email(login_num + '@139.com', '工作日报终稿', '更新内容！')
        # 关键字交集使用“1”
        key_message = '1'
        # 消息页
        message_page = MessagePage()
        message_page.find_message('139邮箱助手', 40)
        # 创建名称为"助手"的群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        # 群聊名测试数据使用“群聊1”
        group_names = ['群聊' + key_message]
        for group_name in group_names:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                # 制造包含关键字的聊天记录
                chat.send_message(key_message)
                chat.click_back_by_android()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()


class MessageOthersAllTest(TestCase):
    """模块：消息"""
    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 2:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                conts.open_contacts_page()
                if conts.is_text_present("发现SIM卡联系人"):
                    conts.click_text("显示")
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits_new(name, number)
                # 创建名片消息联系人
                conts.create_contacts_if_not_exits2("名片消息测试", "13500135001", "中软国际", "经理", "123456@139.com")
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 2:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 2:
            try:
                Preconditions.make_already_in_message_page()
                Preconditions.ensure_have_enterprise_group()
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

    def default_setUp(self):
        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0176(self):
        """名片消息"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        cp.select_contacts_by_name("名片消息测试")
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("大佬1")
        time.sleep(2)
        slc.click_text("发送名片")
        # 1.正常分享
        self.assertEquals(slc.is_toast_exist("已发送"), True)
        cdp.click_back_icon()
        time.sleep(1)
        cdp.click_back_by_android()
        cp.wait_for_page_load()
        cp.open_message_page()
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0177(self):
        """名片消息"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 清空收藏列表确保不影响验证
        mp.open_me_page()
        me_page = MePage()
        mcp = MeCollectionPage()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp.wait_for_page_load()
        mcp.clear_collection_list()
        mcp.click_back()
        me_page.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        share_name = "大佬1"
        slc.selecting_local_contacts_by_name(share_name)
        time.sleep(2)
        slc.click_text("发送名片")
        cdp.click_back_icon()
        time.sleep(1)
        cdp.click_back_by_android()
        cp.wait_for_page_load()
        cp.open_message_page()
        mp.wait_for_page_load()
        # 选择刚刚发送的名片消息收藏
        mp.choose_chat_by_name(share_name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        scp = SingleChatPage()
        scp.press_card_name_by_number(-1)
        scp.click_text("收藏")
        self.assertEquals(scp.is_toast_exist("已收藏"), True)
        scp.click_back()
        mp.wait_for_page_load()
        mp.open_me_page()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp.wait_for_page_load()
        # 1.功能及文案全部正常
        self.assertEquals(mcp.is_exists_card_by_name(card_name), True)
        mcp.click_back()
        me_page.wait_for_page_load()
        me_page.open_message_page()
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0179(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——名称搜索"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给团队联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_share_card()
        # 输入搜索名称
        search_name = "大佬1"
        shc.input_search(search_name)
        shc.selecting_he_contacts_by_name(search_name)
        time.sleep(2)
        # 1.左上角“X”按钮关闭弹窗、和飞信头像、企业下昵称、电话号码、企业-部门、职位/多个职位、邮箱
        self.assertEquals(cdp.is_exists_share_card_close_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_head_img(), True)
        self.assertEquals(cdp.is_exists_share_card_name(), True)
        self.assertEquals(cdp.is_exists_share_card_number(), True)
        self.assertEquals(cdp.is_exists_share_card_company(), True)
        self.assertEquals(cdp.is_exists_share_card_position(), True)
        self.assertEquals(cdp.is_exists_share_card_email(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0180(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——名称搜索"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给手机联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 输入搜索名称
        search_name = "大佬2"
        slc.input_search_keyword(search_name)
        time.sleep(2)
        slc.selecting_local_contacts_by_name(search_name)
        time.sleep(2)
        # 1.左上角“X”按钮关闭弹窗、和飞信头像、企业下昵称、电话号码、企业-部门、职位/多个职位、邮箱
        self.assertEquals(cdp.is_exists_share_card_close_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_head_img(), True)
        self.assertEquals(cdp.is_exists_share_card_name(), True)
        self.assertEquals(cdp.is_exists_share_card_number(), True)
        self.assertEquals(cdp.is_exists_share_card_company(), True)
        self.assertEquals(cdp.is_exists_share_card_position(), True)
        self.assertEquals(cdp.is_exists_share_card_email(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0181(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——号码搜索"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给团队联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_share_card()
        # 输入搜索号码
        search_number = "13800138005"
        shc.input_search(search_number)
        shc.selecting_he_contacts_by_number(search_number)
        time.sleep(2)
        # 1.左上角“X”按钮关闭弹窗、和飞信头像、企业下昵称、电话号码、企业-部门、职位/多个职位、邮箱
        self.assertEquals(cdp.is_exists_share_card_close_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_head_img(), True)
        self.assertEquals(cdp.is_exists_share_card_name(), True)
        self.assertEquals(cdp.is_exists_share_card_number(), True)
        self.assertEquals(cdp.is_exists_share_card_company(), True)
        self.assertEquals(cdp.is_exists_share_card_position(), True)
        self.assertEquals(cdp.is_exists_share_card_email(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0182(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——号码搜索"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给手机联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 输入搜索号码
        search_number = "13800138006"
        slc.input_search_keyword(search_number)
        time.sleep(2)
        slc.selecting_local_contacts_by_number(search_number)
        time.sleep(2)
        # 1.左上角“X”按钮关闭弹窗、和飞信头像、企业下昵称、电话号码、企业-部门、职位/多个职位、邮箱
        self.assertEquals(cdp.is_exists_share_card_close_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_head_img(), True)
        self.assertEquals(cdp.is_exists_share_card_name(), True)
        self.assertEquals(cdp.is_exists_share_card_number(), True)
        self.assertEquals(cdp.is_exists_share_card_company(), True)
        self.assertEquals(cdp.is_exists_share_card_position(), True)
        self.assertEquals(cdp.is_exists_share_card_email(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0183(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——选择和通讯录联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给团队联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_share_card()
        shc.selecting_he_contacts_by_name("大佬3")
        time.sleep(2)
        # 1.左上角“X”按钮关闭弹窗、和飞信头像、企业下昵称、电话号码、企业-部门、职位/多个职位、邮箱
        self.assertEquals(cdp.is_exists_share_card_close_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_head_img(), True)
        self.assertEquals(cdp.is_exists_share_card_name(), True)
        self.assertEquals(cdp.is_exists_share_card_number(), True)
        self.assertEquals(cdp.is_exists_share_card_company(), True)
        self.assertEquals(cdp.is_exists_share_card_position(), True)
        self.assertEquals(cdp.is_exists_share_card_email(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0184(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——选择本地联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        time.sleep(1)
        # 选择名片
        card_name = "名片消息测试"
        cp.select_contacts_by_name(card_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 发送名片消息给手机联系人
        cdp.click_share_business_card()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("大佬4")
        time.sleep(2)
        # 1.左上角“X”按钮关闭弹窗、和飞信头像、企业下昵称、电话号码、企业-部门、职位/多个职位、邮箱
        self.assertEquals(cdp.is_exists_share_card_close_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_head_img(), True)
        self.assertEquals(cdp.is_exists_share_card_name(), True)
        self.assertEquals(cdp.is_exists_share_card_number(), True)
        self.assertEquals(cdp.is_exists_share_card_company(), True)
        self.assertEquals(cdp.is_exists_share_card_position(), True)
        self.assertEquals(cdp.is_exists_share_card_email(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0190(self):
        """名片消息——单聊——发出名片后--消息界面——点击查看"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入单聊会话页面
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        # 发送名片消息
        scp = SingleChatPage()
        scp.click_more()
        time.sleep(1)
        scp.click_profile()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.click_text("选择团队联系人")
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_send_card(name)
        shc.selecting_he_contacts_by_name("郑海")
        time.sleep(2)
        slc.click_text("发送名片")
        scp.wait_for_page_load()
        scp.click_card_name_by_number(-1)
        time.sleep(1)
        self.assertEquals(scp.is_text_present("保存到通讯录"), True)
        scp.click_back_by_android(2)
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0191(self):
        """名片消息——单聊——发出名片后--消息界面——长按"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入单聊会话页面
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        # 发送名片消息给单聊
        scp = SingleChatPage()
        scp.click_more()
        time.sleep(1)
        scp.click_profile()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        scp.wait_for_page_load()
        # 转发名片消息到我的电脑
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.input_search_keyword("我的电脑")
        time.sleep(2)
        slc.selecting_local_contacts_by_name("我的电脑")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 转发名片消息到单聊
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("大佬2")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 转发名片消息到普通群
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.selecting_one_group_by_name("群聊1")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 转发名片消息到企业群
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.select_one_enterprise_group()
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        scp.click_back()
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0202(self):
        """名片消息——场景"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入单聊会话页面
        Preconditions.enter_single_chat_page("大佬1")
        # 发送名片消息给单聊
        scp = SingleChatPage()
        scp.click_more()
        time.sleep(1)
        scp.click_profile()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        # 1.功能及文案全部正常
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        slc.click_back_by_android()
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0203(self):
        """名片消息——场景"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入普通群会话页面
        Preconditions.get_into_group_chat_page("群聊1")
        Preconditions.delete_record_group_chat()
        time.sleep(1)
        # 发送名片消息给普通群
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        # gcp.click_profile()
        gcp.click_text("名片")
        time.sleep(1)
        slc = SelectLocalContactsPage()
        # slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        # 1.功能及文案全部正常
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        slc.click_back_by_android()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0204(self):
        """名片消息——场景"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入企业群会话页面
        Preconditions.get_into_enterprise_group_chat_page()
        Preconditions.delete_record_group_chat()
        # 发送名片消息给企业群
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        # gcp.click_profile()
        gcp.click_text("名片")
        time.sleep(1)
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        # 1.功能及文案全部正常
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        slc.click_back_by_android()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0205(self):
        """名片消息——场景"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入标签分组会话页面
        Preconditions.enter_label_grouping_chat_page()
        # Preconditions.delete_record_group_chat()
        # 发送名片消息给标签分组
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        sc = SingleChatPage()
        sc.click_profile()
        time.sleep(1)
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        # 1.功能及文案全部正常
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        slc.click_back_by_android(4)
        mp.open_message_page()
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0206(self):
        """名片消息——场景"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入我的电脑会话页面
        mp.click_search()
        sp = SearchPage()
        sp.input_search_keyword('我的电脑')
        time.sleep(1)
        mp.choose_chat_by_name('我的电脑')
        time.sleep(1)
        # 发送名片消息给我的电脑
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        sc = SingleChatPage()
        sc.click_profile()
        time.sleep(1)
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        # 1.功能及文案全部正常
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        slc.click_back_by_android(2)
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0212(self):
        """网页消息——发出网页消息消息界面——长按"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入会话页面发送网页消息
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.input_text_message("www.otherpages.com")
        gcp.send_text()
        # 转发网页消息到我的电脑
        gcp.press_message_text_by_number(-1)
        gcp.click_text("转发")
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.input_search_keyword("我的电脑")
        time.sleep(2)
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("我的电脑")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 转发网页消息到单聊
        gcp.press_message_text_by_number(-1)
        gcp.click_text("转发")
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("大佬1")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 转发网页消息到普通群
        gcp.press_message_text_by_number(-1)
        gcp.click_text("转发")
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.selecting_one_group_by_name("群聊2")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 转发网页消息到企业群
        gcp.press_message_text_by_number(-1)
        gcp.click_text("转发")
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.select_one_enterprise_group()
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0213(self):
        """网页消息——发出网页消息消息界面——长按"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 清空收藏列表确保不影响验证
        mp.open_me_page()
        me_page = MePage()
        mcp = MeCollectionPage()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp.wait_for_page_load()
        mcp.clear_collection_list()
        mcp.click_back()
        me_page.wait_for_page_load()
        me_page.open_message_page()
        mp.wait_for_page_load()
        # 进入会话页面
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 获取当前群名片名称
        my_group_name = gcs.get_my_group_name()
        gcs.click_back()
        gcp.wait_for_page_load()
        # 发送网页消息
        text = "www.baidu.com"
        gcp.input_text_message(text)
        gcp.send_text()
        gcp.press_message_text_by_number(-1)
        gcp.click_text("收藏")
        self.assertEquals(gcp.is_toast_exist("已收藏"), True)
        gcp.click_back()
        mp.wait_for_page_load()
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 1.收藏内容来源显示为消息发送者名称
        self.assertEquals(mcp.is_exists_text_message_by_name(text), True)
        self.assertEquals(mcp.is_text_present(my_group_name), True)
        mcp.click_back()
        me_page.wait_for_page_load()
        me_page.open_message_page()
        # 等待消息页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0214(self):
        """网页消息——发出网页消息消息界面——长按"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入会话页面
        Preconditions.get_into_group_chat_page("群聊3")
        time.sleep(2)
        # 发送网页消息
        text = "www.baidu.com"
        gcp = GroupChatPage()
        gcp.input_text_message(text)
        gcp.hide_keyboard()
        time.sleep(2)
        gcp.send_text()
        time.sleep(3)
        gcp.press_message_text_by_number(-1)
        time.sleep(2)
        self.assertEquals(gcp.is_text_present("撤回"), True)
        time.sleep(1)
        gcp.click_back_by_android()
        count = 0
        while count < 610:
            time.sleep(1)
            count += 1
        time.sleep(3)
        gcp.press_message_text_by_number(-1)
        time.sleep(2)
        # 1.超过10分钟隐藏按钮
        self.assertEquals(gcp.is_text_present("撤回"), False)
        gcp.click_back_by_android(3)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0215(self):
        """网页消息——发出网页消息消息界面——长按"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入会话页面
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 清空聊天记录确保不影响验证
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_clear_chat_record()
        time.sleep(1)
        gcs.click_sure()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()
        # 发送网页消息
        text = "www.baidu.com"
        gcp.input_text_message(text)
        gcp.send_text()
        gcp.press_message_text_by_number(-1)
        gcp.click_text("删除")
        time.sleep(2)
        # 1.正常删除
        self.assertEquals(gcp.is_exists_message_by_text(text), False)

    @tags('ALL', 'CMCC', 'LXD', "lxd_debug")
    def test_msg_hanjiabin_0216(self):
        """网页消息——发出网页消息消息界面——长按"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 进入单聊会话页面
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        # 发送名片消息给单聊
        scp = SingleChatPage()
        scp.click_more()
        time.sleep(1)
        scp.click_profile()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("名片消息测试")
        time.sleep(2)
        slc.click_text("发送名片")
        scp.wait_for_page_load()
        # 转发名片消息到我的电脑
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.input_search_keyword("我的电脑")
        time.sleep(2)
        slc.selecting_local_contacts_by_name("我的电脑")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 转发名片消息到单聊
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("大佬2")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 转发名片消息到普通群
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.selecting_one_group_by_name("群聊1")
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 转发名片消息到企业群
        scp.press_card_name_by_number(-1)
        scp.click_text("转发")
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.select_one_enterprise_group()
        scg.click_sure_forward()
        # 是否提示已转发
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        scp.click_back()
        # 等待消息页面加载
        mp.wait_for_page_load()