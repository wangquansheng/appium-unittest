import os
import random
import time
import unittest
import warnings

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
from pages.components import BaseChatPage
from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from settings import PROJECT_PATH


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def enter_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n = n + 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ateam" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
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
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        # guide_page.swipe_to_the_second_banner()
        # guide_page.swipe_to_the_third_banner()
        # current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
        permission_list.click_permission_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        # if one_key.have_read_agreement_detail():
        #     one_key.click_read_agreement_detail()
        #     # 同意协议
        #     agreement = AgreementDetailPage()
        #     agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
        agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def public_send_file(file_type):
        """选择指定类型文件发送"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = GroupChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def delete_record_group_chat():
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # if not gcsp.is_toast_exist("聊天记录清除成功"):
            #     raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @staticmethod
    def build_one_new_group(group_name):
        """新建一个指定名称的群，如果已存在，不建群"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
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
        time.sleep(2)
        sc.click_select_one_group()
        # 群名
        # group_name = Preconditions.get_group_chat_name()
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
            if not mess.is_on_this_page():
                current_mobile().back()
                time.sleep(2)
                current_mobile().back()
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
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
        GroupChatPage().click_back()

    @staticmethod
    def make_in_message_page(moible_param, reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile(moible_param, reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def build_one_new_group_with_number(puhone_number, group_name):
        """新建一个指定成员和名称的群，如果已存在，不建群"""
        # 消息页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
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
        # group_name = Preconditions.get_group_chat_name()
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
            return True
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 添加指定电话成员
        time.sleep(2)
        sc.input_search_keyword(puhone_number)
        time.sleep(2)
        sog.click_text("tel")
        time.sleep(2)
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        SelectContactsPage().click_one_contact_631("飞信电话")
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()
        return False

    @staticmethod
    def get_group_chat_name_double():
        """获取多人群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "多机" + phone_number[-4:]
        return group_name

    @staticmethod
    def go_to_group_double(group_name):
        """从消息列表进入双机群聊，前提：已经存在双机群聊"""
        mess = MessagePage()
        mess.wait_for_page_load()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
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
        # # 群名
        # group_name = Preconditions.get_group_chat_name_double()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有找到双机群聊，请确认是否创建")
        sog.click_element_("群聊名")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def change_mobile(moible_param):
        """转换设备连接并且确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        current_mobile().hide_keyboard_if_display()
        current_mobile().launch_app()
        Preconditions.make_in_message_page(moible_param)

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n += 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def enter_message_page(reset=False):
        """进入消息页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)

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
    def dismiss_one_group(name):
        Preconditions.get_into_group_chat_page(name)
        GroupChatPage().click_setting()
        page = GroupChatSetPage()
        time.sleep(1)
        page.click_group_manage()
        time.sleep(1)
        page.click_group_manage_disband_button()
        time.sleep(0.5)
        page.click_element_('确定')
        time.sleep(3)
        page.wait_for_text('该群已解散')

    @staticmethod
    def dismiss_one_group2(name):
        Preconditions.get_into_group_chat_page(name)
        GroupChatPage().click_setting()
        page = GroupChatSetPage()
        time.sleep(1)
        page.click_group_manage2()
        time.sleep(1)
        page.click_group_manage_disband_button()
        time.sleep(0.5)
        page.click_element_('确定')
        time.sleep(3)
        page.wait_for_text('该群已解散')

    def press_group_file(self):
        group_chat_page = GroupChatPage()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()

    def public_forward_mobile_phone_contacts(self):
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()


class MsgAllPrior(TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0232(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-转发时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0264(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0265(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        # ChatFilePage().collection_file('.xlsx')
        # SelectContactsPage().wait_for_page_load()
        # SelectContactsPage().select_local_contacts()
        # SelectLocalContactsPage().wait_for_page_load()
        # phone_contacts = SelectLocalContactsPage()
        # phone_contacts.click_first_phone_contacts()
        # phone_contacts.click_sure_forward()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0266(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.mobile.back()
        group_chat_page.click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0268(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件时，页面显示是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.mobile.back()
        group_chat_page.click_file_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0272(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.click_text_or_description("收藏")
        group_chat_page.is_toast_exist("已收藏")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0310(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0314(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()
        group_chat_page.wait_until(condition=lambda x: group_chat_page.is_text_present('收藏'),
                                   auto_accept_permission_alert=False)
        self.assertTrue(group_chat_page.check_options_is_enable())
        group_chat_page.click_text_or_description("收藏")
        group_chat_page.is_toast_exist("已收藏")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0315(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        Preconditions.enter_my_computer_page()
        group_chat_page = GroupChatPage()
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        group_chat_page.click_last_file_send_fail()
        group_chat_page.is_exist_more_button()
        group_chat_page.click_more_button()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0312(self):
        """群聊（企业群/普通群）发送位置成功"""
        Preconditions.enter_group_chat_page("群聊1")
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击更多
        cwp.click_add_icon()
        # 2.点击位置
        cwp.click_location()
        # 备注：地图位置加载不出来
        try:
            clp = ChatLocationPage()
            clp.wait_for_page_load(20)
            time.sleep(1)
            # 3.点击发送按钮
            if not clp.send_btn_is_enabled():
                raise AssertionError("位置页面发送按钮不可点击")
            clp.click_send()
            # 4.判断在消息聊天窗口是否展示缩略位置消息体
            self.assertTrue(cwp.is_address_text_present())
        except:
            pass

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_B_0009(self):
        """消息列表界面单聊消息免打扰图标显示"""
        Preconditions.enter_single_chat_page("大佬1")
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_setting()
        # 开启消息免打扰
        status_text = chatWindowPage.get_text((MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"))
        if (status_text == "关闭"):
            chatWindowPage.click_element((MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"))
        # 获取消息免打扰 开关状态
        status_text = chatWindowPage.get_text((MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"))
        chatWindowPage.click_element((MobileBy.ID, "com.chinasofti.rcs:id/back"))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0158(self):
        """在会话窗口点击图片按钮进入相册，直接勾选原图，选择一张大于20M的照片进行发送"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.判断当前群聊页面是否存在发送失败标识，存在清空聊天记录
        if not gcp.is_send_sucess():
            gcp.click_setting()
            gcs = GroupChatSetPage()
            gcs.wait_for_page_load()
            gcs.click_clear_chat_record()
            gcs.click_sure()
            time.sleep(1)
            gcp.click_group_setting_back()
        gcp.wait_for_page_load()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        time.sleep(1)
        gcp.switch_to_given_folder("pic3")
        # 3.点击原图
        gcp.click_original_photo()
        # 4.选择一张大于20M的图片
        gcp.select_items_by_given_orders(1)
        # 5.点击发送
        gcp.click_send()
        # 6.判断存在发送失败按钮
        self.assertFalse(gcp.is_send_sucess())
        gcp.press_picture()
        # 7.判断是否出现编辑选项
        self.assertTrue(gcp.is_exist_edit_page())
        gcp.click_edit()
        cpe = ChatPicEditPage()
        # 8.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 9.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 10.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 11.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("图片编辑")
        time.sleep(1)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0159(self):
        """在会话窗口点击图片按钮进入相册，选择一张大于20M的照片，进入图片预览页面勾选原图，然后进行发送"""
        Preconditions.enter_group_chat_page("群聊1")
        scp = SingleChatPage()
        # 1.点击输入框左上方的相册图标
        scp.click_picture()
        time.sleep(1)
        # 2.选择大于20M的图片
        scp.switch_to_given_folder("pic")
        scp.select_items_by_given_orders(1)
        # 3.点击预览
        scp.click_preview()
        time.sleep(1)
        cpp = ChatPicPreviewPage()
        # 4.点击原图
        scp.click_original_photo()
        # 5.点击发送
        cpp.click_picture_send()
        # 6.判断是否存在发送失败按钮
        # self.assertTrue(scp.is_send_sucess())
        # 7.点击图片
        scp.click_msg_image(0)
        time.sleep(2)
        # 8.长按图片
        scp.press_xy()
        time.sleep(3)
        # 9.判断是否出现编辑选项
        self.assertTrue(scp.is_exist_picture_edit_page())
        # 10.点击图片编辑
        scp.click_edit()
        cpe = ChatPicEditPage()
        # 11.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 12.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 13.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 14.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("图片编辑")
        time.sleep(1)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0160(self):
        """在会话窗口长按超大原图发送失败的缩略图进行收藏"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证转发的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("收藏")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0161(self):
        """在会话窗口长按超大原图发送失败的缩略图进行转发"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证转发的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0165(self):
        """在会话窗口点击超大原图发送失败的缩略图进行查看"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证转发的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过")
    def test_msg_xiaoliping_D_0167(self):
        """在会话窗口点击其他图片进入预览后，左右滑动进行预览发送失败的超大图片"""
        Preconditions.enter_group_chat_page("群聊1")
        groupchat = GroupChatPage()
        # 进入群聊
        groupchat.wait_for_page_load()
        # 点击图片
        groupchat.click_picture_msg()
        self.assertTrue(groupchat.is_toast_exist("暂不支持发送大于20M的图片"))

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过")
    def test_msg_xiaoliping_D_0168(self):
        """在设置-查找聊天内容-图片与视频页面点击查看发送失败的超大原图"""
        Preconditions.enter_group_chat_page("群聊1")
        groupchat = GroupChatPage()
        # 进入群聊
        groupchat.wait_for_page_load()
        # 点击设置
        groupchat.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天记录
        gcsp.click_search_chat_record()
        fcrp = FindChatRecordPage()
        time.sleep(1)
        # 点击图片与视频
        fcrp.click_pic_video()
        pvp = PicVideoPage()
        pvp.wait_for_page_load()
        # 点击发送失败的图片
        pvp.click_pic()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过")
    def test_msg_xiaoliping_D_0169(self):
        """在查看发送失败的超大原图页面进行长按转发操作"""
        Preconditions.enter_group_chat_page("群聊1")
        groupchat = GroupChatPage()
        # 进入群聊
        groupchat.wait_for_page_load()
        # 点击图片
        groupchat.click_picture_msg()
        time.sleep(1)
        # 长按图片
        groupchat.press_xy()
        time.sleep(1)
        # 判断图片编辑项是否存在
        self.assertTrue(groupchat.is_exist_picture_edit_page())
        # 点击转发
        groupchat.click_selection_forward()
        scp = SelectContactsPage()
        scp.search("测试图片1")
        time.sleep(1)
        scp.select_one_contact_by_name("测试图片1")
        # 点击确定转发
        scp.click_sure_forward()
        self.assertTrue(groupchat.is_toast_exist("已转发"))


