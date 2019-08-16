from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class SelectOneGroupPage(BasePage):
    """选择一个群页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '选择一个群': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  '搜索群组': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/recyclerView_contactList': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_contactList'),
                  '群列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
                  '列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
                  'Q': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/contact_image': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_image'),
                  '群聊002': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '群聊001': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '群聊名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  'A': (MobileBy.ID, ''),
                  'B': (MobileBy.ID, ''),
                  'C': (MobileBy.ID, ''),
                  '右侧字母索引': (MobileBy.XPATH,
                             '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
                  '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index"]'),
                  # 选择一个群转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '取消': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '确定': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
                  '分享名片': (MobileBy.ID,'com.chinasofti.rcs:id/send_tv'),
                  '群-搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
                  '搜索-返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  '搜索结果展示': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '黏贴': (MobileBy.XPATH, "//*[contains(@text, '黏贴')]"),
                  }

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def get_group_name(self):
        """获取群名"""
        els = self.get_elements(self.__class__.__locators["群聊名"])
        group_names = []
        if els:
            for el in els:
                group_names.append(el.text)
        return group_names

    @TestLogger.log()
    def select_one_group_by_name(self, name):
        """通过群名选择一个群"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[contains(@text, "%s")]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)


    @TestLogger.log()
    def click_search_group(self):
        """点击搜索群组"""
        self.click_element(self.__class__.__locators['搜索群组'])

    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        time.sleep(2)
        self.click_element(self.__locators['分享名片'])
        time.sleep(1)
        els=self.get_elements(self.__locators['分享名片'])
        if els:
            print("控件点击失败")
            self.tap_coordinate([(700,1900)])

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """
        点击返回，通过android返回键
        """
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log('点击联系人')
    def click_contact(self, name):
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and ' +
                            '@text="{}"]'.format(name)))

    @TestLogger.log()
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['群-搜索'], keyword)

    @TestLogger.log()
    def is_exists_group_search_box(self):
        """是否存在群搜索输入框"""
        return self._is_element_present(self.__class__.__locators['群-搜索'])

    @TestLogger.log()
    def click_back_icon(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators['搜索-返回'])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择一个群页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择一个群"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在选择一个群"""
        el = self.get_elements(self.__locators['选择一个群'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('搜索群')
    def search_group(self, group_name):
        self.input_text(self.__locators['搜索群组'], group_name)

    @TestLogger.log('判断列表中是否包含XX群')
    def is_group_in_list(self, name):
        iterator = self.mobile.list_iterator(self.__locators['群列表'], self.__locators['列表项'])
        for group in iterator:
            if group.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                            '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('toast信息存在判断')
    def catch_message_in_page(self, text):
        return self.is_toast_exist(text)

    @TestLogger.log('点击搜索结果')
    def click_search_result(self):
        self.click_element(self.__class__.__locators['搜索结果展示'])

    @TestLogger.log('点击选择一个群')
    def click_select_ong_group(self):
        self.click_element(self.__class__.__locators['选择一个群'])

    @TestLogger.log()
    def selecting_one_group_by_name(self, name):
        """根据群名选择一个群"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            time.sleep(1)
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log("选择联系人-选择团队")
    def selecting_one_group_by_name2(self, name):
        """根据群名选择一个群"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def select_contact_by_name(self, name):
        """根据联系人名称 -- 选择 联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def select_one_enterprise_group(self):
        """选择一个企业群 返回群名"""
        locator = (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/group_ep"]/../android.widget.LinearLayout/android.widget.TextView[@resource-id="com.chinasofti.rcs:id/contact_name"]')
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(locator)
        name = els[0].text
        els[0].click()
        return name

    @TestLogger.log()
    def get_search_result_group(self):
        """获取搜索结果群"""
        els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'))
        if els:
            return els
        else:
            raise AssertionError("没有搜索结果")

    @TestLogger.log("根据导航栏的第一个字母定位")
    def choose_index_bar_click_element(self, index=0):
        self.click_element(
            ('xpath','//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[1]'))
        elements = self.get_elements(self.__class__.__locators["群聊名"])
        elements[index].click()

    @TestLogger.log()
    def page_contain_element_result(self):
        """页面应该展示搜索结果"""
        self.page_should_contain_element(self.__class__.__locators['搜索结果展示'])

    @TestLogger.log('搜索结果是否存在')
    def is_element_present_result(self):
        return self._is_element_present(self.__locators['搜索结果展示'])

    @TestLogger.log()
    def is_search_group_name_full_match(self, name):
        """搜索群名是否精准匹配"""
        els = self.get_elements(self.__class__.__locators["群聊名"])
        texts = []
        for el in els:
            text = el.text.strip()
            if text:
                texts.append(text)
        for t in texts:
            if name == t:
                return True
        raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的文本'.format(texts, name))

    @TestLogger.log()
    def is_exists_group_by_name(self, name):
        """是否存在指定群聊"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and text="%s"]' % name)
        self.find_element_by_swipe(locator)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_element_exit(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_letter_index(self, name):
        """点击字母索引"""
        locator = (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[@text="%s"]' % name)
        self.click_element(locator)

    @TestLogger.log()
    def press_group_search_bar(self):
        """长按群-搜索输入框"""
        el = self.get_element(self.__locators["群-搜索"])
        self.press(el)