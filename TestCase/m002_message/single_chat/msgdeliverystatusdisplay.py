import unittest
import uuid

from selenium.common.exceptions import TimeoutException
from pages.components import BaseChatPage
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
import preconditions
import time
from pages.message.FreeMsg import FreeMsgPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page():
        """确保进入消息界面"""
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        message_page = MessagePage()
        if message_page.is_on_this_page():
            return
        try:
            current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
        except:
            pass
        current_mobile().launch_app()
        try:
            message_page.wait_until(
                condition=lambda d: message_page.is_on_this_page(),
                timeout=15
            )
            return
        except TimeoutException:
            pass
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

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


class MsgDeliveryStatusDisplay(TestCase):
    """
    模块：单聊->消息送达状态显示
    文件位置：114整理全量测试用例-黄彩最.xlsx
    表格：单聊
    """
    @classmethod
    def setUpClass(cls):
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
                current_mobile().hide_keyboard_if_display()
                preconditions.make_already_in_message_page()
                for name, number in required_contacts:
                    conts.open_contacts_page()
                    if conts.is_text_present("显示"):
                        conts.click_text("不显示")
                    conts.create_contacts_if_not_exits(name, number)

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

    @classmethod
    def tearDownClass(cls):
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    def default_setUp(self):
        """确保进入消息界面"""
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'msg', 'high')
    def test_msg_huangcaizui_A_0260(self):
        """消息送达状态显示开关入口"""
        # 1、客户端已登录
        # Step:1、点击我-设置-消息设置
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        time.sleep(1)
        setting_page = SettingPage()
        setting_page.click_menu("消息")
        time.sleep(1)
        msg_setting = MessageNoticeSettingPage()
        # CheckPoint:1、显示消息设置页，显示【消息送达状态显示】开关，默认开启
        msg_setting.assert_menu_item_has_been_turn_on('消息送达状态显示')
        me_page.click_back_by_android(2)
        cp = ContactsPage()
        cp.open_message_page()

    @tags('ALL', 'CMCC', 'msg', 'high')
    def test_msg_huangcaizui_A_0261(self):
        """关闭送达状态显示"""
        # 1、客户端已登录
        # Step:1、发送任意消息体
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        time.sleep(1)
        setting_page = SettingPage()
        setting_page.click_menu("消息")
        time.sleep(1)
        msg_setting = MessageNoticeSettingPage()
        msg_setting.turn_off("消息送达状态显示")
        me_page.click_back()
        me_page.click_back()
        cp = ContactsPage()
        cp.open_message_page()
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")
        chat = SingleChatPage()
        chat.input_message("test_msg_huangcaizui_A_0261")

        # CheckPoint:1、发送成功，不显示送达状态（已送达、已发送短信提醒、对方离线，已提醒）
        chat.send_message()
        time.sleep(2)
        chat.page_should_not_contain_text("已送达")
        chat.page_should_not_contain_text("已发送短信提醒")
        chat.page_should_not_contain_text("对方离线")
        chat.page_should_not_contain_text("已提醒")
        chat.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0261():
        """清空聊天记录，并设置消息送达状态显示为开启"""
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        time.sleep(1)
        setting_page = SettingPage()
        setting_page.click_menu("消息")
        time.sleep(1)
        msg_setting = MessageNoticeSettingPage()
        msg_setting.turn_on("消息送达状态显示")
        me_page.click_back()
        me_page.click_back()
        cp = ContactsPage()
        cp.open_message_page()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0271():
        # 关闭网络
        Preconditions.make_already_in_message_page()
        MessagePage().set_network_status(0)

    @tags('ALL', 'CMCC', 'msg', 'high')
    def test_msg_huangcaizui_A_0271(self):
        """发送失败-本网发送"""
        # 1、已登录客户端
        # 2、网络异常
        # 3、本网发送
        # Step:1、向用户A发送任意消息体
        Preconditions.enter_single_chat_page("大佬1")
        chat = SingleChatPage()
        chat.input_message("test_msg_huangcaizui_A_0271")
        chat.send_message()
        time.sleep(2)
        # CheckPoint:1、发送失败，不显示送达状态（不用预留状态显示位置）
        self.assertTrue(chat.is_msg_send_fail())
        chat.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0271():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()
        MessagePage().set_network_status(6)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0272():
        # 关闭网络
        Preconditions.make_already_in_message_page()
        MessagePage().set_network_status(0)

    @tags('ALL', '异网', 'msg')
    def test_msg_huangcaizui_A_0272(self):
        """发送失败-异网发送"""
        # 1、已登录客户端
        # 2、网络异常
        # 3、异网发送
        # Step:1、向用户A发送任意消息体
        Preconditions.enter_single_chat_page("大佬1")
        chat = SingleChatPage()
        chat.input_message("test_msg_huangcaizui_A_0272")
        chat.send_message()
        time.sleep(2)
        # CheckPoint:1、发送失败，不显示送达状态（不用预留状态显示位置）
        self.assertTrue(chat.is_msg_send_fail())
        chat.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0272():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()
        MessagePage().set_network_status(6)

