import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import ChatNoticeDialog
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0268():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0268(self):
        """验证转发文件到当前单聊会话窗口，文件发送失败的重发按钮，点击确定时是否正常发送"""
        # 1、当前在单聊会话窗口页面
        # 2、当前会话页面有发送失败的文件
        MessagePage().search_and_enter_631('给个名片1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()

        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        single_chat.set_network_status(1)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(2)
        single_chat.click_msg_send_failed_button(0)
        single_chat.click_sure()


    def tearDown_test_msg_weifenglian_1V1_0268(self):
        SingleChatPage().set_network_status(6)

