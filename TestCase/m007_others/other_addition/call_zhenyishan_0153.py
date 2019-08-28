import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_call_zhenyishan_0153():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0153(self):
        """分组群发/标签分组/群发消息：多方视频联系人选择器--点击任意群成员"""
        # 1、已通过分组群发/标签分组/群发消息进入多方视频联系人选择器
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_label_grouping_631()
        labellist = LabelGroupingPage()
        time.sleep(2)
        if '测试分组Beta' not in labellist.get_label_grouping_names():
            labellist.create_group_631('测试分组Beta', '给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3',
                                       '联系人4')
        # Step 2.任意点击一存在多名成员的标签分组
        labellist.click_label_group('测试分组Beta')
        time.sleep(2)
        # 选择成员进行多方视频
        labellist.click_four_image_call()
        time.sleep(2)
        labellist.click_local_contacts('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3', '联系人4')
        labellist.is_toast_exist('人数已达上限8人')
        labellist.click_back_by_android()
        labellist.click_four_image_call()
        labellist.page_should_contain_text('呼叫')
        labellist.click_local_contacts('测试短信1')
        labellist.page_should_contain_text('呼叫(1/8)')
        labellist.page_should_contain_text('信1')




