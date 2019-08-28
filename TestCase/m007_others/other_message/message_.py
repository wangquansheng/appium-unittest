import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
from pages.components import ChatNoticeDialog, ContactsSelector
from pages.message.FreeMsg import FreeMsgPage
from pages.message.Send_CardName import Send_CardNamePage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_hanjiabin_0179():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0179(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.assert_card_name_equal_to('给个名片2')
        send_card.is_present_card_phone('13800138300')
        send_card.assert_card_comp_equal_to('中软国际')
        send_card.assert_card_emailaddress_equal_to('test1234@163.com')
        send_card.assert_card_position_equal_to('软件工程师')
        send_card.click_close_btn()
        # 判断存在选择联系人
        SelectContactPage().is_exist_select_contact_btn()

    @staticmethod
    def setUp_test_msg_hanjiabin_0187():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0187(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        current_mobile().set_network_status(1)
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        time.sleep(2)
        chatwindow = ChatWindowPage()
        chatwindow.click_resend_button()
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_hanjiabin_0189():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0189(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        mess.click_element((MobileBy.XPATH, '//*[@text="给个名片2"]'))
        GroupChatSetSeeMembersPage().wait_for_profile_page_load()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'))
        mess.choose_chat_by_name('给个名片1')
        ContactDetailsPage().click_message_icon()
        send_card.press_mess('给个名片2')
        mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @staticmethod
    def setUp_test_msg_hanjiabin_0195():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0195(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        mess.click_element((MobileBy.XPATH, '//*[@text="多选"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text="删除"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text="转发"]'))
        mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0022():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0022(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        chatdialog = ChatNoticeDialog()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
        # 判断存在？标志
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'))
        # 判断存在退出短信按钮
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0045():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0045(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        mess.assert_new_message_text_equal_to('新建消息')
        mess.assert_free_sms_text_equal_to('免费短信')
        mess.assert_group_chat_text_equal_to('发起群聊')
        mess.assert_group_mass_text_equal_to('群发助手')
        mess.assert_take_a_scan_text_equal_to('扫一扫')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0052():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0052(self):
        single = SingleChatPage()
        mess = MessagePage()
        chatdialog = ChatNoticeDialog()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')

            # 若存在资费提醒对话框，点击确认
            if chatdialog.is_exist_tips():
                chatdialog.accept_and_close_tips_alert()
            single.input_text_message('呵呵哒')
            single.send_text()
            single.click_back()
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
            # 若存在资费提醒对话框，点击确认
            if chatdialog.is_exist_tips():
                chatdialog.accept_and_close_tips_alert()
        single.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0064():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0064(self):
        single = SingleChatPage()
        mess = MessagePage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single.click_setting()
        self.assertTrue(SingleChatSetPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0065():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0065(self):
        single = SingleChatPage()
        chat_set = SingleChatSetPage()
        mess = MessagePage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.click_avatar()
        GroupChatSetSeeMembersPage().wait_for_profile_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0070():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0070(self):
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.search_chat_record()
        FindChatRecordPage().wait_for_page_loads()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0072():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0072(self):
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="呵呵哒"]')):
            single.input_text_message("呵呵哒")
            single.send_text()
        single.open_expression()
        count = 0
        while(count <= 10):
            single.select_expression()
            count = count + 1
        single.close_expression()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.search_chat_record()
        findchat.wait_for_page_loads()
        findchat.input_search_message('呵呵哒')
        findchat.click_record()
        CallPage().wait_for_chat_page()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0078():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0078(self):
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.search_chat_record()
        findchat.wait_for_page_loads()
        findchat.input_search_message('ADDWOQWIQWOPPQWIDIWQDQW')
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="无搜索结果"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0089():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0089(self):
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.click_add_icon()
        ContactsSelector().wait_for_contacts_selector_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0100():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0100(self):
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        # 如果当前页面不存在消息，发送一条消息
        if single._is_element_present((MobileBy.XPATH, '//*[@text ="呵呵哒"]')):
            single.press_mess('呵呵哒')
            mess.click_element((MobileBy.XPATH, '//*[@text ="删除"]'))
        single.input_text_message("呵呵哒")
        single.send_text()
        single.press_mess('呵呵哒')
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="复制"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="转发"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="收藏"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="删除"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="撤回"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="转为短信发送"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="多选"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0151():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0151(self):
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        self.assertTrue(single.is_exist_send_audio_button())
        single.input_text_message("11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        self.assertTrue(single.is_exist_send_txt_button())
        single.send_text()
        time.sleep(1)
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="已转短信送达"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0182():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0182(self):
        single = SingleChatPage()
        mess = MessagePage()

        # 如果当前页面不存在消息，发送一条消息
        if not mess._is_element_present((MobileBy.XPATH, '//*[@text ="给个红包1"]')):
            # 点击+号
            mess.click_add_icon()
            mess.click_new_message()
            select_page = SelectContactsPage()
            select_page.select_one_contact_by_name('给个红包1')
        else:
            mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        # 如果当前页面不存在消息，发送一条消息
        if single._is_element_present((MobileBy.XPATH, '//*[@text ="呵呵哒"]')):
            single.press_mess('呵呵哒')
            mess.click_element((MobileBy.XPATH, '//*[@text ="删除"]'))
        single.input_text_message("呵呵哒")
        single.send_text()
        single.press_mess('呵呵哒')
        mess.click_element((MobileBy.XPATH, '//*[@text ="撤回"]'))
        single.click_i_know()
        time.sleep(3)
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="你撤回了一条信息"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0184():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0184(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        single.press_mess("测试一个呵呵")
        single.click_multiple_selection()
        time.sleep(2)
        group_chat = GroupChatPage()
        # 勾选消息时校验页面元素
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('已选择')
        self.assertTrue(group_chat.is_exist_multiple_selection_count())
        self.assertTrue(group_chat.is_enabled_multiple_selection_delete())
        self.assertTrue(group_chat.is_enabled_multiple_selection_forward())
        # 未勾选消息时校验页面元素
        group_chat.get_multiple_selection_select_box()[0].click()
        time.sleep(1)
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('未选择')
        self.assertFalse(group_chat.is_exist_multiple_selection_count())
        self.assertFalse(group_chat.is_enabled_multiple_selection_delete())
        self.assertFalse(group_chat.is_enabled_multiple_selection_forward())