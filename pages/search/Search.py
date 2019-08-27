import re
from xml.sax import saxutils

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components import SearchBar
from pages.components.keyboard import Keyboard


class SearchPage(SearchBar, Keyboard, BasePage):
    """快速搜索"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.SearchActivity'

    __locators = {
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'),
        '输入关键词快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        '搜索结果列表': (MobileBy.ID, 'com.chinasofti.rcs:id/single_result_list'),
        '删除搜索框文本按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect01'),
        '搜索和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/content'),
        '搜索团队联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '联系人分割线': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '联系人项列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/root_view'),
        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
        '联系人名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone'),

        '公众号分割线': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '公众号列表项': (MobileBy.XPATH, '//android.widget.RelativeLayout[*[@resource-id="com.chinasofti.rcs:id/svd_head"]]'),
        '公众号头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '公众号名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '群聊名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息页面联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '群聊历史记录数量': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
        '团队联系人文本': (
            MobileBy.XPATH, "//android.widget.TextView[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='团队联系人']"),
    }

    @TestLogger.log("点击返回")
    def click_back_button(self):
        """点击返回"""
        self.click_element(self.__locators['返回上一页'])

    @TestLogger.log("搜索和通讯录联系人")
    def click_search_contacts(self):
        """搜索和通讯录联系人"""
        self.click_element(self.__locators['搜索和通讯录联系人'])

    @TestLogger.log('检查搜索和通讯录联系人入口是否出现')
    def assert_hetongxunlu_entry_is_display(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['搜索和通讯录联系人'])

    @TestLogger.log('检查搜索团队联系人入口是否出现')
    def assert_group_entry_is_display(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['搜索团队联系人'])

    @TestLogger.log('检查搜索到的联系人名字')
    def assert_contact_name_display(self, name, timeout=0):
        """检查搜索到的联系人名字"""
        locator = [MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="{}"]'.format(
            saxutils.escape(name, {"'": "&apos;", '"': "&quot;"}))]
        try:
            self.wait_until(
                condition=lambda d: self.get_elements(locator),
                timeout=timeout
            )
        except:
            raise AssertionError("找不到名字等于：{}的联系人".format(name))

    @TestLogger.log('检查搜索到的号码')
    def assert_contact_number_display(self, number, timeout=0):
        """检查搜索到的号码"""
        locator = [MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_phone" and @text="{}"]'.format(
            saxutils.escape(number, {"'": "&apos;", '"': "&quot;"}))]
        try:
            self.wait_until(
                condition=lambda d: self.get_elements(locator),
                timeout=timeout
            )
        except:
            raise AssertionError("找不到号码等于：{}的联系人".format(number))

    @TestLogger.log("点击名字为XXX的联系人")
    def click_contact_whose_name_is(self, name):
        """
        点击名字为XXX的联系人
        :param name: 联系人名字
        :return: 联系人名字、号码信息
        """
        locator = \
            [MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/root_view" '
             + 'and *//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="{}"]]'.format(
                 saxutils.escape(name, {"'": "&apos;", '"': "&quot;"}))]
        contact_info = self.get_contact_info(locator)
        self.click_element(locator)
        return contact_info

    @TestLogger.log("点击名字为XXX的联系人")
    def click_contact_whose_number_is(self, number):
        """
        点击名字为XXX的联系人
        :param number: 联系人号码
        :return: 联系人名字、号码信息
        """
        locator = \
            [MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/root_view" '
             + 'and *//*[@resource-id="com.chinasofti.rcs:id/tv_phone" and @text="{}"]]'.format(
                 saxutils.escape(number, {"'": "&apos;", '"': "&quot;"}))]
        contact_info = self.get_contact_info(locator)
        self.click_element(locator)
        return contact_info

    @TestLogger.log("获取联系人信息")
    def get_contact_info(self, locator):
        """
        获取联系人名称、号码信息
        :param locator: 联系人父容器的定位器
        :return:
        """
        contact = self.get_element(locator)
        name = contact.find_element(*self.__locators['联系人名字'])
        number = contact.find_element(*self.__locators['联系人号码'])
        return dict(
            name=name.text,
            number=number.text
        )

    @TestLogger.log("滚动到下一页")
    def page_down(self):
        """滚动到下一页"""
        self.swipe_by_direction(self.__locators['搜索结果列表'], 'up')

    @TestLogger.log("滚动到上一页")
    def page_up(self):
        """滚动到上一页"""
        self.swipe_by_direction(
            self.__locators['搜索结果列表'],
            'down'
        )

    @TestLogger.log("判断是否滚动到底部")
    def is_now_on_last_page(self):
        """
        判断是否滚动到底部
        :return:
        """
        container = self.get_element(self.__locators['搜索结果列表'])
        last_item = self.get_elements(
            [MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/single_result_list"]/*[last()]']
        )
        if len(last_item) == 0:
            return True

        # 容器底部底部y轴坐标
        container_bottom = container.location.get('y') + container.size.get('height')

        # 最后一项底部y轴坐标
        item_bottom = last_item[0].location.get('y') + last_item[0].size.get('height')

        # 检查列表是否有内容
        content = self.get_elements(
            [MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/single_result_list"]'
             + '/*[@resource-id="com.chinasofti.rcs:id/root_view"'
             + ' or *[@resource-id="com.chinasofti.rcs:id/svd_head"]]']
        )
        if len(content) == 0:
            return True
        if container_bottom - item_bottom > 0:
            return True
        else:
            return False

    @TestLogger.log('迭代搜索结果')
    def iterate_list(self):
        """
        迭代消息列表,默认从上往下
        :return:
        """
        item_locator = [MobileBy.XPATH, '//*[../../*[@resource-id="com.chinasofti.rcs:id/single_result_list"]]']
        items = self.get_elements(item_locator)
        if not items:
            return
        while True:
            last_one = items[-1]
            pre = last_one.location
            for i in items:
                yield i
                items = self.get_elements(item_locator)
            self.page_down()
            post = last_one.location
            # 如果元素消失或者坐标发生变化，表示翻页后列表有新数据
            post_y, pre_y = post.get('y'), pre.get('y')
            if ec.staleness_of(last_one)(True) or post_y < pre_y:
                new_items = self.get_elements(item_locator)
                stale_items = []

                for item in items:
                    if items.index(item) + 1 >= len(items):
                        break
                    if item.location == items[items.index(item) + 1].location:
                        stale_items.append(item)
                    else:
                        break
                old_items = items[len(stale_items):]
                items = new_items[len(old_items):]
                if not items:
                    return
                continue
            return

    @TestLogger.log('判断列表项类型')
    def determine_list_item_type(self, item):
        is_list_item = 0  # 搜索结果
        tips = 1  # 提示语"搜索和通讯录联系人..."
        split_lines = item.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint"]')
        search_tips = item.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/content"]')

        if not split_lines and not search_tips:
            return is_list_item
        if split_lines:
            return split_lines[0].text
        if search_tips:
            return tips

    @TestLogger.log('搜索结果是否精准匹配关键字')
    def assert_search_result_full_match_keyword(self, item, keyword):
        """
        :param item: 搜索结果列表中的一项，必须是列表项的跟节点元素
        :param keyword: 搜索关键字
        :return:
        """
        texts = []
        sub_items = item.find_elements('xpath', '//*')
        for si in sub_items:
            text = si.text.lower()
            if text:
                texts.append(text)
        for t in texts:
            if keyword.lower() == t:
                return
        raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的文本'.format(texts, keyword))

    @TestLogger.log('搜索结果是否匹配关键字')
    def assert_search_result_match_keyword(self, item, pattern, regex=False):
        """
        :param item: 搜索结果列表中的一项，必须是列表项的跟节点元素
        :param pattern: 匹配模式
        :param regex: 是否使用正则匹配
        :return:
        """
        texts = []
        sub_items = item.find_elements('xpath', '//*')
        for si in sub_items:
            text = si.text.lower()
            if text:
                texts.append(text)
        for t in texts:
            if regex:
                if re.search(pattern, t):
                    return
            else:
                if pattern.lower() in t:
                    return
        raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的文本'.format(texts, pattern))

    @TestLogger.log('迭代搜索列表')
    def search_list_iterator(self):
        """
        迭代消息列表,默认从上往下
        :return:
        """
        scroll_view_locator = self.__locators['搜索结果列表']
        item_locator = [MobileBy.XPATH, '//*[../../*[@resource-id="com.chinasofti.rcs:id/single_result_list"]]']
        yield from self.mobile.list_iterator(scroll_view_locator, item_locator)

    @TestLogger.log('获取联系人名')
    def get_contact_name(self, contact):
        assert isinstance(contact, (list, tuple, WebElement))
        if isinstance(contact, (list, tuple)):
            item = self.get_element(contact)
        else:
            item = contact
        contact_name = item.find_element(*[MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" or ' +
                                           '@resource-id="com.chinasofti.rcs:id/tv_conv_name"]']).text
        return contact_name

    @TestLogger.log('获取联系人数量')
    def get_contact_count(self):
        els = self.get_elements(self.__locators['联系人名字'])
        return len(els)

    @TestLogger.log('获取群聊数量')
    def get_group_count(self):
        els = self.get_elements(self.__locators['群聊名字'])
        return len(els)

    @TestLogger.log('获取群聊数量')
    def get_meslist_contacts(self):
        results = []
        els = self.get_elements(self.__locators['消息页面联系人'])
        if els:
            for el in els:
                results.append(el.text)
        return results

    @TestLogger.log('')
    def is_contains_element(self, results, compare):
        if results:
            for result in results:
                result == compare
                return True
        else:
            return False

    @TestLogger.log('获取联系人列表名字')
    def is_exist__contact_name(self, name):
        els = self.get_elements(self.__locators['联系人名字'])
        if els:
            for el in els:
                if name == el.text:
                    return True
                else:
                    continue
        return False

    @TestLogger.log('获取群聊历史记录数量')
    def get_chat_history_count(self):
        els = self.get_elements(self.__locators['群聊历史记录数量'])
        return len(els)

    @TestLogger.log('检查分栏是否显示"查看更多"')
    def assert_show_more_is_display(self, element):
        assert isinstance(element, (list, tuple, WebElement))
        if isinstance(element, (list, tuple)):
            item = self.get_element(element)
        else:
            item = element
        try:
            self.wait_until(
                condition=lambda d: item.find_element(MobileBy.XPATH, '//*[@text="查看更多"]')
            )
        except TimeoutException:
            raise AssertionError('界面没有显示"查看更多"入口')

    @TestLogger.log('检查分栏是否显示"查看更多"')
    def click_show_more(self, element):
        assert isinstance(element, (list, tuple, WebElement))
        if isinstance(element, (list, tuple)):
            item = self.get_element(element)
        else:
            item = element
        entry = item.find_element(MobileBy.XPATH, '//*[@text="查看更多"]')
        entry.click()

    @TestLogger.log('检查分栏是否显示"查看更多"')
    def click_element_c(self, locator):
       self.click_element(self.__locators[locator])
