import time
import random
import warnings
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage, SelectHeContactsPage, WorkbenchPage, CreateTeamPage
from pages import ChatFilePage
from pages import ChatLocationPage
from pages import ChatMorePage
from pages import ChatSelectFilePage
from pages import ChatSelectLocalFilePage
from pages import ChatWindowPage
from pages import CreateGroupNamePage
from pages import FindChatRecordPage
from pages import GroupChatPage
from pages import GuidePage
from pages import MeCollectionPage
from pages import MePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import SelectContactsPage
from pages import SelectLocalContactsPage
from pages import SelectOneGroupPage
from pages import GroupChatSetPage
from pages.contacts import GroupListSearchPage
from pages.contacts.Contacts import ContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import GroupListPage, WorkbenchPreconditions
from preconditions.BasePreconditions import SelectHeContactsDetailPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.click_one_contact(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

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
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
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
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
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

    # @staticmethod
    # def make_sure_group_have_member():
    #     fail_time = 5
    #     Preconditions.make_already_in_message_page()
    #     while fail_time:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
    #             Preconditions.create_he_contacts(contact_names)
    #             contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
    #                               ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
    #             Preconditions.create_he_contacts2(contact_names2)
    #             fail_time = 0
    #         except:
    #             fail_time -= 1
    #     Preconditions.make_already_in_me_all_page()

    @staticmethod
    def create_team_select_contacts(team_name):
        """创建团队并添加指定名字联系人为团队成员"""
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_create_team()
        team = CreateTeamPage()
        team.wait_for_page_load()
        team.input_team_name(team_name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name("admin")
        # 立即创建团队
        team.click_immediately_create_team()
        # 点击完成设置工作台
        team.wait_for_setting_workbench_page_load()
        team.click_finish_setting_workbench()
        team.wait_for_create_team_success_page_load()
        # 点击邀请成员
        team.click_invite_member()
        time.sleep(3)
        osp = OrganizationStructurePage()
        osp.click_text("从手机通讯录添加")
        time.sleep(2)
        sc = SelectContactsPage()
        slc = SelectLocalContactsPage()
        # 选择联系人加入团队
        slc.wait_for_page_load()
        name_contacts = ["a a", "bb1122",  "大佬1", "给个红包1", "English", "特殊!@$"]
        for name_contact in name_contacts:
            time.sleep(2)
            slc.selecting_local_contacts_by_name(name_contact)
        # 点击确认
        slc.click_sure()
        time.sleep(1)
        #slc.wait_for_page_load()
        osp.click_i_know()
        # 点击取消返回工作台页面
        osp.click_cancle()
        workbench.click_message_icon()

    @staticmethod
    def public_send_location():
        """发送位置信息"""
        gcp = GroupChatPage()
        gcp.click_more()
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
        gcp.wait_for_page_load()
        gcp.click_more()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

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

    # 多人群聊前置条件
    @staticmethod
    def select_one_mobile(moible_param):
        """选择指定的设备连接，并确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        # 消息页面
        Preconditions.make_in_message_page(moible_param, reset=False)

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
    def press_group_file():
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".txt")
            local_file.click_send()
            group_chat_page.wait_for_page_load()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

class MsgGroupChatFileLocationTest(TestCase):
    """
    模块：消息-群聊文件,位置

    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-群聊文件,位置
    """

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        # 创建联系
        # fail_time = 0
        # import dataproviders
        # while fail_time < 3:
        #     try:
        #         required_contacts = dataproviders.get_preset_contacts()
        #         conts = ContactsPage()
        #         Preconditions.connect_mobile('Android-移动')
        #         current_mobile().hide_keyboard_if_display()
        #         Preconditions.make_already_in_message_page()
        #         conts.open_contacts_page()
        #         try:
        #             if conts.is_text_present("发现SIM卡联系人"):
        #                 conts.click_text("显示")
        #         except:
        #             pass
        #         for name, number in required_contacts:
        #             conts.create_contacts_if_not_exits(name, number)
        #         # 创建群
        #         required_group_chats = dataproviders.get_preset_group_chats()
        #         conts.open_group_chat_list()
        #         group_list = GroupListPage()
        #         for group_name, members in required_group_chats:
        #             group_list.wait_for_page_load()
        #             group_list.create_group_chats_if_not_exits(group_name, members)
        #         group_list.click_back()
        #         conts.open_message_page()
        #         return
        #     except:
        #         fail_time += 1
        #         import traceback
        #         msg = traceback.format_exc()
        #         print(msg)

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        scp = GroupChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            # current_mobile().reset_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @staticmethod
    def setUp_test_msg_group_chat_file_location_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0001(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
        2、点击本地文件
        3、不选择文件，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0002(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
        2、点击本地文件
        3、选择任意文件，点击发送按钮"""
        # 选择html文件发送
        Preconditions.public_send_file('.html')

    def tearDown_test_msg_group_chat_file_location_0002(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0003(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
                2、点击视频文件
                3、不选择文件，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击视频选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0004(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击视频按钮
            3、选择任意视频，点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击视频选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        time.sleep(2)
        # 3、选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出视频，则循环6次
        for i in range(6):
            el = local_file.select_file2("视频")
            if el:
                local_file.click_send()
                gcp.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_video()
            time.sleep(1)
        # local_file.click_back()
        # csf.click_back()
        gcp.wait_for_page_load()
        raise AssertionError("There is no video")

    def tearDown_test_msg_group_chat_file_location_0004(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0005(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击照片按钮
            3、不选择照片，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击照片选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0006(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击照片按钮
            3、选择任意照片，点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击照片选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 选择一张照片发送
        local_file = ChatSelectLocalFilePage()
        local_file.wait_for_page_loads()
        el = local_file.select_file2("照片")
        if el:
            local_file.click_send()
            gcp.wait_for_page_load()
        else:
            raise AssertionError("There is no pic")

    def tearDown_test_msg_group_chat_file_location_0006(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0007(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击音乐按钮
            3、不选择音乐，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击音乐选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0008(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击音乐按钮
            3、选择任意音乐，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击音乐选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 选择一个音乐文件发送
        local_file = ChatSelectLocalFilePage()
        local_file.wait_for_page_loads()
        el = local_file.select_file2("音乐")
        if el:
            local_file.click_send()
            gcp.wait_for_page_load()
        else:
            raise AssertionError("There is no music")

    def tearDown_test_msg_group_chat_file_location_0008(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0009(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个群
            3、点击确定"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_select_one_group()

        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        if group_names:
            sog.select_one_group_by_name(group_names[0])
            sog.click_sure_forward()
            if not sog.catch_message_in_page("已转发"):
                raise AssertionError("转发失败")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            time.sleep(1)
        else:
            raise AssertionError("没有群可转发，请创建群")

    def tearDown_test_msg_group_chat_file_location_0009(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0010(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个群
            3、点击取消按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_select_one_group()

        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        if group_names:
            sog.select_one_group_by_name(group_names[0])
            sog.click_cancel_forward()
            sog.wait_for_page_load()
            sog.click_back()
            sc.click_back()
            time.sleep(2)
            if chat_file.is_on_this_page():
                chat_file.click_back()
            search.click_back()
            gcsp.click_back()
            time.sleep(1)
        else:
            raise AssertionError("没有群可转发，请创建群")

    def tearDown_test_msg_group_chat_file_location_0010(self):
        # 删除聊天记录
        scp = GroupChatPage()
        time.sleep(2)
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0013(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个本地通讯录联系人
            3、点击确定"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        time.sleep(3)
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个本地联系人
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.select_local_contacts()
        time.sleep(2)
        # 选择一个联系人
        sc.click_one_contact("和飞信电话")
        # 点击确认转发
        sc.click_sure_forward()
        # 验证转发成功
        if not sc.catch_message_in_page("已转发"):
            raise AssertionError("转发失败")
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0013(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0014(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个本地通讯录联系人
            3、点击取消按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个本地联系人
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.select_local_contacts()
        time.sleep(2)
        sc.click_one_contact("和飞信电话")
        # sc.click_one_local_contacts()
        # 点击取消按钮
        sc.click_cancel_forward()
        # 确保选择联系人页面加载
        sc.wait_for_page_local_contact_load()
        sc.click_back()
        sc.click_back()
        time.sleep(2)
        if chat_file.is_on_this_page():
            chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0014(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0017(self):
        """1、在当前文件列表页面长按任意未下载文件
            2、点击收藏按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按收藏指定类型的文件
        time.sleep(3)
        chat_file.collection_file(".html")
        if not chat_file.is_toast_exist("已收藏"):
            raise AssertionError("收藏验证失败")
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0017(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @staticmethod
    def setUp_test_msg_group_chat_file_location_0018():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        # current_mobile().reset_app()
        current_mobile().launch_app()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_file_location_0018(self):
        """1、在当前文件列表页面长按任意未下载文件
            2、点击收藏按钮
            3、查看我-收藏列表"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按收藏指定类型的文件
        time.sleep(3)
        chat_file.collection_file(".html")
        chat_file.is_toast_exist("已收藏")
        # 返回到消息页面
        time.sleep(2)
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)
        # 返回消息页面过程中删除聊天记录
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(gcp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

        gcp.click_back()
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 跳转到我页面
        me = MePage()
        me.open_me_page()
        # 查看收藏页面
        me.click_collection()
        mcp = MeCollectionPage()
        # 检查刚刚收藏的文件是否存在
        mcp.is_toast_exist(".html")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0019(self):
        """1、在当前文件列表页面长按任意文件
            2、点击删除按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        chat_file.delete_file(".html")
        # 返回群聊天页面
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0040(self):
        """1、在当前群聊天会话页面长按任意文件
            2、点击删除按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 长按刚刚发送的文件删除
        time.sleep(3)
        gcp.press_file_to_do(".html", "删除")
        # 验证删除成功
        time.sleep(3)
        if gcp.is_text_present(".html"):
            raise AssertionError("删除失败")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0041(self):
        """1、在当前群聊天会话页面长按自己十分钟内发送的文件
            2、点击撤回按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        time.sleep(1)
        # 长按刚刚发送的文件撤回
        gcp.press_file_to_do(".html", "撤回")
        time.sleep(2)
        if gcp.is_text_present("我知道了"):
            gcp.click_i_know()
        # 验证撤回成功
        time.sleep(3)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("撤回失败")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0042(self):
        """1、在当前群聊天会话页面长按自己超过十分钟发送的文件
            2、点查看功能菜单"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        # 等待10分钟
        gcp = GroupChatPage()
        # 超过十分钟,长按自己发送的文件撤回，没有撤回菜单按钮
        for i in range(122):
            time.sleep(2)
            text = gcp.driver.page_source
            del text
            time.sleep(3)
            tmp = gcp.driver.current_activity
            del tmp
            print(i)
        gcp.press_file(".html")
        if gcp.is_text_present("撤回"):
            raise AssertionError("超过十分钟可以撤回")
        time.sleep(2)
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    def tearDown_test_msg_group_chat_file_location_0042(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0043(self):
        """1、在当前会话窗口点击位置
            2、点击左上角的返回按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 返回会话窗口
        location_page.click_back()
        gcp.wait_for_page_load()
        gcp.click_more()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0044(self):
        """1、在当前会话窗口点击位置
            2、点击右上角的发送按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
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
        gcp.wait_for_page_load()
        gcp.click_more()
        if not gcp.is_address_text_present():
            raise AssertionError("位置信息发送不成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0045(self):
        """1、在当前会话窗口点击位置
            2、滑动500米内的位置列表，选择其他位置
            3、点击右上角的发送按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 选择其他位置
        location_page.select_other_item()
        # 点击发送按钮
        if not location_page.send_btn_is_enabled():
            raise AssertionError("位置页面发送按钮不可点击")
        location_page.click_send()
        gcp.wait_for_page_load()
        gcp.click_more()
        if not gcp.is_address_text_present():
            raise AssertionError("位置信息发送不成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0046(self):
        """1、在当前会话窗口点击位置
            2、滑动500米内的位置列表，选择其他位置
            3、点击左上角的返回按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 选择其他位置
        location_page.select_other_item()
        # 点击返回
        location_page.click_back()
        gcp.wait_for_page_load()
        gcp.click_more()

    def tearDown_test_msg_group_chat_file_location_0046(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @staticmethod
    def public_send_location():
        """发送位置信息"""
        gcp = GroupChatPage()
        gcp.click_more()
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
        gcp.wait_for_page_load()
        gcp.click_more()
        if not gcp.is_address_text_present():
            raise AssertionError("位置信息发送不成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0047(self):
        """1、长按位置消息体
            2、点击转发按钮
            3、选择任意本地通讯录联系人进行转发"""
        self.public_send_location()
        # 长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if names:
            # slcp.select_one_member_by_name(names[0])
            scp.click_one_contact("和飞信电话")
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            raise AssertionError("WARN: There is no linkman.")

    def tearDown_test_msg_group_chat_file_location_0047(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0049(self):
        """1、长按位置消息体
            2、点击转发按钮
            3、选择任意群转发"""
        self.public_send_location()
        # 长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if names:
            sogp.select_one_group_by_name(names[0])
            # 3、点击确定
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            raise AssertionError("WARN: There is no group.")

    def tearDown_test_msg_group_chat_file_location_0049(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX')
    def test_msg_group_chat_file_location_0050(self):
        """1、在当前页面点击位置消息体
            2、点击右下角按钮"""
        self.public_send_location()
        time.sleep(2)
        # 点击位置消息体
        gcp = GroupChatPage()
        gcp.click_addr_info()
        # 等待页面加载
        gcp.wait_for_location_page_load()
        # 点击右下角按钮
        gcp.click_nav_btn()
        #判断是否有手机导航应用
        if gcp.is_toast_exist("未发现手机导航应用", timeout=3):
            raise AssertionError("未发现手机导航应用")
        map_flag = gcp.is_text_present("地图")
        self.assertTrue(map_flag)
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        gcp.click_location_back()
        time.sleep(2)


    def tearDown_test_msg_group_chat_file_location_0050(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0051(self):
        """1、在当前会话窗口点击自己发送格式为doc的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".doc")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".doc")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0051(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0052(self):
        """1、在当前会话窗口点击自己发送格式为docx的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".docx")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".docx")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0052(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0053(self):
        """1、在当前会话窗口点击自己发送格式为ppt的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".ppt")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".ppt")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0053(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0054(self):
        """1、在当前会话窗口点击自己发送格式为pptx的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".pptx")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".pptx")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0054(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0055(self):
        """1、在当前会话窗口点击自己发送格式为pdf的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".pdf")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".pdf")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0055(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0056(self):
        """1、在当前会话窗口点击自己发送格式为xls的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".xls")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".xls")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0056(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0057(self):
        """1、在当前会话窗口点击自己发送格式为xlsx的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".xlsx")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".xlsx")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0057(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0058(self):
        """1、在当前会话窗口点击自己发送格式为txt的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".txt")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".txt")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0058(self):
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
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0319(self):
        """将自己发送的位置转发到普通群"""
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

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0320(self):
        """将自己发送的位置转发到企业群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个企业群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        sogp.select_one_enterprise_group()
        # 3、点击确定
        sogp.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0321(self):
        """将自己发送的位置转发到普通群时失败"""
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
            sogp.set_network_status(0)
            sogp.click_sure_forward()
            flag = gcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
            # 4、点击返回
            time.sleep(3)
            gcp.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mess = MessagePage()
            mess.wait_for_page_load()
            if not mess.is_iv_fail_status_present():
                raise AssertionError("消息列表没有显示消息发送失败标识")
        else:
            raise AssertionError("需要创建普通群")

    def tearDown_test_msg_weifenglian_qun_0321(self):
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0322(self):
        """将自己发送的位置转发到企业群时失败"""
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_back()
        mess = MessagePage()
        scp = SelectContactsPage()
        if mess.is_on_this_page():
            pass
        else:
            scp.click_back()
        # 1.确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        Preconditions.public_send_location()
        # 2.长按位置消息体转发
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3.点击选择一个企业群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        sogp.select_one_enterprise_group()
        # 4.点击确定
        sogp.set_network_status(0)
        sogp.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")
        # 5.点击返回
        time.sleep(3)
        gcp.click_back()
        scp.wait_for_page_load()
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("消息列表没有显示消息发送失败标识")

    def tearDown_test_msg_weifenglian_qun_0322(self):
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0323(self):
        """"将自己发送的位置转发到普通群时点击取消转发"""
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
            # 3、点击取消
            sogp.click_cancel_forward()
            if not sogp.is_on_this_page():
                raise AssertionError("不是停留在当前选择一个群页面")
        else:
            raise AssertionError("需要创建普通群")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0324(self):
        """"将自己发送的位置转发到企业群时点击取消转发"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个企业群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        sogp.select_one_enterprise_group()
        # 3.点击取消
        sogp.click_cancel_forward()
        if not sogp.is_on_this_page():
            raise AssertionError("不是停留在当前选择一个群页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0325(self):
        """"将自己发送的位置转发到在搜索框输入文字搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('群聊1')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0326(self):
        """将自己发送的位置转发到在搜索框输入英文字母搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("test_group")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0327(self):
        """将自己发送的位置转发到在搜索框输入数字搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("138138138")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0328(self):
        """将自己发送的位置转发到在搜索框输入标点符号搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("；，。")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0329(self):
        """将自己发送的位置转发到在搜索框输入特殊字符搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("&%@")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat',  'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0330(self):
        """将自己发送的位置转发到在搜索框输入空格搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do('转发')
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("a a")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0331(self):
        """将自己发送的位置转发到在搜索框输入多种字符搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("a尼6")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0332(self):
        """将自己发送的位置转发到在搜索框输入多种字符搜索到的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("给个红包1")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0333(self):
        """将自己发送的位置转发到在搜索框粘贴字符搜索到的群"""
        gcp = GroupChatPage()
        # 1.输入群名发送，长按信息并复制
        gcp.input_message("群聊2")
        gcp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("群聊2","复制")
        flag = gcp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("群聊名字复制失败")
        # 2.发送自己的位置
        Preconditions.public_send_location()
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 4.搜索群组
        sogp.click_search_group()
        time.sleep(2)
        # 5.长按搜索框
        sogp.press_group_search_bar()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0334(self):
        """将自己发送的位置转发到搜索到的群时点击取消转发"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        # 2.点击选择一个群
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 3.搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword("群聊1")
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 4.点击返回
            sogp.click_cancel_forward()
            time.sleep(2)
            glsp = GroupListSearchPage()
            if not glsp.is_on_this_page():
                raise AssertionError("当前页面不在搜索群组页面")
        else:
            sogp.page_should_contain_text("无搜索结果")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0335(self):
        """将自己发送的位置转发到滑动右边字母导航栏定位查找的群"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        # 3.根据导航栏的第一个字母定位选择一个群
        sogp.choose_index_bar_click_element()
        # 4.点击确定
        sogp.click_sure_forward()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0337(self):
        """将自己发送的位置转发到手机联系人时点击取消转发"""
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
        names = slcp.get_contacts_name_list()
        name = random.choice(names)
        slcp.selecting_local_contacts_by_name(name)
        # 3.点击取消
        slcp.click_cancel_forward()
        if not slcp.is_on_this_page():
            raise AssertionError("当前页面不在手机联系人页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0338(self):
        """将自己发送的位置转发到手机联系人时发送失败"""
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
        names = slcp.get_contacts_name_list()
        name = random.choice(names)
        if name:
            slcp.selecting_local_contacts_by_name(name)
            slcp.set_network_status(0)
            # 3.点击确认
            slcp.click_sure_forward()
            time.sleep(2)
            if not slcp.is_on_this_page():
                raise AssertionError("当前页面不在手机联系人页面")
            if not gcp.is_on_this_page():
                raise AssertionError("当前页面不在群聊天会话页面")
            # 4.点击返回
            time.sleep(3)
            gcp.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mess = MessagePage()
            mess.wait_for_page_load()
            if not mess.is_iv_fail_status_present():
                raise AssertionError("消息列表没有显示消息发送失败标识")
        else:
            raise AssertionError("需要创建联系人")

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0338():
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0339(self):
        """将自己发送的位置转发到在搜索框输入多种字符搜索到的手机联系人"""
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
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0340(self):
        """将自己发送的位置转发到在搜索框输入数字搜索到的手机联系人"""
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
        # 3.在搜索框输入数字点击搜索到的手机联系人
        slcp.search_and_select_contact("1122")
        gcp.wait_for_page_load()
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0341(self):
        """将自己发送的位置转发到在搜索框输入标点符号搜索到的手机联系人"""
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
        # 3.在搜索框输入标点符号点击搜索到的手机联系人
        slcp.search_and_select_contact("：，。")
        time.sleep(1)
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0342(self):
        """将自己发送的位置转发到在搜索框输入字母搜索到的手机联系人"""
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
        # 3.在搜索框输入字母点击搜索到的手机联系人
        slcp.search_and_select_contact("abc")
        time.sleep(1)
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0343(self):
        """将自己发送的位置转发到在搜索框输入空格搜索到的手机联系人"""
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
        # 3.在搜索框输入含有空格点击搜索到的手机联系人
        slcp.search_and_select_contact("a a")
        time.sleep(1)
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0344(self):
        """将自己发送的位置转发到在搜索框粘贴字符搜索到的手机联系人"""
        gcp = GroupChatPage()
        # 1.输入群名发送，长按信息并复制
        gcp.input_message("大佬1")
        gcp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("大佬1","复制")
        flag = gcp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("群聊名字复制失败")
        # 2.发送自己的位置
        Preconditions.public_send_location()
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3.点击选择手机联系人
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 4.点击搜索框长按粘贴
        slcp.click_search_box()
        slcp.press_search_bar()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0345(self):
        """将自己发送的位置转发到在搜索框输入号码搜索到的手机联系人"""
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
        # 3.在搜索框输入号码点击搜索到的手机联系人
        slcp.search_and_select_contact("012560")
        gcp.wait_for_page_load()
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0346(self):
        """将自己发送的位置转发到在搜索框进行搜索到的手机联系人时取消转发"""
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
        # 3.在搜索框输入手机联系人
        slcp.search_contact("大佬1")
        # 4.点击取消
        slcp.click_cancel_forward()
        if not slcp.is_on_this_page():
            raise AssertionError("当前页面不在选择联系人页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0347(self):
        """将自己发送的位置转发到滑动右边字母导航栏定位查找的手机联系人"""
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
        # 3.根据导航栏的第一个字母定位选择一个群
        slcp.choose_index_bar_click_element()
        # 4.点击确定
        slcp.click_sure_forward()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0348(self):
        """将自己发送的位置转发到滑动右边字母导航栏定位查找的手机联系人时点击取消转发"""
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
        # 3.根据导航栏的第一个字母定位选择一个群
        slcp.choose_index_bar_click_element()
        # 4.点击取消
        slcp.click_cancel_forward()
        if not slcp.is_on_this_page():
            raise AssertionError("当前页面不在选择联系人页面")

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0349():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_contacts()
        contact = ContactsPage()
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        contact.click_text("全部团队")
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        # 确保有这个'测试团队1'并且添加指定联系人
        if contact.is_exist_team_by_name("测试团队1"):
            contact.click_back()
            contact.click_message_icon()
        else:
            contact.click_back()
            contact.click_message_icon()
            Preconditions.create_team_select_contacts("测试团队1")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0349(self):
        """将自己发送的位置转发到团队未置灰的联系人"""
        Preconditions.enter_group_chat_page()
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入多种字符
        shc.input_search("大佬1")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0350(self):
        """将自己发送的位置转发到团队置灰的联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入置灰的联系人
        shc.input_search("admin")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        flag = shc.is_toast_exist("该联系人不可选择")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘该联系人不可选择’提示")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0351(self):
        """将自己发送的位置转发到团队未置灰的联系人时点击取消转发"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入多种字符
        shc.input_search("大佬1")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击取消
        shc.click_cancel_forward()
        if not shc.is_on_this_page():
            raise AssertionError("当前页面不在选择团队联系人页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0352(self):
        """将自己发送的位置转发到团队联系人时发送失败"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入多种字符
        shc.input_search("大佬1")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.断开网络
        shc.set_network_status(0)
        # 7.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        time.sleep(2)
        # 5.点击返回至消息页面
        gcp.click_back()
        scp.wait_for_page_load()
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("消息列表没有显示消息发送失败标识")

    def tearDown_test_msg_weifenglian_qun_0352(self):
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0353(self):
        """将自己发送的位置转发到在企业列表搜索框输入多种字符搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入多种字符
        shc.input_search("给个红包1")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0354(self):
        """将自己发送的位置转发到在企业内搜索框输入多种字符搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入多种字符
        shc.input_search("给个红包1")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0355(self):
        """将自己发送的位置转发到在企业列表搜索框输入数字搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入数字
        shc.input_search("1122")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0356(self):
        """将自己发送的位置转发到在企业内搜索框输入数字搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入数字
        shc.input_search("1122")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0357(self):
        """将自己发送的位置转发到在企业列表搜索框输入标点符号搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入标点符号
        shc.input_search("!")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0358(self):
        """将自己发送的位置转发到在企业内搜索框输入标点符号搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框标点符号
        shc.input_search("!")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0359(self):
        """将自己发送的位置转发到在企业列表搜索框输入字母搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入字母
        shc.input_search("English")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0360(self):
        """将自己发送的位置转发到在企业内搜索框输入英文搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入字母
        shc.input_search("English")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0361(self):
        """将自己发送的位置转发到在企业列表搜索框输入空格搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入含有空格名字
        shc.input_search("a a")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0362(self):
        """将自己发送的位置转发到在企业内搜索框输入空格搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入含有空格名字
        shc.input_search("a a")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0363(self):
        """将自己发送的位置转发到在企业列表搜索框粘贴字符搜索到的团队联系人"""
        gcp = GroupChatPage()
        # 1.输入团队联系人名字发送，长按信息并复制
        gcp.input_message("大佬1")
        gcp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("大佬1", "复制")
        flag = gcp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("团队联系人名字复制失败")
        Preconditions.public_send_location()
        # 2.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.点击搜索：当前组织框
        shc.click_search_box()
        time.sleep(2)
        # 4.长按搜索:当前组织框
        shc.press_search_bar()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0364(self):
        """将自己发送的位置转发到在企业内搜索框粘贴字符搜索到的团队联系人"""
        gcp = GroupChatPage()
        # 1.输入团队联系人名字发送，长按信息并复制
        gcp.input_message("大佬1")
        gcp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("大佬1", "复制")
        flag = gcp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("团队联系人名字复制失败")
        Preconditions.public_send_location()
        # 2.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 4.选择团队
        shc.click_department_name("测试团队1")
        # 5.点击搜索：当前组织框
        shc.click_search_box()
        time.sleep(2)
        # 6.长按搜索:当前组织框
        shc.press_search_bar()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0365(self):
        """将自己发送的位置转发到在企业列表搜索框输入号码搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入号码
        shc.input_search("13800138000")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0366(self):
        """将自己发送的位置转发到在企业内搜索框输入空格搜索到的团队联系人"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入号码
        shc.input_search("13800138000")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0367(self):
        """将自己发送的位置转发到在企业列表搜索框进行搜索到的团队联系人时取消转发"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入团队联系人
        shc.input_search("大佬1")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 5.点击取消
        shc.click_cancel_forward()
        flag = shc.is_on_this_page()
        if not flag:
            raise AssertionError("当前页面不在选择和通讯录联系人页面")

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0377():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_qun_0377(self):
        """将接收到的位置转发到普通群"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击转发
        # 3、点击选择一个群
        # 4、选择任意普通群
        # 5、点击发送按钮
        Preconditions.public_send_location()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.go_to_group_double(group_name)
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_text("选择一个群")
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        sog.click_element_("群聊名")
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0378():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_qun_0378(self):
        """将接收到的位置转发到企业群"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击转发
        # 3、点击选择一个群
        # 4、选择任意企业群
        # 5、点击发送按钮
        Preconditions.public_send_location()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.go_to_group_double(group_name)
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_text("选择一个群")
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword("测试企业群")
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有测试企业群，请创建后重试")
        sog.click_element_("群聊名")
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        mess.click_text("测试企业群")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        Preconditions.delete_record_group_chat()

    # @staticmethod
    # def setUp_test_msg_weifenglian_qun_0386():
    #     """确保有一个多人的群聊"""
    #     Preconditions.select_mobile('Android-移动-移动')
    #     phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
    #     Preconditions.change_mobile('Android-移动')
    #     group_name = Preconditions.get_group_chat_name_double()
    #     flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
    #     if not flag:
    #         Preconditions.change_mobile('Android-移动-移动')
    #         mess = MessagePage()
    #         mess.wait_for_page_load()
    #         mess.click_text("系统消息")
    #         time.sleep(3)
    #         mess.click_text("同意")
    #     Preconditions.change_mobile('Android-移动')
    #     Preconditions.go_to_group_double(group_name)
    #
    # @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    # def test_msg_weifenglian_qun_0386(self):
    #     """将接收到的位置转发到手机联系人"""
    #     # 1、在当前会话窗口长按接收到的位置消息
    #     # 2、点击转发
    #     # 3、点击选择手机联系人
    #     # 4、选择任意联系人
    #     # 5、点击发送按钮
    #     Preconditions.public_send_location()
    #     group_name = Preconditions.get_group_chat_name_double()
    #     Preconditions.change_mobile('Android-移动-移动')
    #     phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
    #     Preconditions.go_to_group_double(group_name)
    #     # 1.长按位置消息体转发
    #     gcp = GroupChatPage()
    #     gcp.wait_for_page_load()
    #     gcp.press_message_to_do("转发")
    #     scp = SelectContactsPage()
    #     scp.wait_for_page_load()
    #     scp.click_text("选择手机联系人")
    #     time.sleep(2)
    #     scp.click_one_contact("飞信电话")
    #     time.sleep(2)
    #     gcp.click_element_("确定移除")
    #     if not gcp.is_toast_exist("已转发"):
    #         raise AssertionError("转发失败")
    #     Preconditions.change_mobile('Android-移动-移动')
    #     mess=MessagePage()
    #     mess.wait_for_page_load()
    #     mess.click_text("飞信电话")
    #     # 验证是否发送成功
    #     cwp = ChatWindowPage()
    #     try:
    #         cwp.wait_for_msg_send_status_become_to('发送成功', 10)
    #     except TimeoutException:
    #         raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
    #     Preconditions.change_mobile('Android-移动-移动')
    #     mess.press_file_to_do("飞信电话","删除聊天")
    #     Preconditions.go_to_group_double(group_name)
    #     Preconditions.delete_record_group_chat()
    #     Preconditions.change_mobile('Android-移动')
    #     Preconditions.go_to_group_double(group_name)
    #     Preconditions.delete_record_group_chat()
    #
    # @staticmethod
    # def setUp_test_msg_weifenglian_qun_0399():
    #     """确保有一个多人的群聊"""
    #     Preconditions.select_mobile('Android-移动-移动')
    #     phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
    #     Preconditions.change_mobile('Android-移动')
    #     group_name = Preconditions.get_group_chat_name_double()
    #     flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
    #     if not flag:
    #         Preconditions.change_mobile('Android-移动-移动')
    #         mess = MessagePage()
    #         mess.wait_for_page_load()
    #         mess.click_text("系统消息")
    #         time.sleep(3)
    #         mess.click_text("同意")
    #     Preconditions.change_mobile('Android-移动-移动')
    #     Preconditions.go_to_group_double(group_name)
    #
    # @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    # def test_msg_weifenglian_qun_0399(self):
    #     """将接收到的位置转发到团队未置灰的联系人"""
    #     # 1、在当前会话窗口长按接收到的位置消息
    #     # 2、点击转发
    #     # 3、点击选择团队联系人
    #     # 4、选择任意企业下的未置灰的联系人
    #     # 5、点击发送按钮
    #     # 用第二台手机Android-移动-移动发送文件
    #     Preconditions.public_send_location()
    #     Preconditions.change_mobile('Android-移动')
    #     group_name = Preconditions.get_group_chat_name_double()
    #     Preconditions.go_to_group_double(group_name)
    #     # 1.长按位置消息体转发
    #     gcp = GroupChatPage()
    #     gcp.wait_for_page_load()
    #     gcp.press_message_to_do("转发")
    #     sc = SelectContactsPage()
    #     sc.wait_for_page_load()
    #     sc.click_text("选择团队联系人")
    #     time.sleep(2)
    #     if sc.is_text_present("当前组织"):
    #         sc.click_one_contact("yyx")
    #         gcp.click_element_("确定移除")
    #         if not gcp.is_toast_exist("已转发"):
    #             raise AssertionError("转发失败")
    #     else:
    #         Preconditions.change_mobile('Android-移动')
    #         Preconditions.enter_organization_page()
    #         osp = OrganizationStructurePage()
    #         osp.wait_for_page_load()
    #         if not osp.swipe_and_find_element("yyx"):
    #             osp.click_text("添加联系人")
    #             time.sleep(1)
    #             osp.click_text("手动输入添加")
    #             time.sleep(1)
    #             osp.input_contacts_name("yyx")
    #             osp.input_contacts_number("18920736596")
    #             time.sleep(2)
    #             osp.click_text("完成")
    #             if not osp.is_toast_exist("成功"):
    #                 raise AssertionError("手动添加失败")
    #             osp.wait_for_page_load()
    #         current_mobile().back()
    #         workbench = WorkbenchPage()
    #         workbench.wait_for_page_load()
    #         workbench.open_message_page()
    #         Preconditions.go_to_group_double(group_name)
    #         gcp.wait_for_page_load()
    #         gcp.press_message_to_do("转发")
    #         sc = SelectContactsPage()
    #         sc.wait_for_page_load()
    #         sc.click_text("选择团队联系人")
    #         time.sleep(2)
    #         sc.click_element_("企业名称")
    #         time.sleep(2)
    #         sc.click_one_contact("yyx")
    #         gcp.click_element_("确定移除")
    #         if not gcp.is_toast_exist("已转发"):
    #             raise AssertionError("转发失败")
    #     Preconditions.change_mobile('Android-移动')
    #     mess=MessagePage()
    #     mess.wait_for_page_load()
    #     mess.click_text("yyx")
    #     from pages import SingleChatPage
    #     chat = SingleChatPage()
    #     time.sleep(2)
    #     if gcp.is_text_present("1元/条"):
    #         chat.click_i_have_read()
    #     chat.wait_for_page_load()
    #     # 验证是否发送成功
    #     cwp = ChatWindowPage()
    #     try:
    #         cwp.wait_for_msg_send_status_become_to('发送成功', 10)
    #     except TimeoutException:
    #         raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
    #     Preconditions.change_mobile('Android-移动')
    #     mess.press_file_to_do("yyx","删除聊天")
    #     Preconditions.go_to_group_double(group_name)
    #     Preconditions.delete_record_group_chat()
    #     Preconditions.change_mobile('Android-移动-移动')
    #     Preconditions.go_to_group_double(group_name)
    #     Preconditions.delete_record_group_chat()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0368(self):
        """将自己发送的位置转发到在企业内搜索框进行搜索到的团队联系人时取消转发"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.选择团队
        shc.click_department_name("测试团队1")
        # 4.在搜索框输入多种字符
        shc.input_search("大佬1")
        # 5.点击搜索的团队联系人
        if shc.is_text_present('无搜索结果'):
            pass
        else:
            shc.click_search_team_contacts()
            # 6.点击取消
            shc.click_cancel_forward()
            if not shc.is_on_this_page():
                raise AssertionError("当前页面不在选择团队联系人页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0371(self):
        """将自己发送的位置转发到最近聊天时点击取消转发"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.选择最近聊天联系人列表的第一个
        scp.select_recent_chat_by_number(0)
        # 3.点击取消发送
        scp.click_cancel_forward()
        flag = scp.is_on_this_page()
        if not flag:
            raise AssertionError("当前页面不在选择联系人页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0372(self):
        """将自己发送的位置转发到最近聊天时转发失败"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.选择最近聊天联系人列表的第一个
        scp.select_recent_chat_by_number(0)
        # 3.断开网络
        scp.set_network_status(0)
        # 4.点击确定发送
        scp.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")
        # 5.点击返回消息页面
        gcp.click_back()
        scp.wait_for_page_load()
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("消息列表没有显示消息发送失败标识")

    def tearDown_test_msg_weifenglian_qun_0372(self):
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0075(self):
        """将自己发送的文件转发到企业群"""
        gcp = GroupChatPage()
        # 1.点击文件
        gcp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        # 2.点击本地文件
        csf.click_local_file()
        # 3.选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 4.进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        # 5.点击选择发送文件
        local_file.select_file('.txt')
        local_file.click_send()
        # 6.长按最后一个文件转发
        gcp.press_last_file_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 7.点击选择一个企业群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 8.点击选择一个企业群
        sogp.select_one_enterprise_group()
        # 9.点击确定发送
        sogp.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0077(self):
        """将自己发送的文件转发到企业群"""
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_back()
        mess = MessagePage()
        scp = SelectContactsPage()
        if mess.is_on_this_page():
            pass
        else:
            scp.click_back()
        # 1.确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        Preconditions.enter_group_chat_page()
        # 2.点击文件
        gcp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        # 3.点击本地文件
        csf.click_local_file()
        # 4.选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 5.进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        # 6.点击选择发送文件
        local_file.select_file('.txt')
        local_file.click_send()
        # 7.长按最后一个文件转发
        gcp.press_last_file_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 8.点击选择一个企业群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 9.点击选择一个企业群
        sogp.select_one_enterprise_group()
        # 10.点击确定发送
        sogp.set_network_status(0)
        sogp.click_sure_forward()
        flag = gcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")
        time.sleep(2)
        # 11.点击返回至消息页面
        gcp.click_back()
        scp.wait_for_page_load()
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("消息列表没有显示消息发送失败标识")

    def tearDown_test_msg_weifenglian_qun_0077(self):
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0079(self):
        """将自己发送的文件转发到企业群时点击取消转发"""
        gcp = GroupChatPage()
        # 1.点击文件
        gcp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        # 2.点击本地文件
        csf.click_local_file()
        # 3.选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 4.进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        # 5.点击选择发送文件
        local_file.select_file('.txt')
        local_file.click_send()
        # 6.长按最后一个文件转发
        gcp.press_last_file_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 7.点击选择一个企业群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 8.点击选择一个企业群
        sogp.select_one_enterprise_group()
        # 9.点击取消
        sogp.click_cancel_forward()
        if not sogp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0088(self):
        """将自己发送的文件转发到在搜索框粘贴字符搜索到的群"""
        gcp = GroupChatPage()
        # 1.输入群名发送，长按信息并复制
        gcp.input_message("群聊2")
        gcp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("群聊2", "复制")
        flag = gcp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("群聊名字复制失败")
        # 2.点击本地文件，选择文件发送
        gcp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 3.长按最后一个文件转发
        gcp.press_last_file_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 4.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 5.搜索群组
        sogp.click_search_group()
        time.sleep(2)
        # 6.长按搜索框
        sogp.press_group_search_bar()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0099(self):
        """将自己发送的文件转发到在搜索框粘贴字符搜索到的手机联系人"""
        gcp = GroupChatPage()
        # 1.输入联系人名字发送，长按信息并复制
        gcp.input_message("大佬1")
        gcp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("大佬1", "复制")
        flag = gcp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("联系人名字复制失败")
        # 2.点击本地文件，选择文件发送
        gcp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 3.长按最后一个文件转发
        gcp.press_last_file_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 4.点击选择联系人
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 5.长按搜索框
        slcp.press_contact_search_bar()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0306(self):
        """网络异常时点击位置按钮有提示"""
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        time.sleep(1)
        cmp = ChatMorePage()
        # 2.断开网络
        cmp.set_network_status(0)
        # 3.点击位置
        cmp.click_location()
        clp = ChatLocationPage()
        flag = clp.is_toast_exist("请检查网络后重试")
        if not flag:
            raise AssertionError("没有'请检查网络后重试'提示")

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0306():
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0311(self):
        """定位界面点击左上角的返回按钮返回到群聊（企业群/普通群）会话页面"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        cmp = ChatMorePage()
        cmp.click_location()
        # 1.等待位置页面加载
        clp = ChatLocationPage()
        clp.wait_for_page_load()
        # 2.点击返回
        clp.click_back()
        time.sleep(3)
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_weifenglian_qun_0318(self):
        """在群聊（企业群/普通群）将自己发送的位置转发到当前会话窗口"""
        Preconditions.public_send_location()
        # 1.长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.选择最近聊天联系人列表的第一个
        scp.select_recent_chat_by_number(0)
        # 3.点击确认发送
        scp.click_sure_forward()
        time.sleep(1)
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not gcp.is_on_this_page():
            raise AssertionError("当前页面不在群聊天会话页面")
