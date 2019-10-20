import unittest
import warnings

from selenium.common.exceptions import TimeoutException

from pages.me.MeCallMulti import MeCallMultiPage
from pages.me.MeViewUserProfile import MeViewUserProfilePage

from pages.message.Send_CardName import Send_CardNamePage
import random
from pages.components import ChatNoticeDialog, ContactsSelector, BaseChatPage
from pages.call.multipartycall import MultipartyCallPage
from pages.message.FreeMsg import FreeMsgPage
import os
import time

from appium.webdriver.common.mobileby import MobileBy
from dataproviders import contact2
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
    def public_send_location():
        """发送位置信息"""
        scp = SingleChatPage()
        scp.click_more()
        time.sleep(1)
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 点击发送按钮
        if not location_page.send_btn_is_enabled():
            raise AssertionError("位置页面发送按钮不可点击")
        location_page.click_send()
        scp.click_more()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ateam" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_set_chart_group_file(file_type):
        """确保群聊已经发送一个文件信息，且已收藏"""
        Preconditions.enter_group_chat_page("群聊1")
        # 1.点击更多位置信息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
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
        # 3.点击该信息收藏
        scp.press_file_to_do(file_type, "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        cmp.click_back()

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


class MsgAllPrior(TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 2:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                Preconditions.ensure_have_enterprise_group()
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

        # 确保测试手机有resource文件夹
        name = "群聊1"
        Preconditions.get_into_group_chat_page(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        local_file.push_preset_file()
        local_file.click_back()
        csfp.wait_for_page_load()
        csfp.click_back()
        gcp.wait_for_page_load()

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
    def test_msg_weifenglian_1V1_0130(self):
        """对自己发送出去的文件消息进行十秒内撤回"""
        Preconditions.enter_single_chat_page("大佬3")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        if scp.is_exist_msg_file():
            pass
        else:
            scp = SingleChatPage()
            scp.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            scp.wait_for_page_load()
        # 长按xls文件
        ChatFilePage().de_file('.xlsx')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0131(self):
        """对自己发送出去的文件消息进行收藏"""
        Preconditions.enter_single_chat_page("大佬3")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        if scp.is_exist_msg_file():
            pass
        else:
            scp = SingleChatPage()
            scp.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            scp.wait_for_page_load()
        # 长按xls文件
        ChatFilePage().collection_file('.xlsx')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0202(self):
        """在收藏列表中打开视频文件"""
        Preconditions.make_already_set_chart_group_file(".mp3")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0203(self):
        """在收藏列表中打开音频文件"""
        Preconditions.make_already_set_chart_group_file(".mp3")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0204(self):
        """在收藏列表中打开图片文件"""
        Preconditions.make_already_set_chart_group_file(".jpg")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0205(self):
        """在收藏列表中打开文本文件"""
        Preconditions.make_already_set_chart_group_file(".ppt")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0206(self):
        """在收藏页面打开幻灯片格式为.ppt .pptx"""
        Preconditions.make_already_set_chart_group_file(".ppt")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0207(self):
        """在收藏页面打开表格格式为.xls  .xlsx"""
        Preconditions.make_already_set_chart_group_file(".xlsx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0208(self):
        """在收藏页面打开文件PDF格式为.pdf"""
        Preconditions.make_already_set_chart_group_file(".pdf")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0226(self):
        """选择其中一文件"""
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")

    def public_enter_file_select_page(self, n=6):
        group_chat_page = GroupChatPage()
        group_chat_page.set_network_status(n)
        group_chat_page.click_file()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0228(self):
        """发送文件"""
        self.public_enter_file_select_page()
        file = ChatSelectLocalFilePage()
        file.select_file('.xlsx')
        self.assertTrue(file.check_element_is_exist('文件显示大小'))
        self.assertTrue(file.check_element_is_enable('发送'))
        file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().check_message_resend_success())
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0362(self):
        """单聊发送位置成功"""
        Preconditions.enter_single_chat_page("大佬1")
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
    def test_msg_weifenglian_1V1_0369(self):
        """将自己发送的位置转发到群"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个普通群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        normal_names = []
        for name in names:
            if '企业' not in name:
                normal_names.append(name)
        normal_name = random.choice(normal_names)
        if normal_name:
            sogp.select_one_group_by_name(normal_name)
            # 3、点击确定
            sogp.click_sure_forward()
            flag = gcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            raise AssertionError("需要创建普通群")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0370(self):
        """将自己发送的位置转发到群"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个普通群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        normal_names = []
        for name in names:
            if '企业' not in name:
                normal_names.append(name)
        normal_name = random.choice(normal_names)
        if normal_name:
            sogp.select_one_group_by_name(normal_name)
            # 3、点击确定
            sogp.click_sure_forward()
            flag = gcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            raise AssertionError("需要创建普通群")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0336(self):
        """将自己发送的位置转发到个人联系人"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择手机联系人
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_search_box()
        # 3.在搜索框输入多种字符点击搜索到的手机联系人
        slcp.search_and_select_contact("大佬1")
        gcp.wait_for_page_load()
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0369(self):
        """将自己发送的位置转发到我的电脑"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择手机联系人
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_search_box()
        # slcp.search_and_select_contact("我的电脑")
        # gcp.wait_for_page_load()
        # if not gcp.is_on_this_page():
        #     raise AssertionError("当前页面不在群聊页面")
        # time.sleep(1)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0370(self):
        """将自己发送的位置转发到最近聊天"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        SelectContactsPage().wait_for_page_load()
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的文件时，没有‘已转发’提示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0373(self):
        """对自己发送出去的位置消息进行删除"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("删除")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0374(self):
        """对自己发送出去的位置消息进行十秒内撤回"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("撤回")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0375(self):
        """对自己发送出去的位置消息进行收藏"""
        Preconditions.enter_group_chat_page("群聊1")
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("收藏")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_B_0007(self):
        """进入免费/发送短信--选择联系人页面"""
        mess = MessagePage()
        mess.click_add_icon()
        # 2.点击免费/发送短信
        mess.click_free_sms()
        # 首次进入会弹出“欢迎使用免费短信”/“欢迎使用短信”弹框，点击确定后直接进入联系人选择器，
        # 非首次进入的直接进入联系人选择器
        try:
            time.sleep(1)
            mess.page_should_contain_text("欢迎使用免费短信")
            mess.click_text("确定")
        except:
            pass
        # 3.查看页面展示
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0191(self):
        """转发默认选中项（1条）—删除"""
        mess = MessagePage()
        Preconditions.enter_single_chat_page("大佬1")
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息

        if not single.is_text_present('测试一个删除'):
            single.input_text_message("测试一个删除")
            single.send_text()
        single.press_mess("测试一个删除")
        single.click_multiple_selection()
        time.sleep(2)
        group_chat = GroupChatPage()
        # 勾选消息时校验页面元素
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('已选择')
        self.assertTrue(group_chat.is_exist_multiple_selection_count())
        self.assertTrue(group_chat.is_enabled_multiple_selection_delete())
        self.assertTrue(group_chat.is_enabled_multiple_selection_forward())
        group_chat.click_multiple_selection_delete()
        group_chat.click_multiple_selection_delete_sure()
        mess.is_toast_exist('删除成功')
        mess.page_should_not_contain_text('测试一个删除')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0212(self):
        """删除选中的消息体"""
        mess = MessagePage()
        Preconditions.enter_single_chat_page("大佬1")
        single = SingleChatPage()
        single.input_text_message("测试一个删除1")
        single.send_text()
        single.input_text_message("测试一个删除2")
        single.send_text()
        single.press_mess("测试一个删除1")
        single.click_multiple_selection()
        time.sleep(2)
        group_chat = GroupChatPage()
        # 勾选消息时校验页面元素
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('已选择')
        self.assertTrue(group_chat.is_exist_multiple_selection_count())
        self.assertTrue(group_chat.is_enabled_multiple_selection_delete())
        self.assertTrue(group_chat.is_enabled_multiple_selection_forward())
        group_chat.get_check_all_not_selected()
        group_chat.click_multiple_selection_delete()
        group_chat.click_multiple_selection_delete_sure()
        mess.is_toast_exist('删除成功')
        mess.page_should_not_contain_text('测试一个删除1')
        mess.page_should_not_contain_text('测试一个删除2')

    # @tags('ALL', 'SMOKE', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过")
    def test_msg_huangcaizui_A_0260(self):
        """消息送达状态显示开关入口"""
        # 打开‘我’页面
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

    # @tags('ALL', 'SMOKE', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过")
    def test_msg_huangcaizui_A_0261(self):
        """关闭送达状态显示"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0273(self):
        """从全局搜索中搜索号码进入单聊"""
        Preconditions.enter_single_chat_page("大佬1")
        single = SingleChatPage()
        single.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0274(self):
        """从新建消息进入单聊"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name("大佬1")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0275(self):
        """从发送短信进入单聊"""
        mess = MessagePage()
        # Step 1.点击右上角“+”
        mess.click_add_icon()
        # Step 2.点击发送短信
        mess.click_free_sms()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.wait_is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            CallPage().wait_for_freemsg_load()
        select_page = SelectContactPage()
        # Checkpoint 进入联系人选择器（直接选择本地通讯录联系人)
        select_page.is_exist_select_contact_btn()
        # Checkpoint 进入联系人选择器（可在搜索框输入联系人姓名或电话号码搜索)
        select_page.is_exist_selectorinput_toast()
        # Checkpoint 进入联系人选择器（选择团队联系人)
        select_page.is_exist_selectortuandui_toast()
        # Step 3.任意选择一联系人
        ContactsSelector().click_local_contacts('给个红包1')
        # Checkpoint 进入短信编辑页面
        freemsg.wait_is_exist_wenhao()
        freemsg.wait_is_exist_exit()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0289(self):
        """单聊/群聊会话页面点击名片进入单聊页面"""
        mess = MessagePage()
        Preconditions.enter_single_chat_page("给个红包3")
        SingleChatPage().click_more()
        mess.click_text_or_description('名片')
        SelectContactsPage().select_one_contact_by_name("a a")
        send_card = Send_CardNamePage()
        send_card.click_share_btn()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0021(self):
        """验证编辑短信不发送，再次进入是否可以再次编辑"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        SelectContactsPage().select_one_contact_by_name("给个红包4")
        singe_chat = SingleChatPage()
        chatdialog = ChatNoticeDialog()
        singe_chat.input_sms_message("测试前一半")
        # 点击退出短信按钮
        singe_chat.click_exit_sms()
        # 点击短信按钮
        singe_chat.click_sms()
        # 判断是否有之前输入的内容
        chatdialog.page_should_contain_text('测试前一半')
        singe_chat.edit_clear("测试前一半")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0022(self):
        """验证非首次发送短信出去没有短信资费弹框"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        SelectContactsPage().select_one_contact_by_name("给个红包4")
        singe_chat = SingleChatPage()
        chatdialog = ChatNoticeDialog()
        singe_chat.input_sms_message("发送第一条")
        # 点击发送短信
        singe_chat.send_sms()
        # # 判断弹出资费提醒提示框
        # chatdialog.page_should_contain_text('资费提醒')
        # # 点击发送
        # mess.click_element_by_text('发送')
        # singe_chat.input_sms_message("发送第二条")
        # # 点击发送短信
        # singe_chat.send_sms()
        # # 判断未弹出资费提醒提示框
        # chatdialog.page_should_not_contain_text('资费提醒')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0025(self):
        """将文本消息转为短信发送"""
        Preconditions.enter_single_chat_page("大佬3")
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        # 长按通过短信发送
        single.send_for_sms('测试一个呵呵')
        # 判断控件存在
        single.is_present_sms_fee_remind()
        single.is_exist_send_button()
        single.is_exist_cancel_button()
        # 点击取消按钮
        single.click_cancel()
        # 再次发送
        single.send_for_sms('测试一个呵呵')
        # single.is_present_sms_fee_remind()
        # single.click_send_button()
        # single.page_should_contain_text('测试一个呵呵')
        # single.page_should_contain_text('短信')
        # single.send_for_sms('测试一个呵呵')
        # single.page_should_not_contain_text('资费提醒')
        # single.page_should_contain_text('测试一个呵呵')
        # single.page_should_contain_text('短信')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0062(self):
        """免费/发送短信—输入姓名/号码搜索"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        select_page = SelectContactsPage()
        select_page.search('给个红包1')
        time.sleep(2)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 给个红包1')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0063(self):
        """免费/发送短信—输入姓名/号码搜索—查看搜索结果"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        select_page = SelectContactsPage()
        # 按姓名搜索存在联系人
        select_page.search('给个红包1')
        time.sleep(1)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 给个红包1')
        # 按手机号搜索存在联系人
        select_page.search('13800138000')
        time.sleep(1)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 13800138000')
        # 按手机号搜索不存在联系人
        select_page.search('199815')
        time.sleep(1)
        mess.page_should_not_contain_text('手机联系人')
        mess.page_should_contain_text('搜索团队联系人 : 199815')
        # 无手机联系人且搜索手机号时
        select_page.search('19981512581')
        time.sleep(1)
        mess.page_should_contain_text('网络搜索')
        mess.page_should_contain_text('搜索团队联系人 : 19981512581')
        select_page.is_present_unknown_member()
        # 搜索我的电脑
        select_page.search('我的电脑')
        time.sleep(1)
        mess.page_should_not_contain_text('手机联系人')
        mess.page_should_contain_text('搜索团队联系人 : 我的电脑')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0004(self):
        """在我的电脑面板点击左上角的返回按钮返回到消息列表页"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("我的电脑")
        # 选择联系人进入联系人页
        SelectContactsPage().select_one_group_by_name("我的电脑")
        mess.click_back_by_android(2)
        mess.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0002(self):
        """搜索框正常弹起和收起"""
        mess = MessagePage()
        mess.click_search()
        time.sleep(2)
        self.assertTrue(current_mobile().is_keyboard_shown())
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/result_wrapper'))
        self.assertFalse(current_mobile().is_keyboard_shown())
        
    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0029(self):
        """已使用过pc版和飞信搜索我的电脑"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("我的电脑")
        # 选择联系人进入联系人页
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 点击进入我的电脑
        SelectContactsPage().select_one_group_by_name("我的电脑")
        # 检查是否进入我的电脑页面
        mess.page_should_contain_text('我的电脑')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0186(self):
        """群二维码详情页——保存二维码"""
        # 1、网络正常（4G / WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主 / 群成员
        mess = MessagePage()
        Preconditions.enter_group_chat_page("群聊2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # Step 2、等待群聊页面加载
        groupchat.wait_for_page_load()
        # Step 3、进入群聊设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 4、点击下载群二维码
        groupset.click_QRCode()
        groupset.click_qecode_download_button()
        # Checkpoint 弹出toast提示：已保存
        mess.is_toast_exist("已保存")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0188(self):
        """群聊设置页面——进入到群管理详情页"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        # 5、当前群人数为：1
        # 6、android端
        Preconditions.enter_group_chat_page("群聊2")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 1、点击群管理，进入到群管理详情页
        gcs.click_group_manage()
        gcs.wait_for_group_manage_load()
        # 2、点击群主管理权转让，会弹出toast提示：暂无群成员并且停留在当前页
        gcs.click_group_manage_transfer_button()
        self.assertEquals(gcs.is_toast_exist("暂无群成员"), True)
        gcs.wait_for_group_manage_load()
        # 3、点击左上角的返回按钮，可以返回到群聊设置页
        gcs.click_group_manage_back_button()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0197(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        SingleChatPage().send_text_if_not_exist("111")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字搜索条件
        search.search('111')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('111')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0198(self):
        """群聊设置页面——查找聊天内容——英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("AAA")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入英文字母搜索条件
        search.search('AAA')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('AAA')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0199(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("!@#$%")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入英文字母搜索条件
        search.search('!@#$%')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('!@#$%')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0201(self):
        """群聊设置页面，查找聊天内容——空格搜索"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        SingleChatPage().send_text_if_not_exist("呵呵  呵呵")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入空格搜索条件
        search.search(' ')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('呵呵  呵呵')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0203(self):
        """群聊设置页面——查找聊天内容——数字+汉字+英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        SingleChatPage().send_text_if_not_exist("呵呵111AAA")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字+汉字+英文作为搜索条件
        search.search('呵呵111AAA')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('呵呵111AAA')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0204(self):
        """群聊设置页面——查找聊天内容——数字+汉字+英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字+汉字+英文作为搜索条件
        search.search('呵呵22BB')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0205(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字+汉字+英文作为搜索条件
        search.search('吉吉娃')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0206(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.enter_group_chat_page("群聊2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字作为搜索条件
        search.search('112233')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0179(self):
        """分享群二维码到——选择最近聊天"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主/群成员
        Preconditions.enter_group_chat_page("群聊2")

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送消息,确保最近聊天中有记录
        gcp.input_text_message("111")
        gcp.send_text()
        time.sleep(2)
        # 解决发送消息后，最近聊天窗口没有记录，需要退出刷新的问题
        gcp.click_back()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，是否会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择最近聊天的联系人或者群聊，会弹出确认弹窗
        scp.select_recent_chat_by_name(group_name)
        time.sleep(1)
        self.assertEquals(gcp.is_text_present("确定"), True)
        # 3、点击取消，会关闭弹窗，不会自动清除搜索结果
        scp.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(scp.is_exists_recent_chat_by_name(group_name), True)
        scp.select_recent_chat_by_name(group_name)
        # 4、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        scp.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0195(self):
        """群聊设置页面——查找聊天内容"""
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        Preconditions.enter_group_chat_page("群聊2")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        text = "12345"
        gcp.input_text_message(text)
        gcp.send_text()
        time.sleep(2)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.search(text)
        # 1、点击聊天内容入口，跳转到聊天内容页面
        gcf.select_message_record_by_text(text)
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        gcf.wait_for_page_load()
        # 2、点击顶部的搜索框，调起小键盘
        gcf.click_search_box()
        self.assertEquals(gcf.is_keyboard_shown(), True)
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0196(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示"""
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        Preconditions.enter_group_chat_page("群聊2")
        SingleChatPage().send_text_if_not_exist("虎虎")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字搜索条件
        search.search('虎虎')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('虎虎')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0163(self):
        """群主——清除旧名片——录入29个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("aaaaaaaaaaaaaaaaaaaiiiiiiiii")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0164(self):
        """群主——清除旧名片——录入30个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("aaaaaaaaaaaaaaaaaaaaiiiiiiiii")
        gcsp.save_group_card_name()
        
    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0165(self):
        """群主——清除旧名片——录入31个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("aaaaaaaaaaaaaaaaaaaaiiiiiiiii")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0166(self):
        """群主——清除旧名片——录入1个数字"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("1")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0167(self):
        """群主——清除旧名片——录入10个数字"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("1234567890")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0168(self):
        """群主——清除旧名片——录入30个数字"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("12345678901234567890123456780")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0169(self):
        """群主——清除旧名片——录入31个数字"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("123456789012345678901234567890")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0170(self):
        """群主——清除旧名片——录入汉字+字母+数字"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("哈bbb123")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0297(self):
        """通话记录详情页：一键建群，网络正常可建群成功"""
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1", "大佬2")
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        # callpage = CallPage()
        # callpage.hang_up_hefeixin_call_631()
        #
        # # Checkpoint：拨打的通话记录为多方电话 进入通话详情页，标题为多方电话通话类型
        # callpage.is_type_hefeixin(0, '飞信电话')
        # # 进入详情页
        # time.sleep(3)
        # callpage.click_ganggang_call_time()
        # # Checkpoint：查看详情页面是否是多方电话？
        # callpage.is_hefeixin_page('飞信电话')
        #
        # # 点击‘一键建群’
        # callpage.click_onekey_build_group()
        # # checkpoint : 删除原有的“群聊”，重新输入群聊名称
        # buildgroup = BuildGroupChatPage()
        # buildgroup.create_group_chat('新群聊')
        # # Checkpoint：群聊创建成功、跳转到群聊窗口
        # time.sleep(2)
        # groupchat = GroupChatPage()
        # self.assertTrue(groupchat.is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0300(self):
        """大陆用户实现自动接听的号码：12560结尾的长度不超过9位的号码"""
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬3")
        selectcontacts.click_contact_by_name("大佬3")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        callpage = CallPage()
        # 挂断和飞信电话
        # callpage.hang_up_hefeixin_call_631()
        # # 1.2 Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        # callpage.is_type_hefeixin(0, '飞信电话')
        # # 进入详情页
        # time.sleep(3)
        # callpage.click_ganggang_call_time()
        # # 查看详情页面是否是飞信电话？
        # callpage.is_hefeixin_page('飞信电话')
        # # 返回到通话页面
        # callpage.click_lefticon_back()
        # # 2.1 选择联系人发起多方电话
        # callcontact.click_free_call()
        # # 2.2选择指定联系人 发起多方电话呼叫
        # selectcontacts = SelectContactsPage()
        # selectcontacts.search("大佬3")
        # selectcontacts.click_contact_by_name("大佬3")
        # selectcontacts.search("大佬4")
        # selectcontacts.click_contact_by_name("大佬4")
        # time.sleep(4)
        # selectcontacts.click_sure_bottom()
        # time.sleep(1)
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 挂断多方电话
        # callpage.hang_up_hefeixin_call_631()
        # # 2.2 Checkpoint：拨打的通话记录为多方电话 进入通话详情页，标题为多方通话类型
        # callpage.is_type_hefeixin(0, '飞信电话')
        # # 进入详情页
        # time.sleep(3)
        # callpage.click_ganggang_call_time()
        # # 查看详情页面是否是多方电话？
        # callpage.is_hefeixin_page('飞信电话')
        # # 返回到通话页面
        # callpage.click_lefticon_back()
        # # 3.1进入‘我-多方电话可用时长’页面
        # callpage.open_me_page()
        # # 进入多方电话可用时长，查看页面展示是否正常
        # mepage = MeCallMultiPage()
        # mepage.click_mutilcall_manage_631()
        # time.sleep(2)
        # # checkpoint；判断当前页面是否在飞信电话管理
        # result = mepage.is_mutil_call_manage_631()
        # self.assertTrue(result)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0351(self):
        """拨号方式选择优先使用和飞信电话拨号盘拨打以和飞信电话呼出"""
        mepage = MePage()
        mepage.open_me_page()
        # 点击‘设置’
        mepage.click_setting_menu()
        # 进入拨号设置 并选择'优先使用和飞信电话（免费）'
        meset = MeSetUpPage()
        meset.click_call_setting('总是询问（默认）')
        # # 返回到‘我’页面
        # meset.click_back()
        # meset.click_back()
        # meset.click_back()
        #
        # # 进入通话页面。跳过相关引导页
        # Preconditions.enter_call_page()
        # # 点击拨号键，输入号码并拨打'
        # callpage = CallPage()
        # callpage.click_call()
        # callpage.dial_number('18311111111')
        # time.sleep(2)
        # # 直接呼叫
        # callpage.click_call_phone()
        # # checkpoint：出现拨号方式选择界面
        # calltypeselect = CallTypeSelectPage()
        # time.sleep(2)
        # self.assertTrue(calltypeselect.is_calltype_selectpage_display_631())
        # # Checkpoint2：出现‘设置为默认’
        # self.assertTrue(calltypeselect.is_setting_default_display())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0353(self):
        """拨号方式选择优先使用和飞信电话拨号盘拨打以和飞信电话呼出"""
        mepage = MePage()
        # 进入通话页面。跳过相关引导页
        Preconditions.enter_call_page()
        # 点击拨号键，输入号码并拨打'
        callpage = CallPage()
        callpage.click_call()
        callpage.dial_number('18311111111')
        time.sleep(2)
        # 直接呼叫
        callpage.click_call_phone()
        # time.sleep(2)
        # # checkpoint：出现拨号方式选择界面
        # calltypeselect = CallTypeSelectPage()
        # self.assertTrue(calltypeselect.is_calltype_selectpage_display_631())
        # # Checkpoint2：出现‘设置为默认’,点击设置为默认
        # self.assertTrue(calltypeselect.is_setting_default_display())
        # calltypeselect.click_setting_default()
        # # Checkpoint3：出现‘可在我-设置-拨号设置”中修改’
        # calltypeselect.is_toast_exist('可前往“我-设置-拨号设置”中修改')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0357(self):
        """拨号方式选择优先使用和飞信电话拨号盘拨打以和飞信电话呼出"""
        mepage = MePage()
        mepage.open_me_page()
        # 点击‘设置’
        mepage.click_setting_menu()
        # 进入拨号设置 并选择'优先使用和飞信电话（免费）'
        meset = MeSetUpPage()
        meset.click_call_setting('优先使用飞信电话（免费）')
        # 返回到‘我’页面
        meset.click_back()
        meset.click_back()
        meset.click_back()

        # 进入通话页面。跳过相关引导页
        Preconditions.enter_call_page()
        # 点击拨号键，输入号码并拨打'
        callpage = CallPage()
        callpage.click_call()
        callpage.dial_number('18311111111')
        time.sleep(2)
        # checkpiont1: 不用选择拨号方式，直接呼叫
        callpage.click_call_phone()
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact = CalllogBannerPage()
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        # callpage.hang_up_hefeixin_call_631()
        #
        # # Checkpoint2：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信电话通话类型
        # callpage.is_type_hefeixin(0, '飞信电话')
        # # checkpiont3: 进入详情页
        # time.sleep(3)
        # callpage.click_ganggang_call_time()
        # # Checkpoint4：查看详情页面是否是和飞信电话？
        # callpage.is_hefeixin_page('飞信电话')
        # time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0374(self):
        """非首次拨打多方电话显示多方电话会控页（去掉原浮层提示），发起后不再放音，缩短呼叫等待时间"""
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬3", "大佬4")
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        time.sleep(2)
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在去掉设置悬浮框提示
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 判断当前是否在系统通话界面 是的话 挂断系统电话
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        time.sleep(2)
        callpage.hang_up_the_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0390(self):
        """非首次拨打多方电话显示多方电话会控页（去掉原浮层提示），发起后不再放音，缩短呼叫等待时间"""
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬3")
        selectcontacts.click_contact_by_name("大佬3")
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # checkpoint1: 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        callpage = CallPage()
        # 挂断和飞信电话
        # 判断当前是否在系统通话界面 是的话 挂断系统电话
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        time.sleep(2)
        callpage.hang_up_the_call()
        # Checkpoint2：拨打的通话记录为和飞信电话 进入通话详情页，标题为和飞信通话类型
        time.sleep(2)
        callpage.is_type_hefeixin(0, '飞信电话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0391(self):
        """会控页未创建会场成功时（12560未回呼）会控置灰文案"""
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬3")
        selectcontacts.click_contact_by_name("大佬3")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        if grantpemiss.is_exist_allow_button():
            grantpemiss.allow_contacts_permission()
        # checkpoint1: 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # checkpoint2: 会控页存在文字‘请先接听来电，随后将自动呼叫对方’
        multiparty = MultipartyCallPage()
        # multiparty.assert_accepttips_is_display()
        #
        # # 判断当前是否在系统通话界面 是的话 挂断系统电话
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # time.sleep(2)
        # callpage.hang_up_the_call()
        # time.sleep(2)
        # # Checkpoint2：拨打的通话记录为和飞信电话 进入通话详情页，标题为和飞信通话类型
        # callpage.is_type_hefeixin(0, '飞信电话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0024(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标.不选择照片，直接点击发送按钮"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击发送图片
        cwp.click_img_msgs()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 不选择照片，判断发送按钮是否可点击
        self.assertFalse(cpp.send_btn_is_enabled())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0025(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2.选择一张照片，点击发送按钮"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击发送图片
        cwp.send_img_msgs({"pic": (1,)})
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0026(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2.选择一张照片，点击左下角的预览按钮"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击发送图片
        cwp.click_img_msgs()
        # 选择图片 选择预览
        cwp.switch_to_given_folder("pic")
        cwp.select_items_by_given_orders(1)
        cwp.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0027(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2.选择一张照片，点击左下角的预览按钮 3.直接点击发送按钮"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击发送图片
        cwp.click_img_msgs()
        # 选择图片 选择预览
        cwp.switch_to_given_folder("pic")
        cwp.select_items_by_given_orders(1)
        cwp.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 点击发送
        cppp.click_send()
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0028(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2.选择多张照片，点击左下角的预览按钮 3.查看发送按钮数字"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击发送图片
        cwp.click_img_msgs()
        # 选择图片 选择预览
        cwp.switch_to_given_folder("pic")
        cwp.select_items_by_given_orders(1, 2, 3)
        cwp.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 判断发送按钮数字与选择图片数是否一致
        self.assertTrue(cppp.check_send_number(3))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0036(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2、选择2张照片后，点击左下角的预览按钮"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击发送图片
        cwp.click_img_msgs()
        # 选择图片 选择预览
        cwp.switch_to_given_folder("pic")
        cwp.select_items_by_given_orders(1, 2)
        cwp.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 判断是否在预览界面
        self.assertTrue(cppp.is_on_gallery_page())
        # 判断编辑按钮是否存在
        self.assertTrue(cppp.is_exist_edit())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0037(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2.选择9张图片，点击发送"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 选择图片 选择预览
        index = []
        for i in range(9):
            index.append(i + 1)
        cwp.send_img_msgs({"pic": set(index)})
        cwp.wait_for_msg_send_status_become_to("发送成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0038(self):
        """1、在当前聊天会话页面，点击输入框左上方的相册图标 2.选择9张图片，点击发送"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击图片
        cwp.click_img_msgs()
        cwp.switch_to_given_folder("pic")
        # 选择10张图片
        for i in range(10):
            cwp.select_items_by_given_orders(i+1)
        self.assertTrue(cwp.is_toast_exist("最多只能选择9张照片"))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0039(self):
        """我的电脑会话页面，同时发送相册中的图片和视屏"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 选择图片
        cwp.click_img_msgs()
        time.sleep(1)
        index = [5, 6]
        for i in index:
            cwp.select_items_by_given_orders(i)
        # self.assertTrue(cwp.is_toast_exist("不能同时选择照片和视频"))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0040(self):
        """1、在当前聊天会话页面，点击富媒体行拍照图标、拍摄照片，点击“√”"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 选择拍照
        cwp.click_photo()
        time.sleep(1)
        cpp = ChatPhotoPage()
        # 拍照并发送
        cpp.take_photo()
        cpp.send_photo()
        time.sleep(1)
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0044(self):
        """1、在当前聊天会话页面，点击富媒体行拍照图标 2、打开照相机，点击“∨”"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 选择拍照
        cwp.click_photo()
        time.sleep(1)
        cpp = ChatPhotoPage()
        # 返回
        cpp.take_photo_back()
        time.sleep(1)
        self.assertTrue(cwp.is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0045(self):
        """1、在当前聊天会话页面，点击富媒体行拍照图标 2、打开照相机，点击“返回图标”"""
        mess = MessagePage()
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 选择拍照
        cwp.click_photo()
        time.sleep(1)
        cpp = ChatPhotoPage()
        # 返回
        cpp.take_photo_back()
        time.sleep(1)
        self.assertTrue(cwp.is_on_this_page())
