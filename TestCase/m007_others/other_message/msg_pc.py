import os
import random
import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
# from pages.message.MessageSetting import MessageSettingPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from settings import PROJECT_PATH
from pages.components.selectors import PictureSelector

class Preconditions(WorkbenchPreconditions):
    """前置条件"""
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
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            return
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
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0232():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0232(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '2018-11-09 11-06-18-722582.log'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        # 点击文件右上方的 ... 图标
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/forward"  and @text="转发"]'))
        # 点击联系人名称
        chatWindowPage.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @index="0"]'))
        chatWindowPage.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        chatWindowPage.is_toast_exist("已转发")

import os
import random
import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

import preconditions
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


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0232():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0232(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '2018-11-09 11-06-18-722582.log'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        # 点击文件右上方的 ... 图标
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/forward"  and @text="转发"]'))
        # 点击联系人名称
        chatWindowPage.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @index="0"]'))
        chatWindowPage.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        chatWindowPage.is_toast_exist("已转发")


    @staticmethod
    def setUp_test_msg_weifenglian_PC_0264():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0264(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '2018-11-09 11-06-18-722582.log'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # chatWindowPage.click_element((MobileBy.XPATH,
        #                               '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        # 点击文件右上方的 ... 图标
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/forward"  and @text="转发"]'))
        # 点击联系人名称
        chatWindowPage.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @index="0"]'))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        chatWindowPage.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0265():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0265(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '2018-11-09 11-06-18-722582.log'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        # 点击文件右上方的 ... 图标
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@class="android.widget.TextView"  and @text="收藏"]'))
        chatWindowPage.is_toast_exist("已收藏")

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0266():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0266(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '2018-11-09 11-06-18-722582.log'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        # 点击文件右上方的 ... 图标
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@class="android.widget.TextView"  and @text="其他应用打开"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="android:id/icon"  and @index="0"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0268():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0268(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '测试文件.rar'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        elements = chatWindowPage.get_elements((MobileBy.XPATH, '//*[@resource-id="android:id/icon"]'))
        self.assertTrue(len(elements) == 0)

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0272():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0272(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '测试文件.rar'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # while len(elements) == 0:
        #     chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
        #     time.sleep(1)
        #     elements = chatWindowPage.get_elements(
        #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        elements = chatWindowPage.get_elements((MobileBy.XPATH, '//*[@resource-id="android:id/icon"]'))
        self.assertTrue(len(elements) == 0)


    @staticmethod
    def setUp_test_msg_weifenglian_PC_0310():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    # def test_msg_weifenglian_PC_0310(self):
    #     """会话窗口中点击删除文本消息"""
    #     # 推送文件到指定目录
    #     path = 'aaaresource'
    #     # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
    #     #                                              os.path.join(PROJECT_PATH, path))
    #
    #     # 转发文件的名称
    #     file_name = '2018-11-09 11-06-18-722582.log'
    #     chatWindowPage = ChatWindowPage()
    #     # 选择文件图标
    #     chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
    #
    #     chatWindowPage.click_element(
    #         (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
    #     time.sleep(2)
    #     # 文件系统找文件目录
    #     elements = chatWindowPage.get_elements(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     while len(elements) == 0:
    #         chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
    #         time.sleep(1)
    #         elements = chatWindowPage.get_elements(
    #             (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     # 文件系统找文件
    #     time.sleep(2)
    #     elements = chatWindowPage.get_elements(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     while len(elements) == 0:
    #         chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
    #         time.sleep(1)
    #         elements = chatWindowPage.get_elements(
    #             (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     # 发送
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
    #     time.sleep(1)
    #     chat_Window_Page = ChatWindowPage()
    #     chat_Window_Page.click_setting()
    #     msg_setting_Page = MessageSettingPage()
    #     msg_setting_Page.enter_serarch_chat_recor()
    #     msg_setting_Page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/layout_file_search'))
    #     time.sleep(2)
    #     file_elements = msg_setting_Page.get_elements(
    #         (MobileBy.XPATH,
    #          '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
    #     file_elements[0].click()
    #     tile_text = msg_setting_Page.get_text((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title"]'))
    #     self.assertTrue(tile_text == file_name)
    #

    # @staticmethod
    # def setUp_test_msg_weifenglian_PC_0314():
    #     # 启动App
    #     Preconditions.select_mobile('Android-移动')
    #     # 启动后不论当前在哪个页面，强制进入消息页面
    #     Preconditions.force_enter_message_page('Android-移动')
    #     # 进入我的电脑页面
    #     message_page = MessagePage()
    #     message_page.wait_for_page_load()
    #     message_page.search_and_enter("我的电脑")

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    # def test_msg_weifenglian_PC_0314(self):
    #     """会话窗口中点击删除文本消息"""
    #     # 推送文件到指定目录
    #     path = 'aaaresource'
    #     # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
    #     #                                              os.path.join(PROJECT_PATH, path))
    #
    #     # 转发文件的名称
    #     file_name = '2018-11-09 11-06-18-722582.log'
    #     chatWindowPage = ChatWindowPage()
    #     # 选择文件图标
    #     chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
    #
    #     chatWindowPage.click_element(
    #         (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
    #     time.sleep(2)
    #     # 文件系统找文件目录
    #     elements = chatWindowPage.get_elements(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     while len(elements) == 0:
    #         chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
    #         time.sleep(1)
    #         elements = chatWindowPage.get_elements(
    #             (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     # 文件系统找文件
    #     time.sleep(2)
    #     elements = chatWindowPage.get_elements(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     while len(elements) == 0:
    #         chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
    #         time.sleep(1)
    #         elements = chatWindowPage.get_elements(
    #             (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     # 发送
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
    #     time.sleep(1)
    #
    #     chat_Window_Page = ChatWindowPage()
    #     chat_Window_Page.click_setting()
    #     msg_setting_Page = MessageSettingPage()
    #     msg_setting_Page.enter_serarch_chat_recor()
    #     msg_setting_Page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/layout_file_search'))
    #     time.sleep(2)
    #     file_elements = msg_setting_Page.get_elements(
    #         (MobileBy.XPATH,
    #          '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
    #     file_elements[0].click()
    #     tile_text = msg_setting_Page.get_text((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title"]'))
    #     self.assertTrue(tile_text == file_name)
    #     # 点击文件右上方的 ... 图标
    #     msg_setting_Page.click_element(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
    #     msg_setting_Page.click_element(
    #         (MobileBy.XPATH, '//*[@class="android.widget.TextView"  and @text="收藏"]'))
    #     msg_setting_Page.is_toast_exist("已收藏")


    # @staticmethod
    # def setUp_test_msg_weifenglian_PC_0315():
    #     # 启动App
    #     Preconditions.select_mobile('Android-移动')
    #     # 启动后不论当前在哪个页面，强制进入消息页面
    #     Preconditions.force_enter_message_page('Android-移动')
    #     # 进入我的电脑页面
    #     message_page = MessagePage()
    #     message_page.wait_for_page_load()
    #     message_page.search_and_enter("我的电脑")

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    # def test_msg_weifenglian_PC_0315(self):
    #     """会话窗口中点击删除文本消息"""
    #     # 推送文件到指定目录
    #     path = 'aaaresource'
    #     # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
    #     #                                              os.path.join(PROJECT_PATH, path))
    #
    #     # 转发文件的名称
    #     file_name = '2018-11-09 11-06-18-722582.log'
    #     chatWindowPage = ChatWindowPage()
    #     # 选择文件图标
    #     chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
    #
    #     chatWindowPage.click_element(
    #         (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
    #     time.sleep(2)
    #     # 文件系统找文件目录
    #     elements = chatWindowPage.get_elements(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     while len(elements) == 0:
    #         chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
    #         time.sleep(1)
    #         elements = chatWindowPage.get_elements(
    #             (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
    #     # 文件系统找文件
    #     time.sleep(2)
    #     elements = chatWindowPage.get_elements(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     while len(elements) == 0:
    #         chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
    #         time.sleep(1)
    #         elements = chatWindowPage.get_elements(
    #             (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
    #     # 发送
    #     chatWindowPage.click_element((MobileBy.XPATH,
    #                                   '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
    #     time.sleep(1)
    #     # chatWindowPage.set_network_status(0)
    #     chat_Window_Page = ChatWindowPage()
    #     chat_Window_Page.click_setting()
    #     msg_setting_Page = MessageSettingPage()
    #     msg_setting_Page.enter_serarch_chat_recor()
    #     msg_setting_Page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/layout_file_search'))
    #     time.sleep(2)
    #     file_elements = msg_setting_Page.get_elements(
    #         (MobileBy.XPATH,
    #          '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
    #     file_elements[0].click()
    #     tile_text = msg_setting_Page.get_text((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title"]'))
    #     self.assertTrue(tile_text == file_name)
    #     # 点击文件右上方的 ... 图标
    #     msg_setting_Page.click_element(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
    #     msg_setting_Page.click_element(
    #         (MobileBy.XPATH, '//*[@class="android.widget.TextView"  and @text="其他应用打开"]'))
    #     msg_setting_Page.click_element(
    #         (MobileBy.XPATH, '//*[@resource-id="android:id/icon"  and @index="0"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0312():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 进入群聊
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_have_my_group()
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.select_one_group_by_name(Preconditions.get_group_chat_name())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0312(self):
        """群聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        if len(elements) > 0:
            chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="android:id/button1"]'))
        chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn"]'))

    @staticmethod
    def setUp_test_msg_xiaoliping_B_0009():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_private_chat_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_B_0009(self):
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_setting()
        # 开启消息免打扰
        status_text = chatWindowPage.get_text((MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"))
        if (status_text == "关闭"):
            chatWindowPage.click_element((MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"))
        # 获取消息免打扰 开关状态
        status_text = chatWindowPage.get_text((MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"))
        self.assertTrue(status_text == '开启')
        chatWindowPage.click_element((MobileBy.ID, "com.chinasofti.rcs:id/back"))
        time.sleep(3)
        slient_elements = chatWindowPage.get_elements((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_slient"]'))
        self.assertTrue(len(slient_elements) > 0)

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0158():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试图片1, 14775200001", "测试图片2, 14775200002"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0158(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 点击照片
        groupchat.click_picture()
        ps = PictureSelector()
        # 选择大于20m的图片
        time.sleep(1)
        ps.switch_to_given_folder("pic1")
        # 点击原图
        ps.click_original_photo()
        ps.select_items_by_given_orders(1)
        # 发送图片
        ps.click_send_of_img_selector()
        time.sleep(1)
        # 判断存在发送失败按钮
        self.assertFalse(groupchat.is_send_sucess())
        # 长按图片
        groupchat.press_picture()
        # 判断是否存在编辑界面
        self.assertTrue(groupchat.is_exist_edit_page())
        # 点击编辑
        groupchat.click_edit()

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0159():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试图片1, 14775200001", "测试图片2, 14775200002"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0159(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 点击照片
        groupchat.click_picture()
        ps = PictureSelector()
        # 选择大于20m的图片
        time.sleep(1)
        ps.switch_to_given_folder("pic1")
        ps.select_items_by_given_orders(1)
        # 点击预览
        ps.click_preview()
        time.sleep(1)
        cppp = ChatPicPreviewPage()
        # 点击原图
        cppp.click_original_photo()
        # 点击发送
        cppp.click_send()
        # 判断存在发送失败按钮
        self.assertFalse(groupchat.is_send_sucess())
        # 长按图片
        groupchat.press_picture()
        # 判断是否存在编辑界面
        self.assertTrue(groupchat.is_exist_edit_page())
        # 点击编辑
        groupchat.click_edit()

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0160():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        Preconditions.create_contacts_if_not_exist_631(["测试图片1, 14775200001", "测试图片2, 14775200002"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0160(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
        # 长按发送失败的图片
        groupchat.press_picture()
        # 点击收藏
        groupchat.click_collection()
        self.assertTrue(groupchat.is_exist_collection())

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0161():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        Preconditions.create_contacts_if_not_exist_631(["测试图片1, 14775200001", "测试图片2, 14775200002"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0161(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
        # 长按发送失败的图片
        groupchat.press_picture()
        # 点击多选
        groupchat.click_selection_forward()
        scp = SelectContactsPage()
        scp.search("测试图片1")
        time.sleep(1)
        scp.select_one_contact_by_name("测试图片1")
        # 点击确定转发
        scp.click_sure_forward()
        self.assertTrue(groupchat.is_toast_exist("已转发"))


    @staticmethod
    def setUp_test_msg_xiaoliping_D_0162():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        Preconditions.create_contacts_if_not_exist_631(["测试图片1, 14775200001", "测试图片2, 14775200002"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0162(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
        # 长按发送失败的图片
        groupchat.press_picture()
        # 点击多选
        groupchat.click_muti_select()
        # 点击转发
        groupchat.click_multiple_selection_forward()
        scp = SelectContactsPage()
        scp.search("测试图片1")
        time.sleep(1)
        scp.select_one_contact_by_name("测试图片1")
        # 点击确定转发
        scp.click_sure_forward()
        self.assertTrue(groupchat.is_toast_exist("已转发"))

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0164():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0164(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
        # 点击红色感叹号
        groupchat.click_send_failed()
        # 判断是否存在暂不支持发送大于20M的图片
        self.assertTrue(groupchat.is_toast_exist("暂不支持发送大于20M的图片"))

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0165():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0165(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
        # 点击图片
        groupchat.click_picture_msg()
        self.assertTrue(groupchat.is_toast_exist("暂不支持发送大于20M的图片"))
        # 点击缩略图
        groupchat.close_pic_preview()
        time.sleep(2)
        self.assertTrue(groupchat.is_on_this_page_631())

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0167():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0167(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
        # 点击图片
        groupchat.click_picture_msg()
        self.assertTrue(groupchat.is_toast_exist("暂不支持发送大于20M的图片"))

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0168():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0168(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
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

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0169():
        # 推送pic并启动App
        pic_dir = os.path.join(PROJECT_PATH, 'bbbresource', "pic")
        Preconditions.select_mobile('Android-移动').push_folder(pic_dir, '/sdcard')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试图片1, 14775200001", "测试图片2, 14775200002"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_D_0169(self):
        """1、网络正常 2、当前在群聊（普通群和企业群）会话窗口页面"""
        Preconditions.create_group_if_not_exist_631('测试图片组1', "测试图片1", "测试图片2")
        groupchat = GroupChatPage()
        # 判断网络是否正常
        network_status = groupchat.get_network_status()
        self.assertTrue(network_status in [2, 4, 6])
        # 进入群聊
        groupchat.wait_for_page_load()
        # 判断存在红色感叹号
        self.assertFalse(groupchat.is_send_sucess())
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


