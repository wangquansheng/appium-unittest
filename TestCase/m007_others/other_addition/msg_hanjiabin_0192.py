import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
from pages.components import ChatNoticeDialog, ContactsSelector
from pages.message.FreeMsg import FreeMsgPage
from pages.message.Send_CardName import Send_CardNamePage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(LoginPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_hanjiabin_0192():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0192(self):
        mess = MessagePage()
        singlechat = SingleChatPage()
        # Step 1.进入一对一聊天窗口
        mess.search_and_enter_631('给个名片1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        singlechat.click_more()
        singlechat.click_profile()

        selectcontact = SelectLocalContactsPage()
        send_card = Send_CardNamePage()
        # Checkpoint 进入到联系人选择器页面
        selectcontact.wait_for_page_load()
        # Step 任意选中一个联系人的名片，发送出去
        ContactsSelector().click_local_contacts('给个名片2')
        time.sleep(2)
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        singlechat.select_collect_item()
        mess.click_back_by_android(times=3)
        mess.click_me_icon()
        me = MePage()
        me.click_collection()
        mess.is_text_present('[名片]给个名片2的个人名片')



    def tearDown_test_msg_hanjiabin_0192(self):
        Preconditions.disconnect_mobile('Android-移动')
