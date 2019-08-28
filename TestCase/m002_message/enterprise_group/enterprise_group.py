import time
import warnings

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions

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
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
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
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

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
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "c" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_have_my_picture():
        """确保当前群聊页面已有图片"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.is_on_this_page()
        if gcp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_pic_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_have_my_videos():
        """确保当前群聊页面已有视频"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.wait_for_page_load()
        if gcp.is_exist_msg_videos():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_video_fk(1)
            cpg.click_send()
            time.sleep(5)

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
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_group_chat(types):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入群聊转发图片/视频"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            gcp = GroupChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            gcp.wait_for_page_load()
            gcp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            group_name = "群聊1"
            Preconditions.get_into_group_chat_page(group_name)
            # 转发图片/视频
            if types == "pic":
                gcp.forward_pic()
            elif types == "video":
                gcp.forward_video()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)

    @staticmethod
    def make_already_delete_my_group():
        """确保删掉所有群"""
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
        sc.click_select_one_group()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群删除，无群返回
        if len(group_names) == 0:
            sog.click_back()
            pass
        else:
            for group_name in group_names:
                sog.select_one_group_by_name(group_name)
                gcp = GroupChatPage()
                gcp.wait_for_page_load()
                gcp.click_setting()
                gcs = GroupChatSetPage()
                gcs.wait_for_page_load()
                gcs.click_delete_and_exit()
                # gcs.click_sure()
                mess.click_add_icon()
                mess.click_group_chat()
                sc.wait_for_page_load()
                sc.click_select_one_group()
            sog.click_back()
            # if not gcs.is_toast_exist("已退出群聊"):
            #     raise AssertionError("无退出群聊提示")
        # sc.click_back()
        # mess.open_me_page()

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
        file = local_file.select_file_by_text(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def enter_preset_file_catalog():
        """进入预置文件目录"""

        # 在当前群聊天会话页面，点击更多富媒体的文件按钮
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
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
    def send_file_by_name(file_type):
        """发送指定文件名字"""

        # 进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送指定名字文件
        local_file.select_file_by_text(file_type)
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

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
    def get_into_enterprise_group_chat_page():
        """进入企业群聊天会话页面 返回群名"""

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
        # 选择一个企业群
        name = sog.select_one_enterprise_group()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        return name


class MsgEnterpriseGroupChatAllTest(TestCase):
    """模块：消息-企业群"""

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
        """
        1、成功登录和飞信
        2、确保当前页面在消息页面
        """

        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0173(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        mess = MessagePage()
        # 1.点击通讯录
        mess.click_contacts()
        contact = ContactsPage()
        # 2.点击群聊
        contact.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3点击搜索框输入企业群名
        glp.click_search_input()
        enterprise_group_name = "测试企业群"
        glp.input_group_name(enterprise_group_name)
        # 4.判断是否存在搜索结果
        self.assertTrue(glp.is_exists_group_by_name(enterprise_group_name))
        time.sleep(1)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0201(self):
        """通讯录-群聊-索引字母定位选择"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、通讯录-群聊
        mess = MessagePage()
        # 1.点击通讯录
        mess.click_contacts()
        contact = ContactsPage()
        # 2.点击群聊
        contact.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.获取所有右侧索引字母，选择点击
        letters = glp.get_letters_index()
        letter = letters[0]
        glp.click_letter_index(letter)
        time.sleep(1)
        # 4.判断是否可以定位
        self.assertEqual(glp.page_should_contain_text("a a"), True)
        glp.click_letter_index('T')
        time.sleep(1)
        self.assertEqual(glp.page_should_contain_text("testa"), True)
        time.sleep(1)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangmianhua_0383(self):
        """企业群/党群在消息列表内展示——最新消息展示——文字及表情"""
        # 1、网络正常
        # 2、已登录和飞信在消息模块首页
        # 1.进入企业群
        Preconditions.get_into_group_chat_page("测试企业群")
        gcp = GroupChatPage()
        # 2.输入信息
        gcp.input_message("测试测试测试测试测试测试测试测试测试测试测试测试测试")
        # 3.点击发送
        gcp.send_message()
        # 4.验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 5.点击返回消息页面
        gcp.click_back()
        mess = MessagePage()
        # 6.判断是否超长后加“...”
        if mess.is_on_this_page():
            exist = mess.is_text_present("…")
            self.assertEqual(exist, True)





