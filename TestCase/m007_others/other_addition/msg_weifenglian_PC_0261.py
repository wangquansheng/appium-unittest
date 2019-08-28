import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0261():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0261(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的可预览文件
        # 3、网络正常
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_id_menu_more()

