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
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage

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

    # 功能：比较a，b两个字符串是否相同
    # a<=b :true   a>b
    def compare(param1, param2):
        ib = 0
        for ia in range(len(param1)):
            if ord(param1[ia:ia + 1]) - ord(param2[ib:ib + 1]) <= 0:
                ib = ib + 1
                if ib == len(param2):
                    return True
                continue

            else:
                return False


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

        # Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        # fail_time1 = 0
        # flag1 = False
        # import dataproviders
        # while fail_time1 < 3:
        #     try:
        #         required_contacts = dataproviders.get_preset_contacts()
        #         conts = ContactsPage()
        #         current_mobile().hide_keyboard_if_display()
        #         Preconditions.make_already_in_message_page()
        #         conts.open_contacts_page()
        #         try:
        #             if conts.is_text_present("发现SIM卡联系人"):
        #                 conts.click_text("显示")
        #         except:
        #             pass
        #         for name, number in required_contacts:
        #             # 创建联系人
        #             conts.create_contacts_if_not_exits(name, number)
        #         required_group_chats = dataproviders.get_preset_group_chats()
        #         conts.open_group_chat_list()
        #         group_list = GroupListPage()
        #         for group_name, members in required_group_chats:
        #             group_list.wait_for_page_load()
        #             # 创建群
        #             group_list.create_group_chats_if_not_exits(group_name, members)
        #         group_list.click_back()
        #         conts.open_message_page()
        #         flag1 = True
        #     except:
        #         fail_time1 += 1
        #     if flag1:
        #         break
        #
        # # 导入团队联系人
        # fail_time2 = 0
        # flag2 = False
        # while fail_time2 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
        #         Preconditions.create_he_contacts(contact_names)
        #         flag2 = True
        #     except:
        #         fail_time2 += 1
        #     if flag2:
        #         break

        # 确保有企业群
        # fail_time3 = 0
        # flag3 = False
        # while fail_time3 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         Preconditions.ensure_have_enterprise_group()
        #         flag3 = True
        #     except:
        #         fail_time3 += 1
        #     if flag3:
        #         break

        # 确保测试手机有resource文件夹
        # name = "群聊1"
        # Preconditions.get_into_group_chat_page(name)
        # gcp = GroupChatPage()
        # gcp.wait_for_page_load()
        # gcp.click_more()
        # cmp = ChatMorePage()
        # cmp.click_file()
        # csfp = ChatSelectFilePage()
        # csfp.wait_for_page_load()
        # csfp.click_local_file()
        # local_file = ChatSelectLocalFilePage()
        # # 没有预置文件，则上传
        # local_file.push_preset_file()
        # local_file.click_back()
        # csfp.wait_for_page_load()
        # csfp.click_back()
        # gcp.wait_for_page_load()

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
    def test_msg_huangmianhua_0090(self):
        """企业群——群内功能"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        time.sleep(1)
        gcp.click_back()
        result = gcp.is_text_present("消息")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0091(self):
        """企业群——群内功能"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        time.sleep(1)
        # 1、群名称过长时最后两个字前加“...”-暂无名字超长企业群
        # 2、群名称后括号内显示群人数（群成员最多2000人）：1位数成员、2位数成员、3位数成员、4位数成员 --无法判断
        #   不是单独控件
        # 3、党群名称前有“党徽”标识 --群聊界面 没有“党徽”标识
        result = gcp.is_text_present("测试企业群")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0092(self):
        """企业群——群内功能——多方电话、多方视频入口——选择弹窗"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        time.sleep(1)
        # 1、点击右上角“多方电话/多方视频”按钮
        # 2、检查弹窗样式是否正常
        gcp.click_mutilcall()
        time.sleep(1)
        result = gcp.is_text_present("飞信电话(免费)")
        self.assertEqual(result, True)
        result = gcp.is_text_present("多方视频")
        self.assertEqual(result, True)
        # 3、点击弹窗外区域弹窗是否收回
        gcp.click_back()
        time.sleep(1)
        result = gcp.is_text_present("多方视频")
        self.assertEqual(result, False)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0093(self):
        """企业群——群内功能——多方电话、多方视频入口——多方电话"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        time.sleep(1)
        gcp.click_mutilcall()
        time.sleep(1)
        result = gcp.is_text_present("飞信电话(免费)")
        self.assertEqual(result, True)
        gcp.click_hf_tel()
        # 正常弹出联系人选择器
        result = gcp.is_text_present("呼叫")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0094(self):
        """企业群——群内功能——多方电话、多方视频入口——多方电话"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        time.sleep(1)
        gcp.click_mutilcall()
        time.sleep(1)
        result = gcp.is_text_present("飞信电话(免费)")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0097(self):
        """企业群——群内功能——多方电话、多方视频入口——多方视频"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        time.sleep(1)
        gcp.click_mutilcall()
        time.sleep(1)
        result = gcp.is_text_present("多方视频")
        self.assertEqual(result, True)
        gcp.click_multi_videos()
        result = gcp.is_text_present("呼叫")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0098(self):
        """企业群——群内功能——多方电话、多方视频入口——多方视频"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        time.sleep(1)
        gcp.click_mutilcall()
        result = gcp.is_text_present("多方视频")
        self.assertEqual(result, True)
        gcp.click_back()

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
            # Checkpoint 校验群主头像皇冠
            GroupChatSetPage().group_chairman_tag_is_exist()
            time.sleep(1)
            # 回到聊天界面
            gcp.click_back_by_android()
            time.sleep(1)
        # 回到信息列表界面
        gcp.click_back()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0115(self):
        """群主——添加一个成员"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('群聊1')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcp.click_element_("添加群成员加号")
            time.sleep(1)
            # 1、点击添加成员的“+”号按钮，可以跳转到联系人选择器页面
            result = gcp.is_text_present("添加群成员")
            self.assertEqual(result, True)
            # 2、任意选中一个联系人，点击右上角的确定按钮，会向邀请人发送一条消息
            gcp.click_text("给个红包2")
            time.sleep(1)
            gcp.click_text("确定")
            result = gcp.is_text_present("发出群邀请")
            self.assertEqual(result, True)
        else:
            raise AssertionError("不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0116(self):
        """选择已在群聊中的联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('群聊1')
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcp.click_element_("添加群成员加号")
            time.sleep(3)
            # 1、点击添加成员的“+”号按钮，可以跳转到联系人选择器页面
            result = gcp.is_text_present("添加群成员")
            self.assertEqual(result, True)
            # 2、任意选中一个联系人，点击右上角的确定按钮，会向邀请人发送一条消息
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
            sc = SelectContactsPage()
            sc.input_search_keyword(phone_number)
            time.sleep(2)
            sc.hide_keyboard()
            sc.click_text("tel")
            result = gcp.is_toast_exist("该联系人不可选择")
            self.assertEqual(result, True)
        else:
            raise AssertionError("不在群聊页面")

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0120(self):
        """群聊设置页面——查找聊天内容"""
        # 1、点击聊天内容入口，跳转到聊天内容页面
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
        mess.selecting_one_group_click_by_name('测试企业群')
        time.sleep(1)
        result = mess.is_text_present("哈哈")
        self.assertEqual(result, True)
        # 2、点击顶部的搜索框，调起小键盘
        gcp.click_back()
        time.sleep(1)
        mess.click_search()
        time.sleep(1)
        result = mess.is_keyboard_shown()
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0123(self):
        """群聊设置页面——关闭消息免打扰——网络异常"""
        # 1、点击关闭消息免打扰开关，会提示：上传失败
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        time.sleep(1)
        # 消息免打扰按钮(打开)
        gcsp = GroupChatSetPage()
        gcsp.click_switch_undisturb()
        time.sleep(1)
        # 断网
        gcp.set_network_status(0)
        time.sleep(3)
        # 点击 消息免打扰按钮
        gcsp.click_switch_undisturb()
        result = gcp.is_text_present("没有网络，请连接网络再试")
        self.assertEqual(result, True)

    def tearDown_test_msg_huangmianhua_0123(self):
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(3)
        # 消息免打扰按钮(关闭)
        gcsp = GroupChatSetPage()
        gcsp.click_switch_undisturb()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0124(self):
        """群聊设置页面——关闭消息免打扰——网络异常"""
        # 1、点击关闭消息免打扰开关，会提示：上传失败
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        time.sleep(1)
        # 消息免打扰按钮(打开)
        gcsp = GroupChatSetPage()
        gcsp.click_switch_undisturb()
        time.sleep(1)
        # 断网
        gcp.set_network_status(0)
        time.sleep(3)
        # 点击 消息免打扰按钮
        gcsp.click_switch_undisturb()
        result = gcp.is_text_present("没有网络，请连接网络再试")
        self.assertEqual(result, True)

    def tearDown_test_msg_huangmianhua_0124(self):
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(3)
        # 消息免打扰按钮(关闭)
        gcsp = GroupChatSetPage()
        gcsp.click_switch_undisturb()

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0125(self):
        """群聊设置页面——开启消息免打扰——网络断网"""
        # 1、点击开启消息免打扰开关，会弹出toast提示：无网络，请连接网络重试
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        time.sleep(1)
        # 断网
        gcp.set_network_status(0)
        time.sleep(3)
        # 点击 消息免打扰按钮
        gcsp = GroupChatSetPage()
        gcsp.click_switch_undisturb()
        result = gcp.is_text_present("没有网络，请连接网络再试")
        self.assertEqual(result, True)

    def tearDown_test_msg_huangmianhua_0125(self):
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0140(self):
        """在聊天会话页面，长按文本消息——转发——选择一个群作为转发对象"""
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        # 2、选择一个群，进入到群聊列表展示页面，任意选中一个群聊，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        # phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0140")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈0140", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择一个群
        sc.click_text("选择一个群")
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(1)
        # 点击-确定
        sc.click_sure_forward()
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        flag = sc.is_toast_exist("群聊1")
        self.assertTrue(flag)
        flag = sc.is_toast_exist("哈哈0140")
        self.assertTrue(flag)
        mess = MessagePage()
        mess.selecting_one_group_click_by_name("群聊1")
        time.sleep(1)
        flag = sc.is_toast_exist("哈哈0140")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0141(self):
        """在聊天会话页面，长按文本消息——转发——选择和通讯录联系人--团队联系人"""
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        # 2、选择和通讯录人联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        # phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0141")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈0141", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        flag = sc.is_toast_exist("b测算")
        self.assertTrue(flag)
        flag = sc.is_toast_exist("哈哈0141")
        self.assertTrue(flag)
        mess = MessagePage()
        mess.selecting_one_group_click_by_name("b测算")
        time.sleep(1)
        flag = sc.is_toast_exist("哈哈0141")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0142(self):
        """在聊天会话页面，长按文本消息——转发——选择本地联系人"""
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        # 2、选择本地联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        # phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0142")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈0142", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择手机联系人
        sc.click_text("选择手机联系人")
        # 选择“给个红包2”联系人进行转发
        sc.click_one_contact("给个红包2")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        flag = sc.is_toast_exist("给个红包2")
        self.assertTrue(flag)
        flag = sc.is_toast_exist("哈哈0142")
        self.assertTrue(flag)
        mess = MessagePage()
        mess.selecting_one_group_click_by_name("给个红包2")
        time.sleep(1)
        flag = sc.is_toast_exist("哈哈0142")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0143(self):
        """在聊天会话页面，长按文本消息——转发——选择最近聊天"""
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        # 2、选择最近聊天，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        # phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0143")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈0143", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择手机联系人
        # sc.click_text("选择手机联系人")
        # 选择“给个红包2”联系人进行转发
        sc.click_one_contact("给个红包2")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        flag = sc.is_toast_exist("给个红包2")
        self.assertTrue(flag)
        flag = sc.is_toast_exist("哈哈0143")
        self.assertTrue(flag)
        mess = MessagePage()
        mess.selecting_one_group_click_by_name("给个红包2")
        time.sleep(1)
        flag = sc.is_toast_exist("哈哈0143")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0144(self):
        """在聊天会话页面，长按文本消息——收藏"""
        # 1、长按文本消息，选择收藏功能，收藏成功后，弹出toast提示：已收藏
        # 2、在我的页面，点击收藏入口，检查刚收藏的消息内容，可以正常展示出来
        # 3、点击收藏成功的消息体，可以进入到消息展示详情页面
        # 4、左滑收藏消息体，会展示删除按钮
        # 5、点击删除按钮，可以删除收藏的消息体
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0144")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈0144", "收藏")
        flag = gcp.is_toast_exist("已收藏")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection2()
        time.sleep(1)
        if not me.is_text_present("哈哈0144"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("哈哈0144")
        time.sleep(1)
        # 收藏内容展示列表，点击收藏内容，会跳转到收藏内容详情页面
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        # 返回收藏列表
        mcp.click_back_by_android()
        time.sleep(1)
        # 左滑收藏消息体
        mcp.press_and_move_left()
        time.sleep(1)
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

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0145(self):
        """企业群，发送文本消息——已读状态——已读分类展示"""
        # 1、在输入框录入内容，然后点击发送按钮，进行发送，发送成功后的消息体下方会展示：已读动态，4个字的文案
        # 2、点击下方的已读动态，会跳转页面已读动态详情页面
        # 3、在已读动态详情页面，已读分类会展示，已读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0145")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)
        # 点击"已读动态"
        gcp.click_text("已读动态")
        time.sleep(1)
        if not gcp.is_text_present("未读"):
            raise AssertionError("不能进入到已读动态详情页面")
        hr = HasRead()
        hr.wait_for_page_load()
        hr.click_has_not_read()
        # 如果有已读联系人，点击第一个
        hr.click_first_contact()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        if not cdp.is_on_this_page():
            raise RuntimeError('打开联系人详情页面出错')

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0146(self):
        """企业群，发送文本消息——已读状态——未读分类展示"""
        # 1、点击消息体下方的已读动态，跳转页面已读动态详情页面
        # 2、在已读动态详情页面，未读分类会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0146")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)
        # 点击"已读动态"
        gcp.click_text("已读动态")
        time.sleep(1)
        if not gcp.is_text_present("未读"):
            raise AssertionError("不能进入到已读动态详情页面")
        hr = HasRead()
        hr.wait_for_page_load()
        hr.click_has_not_read()
        # 如果有已读联系人，点击第一个
        hr.click_first_contact()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        if not cdp.is_on_this_page():
            raise RuntimeError('打开联系人详情页面出错')

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0147(self):
        """企业群，发送语音消息——已读状态——已读分类"""
        # 1、点击语音按钮，设置模式后，开始录制，输入框中识别出内容后，点击发送按钮，进行发送，发送成功后的消息体下方是否会展示：已读动态，4个字的文案
        # 2、点击下方的已读动态，是否会跳转页面已读动态详情页面
        # 3、在已读动态详情页面，已读分类是否会展示，已读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
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
        # 点击下方的已读动态，会跳转页面已读动态详情页面
        if gcp.is_exist_msg_has_read_icon():
            gcp.click_has_read_icon()
            time.sleep(1)
            exist = gcp.is_text_present("已读动态")
            self.assertEqual(exist, True)
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

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0148(self):
        """企业群，发送语音消息——已读状态——未读分类"""
        # 1、点击消息体下方的已读动态，跳转页面已读动态详情页面
        # 2、在已读动态详情页面，未读分类是否会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
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
        # 点击下方的已读动态，会跳转页面已读动态详情页面
        if gcp.is_exist_msg_has_read_icon():
            gcp.click_has_read_icon()
            time.sleep(1)
            exist = gcp.is_text_present("已读动态")
            self.assertEqual(exist, True)
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

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0149(self):
        """企业群，发送表情消息——已读状态——已读分类"""
        # 1、在输入框右边的表情图标，展示表情列表，任意点击选中几个表情展示到输入框中，然后点击发送按钮，进行发送，发送成功后的消息体下方是否会展示：已读动态，4个字的文案
        # 2、点击下方的已读动态，是否会跳转页面已读动态详情页面
        # 3、在已读动态详情页面，已读分类是否会展示，已读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("[微笑1]")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)
        # 点击"已读动态"
        gcp.click_text("已读动态")
        time.sleep(1)
        if not gcp.is_text_present("未读"):
            raise AssertionError("不能进入到已读动态详情页面")
        hr = HasRead()
        hr.wait_for_page_load()
        hr.click_has_not_read()
        # 如果有已读联系人，点击第一个
        hr.click_first_contact()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        if not cdp.is_on_this_page():
            raise RuntimeError('打开联系人详情页面出错')

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0150(self):
        """企业群，发送表情消息——已读状态——未读分类"""
        # 1、点击消息体下方的已读动态，跳转页面已读动态详情页面
        # 2、在已读动态详情页面，未读分类是否会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("[微笑1]")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)
        # 点击"已读动态"
        gcp.click_text("已读动态")
        time.sleep(1)
        if not gcp.is_text_present("未读"):
            raise AssertionError("不能进入到已读动态详情页面")
        hr = HasRead()
        hr.wait_for_page_load()
        hr.click_has_not_read()
        # 如果有已读联系人，点击第一个
        hr.click_first_contact()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        if not cdp.is_on_this_page():
            raise RuntimeError('打开联系人详情页面出错')

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0158(self):
        """群聊天会话页面——输入框输入@字符——@联系人"""
        # 1、在群聊天会话窗口
        # 2、在输入框中，输入@字符，是否会调起联系人选择器页面
        # 3、选择一个联系人后，是否会自动返回到聊天会话页面并且在输入框中展示选中联系人的信息
        # 4、点击右边的发送按钮，发送出去后，被@的联系人是否会在消息列表收到@提示 ？双机
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 输入消息
        gcp.input_text_message("@")
        result = gcp.is_text_present("选择群成员")
        self.assertEqual(result, True)
        gcp.click_text("大佬1")
        time.sleep(1)
        result = gcp.is_text_present("测试企业群")
        self.assertEqual(result, True)
        result = gcp.is_text_present("@大佬1")
        self.assertEqual(result, True)
        # 发送消息
        gcp.send_message()
        gcp.click_back_by_android()
        time.sleep(1)
        result = gcp.is_text_present("@大佬1")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0162(self):
        """普通群聊天会话页面——自己@自己"""
        # 1、在输入框输入@符号，跳转到的联系人选择页面，用户本身不会展示出来
        # 2、在聊天会话页面长按自己，不可以发起@操作
        gcp = GroupChatPage()
        # gcp.click_back()
        # Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 输入消息
        gcp.input_text_message("@")
        time.sleep(1)
        result = gcp.is_text_present("选择群成员")
        self.assertEqual(result, True)
        # 列表不包含自己
        scp = SelectContactsPage()
        result = scp.is_exsit_group_member()
        self.assertEqual(result, True)
        gcp.click_back_by_android()
        time.sleep(1)
        # 发送消息
        gcp.input_text_message("0162")
        gcp.send_message()
        time.sleep(2)
        # 长按头像
        gsm = GlobalSearchMessagePage()
        gsm.press_head_icon()
        time.sleep(3)
        result = gcp.is_text_present("@")
        self.assertEqual(result, False)


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
    def test_msg_huangmianhua_0265(self):
        """已读动态——“已读动态”标识"""
        # 1、全部消息皆正常
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0265")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0266(self):
        """已读动态——“已读动态”标识——已读/未读成员列表"""
        # 1、正常进入
        # 2、人数正常
        # 3、成员数据展示正常
        # 4、正常进入
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0266")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)
        # 点击"已读动态"
        gcp.click_text("已读动态")
        time.sleep(1)
        if not gcp.is_text_present("未读"):
            raise AssertionError("不能进入到已读动态详情页面")
        if not gcp.is_text_present("(0)"):
            raise AssertionError("人数错误")
        if not gcp.is_text_present("(2)"):
            raise AssertionError("人数错误")
        hr = HasRead()
        hr.wait_for_page_load()
        hr.click_has_not_read()
        result = gcp.is_toast_exist("大佬1")
        self.assertTrue(result)
        # 如果有已读联系人，点击第一个
        hr.click_first_contact()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        if not cdp.is_on_this_page():
            raise RuntimeError('打开联系人详情页面出错')

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0268(self):
        """已读动态——“已读动态”标识——已读/未读成员列表——进入个人profile页"""
        # 1.未在个人本地通讯录成员profile页：保存到通讯录
        # 2.已在个人本地通讯录成员profile页:全部正常显示且功能正常
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈0268")
        gcp.send_message()
        time.sleep(1)
        flag = gcp.is_toast_exist("已读动态")
        self.assertTrue(flag)
        # 点击"已读动态"
        gcp.click_text("已读动态")
        time.sleep(1)
        hr = HasRead()
        hr.wait_for_page_load()
        # 点击 "未读"tab
        hr.click_has_not_read()
        # 如果有已读联系人，点击第一个
        hr.click_first_contact()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        if not cdp.is_on_this_page():
            raise RuntimeError('打开联系人详情页面出错')
        if gcp.is_toast_exist("保存到通讯录"):
            gcp.click_text("保存到通讯录")
        else:
            flag = gcp.is_toast_exist("邀请使用")
            self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0279(self):
        """企业群底部全部按钮"""
        # 输入框 # 表情# 语音plus# 相册 #相机# 名片# GIF
        # 全部正常展示
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        gc = GroupChatPage()
        # 输入框
        flag = gcp.is_exist_btn('输入框')
        self.assertTrue(flag)
        # 表情
        flag = gc.is_exist_btn('表情按钮')
        self.assertTrue(flag)
        # 语音plus
        flag = gc.is_exist_btn('语音按钮')
        self.assertTrue(flag)
        # 相册
        flag = gc.is_exist_btn('选择照片')
        self.assertTrue(flag)
        # 相机
        flag = gc.is_exist_btn('富媒体拍照')
        self.assertTrue(flag)
        # 名片
        gc.click_more()
        time.sleep(1)
        flag = gc.is_text_present('名片')
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0280(self):
        """企业群底部全部按钮——更多“+”"""
        # 全部正常展示
        gcp = GroupChatPage()
        gcp.click_back()
        Preconditions.get_into_group_chat_page('测试企业群')
        gc = GroupChatPage()
        # 更多
        gc.click_more()
        time.sleep(1)
        result = gc.is_text_present('飞信电话')
        self.assertTrue(result)
        result = gc.is_text_present('多方视频')
        self.assertTrue(result)
        # 文件
        result = gc.is_exist_btn('文件')
        self.assertTrue(result)
        result = gc.is_text_present('群短信')
        self.assertTrue(result)
        result = gc.is_text_present('位置')
        self.assertTrue(result)
        result = gc.is_text_present('红包')
        self.assertTrue(result)
        # 关闭更多
        gc.click_more()
        time.sleep(1)
        result = gc.is_text_present('群短信')
        self.assertFalse(result)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0286(self):
        """转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0287(self):
        """转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0288(self):
        """转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0289(self):
        """转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0290(self):
        """企业群/党群--查找聊天内容--转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 设置界面查找聊天内容
        gcp.click_setting()
        time.sleep(1)
        gcsp = GroupChatSetPage()
        gcsp.click_find_chat_record()
        # 点击搜索框
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        search.click_edit_query()
        search.input_search_message("哈哈")
        time.sleep(1)
        search.click_record()
        time.sleep(1)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0291(self):
        """企业群/党群--查找聊天内容--转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 设置界面查找聊天内容
        gcp.click_setting()
        time.sleep(1)
        gcsp = GroupChatSetPage()
        gcsp.click_find_chat_record()
        # 点击搜索框
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        search.click_edit_query()
        search.input_search_message("哈哈")
        time.sleep(1)
        search.click_record()
        time.sleep(1)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0292(self):
        """企业群/党群--查找聊天内容--转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 设置界面查找聊天内容
        gcp.click_setting()
        time.sleep(1)
        gcsp = GroupChatSetPage()
        gcsp.click_find_chat_record()
        # 点击搜索框
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        search.click_edit_query()
        search.input_search_message("哈哈")
        time.sleep(1)
        search.click_record()
        time.sleep(1)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0293(self):
        """企业群/党群--查找聊天内容--转发聊天窗口中的可以转发的消息体，选择和通讯录联系人"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 设置界面查找聊天内容
        gcp.click_setting()
        time.sleep(1)
        gcsp = GroupChatSetPage()
        gcsp.click_find_chat_record()
        # 点击搜索框
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        search.click_edit_query()
        search.input_search_message("哈哈")
        time.sleep(1)
        search.click_record()
        time.sleep(1)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0303(self):
        """群聊设置--群成员预览内非RCS用户头像置灰"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 设置界面
        gcp.click_setting()
        time.sleep(1)
        gcp.click_text("大佬1")
        time.sleep(1)
        # 1、非RCS用户头像应置灰
        # 2、能正常进入其profile页
        result = gcp.is_text_present("邀请使用")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0304(self):
        """群聊设置--群成员预览内非RCS用户头像置灰"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        # 设置界面
        gcp.click_setting()
        time.sleep(1)
        gcs = GroupChatSetPage()
        gcs.click_group_member_show()
        time.sleep(1)
        # 1、非RCS用户头像应置灰不再显示“未开通”且后方还有“邀请”按钮
        # 2、能正常进入其profile页
        result = gcp.is_text_present("邀请")
        self.assertEqual(result, True)
        gcp.click_text("大佬1")
        time.sleep(1)
        result = gcp.is_text_present("邀请使用")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0304(self):
        """群聊设置--群成员预览内非RCS用户头像置灰"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        Preconditions.get_into_group_chat_page('测试企业群')
        # Preconditions.delete_record_group_chat()
        # 设置界面
        gcp.click_setting()
        time.sleep(1)
        gcs = GroupChatSetPage()
        gcs.click_group_member_show()
        time.sleep(2)
        # 1、搜索结果内非RCS用户头像应置灰不再显示“未开通”且后方还有“邀请”按钮
        result = gcp.is_text_present("邀请")
        self.assertEqual(result, True)
        # 2、能正常进入其profile页
        gcp.click_element_("搜索成员输入框")
        gcp.input_member_message("大佬")
        gcp.hide_keyboard()
        time.sleep(3)
        gcp.click_text("大佬1")
        time.sleep(3)
        result = gcp.is_text_present("邀请使用")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0344(self):
        """其他创建群入口"""
        # 正常创建
        gcp = GroupChatPage()
        gcp.click_back()
        mess = MessagePage()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        sog = SelectOneGroupPage()
        sog.select_contact_by_name("大佬2")
        time.sleep(1)
        sog.select_contact_by_name("大佬3")
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name("群聊测试1")
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(3)
        result = mess.is_text_present("群聊测试1")
        self.assertEqual(result, True)


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
    def test_msg_hanjiabin_0070(self):
        """普通企业群/长ID企业群：进入审批应用后右上角“？”内部页面样式、文案及交互是否正常（本网号为例）"""
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
        # 1、正常进入审批应用问题解答页面且内部样式文案等与工作台内审批应用一致
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        # 点击 审批
        gcp.click_text("审批")
        time.sleep(10)
        # 点击 问号 ？
        vnp = VoiceNoticePage()
        vnp.click_enter_more()
        time.sleep(3)
        # 2、全部二级页面样式、文案及相关操作正常，关闭页面后应直接返回到群聊页面
        exist = gcp.is_text_present("审批PC版已上线")
        self.assertEqual(exist, True)
        vnp.click_close_more()
        exist = gcp.is_text_present("测试企业群")
        self.assertEqual(exist, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_hanjiabin_0074(self):
        """普通企业群/长ID企业群：发起任意审批类型时页面样式检查"""
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
        exist = gcp.is_text_present("审批")
        self.assertEqual(exist, True)
        # 点击 审批
        gcp.click_text("审批")
        time.sleep(10)
        gcp.click_text("请假")
        time.sleep(3)
        # 1、检查页面样式均正常，“使用上次审批人、使用上次抄送人”按钮被隐藏，页面下方“分享至当前群”栏目后方按钮默认关闭
        exist = gcp.is_text_present("使用上次审批人")
        self.assertEqual(exist, False)
        exist = gcp.is_text_present("使用上次抄送人")
        self.assertEqual(exist, False)
        gcsp = GroupChatSetPage()
        result = gcsp.find_element_share2group_text()
        result = 'false' == result
        print("result = " + str(result))
        self.assertEqual(result, True)





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
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        mess.input_search_message_631(group_name)
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name(group_name)
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
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        mess.input_search_message_631(group_name)
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name(group_name)
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
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        mess.input_search_message_631(group_name)
        mess.hide_keyboard()
        time.sleep(1)
        mess.selecting_one_group_scroll_by_name(group_name)
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        #返回
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        # 消息列表进入群
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        mess.selecting_one_group_click_by_name(group_name)
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
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        sog.selecting_one_group_by_name(group_name)
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
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        sog.input_search_keyword(group_name)
        time.sleep(1)
        # 打开企业群
        sog.selecting_one_group_by_name(group_name)
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

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0110(self):
        """群成员展示列表页，搜索出的搜索结果排序"""
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
            gcp.input_member_message("a")
            time.sleep(1)
            group_member = GroupChatSetSeeMembersPage()
            names = group_member.get_all_group_member_names()
            if len(names) == 0 or len(names) == 1:
                result = False
                self.assertEqual(result, False)
            else:
                print(str(names[0]))
                print(str(names[1]))
                result = Preconditions.compare(names[0], names[1])
                self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0215(self):
        """转发——聊天窗口中的可消息体——选择和通讯录联系人——企业展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page(group_name)
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0216(self):
        """转发——聊天窗口中的消息体——选择和通讯录联系人——企业展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page(group_name)
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0217(self):
        """转发——聊天窗口中的消息体——选择和通讯录联系人——企业展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page(group_name)
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'group_chat')
    def test_msg_huangmianhua_0218(self):
        """转发——聊天窗口中的消息体——选择和通讯录联系人——企业展示"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开企业群
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        Preconditions.get_into_group_chat_page(group_name)
        Preconditions.delete_record_group_chat()
        # 发送消息
        gcp.input_text_message("哈哈")
        gcp.send_message()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择团队联系人
        sc.click_text("选择团队联系人")
        # 选择bm0子一层级？？？？
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name2('bm0')
        # 选择“b测算”联系人进行转发
        sc.click_one_contact("b测算")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("b测算"))

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_150(self):
        """银行预留信息页仅填写手机号"""
        # 1.输入15-19位有效的银行卡号
        # 2.点击下一步
        # 3.只填写持卡人手机号
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.手机号显示正常&下一步按钮置灰不可点
        # me.input_text_card_person_name("张三123")
        # me.input_text_card_id("421127198412125637")
        me.input_text_phoneno("15013708130")
        if me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 可点击")

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_151(self):
        """银行预留信息页填写持卡人姓名与手机号&输入小于15位的身份证号"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.填写信息显示正常，下一步按钮置灰不可点
        me.input_text_card_person_name("姚磊")
        me.input_text_card_id("421127198412121")
        me.input_text_phoneno("15013708130")
        if me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 可点击")

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_152(self):
        """银行预留信息页填写持卡人姓名与手机号&输入大于15位&小于18位的身份证号"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.填写信息显示正常，下一步按钮置灰不可点
        me.input_text_card_person_name("姚磊")
        # 输入大于15位&小于18位的身份证号
        me.input_text_card_id("4211271984121211")
        me.input_text_phoneno("15013708130")
        if me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 可点击")

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_154(self):
        """银行预留信息页填写持卡人姓名&身份证号&手机号，未勾选协议"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.填写完持卡有效信息后，未勾选协议
        me.input_text_card_person_name("姚磊")
        me.input_text_card_id("421127198412125637")
        me.input_text_phoneno("15013708130")
        if not me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 不可点击")

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_157(self):
        """银行预留页面填写错误（无效）的持卡人姓名&正确的身份证号&正确的手机号"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.输入信息显示正确，下一步按钮高亮可点
        me.input_text_card_person_name("张三123")
        me.input_text_card_id("421127198412125637")
        me.input_text_phoneno("15013708130")
        if not me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 不可点击")
        else:
            gcp.click_text("下一步")
            time.sleep(3)
        # 4.弹窗提示您输入的姓名有误 （您输入的信息有误，请核对后重试）
        result = gcp.is_text_present("确认")
        self.assertEqual(result, True)
        gcp.click_text("确认")
        # 5.弹窗消失并停留在当前页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_158(self):
        """银行预留页面填写错误的持卡人姓名&正确的身份证号&正确的手机号-非银行预留持卡人姓名"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.输入信息显示正确，下一步按钮高亮可点
        me.input_text_card_person_name("张三")
        me.input_text_card_id("421127198412125637")
        me.input_text_phoneno("15013708130")
        if not me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 不可点击")
        else:
            gcp.click_text("下一步")
            time.sleep(3)
        # 4.弹窗提示您输入的姓名有误 （您输入的信息有误，请核对后重试）
        result = gcp.is_text_present("确认")
        self.assertEqual(result, True)
        gcp.click_text("确认")
        # 5.弹窗消失并停留在当前页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_159(self):
        """银行预留页面填写正确的姓名&无效的身份证号&正确的手机号-身份证尾数是除X外的英文字母"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.输入信息显示正确，下一步按钮高亮可点
        me.input_text_card_person_name("姚磊")
        # 错误的身份证号码（末尾是除了X外的英文字母）
        me.input_text_card_id("42112719851211111A")
        me.input_text_phoneno("15013708130")
        if not me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 不可点击")
        else:
            gcp.click_text("下一步")
            time.sleep(3)
        # 4.弹窗提示您输入的姓名有误 （您输入的信息有误，请核对后重试）
        result = gcp.is_text_present("确认")
        self.assertEqual(result, True)
        gcp.click_text("确认")
        # 5.弹窗消失并停留在当前页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_160(self):
        """银行预留页面填写正确的姓名&无效的身份证号&正确的手机号-错误的15或18位身份证号"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.输入信息显示正确，下一步按钮高亮可点
        me.input_text_card_person_name("姚磊")
        # 错误的身份证号码（错误的18位或15位数字）
        me.input_text_card_id("421127198512111119")
        me.input_text_phoneno("15013708130")
        if not me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 不可点击")
        else:
            gcp.click_text("下一步")
            time.sleep(3)
        # 4.弹窗提示您输入的姓名有误 （您输入的信息有误，请核对后重试）
        result = gcp.is_text_present("确认")
        self.assertEqual(result, True)
        gcp.click_text("确认")
        # 5.弹窗消失并停留在当前页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_161(self):
        """银行预留页面填写正确的姓名&无效的身份证号&正确的手机号-非银行预留身份证号"""
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("银行卡")
        time.sleep(5)
        if not gcp.is_text_present("绑定新的银行卡"):
            raise AssertionError("没有出现 - 绑定新的银行卡")
        gcp.click_text("绑定新的银行卡")
        time.sleep(3)
        me.input_text_cardno("6228480128139652175")
        # 1.下一步按钮高亮可点
        if me.is_enabled_next_btn():
            gcp.click_text("下一步")
        else:
            raise AssertionError("下一步1 - 不可点击")
        time.sleep(5)
        # 2.跳转到银行预留信息页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)
        # 3.输入信息显示正确，下一步按钮高亮可点
        me.input_text_card_person_name("姚磊")
        # 错误的身份证号码（15位或18位非银行预留身份证号）
        me.input_text_card_id("421127198512111")
        me.input_text_phoneno("15013708130")
        if not me.is_enabled_next_btn2():
            raise AssertionError("下一步2 - 不可点击")
        else:
            gcp.click_text("下一步")
            time.sleep(3)
        # 4.弹窗提示您输入的姓名有误 （您输入的信息有误，请核对后重试）
        result = gcp.is_text_present("确认")
        self.assertEqual(result, True)
        gcp.click_text("确认")
        # 5.弹窗消失并停留在当前页面
        result = gcp.is_text_present("填写银行预留信息")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_089(self):
        """已授权，清除客户端缓存，再授权"""
        # 1、清除缓存成功
        # 2、功能正常使用，无需授权再次授权
        gcp = GroupChatPage()
        gcp.click_back()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_hebao_pay()
        time.sleep(1)
        me.click_hebao_pay_card("现金红包")
        time.sleep(3)
        if not gcp.is_text_present("已收红包"):
            raise AssertionError("没有出现 - 已收红包")
        if not gcp.is_text_present("已发红包"):
            raise AssertionError("没有出现 - 已发红包")

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_093(self):
        """ 发二人红包-未授权 """
        gcp = GroupChatPage()
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        # Step 1、在消息列表页点击全局搜索框，进行"大佬3"
        mess.search_and_enter2('大佬3')
        time.sleep(1)
        gcp.click_text("消息")
        time.sleep(1)
        if gcp.is_text_present("我已阅读"):
            gcp.click_back_by_android()
        groupchat = GroupChatPage()
        # 点击输入框上方的+号
        groupchat.click_more()
        time.sleep(1)
        # 1、A打开B的二人对话窗口，点击红包
        # 2、场景一：点击暂不授权
        # 场景二：点击确认授权
        result = gcp.is_text_present("红包")
        self.assertEqual(result, True)
        groupchat.click_text("红包")
        result = gcp.is_text_present("发红包")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me')
    def test_me_zhangshuli_324(self):
        """ 发二人红包-绑定新银行卡支付 """
        gcp = GroupChatPage()
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        # Step 1、在消息列表页点击全局搜索框，进行"大佬3"
        mess.search_and_enter2('大佬3')
        time.sleep(1)
        gcp.click_text("消息")
        time.sleep(1)
        if gcp.is_text_present("我已阅读"):
            gcp.click_back_by_android()
        groupchat = GroupChatPage()
        # 点击输入框上方的+号
        groupchat.click_more()
        time.sleep(1)
        # 1、A成功打开B的二人会话窗口
        result = gcp.is_text_present("红包")
        self.assertEqual(result, True)
        groupchat.click_text("红包")
        # 2、进入发红包页面，发红包按钮置灰不可点击
        result = gcp.is_text_present("发红包")
        self.assertEqual(result, True)
        me = MePage()
        result = me.is_enabled_red_packet_send()
        self.assertEqual(result, False)
        time.sleep(3)
        # 4、进入绑定银行卡页面
        # 输入金额 点击发红包
        me.input_text_red_packet_num("1")
        time.sleep(1)
        # "发红包"
        me.click_red_packet_send()
        time.sleep(10)
        result = gcp.is_text_present("绑定新的银行卡")
        self.assertEqual(result, True)


















