import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import LoginPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
}


class Preconditions(LoginPreconditions):
    """前置条件"""
    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()


class MsgSelectMoreTest(TestCase):
    """ 消息：查看更多"""
    @classmethod
    def setUpClass(cls):
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.connect_mobile('Android-移动')
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                time.sleep(1)
                mp = MessagePage()
                mp.click_phone_contact()
                time.sleep(1)
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits_new(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)
        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                groupname = "测试企业群2"
                Preconditions.ensure_have_enterprise_group2(groupname)
                Preconditions.make_already_in_message_page()
                groupname = "测试企业群3"
                Preconditions.ensure_have_enterprise_group2(groupname)
                Preconditions.make_already_in_message_page()
                groupname = "测试企业群4"
                Preconditions.ensure_have_enterprise_group2(groupname)
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

    def default_setUp(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL01')
    def test_msg_huangcaizui_E_0017(self):
        """查看更多联系人"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search()
        search_page = SearchPage()
        search_page.input_search_keyword('给个红包')
        time.sleep(3)
        select_contacts = SelectContactsPage()
        select_contacts.hide_keyboard()
        time.sleep(3)
        select_contacts.click_contact_more2()
        time.sleep(3)
        # 判定点
        # 1.搜索结果显示相应匹配的联系人信息
        result = select_contacts.is_text_present("给个红包1")
        self.assertEqual(result, True)
        # 2.跳转到搜索到的所有联系人显示页面
        result = select_contacts.is_text_present("手机联系人")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangcaizui_E_0020(self):
        """查看更多联系人"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search()
        search_page = SearchPage()
        search_page.input_search_keyword('测试企业群')
        time.sleep(3)
        # 判定点
        select_contacts = SelectContactsPage()
        select_contacts.hide_keyboard()
        # 1.搜索结果显示相关匹配的群聊名称；
        result = select_contacts.is_text_present("测试企业群")
        self.assertEquals(result, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0078(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1、点击右上角的+号，发起群聊
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        self.assertEquals(sc.is_text_present("选择联系人"), True)
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        sc.click_select_one_group()
        time.sleep(1)
        self.assertEquals(sc.is_text_present("面对面建群"), False)
        # 3、中文模糊搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("群聊")
        time.sleep(3)
        search_page.hide_keyboard()
        exist = search_page.is_text_present("群聊1")
        self.assertEquals(exist, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0079(self):
        """群搜索-无搜索结果"""
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("群999")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、中文模糊搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0080(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("群聊1")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、中文精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        glsp = GroupListSearchPage()
        exist = glsp.is_group_in_list("群聊1")
        self.assertEquals(exist, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0081(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("群聊20")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、中文精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0082(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("testa")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、英文精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        glsp = GroupListSearchPage()
        exist = glsp.is_group_in_list("testa")
        self.assertEquals(exist, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0083(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("groupa")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、英文精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0084(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint(" ")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、空格精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = search_page.is_text_present("test b")
        self.assertEquals(exist, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0085(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("  ")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、空格精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0086(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("001")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、数字精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = search_page.is_text_present("group001")
        self.assertEquals(exist, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0087(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("999")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、数字精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0088(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("###")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、数字精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = search_page.is_text_present("###001")
        self.assertEquals(exist, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0089(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        time.sleep(1)
        mess.click_group_chat()
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        search_page = SearchPage()
        search_page.click_search_group_hint()
        search_page.input_search_hint("####")
        time.sleep(3)
        search_page.hide_keyboard()
        # 1、数字精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0131(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        time.sleep(1)
        # 联系 tab
        mess.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        # 联系-群聊
        cp.open_group_chat_list()
        time.sleep(1)
        scp = SelectContactsPage()
        scp.click_group_search()
        scp.group_search(text="给个红包1")
        time.sleep(1)
        scp.hide_keyboard()
        scp.select_one_group_by_name2("给个红包1")
        time.sleep(1)
        scp.click_groupchat_setting_icon()
        time.sleep(1)
        # 判定点 1、进入“设置”页面
        exists = scp.is_toast_exist("群聊设置")
        self.assertEquals(exists, True)
        gcsp = GroupChatSetPage()
        # 点击 清空聊天记录
        gcsp.click_clear_chat_record2()
        time.sleep(1)
        scp.click_clear_record_sure()
        # 判定点 2、提示“聊天记录清除成功”
        exists = scp.is_toast_exist("聊天记录清除成功")
        self.assertEquals(exists, True)

    @tags('ALL', 'CMCC', 'MES_OTHER', 'YL')
    def test_msg_huangmianhua_0132(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        time.sleep(1)
        # 联系 tab
        mess.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        # 联系-群聊
        cp.open_group_chat_list()
        time.sleep(1)
        scp = SelectContactsPage()
        scp.click_group_search()
        scp.group_search(text="给个红包1")
        time.sleep(1)
        scp.hide_keyboard()
        scp.select_one_group_by_name2("给个红包1")
        time.sleep(1)
        scp.click_groupchat_setting_icon()
        time.sleep(1)
        # 判定点 1、进入“设置”页面
        exists = scp.is_toast_exist("群聊设置")
        self.assertEquals(exists, True)
        gcsp = GroupChatSetPage()
        # 点击 清空聊天记录
        gcsp.click_clear_chat_record2()
        time.sleep(1)
        # 判定点 2、弹出确认窗口
        exists = scp.is_toast_exist("是否清空聊天记录")
        self.assertEquals(exists, True)

