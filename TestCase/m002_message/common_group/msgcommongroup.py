import time
import unittest
import warnings
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage, SelectHeContactsDetailPage, GroupListPage, ContactsPage
from pages import ChatAudioPage
from pages import ChatMorePage
from pages import ChatSelectFilePage
from pages.chat.ChatPhoto import ChatPhotoPage
from pages import ChatSelectLocalFilePage
from pages import ChatWindowPage
from pages import CreateGroupNamePage
from pages import FindChatRecordPage
from pages import GroupChatPage
from pages import GroupChatSetPage
from pages import GuidePage
from pages import MeCollectionPage
from pages import MePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import SelectContactsPage
from pages import SelectLocalContactsPage
from pages import SelectOneGroupPage
from pages import SingleChatPage
from pages.chat.ChatGroupAddContacts import ChatGroupAddContactsPage

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


class Preconditions(object):
    """前置条件"""

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
        a=0
        names={}
        while a<3:
            names = slc.get_contacts_name()
            num=len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num==1:
                sog.page_up()
                a+=1
                if a==3:
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
        # guide_page.swipe_to_the_second_banner()
        # guide_page.swipe_to_the_third_banner()
        # current_mobile().hide_keyboard_if_display()
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
    def select_one_mobile(moible_param):
        """选择指定的设备连接，并确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        # 消息页面
        Preconditions.make_in_message_page(moible_param,reset=False)

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

class MsgCommonGroupTest(TestCase):
    """
        模块：消息-普通群
        文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
        表格：消息-普通群
    """

    @classmethod
    def setUpClass(cls):
        pass

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
    def setUp_test_msg_common_group_0001():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        # current_mobile().launch_app()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0001(self):
        """输入框中输入字符数为空"""
        #检查是否存在语言按钮
        gcp = GroupChatPage()
        gcp.page_should_contain_audio_btn()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0002(self):
        """输入框中输入字符数大于0"""
        gcp = GroupChatPage()
        #输入信息
        gcp.input_message("哈哈")
        #点击发送
        gcp.send_message()
        #验证是否发送成功
        cwp=ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0002(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','high')
    def test_msg_common_group_0003(self):
        """输入框中输入字符数等于5000"""
        gcp = GroupChatPage()
        # 输入信息
        info="Hello everyone, Welcome to my group, I hope my group can bring you happy."
        gcp.input_message(info)
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0003(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','high')
    def test_msg_common_group_0004(self):
        """输入框中输入字符数大于5000"""
        gcp = GroupChatPage()
        # 输入信息
        info1 = "哈"*5001
        if len(info1)>5000:
            gcp.input_message(info1)
        #获取输入框信息
        info2=gcp.get_input_message()
        #判断输入框是否最多只能输入5000长度字符
        if len(info1) == len(info2):
            raise AssertionError("输入框能输入大于5000长度的字符")
        if len(info2)==5000:
            return True

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0005(self):
        """向上滑动发送按钮，放大发送输入框中的5000文本字符内容"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        #长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0005(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0006(self):
        """向上滑动发送按钮，缩小发送输入框中的5000文本字符内容"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0006(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0007(self):
        """在聊天会话页面，长按文本消息，使用复制功能"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #长按信息并点击复制
        gcp.press_file_to_do("哈哈","复制")
        flag=gcp.is_toast_exist("已复制")
        self.assertTrue(flag)
        #长按输入框
        gcp.press_file("说点什么...")
        time.sleep(2)
        flag2 = gcp.is_toast_exist("粘贴")
        # self.assertTrue(flag2)

    def tearDown_test_msg_common_group_0007(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0008(self):
        """在聊天会话页面，长按文本消息，使用删除功能"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击删除
        gcp.press_file_to_do("哈哈", "删除")
        #验证消息会消失
        flag=gcp.is_text_present("哈哈")
        self.assertFalse(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0009(self):
        """在聊天会话页面，转发5000字符的文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        #搜索联系人
        sc.input_search_contact_message("和")
        time.sleep(3)
        #选择“和飞信电话”联系人进行转发
        sc.click_text("012560")
        time.sleep(2)
        sc.click_sure_forward()
        flag=sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        #返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # time.sleep(2)
        # sogp.click_back()
        # sc.click_back()
        # time.sleep(2)
        #判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            time.sleep(2)
            if gcp.is_text_present("1元/条"):
                chat.click_i_have_read()
            time.sleep(2)
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            chat.click_back()

    @staticmethod
    def setUp_test_msg_common_group_0010():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC-RESET', 'group_chat')
    def test_msg_common_group_0010(self):
        """
        在聊天会话页面，转发5000字符的文本消息
        """
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #断开网络
        gcp.set_network_status(1)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 搜索联系人
        sc.input_search_contact_message("飞信")
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            #判断是否有“！”
            if  not mess.is_iv_fail_status_present():
                try:
                    raise AssertionError("没有消息发送失败“！”标致")
                except AssertionError as e:
                    print(e)
            #进入新消息窗口判断消息是否发送失败
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))

    def tearDown_test_msg_common_group_0010(self):
        #重新连接网络
        scp = GroupChatPage()
        scp.set_network_status(6)

    @staticmethod
    def setUp_test_msg_common_group_0011():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC-RESET', 'group_chat')
    def test_msg_common_group_0011(self):
        """
        在聊天会话页面，长按文本消息，使用转发功能，搜索选择转发对象
        """
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 搜索联系人
        sc.input_search_contact_message("飞信")
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        #删除群聊消息记录
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除聊天记录
        gcsp.click_clear_chat_record()
        gcsp.wait_clear_chat_record_confirmation_box_load()
        # 点击确认
        gcsp.click_determine()
        # flag = gcsp.is_toast_exist("聊天记录清除成功")
        # self.assertTrue(flag)
        time.sleep(3)
        # 点击返回群聊页面
        gcsp.click_back()
        time.sleep(2)
        # 判断是否返回到群聊页面
        self.assertTrue(gcp.is_on_this_page())
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0012(self):
        """在聊天会话页面，点击重发按钮，重新发送发送失败的消息"""
        gcp = GroupChatPage()
        #断开网络
        gcp.set_network_status(1)
        time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送失败
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))
        #重连网络
        gcp.set_network_status(6)
        #判断是否有重发按钮
        if not gcp.is_exist_msg_send_failed_button():
            try:
                raise AssertionError("没有重发按钮")
            except AssertionError as e:
                raise e
        #点击重发按钮
        gcp.click_msg_send_failed_button()
        #点击确定重发
        gcp.click_resend_confirm()
        #判断信息发送状态
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息未在 {}s 内发送成功'.format(10))

    def tearDown_test_msg_common_group_0012(self):
        #重新连接网络
        scp = GroupChatPage()
        scp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','high')
    def test_msg_common_group_0013(self):
        """在聊天会话页面，长按文本消息，使用转发功能，选择一个群作为转发对象"""
        gcp = GroupChatPage()
        cwp = ChatWindowPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.click_select_one_group()
        # 选择一个群进行转发
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        if group_names:
            sog.select_one_group_by_name(group_names[0])
            sog.click_sure_forward()
            if not sog.catch_message_in_page("已转发"):
                try:
                    raise AssertionError("转发失败")
                except AssertionError as e:
                    print(e)
        else:
            try:
                raise AssertionError("没有群可转发，请创建群")
            except AssertionError as e:
                print(e)

        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present(group_names[0]))
            mess.click_element_by_text(group_names[0])
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                current_mobile().back()
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    # @staticmethod
    # def setUp_test_msg_common_group_0015():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','high')
    def test_msg_common_group_0015(self):
        """在聊天会话页面，长按文本消息，使用转发功能，选择本地联系人作为转发对象"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(2)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 删除群聊消息记录
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除聊天记录
        gcsp.click_clear_chat_record()
        gcsp.wait_clear_chat_record_confirmation_box_load()
        # 点击确认
        gcsp.click_determine()
        # flag = gcsp.is_toast_exist("聊天记录清除成功")
        # self.assertTrue(flag)
        time.sleep(2)
        # 点击返回群聊页面
        gcsp.click_back()
        time.sleep(2)
        # 返回消息页面
        gcp.click_back()
        time.sleep(2)
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            sogp.click_back()
            sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            time.sleep(2)
            if gcp.is_text_present("1元/条"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            time.sleep(2)
            # 最后删除消息记录，返回消息页面结束用例
            mess.press_file_to_do("哈哈","删除")
            chat.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','high')
    def test_msg_common_group_0016(self):
        """在聊天会话页面，长按文本消息，使用转发功能，选择最近聊天作为转发对象"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        time.sleep(2)
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择最近聊天中“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            time.sleep(2)
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            #判断是否新增一条消息记录
            if not chat.is_text_present("哈哈"):
                try:
                    raise AssertionError("没有新增一条消息记录")
                except AssertionError as e:
                    print(e)
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            chat.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','high')
    def test_msg_common_group_0017(self):
        """在聊天会话页面，长按文本消息，使用收藏功能"""
        gcp = GroupChatPage()
        # 长按信息并点击收藏
        gcp.press_file_to_do("哈哈", "收藏")
        flag = gcp.is_toast_exist("已收藏")
        self.assertTrue(flag)
        # 删除群聊消息记录
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除聊天记录
        gcsp.click_clear_chat_record()
        gcsp.wait_clear_chat_record_confirmation_box_load()
        # 点击确认
        gcsp.click_determine()
        # flag = gcsp.is_toast_exist("聊天记录清除成功")
        # self.assertTrue(flag)
        time.sleep(3)
        # 点击返回群聊页面
        gcsp.click_back()
        time.sleep(2)
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # time.sleep(2)
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        #进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me=MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp=MeCollectionPage()
        mcp.click_text("哈哈")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        mcp.click_back()
        time.sleep(2)
        #左滑收藏消息体
        mcp.press_and_move_left()
        #判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
            time.sleep(1)
            mcp.click_back()
            mess.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0018(self):
        """在聊天会话页面，长按语音消息，使用收藏功能"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            #点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("收藏")
        if not gcp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("秒"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp=MeCollectionPage()
        mcp.click_text("秒")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        #播放语音消息
        mcp.click_collection_voice_msg()
        time.sleep(2)
        #暂停语音消息
        mcp.click_collection_voice_msg()
        mcp.click_back()
        time.sleep(2)
        # 左滑收藏消息体
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            time.sleep(2)
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
        mcp.click_back()
        mess.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0133(self):
        """在群聊天会话页面，长按消息体，点击收藏"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 1、长按消息体，会弹出功能列表
        # 2、点击收藏，收藏成功，会提示：已收藏
        # flag = gcp.is_toast_exist("收藏")
        # self.assertTrue(flag)
        # 长按信息并点击收藏
        gcp.press_file_to_do("哈哈", "收藏")
        flag = gcp.is_toast_exist("已收藏")
        self.assertTrue(flag)

    def tearDown_test_msg_huangmianhua_0133(self):
        gcp = GroupChatPage()
        # 删除群聊消息记录
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除聊天记录
        gcsp.click_clear_chat_record2()
        gcsp.wait_clear_chat_record_confirmation_box_load()
        # 点击确认
        gcsp.click_determine()

    @staticmethod
    def setUp_test_msg_huangmianhua_0134():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0134(self):
        """我——收藏——收藏内容展示"""
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        # 1、我——收藏——收藏内容展示列表
        # 2、收藏内容展示：内容来源、收藏时间、收藏内容（部分或全部）
        # '我' locator
        exists = me.is_text_present("哈哈")
        self.assertEquals(exists, True)
        collection_page = MeCollectionPage()
        exists = collection_page.element_contain_text("我", Preconditions.get_group_chat_name())
        self.assertEquals(exists, True)
        collection_page.click_back()

    @staticmethod
    def setUp_test_msg_huangmianhua_0135():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0135(self):
        """我——收藏——收藏内展示——点击收藏内容"""
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("哈哈")
        time.sleep(1)
        # 1、收藏内容展示列表，点击收藏内容，会跳转到收藏内容详情页面
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        mcp.click_back()
        time.sleep(1)
        if not mcp.is_text_present("收藏"):
            raise AssertionError("不能返回到收藏列表展示页面")

    @staticmethod
    def setUp_test_msg_huangmianhua_0136():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0136(self):
        """我——收藏——收藏内展示——点击收藏内容——点击播放收藏语音文件"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("收藏")
        if not gcp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(1)
        if not me.is_text_present("秒"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("秒")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        # 播放语音消息
        mcp.click_collection_voice_msg()
        time.sleep(2)
        # 暂停语音消息
        mcp.click_collection_voice_msg()
        mcp.click_back()
        time.sleep(2)
        mcp.click_back()
        me.open_message_page()

    @staticmethod
    def setUp_test_msg_huangmianhua_0137():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0137(self):
        """我——收藏——收藏内展示——点击收藏内容——点击删除收藏内容"""
        gcp = GroupChatPage()
        time.sleep(2)
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(2)
        # 左滑收藏消息体
        mcp = MeCollectionPage()
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            time.sleep(2)
            #判断是否会弹出确认弹窗
            if not mcp.is_text_present("确定"):
                raise AssertionError("没有弹出确认窗口")
            #点击取消
            mcp.click_cancel_forward()
            flag=mcp.is_delete_element_present()
            self.assertTrue(flag)
            time.sleep(1)
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            time.sleep(2)
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
        else:
            raise AssertionError("没有删除按钮")
        mcp.click_back()
        me.open_message_page()

    @staticmethod
    def setUp_test_msg_huangmianhua_0152():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0152(self):
        """在群聊会话窗口，点击页面顶部的通话按钮"""
        # 1、点击页面顶部的通话按钮，是否会调起通话选择项弹窗
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_mutilcall()
        time.sleep(2)
        if not gcp.is_text_present("多方视频"):
            raise AssertionError("不会调起通话选择项弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])

    @staticmethod
    def setUp_test_msg_huangmianhua_0153():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0153(self):
        """在群聊会话窗口，点击通话按钮——拨打多方电话"""
        # 1、点击页面顶部的通话按钮，是否会调起通话选择项弹窗
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_mutilcall()
        time.sleep(2)
        lgdp = GroupChatPage()
        lgdp.click_hf_tel()
        time.sleep(1)
        exsit = gcp.is_text_present("搜索成员")
        self.assertEqual(exsit, True)

    @staticmethod
    def setUp_test_msg_huangmianhua_0154():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0154(self):
        """在群聊会话窗口，点击通话按钮——拨打多方视频"""
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_mutilcall()
        time.sleep(2)
        lgdp = GroupChatPage()
        lgdp.click_multi_videos()
        mess = MessagePage()
        for i in range(2):
            print(" i ==== " + str(i))
            if gcp.is_text_present("始终允许"):
                mess.click_text("始终允许")
                time.sleep(2)
        time.sleep(1)
        exsit = gcp.is_text_present("搜索成员")
        self.assertEqual(exsit, True)

    @staticmethod
    def setUp_test_msg_huangmianhua_0155():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0155(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""
        # 1、点击输入框上方的图片ICON，是否可以进入到相册列表页
        # 2、任意选中一张照片，点击右下角的发送按钮，是否可以发送成功
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        if gcp.is_text_present("退出"):
            audio = ChatAudioPage()
            audio.click_exit()
            time.sleep(2)
        gcp.click_picture()
        time.sleep(2)
        # 1、点击输入框上方的图片ICON，可以进入到相册列表页
        if not gcp.is_text_present("原图"):
            raise AssertionError("不可以进入到相册列表页")
        gcp.select_picture()
        time.sleep(2)
        gcp.click_text("发送")
        # 2、任意选中一张照片，点击右下角的发送按钮，可以发送成功
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @staticmethod
    def setUp_test_msg_huangmianhua_0156():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0156(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 1、点击页面顶部的通话按钮，是否会调起通话选择项弹窗
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        gcp.click_take_picture2()
        time.sleep(2)
        chat_photo = ChatPhotoPage()
        # 1、点击输入框上方的相机ICON,可以正常调起相机操作页
        # Checkpoint 可以正常调起相机操作页
        chat_photo.wait_for_page_load()
        # Step 轻触拍摄按钮
        chat_photo.take_photo()
        # 2、轻触拍摄按钮，会拍摄成功一张照片
        # 3、点击右下角的“√”按钮，可以发送成功
        chat_photo.send_photo()
        time.sleep(5)
        # Checkpoint 可以发送成功
        gcp.is_exist_pic_msg()

    @staticmethod
    def setUp_test_msg_huangmianhua_0157():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0157(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 1、点击页面顶部的通话按钮，是否会调起通话选择项弹窗
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        gcp.click_take_picture2()
        time.sleep(2)
        chat_photo = ChatPhotoPage()
        # 1、点击输入框上方的相机ICON,可以正常调起相机操作页
        chat_photo.wait_for_page_load()
        # 2、长按拍摄按钮，会进入到录像功能
        chat_photo.record_video(5000)
        # 3、录制时间超过1秒钟后，松手，会录制成功的视频
        # 4、点击右下角的“√”按钮，可以发送成功
        chat_photo.send_photo()
        time.sleep(5)
        # Checkpoint 可以发送成功
        gcp.is_exist_video_msg()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0167(self):
        """消息草稿-聊天列表显示-输入空格消息"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、再输入空格不发送返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        info = " "
        gcp.input_message(info)
        gcp.click_back()
        # 聊天页面显示群聊会话窗口页最新一条消息预览，无[草稿]标识
        mess = MessagePage()
        if mess.is_on_this_page():
            if mess.is_text_present("草稿"):
                raise AssertionError("有草稿标识出现")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0168(self):
        """消息草稿-聊天列表显示-不输入任何消息"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        info = ""
        gcp.input_message(info)
        if gcp.is_on_this_page():
            if gcp.is_element_exit_("文本发送按钮"):
                raise AssertionError("有发送按钮")
        gcp.click_back()
        mess = MessagePage()
        if mess.is_on_this_page():
            if mess.is_text_present("草稿"):
                raise AssertionError("有草稿标识出现")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0169(self):
        """消息草稿-聊天列表显示-输入文本信息"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 1、发送按钮高亮，可点击
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 2、聊天页面显示输入文本信息预览，有[草稿]标识并标红
        info = "测试未发送信息"
        gcp.input_message(info)
        # if gcp.is_on_this_page():
        #     if gcp.is_element_exit_("文本发送按钮"):
        #         raise AssertionError("有发送按钮")
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            exists =mess.is_text_present("草稿")
            self.assertEquals(exists, True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0170(self):
        """消息草稿-聊天列表显示-输入表情信息"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("[微笑1]")
        # 点击发送
        gcp.send_message()
        # 1、发送按钮高亮，可点击
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 2、聊天页面显示输入文本信息预览，有[草稿]标识并标红
        info = "[微笑1]"
        gcp.input_message(info)
        # if gcp.is_on_this_page():
        #     if gcp.is_element_exit_("文本发送按钮"):
        #         raise AssertionError("有发送按钮")
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0171(self):
        """消息草稿-聊天列表显示-输入特殊字符"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("#$%*&")
        # 点击发送
        gcp.send_message()
        # 1、发送按钮高亮，可点击
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 2、聊天页面显示输入文本信息预览，有[草稿]标识并标红
        info = "#$%*&"
        gcp.input_message(info)
        # if gcp.is_on_this_page():
        #     if gcp.is_element_exit_("文本发送按钮"):
        #         raise AssertionError("有发送按钮")
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0172(self):
        """消息草稿-聊天列表显示-输入空格消息-网络异常"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message(" ")
        # 点击发送
        gcp.send_message()
        # 1、发送按钮高亮，可点击
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            # 控信息是发送不成功的
            # raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            pass
        # 2、聊天页面显示输入文本信息预览，有[草稿]标识并标红
        info = " "
        gcp.input_message(info)
        # if gcp.is_on_this_page():
        #     if gcp.is_element_exit_("文本发送按钮"):
        #         raise AssertionError("有发送按钮")
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0173(self):
        """消息草稿-聊天列表显示-输入文本信息-网络异常"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 1、发送按钮高亮，可点击
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 2、聊天页面显示输入文本信息预览，有[草稿]标识并标红
        info = "测试未发送信息"
        gcp.input_message(info)
        # if gcp.is_on_this_page():
        #     if gcp.is_element_exit_("文本发送按钮"):
        #         raise AssertionError("有发送按钮")
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0174(self):
        """消息草稿-聊天列表显示-草稿信息发送成功"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        gcp.click_back()
        time.sleep(1)
        # 1、保存为草稿信息
        # 2、消息列表，显示[草稿]标红字
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, True)
        # 点击群名，进入群聊页面
        sogp = SelectOneGroupPage()
        group_name = Preconditions.get_group_chat_name()
        sogp.click_one_contact(group_name)
        scp = GroupChatPage()
        scp.wait_for_page_load()

        # 点击发送
        gcp.send_message()
        # 3、消息发送成功
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_back()
        time.sleep(1)
        # 4、消息列表[草稿]标红字样消失，显示为正常消息预览
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0175(self):
        """消息草稿-聊天列表显示-草稿信息删除"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        gcp.click_back()
        time.sleep(1)
        # 1、保存为草稿信息
        # 2、消息列表，显示[草稿]标红字
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, True)
        # 点击群名，进入群聊页面
        sogp = SelectOneGroupPage()
        group_name = Preconditions.get_group_chat_name()
        sogp.click_one_contact(group_name)
        scp = GroupChatPage()
        scp.wait_for_page_load()
        # 3、草稿信息删除成功。清空信息
        gcp.input_message("")
        gcp.click_back()
        time.sleep(1)
        #4、消息列表[草稿]标红字样消失，显示为最近一次消息预览
        mess = MessagePage()
        if mess.is_on_this_page():
            exists = mess.is_text_present("草稿")
            self.assertEquals(exists, False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    @staticmethod
    def setUp_test_msg_xiaoqiu_0056():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC-RESET', 'group_chat','4281','high')
    def test_msg_xiaoqiu_0056(self):
        """未获取权限时，点击输入框右边的语音按钮，检查是否会弹出提示权限"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        flag = audio.wait_for_audio_allow_page_load()
        self.assertTrue(flag)
        audio.click_allow()
        audio.wait_until(condition=lambda d: audio.is_text_present("退出"))
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','4281','high')
    def test_msg_xiaoqiu_0057(self):
        """首次使用语音功能"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        audio.click_send_bottom()
        time.sleep(1)
        audio.click_setting_bottom()
        time.sleep(1)
        # flag = audio.wait_for_audio_type_select_page_load()
        # self.assertTrue(flag)
        # 2、默认展示的选择项是否是，语音+文字模式
        # info = audio.get_selected_item()
        # self.assertIn("语音+文字", info)
        flag=audio.get_audio_and_text_icon_selected()
        self.assertTrue(flag)
        audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0021(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_text("说点什么...")
            time.sleep(2)
            audio.hide_keyboard()
            raise AssertionError("不会提示‘无法识别，请重试’")
        audio.click_text("说点什么...")
        time.sleep(2)
        audio.hide_keyboard()


    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0022(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        # 断开网络
        gcp.set_network_status(0)
        time.sleep(10)
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if gcp.is_text_present("请选择您偏好的语音发送模式:"):
            audio.click_text("确定")
            time.sleep(2)
            audio.click_text("始终允许")
            time.sleep(2)
        if audio.is_text_present("我知道了"):
            audio.click_i_know()
        time.sleep(2)
        if not audio.is_text_present("网络不可用，请检查网络设置"):
            audio.click_text("说点什么...")
            time.sleep(2)
            audio.hide_keyboard()
            raise AssertionError("不会提示‘网络不可用，请检查网络设置’")
        audio.click_text("说点什么...")
        time.sleep(2)
        audio.hide_keyboard()
        time.sleep(2)

    def tearDown_test_msg_common_group_0022(self):
        #重新连接网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0023(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_text("说点什么...")
            time.sleep(2)
            audio.hide_keyboard()
            raise AssertionError("不会提示‘无法识别，请重试’")
        audio.click_text("说点什么...")
        time.sleep(2)
        audio.hide_keyboard()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0028(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(2)
        audio = ChatAudioPage()
        audio.click_exit()
        if audio.is_text_present("智能识别中"):
            raise AssertionError("不会退出语音识别模式")
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0030(self):
        """语音转文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_text("说点什么...")
            time.sleep(2)
            audio.hide_keyboard()
            raise AssertionError("不会提示‘无法识别，请重试’")
        audio.click_text("说点什么...")
        time.sleep(2)
        audio.hide_keyboard()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0031(self):
        """语音转文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_text("说点什么...")
            time.sleep(2)
            audio.hide_keyboard()
            raise AssertionError("不会提示‘无法识别，请重试’")
        audio.click_text("说点什么...")
        time.sleep(2)
        audio.hide_keyboard()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    @unittest.skip("容易受外界干扰运行失败，不连跑")
    def test_msg_common_group_0036(self):
        """仅语音模式发送语音消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        audio.click_send_bottom()
        audio.click_setting_bottom()
        if audio.wait_for_audio_type_select_page_load():
            #点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        else:
            raise AssertionError("语音模式选择页面加载失败")
        time.sleep(2)
        audio.click_exit()
        time.sleep(1)
        if gcp.is_text_present("语音录制中"):
            raise AssertionError("退出语音录制模式失败")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428')
    def test_msg_common_group_0039(self):
        """放大发送文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #判断文本是否放大,‘哈哈’文本框信息正常宽度为163
        if not gcp.get_width_of_msg_of_text()>136:
            raise AssertionError("文本消息没有放大展示")

    def tearDown_test_msg_common_group_0039(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428')
    def test_msg_common_group_0040(self):
        """缩小发送文本消息"""
        gcp = GroupChatPage()
        #获取文本信息正常的宽度
        info = "哈哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width=gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428')
    def test_msg_common_group_0041(self):
        """发送一串号码到聊天会话页面"""
        gcp = GroupChatPage()
        # 输入信息
        info = "123456"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428')
    def test_msg_common_group_0042(self):
        """点击聊天会话页面中的一组号码数字"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        info = "123456"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_text("123456")
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("不会弹出呼叫，复制号码窗体")
        gcp.click_text("呼叫")
        time.sleep(5)
        if gcp.is_text_present('始终允许'):
            gcp.click_text("始终允许")
        time.sleep(5)
        if gcp.is_text_present('始终允许'):
            gcp.click_text("始终允许")
        time.sleep(2)
        #判断是否可以发起呼叫
        if not gcp.is_phone_in_calling_state():
            raise AssertionError("不可以发起呼叫")
        time.sleep(1)
        #点击结束呼叫按钮
        gcp.hang_up_the_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_xiaoqiu_0044(self):
        """发送一组数字：12345678900，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "12345678900"
        gcp.input_message(info)
        if gcp.is_keyboard_shown():
            gcp.hide_keyboard()
        time.sleep(1)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #判断是否被识别为号码
        gcp.click_text("12345678900")
        time.sleep(1)
        if gcp.is_text_present("呼叫"):
            raise AssertionError("12345678900被识别为号码,点击有弹窗")

    def tearDown_test_msg_xiaoqiu_0044(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_xiaoqiu_0045(self):
        """发送一组数字：123456，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "123456"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("123456")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("123456不被识别为号码,点击没有弹窗")
        time.sleep(1)
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_xiaoqiu_0046(self):
        """发送一组数字：18431931414，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "18431931414"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("18431931414")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("18431931414不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_xiaoqiu_0047(self):
        """发送一组数字：+85267656003，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "+85267656003"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("+85267656003")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("+85267656003不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_xiaoqiu_0048(self):
        """发送一组数字：67656003，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "67656003"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("67656003")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("67656003不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_xiaoqiu_0049(self):
        """发送一组数字：95533，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "95533"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("95533")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("95533不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','428','high')
    def test_msg_common_group_0049(self):
        """点击聊天会话页面中的一组非号码数字"""
        gcp = GroupChatPage()
        # 输入非号码数字
        info = "36363"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("36363")
        time.sleep(1)
        if gcp.is_text_present("呼叫"):
            raise AssertionError("36363被识别为号码,点击有弹窗")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0050(self):
        """在聊天会话页面，点击右上角的聊天设置按钮"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0051(self):
        """聊天设置页面，添加一个群成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击“+”按钮
        gcsp.click_add_member()
        contacts_page = SelectLocalContactsPage()
        #未选择联系人时，右上角的确定按钮是否置灰展示
        if contacts_page.is_text_present("确定(1/499)"):
            raise AssertionError("未选择联系人时，右上角的确定按钮没有置灰展示")
        time.sleep(2)
        contacts_page.click_back()
        time.sleep(1)
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0052(self):
        """聊天设置页面，添加一个群成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp=ChatGroupAddContactsPage()
        # contactNnames=cgacp.get_contacts_name()
        # if contactNnames:
        #     #选择一个联系人
        #     cgacp.select_one_member_by_name(contactNnames[0])
        # else:
        #     raise AssertionError("通讯录没有联系人，请添加")
        cgacp.click_one_contact("飞信电话")
        time.sleep(1)
        if not cgacp.sure_btn_is_enabled():
            raise AssertionError("右上角的确定按钮不能高亮展示")
        cgacp.click_sure()
        time.sleep(2)
        gcp.page_should_contain_text("发出群邀请")

    def tearDown_test_msg_common_group_0052(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0053(self):
        """聊天设置页面，添加多个成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        contactNnames = cgacp.get_contacts_name()
        if len(contactNnames)>1:
            # 选择多个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
            cgacp.select_one_member_by_name(contactNnames[1])
        else:
            raise AssertionError("通讯录联系人数量不足，请添加")
        cgacp.click_sure()
        time.sleep(2)
        gcp.page_should_contain_text("发出群邀请")

    def tearDown_test_msg_common_group_0053(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0059(self):
        """聊天设置页面，添加501个成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        contactNnames = cgacp.get_contacts_name()
        if contactNnames:
            # 选择一个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
        else:
            raise AssertionError("通讯录没有联系人，请添加")
        cgacp.click_sure()
        time.sleep(2)
        gcp.is_toast_exist("发出群邀请")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0060(self):
        """聊天设置页面，进入到成员移除页面"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“-”按钮
        gcsp.click_del_member()
        time.sleep(3)
        if gcsp.is_text_present("移除群成员"):
            raise AssertionError("在一人情况下还可以进入移除群成员页面")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0065(self):
        """聊天设置页面，修改群名称"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        if gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有置灰展示")
        gcsp.click_edit_group_name_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0066(self):
        """聊天设置页面，修改群名称"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        #录入新群名
        gcsp.input_new_group_name("NGN")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()
        #恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        group_name = Preconditions.get_group_chat_name()
        gcsp.input_new_group_name(group_name)
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0067(self):
        """聊天设置页面，修改群名片，清除旧名称"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        gcsp.input_new_group_name("aa")
        #判断是否有“X”按钮
        if gcsp.is_iv_delete_exit():
            #点击“X”按钮
            gcsp.click_iv_delete_button()
            time.sleep(1)
            #判断是否清除成功
            if not gcsp.is_text_present("设置你在群内显示的昵称"):
                raise AssertionError("旧群名片不能清除成功")
            #判断右上角的按钮是否置灰展示
            if gcsp.is_enabled_of_group_card_save_button():
                raise AssertionError("名称修改框为空时，右上角的完成按钮没有置灰展示")
        else:
            raise AssertionError("没有找到“X”按钮")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0068(self):
        """聊天设置页面，修改群名片，录入10个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        gcsp.input_new_group_name("哈哈哈哈哈哈哈哈哈哈")
        #判断按钮是否高亮展示
        if gcsp.is_enabled_of_group_card_save_button():
            gcsp.save_group_card_name()
            gcsp.is_toast_exist("修改成功")
            time.sleep(2)
            #验证上面输入的名称内容都保存
            gcsp.click_my_card()
            time.sleep(1)
            if not gcsp.get_edit_query_text()=="哈哈哈哈哈哈哈哈哈哈":
                raise AssertionError("不可以保存输入的名称内容")
            gcsp.click_edit_group_card_back()
            gcsp.click_back()
        else:
            raise AssertionError("按钮不会高亮展示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0069(self):
        """聊天设置页面，修改群名片，录入11个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        gcsp.input_new_group_name("哈哈哈哈哈哈哈哈哈哈哈")
        time.sleep(1)
        text=gcsp.get_edit_query_text()
        if text=="哈哈哈哈哈哈哈哈哈哈哈":
            raise AssertionError("可录入11个汉字")
        else:
            if not text=="哈哈哈哈哈哈哈哈哈哈":
                raise AssertionError("录入的汉字最多不是10个")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0070(self):
        """聊天设置页面，修改群名片，录入30个英文字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName="h"*30
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if not gcsp.get_edit_query_text()==newName:
            raise AssertionError("录入30个英文字符不可以录入成功")
        gcsp.save_group_card_name()
        gcsp.is_toast_exist("修改成功")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0071(self):
        """聊天设置页面，修改群名片，录入31个英文字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "j" * 31
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if gcsp.get_edit_query_text() == newName:
            raise AssertionError("可以录入31个英文字符")
        if not gcsp.get_edit_query_text()=="j"*30:
            raise AssertionError("无法最多录入30个英文字符")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0072(self):
        """聊天设置页面，修改群名片，录入30个数字字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "1" * 30
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if not gcsp.get_edit_query_text() == newName:
            raise AssertionError("录入30个英文字符不可以录入成功")
        gcsp.save_group_card_name()
        gcsp.is_toast_exist("修改成功")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0073(self):
        """聊天设置页面，修改群名片，录入中文、英文、数字字符（小于等于30个字符）"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "aa11嗯嗯"
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if not gcsp.get_edit_query_text() == newName:
            raise AssertionError("录入30个英文字符不可以录入成功")
        gcsp.save_group_card_name()
        gcsp.is_toast_exist("修改成功")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0074(self):
        """聊天设置页面，修改群名片、录入特殊字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        # gcsp.click_iv_delete_button()
        newName = "_(:3」∠❀)_"
        gcsp.input_new_group_name(newName)
        if not gcsp.is_toast_exist("不能包含特殊字符和表情"):
            raise AssertionError("输入特殊字符也可以录入成功")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0075(self):
        """聊天设置页面，分享群二维码"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击群二维码
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_qecode_download_button()
        if not gcsp.is_toast_exist("已保存"):
            raise AssertionError("群二维码保存失败")
        gcsp.click_qecode_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0076(self):
        """聊天设置页面，分享群二维码"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群二维码
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_qecode_share_button()
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_back()
        gcsp.click_qecode_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0077(self):
        """聊天设置页面，分享群二维码"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群二维码
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_qecode_share_button()
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.select_local_contacts()
        sc.click_one_contact("飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        gcsp.click_qecode_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0078(self):
        """聊天设置页面，转让群聊"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击群管理
        gcsp.click_group_manage()
        gcsp.wait_for_group_manage_load()
        #点击群主管理权转让
        gcsp.click_group_manage_transfer_button()
        flag = gcsp.is_toast_exist("暂无群成员")
        self.assertTrue(flag)
        gcsp.click_group_manage_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0081(self):
        """聊天设置页面，解散群聊"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_group_manage()
        gcsp.wait_for_group_manage_load()
        #点击解散群
        gcsp.click_group_manage_disband_button()
        time.sleep(3)
        # if not gcsp.is_text_present("解散群后，所有成员将被移出此群"):
        #     raise AssertionError("不会弹出确认弹窗")
        #点击取消
        gcsp.click_cancel()
        time.sleep(1)
        if not gcsp.is_text_present("群管理"):
            raise AssertionError("点击取消，不能停留在群管理页面")
        gcsp.click_group_manage_disband_button()
        #点击确定
        gcsp.click_sure()
        if not gcsp.is_toast_exist("该群已解散"):
            raise AssertionError("没有toast提示该群已解散")
        sog = SelectOneGroupPage()
        time.sleep(2)
        if sog.is_on_this_page():
            sog.click_back()
            sc = SelectContactsPage()
            sc.click_back()
        time.sleep(2)
        msg=MessagePage()
        if not msg.is_text_present("该群已解散"):
            raise AssertionError("没有系统消息通知该群已解散")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0087(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击查找聊天内容
        gcsp.click_find_chat_record()
        #点击搜索框
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        search.click_edit_query()
        #判断键盘是否调起
        if not search.is_keyboard_shown():
            raise AssertionError("不可以调起小键盘")
        search.click_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0088(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        #输入搜索信息
        search.input_search_message("哈哈")
        #判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        #任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("哈哈"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    def tearDown_test_msg_common_group_0088(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0089(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("123")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        # 输入搜索信息
        search.input_search_message("123")
        # 判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        # 任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("123"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    def tearDown_test_msg_common_group_0089(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0090(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("abc")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        # 输入搜索信息
        search.input_search_message("abc")
        # 判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        # 任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("abc"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    def tearDown_test_msg_common_group_0090(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            # flag=gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0091(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("$%&")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        # 输入搜索信息
        search.input_search_message("$%&")
        # 判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        # 任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("$%&"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0092(self):
        """聊天设置页面，清空聊天记录"""
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击取消
            gcsp.click_cancel()
            time.sleep(1)
            if not gcsp.is_text_present("群聊设置"):
                raise AssertionError("弹窗消失后不会停留在聊天设置页面")
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            # flag = gcsp.is_toast_exist("聊天记录清除成功")
            # self.assertTrue(flag)
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
            #验证聊天内容已经被清除
            if scp.is_text_present("$%&"):
                raise AssertionError("聊天内容记录没有被清除")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','xin')
    def test_msg_common_group_0094(self):
        """聊天设置页面，删除并退出群聊"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击“删除并退出”按钮
        if not gcsp.is_text_present("删除并退出"):
            gcsp.page_up()
        gcsp.click_delete_and_exit2()
        time.sleep(3)
        #验证弹出弹窗
        # if not gcsp.is_text_present("退出后不会再接收该群消息"):
        #     raise AssertionError("没有弹出确认弹窗")
        #点击取消
        gcsp.click_cancel()
        time.sleep(1)
        if gcsp.is_text_present("退出后不会再接收该群信息"):
            raise AssertionError("不可以关闭弹窗")
        #点击确定
        gcsp.click_delete_and_exit2()
        time.sleep(1)
        gcsp.click_sure()
        if not gcsp.is_toast_exist("已退出群聊"):
            raise AssertionError("没有toast提示已退出群聊")
        time.sleep(1)
        sog = SelectOneGroupPage()
        if sog.is_on_this_page():
            sog.click_back()
            sc = SelectContactsPage()
            sc.click_back()
        time.sleep(2)
        mess=MessagePage()
        if not mess.is_on_this_page():
            raise AssertionError("退出当前群聊没有返回到消息列表")
        mess.click_element_by_text("系统消息")
        time.sleep(1)
        if not mess.is_text_present("你已退出群"):
            raise AssertionError("没有系统消息：你已退出群")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0096(self):
        """聊天窗口，发送表情"""
        gcp = GroupChatPage()
        #点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        #判断是否可以展示表情页
        if not gcp.is_exist_expression_page():
            raise AssertionError("不可以展示表情页")
        #任意点击一个表情
        els=gcp.get_expressions()
        els[0].click()
        inputText=gcp.get_input_box().get_attribute("text")
        if not inputText==els[0].get_attribute("text"):
            raise AssertionError("被选中的表情不可以存放输入框展示")
        time.sleep(1)
        #清空输入框内容
        gcp.get_input_box().clear()
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0097(self):
        """聊天窗口，发送表情"""
        gcp = GroupChatPage()
        # 点击表情按钮
        gcp.click_expression_button()
        els = gcp.get_expressions()
        a=0
        while a<3:
            els[0].click()
            a+=1
        #判断发送按钮是否高亮
        if not gcp.is_enabled_of_send_button():
            raise AssertionError("发送按钮不可高亮展示")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    def tearDown_test_msg_common_group_0097(self):
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
                # flag = gcsp.is_toast_exist("聊天记录清除成功")
                # self.assertTrue(flag)
                time.sleep(3)
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0098(self):
        """聊天窗口，发送表情"""
        gcp = GroupChatPage()
        # 点击表情按钮
        if gcp.is_element_exit_("关闭表情页"):
            gcp.click_expression_page_close_button()
        time.sleep(2)
        gcp.click_expression_button()
        time.sleep(2)
        # 判断是否可以展示表情页
        if not gcp.is_exist_expression_page():
            raise AssertionError("不可以展示表情页")
        #连续点击多个表情
        els = gcp.get_expressions()
        a = 0
        while a < 3:
            els[0].click()
            a += 1
        inputText = gcp.get_input_box().get_attribute("text")
        if not inputText==els[0].get_attribute("text")*3:
            raise AssertionError("被选中的表情不可以存放输入框展示")
        time.sleep(1)
        # 清空输入框内容
        gcp.get_input_box().clear()
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin','high')
    def test_msg_common_group_0099(self):
        """聊天窗口，放大发送表情"""
        gcp = GroupChatPage()
        # 点击表情按钮
        if gcp.is_element_exit_("关闭表情页"):
            gcp.click_expression_page_close_button()
        time.sleep(2)
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        inputText = gcp.get_input_box().get_attribute("text")
        if not inputText == els[0].get_attribute("text"):
            raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

        # 判断是否缩小,一个表情文本框信息正常宽度为107
        if not gcp.get_width_of_msg_of_text() > 107:
            raise AssertionError("表情没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    def tearDown_test_msg_common_group_0099(self):
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
                # flag = gcsp.is_toast_exist("聊天记录清除成功")
                # self.assertTrue(flag)
                time.sleep(3)
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin','high')
    def test_msg_common_group_0100(self):
        """聊天窗口，缩小发送表情"""
        gcp = GroupChatPage()
        # 获取文本信息正常的宽度
        if gcp.is_element_exit_("关闭表情页"):
            gcp.click_expression_page_close_button()
        time.sleep(2)
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()
        time.sleep(2)


        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        inputText = gcp.get_input_box().get_attribute("text")
        if not inputText == els[0].get_attribute("text"):
            raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

        # 判断是否缩小,一个表情文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("表情没有缩小展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    def tearDown_test_msg_common_group_0100(self):
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
                # flag = gcsp.is_toast_exist("聊天记录清除成功")
                # self.assertTrue(flag)
                time.sleep(3)
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0101(self):
        """聊天会话窗口的批量选择器页面展示"""
        gcp = GroupChatPage()
        if gcp.is_element_exit_("关闭表情页"):
            gcp.click_expression_page_close_button()
        time.sleep(2)
        # 输入信息
        dex=0
        while dex<3:
            messgage="哈哈"+str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex+=1
        gcp.press_file_to_do("哈哈0","多选")
        #显示左上角的【×】关闭按钮，有勾选消息时，左上角文案展示为： 已选择+数量
        if not gcp.is_exist_multiple_selection_back():
            raise AssertionError("没有显示【×】关闭按钮")
        #验证有勾选信息
        els=gcp.get_multiple_selection_select_box()
        if els[0].get_attribute("checked")=="true":
            if gcp.is_exist_multiple_selection_count():
                if not gcp.is_text_present("已选择"):
                    raise AssertionError("没有显示‘已选择+数量’字样")
            else:
                raise AssertionError("没有显示‘已选择+数量’字样")
            #底部删除、转发按钮，高亮展示
            if not gcp.is_enabled_multiple_selection_delete():
                raise AssertionError("勾选信息后底部删除按钮没有高亮展示")
            if not gcp.is_enabled_multiple_selection_forward():
                raise AssertionError("勾选信息后底部转发按钮没有高亮展示")
        else:
            raise AssertionError("没有勾选信息")
        #取消勾选信息
        els[0].click()
        time.sleep(1)
        #未选择任何消息时，左上角文案展示为：未选择，底部删除，转发按钮默认置灰展示
        if not gcp.is_text_present("未选择"):
            raise AssertionError("未选择任何消息时没有展示‘未选择’")
        # 底部删除、转发按钮，置灰展示
        if gcp.is_enabled_multiple_selection_delete():
            raise AssertionError("未勾选信息后底部删除按钮没有置灰展示")
        if gcp.is_enabled_multiple_selection_forward():
            raise AssertionError("未勾选信息后底部转发按钮没有置灰展示")
        gcp.click_multiple_selection_back()

    def tearDown_test_msg_common_group_0101(self):
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
                # flag = gcsp.is_toast_exist("聊天记录清除成功")
                # self.assertTrue(flag)
                time.sleep(3)
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0102(self):
        """下拉是否可加载历史消息"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 30:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            current_mobile().hide_keyboard_if_display()
            # 点击发送
            time.sleep(1)
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.click_back()
        time.sleep(1)
        groupName=Preconditions.get_group_chat_name()
        gcp.click_text(groupName)
        time.sleep(1)
        gcp.press_file_to_do("哈哈26", "多选")
        a=0
        while a<5:
            gcp.page_down()
            a+=1
        time.sleep(2)
        if not gcp.is_text_present("跳转到最新消息"):
            raise AssertionError("下滑加载历史信息不成功")
        gcp.click_multiple_selection_back()

    def tearDown_test_msg_common_group_0102(self):
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
                # flag = gcsp.is_toast_exist("聊天记录清除成功")
                # self.assertTrue(flag)
                time.sleep(3)
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0103(self):
        """取消多选模式"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        gcp.click_multiple_selection_back()
        if gcp.is_exist_multiple_selection_select_box():
            raise AssertionError("复选框没有消失")
        #转发操作选项直接消失
        if gcp.is_text_present("转发"):
            raise AssertionError("转发操作选项没有消失")
        #出现底部聊天输入框
        if not gcp.is_text_present("说点什么..."):
            raise AssertionError("底部聊天输入框没有出现")
        #返回到聊天会话窗口
        if not gcp.is_on_this_page():
            raise AssertionError("没有返回到聊天会话窗口")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0104(self):
        """转发默认选中项（1条）—如下消息体是不支持转发的类型（①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体）"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        time.sleep(1)
        gcp.press_file_to_do("哈哈0", "多选")
        gcp.click_text("转发")
        time.sleep(2)
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("不符合UI设计")
        scp=SelectContactsPage()
        scp.click_back()
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0105(self):
        """转发默认选中项（1条）—如下消息体是不支持转发的类型（①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体）"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        time.sleep(1)
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        sc.click_cancel_forward()
        sc.click_back()
        sc.click_back()
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0106(self):
        """转发默认选中项（1条）—当消息体是支持转发的类型——网络正常转发"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX','xin')
    def test_msg_common_group_0108(self):
        """转发默认选中项（1条）—删除"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        #点击删除
        gcp.click_multiple_selection_delete()
        #点击确定
        gcp.click_multiple_selection_delete_sure()
        flag = gcp.is_toast_exist("删除成功")
        self.assertTrue(flag)
        if gcp.is_text_present("哈哈0"):
            raise AssertionError("删除掉的消息体没有删除成功")

    def tearDown_test_msg_common_group_0108(self):
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
                # flag = gcsp.is_toast_exist("聊天记录清除成功")
                # self.assertTrue(flag)
                time.sleep(3)
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX',"aa",'xin')
    def test_msg_common_group_0109(self):
        """转发默认选中项（1条）—取消删除"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        # 点击删除
        gcp.click_multiple_selection_delete()
        # 点击取消
        gcp.click_multiple_selection_delete_cancel()
        #验证选中的消息体还是选中状态
        els = gcp.get_multiple_selection_select_box()
        if not els[0].get_attribute("checked")=="true":
            raise AssertionError("选中的消息体不是选中状态")
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX',"aa",'xin')
    def test_msg_common_group_0110(self):
        """取消默认选中项"""
        gcp = GroupChatPage()
        gcp.press_file_to_do("哈哈0", "多选")
        els=gcp.get_multiple_selection_select_box()
        if els:
            els[0].click()
        else:
            raise AssertionError("没有找到复选框")
        time.sleep(1)
        if not gcp.is_text_present("未选择"):
            raise AssertionError("标题没有变化为“未选择”")
        #验证删除和转发按钮是否置灰
        if gcp.is_enabled_multiple_selection_delete():
            raise AssertionError("删除按钮没有置灰")
        if gcp.is_enabled_multiple_selection_forward():
            raise AssertionError("转发按钮没有置灰")
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX',"aa",'xin')
    def test_msg_common_group_0111(self):
        """选择多条消息体"""
        gcp = GroupChatPage()
        gcp.press_file_to_do("哈哈0", "多选")
        #点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        #验证其他复选框被选中
        if not els[1].get_attribute("checked")=="true" and els[2].get_attribute("checked")=="true":
            raise AssertionError("点击的消息体没有被选中")
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @staticmethod
    def setUp_test_msg_common_group_0112():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC-RESET', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0112(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1

        # 发送语音
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()

        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
            els[3].click()
        else:
            raise AssertionError("没有找到复选框")
        time.sleep(1)
        #点击转发
        gcp.click_multiple_selection_forward()
        #点击取消
        gcp.click_cancel_repeat_msg()
        #验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
           raise AssertionError("点击取消没有停留在批量选择器页面")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击确定
        gcp.click_sure_repeat_msg()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        #验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
           raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # time.sleep(2)
        # sogp.click_back()
        # sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            if chat.is_audio_exist():
                raise AssertionError("不支持转发的消息体没有被过滤掉")
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("飞信电话","删除聊天")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1',"aa",'xin')
    def test_msg_common_group_0113(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络异常"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        #断开网络
        gcp.set_network_status(0)
        time.sleep(8)
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
            # els[3].click()
        else:
            raise AssertionError("没有找到复选框")
        time.sleep(1)
        # 点击转发
        # gcp.click_multiple_selection_forward()
        # 点击取消
        # gcp.click_cancel_repeat_msg()
        # 验证停留在批量选择器页面
        # if not gcp.is_text_present("已选择"):
        #     raise AssertionError("点击取消没有停留在批量选择器页面")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击确定
        # gcp.click_sure_repeat_msg()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        time.sleep(2)
        if sogp.is_on_this_page():
            sogp.click_back()
            sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            time.sleep(3)
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            # 验证是否发送失败
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))
            # 判断是否有重发按钮
            if not gcp.is_exist_msg_send_failed_button():
                try:
                    raise AssertionError("没有重发按钮")
                except AssertionError as e:
                    raise e
            if chat.is_audio_exist():
                raise AssertionError("不支持转发的消息体没有被过滤掉")
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("飞信电话", "删除聊天")

    def tearDown_test_msg_common_group_0113(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0114(self):
        """当消息体都是不支持转发的类型（①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体）"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        #发送多条语音
        dex = 0
        while dex < 2:
            # 发送语音
            gcp.click_audio_btn()
            audio = ChatAudioPage()
            # if audio.wait_for_audio_type_select_page_load():
            #     # 点击只发送语言模式
            #     audio.click_only_voice()
            #     audio.click_sure()
            # # 权限申请允许弹窗判断
            # time.sleep(1)
            # audio.click_allow()
            time.sleep(3)
            audio.click_send_bottom()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                if cwp.is_text_present("退出"):
                    cwp.click_text("退出")
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
            dex+=1
        gcp.press_audio_to_do("多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
        else:
            raise AssertionError("没有找到其他复选框")
        # 验证其他复选框被选中
        if not els[1].get_attribute("checked")=="true":
            raise AssertionError("点击的消息体没有被选中")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("点击取消没有停留在批量选择器页面")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击确定
        gcp.click_sure_repeat_msg()
        # 验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("点击取消没有停留在批量选择器页面")
        if not els[0].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true":
            raise AssertionError("点击的消息体没有被选中")
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0115(self):
        """当消息体是支持转发的类型——网络正常转发"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                if cwp.is_text_present("退出"):
                    cwp.click_text("退出")
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        # 点击转发
        gcp.click_multiple_selection_forward()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # time.sleep(2)
        # sogp.click_back()
        # sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("飞信电话", "删除聊天")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0116(self):
        """当消息体是支持转发的类型——网络异常转发"""
        gcp = GroupChatPage()
        time.sleep(2)
        # 断开网络
        gcp.set_network_status(0)
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        # 点击转发
        gcp.click_multiple_selection_forward()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # time.sleep(2)
        # sogp.click_back()
        # sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("飞信电话"))
            mess.click_element_by_text("飞信电话")
            chat = SingleChatPage()
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            # 验证是否发送失败
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))
            # 判断是否有重发按钮
            if not gcp.is_exist_msg_send_failed_button():
                try:
                    raise AssertionError("没有重发按钮")
                except AssertionError as e:
                    raise e
            if chat.is_audio_exist():
                raise AssertionError("不支持转发的消息体没有被过滤掉")
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("飞信电话", "删除聊天")

    def tearDown_test_msg_common_group_0116(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0117(self):
        """删除选中的消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        #被点到的相对应消息体被选中
        if not (els[2].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true"):
            raise AssertionError("点击的消息体没有被选中")
        # 点击删除
        gcp.click_multiple_selection_delete()
        #点击确定
        gcp.click_multiple_selection_delete_sure()
        flag = gcp.is_toast_exist("删除成功")
        self.assertTrue(flag)
        #验证删除掉的消息体已删除成功
        if gcp.is_text_present("哈哈0"):
            raise AssertionError("删除掉的消息体没有删除成功")
        if gcp.is_text_present("哈哈1"):
            raise AssertionError("删除掉的消息体没有删除成功")
        if gcp.is_text_present("哈哈2"):
            raise AssertionError("删除掉的消息体没有删除成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0118(self):
        """取消删除选中的消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        # 被点到的相对应消息体被选中
        if not (els[2].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true"):
            raise AssertionError("点击的消息体没有被选中")
        # 点击删除
        gcp.click_multiple_selection_delete()
        # 点击取消
        gcp.click_multiple_selection_delete_cancel()
        #验证还停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("没有停留在批量选择器页面")
        #验证选中的消息体还在选中状态
        if not (els[2].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true" and els[0].get_attribute("checked")=="true"):
            raise AssertionError("选中的消息体没有在选中状态")
        time.sleep(2)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0119(self):
        """选择第101条消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 101:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            time.sleep(1)
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        while not gcp.is_text_present("哈哈0"):
            gcp.page_down()
        gcp.press_file_to_do("哈哈0", "多选")
        while not gcp.is_text_present("哈哈100"):
            els = gcp.get_multiple_selection_select_box()
            for el in els:
                flag = el.get_attribute("checked")
                if not flag == "true":
                    el.click()
            gcp.page_up()
        count=gcp.get_multiple_selection_count()
        a = int(count.get_attribute("text"))
        num=101-a-1
        i=0
        while i<num:
            mess="哈哈"+str(a)
            gcp.click_text(mess)
            a+=1
            i+=1
        gcp.click_text("哈哈100")
        if not gcp.is_toast_exist("聊天消息多选最多支持选择100条"):
            raise AssertionError("不会toast提示")
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0156(self):
        """发送失败的消息，长按撤回"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.set_network_status(0)
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送失败
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
        gcp.press_file("哈哈0")
        if gcp.is_text_present("撤回"):
            raise AssertionError("长按发送失败的消息体存在撤回按钮")
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    def tearDown_test_msg_common_group_0156(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0158(self):
        """撤回，发送成功不足一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("哈哈0","撤回")
        time.sleep(1)
        if gcp.is_text_present("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        time.sleep(1)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0159(self):
        """撤回，发送成功不足一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #断开网络
        gcp.set_network_status(0)
        time.sleep(2)
        gcp.press_file_to_do("哈哈0", "撤回")
        if not gcp.is_toast_exist("当前网络不可用，请检查网络设置"):
            raise AssertionError("没有toast提示")
        if not gcp.is_text_present("哈哈0"):
            raise AssertionError("网络异常时撤回成功")

    def tearDown_test_msg_common_group_0159(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0160(self):
        """撤回，发送成功时间，超过一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(62)
        gcp.press_file_to_do("哈哈0", "撤回")
        time.sleep(1)
        if gcp.is_text_present("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        time.sleep(1)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0162(self):
        """撤回，发送成功时间，超过10分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #等待超过十分钟
        a=1
        while a<11:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a+=1
        gcp.press_file("哈哈0")
        if gcp.is_text_present("撤回"):
            raise AssertionError("存在撤回按钮")

    @staticmethod
    def setUp_test_msg_common_group_0164():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC-RESET', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0164(self):
        """APP端第一次使用撤回功能"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("哈哈0", "撤回")
        time.sleep(1)
        if gcp.is_text_present("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        else:
            raise AssertionError("没有弹窗出现")
        if gcp.is_text_present("哈哈0"):
            raise AssertionError("消息撤回失败")
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("不会展示：你撤回了一条信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0165(self):
        """撤回，发送成功不足一分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0166(self):
        """网络异常，撤回，发送成功不足一分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        #断开网络
        gcp.set_network_status(0)
        time.sleep(2)
        gcp.press_voice_message_to_do("撤回")
        if not gcp.is_toast_exist("当前网络不可用，请检查网络设置"):
            raise AssertionError("没有toast提示")
        if gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("网络异常时成功撤回信息")

    def tearDown_test_msg_common_group_0166(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0167(self):
        """撤回，发送成功的语音消息，时间超过一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 1
        while a < 3:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a += 1
        gcp.press_voice_message_to_do("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0169(self):
        """撤回，发送成功的语音消息，时间超过10分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待超过十分钟
        a = 1
        while a < 11:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a += 1
        gcp.press_voice_message()
        if gcp.is_text_present("撤回"):
            raise AssertionError("存在撤回按钮")
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1','xin')
    def test_msg_common_group_0170(self):
        """发送一条语音消息，在9分55秒时，长按展示功能菜单列表"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待到九分钟以上
        a = 1
        while a < 10:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a += 1
        gcp.press_voice_message()
        time.sleep(60)
        gcp.click_text("撤回")
        if gcp.is_toast_exist("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        if gcp.is_toast_exist("你撤回了一条信息"):
            raise AssertionError("消息超过十秒可以撤回")

    @staticmethod
    def setUp_test_msg_huangmianhua_0206():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0206(self):
        """收到一条：该群已解散——系统消息"""
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit2()
        time.sleep(1)
        # 解散退出群
        group_set.click_btn_logout()
        time.sleep(1)
        gcp.click_back()
        mess = MessagePage()
        mess.selecting_one_group_click_by_name("系统消息")
        # 判定点
        exsit = gcp.is_text_present("该群已解散")
        self.assertEqual(exsit, True)
        groupname = Preconditions.get_group_chat_name()
        exsit = gcp.is_text_present(groupname)
        self.assertEqual(exsit, True)

    def tearDown_test_msg_huangmianhua_0206(self):
        gcp = GroupChatPage()
        gcp.click_back_by_android()
        time.sleep(1)
        # 删除 消息（系统消息 群组名）
        mess = MessagePage()
        # 长按 "测试企业群"
        mess.selecting_one_group_press_by_name('系统消息')
        mess.press_groupname_to_do("删除聊天")
        time.sleep(1)
        groupname = Preconditions.get_group_chat_name()
        mess.selecting_one_group_press_by_name(groupname)
        mess.press_groupname_to_do("删除聊天")

    @staticmethod
    def setUp_test_msg_huangmianhua_0219():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0219(self):
        """聊天会话窗口的批量选择器——页面展示"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        # 1.弹出操作列表
        # 2.进入聊天会话窗口的批量选择器页面
        # gcp.press_voice_message_to_do("多选")
        gcp.press_message_longclick()
        gcp.click_message("多选")
        # 显示左上角的【×】关闭按钮，有勾选消息时，左上角文案展示为： 已选择+数量
        if not gcp.is_exist_multiple_selection_back():
            raise AssertionError("没有显示【×】关闭按钮")
        # 验证有勾选信息
        els = gcp.get_multiple_selection_select_box()
        if els[3].get_attribute("checked") == "true":
            if gcp.is_exist_multiple_selection_count():
                if not gcp.is_text_present("已选择"):
                    raise AssertionError("没有显示‘已选择+数量’字样")
            else:
                raise AssertionError("没有显示‘已选择+数量’字样")
            # 底部删除、转发按钮，高亮展示
            if not gcp.is_enabled_multiple_selection_delete():
                raise AssertionError("勾选信息后底部删除按钮没有高亮展示")
            if not gcp.is_enabled_multiple_selection_forward():
                raise AssertionError("勾选信息后底部转发按钮没有高亮展示")
        else:
            raise AssertionError("没有勾选信息")
        # 取消勾选信息
        els[3].click()
        time.sleep(1)
        # 未选择任何消息时，左上角文案展示为：未选择，底部删除，转发按钮默认置灰展示
        if not gcp.is_text_present("未选择"):
            raise AssertionError("未选择任何消息时没有展示‘未选择’")
        # 底部删除、转发按钮，置灰展示
        if gcp.is_enabled_multiple_selection_delete():
            raise AssertionError("未勾选信息后底部删除按钮没有置灰展示")
        if gcp.is_enabled_multiple_selection_forward():
            raise AssertionError("未勾选信息后底部转发按钮没有置灰展示")
        gcp.click_multiple_selection_back()

    @staticmethod
    def setUp_test_msg_huangmianhua_0220():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0220(self):
        """下拉——加载历史消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        # 1.弹出操作列表
        # 2.进入聊天会话窗口的批量选择器页面
        # gcp.press_voice_message_to_do("多选")
        gcp.press_message_longclick()
        if not gcp.is_toast_exist("多选"):
            raise AssertionError("多选-功能项没找到")
        gcp.click_message("多选")
        if not gcp.is_toast_exist("已选择"):
            raise AssertionError("多选-点击失败")

    @staticmethod
    def setUp_test_msg_huangmianhua_0221():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0221(self):
        """取消多选模式"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        # 1.弹出操作列表
        # 2.进入聊天会话窗口的批量选择器页面
        # gcp.press_voice_message_to_do("多选")
        gcp.press_message_longclick()
        if not gcp.is_toast_exist("多选"):
            raise AssertionError("多选-功能项没找到")
        gcp.click_message("多选")
        if not gcp.is_toast_exist("已选择"):
            raise AssertionError("多选-点击失败")
        # 3.复选框消失，转发操作选项直接消失，出现底部聊天输入框，自动返回聊天会话窗口
        # 点击 “X”按钮
        gcp.click_multiple_selection_back()
        exist = gcp.is_toast_exist("转发")
        self.assertEqual(exist, False)
        exist = gcp.is_toast_exist("说点什么")
        self.assertEqual(exist, True)

    @staticmethod
    def setUp_test_msg_huangmianhua_0222():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0222(self):
        """转发——不支持转发的——默认选中项（1条）"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        # 1.弹出操作列表
        # 2.进入聊天会话窗口的批量选择器页面
        # gcp.press_voice_message_to_do("多选")
        gcp.press_message_longclick()
        if not gcp.is_toast_exist("多选"):
            raise AssertionError("多选-功能项没找到")
        gcp.click_message("多选")
        if not gcp.is_toast_exist("已选择"):
            raise AssertionError("多选-点击失败")
        # 3.复选框消失，转发操作选项直接消失，出现底部聊天输入框，自动返回聊天会话窗口
        # 点击 “转发”按钮
        gcp.click_multiple_selection_forward()
        exist = gcp.is_toast_exist("转发提示")
        self.assertEqual(exist, True)

    @staticmethod
    def setUp_test_msg_huangmianhua_0223():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0223(self):
        """转发——不支持转发的——默认选中项（1条）"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        # 1.弹出操作列表
        # 2.进入聊天会话窗口的批量选择器页面
        # gcp.press_voice_message_to_do("多选")
        gcp.press_message_longclick()
        if not gcp.is_toast_exist("多选"):
            raise AssertionError("多选-功能项没找到")
        gcp.click_message("多选")
        if not gcp.is_toast_exist("已选择"):
            raise AssertionError("多选-点击失败1")
        # 3.复选框消失，转发操作选项直接消失，出现底部聊天输入框，自动返回聊天会话窗口
        # 点击 “转发”按钮
        gcp.click_multiple_selection_forward()
        exist = gcp.is_toast_exist("转发提示")
        self.assertEqual(exist, True)
        # 返回 弹出框消失
        gcp.click_back_by_android()
        time.sleep(1)
        exist = gcp.is_toast_exist("转发提示")
        self.assertEqual(exist, False)
        if not gcp.is_toast_exist("已选择"):
            raise AssertionError("多选-点击失败2")

    @staticmethod
    def setUp_test_msg_huangmianhua_0240():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0240(self):
        """聊天会话页面——长按——撤回——发送失败的文本消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 断网
        mess = MessagePage()
        mess.set_network_status(0)
        time.sleep(1)
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.hide_keyboard()
        mess.set_network_status(6)
        time.sleep(1)
        # 1、长按发送失败的消息
        # 2、弹出的功能列表中，不存在撤回功能（发送失败的消息，不允许进行撤回操作）
        gcp.press_message_longclick2()
        if gcp.is_toast_exist("撤回"):
            raise AssertionError("存在--撤回功能")

    @staticmethod
    def setUp_test_msg_huangmianhua_0241():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0241(self):
        """聊天会话页面——长按——撤回——发送中途的文本消息---暂时以失败方式实现"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 断网
        mess = MessagePage()
        mess.set_network_status(0)
        time.sleep(1)
        for num in range(3):
            gcp.input_message("哈哈")
            gcp.send_message()
        gcp.hide_keyboard()
        mess.set_network_status(6)
        time.sleep(1)
        # 1、长按发送失败的消息
        # 2、弹出的功能列表中，不存在撤回功能（发送失败的消息，不允许进行撤回操作）
        gcp.press_message_longclick2()
        if gcp.is_toast_exist("撤回"):
            raise AssertionError("存在--撤回功能")

    @staticmethod
    def setUp_test_msg_huangmianhua_0242():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0242(self):
        """聊天会话页面——第一次使用撤回功能"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待超过一分钟
        # a = 1
        # while a < 3:
        #     time.sleep(60)
        #     gcp.get_input_box()
        #     print("{}分钟".format(a))
        #     a += 1
        gcp.press_message_longclick()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0243():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_common_group_0243(self):
        """聊天会话页面——长按——撤回——不足一分钟的文本消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.input_message("哈哈")
        gcp.send_message()
        gcp.hide_keyboard()
        # 等待超过一分钟
        # a = 1
        # while a < 3:
        #     time.sleep(60)
        #     gcp.get_input_box()
        #     print("{}分钟".format(a))
        #     a += 1
        gcp.press_message_longclick2()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0244():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0244(self):
        """聊天会话页面——长按——撤回——超过一分钟的文本消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.input_message("哈哈")
        gcp.send_message()
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 0
        while a < 1:
            time.sleep(61)
            # gcp.get_input_box()
            # print("{}分钟".format(a))
            a += 1
        gcp.press_message_longclick2()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0245():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0245(self):
        """聊天会话页面——长按撤回——等于10分钟的文本消息 """
        # 暂时已1分钟替代
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.input_message("哈哈")
        gcp.send_message()
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 0
        while a < 1:
            time.sleep(61)
            # gcp.get_input_box()
            # print("{}分钟".format(a))
            a += 1
        gcp.press_message_longclick2()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0246():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0246(self):
        """聊天会话页面——长按撤回——大于10分钟的文本消息 """
        # 测试时，暂时失败信息替代
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # gcp.set_network_status(0)
        time.sleep(1)
        gcp.input_message("哈哈")
        gcp.send_message()
        gcp.hide_keyboard()
        # 等待超过十分钟
        a = 0
        while a < 1:
            time.sleep(601)
            a += 1
        gcp.press_message_longclick2()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮 有显示")
        # gcp.set_network_status(6)
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangmianhua_0247():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0247(self):
        """更改手机系统时间后——长按——撤回消息 """
        # 暂时已1分钟替代
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.input_message("哈哈")
        gcp.send_message()
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 0
        while a < 1:
            time.sleep(61)
            # gcp.get_input_box()
            # print("{}分钟".format(a))
            a += 1
        gcp.press_message_longclick2()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0248():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0248(self):
        """聊天会话页面——长按——撤回——发送失败的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        # 断网
        gcp.set_network_status(0)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     if cwp.is_text_present("退出"):
        #         cwp.click_text("退出")
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        gcp.press_message_longclick()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮-有显示")

    def tearDown_test_msg_huangmianhua_0248(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangmianhua_0249():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0249(self):
        """聊天会话页面——长按——撤回——发送中途的语音消息"""
        # 暂时msg_huangmianhua_0248用例的实现方式
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        # 断网
        gcp.set_network_status(0)
        audio.click_send_bottom()
        # 验证是否发送成功
        # cwp = ChatWindowPage()
        # try:
        #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # except TimeoutException:
        #     if cwp.is_text_present("退出"):
        #         cwp.click_text("退出")
        #     raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        gcp.press_message_longclick()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮-有显示")

    def tearDown_test_msg_huangmianhua_0249(self):
        # 重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangmianhua_0250():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0250(self):
        """天会话页面——长按——撤回——不足一分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        gcp.press_message_longclick()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0251():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0251(self):
        """聊天会话页面——长按撤回——超过一分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 0
        while a < 1:
            time.sleep(61)
            a += 1
        gcp.press_message_longclick()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0252():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0252(self):
        """聊天会话页面——长按撤回——等于10分钟的语音消息"""
        # 暂以超过1分钟用例代替 同msg_huangmianhua_0252用例
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 0
        while a < 1:
            time.sleep(61)
            a += 1
        gcp.press_message_longclick()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0253():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0253(self):
        """聊天会话页面——长按撤回——大于10分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        # 等待超过十分钟
        a = 0
        while a < 1:
            time.sleep(601)
            a += 1
        gcp.press_message_longclick()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回功能按钮--有显示")

    @staticmethod
    def setUp_test_msg_huangmianhua_0254():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0254(self):
        """更改手机系统时间后——长按撤回语音消息，已发送10分钟内的消息进行脚本编写"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            if cwp.is_text_present("退出"):
                cwp.click_text("退出")
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        time.sleep(1)
        gcp.hide_keyboard()
        # 等待超过十分钟
        # a = 0
        # while a < 1:
        #     time.sleep(601)
        #     a += 1
        gcp.press_message_longclick()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回功能按钮--没有显示")
        gcp.click_message("撤回")
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        time.sleep(2)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @staticmethod
    def setUp_test_msg_huangmianhua_0256():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0256(self):
        """聊天会话页面——长按——不支持撤回的消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        # 断网
        gcp.set_network_status(0)
        audio.click_send_bottom()
        time.sleep(1)
        gcp.hide_keyboard()
        gcp.press_message_longclick()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮-有显示")

    def tearDown_test_msg_huangmianhua_0256(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangmianhua_0257():
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'high')
    def test_msg_huangmianhua_0257(self):
        """聊天会话页面——在10分钟内长按——弹出功能菜单列表——10分钟后撤回"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.input_message("哈哈")
        gcp.send_message()
        gcp.hide_keyboard()
        gcp.press_message_longclick2()
        if not gcp.is_text_present("撤回"):
            raise AssertionError("撤回功能按钮--没有显示")
        # 等待超过十分钟
        a = 0
        while a < 1:
            time.sleep(601)
            a += 1
        gcp.click_message("撤回")
        time.sleep(2)
        if gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("成功撤回了信息")

class MsgCommonGroupPriorityTest(TestCase):
    """
        模块：消息-普通群

        文件位置：1.1.4和飞信APP全量测试用例-优先编写用例 .xlsx
        表格：消息-普通群
    """

    @classmethod
    def setUpClass(cls):
        pass

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

    # @tags('ALL', 'Priority', 'CMCC')
    @unittest.skip("卸载先不执行")
    def test_msg_xiaoqiu_0043(self):
        """ 先卸载后安装"""
        # 卸载和飞信
        from settings.available_devices import TARGET_APP
        current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("没有任何收藏"):
            raise AssertionError("收藏的文件内容没有被清除")
        mcp = MeCollectionPage()
        mcp.click_back()
        me.open_message_page()

    def tearDown_test_msg_xiaoqiu_0043(self):
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        if current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            return

        # 预防安装应用的时候发生异常，尝试恢复安装，（还不知道好不好使）
        reinstall_try_time = 3
        while reinstall_try_time > 0:
            try:
                current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
                current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                             replace=True)
                break
            except:
                reinstall_try_time -= 1
                if reinstall_try_time == 0:
                    import traceback
                    traceback.print_exc()

    # @tags('ALL', 'Priority', 'CMCC')
    @unittest.skip("卸载先不执行")
    def test_msg_xiaoqiu_0092(self):
        """ 先卸载后安装"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        flag = audio.wait_for_audio_allow_page_load()
        self.assertTrue(flag)
        audio.click_allow()
        audio.wait_until(condition=lambda d: audio.is_text_present("退出"))
        audio.click_exit()
        gcp.wait_for_page_load()
        self.assertFalse(gcp.is_exist_red_dot())
        # 卸载和飞信
        from settings.available_devices import TARGET_APP
        current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        Preconditions.enter_group_chat_page()
        self.assertTrue(gcp.is_exist_red_dot())

    def tearDown_test_msg_xiaoqiu_0092(self):
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        if current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            return

        # 预防安装应用的时候发生异常，尝试恢复安装，（还不知道好不好使）
        reinstall_try_time = 3
        while reinstall_try_time > 0:
            try:
                current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
                current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                             replace=True)
                break
            except:
                reinstall_try_time -= 1
                if reinstall_try_time == 0:
                    import traceback
                    traceback.print_exc()

    @tags('ALL', 'Priority', 'CMCC','high')
    def test_msg_xiaoqiu_0124(self):
        """普通群——群成员——添加一个成员"""
        # 1、点击添加成员的“+”号按钮，是否可以跳转到联系人选择器页面
        # 2、任意选中一个联系人，点击右上角的确定按钮，是否会向邀请人发送一条消息
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        if not cgacp.is_text_present("添加群成员"):
            raise AssertionError("不可以跳转到联系人选择器页面")
        cgacp.click_one_contact("飞信电话")
        time.sleep(1)
        cgacp.click_sure()
        time.sleep(2)
        gcp.page_should_contain_text("发出群邀请")

    @tags('ALL', 'Priority', 'CMCC','high')
    def test_msg_xiaoqiu_0125(self):
        """普通群——群主——添加2个成员"""
        # 1、点击添加成员的“+”号按钮
        # 2、任意选中2个联系人，点击右上角的确定按钮，是否会向邀请人发送一条消息
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        contactNnames = cgacp.get_contacts_name()
        if len(contactNnames) > 1:
            # 选择多个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
            cgacp.select_one_member_by_name(contactNnames[1])
        else:
            raise AssertionError("通讯录联系人数量不足，请添加")
        time.sleep(3)
        cgacp.click_sure()
        time.sleep(2)
        gcp.page_should_contain_text("发出群邀请")

    @tags('ALL', 'Priority', 'CMCC','high')
    def test_msg_xiaoqiu_0129(self):
        """普通群——群成员——添加一个成员"""
        # 1、点击添加成员的“+”号按钮，是否可以跳转到联系人选择器页面
        # 2、任意选中一个联系人，点击右上角的确定按钮，是否会向邀请人发送一条消息
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        if not cgacp.is_text_present("添加群成员"):
            raise AssertionError("不可以跳转到联系人选择器页面")
        cgacp.click_one_contact("飞信电话")
        time.sleep(1)
        cgacp.click_sure()
        time.sleep(2)
        gcp.page_should_contain_text("发出群邀请")

    @tags('ALL', 'Priority', 'CMCC','high')
    def test_msg_xiaoqiu_0131(self):
        """普通群——群主——添加2个成员"""
        # 1、点击添加成员的“+”号按钮，是否可以跳转到联系人选择器页面
        # 2、任意选中2个联系人，点击右上角的确定按钮，是否会向邀请人发送一条消息
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        if not cgacp.is_text_present("添加群成员"):
            raise AssertionError("不可以跳转到联系人选择器页面")
        contactNnames = cgacp.get_contacts_name()
        if len(contactNnames) > 1:
            # 选择多个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
            cgacp.select_one_member_by_name(contactNnames[1])
        else:
            raise AssertionError("通讯录联系人数量不足，请添加")
        time.sleep(3)
        cgacp.click_sure()
        time.sleep(2)
        gcp.page_should_contain_text("发出群邀请")

    @tags('ALL', 'Priority', 'CMCC','high')
    def test_msg_xiaoqiu_0140(self):
        """群主——修改群昵称"""
        # 1、点击群名称入口，是否可以进入到修改群名称页面并且群名称为编辑状态
        # 2、点击左上角的返回按钮，是否可以返回到群聊设置页面
        # 3、点击右上角的保存按钮，是否会直接保存现有群名称并返回到群聊设置页面
        # 4、点击编辑状态群名称右边的“X”，是否可以一次性清除群名称文案，群名称编辑框中，展示默认文案：修改群名称
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        if not gcsp.is_text_present("修改群名称"):
            raise AssertionError("不可以进入到修改群名称页面")
        gcsp.click_edit_group_card_back()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(2)
        gcsp.save_group_name()
        gcsp.wait_for_page_load()
        gn=Preconditions.get_group_chat_name()
        if not gcsp.is_text_present(gn):
            raise AssertionError("没有直接保存现有群名称")
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.click_iv_delete_button()
        time.sleep(2)
        if not gcsp.is_text_present("请输入群聊名称"):
            raise AssertionError("不可以一次性清除群名称文案")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'Priority', 'CMCC','high')
    def test_msg_xiaoqiu_0141(self):
        """群主——清除旧名称——录入一个汉字"""
        # 1、群名称编辑页面，清除旧名称后，录入一个汉字，点击右上角的完成按钮，是否可以完成保存
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("哈")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        group_name = Preconditions.get_group_chat_name()
        gcsp.input_new_group_name(group_name)
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'Priority', 'CMCC', 'high')
    def test_msg_huangmianhua_0049(self):
        """1.默认头像 2.群名称：超长时后面加“...”（是否超长按宽度来计算"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名 "adcdefghijklmnopqrstuvwxyzjkhuuibb"
        gcsp.input_new_group_name("adcdefghijklmnopqrstuvwxyzjkhuuibb")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        gcp.wait_for_page_load()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 回到消息列表界面
        gcp.click_back()
        time.sleep(1)
        # 判定
        mess = MessagePage()
        exist = mess.is_text_present("…")
        self.assertEqual(exist, True)
        mess.selecting_one_group_click_by_name("adcdefghijklmnopqrstuvwxyzjkhuuibb")
        # 恢复群名
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        group_name = Preconditions.get_group_chat_name()
        gcsp.input_new_group_name(group_name)
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0050(self):
        """系统消息入口——系统消息展示规则——时间展示规则"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_back()
        mess = MessagePage()
        exist = mess.is_text_present("刚刚")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0051(self):
        """系统消息入口——系统消息展示规则——时间展示规则"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_back()
        mess = MessagePage()
        # 暂时这样判断处理
        exist = mess.is_text_present(":")
        self.assertEqual(exist, True)

class MsgCommonGroupAllTest(TestCase):
    """
            模块：消息-普通群

            文件位置：1.1.3全量测试用例\113和飞信全量测试用例-肖秋.xlsx
            表格：和飞信全量测试用例
        """

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
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
    def setUp_test_msg_xiaoqiu_0001():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL','CMCC','group_chat','full','high')
    def test_msg_xiaoqiu_0001(self):
        """消息列表——发起群聊——选择已有群"""
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，是否可以进入到群聊列表展示页面
        # 3、中文模糊搜索，是否可以匹配展示搜索结果
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        #先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "啊测测试试":
            raise AssertionError("无法中文模糊搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0002():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0002(self):
        """消息列表——发起群聊——选择已有群"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊啊测")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0003():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0003(self):
        """群聊列表展示页面——中文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊测测试试")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "啊测测试试":
            raise AssertionError("无法中文精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0004():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0004(self):
        """群聊列表展示页面——中文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊测测试试啊")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0005():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0005(self):
        """群聊列表展示页面——英文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("atteesstt")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("atteesstt")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "atteesstt":
            raise AssertionError("无法英文精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0006():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0006(self):
        """群聊列表展示页面——英文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("atteesstt")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("aatteesstt")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0007():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0007(self):
        """群聊列表展示页面——空格精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("a a")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword(" ")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "a a":
            raise AssertionError("无法空格精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0008():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0008(self):
        """群聊列表展示页面——空格精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("a a")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("  ")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0009():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0009(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("112233445566")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "112233445566":
            raise AssertionError("无法数字精确搜索")
        # sog.click_back_icon()
        # sog.click_back()
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0010():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0010(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("1112233445566")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0011():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0011(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("112233445566")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "112233445566":
            raise AssertionError("无法数字精确搜索")
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0012():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0012(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("1112233445566")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0013():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0013(self):
        """群聊列表展示页面——字符精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("$$")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("$$")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "$$":
            raise AssertionError("无法字符精确搜索")
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0014():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0014(self):
        """群聊列表展示页面——字符精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("$$")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("$$$")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0015():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0015(self):
        """群聊列表展示页面——索引字母定位选择"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("ii")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_text("I")
        time.sleep(2)
        if not sog.is_text_present("ii"):
            raise AssertionError("索引字母不能进行定位")
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_back()
        sog.click_back()
        # sc.click_back()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0017(self):
        """在群聊天会话页面，发送一条字符长度等于：1的，文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈")
        if gcp.is_audio_btn_exit():
            raise AssertionError("右边的语音按钮不会自动变为发送按钮")
        gcp.page_should_contain_send_btn()
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        mess="哈"*10
        gcp.input_message(mess)
        if gcp.is_audio_btn_exit():
            raise AssertionError("右边的语音按钮不会自动变为发送按钮")
        gcp.page_should_contain_send_btn()
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        # if not gcp.get_width_of_msg_of_text() <= width:
        #     raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0022(self):
        """在群聊天会话页面，输入框中录入500个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的高度
        info = "哈"*500
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        height= gcp.get_height_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"*500
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,文本框信息正常高度为height
        if not gcp.get_height_of_msg_of_text() < height:
            raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0023(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的高度
        info = "哈" * 5000
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        height = gcp.get_height_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,文本框信息正常高度为height
        # if not gcp.get_height_of_msg_of_text() <= height:
        #     raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0024(self):
        """在群聊天会话页面，输入框中录入1个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() > width:
            raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0025(self):
        """在群聊天会话页面，输入框中录入500个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"*500
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"*500
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        # if not gcp.get_width_of_msg_of_text() > width:
        #     raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0026(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈" * 5000
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
            # if not gcp.get_width_of_msg_of_text() > width:
            #     raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    # @unittest.skip("过跳过")
    def test_msg_xiaoqiu_0028(self):
        """进入到群聊天会话页面，录入500个表情字符，缩小发送"""
        gcp=GroupChatPage()
        Preconditions.delete_record_group_chat()
        info = "[微笑1]" * 500
        gcp.input_message(info)
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    # @unittest.skip("先跳过")
    def test_msg_xiaoqiu_0032(self):
        """进入到群聊天会话页面，录入500个表情字符，放大发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        info = "[微笑1]" * 500
        gcp.input_message(info)
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0035(self):
        """进入到群聊天会话页面，录入文字+表情字符，放大发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        gcp.input_message(info)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() > width:
            raise AssertionError("文本消息没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0036(self):
        """进入到群聊天会话页面，录入文字+表情字符，缩小发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        gcp.input_message(info)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("文本消息没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0037(self):
        """在群聊天会话页面，长按消息体，点击收藏"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        #输入信息
        info = "哈哈"
        gcp.input_message(info)
        gcp.send_message()
        # 长按信息并点击收藏
        time.sleep(2)
        gcp.press_file_to_do("哈哈", "收藏")
        flag = gcp.is_toast_exist("已收藏")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0038(self):
        """我——收藏——收藏内容展示"""
        gcp = GroupChatPage()
        time.sleep(2)
        gcp.click_back()
        time.sleep(2)
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            sogp.click_back()
            sc = SelectContactsPage()
            sc.click_back()
        # 进入我页面
        mess = MessagePage()
        time.sleep(2)
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.page_contain_element("收藏时间")
        mcp.page_contain_element("内容来源")
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0039(self):
        """我——收藏——收藏内展示——点击收藏内容"""
        gcp = GroupChatPage()
        time.sleep(2)
        if gcp.is_on_this_page():
            gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("哈哈")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        mcp.click_back()
        time.sleep(2)
        #验证可以返回到收藏列表页
        if not mcp.is_text_present("收藏"):
            raise AssertionError("不能返回到收藏列表页")
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0040(self):
        """我——收藏——收藏内展示——点击收藏内容——点击播放收藏语音文件"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("收藏")
        if not gcp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(1)
        if not me.is_text_present("秒"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("秒")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        # 播放语音消息
        mcp.click_collection_voice_msg()
        time.sleep(2)
        # 暂停语音消息
        mcp.click_collection_voice_msg()
        mcp.click_back()
        time.sleep(2)
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0041(self):
        """我——收藏——收藏内展示——点击收藏内容——点击删除收藏内容"""
        gcp = GroupChatPage()
        time.sleep(2)
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(2)
        # 左滑收藏消息体
        mcp = MeCollectionPage()
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            time.sleep(2)
            #判断是否会弹出确认弹窗
            if not mcp.is_text_present("确定"):
                raise AssertionError("没有弹出确认窗口")
            #点击取消
            mcp.click_cancel_forward()
            flag=mcp.is_delete_element_present()
            self.assertTrue(flag)
            time.sleep(1)
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            time.sleep(2)
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
        else:
            raise AssertionError("没有删除按钮")
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0050(self):
        """发送一组数字：95533，发送失败的状态展示"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.set_network_status(0)
        # 输入信息
        info = "95533"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
        # 判断是否会展示重新发送按钮
        if not gcp.is_exist_msg_send_failed_button():
            try:
                raise AssertionError("没有重发按钮")
            except AssertionError as e:
                raise e
        time.sleep(2)
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            # 判断是否有“！”
            if not mess.is_iv_fail_status_present():
                try:
                    raise AssertionError("没有消息发送失败“！”标致")
                except AssertionError as e:
                    raise e
            # 进入新消息窗口判断消息是否发送失败
            mess.click_text("95533")
            gcp.wait_for_page_load()
            gcp.set_network_status(6)
            time.sleep(2)
            # 点击重发按钮
            gcp.click_msg_send_failed_button()
            # 点击确定重发
            gcp.click_resend_confirm()
            # 判断信息发送状态
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息未在 {}s 内发送成功'.format(10))

    def tearDown_test_msg_xiaoqiu_0050(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(5)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0072(self):
        """仅语音模式，录制时长等于1秒时，点击发送按钮"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(1)
            audio.click_send_bottom()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                audio.click_send_bottom()
                # 验证是否发送成功
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0073(self):
        """仅语音模式，发送录制时长大于1秒的语音"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(2)
            audio.click_send_bottom()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(2)
                audio.click_send_bottom()
                # 验证是否发送成功
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0074(self):
        """仅语音模式，录制时长大于10秒——发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(11)
            audio.click_exit()
            time.sleep(1)
            if gcp.is_text_present("语音录制中"):
                raise AssertionError("退出语音录制模式失败")
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(11)
                audio.click_exit()
                time.sleep(1)
                if gcp.is_text_present("语音录制中"):
                    raise AssertionError("退出语音录制模式失败")
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0075(self):
        """仅语音模式，录制时长等于60秒—自动发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(60)
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(1)
                audio.click_exit()
                Preconditions.delete_record_group_chat()
                gcp.click_audio_btn()
                time.sleep(60)
                # 验证是否发送成功
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0076(self):
        """仅语音模式，录制时长超过60秒"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(65)
            if gcp.is_text_present("语音录制中"):
                raise AssertionError("录制时长可以超过60秒")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(65)
                if gcp.is_text_present("语音录制中"):
                    raise AssertionError("录制时长可以超过60秒")
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0085(self):
        """在聊天会话页面——点击语音ICON"""
        gcp = GroupChatPage()
        #断网
        gcp.set_network_status(0)
        time.sleep(8)
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            time.sleep(2)
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()

    def tearDown_test_msg_xiaoqiu_0085(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0088(self):
        """进入到语音录制页——网络异常"""
        gcp = GroupChatPage()
        # 断网
        gcp.set_network_status(0)
        time.sleep(2)
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()

    def tearDown_test_msg_xiaoqiu_0088(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0089(self):
        """语音录制中途——网络异常"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(5)
            # 断网
            gcp.set_network_status(0)
            time.sleep(3)
            if not gcp.is_text_present("语音录制中"):
                raise AssertionError("录制会被中断")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(5)
                # 断网
                gcp.set_network_status(0)
                time.sleep(3)
                if not gcp.is_text_present("语音录制中"):
                    raise AssertionError("录制会被中断")
                audio.click_exit()
                # gcp.hide_keyboard()
                current_mobile().hide_keyboard_if_display()
                time.sleep(3)
            else:
                raise AssertionError("语音模式选择页面加载失败")

    def tearDown_test_msg_xiaoqiu_0089(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0090(self):
        """语音录制完成——网络异常"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(5)
            # 断网
            gcp.set_network_status(0)
            time.sleep(3)
            audio.click_send_bottom()
            # 验证是否发送失败
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(5)
                # 断网
                gcp.set_network_status(0)
                time.sleep(3)
                audio.click_send_bottom()
                # 验证是否发送失败
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送失败', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    def tearDown_test_msg_xiaoqiu_0090(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0095():
        Preconditions.select_mobile('Android-移动')
        # current_mobile().launch_app()
        current_mobile().reset_app()
        Preconditions.enter_group_chat_page()

    # @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    @unittest.skip("先跳过")
    def test_msg_xiaoqiu_0095(self):
        """当前版本，消息语音icon上红点展示后，清除数据重新登录"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(2)
        gcp.click_more()
        time.sleep(2)
        if not gcp.is_exist_red_dot():
            raise AssertionError("清除数据重新登陆,语音icon不存在红点提示")
        time.sleep(2)
        current_mobile().reset_app()
        Preconditions.enter_group_chat_page()
        gcp.click_more()
        time.sleep(2)
        gcp.click_more()
        time.sleep(2)
        if not gcp.is_exist_red_dot():
            raise AssertionError("清除数据重新登陆,语音icon不存在红点提示")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0097():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name=Preconditions.get_group_chat_name_double()
        flag=Preconditions.build_one_new_group_with_number(phone_number, group_name)
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
    def test_msg_xiaoqiu_0097(self):
        """在群聊会话页，点击分享过来的卡片消息体——进入到卡片链接页"""
        # 1、点击接收到的卡片消息体，是否可以进入到卡片链接页
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_profile()
        time.sleep(2)
        gcp.click_one_contact("飞信电话")
        time.sleep(2)
        gcp.click_text("发送名片")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        #切换另一台设备
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.click_text("飞信电话")
        time.sleep(3)
        if not gcp.is_text_present("邀请使用"):
            raise AssertionError("无法进入到卡片链接页")
        current_mobile().back()
        Preconditions.delete_record_group_chat()


    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0098(self):
        """在群聊会话窗口，点击页面顶部的通话按钮"""
        # 1、点击页面顶部的通话按钮，是否会调起通话选择项弹窗
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_mutilcall()
        time.sleep(2)
        if not gcp.is_text_present("多方视频"):
            raise AssertionError("不会调起通话选择项弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    @staticmethod
    def setUp_test_msg_xiaoqiu_0099():
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
    def test_msg_xiaoqiu_0099(self):
        """在群聊会话窗口，点击通话按钮——拨打多方电话"""
        # 1、点击多方电话按钮，是否可以跳转到群成员联系人选择器页
        # 2、任意选中几个群成员，点击右上角的呼叫按钮，是否可以成功发起呼叫
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_mutilcall()
        time.sleep(2)
        gcp.click_text("免费")
        #选择联系人
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_text("呼叫")
        time.sleep(3)
        if gcp.is_text_present("我知道了"):
            gcp.click_text("我知道了")
        if gcp.is_text_present("始终允许"):
            gcp.click_text("始终允许")
        time.sleep(8)
        if not gcp.is_phone_in_calling_state():
            raise AssertionError("没有出现通话界面")
        gcp.pick_up_the_call()
        Preconditions.select_mobile('Android-移动-移动')
        time.sleep(10)
        if not gcp.is_phone_in_calling_state():
            raise AssertionError("没有成功发起呼叫")
        gcp.hang_up_the_call()
        Preconditions.select_mobile('Android-移动')
        gcp.hang_up_the_call()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0113():
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
    def test_msg_xiaoqiu_0113(self):
        """在群聊设置页面，群成员展示列表，点击“>”"""
        # 1、在群聊设置页面，点击群成员展示列表右上角的“ > ”按钮，是否可以跳转到群成员列表页
        # 2、任意点击一个陌生的群成员头像，是否会跳转到陌生人详情页中并展示交换名片按钮
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 选择联系人
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        for name in names:
            slc.select_one_member_by_name(name)
            time.sleep(3)
            if gcp.is_text_present("编辑"):
                current_mobile().back()
                time.sleep(2)
            else:
                if not gcp.is_text_present("交换名片"):
                    raise AssertionError("不会跳转到陌生人详情页中并展示交换名片按钮")
                break
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0114():
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
    def test_msg_xiaoqiu_0114(self):
        """群成员展示列表页，输入框输入号码——前3位搜索群成员"""
        # 1、在页面顶部的搜索框中，输入一个号码的前3位作为搜索条件进行搜索，是否可以搜索出对应的群成员信息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        gcp.input_member_message(phone_number[0:3])
        #验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()


    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0101(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""
        # 1、点击输入框上方的图片ICON，是否可以进入到相册列表页
        # 2、任意选中一张照片，点击右下角的发送按钮，是否可以发送成功
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        if gcp.is_text_present("退出"):
            audio = ChatAudioPage()
            audio.click_exit()
            time.sleep(2)
        gcp.click_picture()
        time.sleep(2)
        if not gcp.is_text_present("原图"):
            raise AssertionError("不可以进入到相册列表页")
        gcp.select_picture()
        time.sleep(2)
        gcp.click_text("发送")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0231():
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
    def test_msg_xiaoqiu_0231(self):
        """群聊天会话页面——同时@多个人——@效果展示"""
        # 1、同时 @ 多群成员联系人，发送成功后，被 @ 的联系人收到后，是否存在 @ 效果
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_message("@")
        time.sleep(2)
        sc=SelectContactsPage()
        sc.click_element_("联系人栏")
        time.sleep(2)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        # 切换另一台设备
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        if not mess.is_element_exit_("有人@我"):
            raise AssertionError("被@的联系人收到后，不存在@效果")
        Preconditions.go_to_group_double(group_name)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0115():
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
    def test_msg_xiaoqiu_0115(self):
        """群成员展示列表页，输入框输入号码——前3位搜索群成员"""
        # 1、在页面顶部的搜索框中，输入一个号码的前3位作为搜索条件进行搜索，是否可以搜索出对应的群成员信息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        gcp.input_member_message(phone_number[0:3])
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0116():
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
    def test_msg_xiaoqiu_0116(self):
        """群成员展示列表页，输入框输入——完整号码搜索群成员"""
        # 1、在页面顶部的搜索框中，输入一个完整的号码的作为搜索条件进行搜索，是否可以搜索出对应的群成员信息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        gcp.input_member_message(phone_number)
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0117():
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
    def test_msg_xiaoqiu_0117(self):
        """群成员展示列表页，输入框输入——中文字符搜索群成员"""
        # 1、在页面顶部的搜索框中，输入一个中文字符作为搜索条件进行搜索，是否可以搜索出对应的群成员信息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        gcp.input_member_message("哈")
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0118():
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
    def test_msg_xiaoqiu_0118(self):
        """群成员展示列表页，输入框输入——英文字符搜索群成员"""
        # 1、在页面顶部的搜索框中，输入一个英文字符作为搜索条件进行搜索，是否可以搜索出对应的群成员信息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        gcp.input_member_message("A")
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0636():
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
    def test_msg_xiaoqiu_0636(self):
        """群成员展示列表页，输入搜索条件——搜索——不存在搜索结果时展示"""
        # 1、在页面顶部的搜索框中，输入一个字符作为搜索条件进行搜索，无搜索结果展示
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        gcp.input_member_message("$")
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0119():
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
    def test_msg_xiaoqiu_0119(self):
        """群成员展示列表页，搜索出的搜索结果排序"""
        # 1、在页面顶部的搜索框中，输入一个英文字符作为搜索条件进行搜索，搜索出的搜索结果，是否是按照：排序规则：精确匹配>模糊匹配排序；其次按照结果的首字母顺序排序
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 输入群成员信息
        gcp.input_member_message("A")
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0120():
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
    def test_msg_xiaoqiu_0120(self):
        """在群聊设置页面——群主——群成员头像展示"""
        # 1、群主在群聊天设置页面，展示的群成员头像，最多是否只能展示10个头像
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 判断群成员头像是否存在
        if not gcp.is_element_exit_("群成员头像"):
            raise AssertionError("没有展示出群成员头像")
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0121():
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
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0121(self):
        """在群聊设置页面——群成员——群成员头像展示"""
        # 1、群成员在群聊天设置页面，展示的群成员头像，最多是否只能展示11个头像
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        gcp.click_element_("群成员")
        time.sleep(3)
        if not gcp.is_text_present("搜索成员"):
            raise AssertionError("不可以跳转到群成员列表页")
        # 判断群成员头像是否存在
        if not gcp.is_element_exit_("群成员头像"):
            raise AssertionError("没有展示出群成员头像")
        # 验证搜索结果
        current_mobile().back()
        current_mobile().back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0220():
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
    def test_msg_xiaoqiu_0220(self):
        """聊天设置页面——打开置顶聊天功能——置顶一个聊天会话窗口"""
        # 1、点击置顶聊天功能右边的开关，是否可以打开置顶聊天功能
        # 2、置顶聊天功能开启后，返回到消息列表，接收一条消息，置顶聊天会话窗口是否会展示到页面顶部并且会话窗口成浅灰色展示
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        if gcp.is_element_exit_("置顶聊天"):
            gcp.click_element_("置顶聊天")
        else:
            gcp.page_up()
            time.sleep(2)
            gcp.click_element_("置顶聊天")
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        if not gcp.is_text_present(group_name):
            raise AssertionError("会话窗口没有置顶")
        gcp.press_element_by_text(group_name,3000)
        time.sleep(2)
        if not gcp.is_text_present("取消置顶"):
            raise AssertionError("会话窗口没有置顶")
        time.sleep(2)
        gcp.click_text("取消置顶")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0221():
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
    def test_msg_xiaoqiu_0221(self):
        """聊天设置页面——打开置顶聊天功能——置顶二个聊天会话窗口"""
        # 1、打开二个群聊或者单聊的置顶聊天功能，后续接收到消息时，后面置顶的聊天会话窗口是否会展示在第一个置顶的聊天会话窗口上方
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        time.sleep(2)
        if gcp.is_element_exit_("置顶聊天"):
            gcp.click_element_("置顶聊天")
        else:
            gcp.page_up()
            time.sleep(2)
            gcp.click_element_("置顶聊天")
        current_mobile().launch_app()
        #置顶单聊
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择手机联系人
        sc = SelectContactsPage()
        sc.click_phone_contact()
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        chat = SingleChatPage()
        time.sleep(2)
        if gcp.is_text_present("1元/条"):
            chat.click_i_have_read()
        gcp.input_text_message("哈哈")
        gcp.send_message()
        gcp.click_setting()
        time.sleep(2)
        if gcp.is_element_exit_("置顶聊天"):
            gcp.click_element_("置顶聊天")
        else:
            gcp.page_up()
            time.sleep(2)
            gcp.click_element_("置顶聊天")
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        if not gcp.is_text_present(group_name):
            raise AssertionError("会话窗口没有置顶")
        gcp.press_element_by_text(group_name, 3000)
        time.sleep(2)
        if not gcp.is_text_present("取消置顶"):
            raise AssertionError("会话窗口没有置顶")
        time.sleep(2)
        gcp.click_text("取消置顶")
        gcp.press_element_by_text("飞信电话", 3000)
        time.sleep(2)
        gcp.click_text("取消置顶")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0222():
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
    def test_msg_xiaoqiu_0222(self):
        """聊天设置页面——关闭置顶聊天"""
        # 1、点击置顶聊天功能右边的开关，是否可以关闭置顶聊天功能
        # 2、置顶聊天功能关闭后，返回到消息列表，接收一条消息，聊天会话窗口在消息列表展示时，是否会随着其他聊天窗口的新消息进行排序
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("hh")
        gcp.send_message()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        time.sleep(2)
        if gcp.is_element_exit_("置顶聊天"):
            gcp.click_element_("置顶聊天")
        else:
            gcp.page_up()
            time.sleep(2)
            gcp.click_element_("置顶聊天")
        current_mobile().launch_app()
        mess = MessagePage()
        mess.wait_for_page_load()
        group_name = Preconditions.get_group_chat_name_double()
        mess.click_text(group_name)
        #取消置顶
        gcp.click_setting()
        time.sleep(2)
        if gcp.is_element_exit_("置顶聊天"):
            gcp.click_element_("置顶聊天")
        else:
            gcp.page_up()
            time.sleep(2)
            gcp.click_element_("置顶聊天")
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        if not gcp.is_text_present(group_name):
            raise AssertionError("聊天会话窗口在消息列表展示失败")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0230():
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
    def test_msg_xiaoqiu_0230(self):
        """聊天设置页面，删除并退出群聊——群主"""
        # 1、在聊天设置页面
        # 2、点击页面底部的“删除并退出”按钮，把群主转让给选择的群成员后，是否会退出当前群聊并返回到消息列表，收到一条系统消息：你已退出群
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present("系统消息"):
            raise AssertionError("系统消息不显示")
        mess.click_text("系统消息")
        time.sleep(2)
        if not mess.is_text_present("你已退出群"):
            raise AssertionError("没有收到一条系统消息：你已退出群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0234():
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
    def test_msg_xiaoqiu_0234(self):
        """消息列表页面——有人@我——然后撤回@消息"""
        # 1、有人 @ 我后再撤回 @ 我的消息，查看消息列表页面是否还会提示有人 @ 我
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("@")
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(2)
        gcp.press_element_by_text("@",3000)
        gcp.click_text("撤回")
        if gcp.is_text_present("知道了"):
            gcp.click_text("知道了")
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("对话窗口显示不正常")
        if mess.is_text_present("有人@我"):
            raise AssertionError("存在有人@我")
        mess.click_text(group_name)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0236():
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
    def test_msg_xiaoqiu_0236(self):
        """普通群——聊天会话页面——超长文本消息中带有@群成员"""
        # 1、超长文本消息中带有 @ 群成员，发送成功后，被 @ 的联系人收到后，是否存在 @ 效果
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("@")
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("对话窗口显示不正常")
        if not mess.is_text_present("有人@我"):
            raise AssertionError("不存在有人@我")
        mess.click_text(group_name)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0237():
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
    def test_msg_xiaoqiu_0237(self):
        """群聊天会话页面——复制粘贴的@内容"""
        # 1、复制粘贴的 @ 群成员内容，发送成功后，被 @ 的联系人收到后，是否存在 @ 效果
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        gcp.input_text_message("@")
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(2)
        message_=gcp.get_message_text_by_number()
        gcp.press_element_by_text("@", 3000)
        gcp.click_text("撤回")
        if gcp.is_text_present("知道了"):
            gcp.click_text("知道了")
        gcp.input_text_message(message_)
        gcp.send_message()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("对话窗口显示不正常")
        if not mess.is_text_present("有人@我"):
            mess.click_text(group_name)
            Preconditions.delete_record_group_chat()
            raise AssertionError("不存在有人@我")
        mess.click_text(group_name)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0238():
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
    def test_msg_xiaoqiu_0238(self):
        """群聊天会话页面——输入多个@后——再选要@的群成员查看@效果"""
        # 1、输入多个 @ 后再选要 @ 的群成员，发送成功后，被 @ 的联系人收到后，是否存在 @ 效果
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        gcp.input_text_message("@@@")
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("对话窗口显示不正常")
        if not mess.is_text_present("有人@我"):
            mess.click_text(group_name)
            Preconditions.delete_record_group_chat()
            raise AssertionError("不存在有人@我")
        mess.click_text(group_name)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0239():
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
    def test_msg_xiaoqiu_0239(self):
        """群聊天会话页面——同时@多个人——@效果展示"""
        # 1、同时 @ 多群成员联系人，发送成功后，被 @ 的联系人收到后，是否存在 @ 效果
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        gcp.input_text_message("@")
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("对话窗口显示不正常")
        if not mess.is_text_present("有人@我"):
            mess.click_text(group_name)
            Preconditions.delete_record_group_chat()
            raise AssertionError("不存在有人@我")
        mess.click_text(group_name)
        time.sleep(2)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0252():
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
    def test_msg_xiaoqiu_0252(self):
        """A被B——移除普通群——群聊解散"""
        # 1、B使用群主权限把A从普通群中移除后，A是否会收到一体系统消息：你已被请出该群
        # 2、消息列表，是否会保存被移除群聊的会话窗口
        # 3、群聊人数小于2人时，是否会自动解散
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("hh")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("移除群成员减号")
        time.sleep(3)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        gcp.click_text("确定")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(10)
        if not gcp.is_text_present("该群已解散"):
            raise AssertionError("群聊人数小于2人时，不会自动解散")
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("不会保存被移除群聊的会话窗口")
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        if not mess.is_text_present("你已被请出该群"):
            raise AssertionError("不会收到系统消息：你已被请出该群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0253():
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

    @tags('ALL', 'CMCC_double','full', 'full-yyx')
    def test_msg_xiaoqiu_0253(self):
        """A被B——移除普通群——群聊存在"""
        # 1、B使用群主权限把A从群聊中移除后，A是否会收到一体系统消息：你已被请出群
        # 2、消息列表，是否会保存被移除群聊的会话窗口
        # 3、群聊人数大于2人时，是否会自动解散
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("移除群成员减号")
        time.sleep(3)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        gcp.click_text("确定")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(10)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("不会保存被移除群聊的会话窗口")
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        if not mess.is_text_present("你已被请出该群"):
            raise AssertionError("不会收到系统消息：你已被请出该群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0381():
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
    def test_msg_xiaoqiu_0381(self):
        """验证群主在群设置页面点击—移除群成员A后,A收到的群消息是否正确"""
        # 1、群主点击—删除A
        # 2、A在会话窗口收到提示
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("hh")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("移除群成员减号")
        time.sleep(3)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        gcp.click_text("确定")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(10)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("不会保存被移除群聊的会话窗口")
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        mess.click_text(group_name)
        time.sleep(2)
        if not mess.is_text_present("你已被请出该群"):
            raise AssertionError("不会收到群消息：你已被请出该群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0382():
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
    def test_msg_xiaoqiu_0382(self):
        """验证群主在群设置页面点击—移除群成员A后,A收到的系统消息是否正确"""
        # 1、群主点击—删除A
        # 2、A在消息列表页收到系统消息，点击查看
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("移除群成员减号")
        time.sleep(3)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        gcp.click_text("确定")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(10)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        if not mess.is_text_present("你已被请出该群"):
            raise AssertionError("不会收到系统消息：你已被请出该群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0383():
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
    def test_msg_xiaoqiu_0383(self):
        """验证群主在群设置页面点击—移除群成员A后其他群成员B是否有提示"""
        # 1、群主点击—删除A
        # 2、B查看系统消息和群会话窗口
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("移除群成员减号")
        time.sleep(3)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        gcp.click_text("确定")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(10)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        if not mess.is_text_present("你已被请出该群"):
            raise AssertionError("不会收到系统消息：你已被请出该群")
        Preconditions.change_mobile('Android-移动')
        if mess.is_text_present("被请出该群"):
            raise AssertionError("其他群成员会收到提示")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0384():
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
    def test_msg_xiaoqiu_0384(self):
        """验证群主在群设置页面——修改群名称后——全员收到的提示"""
        # 1、群主点击右上角的群设置按钮
        # 2、群主点击群名称进行修改
        # 3、全员在会话窗口查看提示
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_element_("群名称")
        time.sleep(2)
        gcsp.input_new_group_name(group_name+'change')
        time.sleep(2)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("没有修改成功弹窗")
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name+'change')
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        if not gcp.is_text_present("群名称已修改为"):
            raise AssertionError("全员没有收到提示")
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name+'change')
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_element_("群名称")
        time.sleep(2)
        gcsp.input_new_group_name(group_name)
        time.sleep(2)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称没有还原成功")
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0385():
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
    def test_msg_xiaoqiu_0385(self):
        """验证群主在设置页面——点击群管理——点击解散群按钮后——全员收到的群消息"""
        # 1、群主点击右上角的群设置按钮，点击群管理，点击解散群，点击确认解散群
        # 2、全员查看群消息提示
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("hh")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_element_("群管理")
        time.sleep(2)
        gcsp.click_element_("解散群")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(8)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("不会保存被移除群聊的会话窗口")
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        mess.click_text(group_name)
        time.sleep(2)
        if not mess.is_text_present("该群已解散"):
            raise AssertionError("不会收到群消息：该群已解散")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0386():
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
    def test_msg_xiaoqiu_0386(self):
        """验证群主在设置页面——点击群管理——点击解散群按钮后——全员收到的系统消息"""
        # 1、群主点击右上角的群设置按钮，点击群管理，点击解散群，点击确认解散群
        # 2、全员查看系统消息消息提示
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_element_("群管理")
        time.sleep(2)
        gcsp.click_element_("解散群")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(8)
        # group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        time.sleep(2)
        if not mess.is_text_present("该群已解散"):
            raise AssertionError("不会收到系统消息：该群已解散")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0389():
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
    def test_msg_xiaoqiu_0389(self):
        """验证群主在群设置页面——将所有群成员移出群后——群成员收到的群消息"""
        # 1、点击 - 删除群成员，全选群成员进行删除
        # 2、群成员查看群消息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("hh")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("移除群成员减号")
        time.sleep(3)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        gcp.click_text("确定")
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(10)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("不会保存被移除群聊的会话窗口")
        if not mess.is_text_present("系统消息"):
            raise AssertionError("没有出现系统信息")
        mess.click_text(group_name)
        time.sleep(2)
        if not mess.is_text_present("你已被请出该群"):
            raise AssertionError("不会收到群消息：你已被请出该群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0390():
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
    def test_msg_xiaoqiu_0390(self):
        """验证群成员在群设置页面——点击删除并退出按钮后——群主收到的群消息"""
        # 1、群成员在群设置页面点击删除并退出按钮
        # 2、群主查看群消息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("hh")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        mess = MessagePage()
        mess.wait_for_page_load()
        Preconditions.change_mobile('Android-移动')
        mess.wait_for_page_load()
        if not mess.is_text_present(group_name):
            raise AssertionError("消息列表显示不正确")
        mess.click_text(group_name)
        time.sleep(2)
        if not mess.is_text_present("已退出群"):
            raise AssertionError("没有收到一条群消息：某某已退出群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0393():
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
    def test_msg_xiaoqiu_0393(self):
        """验证群主在设置页面——点击群管理——点击群主管理权转让——转让给群成员A后——A收到的群消息"""
        # 1、群主点击群管理，点击群主管理权转让，转让给A
        # 2、A查看群消息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_element_("群管理")
        time.sleep(2)
        gcsp.click_element_("群主管理权转让")
        time.sleep(2)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(8)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        if not gcp.is_text_present("你已成为群主"):
            raise AssertionError("没有出现：你已成为群主")
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_element_("群管理")
        time.sleep(2)
        gcsp.click_element_("群主管理权转让")
        time.sleep(2)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.click_element_("确定移除")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0394():
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
    def test_msg_xiaoqiu_0394(self):
        """验证群主在设置页面——点击群管理——点击群主管理权转让——转让给群成员A后——A收到的系统消息"""
        # 1、群主点击群管理，点击群主管理权转让，转让给A
        # 2、A查看系统消息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_element_("群管理")
        time.sleep(2)
        gcsp.click_element_("群主管理权转让")
        time.sleep(2)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(8)
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        if not gcp.is_text_present("系统消息"):
            raise AssertionError("没有出现系统消息")
        if not gcp.is_text_present("你已成为群主"):
            raise AssertionError("没有出现系统消息：你已成为群主")
        # 还原初始状态
        Preconditions.go_to_group_double(group_name)
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_element_("群管理")
        time.sleep(2)
        gcsp.click_element_("群主管理权转让")
        time.sleep(2)
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        time.sleep(2)
        gcp.click_element_("确定移除")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0395():
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
    def test_msg_xiaoqiu_0395(self):
        """验证被邀请人A在系统消息页面——点击同意邀请后——其他群成员收到的群消息"""
        # 1、A在系统消息也没得点击同意进群邀请
        # 2、其他群成员查看群消息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 先退出群再重新建群
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(3)
        #重新建群
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.build_one_new_group_with_number(phone_number, group_name)
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text("系统消息")
        time.sleep(3)
        mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        if not (gcp.is_text_present("欢迎") and gcp.is_text_present("加入群")):
            raise AssertionError("群没有显示欢迎加入群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0396():
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
    def test_msg_xiaoqiu_0396(self):
        """验证被邀请人A在系统消息页面——点击同意邀请后——A收到的群消息"""
        # 1、A在系统消息也没得点击同意进群邀请
        # 2、A查看群消息
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 先退出群再重新建群
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(3)
        #重新建群
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.build_one_new_group_with_number(phone_number, group_name)
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text("系统消息")
        time.sleep(3)
        mess.click_text("同意")
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        if not (gcp.is_text_present("欢迎") and gcp.is_text_present("加入群")):
            raise AssertionError("群没有显示欢迎加入群")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0398():
        """先建一个群可以来分享群二维码"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0398(self):
        """验证被邀请人A长按识别群二维码加入群后——其他群成员收到的群消息"""
        # 1、A在会话窗口长按识别未加入群的群二维码，点击加入群聊
        # 2、其他群成员查看群消息
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if mess.is_text_present(phone_number2):
            mess.press_file_to_do(phone_number2,"删除聊天")
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_element_("二维码转发")
        sc = SelectContactsPage()
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("群二维码转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        if not mess.is_text_present(phone_number2):
            raise AssertionError("没有接收到群二维码")
        gcp.click_text(phone_number2)
        time.sleep(2)
        gcp.click_element_("消息图片")
        time.sleep(2)
        gcp.press_xy()
        gcp.click_text("识别图中二维码")
        time.sleep(3)
        gcp.click_element_("加入群聊")
        gcp.wait_for_page_load()
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        if not (gcp.is_text_present("欢迎") and gcp.is_text_present("加入群")):
            raise AssertionError("群没有显示欢迎加入群")
        gcp.wait_for_page_load()
        # 删除群
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(3)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0399():
        """先建一个群可以来分享群二维码"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0399(self):
        """验证被邀请人A长按识别群二维码加入群后——A收到的群消息"""
        # 1、A在会话窗口长按识别未加入群的群二维码，点击加入群聊
        # 2、A查看群消息
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        if mess.is_text_present(phone_number2):
            mess.press_file_to_do(phone_number2,"删除聊天")
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_element_("二维码转发")
        sc = SelectContactsPage()
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("群二维码转发失败")
        Preconditions.change_mobile('Android-移动-移动')
        if not mess.is_text_present(phone_number2):
            raise AssertionError("没有接收到群二维码")
        gcp.click_text(phone_number2)
        time.sleep(2)
        gcp.click_element_("消息图片")
        time.sleep(2)
        gcp.press_xy()
        gcp.click_text("识别图中二维码")
        time.sleep(3)
        gcp.click_element_("加入群聊")
        gcp.wait_for_page_load()
        if not (gcp.is_text_present("欢迎") and gcp.is_text_present("加入群")):
            raise AssertionError("群没有显示欢迎加入群")
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 删除群
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(3)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0401():
        """先建一个群可以来分享群二维码"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0401(self):
        """验证群主A或群成员B在设置页面——点击+邀请群成员C后——C收到的系统消息"""
        # 1、群主A或群成员B在群设置页面点击 + 添加C
        # 2、C点击查看系统消息
        Preconditions.change_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("添加群成员加号")
        sc = SelectContactsPage()
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        gcp.click_text("确定")
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text("系统消息")
        time.sleep(3)
        if not mess.is_text_present("邀请你加入群"):
            raise AssertionError("没有系统消息：邀请你加入群")
        mess.click_text("同意")
        gcp.wait_for_page_load()
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 删除群
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(3)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0403():
        """先建一个群可以来分享群二维码"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0403(self):
        """验证群主A点击消息列表右上角的+——发起群聊/点对点建群/点击通讯录右上角，创建群后被邀请人收到的系统消息"""
        # 1、A选择联系人后进行创建群
        # 2、被邀请人点击查看系统消息
        Preconditions.change_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcp.click_element_("添加群成员加号")
        sc = SelectContactsPage()
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        gcp.click_text("确定")
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text("系统消息")
        time.sleep(3)
        if not mess.is_text_present("邀请你加入群"):
            raise AssertionError("没有系统消息：邀请你加入群")
        mess.click_text("同意")
        gcp.wait_for_page_load()
        Preconditions.change_mobile('Android-移动')
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 删除群
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击删除并退出
        gcsp.click_delete_and_exit()
        time.sleep(2)
        gcp.click_element_("确定移除")
        time.sleep(3)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0442():
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
    def test_msg_xiaoqiu_0442(self):
        """（普通消息体）聊天会话页面——5分钟内——不连续发送文本消息体"""
        # 1、5分钟内，发送方发送的消息，被其它消息中途分割时，被分割的部分消息是否会另起一个头像和昵称
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("1")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.input_text_message("2")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.input_text_message("3")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_xiaoqiu_0240(self):
        """消息草稿-聊天列表显示-输入空格消息"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、再输入空格不发送返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        info = " "
        gcp.input_message(info)
        gcp.click_back()
        mess = MessagePage()
        if mess.is_on_this_page():
            if mess.is_text_present("草稿"):
                raise AssertionError("有草稿标识出现")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_xiaoqiu_0241(self):
        """消息草稿-聊天列表显示-不输入任何消息"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        # 3、不输入任何信息返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        info = ""
        gcp.input_message(info)
        if gcp.is_on_this_page():
            if gcp.is_element_exit_("文本发送按钮"):
                raise AssertionError("有发送按钮")
        gcp.click_back()
        mess = MessagePage()
        if mess.is_on_this_page():
            if mess.is_text_present("草稿"):
                raise AssertionError("有草稿标识出现")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'high', 'yx')
    def test_msg_xiaoqiu_0244(self):
        """消息草稿-聊天列表显示-输入特殊字符"""
        # 1、删除聊天记录
        # 2、先发送一条信息确保在消息页可以看到
        # 3、输入特殊字符返回消息页面
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        info = "*……%#"
        self.message = gcp.input_message(info)
        gcp.click_back()
        mess = MessagePage()
        if mess.is_on_this_page():
            if not mess.is_text_present("草稿"):
                raise AssertionError("没有草稿标识出现")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0024(self):
        """企业群/党群在消息列表内展示——最新消息时间（修改手机时间可以测试）"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_back()
        mess = MessagePage()
        time.sleep(3)
        exist = mess.is_text_present("刚刚")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0025(self):
        """企业群/党群在消息列表内展示——最新消息时间（修改手机时间可以测试）"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_back()
        mess = MessagePage()
        # 暂时这样判断处理
        exist = mess.is_text_present(":")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0031(self):
        """企业群/党群在消息列表内展示——最新消息展示——文字及表情"""
        # 1、删除聊天记录
        # 2、选择一个群输入先发送一条信息确保在消息页可以看到
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
        # 输入信息
        gcp.input_message("测试超长文字测试超长文字测试超长文字")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_back()
        mess = MessagePage()
        if mess.is_on_this_page():
            exist = mess.is_text_present("…")
            self.assertEqual(exist, True)
            # if not mess.is_text_present("测试超长文字"):
            #     raise AssertionError("测试超长文字")

    @tags('ALL', 'CMCC', 'group_chat', 'yx')
    def test_msg_xiaoqiu_0162(self):
        """群主——清除旧名片——录入10个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        # 4.输入10个字母
        gcsp.input_my_group_card_name("aaabbbcccd")
        # 5.点击保存
        gcsp.save_group_card_name()
        # flag = gcsp.is_toast_exist("修改成功")
        # if not flag:
        #     raise AssertionError("没有'修改成功'提示框提示")

    @tags('ALL', 'CMCC', 'group_chat', 'yx')
    def test_msg_xiaoqiu_0171(self):
        """群主——清除旧名片——录入特殊字符"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        # 4.输入特殊字符
        gcsp.input_my_group_card_name("！@#")
        # 5.点击保存
        gcsp.save_group_card_name()
        time.sleep(1)
        # 6.点击群名片
        gcsp.click_modify_my_group_name()
        time.sleep(1)
        # 7.点击‘X’按钮清空群昵称
        gcsp.click_iv_delete_button()
        # 8.判断群名片为空时，是否可以点击完成按钮
        self.assertFalse(gcsp.save_btn_is_enabled())

    @tags('ALL', 'CMCC', 'group_chat', 'yx')
    def test_msg_xiaoqiu_0172(self):
        """群二维码入口详情页"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主/群成员
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群二维码
        gcsp.click_QRCode()
        gcsp.click_qecode_download_button()
        gcsp.is_toast_exist("已保存")
        # 3.点击返回
        gcsp.click_back()
        time.sleep(2)
        # 4.判断当前页面是否在群聊设置页面
        self.assertTrue(gcsp.is_on_this_page())

