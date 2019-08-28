import time
import unittest
from appium.webdriver.common.mobileby import MobileBy
import preconditions
from dataproviders import contact2
from pages.components import ChatNoticeDialog
from pages.message.FreeMsg import FreeMsgPage
from pages.components import ChatNoticeDialog, SearchBar, ContactsSelector
from pages.components.PickGroup import PickGroupPage
from pages.components.SearchGroup import SearchGroupPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from library.core.BasePage import BasePage



class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_huangmianhua_0191():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0191(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、英文精确搜索，存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行英文精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("groupchat")
        #CheckPoint：英文精确搜索，存在跟搜索条件匹配的群聊
        self.assertTrue(global_search_group_page.is_group_in_list("groupchat"))


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0431(self):
        """聊天会话页面——长按——撤回——发送失败的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，存在发送失败的消息
        # 5、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        current_mobile().set_network_status(1)
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(1)
        # Step 1、长按发送失败的消息
        groupchat.press_voice_message()
        # Checkpoint 2、弹出的功能列表中，不存在撤回功能（发送失败的消息，不允许进行撤回操作）
        mess.page_should_not_contain_text('撤回')

    def tearDown_msg_xiaoqiu_0431(self):
        current_mobile().set_network_status(6)


    @staticmethod
    def setUp_test_msg_huangmianhua_0192():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0192(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、英文精确搜索，不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行英文精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("groupchatabc")
        #CheckPoint：英文精确搜索，不存在跟搜索条件匹配的群聊
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))


    @staticmethod
    def setUp_test_msg_huangmianhua_0193():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0193(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行空格精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("群 ")
        #CheckPoint：空格精确搜索，是否可以匹配展示搜索结果
        self.assertTrue(global_search_group_page.is_group_in_list("群 "))


    @staticmethod
    def setUp_test_msg_huangmianhua_0194():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0194(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行空格精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("群   ")
        #CheckPoint：空格精确搜索，无匹配展示搜索结果
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))


    @staticmethod
    def setUp_test_msg_huangmianhua_0195():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0195(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行数字精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("123")
        #CheckPoint：数字精确搜索，可以匹配展示搜索结果
        time.sleep(5)
        self.assertTrue(global_search_group_page.is_group_in_list("123"))


    @staticmethod
    def setUp_test_msg_huangmianhua_0196():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0196(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行数字精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("123")
        #CheckPoint：数字精确搜索，无匹配搜索结果，展示提示：无搜索结果
        time.sleep(5)
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))


    @staticmethod
    def setUp_test_msg_huangmianhua_0197():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0197(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行数字精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("123")
        #CheckPoint：数字精确搜索，可以匹配展示搜索结果
        time.sleep(5)
        self.assertTrue(global_search_group_page.is_group_in_list("123"))

    @staticmethod
    def setUp_test_msg_huangmianhua_0198():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0198(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行数字精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("123")
        #CheckPoint：数字精确搜索，无匹配搜索结果，展示提示：无搜索结果
        time.sleep(5)
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))

    @staticmethod
    def setUp_test_msg_huangmianhua_0197():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0197(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行字符精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("abc")
        # CheckPoint：字符精确搜索，可以匹配展示搜索结果
        time.sleep(5)
        self.assertTrue(global_search_group_page.is_group_in_list("abc"))

    @staticmethod
    def setUp_test_msg_huangmianhua_0200():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0200(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行字符精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("abcde")
        # CheckPoint：字符精确搜索，无匹配搜索结果，展示提示：无搜索结果
        time.sleep(5)
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0411():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组2', "测试短信1", "测试短信2")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0411(self):
        """长按——识别群二维码——进入群会话窗口和群设置页面"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前消息列表页面
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        contactsel = ContactsSelector()
        sel_con = SelectContactsPage()
        groupchat.wait_for_page_load()
        # Step 进入群聊设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_group_avatars()
        # Step 点击左下角的分享按钮
        groupset.click_qecode_share_button()
        # Checkpoint 跳转到联系人选择器页面
        contactsel.wait_for_contacts_selector_page_load()
        # Step 点击选择一个群
        sel_con.click_select_one_group()
        # Step 搜索选中一个群
        time.sleep(2)
        SearchGroupPage().click_group('测试群组2')
        # Step 点击确定
        SingleChatPage().click_sure()
        # Checkpoint 弹出toast提示：已转发
        mess.is_toast_exist("已转发")
        groupset.click_back()
        groupset.click_back()
        groupchat.click_back()
        SearchPage().click_back_button()
        mess.search_and_enter('测试群组2')
        # Step 1、长按识别群二维码
        sel_con.click_group_code()
        sel_con.click_recognize_code_631()
        # Checkpoint 1、进入会话窗口页面
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        groupset.wait_for_page_load()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0431():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0431(self):
        """聊天会话页面——长按——撤回——发送失败的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，存在发送失败的消息
        # 5、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        current_mobile().set_network_status(1)
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(1)
        # Step 1、长按发送失败的消息
        groupchat.press_voice_message()
        # Checkpoint 2、弹出的功能列表中，不存在撤回功能（发送失败的消息，不允许进行撤回操作）
        mess.page_should_not_contain_text('撤回')

    def tearDown_msg_xiaoqiu_0431(self):
        current_mobile().set_network_status(6)
















