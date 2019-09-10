from appium.webdriver.common.mobileby import MobileBy
import re
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectLocalContactsPage(BasePage):
    """选择联系人->本地联系人 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '无搜索结果': (MobileBy.ID, 'com.chinasofti.rcs:id/no_contact_text'),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/top_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/top_layout'),
                  'com.chinasofti.rcs:id/layout_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_search'),
                  '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  'com.chinasofti.rcs:id/bottom_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/bottom_layout'),
                  'com.chinasofti.rcs:id/contact_selection_list_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_selection_list_view'),
                  '容器列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
                  'com.chinasofti.rcs:id/contact_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
                  '联系人列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
                  'com.chinasofti.rcs:id/asp_selecttion_contact_content': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/asp_selecttion_contact_content'),
                  'D': (MobileBy.ID, ''),
                  'dx1645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '15338821645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'F': (MobileBy.ID, ''),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '18681151872': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'H': (MobileBy.ID, ''),
                  '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '12560': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'X': (MobileBy.ID, ''),
                  'xzq': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '13510772034': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '电话号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  '右侧字母索引': (MobileBy.XPATH,
                             '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
                  '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index"]'),
                  # 删除成员
                  '确定删除': (MobileBy.XPATH, '//*[@text="确定"]'),
                  # 分享群二维码 名片时选择联系人后的弹窗页面
                  '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv'),
                  '确定分享': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '取消分享': (MobileBy.XPATH, '//*[@text="取消"]'),
                  '发送给:xxx': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
                  # 群主转让
                  '确定转让': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '取消转让': (MobileBy.XPATH, '//*[@text="取消"]'),
                  # 选择一个本地联系人转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '取消转发': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '确定转发': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
                  '被选中的联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/avator'),
                  '搜索结果展示': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '已选联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/image_text'),
                  '搜索结果列表': (MobileBy.XPATH, '//android.support.v7.widget.RecyclerView'),
                  '列表项根节点': (MobileBy.XPATH, '//android.support.v7.widget.RecyclerView/*'),
                  '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
                  '查看更多': (MobileBy.XPATH, '//*[@text ="查看更多"]'),
                  '关闭返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
                  }


    @TestLogger.log()
    def click_read_more(self):
        """点击查看更多"""
        self.click_element(self.__class__.__locators["查看更多"])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定转发'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消转发'])

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators['搜索或输入手机号'])

    @TestLogger.log()
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索或输入手机号'], keyword)

    @TestLogger.log("根据导航栏的第一个字母定位")
    def choose_index_bar_click_element(self):
        self.click_element(
            ('xpath','//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[1]'))
        elements = self.get_elements(self.__class__.__locators["联系人名"])
        elements[0].click()

    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        time.sleep(2)
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log()
    def click_sure_share(self):
        """点击确定分享"""
        self.click_element(self.__class__.__locators["确定分享"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_sure_transfer(self):
        """点击确定群主转让"""
        self.click_element(self.__class__.__locators["确定转让"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_cancel_transfer(self):
        """点击取消转让群主"""
        self.click_element(self.__class__.__locators["取消转让"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def get_contacts_name(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        b = set(contacts_name)
        return b

    @TestLogger.log()
    def get_contacts_name2(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        # b = set(contacts_name)
        return contacts_name

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
        time.sleep(1)

    @TestLogger.log()
    def click_sure_del(self):
        """点击确定删除成员"""
        self.click_element(self.__class__.__locators["确定删除"])

    @TestLogger.log()
    def get_phone_numbers(self):
        """获取电话号码"""
        els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'))
        phones = []
        if els:
            for el in els:
                phones.append(el.text)
        return phones

    @TestLogger.log()
    def search(self, text):
        """搜索联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], text)
        try:
            self.driver.hide_keyboard()
        except:
            pass

    @TestLogger.log()
    def select_one_member_by_name(self, name):
        """通过人名选择一个联系人"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % name))

    @TestLogger.log()
    def select_one_contact_by_name(self, name):
        """通过人名选择一个联系人"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % name))

    @TestLogger.log()
    def search_and_select_one_member_by_name(self, name):
        """搜索选择联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], name)
        # self.click_element(self.__class__.__locators["联系人名"])
        self.click_element(self.__class__.__locators["联系人列表"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])
        time.sleep(1)

    @TestLogger.log()
    def sure_btn_is_enabled(self):
        """确定按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["确定"])

    @TestLogger.log()
    def get_sure_btn_text(self):
        """获取确定点击按钮文本"""
        return self.get_element(self.__class__.__locators["确定"]).text

    @TestLogger.log()
    def contacts_is_selected(self, name):
        """获取联系人的选择状态"""
        selected_els = self.get_elements((MobileBy.XPATH,
                                          '//*[@text ="%s"]/../android.widget.ImageView[@resource-id="com.chinasofti.rcs:id/contact_icon"]' % name))
        if selected_els:
            return True
        else:
            return False

    @TestLogger.log()
    def is_exist_select_contacts_name(self):
        """是否存在已选联系人名"""
        return self._is_element_present(self.__class__.__locators["已选联系人名"])

    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    def swipe_to_top(self, times=20):
        """滑动到顶部"""
        while times > 0:
            self.swipe_by_direction(self.__class__.__locators['容器列表'], 'down')
            flag = self.is_text_present("选择团队联系人")
            if flag:
                break
            times = times - 1

    @TestLogger.log()
    def get_all_contacts_name(self):
        """获取所有联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        flag = True
        current = 0
        while flag:
            current += 1
            if current > 20:
                return
            self.page_up()
            els = self.get_elements(self.__class__.__locators["联系人名"])
            for el in els:
                if el.text not in contacts_name:
                    contacts_name.append(el.text)
                    flag = True
                else:
                    flag = False
        return contacts_name

    @TestLogger.log()
    def swipe_select_one_member_by_name(self, name, times=15):
        """通过人名选择一个联系人"""
        time.sleep(2)
        while times > 0:
            els = self.get_elements((MobileBy.XPATH, '//*[@text ="%s"]' % name))
            if els:
                els[0].click()
                break
            self.page_up()
            times = times - 1
        return "no %s" % name

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['选择联系人'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_selected_and_threshold_nums(self):
        """获取确定按钮上的选择人数与可选的总人数"""
        # sure_info = "确定(3/499)"
        sure_info = self.get_element(self.__class__.__locators['确定']).text
        nums = re.findall(r'\d+', sure_info)
        if len(nums) == 2:
            return int(nums[0]), int(nums[1])
        else:
            if not sure_info == '确定':
                raise AssertionError("确定按钮显示异常，不是‘确定’或者 ‘确定(3/499)’格式")

    @TestLogger.log()
    def selecting_local_contacts_by_name(self, name):
        """根据名字选择一个手机联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def selecting_local_contacts_by_number(self, number):
        """根据号码选择一个手机联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_number" and @text="%s"]' % number)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def is_exists_local_contacts_by_name(self, name):
        """是否存在指定手机联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_search_result(self, msg):
        """搜索结果判断"""
        els = self.get_elements((MobileBy.XPATH, '//*[contains(@text, "%s")]' % msg))
        return len(els) > 1

    @TestLogger.log()
    def no_search_result(self):
        """搜索结果判断"""
        els = self.get_elements(self.__class__.__locators["无搜索结果"])
        return len(els) > 0

    @TestLogger.log()
    def select_local_contacts(self, n):
        """选择n个本地联系人"""

        els = self.get_elements(self.__class__.__locators["联系人名"])
        current = 0
        while current < n:
            els[current].click()
            current += 1

    @TestLogger.log()
    def get_contacts_name_list(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        return contacts_name

    @TestLogger.log("点击第一个联系人")
    def click_first_phone_contacts(self):
        self.wait_until(
            condition=lambda x: self.get_elements(self.__locators['电话号码'])[0],
            auto_accept_permission_alert=False
        ).click()

    @TestLogger.log("当前页面是否在选择联系人页")
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['选择联系人'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log("点击搜索第一个联系人")
    def click_search_phone_contacts(self):
        self.wait_until(
            condition=lambda x: self.get_elements(('id', 'com.chinasofti.rcs:id/contact_list_item'))[0],
            auto_accept_permission_alert=False
        ).click()

    @TestLogger.log()
    def is_search_contact_name_full_match(self, name):
        """搜索联系人名是否精准匹配"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
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
    def is_search_contact_number_full_match(self, name):
        """搜索联系人号码是否精准匹配"""
        els = self.get_elements(self.__class__.__locators["电话号码"])
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
    def is_exists_letter_index(self):
        """是否存在字母索引"""
        return self._is_element_present(self.__class__.__locators["右侧字母索引"])

    @TestLogger.log()
    def click_letter_index(self, name):
        """点击字母索引"""
        locator = (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[@text="%s"]' % name)
        self.click_element(locator)

    @TestLogger.log("输入搜索关键字")
    def input_search_key(self, keyword):
        self.input_text(self.__locators['搜索或输入手机号'], keyword)

    @TestLogger.log('选择搜索结果第一项')
    def select_the_first_result(self):
        iterator = self.mobile.list_iterator(self.__locators['搜索结果列表'], self.__locators['列表项根节点'])
        for item in iterator:
            if item.find_elements(*self.__locators['联系人头像']):
                item.click()
                return

    @TestLogger.log('如果键盘弹出，就收回键盘')
    def hide_keyboard_if_display(self):
        if self.mobile.is_keyboard_shown():
            self.hide_keyboard()

    @TestLogger.log("查找并选择联系人")
    def search_and_select_contact(self, *contacts):
        for contact in contacts:
            self.input_search_key(contact)
            self.hide_keyboard_if_display()
            self.select_the_first_result()
        self.click_sure_forward()

    @TestLogger.log("长按搜索或输入手机号")
    def press_search_bar(self):
        el = self.get_element(self.__locators['搜索或输入手机号'])
        self.press(el)

    @TestLogger.log("查找联系人")
    def search_contact(self, *contacts):
        for contact in contacts:
            self.input_search_key(contact)
            self.hide_keyboard_if_display()
            self.select_the_first_result()

    @TestLogger.log()
    def click_cancle(self):
        """点击关闭返回"""
        self.click_element(self.__class__.__locators["关闭返回"])

    @TestLogger.log()
    def press_contact_search_bar(self):
        """长按本地联系人-搜索输入框"""
        el = self.get_element(self.__locators["搜索或输入手机号"])
        self.press(el)