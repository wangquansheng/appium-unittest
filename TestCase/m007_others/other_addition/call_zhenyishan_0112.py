from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import ContactsSelector
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_call_zhenyishan_0112():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
                                                        "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0112(self):
        """通话模块：当前勾选人数已有8人，继续勾选团队联系人，检查提示"""
        # 1、当前为团队联系人选择页
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()

        ContactsSelector().select_local_contacts('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3', '联系人4')
        mess.is_toast_exist('最多只能选择8人')


