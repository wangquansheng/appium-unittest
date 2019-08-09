import csv
import random
import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from pages import *
from pages.workbench.announcement_message.AnnouncementMessage import AnnouncementMessagePage
from pages.workbench.create_group.CreateGroup import CreateGroupPage
from pages.workbench.create_group.SelectEnterpriseContacts import SelectEnterpriseContactsPage
from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.super_meeting.SuperMeeting import SuperMeetingPage
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage

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

import os
curPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filePath = curPath + "\Resources\\test_datas\contacts_call.csv"
# contacts_call.csv文件的绝对路径如有变动，请在此处页面更新
# 如果修改contacts_call.csv文件名，请同步修改此页面方法get_contacts_by_row_linename中变量
File_Paths = {
    'contacts_call.csv': filePath,
}


class LoginPreconditions(object):
    """登录前置条件"""

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def disconnect_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.disconnect_mobile()


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
        if permission_list.page_should_contain_text2("确定"):
            permission_list.click_text("确定")
        one_key.wait_for_page_load(30)

    @staticmethod
    def make_already_in_one_key_login_page_631():
        """已经进入一键登录页(6.3.1版本)"""
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
        guide_page.click_start_the_experience_631()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
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
    def login_by_one_key_login_631():
        """
        从一键登录页面登录(6.3.1版本)
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail_631():
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button_631()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        LoginPreconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                LoginPreconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                LoginPreconditions.login_by_one_key_login()

    @staticmethod
    def enter_private_chat_page(reset=False):
        """进入单聊会话页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        contacts.click_tel_contacts_631()
        time.sleep(3)
        # if contacts.is_text_present("显示"):
        #     contacts.click_text("显示")
        contacts.click_sim_contact_ok()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        chat = SingleChatPage()
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()
        # 点击消息进入单聊会话页面
        cdp.click_message_icon()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()

    @staticmethod
    def check_in_message_page():
        """判断当前页面是否在消息页，返回True，False"""
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        mess = MessagePage()
        check_result = mess.is_on_this_page()
        return check_result

    @staticmethod
    def enter_call_page():
        """进入通话页面并进行授权等相关操作"""
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()

    @staticmethod
    def force_enter_message_page(self):
        """若当前在消息页，直接返回；若当前不在消息页，强制进入消息页"""
        time.sleep(2)
        if LoginPreconditions.check_in_message_page():
            return
        else:
            # LoginPreconditions.make_already_in_one_key_login_page()
            # LoginPreconditions.login_by_one_key_login()
            try:
                mess=MessagePage()
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                LoginPreconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                LoginPreconditions.login_by_one_key_login()

    @staticmethod
    def force_enter_message_page_631():
        """若当前在消息页，直接返回；若当前不在消息页，强制进入消息页(6.3.1版本)"""
        time.sleep(2)
        if LoginPreconditions.check_in_message_page():
            return
        else:
            LoginPreconditions.make_already_in_one_key_login_page_631()
            LoginPreconditions.login_by_one_key_login_631()

    @staticmethod
    def create_contacts_if_not_exist(member_list):
        """
        预置多个联系人
        :param member_list:['name,number']
        :return:
        """
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        for member in member_list:
            name = member.split(',')[0].strip()
            number = member.split(',')[1].strip()
            contactspage.create_contacts_if_not_exits(name, number)
        contactspage.open_message_page()

    @staticmethod
    def create_group_if_not_exist(group_name, *member_list):
        """
        创建群聊并进入群聊页面
        :param group_name:群聊名称
        :return:
        """
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword(group_name)
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]'% group_name)):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().select_local_contacts(*member_list)
            BuildGroupChatPage().create_group_chat(group_name)

    @staticmethod
    def create_group_if_not_exist_not_enter_chat(group_name, *member_list):
        """
        创建群聊不进入群聊页面
        :param group_name:群聊名称
        :return:
        """
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword(group_name)
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (
                MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name)):
            ContactListSearchPage().click_back()
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().select_local_contacts(*member_list)
            BuildGroupChatPage().create_group_chat(group_name)
            mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back'))
            mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/left_back'))
            contactspage.open_message_page()

    @staticmethod
    def create_contacts_if_not_exist_631(member_list):
        """
        预置多个联系人
        :param member_list:['name,number']
        :return:
        """
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        for member in member_list:
            name = member.split(',')[0].strip()
            number = member.split(',')[1].strip()
            contactspage.create_contacts_if_not_exits_631(name, number)
        contactspage.open_message_page()

    @staticmethod
    def get_contacts_by_row_linename(row, line_name):
        """获取contact_call.csv中联系人
            row为行，起始为0
            line_name为列名，可选值为contacts_name，telephone_num
        """
        file_path = File_Paths['contacts_call.csv']
        csv_file = open(file_path, encoding='utf-8')

        # 读取csv文件，输出一个字典列表
        csv_reader_dict = csv.DictReader(csv_file)
        items = list(csv_reader_dict)
        # 返回row行，列名line_name的值
        return items[row][line_name]

    @staticmethod
    def delete_group_if_exist(group_name):
        """删除群若存在，返回消息列表页"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631(group_name)
        if mess._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name)):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name))
            groupchat = GroupChatPage()
            groupset = GroupChatSetPage()
            groupchat.wait_for_page_load()
            groupchat.click_setting()
            # Step 群主在设置页面点击群管理
            groupset.wait_for_page_load()
            groupset.click_group_manage()
            # Step 点击解散群按钮后
            groupset.wait_exist_and_delete_confirmation_box_load()
            groupset.click_group_manage_disband_button()
            SingleChatPage().click_sure()
            GroupChatPage().click_back()
            SearchPage().click_back_button()
        else:
            SearchPage().click_back_button()

    @staticmethod
    def create_group_if_not_exist_not_enter_chat_631(group_name, *member_list):
        """
        创建群聊不进入群聊页面
        :param group_name:群聊名称
        :return:
        """
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword(group_name)
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (
                        MobileBy.XPATH,
                        '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name)):
            ContactListSearchPage().click_back()
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.click_group_chat_631()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().select_local_contacts(*member_list)
            BuildGroupChatPage().create_group_chat(group_name)

            mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
            contactspage.click_back()
            contactspage.open_message_page()

    @staticmethod
    def create_group_if_not_exist_631(group_name, *member_list):
        """
        创建群聊并进入群聊页面
        :param group_name:群聊名称
        :return:
        """
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword(group_name)
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (
                MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name)):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % group_name))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.click_group_chat_631()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().select_local_contacts(*member_list)
            BuildGroupChatPage().create_group_chat(group_name)

    @staticmethod
    def enter_my_computer_page(reset=False):
        """从消息进入我的电脑页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入我的电脑
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(1)
        if mess._is_element_present(
                (
                        MobileBy.XPATH,
                        '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % "我的电脑")):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % "我的电脑"))
        else:
            raise AssertionError('没有我的电脑选项!')


class WorkbenchPreconditions(LoginPreconditions):
    """工作台前置条件"""

    @staticmethod
    def enter_create_team_page(reset=False):
        """从消息进入创建团队页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_create_team()
        team = CreateTeamPage()
        team.wait_for_page_load()

    @staticmethod
    def enter_create_team_page2(reset=False, name="ateam7272"):
        """创建团队及选择团队"""
        mess = MessagePage()
        mess.click_contacts()
        time.sleep(1)
        contact = ContactsPage()
        contact.click_text("全部团队")
        time.sleep(1)
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, name)
        contact.click_back_by_android()
        # 当前在联系tab页面
        if not result:
            # 从消息进入创建团队页面
            # 1、不存在ateam7272团队
            mess.open_workbench_page()
            workbench = WorkbenchPage()
            if workbench.is_on_welcome_page():
                workbench.click_now_create_team()
            else:
                workbench.wait_for_page_load()
                workbench.click_create_team()
            team = CreateTeamPage()
            if team.is_on_this_page():
                current_mobile().hide_keyboard_if_display()
            time.sleep(3)
            WorkbenchPreconditions.create_team(name)
            # 进入联系Tab页面
            workbench.open_contacts_page()
            time.sleep(3)
        # 1、保证当前在联系tab页面
        # 2、无论是否存在ateam7272团队，重新选择
        # 3、选择该团队(1、当前没有选择该团队 2、当前已选择该团队)
        contact = ContactsPage()
        contact.click_team_setting_btn()
        contact.choose_team_by_name(name)
        contact.open_message_page()

    @staticmethod
    def get_team_name():
        """获取团队"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # str=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        team_name = "ateam" + phone_number[-4:]
        return team_name

    @staticmethod
    def create_team(team_name=None, user_name="admin"):
        """创建团队"""
        if not team_name:
            team_name = WorkbenchPreconditions.get_team_name()
        team = CreateTeamPage()
        team.input_team_name(team_name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name(user_name)
        # 立即创建团队
        team.click_immediately_create_team()
        # 点击完成设置工作台
        team.wait_for_setting_workbench_page_load()
        team.click_finish_setting_workbench()
        team.wait_for_create_team_success_page_load()
        # 进入工作台
        team.click_enter_workbench()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        time.sleep(3)

    @staticmethod
    def enter_organization_page(reset=False):
        """从消息进入组织架构页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            a = 0
            while a < 20:
                workbench.wait_for_page_load()
                workbench.click_organization()
                # time.sleep(5)
                if not workbench.page_should_contain_text2("添加联系人"):
                    current_mobile().back()
                    a += 1
                else:
                    break
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()

    @staticmethod
    def enter_workbench_manager_page(reset=False):
        """从消息进入工作台管理页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_workbench_manage()
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()

    @staticmethod
    def enter_voice_announcement_page(reset=False):
        """从消息进入语音通知页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            a=0
            while a<10:
                workbench.wait_for_page_load()
                workbench.click_voice_notice()
                time.sleep(5)
                if workbench.is_text_present("认证失败"):
                    current_mobile().back()
                    a+=1
                else:
                    break
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()

    @staticmethod
    def create_sub_department(departmentName):
        """从消息列表开始创建子部门并添加部门成员"""
        WorkbenchPreconditions.enter_organization_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加子部门")
        osp.wait_for_sub_department_page_load()
        osp.input_sub_department_name(departmentName)
        osp.click_text("完成")
        if osp.is_toast_exist("部门已存在，请勿重复添加"):
            current_mobile().back()
            osp.wait_for_page_load()
        else:
            osp.wait_for_page_load()
            time.sleep(2)
            osp.click_text(departmentName)
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            slc = SelectLocalContactsPage()
            # 选择联系人
            names=slc.get_contacts_name_list()
            time.sleep(2)
            sc.click_one_contact(names[0])
            sc.click_one_contact(names[1])
            sc.click_one_contact(names[2])
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            # if not slc.is_toast_exist("操作成功"):
            #     raise AssertionError("操作不成功")
            time.sleep(2)
            current_mobile().back()
            time.sleep(2)
            if not osp.is_on_this_page():
                raise AssertionError("没有返回上一级")
            time.sleep(2)
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            time.sleep(3)
            current_mobile().back()
            workbench.open_message_page()

    @staticmethod
    def enter_super_meeting_page(reset=False):
        """从消息进入超级会议页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()

    @staticmethod
    def create_he_contacts(names):
        """选择手机联系人创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name in names:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name(name)
                slc.click_sure()
                time.sleep(2)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_he_contacts2(contacts):
        """手动输入联系人创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name, number in contacts:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("手动输入添加")
                osp.input_contacts_name(name)
                osp.input_contacts_number(number)
                osp.click_confirm()
                time.sleep(2)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_enterprise_group(name):
        """创建企业群"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()
        wbp.click_add_create_group()
        cgp = CreateGroupPage()
        # 等待创建群首页加载
        cgp.wait_for_page_load()
        cgp.click_create_group()
        time.sleep(3)
        # 适配部分手机
        if cgp.is_text_present("ateam7272"):
            cgp.click_text("ateam7272")
        sec = SelectEnterpriseContactsPage()
        sec.wait_for_page_load()
        time.sleep(2)
        # 创建企业群
        sec.click_contacts_by_name("大佬1")
        sec.click_contacts_by_name("大佬2")
        sec.click_sure()
        cgp.input_group_name(name)
        cgp.click_create_group()
        time.sleep(2)
        # 返回消息列表
        cgp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def ensure_have_enterprise_group():
        """确保有企业群"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        time.sleep(2)
        flag = False
        if not cp.is_exist_enterprise_group():
            flag = True
        cp.click_return()
        cp.wait_for_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()
        if flag:
            WorkbenchPreconditions.create_enterprise_group("测试企业群")

    @staticmethod
    def ensure_have_enterprise_group2(groupname):
        """确保有企业群 """
        # 如果没有，创建制定企业群名groupname的企业群
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        time.sleep(2)
        flag = False
        if not cp.is_exist_enterprise_group():
            flag = True
        cp.click_return()
        cp.wait_for_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()
        if flag:
            WorkbenchPreconditions.create_enterprise_group(groupname)

    @staticmethod
    def ensure_have_enterprise_group2(groupname):
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        time.sleep(2)
        flag = False
        if not cp.is_exist_enterprise_group_name(groupname):
            flag = True
        cp.click_return()
        cp.wait_for_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()
        if flag:
            WorkbenchPreconditions.create_enterprise_group(groupname)

    @staticmethod
    def create_department_and_add_member(department_names):
        """创建企业部门并从手机联系人添加成员"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for department_name in department_names:
            if not osp.is_exist_specify_element_by_name(department_name):
                osp.click_specify_element_by_name("添加子部门")
                time.sleep(2)
                osp.input_sub_department_name(department_name)
                osp.input_sub_department_sort("1")
                osp.click_confirm()
                if osp.is_toast_exist("部门已存在", 2):
                    osp.click_back()
                osp.wait_for_page_load()
                osp.click_specify_element_by_name(department_name)
                time.sleep(2)
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name("大佬1")
                slc.selecting_local_contacts_by_name("大佬2")
                slc.selecting_local_contacts_by_name("大佬3")
                slc.selecting_local_contacts_by_name("大佬4")
                slc.click_sure()
                time.sleep(2)
                osp.click_back()
                time.sleep(1)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def enter_announcement_message_page(reset=False):
        """从消息进入公告信息页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_notice_info()
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()

    @staticmethod
    def enter_announcement_message_page_not_admin(reset=False):
        """从消息进入公告信息页面--非管理员"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_notice_info()
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
