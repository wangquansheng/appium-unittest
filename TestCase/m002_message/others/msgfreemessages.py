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
    def make_already_have_used_free_sms():
        """确保非首次使用免费短信功能"""
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        mp = MessagePage()
        mp.click_add_icon()
        mp.click_free_sms()
        time.sleep(1)
        if FreeMsgPage().is_exist_cancle_btn():
            FreeMsgPage().click_sure_btn()
            time.sleep(1)
            SelectContactsPage().click_search_contact()
            current_mobile().hide_keyboard_if_display()
        mp.click_back_by_android()
        return

    @staticmethod
    def make_already_have_used_free_sms2():
        """确保非首次使用免费短信功能"""
        mp = MessagePage()
        mp.click_add_icon()
        mp.click_free_sms()
        time.sleep(1)
        if FreeMsgPage().is_exist_cancle_btn():
            FreeMsgPage().click_sure_btn()
            time.sleep(1)
            SelectContactsPage().click_search_contact()
            current_mobile().hide_keyboard_if_display()
        # mp.click_back_by_android()

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
    def select_contact_send_sms(name):
        """选择联系人，发送短信"""
        Preconditions.make_already_have_used_free_sms()
        Preconditions.enter_single_chat_page(name)
        basepg = BaseChatPage()
        basepg.click_free_msg()
        time.sleep(2)
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        if basepg.is_exist_send_button():
            basepg.click_send_button()
        basepg.click_exit_sms()
        basepg.click_back_by_android()


