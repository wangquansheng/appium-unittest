from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class GlobalSearchMessagePage(Keyboard, BasePage):
    """聊天记录搜索"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GlobalSearchMessageActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '输入关键字搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
        '清空关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '数据类型名称': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '列表': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/result_list"]/*'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '对话名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('长按头像')
    def press_head_icon(self):
        el = self.get_element(self.__locators['头像'])
        self.press(el)

    @TestLogger.log('输入搜索关键字')
    def search(self, keyword):
        self.input_text(self.__locators['输入关键字搜索'], keyword)

    @TestLogger.log('清空搜索关键字')
    def clear_search_keyword(self):
        self.click_element(self.__locators['清空关键字'])

    @TestLogger.log('检查列表是否包含XX聊天记录')
    def assert_list_contains_message(self, content):
        messages = self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项'])
        find_out = False
        for message in messages:
            message_content = message.find_element(*self.__locators['消息内容']).text
            if content == message_content:
                find_out = True
                break
        if not find_out:
            raise AssertionError('列表没有找到内容等于"{}"的聊天记录'.format(content))
