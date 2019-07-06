import random
import re
import time
import unittest
import uuid
import warnings

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage
from pages.otherpages.HasRead import HasRead
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage

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
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

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
    def search_into_group_chat_page(name):
        """搜索群后，选择该群，并进入群聊聊天会话页面"""
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
        # 搜索群组
        sog.click_search_group()
        sog.input_search_keyword(name)
        # 选择一个普通群（企业群）
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def get_into_group_chat_page2():
        """进入企业群聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        name = sog.select_one_enterprise_group()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        return name

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
    def get_current_activity_name():
        import os, sys
        global findExec
        findExec = 'findstr' if sys.platform == 'win32' else 'grep'
        device_name = current_driver().capabilities['deviceName']
        cmd = 'adb -s %s shell dumpsys window | %s mCurrentFocus' % (device_name, findExec)
        res = os.popen(cmd)
        time.sleep(2)
        # 截取出activity名称 == ''为第三方软件
        current_activity = res.read().split('u0 ')[-1].split('/')[0]
        res.close()
        return current_activity


class MsgGroupChatVideoPicAllTest(TestCase):
    """
    模块：群聊-图片视频-GIF
    文件位置：1.1.3全量测试用例->113全量用例--肖立平.xlsx
    表格：群聊-图片视频-GIF
    Author:刘晓东
    """

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore',ResourceWarning)
    #
    #     Preconditions.select_mobile('Android-移动')
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             current_mobile().hide_keyboard_if_display()
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break
    #
    #     # 导入团队联系人
    #     fail_time2 = 0
    #     flag2 = False
    #     while fail_time2 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
    #             Preconditions.create_he_contacts(contact_names)
    #             flag2 = True
    #         except:
    #             fail_time2 += 1
    #         if flag2:
    #             break
    #
    #     # 确保有企业群
    #     fail_time3 = 0
    #     flag3 = False
    #     while fail_time3 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             Preconditions.ensure_have_enterprise_group()
    #             flag3 = True
    #         except:
    #             fail_time3 += 1
    #         if flag3:
    #             break
    #
    #     # 确保测试手机有resource文件夹
    #     name = "群聊1"
    #     Preconditions.get_into_group_chat_page(name)
    #     gcp = GroupChatPage()
    #     gcp.wait_for_page_load()
    #     gcp.click_more()
    #     cmp = ChatMorePage()
    #     cmp.click_file()
    #     csfp = ChatSelectFilePage()
    #     csfp.wait_for_page_load()
    #     csfp.click_local_file()
    #     local_file = ChatSelectLocalFilePage()
    #     # 没有预置文件，则上传
    #     local_file.push_preset_file()
    #     local_file.click_back()
    #     csfp.wait_for_page_load()
    #     csfp.click_back()
    #     gcp.wait_for_page_load()

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、确保当前页面在群聊聊天会话页面
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        name = "群聊1"
        if mp.is_on_this_page():
            Preconditions.get_into_group_chat_page(name)
            return
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page(name)

    def default_tearDown(self):
        pass
        # Preconditions.make_already_in_message_page()
        # cdp = ContactDetailsPage()
        # cdp.delete_all_contact()
    # def is_search_contacts_number_full_match(self, number):
    #     """搜索联系人号码是否精准匹配"""
    #     els = self.get_elements(self.__class__.__locators["联系人号码"])
    #     texts = []
    #     for el in els:
    #         text = el.text.strip()
    #         if text:
    #             texts.append(text)
    #     for t in texts:
    #         if number == t:
    #             return True
    #     raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的号码'.format(texts, number))
    #

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0230(self):
        """群聊会话页面，发送一条网页消息"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_message('http://www.baidu.com')
        # 发送消息
        gcp.send_message()
        gcp.click_back()
        cwp = ChatWindowPage()
        # 5.验证是否发送成功
        if not cwp.wait_for_msg_send_status_become_to('发送成功', 30):
            raise RuntimeError('发送失败')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0231(self):
        """企业群/党群会话页面，发送一网页消息"""
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page2()
        msg = 'http://www.baidu.com'
        gcp.input_message(msg)
        gcp.send_message()
        cwp = ChatWindowPage()
        # 5.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        gcp.click_back()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0130(self):
        """
            1、点击添加成员的“+”号按钮，跳转到联系人选择器页面
            2、选择一个已存在当前群聊的联系人，是否会弹出toast提示：该联系人不可选并且选择失败"
        """
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page2()
        gcp.click_setting()
        page = GroupChatSetPage()
        page.wait_for_page_load()
        page.click_add_member()
        from pages.chat.ChatGroupAddContacts import ChatGroupAddContactsPage
        contacts_page = ChatGroupAddContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_d()
        contacts_page.select_one_member_by_name('大佬2')
        if not contacts_page.is_toast_exist('该联系人不可选择'):
            raise RuntimeError('不可选联系人难失败')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0136(self):
        """
            1、点击添加成员的“+”号按钮，跳转到联系人选择器页面
            2、选择一个已存在当前群聊的联系人，是否会弹出toast提示：该联系人不可选并且选择失败"
        """
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('a0071')
        gcp.click_setting()
        page = GroupChatSetPage()
        page.wait_for_page_load()
        page.click_del_member()
        from pages.otherpages.RemoveMember import RemoveMember
        rm = RemoveMember()
        time.sleep(2)
        rm.select_member_by_name('测试147')
        rm.click_sure()
        rm.click_ok()
        page.click_back()
        time.sleep(1)
        num = 0
        while num < 30:
            if not rm.is_element_exist('该群已解散'):
                time.sleep(1)
                num += 1
                continue
            else:
                break
        else:
            raise RuntimeError('解散群失败')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0244(self):
        """群聊会话页面，发送一条含有特殊符号的消息，点击返回，检查是否包含‘草稿’字样"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        msg = '#￥￥*&￥（*&^#!#%&&￥$$$**&'
        gcp.input_message(msg)
        # 发送消息
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        exist = mp.page_contain_element('草稿')
        if not exist:
            raise RuntimeError('当前页面不包含‘草稿’字样')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0079(self):
        """
            1、在输入框录入内容，然后点击发送按钮，进行发送，发送成功后的消息体下方是否会展示：已读动态，4个字的文案
            2、点击下方的已读动态，是否会跳转页面已读动态详情页面
            3、在已读动态详情页面，已读分类是否会展示，已读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # 判断是否有重发按钮，如果有，点击重发
        while gcp.is_exist_msg_send_failed_button():
            gcp.click_msg_send_failed_button()
            gcp.click_resend_confirm()
            time.sleep(1)
        # 发送测试消息
        gcp.input_message('大家好，这里是测试消息')
        gcp.send_message()
        cwp = ChatWindowPage()
        # 5.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 是否有[已读动态图标]
        if gcp.is_exist_msg_has_read_icon():
            # 点击已读动态图标
            gcp.click_has_read_icon()
            hr = HasRead()
            hr.wait_for_page_load()
            hr.click_has_read()
            # 如果有已读联系人，点击第一个
            hr.click_first_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            if not cdp.is_on_this_page():
                raise RuntimeError('打开联系人详情页面出错')
        else:
            raise RuntimeError('没有找到[已读动态]标识')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0080(self):
        """
            1、点击消息体下方的已读动态，跳转页面已读动态详情页面
            2、在已读动态详情页面，未读分类会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # 判断是否有重发按钮，如果有，点击重发
        while gcp.is_exist_msg_send_failed_button():
            gcp.click_msg_send_failed_button()
            gcp.click_resend_confirm()
            time.sleep(1)
        # 发送测试消息
        gcp.input_message('大家好，这里是测试消息')
        gcp.send_message()
        cwp = ChatWindowPage()
        # 5.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 是否有[已读动态图标]
        if gcp.is_exist_msg_has_read_icon():
            # 点击已读动态图标
            gcp.click_has_read_icon()
            hr = HasRead()
            hr.wait_for_page_load()
            hr.click_has_not_read()
            # 如果有已读联系人，点击第一个
            hr.click_first_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            if not cdp.is_on_this_page():
                raise RuntimeError('打开联系人详情页面出错')
        else:
            raise RuntimeError('没有找到[已读动态]标识')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0081(self):
        """
            企业群，发送语音消息——已读状态——已读分类
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语音模式
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
        # 1、点击语音按钮，设置模式后，开始录制，输入框中识别出内容后，点击发送按钮，进行发送，发送成功后的消息体下方会展示：已读动态，4个字的文案
        if gcp.is_exist_msg_has_read_icon():
            # 2、点击下方的已读动态，会跳转页面已读动态详情页面
            gcp.click_has_read_icon()
            time.sleep(1)
            exist =gcp.is_text_present("已读动态")
            self.assertEqual(exist, True)
        else:
            raise RuntimeError('没有找到[已读动态]标识')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0082(self):
        """
            企业群，发送语音消息——已读状态——未读分类
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语音模式
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
        # 1、点击下方的已读动态，会跳转页面已读动态详情页面
        if gcp.is_exist_msg_has_read_icon():
            gcp.click_has_read_icon()
            time.sleep(1)
            exist = gcp.is_text_present("已读动态")
            self.assertEqual(exist, True)
        else:
            raise RuntimeError('没有找到[已读动态]标识')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0083(self):
        """
            1、点击消息体下方的已读动态，跳转页面已读动态详情页面
            2、在已读动态详情页面，未读分类会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # 判断是否有重发按钮，如果有，点击重发
        while gcp.is_exist_msg_send_failed_button():
            gcp.click_msg_send_failed_button()
            gcp.click_resend_confirm()
            time.sleep(1)
        # 发送测试消息
        gcp.input_message('[呲牙1]')
        gcp.send_message()
        cwp = ChatWindowPage()
        # 5.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 是否有[已读动态图标]
        if gcp.is_exist_msg_has_read_icon():
            # 点击已读动态图标
            gcp.click_has_read_icon()
            hr = HasRead()
            hr.wait_for_page_load()
            hr.click_has_read()
            # 如果有已读联系人，点击第一个
            hr.click_first_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            if not cdp.is_on_this_page():
                raise RuntimeError('打开联系人详情页面出错')
        else:
            raise RuntimeError('没有找到[已读动态]标识')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_xiaoqiu_0084(self):
        """
            1、在输入框右边的表情图标，展示表情列表，任意点击选中几个表情展示到输入框中，然后点击发送按钮，进行发送，发送成功后的消息体下方会展示：已读动态，4个字的文案
            2、点击下方的已读动态，会跳转页面已读动态详情页面
            3、在已读动态详情页面，已读分类会展示，已读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # 判断是否有重发按钮，如果有，点击重发
        while gcp.is_exist_msg_send_failed_button():
            gcp.click_msg_send_failed_button()
            gcp.click_resend_confirm()
            time.sleep(1)
        # 发送测试消息
        gcp.input_message('[呲牙1]')
        gcp.send_message()
        cwp = ChatWindowPage()
        # 5.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 是否有[已读动态图标]
        if gcp.is_exist_msg_has_read_icon():
            # 点击已读动态图标
            gcp.click_has_read_icon()
            hr = HasRead()
            hr.wait_for_page_load()
            hr.click_has_not_read()
            # 如果有已读联系人，点击第一个
            hr.click_first_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            if not cdp.is_on_this_page():
                raise RuntimeError('打开联系人详情页面出错')
        else:
            raise RuntimeError('没有找到[已读动态]标识')

    @tags('ALL', 'CMCC', 'YL')
    def test_msg_xiaoqiu_0091(self):
        """语音消息，发送中途，网络异常"""
        Preconditions.delete_record_group_chat()
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语音模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 等待0.1秒
        time.sleep(0.1)
        # 恢复网络
        gcp.set_network_status(6)
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'YL')
    def test_msg_huangmianhua_0046(self):
        """
            企业群/党群在消息列表内展示——免打扰
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        if not switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)
        # 免打扰时右下角免打扰标识
        group_set.click_back()
        time.sleep(1)
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        flag = mess.is_exist_no_disturb_icon()
        self.assertEqual(flag, True)

    @tags('ALL', 'CMCC', 'YL')
    def test_msg_huangmianhua_0047(self):
        """
            企业群/党群在消息列表内展示——长按/左划出功能选择弹窗——安卓（长按）
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        time.sleep(1)
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        mess.selecting_one_group_press_by_name('测试企业群')
        # 1.弹窗本身:弹窗本身样式是否正常,点击弹窗外应收回弹窗
        # 2.标为已读:无未读则不出现该选项
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, True)
        exist = mess.is_text_present("标为已读")
        self.assertEqual(exist, False)
        gcp.click_back_by_android()
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, False)
        # 3.置顶聊天:已置顶则显示“取消置顶”
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        mess.press_groupname_to_do("置顶聊天")
        # 置顶聊天后，再次显示：取消置顶
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        exist = mess.is_text_present("取消置顶")
        self.assertEqual(exist, True)
        # 4.删除聊天
        # 删除聊天前，取消置顶
        mess.press_groupname_to_do("取消置顶")
        time.sleep(1)
        # 再次 删除聊天
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        mess.press_groupname_to_do("删除聊天")
        exist = mess.is_text_present("测试企业群")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'YL')
    def test_msg_huangmianhua_0048(self):
        """
            企业群/党群在消息列表内展示——长按/左划出功能选择弹窗
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        time.sleep(1)
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()

        mess.selecting_one_group_press_by_name('测试企业群')
        # 1.弹窗本身:弹窗本身样式是否正常,点击弹窗外应收回弹窗
        # 2.标为已读:无未读则不出现该选项
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, True)
        # exist = mess.is_text_present("标为已读")
        # self.assertEqual(exist, False)
        gcp.click_back_by_android()
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, False)
        # 3.置顶聊天:已置顶则显示“取消置顶”
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        mess.press_groupname_to_do("置顶聊天")
        # 置顶聊天后，再次显示：取消置顶
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        exist = mess.is_text_present("取消置顶")
        self.assertEqual(exist, True)
        # 4.删除聊天
        # 删除聊天前，取消置顶
        mess.press_groupname_to_do("取消置顶")
        time.sleep(1)
        # 再次 删除聊天
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        mess.press_groupname_to_do("删除聊天")
        exist = mess.is_text_present("测试企业群")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0101(self):
        """在群聊设置页面，群成员头像展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 没有头像展示为对应昵称的首字母或数字大写 yaolei "Y"
            exist = gcp.is_text_present("Y")
            self.assertEqual(exist, True)
            time.sleep(1)
            # 回到聊天界面
            gcsp.click_back()
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0102(self):
        """在群聊设置页面，群成员头像上方文案展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            exist = gcp.is_text_present("群成员")
            self.assertEqual(exist, True)
            exist = gcp.is_text_present("群聊设置")
            self.assertEqual(exist, True)
            time.sleep(1)
            # 返回到聊天界面
            gcsp.click_back()
            exist = gcp.is_text_present("群聊设置")
            self.assertEqual(exist, False)
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0103(self):
        """在群聊设置页面，群成员头像上方文案展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            exist = gcp.is_text_present("D")
            self.assertEqual(exist, True)
            exist = gcp.is_text_present("大佬1")
            self.assertEqual(exist, True)
            time.sleep(1)
            # 返回到聊天界面
            gcsp.click_back()
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0104(self):
        """在群聊设置页面，群成员头像上方文案展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            gcsp.click_group_member_show()
            time.sleep(1)
            exist = gcp.is_text_present("群成员")
            self.assertEqual(exist, True)
            #  选择一个群成员
            gcp.click_text("大佬1")
            time.sleep(1)
            exist = gcp.is_text_present("交换名片")
            self.assertEqual(exist, False)
            gcsp.click_back_by_android()
            time.sleep(1)
            gcsp.click_back_by_android()
            time.sleep(1)
            # 返回到聊天界面
            gcsp.click_back()
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0113(self):
        """在群聊设置页面中——群成员头像展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 最少会展示一个头像 yaolei
            exist = gcp.is_text_present("Y")
            self.assertEqual(exist, True)
            time.sleep(1)
            # 回到聊天界面
            gcsp.click_back()
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0114(self):
        """在群聊设置页面中——群成员头像展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # Checkpoint 校验群主头像皇冠
            GroupChatSetPage().group_chairman_tag_is_exist()
            time.sleep(1)
            # 回到聊天界面
            gcsp.click_back()
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0204(self):
        """
            消息列表——长按——删除会话窗口
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        time.sleep(1)
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        # 长按 "测试企业群"
        mess.selecting_one_group_press_by_name('测试企业群')
        # 1、长按消息列表的会话窗口，会弹出功能菜单列表
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, True)
        # 消息列表 删除"测试企业群"记录
        mess.press_groupname_to_do("删除聊天")
        exist = mess.is_text_present("测试企业群")
        self.assertEqual(exist, False)
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        exist = mess.is_text_present("哈哈")
        self.assertEqual(exist, False)
        # 返回到消息列表界面
        gcp.click_back_by_android()
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0205(self):
        """
            消息列表——长按——删除会话窗口
        """
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        time.sleep(1)
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        # 长按 "测试企业群"
        mess.selecting_one_group_press_by_name('测试企业群')
        # 1、长按消息列表的会话窗口，会弹出功能菜单列表
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, True)
        # 消息列表 删除"测试企业群"记录
        mess.press_groupname_to_do("删除聊天")
        exist = mess.is_text_present("测试企业群")
        self.assertEqual(exist, False)
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        exist = mess.is_text_present("哈哈")
        self.assertEqual(exist, False)
        # 返回到消息列表界面
        gcp.click_back_by_android()
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0209(self):
        """群聊设置页面——点击群成员头像"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        gcp.click_setting()
        time.sleep(1)
        gcp.click_text("大佬1")
        mess = MessagePage()
        # 1、点击未保存在本地的陌生人头像，会跳转到交换名片申请页面
        if not mess.is_text_present("保存到通讯录"):
            raise AssertionError("没有跳转到交换名片申请页面")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0210(self):
        """群聊设置页面——点击已保存在本地通讯录中——群成员头像"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        gcp.click_setting()
        time.sleep(1)
        gcp.click_text("姚磊")
        mess = MessagePage()
        # 1、点击已保存在本地的联系人头像，会跳转到联系人的个人profile页
        if not mess.is_text_present("编辑"):
            raise AssertionError("没有跳转到联系人的个人profile页")
        time.sleep(1)
        gcp.click_text("大佬1")
        mess = MessagePage()
        # 1、点击未保存在本地的陌生人头像，会跳转到交换名片申请页面
        if not mess.is_text_present("保存到通讯录"):
            raise AssertionError("没有跳转到交换名片申请页面")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0211(self):
        """群聊设置页面——点击已保存在本地通讯录中——群成员头像"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        gcp.click_setting()
        time.sleep(1)
        gcp.click_text("姚磊")
        mess = MessagePage()
        # 1、点击已保存在本地的联系人头像，会跳转到联系人的个人profile页
        if not mess.is_text_present("编辑"):
            raise AssertionError("没有跳转到联系人的个人profile页")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0212(self):
        """企业群profile优化：群聊设置页--“>”群成员列表"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # "群成员展开 >
            gcsp.click_group_member_show()
            time.sleep(1)
            # exist = gcp.is_text_present("群成员")
            # self.assertEqual(exist, True)
            #  选择一个群成员
            gcp.click_text("大佬1")
            time.sleep(1)
            exist = gcp.is_text_present("保存到通讯录")
            if exist:
                gcp.click_text("保存到通讯录")
                time.sleep(1)
                gcp.click_text("保存")
                time.sleep(1)
            # 判定
            exist = gcp.is_text_present("分享名片")
            self.assertEqual(exist, True)
            exist = gcp.is_text_present("编辑")
            self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0213(self):
        """企业群profile优化：群聊设置页--“>”群成员列表--搜索结果"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # "群成员展开 >
            gcsp.click_group_member_show()
            time.sleep(1)
            gcp.input_member_message("大佬")
            time.sleep(1)
            #  1、点击已保存本地的联系人成员头像进入profile页 --选择一个群成员
            gcp.click_text("大佬1")
            time.sleep(1)
            exist = gcp.is_text_present("保存到通讯录")
            if exist:
                gcp.click_text("保存到通讯录")
                time.sleep(1)
                gcp.click_text("保存")
                time.sleep(1)
            # 判定
            exist = gcp.is_text_present("分享名片")
            self.assertEqual(exist, True)
            exist = gcp.is_text_present("编辑")
            self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0214(self):
        """企业群profile优化：消息界面——点击消息头像"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # "群成员展开 >
            gcsp.click_group_member_show()
            time.sleep(1)
            gcp.click_text("大佬1")
            time.sleep(1)
            exist = gcp.is_text_present("保存到通讯录")
            if exist:
                gcp.click_text("保存到通讯录")
                time.sleep(1)
                gcp.click_text("保存")
                time.sleep(1)
            # 判定
            exist = gcp.is_text_present("分享名片")
            self.assertEqual(exist, True)
            exist = gcp.is_text_present("编辑")
            self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0258(self):
        """（普通消息体）聊天会话页面——5分钟内——连续发送文本消息体"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        i=0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈"+str(i))
            gcp.send_message()
        time.sleep(1)
        #防止出现 群成员没有使用和飞信信息，干扰判断
        Preconditions.delete_record_group_chat()
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈"+str(i))
            gcp.send_message()
        time.sleep(1)
        # 判断
        groupchat = GroupChatPage()
        self.assertTrue(groupchat.is_multi_show())
        Preconditions.delete_record_group_chat()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0261(self):
        """（普通消息体）聊天会话页面——5分钟内——发送失败的消息——重发"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        #Preconditions.delete_record_group_chat()
        gcp.set_network_status(0)
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈" + str(i))
            gcp.send_message()
        time.sleep(1)
        # 防止出现 群成员没有使用和飞信信息，干扰判断
        Preconditions.delete_record_group_chat()
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈" + str(i))
            gcp.send_message()
        time.sleep(1)
        gcp.set_network_status(6)
        for i in range(2):
            # 重新发送
            cwp = ChatWindowPage()
            cwp.click_resend_button()
            cwp.click_resend_sure()
            time.sleep(1)
        time.sleep(1)
        # 判断
        groupchat = GroupChatPage()
        if not gcp.is_text_present("邀请他们"):
            self.assertTrue(groupchat.is_multi_show())
        self.assertFalse(groupchat.is_multi_show())
        Preconditions.delete_record_group_chat()

    def tearDown_test_msg_huangmianhua_0261(self):
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0262(self):
        """（普通消息体）聊天会话页面——5分钟内——连续发送文本消息体"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈" + str(i))
            gcp.send_message()
        time.sleep(1)
        # 等待5分钟
        time.sleep(5*60)
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈" + str(i))
            gcp.send_message()
        time.sleep(1)
        # 判断
        groupchat = GroupChatPage()
        self.assertFalse(groupchat.is_multi_show())
        Preconditions.delete_record_group_chat()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0264(self):
        """（普通消息体）聊天会话页面——5分钟内——发送失败的消息——重发"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        gcp.set_network_status(0)
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈" + str(i))
            gcp.send_message()
        time.sleep(1)
        # 防止出现 群成员没有使用和飞信信息，干扰判断
        Preconditions.delete_record_group_chat()
        i = 0
        for i in range(2):
            # 发送信息
            gcp.input_message("哈哈" + str(i))
            gcp.send_message()
        time.sleep(1)
        time.sleep(5*60)
        gcp.set_network_status(6)
        for i in range(2):
            # 重新发送
            cwp = ChatWindowPage()
            cwp.click_resend_button()
            cwp.click_resend_sure()
            time.sleep(1)
        time.sleep(1)
        # 判断
        groupchat = GroupChatPage()
        self.assertFalse(groupchat.is_multi_show())
        Preconditions.delete_record_group_chat()

    def tearDown_test_msg_huangmianhua_0264(self):
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0057(self):
        """普通企业群/长ID企业群：三种用户类型打开“+”后是否都展示正常——本网号"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0060(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——消息模块内全局搜索企业群（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 消息页 搜索'测试企业群'
        mess = MessagePage()
        mess.click_search()
        time.sleep(1)
        groupname = "测试企业群"
        mess.input_search_message_631(groupname)
        time.sleep(1)
        mess.selecting_one_group_click_by_name(groupname)
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0061(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——消息模块内发起群聊--选择一个群--搜索企业群（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群，并进入企业群聊天页面
        Preconditions.search_into_group_chat_page('测试企业群')
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0062(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——消息模块内发起群聊--选择一个群--群列表内选择企业群（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0063(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——消息模块内发起群聊--选择一个群--群列表内选择企业群（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        #发送信息
        gcp.input_message("哈哈")
        gcp.send_message()
        # 返回到消息页面
        gcp.click_back()
        # 再次进入企业群聊天页面
        mess = MessagePage()
        mess.selecting_one_group_click_by_name('测试企业群')
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0065(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——通讯录模块--群聊--搜索企业群（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        # 搜索 测试企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword('测试企业群')
        mess.hide_keyboard()
        time.sleep(1)
        # 打开企业群
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0066(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——通讯录模块--群聊--群列表内选择企业群（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        # 选择 测试企业群
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0067(self):
        """普通企业群/长ID企业群：多个入口进入群打开“+”后是否都展示正常——新创建的群从“系统消息”进入后是否及时展示按钮（本网号为例）"""
        # 1、在目标企业后台创建一个企业群--群主（本网）登录和飞信--点击消息模块“系统消息”按钮
        # 2、点击该条系统消息的“进入群”按钮--点击下方输入框右上角的“+”按钮
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        # 选择 测试企业群
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 点击 + 号
        gcp.click_more()
        # 判定  "文件" "卡券"-没有
        exist = gcp.is_text_present("群短信")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("位置")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("红包")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("日志")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0068(self):
        """普通企业群/长ID企业群：进入审批应用后页面样式检查（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        # 选择 测试企业群
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 点击 + 号
        gcp.click_more()
        # 1、正常进入该企业下审批应用一级页面且页面样式及文案与工作台进入审批一致
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        # 点击 审批
        gcp.click_text("审批")
        time.sleep(10)
        exist = gcp.is_text_present("我审批的")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("我发起的")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("抄送我的")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0069(self):
        """普通企业群/长ID企业群：进入审批应用后能否正常返回群聊页面（本网号为例）"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        # 选择 测试企业群
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 点击 + 号
        gcp.click_more()
        # 1、正常进入该企业下审批应用一级页面且页面样式及文案与工作台进入审批一致
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        # 点击 审批
        gcp.click_text("审批")
        time.sleep(3)
        # 点击 < 返回
        gcp.click_back2()
        time.sleep(5)
        # 1、正常返回进入前的群聊页面且群内“+”保持打开状态
        exist = gcp.is_text_present("飞信电话")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0353(self):
        """全局搜索入口——搜索企业群/党群名称默认的三个结果"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("测试企业群")
        mess.hide_keyboard()
        time.sleep(2)
        # 判断
        # 1、全局搜索企业群/党群名称默认的三个结果
        # 2、检查群头像、企业/党群标识、群名称、搜索字符高亮、群人数等元素
        mess.is_exist_the_element("企业头像")
        mess.is_exist_the_element("企业标识")
        mess.is_exist_the_element("企业群名")
        mess.is_exist_the_element("企业成员数量")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0354(self):
        """全局搜索入口——搜索企业群/党群名称默认的三个结果"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("测试企业群")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('测试企业群')
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 普通成员在群聊设置页没有拉人“+”和踢人“-”按钮
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0355(self):
        """全局搜索入口——搜索企业群/党群名称默认的三个结果"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("ag6421")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('ag6421')
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 群主在群聊设置页有拉人“+”和踢人“-”按钮正常展示
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0358(self):
        """全局搜索入口——搜索企业群/党群名称默认的三个结果"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("测试企业群")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('测试企业群')
        # 发送消息
        gcp.input_text_message("123456")
        gcp.send_message()
        gcp.click_back()
        gcp.click_back_by_android()
        time.sleep(1)
        # 1、消息列表内有消息记录的 正常进入和消息记录正常展示
        mess.selecting_one_group_click_by_name("测试企业群")
        time.sleep(1)
        exist =gcp.is_text_present("已读动态")
        self.assertEqual(exist, True)
        exist =gcp.is_text_present("123456")
        self.assertEqual(exist, True)
        # 2、消息列表内没有消息记录的 正常进入和消息记录正常展示
        Preconditions.delete_record_group_chat()
        # 回到消息列表页面
        gcp.click_back()
        mess.selecting_one_group_click_by_name("测试企业群")
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, False)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0359(self):
        """全全局搜索入口——搜索企业群/党群名结果——查看更多列表页"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("测试企业群")
        mess.hide_keyboard()
        time.sleep(2)
        # 判断
        # 1、全局搜索企业群/党群名称默认的三个结果
        # 2、检查群头像、企业/党群标识、群名称、搜索字符高亮、群人数等元素
        mess.is_exist_the_element("企业头像")
        mess.is_exist_the_element("企业标识")
        mess.is_exist_the_element("企业群名")
        mess.is_exist_the_element("企业成员数量")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0360(self):
        """全局搜索入口——搜索企业群/党群名结果——查看更多列表页"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("测试企业群")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('测试企业群')
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 普通成员在群聊设置页没有拉人“+”和踢人“-”按钮
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0361(self):
        """全局搜索入口——搜索企业群/党群名结果——查看更多列表页"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("ag6421")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('ag6421')
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 群主在群聊设置页有拉人“+”和踢人“-”按钮正常展示
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0364(self):
        """全局搜索入口——搜索企业群/党群名结果——查看更多列表页"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索企业群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("测试企业群")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('测试企业群')
        # 发送消息
        gcp.input_text_message("123456")
        gcp.send_message()
        gcp.click_back()
        gcp.click_back_by_android()
        time.sleep(1)
        # 1、消息列表内有消息记录的 正常进入和消息记录正常展示
        mess.selecting_one_group_click_by_name("测试企业群")
        time.sleep(1)
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, True)
        # 2、消息列表内没有消息记录的 正常进入和消息记录正常展示
        Preconditions.delete_record_group_chat()
        # 回到消息列表页面
        gcp.click_back()
        mess.selecting_one_group_click_by_name("测试企业群")
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, False)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0370(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        # # 搜索企业群
        mess = MessagePage()
        # 进入企业群
        Preconditions.get_into_group_chat_page("测试企业群")
        # 发送消息
        gcp.input_text_message("123456")
        gcp.send_message()
        gcp.click_back()
        time.sleep(1)
        # 1、消息列表内有消息记录的 正常进入和消息记录正常展示
        mess.selecting_one_group_click_by_name("测试企业群")
        time.sleep(1)
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, True)
        # 2、消息列表内没有消息记录的 正常进入和消息记录正常展示
        Preconditions.delete_record_group_chat()
        # 回到消息列表页面
        gcp.click_back()
        mess.selecting_one_group_click_by_name("测试企业群")
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, False)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0372(self):
        """消息列表入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 搜索群
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("ag6421")
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name('ag6421')
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        #返回
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        # 消息列表进入群
        mess.selecting_one_group_click_by_name('ag6421')
        time.sleep(1)
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 群主在群聊设置页有拉人“+”和踢人“-”按钮正常展示
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0375(self):
        """企业群/党群在消息列表内展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # # 搜索企业群
        mess = MessagePage()
        # 进入企业群
        Preconditions.get_into_group_chat_page("测试企业群")
        # 发送消息
        gcp.input_text_message("123456")
        gcp.send_message()
        gcp.click_back()
        time.sleep(1)
        # 1、群头像
        # 2、企群头像右下角“企”标识；党群的群名称后党徽标识
        mess.is_exist_the_element("企业头像")
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0420(self):
        """通讯录——群聊入口——群聊列表入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        time.sleep(1)
        # 打开企业群
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name('ag6421')
        time.sleep(1)
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 群主在群聊设置页有拉人“+”和踢人“-”按钮正常展示
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0423(self):
        """通讯录——群聊入口——群聊列表入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        time.sleep(1)
        # 打开企业群
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 发送消息
        gcp.input_text_message("123456")
        gcp.send_message()
        gcp.click_back()
        gcp.click_back_by_android()
        time.sleep(1)
        # 切换到 消息 tab
        cp = ContactsPage()
        cp.open_message_page()
        # 1、消息列表内有消息记录的 正常进入和消息记录正常展示
        mess.selecting_one_group_click_by_name("测试企业群")
        time.sleep(1)
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, True)
        # 2、消息列表内没有消息记录的 正常进入和消息记录正常展示
        Preconditions.delete_record_group_chat()
        # 回到消息列表页面
        gcp.click_back()
        mess.selecting_one_group_click_by_name("测试企业群")
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, False)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0424(self):
        """通讯录——群聊入口——搜索群组结果入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        time.sleep(1)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("测试企业群")
        time.sleep(1)
        # 判断企业群是否存在
        exist = sog.is_text_present('测试企业群')
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0425(self):
        """通讯录——群聊入口——搜索群组结果入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        time.sleep(1)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("测试企业群")
        time.sleep(1)
        # 打开企业群
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 群主在群聊设置页没有拉人“+”和踢人“-”按钮正常展示
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0426(self):
        """通讯录——群聊入口——搜索群组结果入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        time.sleep(1)
        #搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("ag6421")
        time.sleep(1)
        # 打开企业群
        sog.selecting_one_group_by_name('ag6421')
        time.sleep(1)
        gcp.click_setting()
        time.sleep(1)
        # 判断
        # 群主在群聊设置页有拉人“+”和踢人“-”按钮正常展示
        sc = SelectContactsPage()
        exist = sc.is_exisit_null_contact(None)
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0429(self):
        """通讯录——群聊入口——搜索群组结果入口"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 进入"联系"标签
        mess = MessagePage()
        mess.open_contacts_page()
        contact = ContactsPage()
        contact.click_group_chat_631()
        time.sleep(1)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("测试企业群")
        time.sleep(1)
        # 打开企业群
        sog.selecting_one_group_by_name('测试企业群')
        time.sleep(1)
        # 发送消息
        gcp.input_text_message("123456")
        gcp.send_message()
        gcp.hide_keyboard()
        gcp.click_back()
        gcp.click_back_by_android()
        gcp.click_back_by_android()
        time.sleep(1)
        # 切换到 消息 tab
        cp = ContactsPage()
        cp.open_message_page()
        # 1、消息列表内有消息记录的 正常进入和消息记录正常展示
        mess.selecting_one_group_click_by_name("测试企业群")
        time.sleep(1)
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, True)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, True)
        # 2、消息列表内没有消息记录的 正常进入和消息记录正常展示
        Preconditions.delete_record_group_chat()
        # 回到消息列表页面
        gcp.click_back()
        mess.selecting_one_group_click_by_name("测试企业群")
        exist = gcp.is_text_present("已读动态")
        self.assertEqual(exist, False)
        exist = gcp.is_text_present("123456")
        self.assertEqual(exist, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0430(self):
        """消息列表——发起群聊——选择一个群——模糊搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        exist = gcp.is_text_present("搜索群组")
        self.assertEqual(exist, True)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("测试企业")
        sog.hide_keyboard()
        time.sleep(1)
        # 3、中文模糊搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = gcp.is_text_present("测试企业群")
        self.assertEqual(exist, True)
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0431(self):
        """消息列表——发起群聊——选择一个群——模糊搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 中文模糊搜索企业群和党群，是否可以匹配展示搜索结果
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("企业测试")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、中文模糊搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        exist = gcp.is_text_present("无搜索结果")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0432(self):
        """群聊列表展示页面——中文精确搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        exist = gcp.is_text_present("搜索群组")
        self.assertEqual(exist, True)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("测试企业")
        sog.hide_keyboard()
        time.sleep(1)
        # 3、中文精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = gcp.is_text_present("测试企业群")
        self.assertEqual(exist, True)
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0433(self):
        """群聊列表展示页面——中文精确搜索不存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 中文精确搜索企业群和党群，是否可以匹配展示搜索结果
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("企业测试1")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、中文精确索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        exist = gcp.is_text_present("无搜索结果")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0434(self):
        """群聊列表展示页面——英文精确搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        exist = gcp.is_text_present("搜索群组")
        self.assertEqual(exist, True)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("csqyq")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、英文精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = gcp.is_text_present("测试企业群")
        self.assertEqual(exist, True)
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0435(self):
        """群聊列表展示页面——英文精确搜索不存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 英文精确搜索企业群和党群，是否可以匹配展示搜索结果
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("csqyqa")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、英文精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        exist = gcp.is_text_present("无搜索结果")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0436(self):
        """群聊列表展示页面——空格精确搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        exist = gcp.is_text_present("搜索群组")
        self.assertEqual(exist, True)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword(" ")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、空格精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = gcp.is_text_present("test b")
        self.assertEqual(exist, True)
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0437(self):
        """群聊列表展示页面——空格精确搜索不存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 空格精确搜索企业群和党群，是否可以匹配展示搜索结果
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("   ")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、空格精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        exist = gcp.is_text_present("无搜索结果")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0438(self):
        """群聊列表展示页面——数字精确搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        exist = gcp.is_text_present("搜索群组")
        self.assertEqual(exist, True)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("138138138")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、数字精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = gcp.is_text_present("138138138")
        self.assertEqual(exist, True)
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0439(self):
        """群聊列表展示页面——数字精确搜索不存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 数字精确搜索企业群和党群，是否可以匹配展示搜索结果
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("123456")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、数字精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        exist = gcp.is_text_present("无搜索结果")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0440(self):
        """群聊列表展示页面——字符精确搜索存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        exist = gcp.is_text_present("搜索群组")
        self.assertEqual(exist, True)
        # 搜索企业群
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("testa")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、字符精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        exist = gcp.is_text_present("testa")
        self.assertEqual(exist, True)
        mess.is_exist_the_element("企业标识")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0441(self):
        """群聊列表展示页面——字符精确搜索不存在的企业群和党群"""
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        # 字符精确搜索企业群和党群，是否可以匹配展示搜索结果
        sog = SelectOneGroupPage()
        sog.click_search_group()
        sog.input_search_keyword("testabc")
        sog.hide_keyboard()
        time.sleep(1)
        # 1、字符精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        exist = gcp.is_text_present("无搜索结果")
        self.assertEqual(exist, True)

















