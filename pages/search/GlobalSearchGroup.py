from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class GlobalSearchGroupPage(Keyboard, BasePage):
    """查看更多群组"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.search.GlobalSearchGroupActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '输入关键字搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
        '输入关键字快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        '清空关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '数据类型名称': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '列表': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/result_list"]/*'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '联系人名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        '成员数量': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_member_count'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('输入搜索关键字')
    def search(self, keyword):
        self.input_text(self.__locators['输入关键字搜索'], keyword)

    @TestLogger.log('输入关键字快速搜索')
    def search2(self, keyword):
        self.input_text(self.__locators['输入关键字快速搜索'], keyword)

    @TestLogger.log('清空搜索关键字')
    def clear_search_keyword(self):
        self.click_element(self.__locators['清空关键字'])

    @TestLogger.log('检查列表是否包含XX群组')
    def assert_list_contains_group(self, name):
        groups = self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项'])
        find_out = False
        for group in groups:
            group_name = group.find_element(*self.__locators['群名']).text
            if name == group_name:
                find_out = True
                break
        if not find_out:
            raise AssertionError('列表没有找到名字等于"{}"的群组'.format(name))

    @TestLogger.log('检查列表是否包含XX群组')
    def assert_list_contains_group(self, name):
        groups = self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项'])
        find_out = False
        for group in groups:
            group_name = group.find_element(*self.__locators['群名']).text
            if name == group_name:
                find_out = True
                break
        if not find_out:
            raise AssertionError('列表没有找到名字等于"{}"的群组'.format(name))