class MessageScanTest(TestCase):
    """消息->免费短信"""
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

    @classmethod
    def tearDownClass(cls):
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    def default_setUp(self):
        """确保进入消息界面"""
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC_RESET', 'freemsg')
    def test_msg_huangcaizui_B_0007(self):
        """从+号首次点击“免费短信”是否有资费弹框出来"""
        # 1.正常联网
        # 2.客户端在线
        # Step: 1.进入消息模块页面
        mp = MessagePage()
        # Step: 2.点击右上角“+”
        mp.click_add_icon()
        time.sleep(1)
        # CheckPoint: 2.弹出多功能列表
        mp.page_should_contain_text("新建消息")
        mp.page_should_contain_text("免费短信")
        mp.page_should_contain_text("发起群聊")
        mp.page_should_contain_text("群发助手")
        mp.page_should_contain_text("扫一扫")

        # Step: 3.点击免费短信
        mp.click_free_sms()
        # CheckPoint: 3.触发短信资费介绍页“欢迎使用免费短信！”
        time.sleep(1)
        mp.page_should_contain_text("欢迎使用免费短信")

    @tags('ALL', '异网', 'freemsg')
    def test_msg_huangcaizui_B_0008(self):
        """从+号首次点击“免费短信”是否有资费弹框出来-大陆异网用户"""
        # 1.正常联网
        # 2.客户端在线
        # 3.大陆异网用户
        # Step: 1.进入消息模块页面
        mp = MessagePage()
        # Step: 2.点击右上角“+”
        mp.click_add_icon()
        time.sleep(1)
        # CheckPoint: 2.弹出多功能列表
        mp.page_should_contain_text("新建消息")
        mp.page_should_contain_text("免费短信")
        mp.page_should_contain_text("发起群聊")
        mp.page_should_contain_text("群发助手")
        mp.page_should_contain_text("扫一扫")

        # Step: 3.点击免费短信
        mp.click_free_sms()
        # CheckPoint: 3.触发短信资费介绍页“欢迎使用免费短信！”
        time.sleep(1)
        mp.page_should_contain_text("欢迎使用免费短信")

    @tags('ALL', 'CMCC_RESET', 'freemsg')
    def test_msg_huangcaizui_B_0010(self):
        """点击以后再说时候会返回消息列表"""
        # 1.正常联网
        # 2.客户端在线
        # 3.大陆本网用户
        # Step: 1.进入消息模块页面
        mp = MessagePage()
        # Step: 2.点击右上角“+”
        mp.click_add_icon()
        time.sleep(1)
        # CheckPoint: 2.弹出多功能列表
        mp.page_should_contain_text("新建消息")
        mp.page_should_contain_text("免费短信")
        mp.page_should_contain_text("发起群聊")
        mp.page_should_contain_text("群发助手")
        mp.page_should_contain_text("扫一扫")

        # Step: 3.点击免费短信
        mp.click_free_sms()
        # CheckPoint: 3.触发短信资费介绍页“欢迎使用免费短信！”
        time.sleep(1)
        mp.page_should_contain_text("欢迎使用免费短信")

        # Step: 4.点击“以后再说”
        FreeMsgPage().click_cancle_btn()
        time.sleep(1)

        # CheckPoint: 4.自动退回消息列表
        mp.is_on_this_page()

    @tags('ALL', 'CMCC_RESET', 'freemsg')
    def test_msg_huangcaizui_B_0011(self):
        """点击确实时候会进入联系人选择器"""
        # 1.正常联网
        # 2.客户端在线
        # 3.大陆本网用户
        # Step: 1.进入消息模块页面
        mp = MessagePage()
        # Step: 2.点击右上角“+”
        mp.click_add_icon()
        time.sleep(1)
        # CheckPoint: 2.弹出多功能列表
        mp.page_should_contain_text("新建消息")
        mp.page_should_contain_text("免费短信")
        mp.page_should_contain_text("发起群聊")
        mp.page_should_contain_text("群发助手")
        mp.page_should_contain_text("扫一扫")

        # Step: 3.点击免费短信
        mp.click_free_sms()
        # CheckPoint: 3.触发短信资费介绍页“欢迎使用免费短信！”
        time.sleep(1)
        mp.page_should_contain_text("欢迎使用免费短信")

        # Step: 4.点击“确定”
        FreeMsgPage().click_sure_btn()
        time.sleep(1)
        SelectContactsPage().click_search_contact()
        # CheckPoint: 4.进入联系人选择界面
        mp.page_should_contain_text("选择联系人")

    @tags('ALL', 'CMCC_RESET', 'freemsg')
    def test_msg_huangcaizui_B_0012(self):
        """从+号首次点击“发送短信”是否有资费弹框出来"""
        # 1.正常联网
        # 2.客户端在线
        # Step: 1.进入消息模块页面
        mp = MessagePage()
        # Step: 2.点击右上角“+”
        mp.click_add_icon()
        time.sleep(1)
        # CheckPoint: 2.弹出多功能列表
        mp.page_should_contain_text("新建消息")
        mp.page_should_contain_text("免费短信")
        mp.page_should_contain_text("发起群聊")
        mp.page_should_contain_text("群发助手")
        mp.page_should_contain_text("扫一扫")

        # Step: 3.点击免费短信

        mp.click_free_sms()
        # CheckPoint: 3.触发短信资费介绍页“欢迎使用免费短信！”
        time.sleep(1)
        mp.page_should_contain_text("欢迎使用免费短信")

        # Step: 4.点击“以后再说”
        FreeMsgPage().click_cancle_btn()
        time.sleep(1)

        # CheckPoint: 4.自动退回消息列表
        mp.is_on_this_page()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0023(self):
        """在单聊页面中非首次点击发送短信按钮是否有短信资费介绍页"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.已经使用过发送短信功能，短信设置开关已开启
        Preconditions.make_already_have_used_free_sms2()
        # 4.在单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        # Step: 1.点击下方发送短信按钮
        basepg = BaseChatPage()
        # CheckPoint: 1.直接进入短信编辑页面
        self.assertTrue(basepg.is_exist_exit_sms())
        # Step: 2.编辑好短信，点击发送按钮
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(1)
        if basepg.is_exist_send_button():
            basepg.click_send_button()
        time.sleep(2)
        # CheckPoint: 2.短信发送成功并返回短信编辑页面
        self.assertTrue(basepg.is_exist_exit_sms())
        basepg.click_exit_sms()
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0023():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0024():
        """确保进入消息界面"""
        Preconditions.make_already_in_message_page()
        MessagePage().set_network_status(0)

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0024(self):
        """在单聊页面中非首次点击发送短信按钮是否有短信资费介绍页--网络异常"""
        # 1.网络异常，本网用户
        # 2.客户端已登录
        # 3.已经使用过发送短信功能，短信设置开关已开启
        Preconditions.make_already_have_used_free_sms2()
        # 4.在单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        # Step: 1.点击下方发送短信按钮
        basepg = BaseChatPage()
        time.sleep(2)
        # CheckPoint: 1.直接进入短信编辑页面
        self.assertTrue(basepg.is_exist_exit_sms())
        # Step: 2.编辑好短信，点击发送按钮
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(1)
        if basepg.is_exist_send_button():
            basepg.click_send_button()
        time.sleep(2)
        # CheckPoint: 2.短信发送失败，toast提示：网络异常，请检查网络设置(IOS)
        self.assertTrue(SingleChatPage().is_msg_send_fail())

        basepg.click_exit_sms()
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0024():
        MessagePage().set_network_status(6)
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0035(self):
        """在单聊页面中非首次点击发送短信按钮是否有短信资费介绍页--无资费介绍"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.已经使用过发送短信功能，短信设置开关已开启
        Preconditions.make_already_have_used_free_sms2()
        # 4.在单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        # Step: 1.点击下方发送短信按钮
        basepg = BaseChatPage()
        # CheckPoint: 1.直接进入短信编辑页面，无资费介绍页
        basepg.page_should_not_contain_text("欢迎使用免费短信")
        self.assertTrue(basepg.is_exist_exit_sms())
        basepg.click_exit_sms()
        basepg.click_back_by_android()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0036(self):
        """转发短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg.press_mess("测试短信，请勿回复")
        # 3、点击转发按钮
        basepg.click_forward()
        # CheckPoint: 选择转发会调起联系人选择器，转发短信成功
        basepg.page_should_contain_text("选择联系人")
        # 4、选择转发联系人
        SelectContactsPage().search("14775970982")
        SelectContactsPage().select_one_contact_by_name('测试号码')
        # 5、点击发送
        SelectLocalContactsPage().click_sure_forward()
        # CheckPoint: 选择转发会调起联系人选择器，转发短信成功
        self.assertTrue(basepg.is_toast_exist("已转发"))
        time.sleep(2)
        if basepg.is_exist_exit_sms():
            basepg.click_exit_sms()
        time.sleep(1)
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0036():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0037(self):
        """删除短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_mess("测试短信，请勿回复")
        # 3、点击删除按钮
        basepg.click_delete()
        # 4、确认删除（IOS）
        # SelectLocalContactsPage().click_sure_forward()
        # CheckPoint: 短信成功删除
        basepg.page_should_not_contain_text("测试短信，请勿回复")
        time.sleep(2)
        if basepg.is_exist_exit_sms():
            basepg.click_exit_sms()
        time.sleep(1)
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0037():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0038(self):
        """复制短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_mess("测试短信，请勿回复")
        # 3、点击复制按钮
        basepg.click_copy()
        # CheckPoint: 短信成功复制
        self.assertTrue(basepg.is_toast_exist("已复制"))
        time.sleep(2)
        if basepg.is_exist_exit_sms():
            basepg.click_exit_sms()
            time.sleep(1)
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0038():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0039(self):
        """收藏短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_mess("测试短信，请勿回复")
        # 3、点击收藏按钮
        basepg.click_collection()
        # CheckPoint: 短信成功收藏
        self.assertTrue(basepg.is_toast_exist("已收藏"))
        time.sleep(3)
        if basepg.is_exist_exit_sms():
            basepg.click_exit_sms()
            time.sleep(1)
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0039():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0040(self):
        """多选，批量转发与删除短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.click_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_mess("测试短信，请勿回复")
        # 3、点击多选按钮
        basepg.click_multiple_selection()
        time.sleep(1)
        # CheckPoint: 成功进入多选模式，可批量转发与删除短信
        basepg.page_should_contain_text("删除")
        basepg.page_should_contain_text("转发")
        time.sleep(1)
        basepg.click_back_by_android()
        if basepg.is_exist_exit_sms():
            basepg.click_exit_sms()
            time.sleep(1)
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0040():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()
