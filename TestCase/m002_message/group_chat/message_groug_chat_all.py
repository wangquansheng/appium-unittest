import time
import unittest
import warnings

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        time.sleep(1)
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        sog.click_back()
        time.sleep(2)
        sc.click_back()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.click_one_contact(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""
        mp = MessagePage()
        current_mobile().launch_app()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def create_contacts_groups():
        # 创建联系人
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 2:
            try:
                Preconditions.make_already_in_message_page()
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                conts.open_contacts_page()
                if conts.is_text_present("发现SIM卡联系人"):
                    conts.click_text("显示")
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
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break


class MsgAllPrior(TestCase):
    """消息-单聊"""

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.create_contacts_groups()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0605():
        """确保在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0605(self):
        """开启免打扰后，在聊天页面在输入框输入内容-返回到消息列表页时，该消息列表窗口直接展示：草稿"""
        # 1、点击消息免打扰的开关，是否可以打开消息免打扰开关
        Preconditions.enter_group_chat_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        if not switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)
        # 返回到聊天会话页面，页面上方是否会展示免打扰标志
        group_set.click_back()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_message("this is a test message")
        group_chat_page.send_text()
        group_chat_page.input_message("this is a test message")
        group_chat_page.click_back()
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        self.assertTrue(msg_page.wait_until(lambda x: msg_page.is_text_present('草稿')))
        MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page = GroupChatPage()
        group_chat_page.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        if switch_status:
            group_set.click_switch_undisturb()
            time.sleep(1)

    def enter_o2o_message_page(self):
        msg_page = MessagePage()
        msg_page.open_message_page()
        msg_page.click_add_icon()
        msg_page.click_new_message()
        select_contact = SelectContactsPage()
        select_contact.wait_for_create_msg_page_load()
        select_contact.click_one_local_contacts()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0058():
        Flag = True
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page(reset=Flag)

    @unittest.skip('用例需要重置')
    def test_msg_huangcaizui_A_0058(self):
        """新建消息入口首次进入一对一聊天页面是否有弹框出来"""
        self.enter_o2o_message_page()
        self.assertTrue(SingleChatPage().is_exist_dialog(timeout=8))
        SingleChatPage().driver.back()
        SingleChatPage().click_back()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0059():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @unittest.skip('用例需要重置')
    def test_msg_huangcaizui_A_0059(self):
        """观察从新建消息入口出现的弹框页面"""
        self.enter_o2o_message_page()
        single_chat = SingleChatPage()
        self.assertTrue(single_chat.is_exist_dialog(timeout=8))
        self.assertTrue(single_chat.check_element_enabled('我已阅读'))
        self.assertFalse(single_chat.check_element_enabled('确定'))
        single_chat.driver.back()
        single_chat.click_back()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0060():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @unittest.skip('用例需要重置')
    def test_msg_huangcaizui_A_0060(self):
        """验证点选弹框中的“我已阅读”按钮后确定按钮是否会变高亮"""
        self.enter_o2o_message_page()
        single_chat = SingleChatPage()
        self.assertTrue(single_chat.is_exist_dialog(timeout=8))
        self.assertFalse(single_chat.check_element_enabled('确定'))
        single_chat.click_only_i_have_read()
        self.assertTrue(single_chat.check_element_enabled('确定'))
        single_chat.driver.back()
        single_chat.click_back()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0061():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @unittest.skip('用例需要重置')
    def test_msg_huangcaizui_A_0061(self):
        """验证点选弹框中的“我已阅读”按钮后确定按钮是否会变高亮"""
        self.enter_o2o_message_page()
        single_chat = SingleChatPage()
        self.assertTrue(single_chat.is_exist_dialog(timeout=8))
        self.assertFalse(single_chat.check_element_enabled('确定'))
        single_chat.click_only_i_have_read()
        self.assertTrue(single_chat.check_element_enabled('确定'))
        single_chat.click_only_sure_button()
        single_chat.wait_for_page_load()
        self.assertTrue(single_chat.is_on_this_page)
        single_chat.click_back()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0062():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page(reset=True)

    @unittest.skip('用例需要重置')
    def test_msg_huangcaizui_A_0062(self):
        """验证不点击确定，使用手机系统返回，再次进入一对一聊天窗口是否会再次弹出使用须知"""
        self.enter_o2o_message_page()
        single_chat = SingleChatPage()
        self.assertTrue(single_chat.is_exist_dialog(timeout=8))
        self.assertFalse(single_chat.check_element_enabled('确定'))
        single_chat.click_only_i_have_read()
        self.assertTrue(single_chat.check_element_enabled('确定'))
        single_chat.driver.back()
        single_chat.click_back()
        self.enter_o2o_message_page()
        self.assertTrue(single_chat.is_exist_dialog(timeout=8))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0103():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0103(self):
        """页面样式"""
        single_chat_page = SingleChatPage()
        if not single_chat_page.is_open_expression():
            single_chat_page.open_expression()
        time.sleep(2)
        single_chat_page.page_should_contains_element('表情id')
        single_chat_page.page_should_contains_element('翻页小圆点')
        single_chat_page.page_should_contains_element('删除表情按钮')
        single_chat_page.page_should_contains_element('表情集选择栏')
        single_chat_page.page_should_contains_element('关闭表情')  # 键盘
        single_chat_page.close_expression()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0128():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0128(self):
        """进入发送页面"""
        # 1、进入一对一天界面
        single_chat_page = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        single_chat_page.click_sms()
        time.sleep(2)
        if single_chat_page.wait_until(lambda x: single_chat_page.page_should_contain_text("欢迎使用免费短信"), timeout=8,
                                       auto_accept_permission_alert=False):
            single_chat_page.page_should_contain_text("欢迎使用免费短信")
            single_chat_page.page_should_contain_text("免费给移动用户发送短信")
            single_chat_page.page_should_contain_text("给非移动用户发短信将收取0.01元/条")
            single_chat_page.page_should_contain_text("给港澳台等境外用户发短信将收取1元/条")
            single_chat_page.driver.back()
        else:
            single_chat_page.wait_for_page_load()
            self.assertTrue(single_chat_page.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0129():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0129(self):
        """进入发送页面"""
        # 1、进入一对一天界面
        single_chat_page = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        single_chat_page.click_sms()
        time.sleep(2)
        if single_chat_page.wait_until(lambda x: single_chat_page.page_should_contain_text("欢迎使用免费短信"), timeout=8,
                                       auto_accept_permission_alert=False):
            self.assertTrue(single_chat_page.check_cmcc_msg_two_button())
            single_chat_page.driver.back()
        else:
            single_chat_page.wait_for_page_load()
            self.assertTrue(single_chat_page.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0147():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0147(self):
        """会话窗口中点击删除文本消息"""
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.input_text_message('this is a test message')
        single_chat_page.send_text()
        single_chat_page.delete_mess('this is a test message')
        single_chat_page.page_should_not_contain_text('this is a test message')


class MsgGroupChatTest(TestCase):
    """消息:群聊"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        Preconditions.create_contacts_groups()

    def default_setUp(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().launch_app()
        mess = MessagePage()
        if mess.is_on_this_page():
            try:
                mess.choose_chat_by_name(Preconditions.get_group_chat_name(), max_try=3)
                return
            except:
                Preconditions.enter_group_chat_page()
                return
        scp = GroupChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass

    def make_sure_have_loc_msg(self):
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_loc_msg():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_location()
            location_page = ChatLocationPage()
            location_page.wait_for_page_load()
            time.sleep(1)
            # 点击发送按钮
            if not location_page.send_btn_is_enabled():
                raise AssertionError("位置页面发送按钮不可点击")
            location_page.click_send()
            group_chat_page.wait_for_page_load()
            group_chat_page.click_more()

    def public_find_group_chat_open_file(self, file_type='.xlsx'):
        self.make_sure_have_file_msg(file_type)
        GroupChatPage().wait_for_page_load()
        # 1. 点击右上角个人设置按钮
        GroupChatPage().click_setting()
        # 2. 点击下方的查找聊天内容按钮
        GroupChatSetPage().click_search_chat_record()
        current_mobile().hide_keyboard_if_display()
        FindChatRecordPage().wait_for_page_loads()
        FindChatRecordPage().click_file()
        time.sleep(3)
        chat_file = ChatFilePage()
        chat_file.click_file(file_type)
        GroupChatPage().is_exist_more_button()

    def public_open_file(self):
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()

    def public_open_file_click_more_button(self):
        self.public_open_file()
        GroupChatPage().click_more_button()
        time.sleep(1)

    def public_select_recent_chat_send(self):
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        self.assertTrue(GroupChatPage().is_exist_more_button())

    def public_enter_file_select_page(self, n=6):
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(n)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.wait_for_page_load()

    # 群信息转发到手机联系人
    def public_forward_mobile_phone_contacts(self):
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()

    def press_group_file(self):
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.set_network_status(4)
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()

    def pubilic_group_search_text(self, text):
        self.press_group_file()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword(text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            SelectOneGroupPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            GroupChatPage().wait_for_page_load()
            self.assertTrue(GroupChatPage().is_on_this_page())

    def make_sure_have_file_msg(self, file_type='.xlsx'):
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if not group_chat_page.is_exist_msg_send_failed_button() and group_chat_page.is_exist_msg_file():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.set_network_status(4)
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            # 进入预置文件目录，选择文件发送
            local_file.enter_preset_file_dir()
            local_file.select_file(file_type)
            local_file.click_send()
            GroupChatPage().wait_for_page_load()

    def make_sure_have_file_send_fail(self):
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.set_network_status(0)
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            # 进入预置文件目录，选择文件发送
            local_file.enter_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            GroupChatPage().wait_for_page_load()

    # 本地联系人搜索框里输入字符串搜索
    def pubilic_phone_contacts_search_text(self, text):
        self.public_forward_mobile_phone_contacts()
        # 搜索联系人
        search_contact = SelectLocalContactsPage()
        search_contact.search(text)
        if search_contact.is_text_present('无搜索结果'):
            pass
        else:
            search_contact.click_search_phone_contacts()
            search_contact.click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            GroupChatPage().wait_for_page_load()
            self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0001(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""
        # 关闭网络发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(0)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        self.assertTrue(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0002(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0001()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0002():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0003(self):
        """对发送失败的文件进行重发"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0001()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            group_chat_page.click_back()  # xiugaichu
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        group_chat_page.wait_for_message_down_file()
        self.assertTrue(group_chat_page.check_message_resend_success())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0003():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0004(self):
        """对发送失败的文件进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0003()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertFalse(message_page.is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0005(self):
        """点击取消重发文件消失，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0001()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0005():
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0006(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""
        # 关闭wifi发送文件
        # chat_more = ChatMorePage()
        # chat_more.mobile.turn_off_wifi()
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file("2M_data.json")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0007(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file("2M_data.json")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0006()
        GroupChatPage().click_back()
        MessagePage().wait_for_page_load()
        MessagePage().clear_message_record()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0009(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        time.sleep(5)
        if group_chat_page.is_text_present('切换'):
            group_chat_page.click_element_('切换')
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file("2M_data.json")
        local_file.click_single_send()
        local_file.click_free_data_button()
        time.sleep(3)
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'))
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        time.sleep(1)
        local_file.click_back()
        time.sleep(1)
        local_file.click_back()
        time.sleep(1)
        select_file_type.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0009():
        GroupChatPage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0011(self):
        """在文件列表页选择文件后再点击取消按钮，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        # local_file.select_file(".xlsx")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0012(self):
        """在文件列表页点击返回按钮时可正常逐步返回到会话页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        time.sleep(2)
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0012():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0013(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0014(self):
        """网络异常时勾选本地照片内任意相册的图片点击发送按钮"""
        # 1, 聊天页面打开文件夹

        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(0)
        group_chat_page.click_file()
        # 2， 选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0015(self):
        """会话页面有图片发送失败时查看消息列表是否有消息发送失败的标识"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0014()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0015():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0016(self):
        """对发送失败的图片文件进行重发"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0014()
            group_chat_page.set_network_status(6)
            group_chat_page.click_back()
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        self.assertFalse(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0017(self):
        """对发送失败的图片进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0016()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0018(self):
        """点击取消重发图片消息，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0014()
            group_chat_page.set_network_status(0)
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0018():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0019(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""
        # 关闭wifi发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_pic.jpg")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0020(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_pic.jpg")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0019()
        GroupChatPage().click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0020():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0022(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_pic.jpg")
        local_file.click_single_send()
        local_file.click_free_data_button()
        time.sleep(3)
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        time.sleep(1)
        local_file.click_back()
        time.sleep(1)
        select_file_type.click_back()
        time.sleep(1)
        GroupChatPage().click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0022():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0024(self):
        """在选择图片页面选择文件后再点击取消按钮，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.select_file("23e.jpg")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0025(self):
        """在选择图片页面点击返回按钮时可正常逐步返回到会话页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.select_file("23e.jpg")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0027(self):
        """勾选本地视频内任意视频点击发送按钮"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0028(self):
        """网络异常时勾选本地文件内任意视频点击发送按钮"""
        # 1, 聊天页面打开文件夹
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(0)
        group_chat_page.click_file()
        # 2， 选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0029(self):
        """会话页面有视频发送失败时查看消息列表是否有消息发送失败的标识"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0028()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0029():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0030(self):
        """对发送失败的视频进行重发"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0028()
            group_chat_page.set_network_status(6)
            group_chat_page.click_back()
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        self.assertFalse(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0031(self):
        """对发送失败的视频进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0030()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0032(self):
        """点击取消重发视频文件消失，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0028()
            group_chat_page.set_network_status(0)
            import time
            time.sleep(2)
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0032():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0033(self):
        """未订购每月10G的用户发送大于2M的视频时有弹窗提示"""
        # 关闭wifi发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_vedio.mp4")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0034(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_vedio.mp4")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0033()
        GroupChatPage().click_back()
        MessagePage().wait_for_page_load()
        MessagePage().clear_message_record()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0036(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_vedio.mp4")
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0036():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0038(self):
        """在视频列表页选择文件后再点击取消按钮，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.select_file(".mp4")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0039(self):
        """在视频列表页点击返回按钮时可正常逐步返回到会话页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.select_file(".mp4")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0041(self):
        """勾选音乐列表页面任意音乐点击发送按钮"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("28618718.mp3")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0042(self):
        """网络异常时勾选音乐列表页面任意音乐点击发送按钮"""
        # 1, 聊天页面打开文件夹
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(0)
        group_chat_page.click_file()
        # 2， 选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("28618718.mp3")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0043(self):
        """会话页面有音乐文件发送失败时查看消息列表是否有消息发送失败的标识"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0042()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0043():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0044(self):
        """对发送失败的音乐进行重发"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0042()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            group_chat_page.click_back()
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        self.assertFalse(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0045(self):
        """对发送失败的音乐进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0044()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0046(self):
        """点击取消重发音乐文件消失，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0042()
            group_chat_page.set_network_status(6)
            import time
            time.sleep(2)
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0046():
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0047(self):
        """未订购每月10G的用户发送大于2M的音乐时有弹窗提示"""
        # 关闭wifi发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("喜欢你.mp3")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0048(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("喜欢你.mp3")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0047()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0050(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("喜欢你.mp3")
        local_file.click_single_send()
        local_file.click_free_data_button()
        time.sleep(3)
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        time.sleep(1)
        local_file.click_back()
        time.sleep(1)
        select_file_type.click_back()
        time.sleep(1)
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        time.sleep(3)
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0050():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0052(self):
        """在音乐列表页选择文件后再点击取消按钮，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp3")
        # local_file.select_file(".mp3")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0053(self):
        """在音乐列表页点击返回按钮时可正常逐步返回到会话页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp3")
        local_file.select_file(".mp3")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0073(self):
        """在群聊（普通群/企业群）将自己发送的文件转发到当前会话窗口"""
        # 发送一个xls文件并返回聊天页面
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        group_name = Preconditions.get_group_chat_name()
        GroupChatPage().click_back()
        MessagePage().wait_for_page_load()
        MessagePage().choose_chat_by_name(group_name)
        # 转发xls文件
        GroupChatPage().wait_for_page_load()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 选择需要转发的群名
        SelectContactsPage().select_one_recently_contact_by_name(group_name)
        SelectContactsPage().click_sure_forward()
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0074(self):
        """将自己发送的文件转发到普通群"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.set_network_status(4)
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC-skip', 'group_chat')
    def test_msg_weifenglian_qun_0076(self):
        """将自己发送的文件转发到普通群时失败"""
        group_chat_page = GroupChatPage()
        group_chat_page.mobile.turn_off_wifi()
        group_chat_page.mobile.turn_off_mobile_data()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发失败并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC-skip', 'group_chat')
    def test_msg_weifenglian_qun_0078(self):
        """将自己发送的文件转发到普通群时点击取消转发"""
        group_chat_page = GroupChatPage()
        group_chat_page.mobile.turn_off_wifi()
        group_chat_page.mobile.turn_off_mobile_data()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.set_network_status(4)
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_cancel_forward()
        # 点击取消留在当前页面
        SelectOneGroupPage().wait_for_page_load()
        self.assertTrue(SelectOneGroupPage().is_on_this_page())
        # 返回聊天页面
        SelectOneGroupPage().click_back()
        SelectContactsPage().click_back()
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0078():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0080(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""
        self.pubilic_group_search_text('群聊')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0081(self):
        """将自己发送的文件转发到在搜索框输入英文字母搜索到的群"""
        self.pubilic_group_search_text('test')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0082(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的群"""
        self.pubilic_group_search_text('2345')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0083(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的群"""
        self.pubilic_group_search_text('.;,')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0084(self):
        """将自己发送的文件转发到在搜索框输入特殊字符搜索到的群"""
        self.pubilic_group_search_text('αβγ')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0085(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的群"""
        self.pubilic_group_search_text('   ')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0086(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""
        self.pubilic_group_search_text('int123')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0087(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""
        self.pubilic_group_search_text('float0.123')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0089(self):
        """将自己发送的文件转发到搜索到的群时点击取消转发"""
        self.press_group_file()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('test')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            SelectOneGroupPage().click_cancel_forward()
            bol = SelectOneGroupPage().wait_until(lambda x: SelectOneGroupPage().is_text_present('群聊'),
                                                  auto_accept_permission_alert=False)
            self.assertTrue(bol)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0090(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的群"""
        self.press_group_file()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 导航栏选择群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().choose_index_bar_click_element()
        SelectOneGroupPage().click_sure_forward()
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0091(self):
        """将自己发送的文件转发到手机联系人"""
        self.public_forward_mobile_phone_contacts()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0092(self):
        """将自己发送的文件转发到手机联系人时点击取消转发"""
        self.public_forward_mobile_phone_contacts()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_cancel_forward()
        phone_contacts.wait_for_page_load()
        self.assertTrue(phone_contacts.is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0093(self):
        """将自己发送的文件转发到手机联系人时发送失败"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        mp = MessagePage()
        mp.set_network_status(0)
        self.public_forward_mobile_phone_contacts()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()
        GroupChatPage().click_back()
        time.sleep(1)
        mp.click_back_by_android()
        MessagePage().wait_for_page_load(timeout=60)
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        MessagePage().clear_fail_in_send_message()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0093():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0094(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的手机联系人"""
        self.pubilic_phone_contacts_search_text('给个红包1')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0095(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的手机联系人"""
        self.pubilic_phone_contacts_search_text('23579')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0096(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的手机联系人"""
        self.pubilic_phone_contacts_search_text('.;,')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0097(self):
        """将自己发送的文件转发到在搜索框输入字母搜索到的手机联系人"""
        self.pubilic_phone_contacts_search_text('abc')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0098(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的手机联系人"""
        self.pubilic_phone_contacts_search_text('   ')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0100(self):
        """将自己发送的文件转发到在搜索框输入号码搜索到的手机联系人"""
        self.pubilic_phone_contacts_search_text('13800138005')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0101(self):
        """将自己发送的文件转发到在搜索框进行搜索到的手机联系人时取消转发"""
        self.public_forward_mobile_phone_contacts()
        search_contact = SelectLocalContactsPage()
        search_contact.search('13800138005')
        if search_contact.is_text_present('无搜索结果'):
            pass
        else:
            search_contact.click_search_phone_contacts()
            search_contact.click_cancel_forward()
            search_contact.wait_for_page_load()
            self.assertTrue(search_contact.is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0102(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的手机联系人"""
        self.public_forward_mobile_phone_contacts()
        # 导航栏选择联系人
        SelectOneGroupPage().choose_index_bar_click_element()
        SelectOneGroupPage().click_sure_forward()
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0103(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的手机联系人"""
        self.public_forward_mobile_phone_contacts()
        # 导航栏选择联系人
        SelectOneGroupPage().choose_index_bar_click_element()
        SelectOneGroupPage().click_cancel_forward()
        SelectLocalContactsPage().wait_for_page_load()
        self.assertTrue(SelectLocalContactsPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0124(self):
        """将自己发送的文件转发到我的电脑"""
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().search('我的电脑')
        SelectOneGroupPage().click_search_result()
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0125(self):
        """将自己发送的文件转发到最近聊天"""
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0126(self):
        """将自己发送的文件转发到最近聊天时点击取消转发"""
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        select_recent_chat.click_cancel_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(select_recent_chat.is_on_this_page())
        select_recent_chat.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0127(self):
        """将自己发送的文件转发到最近聊天时转发失败"""
        MessagePage().set_network_status(0)
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        select_recent_chat.click_sure_forward()
        GroupChatPage().wait_for_page_load()
        GroupChatPage().click_back()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        MessagePage().clear_fail_in_send_message()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0127():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0128(self):
        """对自己发送出去的文件消息进行删除"""
        self.press_group_file()
        GroupChatPage().delete_group_all_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0129(self):
        """对自己发送出去的文件消息进行十秒内撤回"""
        self.press_group_file()
        GroupChatPage().recall_file('.xlsx')

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0129():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0130(self):
        """对自己发送出去的文件消息进行收藏"""
        self.press_group_file()
        ChatFilePage().collection_file('.xlsx')
        GroupChatPage().wait_for_page_load()
        GroupChatPage().is_exist_collection()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        MePage().click_back()
        MePage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0189(self):
        """在收藏页面查看在群聊收藏自己发送的文件"""
        self.press_group_file()
        ChatFilePage().collection_file('.xlsx')
        GroupChatPage().wait_for_page_load()
        GroupChatPage().is_exist_collection()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        self.assertTrue(collection_page.get_width_of_collection('文件名', 2))
        self.assertTrue(collection_page.page_contain_element('文件大小'))
        file_names = collection_page.get_all_file_names()
        self.assertTrue(file_names[0].endswith(".xlsx"))
        file_ele = collection_page.get_all_collection()
        for i in range(len(file_ele)):
            collection_page.press_and_move_left()
            if collection_page.is_delete_element_present():
                collection_page.click_delete_collection()
                collection_page.click_sure_forward()
        MePage().click_back()
        MePage().wait_for_page_load()
        MePage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0191(self):
        """群聊聊天文件列表页面显示正常"""
        self.press_group_file()
        GroupChatPage().click_setting()
        # 2. 点击下方的查找聊天内容按钮
        GroupChatSetPage().click_search_chat_record()
        current_mobile().hide_keyboard_if_display()
        FindChatRecordPage().wait_for_page_loads()
        FindChatRecordPage().click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        chat_file.click_back()
        FindChatRecordPage().click_back()
        GroupChatSetPage().click_back()
        GroupChatPage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0194(self):
        """群聊聊天文件列表页打开不可直接打开的文件时关闭第三方软件弹窗"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".html")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        # 1. 点击右上角个人设置按钮
        GroupChatPage().click_setting()
        # 2. 点击下方的查找聊天内容按钮
        GroupChatSetPage().click_search_chat_record()
        current_mobile().hide_keyboard_if_display()
        FindChatRecordPage().wait_for_page_loads()
        FindChatRecordPage().click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        chat_file.click_file('.html')
        time.sleep(2)
        current_mobile().back()
        self.assertTrue(chat_file.is_on_this_page())
        chat_file.click_back()
        FindChatRecordPage().click_back()
        GroupChatSetPage().click_back()
        GroupChatPage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0195(self):
        """群聊聊天文件列表页面显示正常"""
        self.press_group_file()
        # 1. 点击右上角个人设置按钮
        GroupChatPage().click_setting()
        # 2. 点击下方的查找聊天内容按钮
        GroupChatSetPage().click_search_chat_record()
        current_mobile().hide_keyboard_if_display()
        FindChatRecordPage().wait_for_page_loads()
        FindChatRecordPage().click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        chat_file.click_file('.xlsx')
        chat_file.click_back()
        chat_file.wait_for_page_loads()
        self.assertTrue(chat_file.is_on_this_page)
        chat_file.click_back()
        time.sleep(1)
        FindChatRecordPage().click_back()
        time.sleep(1)
        GroupChatSetPage().click_back()
        time.sleep(1)
        GroupChatPage().click_back()
        time.sleep(1)
        MessagePage().clear_message_record()

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0199():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0199(self):
        """进入消息模块中"""
        self.assertTrue(MessagePage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0200(self):
        """进入群聊天页面调起隐藏菜单栏"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        time.sleep(1.5)
        self.assertTrue(chat_more.check_all_element_is_enable())
        chat_more.close_more()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0201(self):
        """选择点击文件"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(4)
        group_chat_page.click_file()
        ChatSelectFilePage().wait_for_page_load()
        ChatSelectFilePage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0202(self):
        """观察文件选择页面"""
        self.public_enter_file_select_page()
        local_file = ChatSelectLocalFilePage()
        self.assertTrue(local_file.check_element_is_exist('文件按钮'))
        self.assertFalse(local_file.check_element_is_exist('文件显示大小'))
        self.assertFalse(local_file.check_element_is_enable('发送'))
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0203(self):
        """未选择文件的情况下点击发送按钮"""
        self.public_enter_file_select_page()
        file = ChatSelectLocalFilePage()
        self.assertFalse(file.check_element_is_enable('发送'))
        file.click_back()
        file.click_back()
        ChatSelectFilePage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0204(self):
        """选择其中一文件"""
        self.public_enter_file_select_page()
        file = ChatSelectLocalFilePage()
        file.select_file('.xlsx')
        self.assertTrue(file.check_element_is_exist('文件显示大小'))
        self.assertTrue(file.check_element_is_enable('发送'))
        file.click_back()
        file.click_back()
        ChatSelectFilePage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0205(self):
        """网络异常选择其中一文件"""
        self.public_enter_file_select_page()
        MessagePage().set_network_status(0)
        file = ChatSelectLocalFilePage()
        file.select_file('.xlsx')
        time.sleep(3)
        self.assertTrue(file.check_element_is_exist('文件显示大小'))
        self.assertTrue(file.check_element_is_enable('发送'))
        file.click_back()
        time.sleep(1)
        file.click_back()
        time.sleep(1)
        ChatSelectFilePage().click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0205():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0206(self):
        """发送文件"""
        self.public_enter_file_select_page()
        file = ChatSelectLocalFilePage()
        file.select_file('.xlsx')
        self.assertTrue(file.check_element_is_exist('文件显示大小'))
        self.assertTrue(file.check_element_is_enable('发送'))
        file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().check_message_resend_success())
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0207(self):
        """网络异常时发送文件"""
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        MessagePage().set_network_status(0)
        self.public_enter_file_select_page(n=0)
        file = ChatSelectLocalFilePage()
        file.select_file('.xlsx')
        self.assertTrue(file.check_element_is_exist('文件显示大小'))
        self.assertTrue(file.check_element_is_enable('发送'))
        file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0207():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0223(self):
        """验证在群聊会话窗口点击文件按钮发送文件，文件消息发送失败时左侧是否有重发按钮"""
        self.make_sure_have_file_send_fail()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0223():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0224(self):
        """验证在群聊会话窗口点击文件发送失败的重发按钮是否有弹窗询问"""
        self.make_sure_have_file_send_fail()
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(6)
        group_chat_page.click_msg_send_failed_button()
        bol = group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('是否重发该条信息'))
        self.assertTrue(bol)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0224():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0225(self):
        """验证在群聊会话窗口点击文件发送失败的重发按钮，点击取消时是否正常"""
        self.make_sure_have_file_send_fail()
        group_chat_page = GroupChatPage()
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        time.sleep(10)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0225():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0227(self):
        """验证在群聊会话窗口点击发送失败的文件是否可以正常打开"""
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(0)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0227():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0228(self):
        """验证在群聊会话窗口有发送失败的文件时返回到消息列表是否有发送失败标识"""
        self.make_sure_have_file_send_fail()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0228():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0237(self):
        """验证转发文件到群聊会话窗口时发送失败，点击发送失败的文件是否可以正常打开"""
        self.make_sure_have_file_send_fail()
        MessagePage().set_network_status(0)
        group_chat_page = GroupChatPage()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        group_name = Preconditions.get_group_chat_name()
        SelectContactsPage().select_one_recently_contact_by_name(group_name)
        SelectContactsPage().click_sure_forward()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_last_file_send_fail()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()
        group_chat_page.delete_group_all_file()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0237():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0238(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件时，标题显示是否正常"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('测试用例.xlsx'),
                                   auto_accept_permission_alert=False)
        group_chat_page.click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0239(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0240(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.mobile.back()
        group_chat_page.click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0241(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        group_chat_page.click_element_by_text('转发')
        SelectContactPage().click_back()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0242(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        self.public_open_file_click_more_button()
        GroupChatPage().click_element_by_text('转发')
        self.public_select_recent_chat_send()
        GroupChatPage().click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0243(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        self.public_open_file_click_more_button()
        GroupChatPage().click_element_by_text('收藏')
        GroupChatPage().click_file_back()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        MePage().click_back()
        MePage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0244(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        self.public_open_file_click_more_button()
        GroupChatPage().click_element_by_text('其他应用打开')
        self.assertFalse(GroupChatPage().is_text_present('其他应用打开'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0245(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-取消时是否正常"""
        self.public_open_file_click_more_button()
        current_mobile().back()
        self.assertTrue(GroupChatPage().is_exist_more_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0246(self):
        """验验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件时，标题显示是否正常"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('测试用例.xlsx'),
                                   auto_accept_permission_alert=False)
        # 返回到聊天页面
        ChatFilePage().click_back()
        ChatFilePage().click_back()
        FindChatRecordPage().click_back()
        GroupChatSetPage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0247(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        ChatFilePage().click_back()
        ChatFilePage().click_back()
        FindChatRecordPage().click_back()
        GroupChatSetPage().click_back()

    def public_find_group_chat_back(self):
        """查找聊天内容返回到群聊页面"""
        ChatFilePage().wait_for_page_loads()
        ChatFilePage().click_back()
        FindChatRecordPage().wait_for_page_loads()
        FindChatRecordPage().click_back()
        GroupChatSetPage().wait_for_page_load()
        GroupChatSetPage().click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0248(self):
        """验证在在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.mobile.back()
        group_chat_page.click_file_back()
        self.public_find_group_chat_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0249(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        group_chat_page.click_element_by_text('转发')
        SelectContactPage().click_back()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()
        self.public_find_group_chat_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0250(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        GroupChatPage().click_element_by_text('转发')
        self.public_select_recent_chat_send()
        GroupChatPage().click_file_back()
        self.public_find_group_chat_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0251(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        GroupChatPage().click_element_by_text('收藏')
        GroupChatPage().click_file_back()
        self.public_find_group_chat_back()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        # collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        MePage().click_back()
        MePage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0252(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        group_chat_page.click_element_by_text('其他应用打开')
        self.assertFalse(group_chat_page.is_text_present('其他应用打开'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0253(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-取消时是否正常"""
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        time.sleep(1)
        current_mobile().back()
        self.assertTrue(GroupChatPage().is_exist_more_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0276(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件时，标题显示是否正常"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        MessagePage().set_network_status(0)
        group_chat_page.click_last_file_send_fail()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('测试用例.xlsx'),
                                   auto_accept_permission_alert=False)
        group_chat_page.click_file_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0276():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0277(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        MessagePage().set_network_status(0)
        group_chat_page.click_last_file_send_fail()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0277():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0278(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        MessagePage().set_network_status(0)
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.mobile.back()
        group_chat_page.click_file_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0278():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0279(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        MessagePage().set_network_status(0)
        self.make_sure_have_file_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        group_chat_page.click_element_by_text('转发')
        SelectContactPage().click_back()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0279():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0280(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_file_click_more_button()
        GroupChatPage().click_element_by_text('转发')
        self.public_select_recent_chat_send()
        GroupChatPage().click_file_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0280():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0281(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_file_click_more_button()
        GroupChatPage().click_element_by_text('收藏')
        GroupChatPage().click_file_back()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        MePage().click_back()
        MePage().open_message_page()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0281():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0282(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_file_click_more_button()
        GroupChatPage().click_element_by_text('其他应用打开')
        self.assertFalse(GroupChatPage().is_text_present('其他应用打开'))

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0282():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0283(self):
        """验证在群聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-取消时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_file_click_more_button()
        current_mobile().back()
        self.assertTrue(GroupChatPage().is_exist_more_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0283():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0284(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件时，标题显示是否正常"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('测试用例.xlsx'),
                                   auto_accept_permission_alert=False)
        # 返回到聊天页面
        ChatFilePage().click_back()
        self.public_find_group_chat_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0284():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0285(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        ChatFilePage().click_back()
        self.public_find_group_chat_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0285():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0286(self):
        """验证在在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.mobile.back()
        group_chat_page.click_file_back()
        self.public_find_group_chat_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0286():
        MessagePage().set_network_status(6)

    def public_open_find_file_click_more_button(self):
        self.public_find_group_chat_open_file()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0287(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_find_file_click_more_button()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.click_element_by_text('转发')
        SelectContactPage().click_back()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到消息页面
        group_chat_page.click_file_back()
        self.public_find_group_chat_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0287():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0288(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_find_file_click_more_button()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.click_element_by_text('转发')
        self.public_select_recent_chat_send()
        # 返回到消息页面
        group_chat_page.click_file_back()
        self.public_find_group_chat_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0288():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0289(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_find_file_click_more_button()
        GroupChatPage().click_element_by_text('收藏')
        GroupChatPage().is_exist_collection()
        GroupChatPage().click_file_back()
        self.public_find_group_chat_back()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        # collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        # 返回到消息页面
        MePage().click_back()
        MePage().open_message_page()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0289():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0290(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_find_file_click_more_button()
        GroupChatPage().click_element_by_text('其他应用打开')
        time.sleep(2)
        self.assertFalse(GroupChatPage().is_text_present('其他应用打开'))

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0290():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0291(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-取消时是否正常"""
        MessagePage().set_network_status(0)
        self.public_open_find_file_click_more_button()
        current_mobile().back()
        self.assertTrue(GroupChatPage().is_exist_more_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0291():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0293(self):
        """验证在在群聊-查找聊天内容-文件页面点击打开已下载的不可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file(file_type='.log')
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0293():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0294(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file(file_type='.log')
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        GroupChatPage().click_element_by_text('转发')
        SelectContactPage().click_back()
        self.assertTrue(group_chat_page.is_exist_more_button())
        group_chat_page.click_file_back()
        self.public_find_group_chat_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0294():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0295(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发时是否正常"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file(file_type='.log')
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_more_button())
        # 返回到聊天页面
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        GroupChatPage().click_element_by_text('转发')
        self.public_select_recent_chat_send()
        GroupChatPage().click_file_back()
        self.public_find_group_chat_back()
        time.sleep(10)
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0295():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0296(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-收藏时是否正常"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file(file_type='.log')
        group_chat_page = GroupChatPage()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        GroupChatPage().click_element_by_text('收藏')
        GroupChatPage().click_file_back()
        self.public_find_group_chat_back()
        GroupChatPage().click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        # collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        MePage().click_back()
        MePage().open_message_page()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0296():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0297(self):
        """验证在群聊-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-取消时是否正常"""
        MessagePage().set_network_status(0)
        self.public_find_group_chat_open_file(file_type='.log')
        group_chat_page = GroupChatPage()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        time.sleep(1)
        current_mobile().back()
        self.assertTrue(GroupChatPage().is_exist_more_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0297():
        MessagePage().set_network_status(6)


class MsgGroupChatPrior(TestCase):
    """消息 - 单聊"""

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.create_contacts_groups()

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            try:
                mess.choose_chat_by_name(Preconditions.get_group_chat_name())
                return
            except:
                Preconditions.enter_group_chat_page()
                return
        scp = GroupChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass

    def make_sure_have_loc_msg(self):
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_loc_msg():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_location()
            location_page = ChatLocationPage()
            location_page.wait_for_page_load()
            time.sleep(1)
            # 点击发送按钮
            if not location_page.send_btn_is_enabled():
                raise AssertionError("位置页面发送按钮不可点击")
            location_page.click_send()
            group_chat_page.wait_for_page_load()
            group_chat_page.click_more()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'level_high')
    def test_msg_weifenglian_qun_0336(self):
        """将自己发送的位置转发到手机联系人"""
        self.make_sure_have_loc_msg()
        GroupChatPage().press_message_to_do("转发")
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_local_contacts()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.wait_for_page_load()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'level_high')
    def test_msg_weifenglian_qun_0369(self):
        """将自己发送的位置转发到我的电脑"""
        self.make_sure_have_loc_msg()
        GroupChatPage().press_message_to_do("转发")
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().search('我的电脑')
        SelectOneGroupPage().click_search_result()
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'level_high')
    def test_msg_weifenglian_qun_0370(self):
        """将自己发送的位置转发到我的电脑"""
        self.make_sure_have_loc_msg()
        GroupChatPage().press_message_to_do("转发")
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'level_high')
    def test_msg_weifenglian_qun_0373(self):
        """对自己发送出去的位置消息进行删除"""
        self.make_sure_have_loc_msg()
        GroupChatPage().press_message_to_do("删除")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'level_high')
    def test_msg_weifenglian_qun_0374(self):
        """对自己发送出去的位置消息进行十秒内撤回"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 点击发送按钮
        if not location_page.send_btn_is_enabled():
            raise AssertionError("位置页面发送按钮不可点击")
        location_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_more()
        group_chat_page.recall_loc_msg()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'level_high')
    def test_msg_weifenglian_qun_0375(self):
        """对自己发送出去的位置消息进行收藏"""
        self.make_sure_have_loc_msg()
        group_chat_page = GroupChatPage()
        group_chat_page.press_message_to_do("收藏")
        GroupChatPage().is_exist_collection()
        GroupChatPage().click_back_by_android()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        time.sleep(1)
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        bol = collection_page.wait_until(condition=lambda x: collection_page.is_text_present('位置'))
        self.assertTrue(bol)
        MePage().click_back()
        MePage().open_message_page()
