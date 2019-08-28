import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0259():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0259(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发时是否正常"""
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的不可预览文件
        # 3、网络异常
        MessagePage().search_and_enter_631('给个名片1')
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
        single_chat.click_mess_text('录制.txt')
        time.sleep(3)
        single_chat.page_should_contain_text('录制.txt')


    def tearDown_test_msg_weifenglian_1V1_0259(self):
        SingleChatPage().set_network_status(6)

