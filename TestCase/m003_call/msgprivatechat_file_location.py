import random
import time
import warnings

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

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
    def enter_preset_file_catalog():
        """进入预置文件目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # scp.click_more()
        # 点击本地文件
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csfp.click_local_file()
        # 进入预置文件目录
        local_file.click_preset_file_dir()

    @staticmethod
    def send_file_by_type(file_type):
        """发送指定类型文件"""

        # 进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送指定类型文件
        local_file.select_file(file_type)
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_file():
        """发送大型文件"""

        # 进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            local_file.click_preset_file_dir()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_picture_catalog():
        """进入本地照片目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地照片
        csfp.click_pic()

    @staticmethod
    def send_local_picture():
        """发送本地图片"""

        # 进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送本地照片
        local_file.click_picture()
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_picture_file():
        """发送大型图片文件"""

        # 进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型图片文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_pic()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_video_catalog():
        """进入本地视频目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地视频
        csfp.click_video()

    @staticmethod
    def send_local_video():
        """发送本地视频"""

        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送本地视频
        local_file.click_video()
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_video_file():
        """发送大型视频文件"""

        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型视频文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_video()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_music_catalog():
        """进入本地音乐目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地音乐
        csfp.click_music()

    @staticmethod
    def send_local_music():
        """发送本地音乐"""

        # 进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送本地音乐
        local_file.click_music()
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_music_file():
        """发送大型音乐文件"""

        # 进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型音乐文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_music()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def make_no_retransmission_button(name):
        """确保当前单聊会话页面没有重发按钮影响验证结果"""

        scp = SingleChatPage()
        if scp.is_exist_msg_send_failed_button():
            scp.click_back()
            mp = MessagePage()
            mp.wait_for_page_load()
            mp.delete_message_record_by_name(name)
            Preconditions.enter_single_chat_page(name)

    @staticmethod
    def make_no_message_send_failed_status(name):
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()
        Preconditions.enter_single_chat_page(name)

    @staticmethod
    def if_exists_multiple_enterprises_enter_single_chat(file_type):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入单聊转发文件"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            scp = SingleChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            single_name = "大佬1"
            Preconditions.enter_single_chat_page(single_name)
            scp.forward_file(file_type)
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)

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
        scp.wait_for_page_load()
        scp.click_more()
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

    @staticmethod
    def make_in_message_page(moible_param,reset=False):
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
    def build_one_new_group_with_number(puhone_number,group_name):
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
        #添加指定电话成员
        time.sleep(2)
        sc.input_search_keyword(puhone_number)
        time.sleep(2)
        sog.click_text("tel")
        time.sleep(2)
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        slc.click_one_contact("飞信电话")
        # a = 0
        # names = {}
        # while a < 3:
        #     names = slc.get_contacts_name()
        #     num = len(names)
        #     if not names:
        #         raise AssertionError("No contacts, please add contacts in address book.")
        #     if num == 1:
        #         sog.page_up()
        #         a += 1
        #         if a == 3:
        #             raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
        #     else:
        #         break
        # # 选择成员
        # for name in names:
        #     slc.select_one_member_by_name(name)
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
    def create_team_select_contacts(team_name):
        """创建团队并添加指定名字联系人为团队成员"""
        current_driver().launch_app()
        gcp = GroupChatPage()
        # gcp.click_back()
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
        try:
            slc.wait_for_page_load()
            # 点击取消返回工作台页面
            slc.click_cancle()
            workbench.click_message_icon()
        except:
            current_driver().launch_app()

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
        scg.wait_for_page_load()
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
        if not sog.is_exists_group_by_name(name):
            return False
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        return True

    @staticmethod
    def create_contacts_groups():
        # 创建联系
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.select_mobile('Android-移动')
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    conts.create_contacts_if_not_exits(name, number)
                # 创建群
                phone_number = (current_mobile().get_cards(CardType.CHINA_MOBILE)[0])[-4:]
                name = 'Test_' + phone_number
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.create_group_chats_if_not_exits(name, ['大佬1', '大佬2', '大佬3', '大佬4', '大佬5', '大佬6'])
                group_list.click_back()
                conts.open_message_page()
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                Preconditions.create_he_contacts_for_sub_department("bm0", contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 导入标签分组联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                name_list = ['a a', 'abc', 'b测算', 'bb1122', '大佬1', '给个红包1', 'English']
                mp = MessagePage()
                mp.open_contacts_page()
                time.sleep(1)
                con = ContactsPage()
                con.click_mobile_contacts()
                time.sleep(1)
                con.click_label_grouping()
                time.sleep(1)
                label_group = LabelGroupingPage()
                label_name = Preconditions.get_label_grouping_name()
                if con.find_text(label_name):
                    con.click_text_or_description(label_name)
                    time.sleep(2)
                    if con.is_text_present('该标签分组内暂无成员'):
                        con.click_text_or_description('我知道了')
                        time.sleep(1)
                    label_group.click_element_c('添加成员')
                    for name in name_list:
                        time.sleep(1)
                        con.find_text(name)
                        con.click_text_or_description(name)
                    if label_group.is_sure('确定'):
                        label_group.click_ok_button()
                    current_mobile().launch_app()
                else:
                    label_group.click_element_c('新建分组')
                    time.sleep(1)
                    label_group.input_label_grouping_name(label_name)
                    time.sleep(1)
                    label_group.click_ok_button()
                    time.sleep(1)
                    for name in name_list:
                        con.find_text(name)
                        label_group.click_text_or_description(name)
                        time.sleep(1)
                    label_group.click_ok_button()
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    @staticmethod
    def dismiss_one_group(name):
        current_mobile().launch_app()
        if not Preconditions.enter_group_chat_page(name):
            return
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


class MsgPrivateChatFileLocationTest(TestCase):
    """消息->单聊文件,位置"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore')
        Preconditions.select_mobile('Android-移动')
        current_mobile().launch_app()

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        warnings.simplefilter('ignore')
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @staticmethod
    def public_send_file(file_type):
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0001(self):
        """单聊会话页面，不勾选本地文件内文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、不选择文件，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0002(self):
        """ 单聊会话页面，勾选本地文件内任意文件点击发送按钮"""
        self.public_send_file('.txt')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0003(self):
        """单聊会话页面，不勾选本地视频文件内视频点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、不选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0004(self):
        """单聊会话页面，勾选本地视频文件内任意视频点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出视频，则循环6次
        for i in range(6):
            el = local_file.select_file(".mp4")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_video()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no video")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0005(self):
        """单聊会话页面，不勾选本地照片文件内照片点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、不选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0006(self):
        """单聊会话页面，勾选本地照片文件内任意照片点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出照片，则循环6次
        for i in range(6):
            el = local_file.select_file(".jpg")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_pic()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no pic")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0007(self):
        """单聊会话页面，不勾选本地音乐文件内音乐点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、不选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0008(self):
        """单聊会话页面，勾选本地音乐文件内任意音乐点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出音乐，则循环6次
        for i in range(6):
            el = local_file.select_file(".mp3")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_music()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no music")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0019(self):
        """单聊设置-查找聊天内容-文件页面，长按文件进行删除"""
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 点击设置
        chat.click_setting()
        set_page = SingleChatSetPage()
        # 点击查找聊天内容
        set_page.search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        chat_file.delete_file(".xlsx")
        # 返回聊天会话页面
        chat_file.click_back()
        search.click_back()
        set_page.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0040(self):
        """单聊天会话页面，长按文件进行删除"""
        # 预置数据，发送文件
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 长按文件删除
        chat.delete_mess(".xlsx")
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0041(self):
        """单聊天会话页面，长按自己发送的文件，十分钟内撤回"""
        # 预置数据，发送文件
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 长按文件撤回消息
        chat.recall_mess(".xlsx")
        try:
            chat.wait_until(
                timeout=3,
                auto_accept_permission_alert=True,
                condition=lambda d: chat.is_text_present("知道了")
            )
        except:
            pass
        if chat.is_text_present("知道了"):
            chat.click_i_know()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'SLOW')
    def test_msg_private_chat_file_location_0042(self):
        """单聊天会话页面，长按自己发送的文件，超过十分钟撤回"""
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 超过十分钟,长按自己发送的文件撤回，没有撤回菜单按钮
        for i in range(122):
            time.sleep(2)
            text = chat.driver.page_source
            del text
            time.sleep(3)
            tmp = chat.driver.current_activity
            del tmp
            print(i)
        chat.press_mess(".xlsx")
        flag = chat.is_text_present("撤回")
        self.assertFalse(flag)
        # 删除文件，关闭弹框菜单
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0043(self):
        """单聊天会话页面，点击位置，再返回到会话页面"""
        # 1、在当前会话窗口点击位置
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、点击左上角的返回按钮
        location_page.click_back()
        chat.click_more()
        chat.wait_for_page_load()

    @staticmethod
    def public_send_location():
        """ 在发送位置信息 """
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        # 1、在当前会话窗口点击位置
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        addr_info = location_page.get_location_info()
        # 2、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()
        return addr_info

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0044(self):
        """单聊天会话页面，点击位置，默认当前位置直接发送"""
        self.public_send_location()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0045(self):
        """单聊天会话页面，点击位置，选择500米内的其他位置发送"""
        # 1、在当前会话窗口点击位置
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0046(self):
        """单聊天会话页面，点击位置，选择500米内的其他位置后返回到会话窗口"""
        # 1、在当前会话窗口点击位置
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击左上角的返回按钮
        location_page.click_back()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0047(self):
        """单聊天会话页面，长按位置消息体进行转发到本地通讯录联系人"""
        # 1、长按位置消息体
        addr_info = self.public_send_location()
        chat = SingleChatPage()
        # 2、选择转发，选择一个本地通讯录联系人
        chat.forward_file(addr_info)
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0048(self):
        """单聊天会话页面，长按位置消息体进行转发到和通讯录联系人"""
        # 1、在当前群聊天会话页面长按长按位置消息体
        addr_info = self.public_send_location()
        chat = SingleChatPage()
        # 2、选择一个和通讯录联系人转发
        chat.forward_file(addr_info)
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page = SelectHeContactsDetailPage()
            detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            if not names:
                print("WARN: Please add m005_contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                if not flag:
                    break
            # 3、点击确定
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发")
            self.assertTrue(flag2)
        else:
            print("WARN: Please create a team and add m005_contacts.")
            shcp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0049(self):
        """单聊天会话页面，长按位置消息体进行转发到群"""
        # 1、在当前群聊天会话页面长按位置消息体
        addr_info = self.public_send_location()
        chat = SingleChatPage()
        # 2、选择一个群转发
        chat.forward_file(addr_info)
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
            print("WARN: There is no group.")
            sogp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0050(self):
        """单聊天会话页面点击位置消息体，在位置界面点击右下角按钮进行导航"""
        # 先发送位置信息
        chat = SingleChatPage()
        self.public_send_location()
        # 1、在当前页面点击位置消息体
        chat.click_addr_info()
        chat.wait_for_location_page_load()
        # 2、点击右下角按钮
        chat.click_nav_btn()
        location_page = ChatLocationPage()
        toast_flag = location_page.is_toast_exist("未发现手机导航应用", timeout=3)
        map_flag = location_page.is_text_present("地图")
        self.assertTrue(toast_flag or map_flag)
        location_page.driver.back()
        time.sleep(0.3)
        if not chat.is_on_this_page():
            location_page.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def click_open_file(file_type):
        """在聊天会话页面打开自己发送的文件"""
        chat = SingleChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
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
            # 打开文件
            chat.open_file_in_chat_page(file_type)
            chat.wait_for_open_file()
            chat.click_back_in_open_file_page()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0051(self):
        """单聊天会话页面，点击自己发送格式为doc的文件"""
        self.click_open_file(".doc")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0052(self):
        """单聊天会话页面，点击自己发送格式为docx的文件"""
        self.click_open_file(".docx")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0053(self):
        """单聊天会话页面，点击自己发送格式为ppt的文件"""
        self.click_open_file(".ppt")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0054(self):
        """单聊天会话页面，点击自己发送格式为pptx的文件"""
        self.click_open_file(".pptx")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0055(self):
        """单聊天会话页面，点击自己发送格式为pdf的文件"""
        self.click_open_file(".pdf")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0056(self):
        """单聊天会话页面，点击自己发送格式为xls的文件"""
        self.click_open_file(".xls")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0057(self):
        """单聊天会话页面，点击自己发送格式为xlsx的文件"""
        self.click_open_file(".xlsx")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0058(self):
        """单聊天会话页面，点击自己发送格式为txt的文件"""
        self.click_open_file(".txt")


class MsgPrivateChatAllTest(TestCase):
    """模块：单聊"""

    @classmethod
    def setUpClass(cls):

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
                    conts.create_contacts_if_not_exits_new(name, number)

                # 创建名片消息联系人
                conts.create_contacts_if_not_exits2("名片消息测试", "13500135001", "中软国际", "经理", "123456@139.com")
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
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
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

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        name = "大佬1"
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_single_chat_page(name)
            return
        scp = SingleChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_single_chat_page(name)

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        file_type = ".txt"
        # 1、2.发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        time.sleep(2)
        # 获取发送的文件名称
        file_name = scp.get_current_file_name()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示文件+文件名
        self.assertEquals(mp.is_message_content_match_file_name(file_name), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0002(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        name = "大佬1"
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0002():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0003(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".txt"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0003():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0004(self):
        """对发送失败的文件进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的文件重发
        file_type = ".txt"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0004():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0005(self):
        """对发送失败的文件进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的文件重发
        file_type = ".txt"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0005():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0006(self):
        """点击取消重发文件消失，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的文件重发
        file_type = ".txt"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0006():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0007(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0007():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0008(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型文件发送
        Preconditions.send_large_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0008():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_weifenglian_1V1_0009(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型文件发送
        Preconditions.send_large_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0009():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0010(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0010():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0012(self):
        """在文件列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        file_type = ".txt"
        # 1、2.进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择文件
        local_file.select_file(file_type)
        time.sleep(2)
        # 再次选择，取消
        local_file.select_file(file_type)
        # 3.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0013(self):
        """在文件列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地文件
        csfp.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        time.sleep(2)
        # 1.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        time.sleep(2)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0014(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.发送本地图片
        Preconditions.send_local_picture()
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示图片
        self.assertEquals(mp.is_message_content_match_picture(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0015(self):
        """网络异常时勾选本地照片内任意相册的图片点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送本地图片
        Preconditions.send_local_picture()
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0015():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0016(self):
        """会话页面有图片发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".jpg"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        time.sleep(2)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0016():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0017(self):
        """对发送失败的图片文件进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的图片文件重发
        file_type = ".jpg"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0017():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0018(self):
        """对发送失败的图片进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的图片文件重发
        file_type = ".jpg"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0018():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0019(self):
        """点击取消重发图片消息，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的图片文件重发
        file_type = ".jpg"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0019():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0020(self):
        """未订购每月10G的用户发送大于2M的图片时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0020():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0021(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型图片文件发送
        Preconditions.send_large_picture_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0021():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_weifenglian_1V1_0022(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型图片文件发送
        Preconditions.send_large_picture_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0022():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0023(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0023():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0025(self):
        """在选择图片页面选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择本地照片
        local_file.click_picture()
        time.sleep(2)
        # 再次选择，取消
        local_file.click_picture()
        # 3.等待图片列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0026(self):
        """在选择图片页面点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        # 2.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        # 3.等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0028(self):
        """勾选本地视频内任意视频点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.发送本地视频
        Preconditions.send_local_video()
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示视频
        self.assertEquals(mp.is_message_content_match_video(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0029(self):
        """网络异常时勾选本地文件内任意视频点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送本地视频
        Preconditions.send_local_video()
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0029():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0030(self):
        """会话页面有视频发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        # Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".mp4"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0030():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0031(self):
        """对发送失败的视频进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的视频文件重发
        file_type = ".mp4"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        time.sleep(2)
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0031():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0032(self):
        """对发送失败的视频进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的视频文件重发
        file_type = ".mp4"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0032():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0033(self):
        """点击取消重发视频文件消失，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的视频文件重发
        file_type = ".mp4"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0033():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0034(self):
        """未订购每月10G的用户发送大于2M的视频时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0034():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0035(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型视频文件发送
        Preconditions.send_large_video_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0035():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_weifenglian_1V1_0036(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型视频文件发送
        Preconditions.send_large_video_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0036():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0037(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0037():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0039(self):
        """在视频列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择本地视频
        local_file.click_video()
        time.sleep(2)
        # 再次选择，取消
        local_file.click_video()
        # 3.等待视频列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0040(self):
        """在视频列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        # 1.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0042(self):
        """勾选音乐列表页面任意音乐点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.发送本地音乐
        Preconditions.send_local_music()
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        time.sleep(2)
        # 获取发送的文件名称
        file_name = scp.get_current_file_name()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示文件+文件名
        self.assertEquals(mp.is_message_content_match_file_name(file_name), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0043(self):
        """网络异常时勾选音乐列表页面任意音乐点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送本地音乐
        Preconditions.send_local_music()
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0043():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0044(self):
        """会话页面有音乐文件发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".mp3"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0044():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0045(self):
        """对发送失败的音乐进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的音乐文件重发
        file_type = ".mp3"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0045():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0046(self):
        """对发送失败的音乐进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的音乐文件重发
        file_type = ".mp3"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0046():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0047(self):
        """点击取消重发音乐文件消失，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的音乐文件重发
        file_type = ".mp3"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0047():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0048(self):
        """未订购每月10G的用户发送大于2M的音乐时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型音乐文件
        Preconditions.send_large_music_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0048():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0049(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型音乐文件
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型音乐文件发送
        Preconditions.send_large_music_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0049():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_weifenglian_1V1_0050(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型音乐文件
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型音乐文件发送
        Preconditions.send_large_music_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0050():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0051(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型音乐文件
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0051():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0053(self):
        """在音乐列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择本地音乐
        local_file.click_music()
        time.sleep(2)
        # 再次选择，取消
        local_file.click_music()
        # 3.等待音乐列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0054(self):
        """在音乐列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        # 1.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0074(self):
        """在单聊将自己发送的文件转发到当前会话窗口"""

        # 在当前会话页面发送文件,确保最近聊天中有记录
        scp = SingleChatPage()
        file_type = ".txt"
        Preconditions.send_file_by_type(file_type)
        time.sleep(5)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 解决发送文件后，最近聊天窗口没有记录，需要退出刷新的问题
        scp.click_back()
        single_name = "大佬1"
        Preconditions.enter_single_chat_page(single_name)
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(single_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0075(self):
        """将自己发送的文件转发到普通群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 4.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0076(self):
        """将自己发送的文件转发到企业群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 4.选择一个企业群
        sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0077(self):
        """将自己发送的文件转发到普通群时失败"""

        scp = SingleChatPage()
        single_name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(single_name)
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        group_name = "群聊1"
        # 4.选择一个普通群
        sog.selecting_one_group_by_name(group_name)
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 6.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0077():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0078(self):
        """将自己发送的文件转发到企业群时失败"""

        scp = SingleChatPage()
        single_name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(single_name)
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 4.选择一个企业群
        sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 6.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0078():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0079(self):
        """将自己发送的文件转发到普通群时点击取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 4.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 取消转发
        sog.click_cancel_forward()
        # 5.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0080(self):
        """将自己发送的文件转发到企业群时点击取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 4.选择一个企业群
        sog.select_one_enterprise_group()
        # 取消转发
        sog.click_cancel_forward()
        # 5.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0081(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "测试测试群"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0082(self):
        """将自己发送的文件转发到在搜索框输入英文字母搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "test_group"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0083(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "138138138"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0084(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "；，。"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0085(self):
        """将自己发送的文件转发到在搜索框输入特殊字符搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "&%@"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0086(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "   "
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.是否提示无搜索结果
        self.assertEquals(sog.is_toast_exist("无搜索结果"), True)
        # 返回单聊页面
        sog.click_back_icon()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0087(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "a尼6"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0088(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "a尼6"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.点击搜索结果
        sog.selecting_one_group_by_name(search_name)
        # 确定转发
        sog.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0090(self):
        """将自己发送的文件转发到搜索到的群时点击取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.调起功能菜单
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_group()
        search_name = "群聊1"
        # 输入查找信息
        sog.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（间接验证）
        self.assertEquals(sog.is_search_group_name_full_match(search_name), True)
        # 5.弹起询问弹窗：发送、取消
        sog.selecting_one_group_by_name(search_name)
        # 6.取消转发
        sog.click_cancel_forward()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0091(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的群"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_letter_index("Q")
        time.sleep(1)
        name = "群聊1"
        # 4.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0092(self):
        """将自己发送的文件转发到手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        contact_name = "大佬2"
        # 4.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 确定转发
        slc.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0093(self):
        """将自己发送的文件转发到手机联系人时点击取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        contact_name = "大佬2"
        # 4.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 取消转发
        slc.click_cancel_forward()
        # 5.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0094(self):
        """将自己发送的文件转发到手机联系人时发送失败"""

        scp = SingleChatPage()
        single_name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(single_name)
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        contact_name = "大佬2"
        # 4.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 6.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0094():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0095(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        search_name = "b马9"
        # 输入查找信息
        slc.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（字母导航栏由于页面问题难以验证）
        self.assertEquals(slc.is_search_contact_name_full_match(search_name), True)
        # self.assertEquals(slc.is_exists_letter_index(), False)
        # 5.点击搜索结果
        slc.selecting_local_contacts_by_name(search_name)
        # 确定转发
        slc.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0096(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        search_name = "123987"
        # 输入查找信息
        slc.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（字母导航栏由于页面问题难以验证）
        self.assertEquals(slc.is_search_contact_name_full_match(search_name), True)
        # self.assertEquals(slc.is_exists_letter_index(), False)
        # 5.点击搜索结果
        slc.selecting_local_contacts_by_name(search_name)
        # 确定转发
        slc.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0097(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        search_name = "。：、"
        # 输入查找信息
        slc.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（字母导航栏由于页面问题难以验证）
        self.assertEquals(slc.is_search_contact_name_full_match(search_name), True)
        # self.assertEquals(slc.is_exists_letter_index(), False)
        # 5.点击搜索结果
        slc.selecting_local_contacts_by_name(search_name)
        # 确定转发
        slc.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0098(self):
        """将自己发送的文件转发到在搜索框输入字母搜索到的手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        search_name = "test_contact"
        # 输入查找信息
        slc.input_search_keyword(search_name)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（字母导航栏由于页面问题难以验证）
        self.assertEquals(slc.is_search_contact_name_full_match(search_name), True)
        # self.assertEquals(slc.is_exists_letter_index(), False)
        # 5.点击搜索结果
        slc.selecting_local_contacts_by_name(search_name)
        # 确定转发
        slc.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0101(self):
        """将自己发送的文件转发到在搜索框输入号码搜索到的手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        search_number = "13800138007"
        # 输入查找信息
        slc.input_search_keyword(search_number)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（字母导航栏由于页面问题难以验证）
        self.assertEquals(slc.is_search_contact_number_full_match(search_number), True)
        # self.assertEquals(slc.is_exists_letter_index(), False)
        # 5.点击搜索结果
        slc.selecting_local_contacts_by_number(search_number)
        # 确定转发
        slc.click_sure_forward()
        # 6.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0102(self):
        """将自己发送的文件转发到在搜索框进行搜索到的手机联系人时取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        search_number = "13800138008"
        # 输入查找信息
        slc.input_search_keyword(search_number)
        time.sleep(2)
        # 4.检查搜索结果是否完全匹配关键字（字母导航栏由于页面问题难以验证）
        self.assertEquals(slc.is_search_contact_number_full_match(search_number), True)
        # self.assertEquals(slc.is_exists_letter_index(), False)
        # 5.点击搜索结果
        slc.selecting_local_contacts_by_number(search_number)
        # 取消转发
        slc.click_cancel_forward()
        # 6.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0103(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的手机联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.click_letter_index("D")
        time.sleep(1)
        contact_name = "大佬2"
        # 4.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 确定转发
        slc.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0104(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的手机联系人时点击取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 3.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.click_letter_index("D")
        time.sleep(1)
        contact_name = "大佬2"
        # 4.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 取消转发
        slc.click_cancel_forward()
        # 5.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0105(self):
        """将自己发送的文件转发到团队未置灰的联系人"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 3.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 4.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat(file_type)
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        shc.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0107(self):
        """将自己发送的文件转发到团队未置灰的联系人时点击取消转发"""

        scp = SingleChatPage()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 3.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 4.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat(file_type)
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 取消转发
        shc.click_cancel_forward()
        # 5.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        shc.click_back()
        time.sleep(1)
        shc.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0133(self):
        """将接收到的文件转发到普通群"""
        # 1、在当前会话窗口长按接收到的文件消息
        # 2、点击转发
        # 3、点击选择一个群
        # 4、选择任意普通群
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并转发
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件",3000)
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择一个群")
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword("给个红包1")
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有给个红包1群，请创建后重试")
        sog.click_element_("群聊名")
        time.sleep(2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动-移动')
        mess.click_text("给个红包1")
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.press_file_to_do('给个红包1', "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0134(self):
        """将接收到的文件转发到企业群"""
        # 1、在当前会话窗口长按接收到的文件消息
        # 2、点击转发
        # 3、点击选择一个群
        # 4、选择任意企业群
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并转发
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件",3000)
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择一个群")
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
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动-移动')
        mess.click_text("测试企业群")
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.press_file_to_do('测试企业群', "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0163(self):
        """将接收到的文件转发到团队未置灰的联系人"""
        # 1、在当前会话窗口长按接收到的文件消息
        # 2、点击转发
        # 3、点击选择团队联系人
        # 4、选择任意企业下的未置灰的联系人
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并转发
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件",3000)
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择团队联系人")
        time.sleep(2)
        sc.click_element_("企业名称")
        time.sleep(2)
        sc.click_one_contact("大佬3")
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动')
        mess.click_text("大佬3")
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.press_file_to_do('大佬3', "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0183(self):
        """将接收到的文件转发到我的电脑"""
        # 1、在当前会话窗口长按接收到的文件消息
        # 2、点击转发
        # 3、点击搜索框输入我的电脑进行搜索
        # 4、选择搜索结果：我的电脑
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并转发
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件",3000)
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.input_search_keyword("我的")
        time.sleep(2)
        sc.click_text("我的电脑")
        time.sleep(2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动-移动')
        mess.click_text("我的电脑")
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.press_file_to_do('我的电脑', "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0184(self):
        """将接收到的文件转发到最近聊天"""
        # 1、在当前会话窗口长按接收到的文件消息
        # 2、点击转发
        # 3、点击选择最近聊天
        # 4、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并转发
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件",3000)
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text(phone_number2)
        time.sleep(2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动-移动')
        mess.click_text(phone_number2)
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0187(self):
        """对接收到的文件消息进行删除"""
        # 1、在当前会话窗口长按接收到的文件消息
        # 2、点击删除
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并删除
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件",3000)
        scp.click_text("删除")
        time.sleep(2)
        if scp.is_element_exit_("消息文件"):
            raise AssertionError("删除文件不成功")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0188(self):
        """对接收到的已下载文件消息进行收藏"""
        # 1、在当前会话窗口长按接收到的已下载文件消息
        # 2、点击收藏
        # 3、去收藏列表查看
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        # 1.长按接受到的文件并收藏
        scp.click_element_("消息文件")
        scp.wait_for_file_load()
        scp.press_element_("消息文件", 3000)
        scp.click_text("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.open_me_page()
        mep = MePage()
        mep.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        if not mcp.is_element_exit_("收藏的文件"):
            raise AssertionError("收藏的视频不可见")
        # 左滑收藏消息体
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
            time.sleep(1)
            mcp.click_back()
            mess.open_message_page()
        else:
            raise AssertionError("没有删除收藏按钮")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0189(self):
        """对接收到的未下载文件消息进行收藏"""
        # 1、在当前会话窗口长按接收到的未下载文件消息
        # 2、点击收藏
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(2)
        # 1.长按接受到的文件并收藏
        # scp.click_element_("消息文件")
        # scp.wait_for_file_load()
        scp.press_element_("消息文件", 3000)
        scp.click_text("收藏")
        if not scp.is_toast_exist("请先下载文件"):
            raise AssertionError("没有出现‘请先下载文件’toast")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0386(self):
        """将接收到的位置转发到手机联系人"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击转发
        # 3、点击选择手机联系人
        # 4、选择任意联系人
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        scp.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_element_("确定")
        if not sc.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        mess.click_text("飞信电话")
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do("飞信电话","删除聊天")
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0399(self):
        """将接收到的位置转发到团队未置灰的联系人"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击转发
        # 3、点击选择团队联系人
        # 4、选择任意企业下的未置灰的联系人
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择团队联系人")
        time.sleep(2)
        if sc.is_text_present("当前组织"):
            sc.click_one_contact("yyx")
            scp.click_element_("确定")
            if not scp.is_toast_exist("已转发"):
                raise AssertionError("转发失败")
        else:
            Preconditions.change_mobile('Android-移动')
            Preconditions.enter_organization_page()
            osp = OrganizationStructurePage()
            osp.wait_for_page_load()
            if not osp.swipe_and_find_element("yyx"):
                osp.click_text("添加联系人")
                time.sleep(1)
                osp.click_text("手动输入添加")
                time.sleep(1)
                osp.input_contacts_name("yyx")
                osp.input_contacts_number("18920736596")
                time.sleep(2)
                osp.click_text("完成")
                if not osp.is_toast_exist("成功"):
                    raise AssertionError("手动添加失败")
                osp.wait_for_page_load()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_message_page()
            mess.wait_for_page_load()
            mess.click_text(phone_number2)
            scp.wait_for_page_load()
            time.sleep(3)
            scp.press_message_to_do("转发")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择团队联系人")
            time.sleep(2)
            sc.click_element_("企业名称")
            time.sleep(2)
            sc.click_one_contact("yyx")
            scp.click_element_("确定")
            if not scp.is_toast_exist("已转发"):
                raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        mess.click_text("yyx")
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do("yyx","删除聊天")
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0419(self):
        """将接收到的位置转发到我的电脑"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击转发
        # 3、点击搜索框输入我的电脑进行搜索
        # 4、选择搜索结果：我的电脑
        # 5、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.input_search_keyword("我的")
        time.sleep(2)
        sc.click_text("我的电脑")
        time.sleep(2)
        scp.click_element_("确定")
        if not sc.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        mess.click_text("我的电脑")
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do("我的电脑","删除聊天")
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0420(self):
        """将接收到的位置转发到最近聊天"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击转发
        # 3、点击选择最近聊天
        # 4、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text(phone_number2)
        time.sleep(2)
        scp.click_element_("确定")
        if not sc.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0423(self):
        """对接收到的位置消息进行删除"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击删除
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("删除")
        time.sleep(2)
        if scp.is_element_exit_("消息位置"):
            raise AssertionError("删除位置信息不成功")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0424(self):
        """对接收到的位置消息进行收藏"""
        # 1、在当前会话窗口长按接收到的位置消息
        # 2、点击收藏
        # 3、去收藏列表查看
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        if not mcp.is_element_exit_("收藏的位置"):
            raise AssertionError("收藏的位置不可见")
        # 左滑收藏消息体
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
            time.sleep(1)
            mcp.click_back()
            mess.open_message_page()
        else:
            raise AssertionError("没有删除收藏按钮")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0439_01(self):
        """长按接收到的位置消息体进行转发、删除、收藏等操作"""
        # 1.在聊天会话页面，长按接收到位置消息，是否会展示：转发、收藏、删除等功能_
        # 2.检查这些功能是否可以正常使用
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        if not mcp.is_element_exit_("收藏的位置"):
            raise AssertionError("收藏的位置不可见")
        # 左滑收藏消息体
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
            time.sleep(1)
            mcp.click_back()
            mess.open_message_page()
        else:
            raise AssertionError("没有删除收藏按钮")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0439_02(self):
        """长按接收到的位置消息体进行转发、删除、收藏等操作"""
        # 1.在聊天会话页面，长按接收到位置消息，是否会展示：转发、收藏、删除等功能_
        # 2.检查这些功能是否可以正常使用
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("删除")
        time.sleep(2)
        if scp.is_element_exit_("消息位置"):
            raise AssertionError("删除位置信息不成功")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_weifenglian_1V1_0439_03(self):
        """长按接收到的位置消息体进行转发、删除、收藏等操作"""
        # 1.在聊天会话页面，长按接收到位置消息，是否会展示：转发、收藏、删除等功能_
        # 2.检查这些功能是否可以正常使用
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        Preconditions.public_send_location()
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        time.sleep(3)
        scp.press_message_to_do("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text(phone_number2)
        time.sleep(2)
        scp.click_element_("确定")
        if not sc.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0089(self):
        """将自己发送的文件转发到在搜索框粘贴字符搜索到的群"""
        scp = SingleChatPage()
        # 1.输入群名发送，长按信息并复制
        scp.input_message("群聊1")
        scp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        scp.press_file_to_do("群聊1", "复制")
        flag = scp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("群聊名字复制失败")
        # 2.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 3.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        # 4.等待选择联系人页面加载
        select_contacts.wait_for_page_load()
        # 5.点击选择一个群
        select_contacts.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 6.搜索群组
        sogp.click_search_group()
        time.sleep(1)
        # 7.长按搜索框
        sogp.press_group_search_bar()

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0099(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的手机联系人"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 3.点击选择手机联系人
        select_contacts.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_search_box()
        # 3.在搜索框输入含有空格点击搜索到的手机联系人
        slcp.search_and_select_contact("a a")
        if scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0100(self):
        """将自己发送的文件转发到在搜索框粘贴字符搜索到的手机联系人"""
        scp = SingleChatPage()
        # 1.输入联系人名字发送，长按信息并复制
        scp.input_message("飞信电话")
        scp.send_message()
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        scp.press_file_to_do("飞信电话", "复制")
        flag = scp.is_toast_exist("已复制")
        if not flag:
            raise AssertionError("联系人名字复制失败")
        # 2.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 3.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 3.点击选择手机联系人
        select_contacts.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 4.点击搜索框长按粘贴
        slcp.click_search_box()
        slcp.press_search_bar()

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0108(self):
        """将自己发送的文件转发到团队联系人时发送失败"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 6.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 7.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat(file_type)
        name = "大佬1"
        shc.selecting_he_contacts_by_name(name)
        # 8.断开网络
        shc.set_network_status(0)
        # 9.点击确认
        shc.click_sure_forward()
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        # 10.返回单聊会话页面
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("消息列表没有显示消息发送失败标识")

    def tearDown_test_msg_weifenglian_1V1_0108(self):
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0109(self):
        """将自己发送的文件转发到在企业列表搜索框输入多种字符搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击“选择团队联系人”菜单
        select_contacts.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 5.在搜索框输入多种字符
        shc.input_search("给个红包1")
        # 6.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 7.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0110():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_contacts()
        contact = ContactsPage()
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        contact.click_contact_all_team()
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        # 确保有这个'测试团队1'并且添加指定联系人
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, "测试团队1")
        # if contact.is_exist_team_by_name("测试团队1"):
        if result:
            contact.click_back()
            contact.click_message_icon()
        else:
            contact.click_back()
            contact.click_message_icon()
            Preconditions.create_team_select_contacts("测试团队1")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0110(self):
        """将自己发送的文件转发到在企业内搜索框输入多种字符搜索到的团队联系人"""
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 6.选择团队
        shc.click_department_name("测试团队1")
        # 7.在搜索框输入多种字符
        shc.input_search("给个红包1")
        # 8.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 9.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0111(self):
        """将自己发送的文件转发到在企业列表搜索框输入数字搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击“选择团队联系人”菜单
        select_contacts.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 5.在搜索框输入数字
        shc.input_search("1122")
        # 6.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 7.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0112(self):
        """将自己发送的文件转发到在企业内搜索框输入数字搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        scg.click_he_contacts()
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
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0113(self):
        """将自己发送的文件转发到在企业列表搜索框输入标点符号搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击“选择团队联系人”菜单
        select_contacts.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 5.在搜索框输入标点符号
        shc.input_search("!")
        # 6.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 7.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0114(self):
        """将自己发送的文件转发到在企业内搜索框输入标点符号搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 6.选择团队
        shc.click_department_name("测试团队1")
        # 7.在搜索框输入标点符号
        shc.input_search("!")
        # 8.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 9.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0115(self):
        """将自己发送的文件转发到在企业列表搜索框输入字母搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击“选择团队联系人”菜单
        select_contacts.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 5.在搜索框输入字母
        shc.input_search("English")
        # 6.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 7.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0116(self):
        """将自己发送的文件转发到在企业内搜索框输入字母搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 6.选择团队
        shc.click_department_name("测试团队1")
        # 7.在搜索框输入字母
        shc.input_search("English")
        # 8.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 9.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0117(self):
        """将自己发送的文件转发到在企业列表搜索框输入空格搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击“选择团队联系人”菜单
        select_contacts.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 5.在搜索框输入空格
        shc.input_search("a a")
        # 6.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 7.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0118(self):
        """将自己发送的文件转发到在企业内搜索框输入空格搜索到的团队联系人"""
        scp = SingleChatPage()
        file_type = ".txt"
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(file_type):
            Preconditions.send_file_by_type(file_type)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()
        # 3.长按自己发送的文件并转发
        scp.forward_file(file_type)
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 6.选择团队
        shc.click_department_name("测试团队1")
        # 7.在搜索框输入空格
        shc.input_search("a a")
        # 8.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 9.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在群聊页面")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0213(self):
        """单聊聊天文件列表页点击文件进行打开"""
        scp = SingleChatPage()
        # 1.确保当前聊天页面已有文件
        if not scp.is_exist_file_by_type(".txt"):
            Preconditions.send_file_by_type(".txt")
        scp.wait_for_page_load()
        # 2.点击打开自己发送的txt文件
        scp.click_open_file(".txt")
        time.sleep(2)
        # 3.返回单聊页面查找html文件
        current_mobile().back()
        if not scp.is_exist_file_by_type(".html"):
            Preconditions.send_file_by_type(".html")
        scp.wait_for_page_load()
        # 4.点击打开自己发送的html文件
        scp.click_open_file(".html")
        time.sleep(2)
        # 5.验证是否提示调起第三方打开软件，选择弹窗
        self.assertTrue(scp.is_toast_exist("使用以下方式打开"))
        time.sleep(2)

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_huangcaizui_A_0066(self):
        """消息-一对一消息-关闭消息免打扰"""
        # 1、正常联网环境
        # 2、成功登录
        # 3、当前一对一设置页面
        # 4、消息免打扰已开启
        scp = SingleChatPage()
        # 1.点击设置
        scp.click_setting()
        scsp = SingleChatSetPage()
        scsp.wait_for_page_load()
        # 2.消息免打扰,如果开启状态，需要点击关闭
        if not scsp.is_selected_no_disturb():
            pass
        else:
            scsp.click_no_disturb()
        scsp.click_back()
        scp.wait_for_page_load()
        # 3.验证是否存在消息免打扰标识
        self.assertFalse(scp.is_exist_no_disturb_icon())
        # 4.返回消息列表页面
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        self.assertTrue(mess.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0207():
        """确保聊天会话窗口中已存在多条消息体"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")
        scp = SingleChatPage()
        for i in range(3):
            scp.input_message("哈哈")
            scp.send_message()
            time.sleep(3)

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_huangcaizui_A_0207(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        # 1.网络正常
        # 2.单聊/群聊/我的电脑/分组群发--聊天会话窗中，已存在多条消息体
        # 3.选中的消息体为（2—100条）
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.长按消息选择多选
        scp.press_last_message_to_do("多选")
        # 2.选择多条消息
        scp.click_select_many_messages()
        # 3.点击转发
        scp.click_text("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击最近聊天中的联系人
        select_contacts.click_recent_contact()
        time.sleep(2)
        # 5.点击确定
        select_contacts.click_text("确定")
        self.assertTrue(scp.is_toast_exist("已转发"))
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0281():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_contacts_only()
        contact = ContactsPage()
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        contact.wait_for_page_load()
        time.sleep(1)
        contact.click_contact_all_team()
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        # 确保有这个'测试团队1'并且添加指定联系人
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, "测试团队1")
        # if contact.is_exist_team_by_name("测试团队1"):
        if result:
            contact.click_back()
        else:
            contact.click_back()
            contact.click_message_icon()
            Preconditions.create_team_select_contacts("测试团队1")
            mess.click_contacts_only()

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_huangcaizui_A_0281(self):
        """联系——选择团队联系人——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        contact = ContactsPage()
        contact.wait_for_page_load()
        # 1.点击全部团队
        contact.click_contact_all_team()
        time.sleep(2)
        contact.click_text("测试团队1")
        time.sleep(2)
        contact.click_text("大佬1")
        time.sleep(2)
        cdp = ContactDetailsPage()
        time.sleep(2)
        # 3.点击消息
        cdp.click_text("消息")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 4.验证是否在单聊页面
        self.assertTrue(scp.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0291():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_huangcaizui_A_0291(self):
        """通过点击群聊中头像进入单聊"""
        # 1.客户端已登录
        # 2.网络正常
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 2.点击第一个群成员头像
        gcsp.click_first_group_member_avatar()
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_text("消息")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 4.验证是否在单聊页面
        self.assertTrue(scp.is_on_this_page())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0356():
        """确保消息列表没有发送失败标识，聊天会话窗口中已存在多条消息体"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")
        Preconditions.make_no_message_send_failed_status("大佬2")
        scp = SingleChatPage()
        for i in range(3):
            scp.input_message("哈哈")
            scp.send_message()
            time.sleep(3)

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_xiaoqiu_0356(self):
        """转发——支持转发的——默认选中项（1条）"""
        # 1.网络异常
        # 2.单聊/群聊/我的电脑/分组群发--聊天会话窗中，已存在多条消息体
        # 3、当前消息支持转发）
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.长按消息选择多选
        scp.press_last_message_to_do("多选")
        # 2.选择多条消息
        scp.click_select_many_messages()
        # 3.点击转发
        scp.click_text("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击最近聊天中的联系人
        select_contacts.click_recent_contact()
        time.sleep(2)
        # 5.断开网络
        select_contacts.set_network_status(0)
        # 6.点击确定
        select_contacts.click_text("确定")
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 7.验证当前页面是否有发送失败标识
        self.assertTrue(scp.is_send_sucess())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0356():
        # 重新连接网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0055(self):
        """将系统文件分享到普通群"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        # 3.等待选择联系人页面加载
        select_contacts.wait_for_page_load()
        # 4.点击选择一个群
        select_contacts.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 6.根据名字选择一个群
        sogp.selecting_one_group_by_name("群聊1")
        sogp.click_sure_forward()
        time.sleep(1)
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 7.验证是否在消息页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0057(self):
        """将系统文件分享到企业群"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        # 3.等待选择联系人页面加载
        select_contacts.wait_for_page_load()
        # 4.点击选择一个群
        select_contacts.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 6.根据名字选择一个企业群
        sogp.selecting_one_group_by_name("测试企业群")
        sogp.click_sure_forward()
        time.sleep(1)
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 7.验证是否在消息页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0061(self):
        """将系统文件分享到团队联系人"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        # 3.等待选择联系人页面加载
        select_contacts.wait_for_page_load()
        select_contacts.click_group_contact()
        # 4.选择团队联系人
        select_contacts.input_search_keyword("大佬1")
        select_contacts.selecting_contacts_by_name("大佬1")
        # 5.点击确定
        select_contacts.click_sure_forward()
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 6.验证是否在消息页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0065(self):
        """将系统文件分享到手机联系人"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 3.点击手机联系人
        select_contacts.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name_list()
        # 4.随机选择一个手机联系人
        name = random.choice(names)
        if name:
            slcp.selecting_local_contacts_by_name(name)
        # 4.点击确定
        select_contacts.click_sure_forward()
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 5.验证是否在消息页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0068(self):
        """将系统文件分享到最近聊天"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 3.选择最近聊天联系人列表的第一个
        select_contacts.select_recent_chat_by_number(0)
        # 4.点击确定
        select_contacts.click_sure_forward()
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 5.验证是否在消息页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0071(self):
        """将系统文件分享到我的电脑"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件转发
        scp.press_last_file_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 3.搜索框输入我的电脑
        select_contacts.search("我的电脑")
        select_contacts.select_one_contact_by_name("我的电脑")
        # 4.点击确定
        select_contacts.click_sure_forward()
        self.assertTrue(scp.is_toast_exist("已转发"))
        # 5.验证是否在消息页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_01(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_02(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.doc')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_03(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.docx')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_04(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.ppt')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_05(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.pptx')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_06(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.pdf')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_07(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.xls')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))

    @tags('ALL', 'CMCC', 'full', 'high', 'yx')
    def test_msg_weifenglian_1V1_0244_08(self):
        """验证在收藏页面是否可以正常打开查阅文件"""
        scp = SingleChatPage()
        # 1.点击本地文件，选择文件发送
        scp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.xlsx')
        local_file.click_send()
        # 2.长按最后一个文件收藏
        scp.press_last_file_to_do("收藏")
        # 3.验证是否收藏成功
        self.assertTrue(scp.is_toast_exist("已收藏"))







