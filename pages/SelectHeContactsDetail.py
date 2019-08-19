import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from library.core.utils.applicationcache import current_mobile


class SelectHeContactsDetailPage(BasePage):
    """选择和通讯录联系人页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseContactSelectInnerActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
                  'com.chinasofti.rcs:id/btn_close_actionbar': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_action_bar_title'),
                  'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity'),
                  '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/breadCrumbs_enterprise_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/breadCrumbs_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/breadcrumbs_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/breadcrumbs_layout'),
                  '和通讯录': (MobileBy.ID, 'android:id/title'),
                  'android:id/icon': (MobileBy.ID, 'android:id/icon'),
                  'myteam': (MobileBy.ID, 'android:id/title'),
                  'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity'),
                  'android:id/list': (MobileBy.ID, 'android:id/list'),
                  'com.chinasofti.rcs:id/layout_personal_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_personal_contactlist'),
                  'com.chinasofti.rcs:id/img_icon_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_contactlist'),
                  'com.chinasofti.rcs:id/line_search_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/line_search_contactlist'),
                  'axzq': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '13510772034': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_position_personal_contactlist'),
                  '测试号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '14775290489': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_position_personal_contactlist'),
                  '张三': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '联系电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_number_personal_contactlist'),
                  'com.chinasofti.rcs:id/line_big_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/line_big_contactlist'),
                  'com.chinasofti.rcs:id/layout_department_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_department_contactlist'),
                  'com.chinasofti.rcs:id/img_icon_department': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_department'),
                  '测试一部': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  '部门名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  'com.chinasofti.rcs:id/img_right_department': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/img_right_department'),
                  'com.chinasofti.rcs:id/line_contactlist1': (MobileBy.ID, 'com.chinasofti.rcs:id/line_contactlist1'),
                  # 选择一个和通讯录联系人转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '取消': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '确定': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
                  '企业层级': (MobileBy.ID, "android:id/title"),
                  '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv'),
                  "快捷方式": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_shortcut'),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """默认使用activity作为判断页面是否加载的条件，继承类应该重写该方法"""
        try:
            self.wait_until(
                lambda d: self.is_text_present('编辑'),
                timeout,
                auto_accept_alerts
            )
            return self
        except:
            return self.is_text_present('编辑')

    @TestLogger.log("")
    def page_not_contain_shortcut(self):
        """当前页面是否存在快捷方式"""
        return self.page_should_not_contain_element(self.__locators['快捷方式'])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        time.sleep(2)
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log()
    def select_one_linkman(self, name):
        """选择一个联系人"""
        name = 'b测算'
        locator = (MobileBy.XPATH, "//*[@text='%s']" % name)
        self.find_element_by_swipe(locator)
        self.click_element(locator)

    @TestLogger.log()
    def select_one_department(self, name):
        """选择一个部门"""
        self.click_element((MobileBy.XPATH, "//*[@text='%s']" % name))

    @TestLogger.log()
    def get_contacts_names(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators['联系人名'])
        contacts_names = []
        if els:
            for el in els:
                contacts_names.append(el.text)
        return contacts_names

    @TestLogger.log()
    def is_enabled_search_result(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators['联系人名'])
        if els:
            for el in els:
                if not self._is_enabled(el):
                    return False
        return True

    @TestLogger.log()
    def get_contacts_numbers(self):
        """获取联系人电话"""
        els = self.get_elements(self.__class__.__locators['联系电话'])
        contacts_numbers = []
        if els:
            for el in els:
                contacts_numbers.append(el.text)
        return contacts_numbers

    @TestLogger.log()
    def get_department_names(self):
        """获取部门名称"""
        els = self.get_elements(self.__class__.__locators['部门名称'])
        department_names = []
        if els:
            for el in els:
                department_names.append(el.text)
        return department_names

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def input_search(self, text):
        """输入名字"""
        self.input_text(self.__locators["搜索"], text)
        time.sleep(2.5)
        current_mobile().hide_keyboard_if_display()

    @TestLogger.log()
    def is_exists_search_box(self):
        """是否存在搜索输入框"""
        return self._is_element_present(self.__class__.__locators['搜索'])

    @TestLogger.log()
    def select_one_he_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name_personal_contactlist" and contains(@text,"%s")]' % name))

    @TestLogger.log()
    def select_one_he_contact_by_number(self, number):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_number_personal_contactlist" and contains(@text,"%s")]' % number))

    @TestLogger.log()
    def selecting_he_contacts_by_name(self, name):
        """根据名字选择一个团队联系人"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/tv_name_personal_contactlist" and contains(@text,"%s")]' % name)
        time.sleep(2)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def selecting_he_contacts_by_number(self, number):
        """根据号码选择一个团队联系人"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/tv_number_personal_contactlist" and contains(@text,"%s")]' % number)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def wait_for_he_contacts_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择联系人->和通讯录联系人 页面加载"""
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
    def click_department_name(self, name):
        """点击指定企业/部门名称"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title" and @text="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def is_exist_corporate_grade(self):
        """是否存在企业层级"""
        return self._is_element_present(self.__class__.__locators['企业层级'])

    @TestLogger.log("点击搜索第一个联系人")
    def click_search_team_contacts(self):
        self.wait_until(
            condition=lambda x: self.get_elements(self.__locators['联系人名'])[0],
            auto_accept_permission_alert=False
        ).click()

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在团队联系人"""
        el = self.get_elements(self.__locators['搜索'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索：当前组织框"""
        self.click_element(self.__class__.__locators['搜索'])

    @TestLogger.log("长按搜索：当前组织框")
    def press_search_bar(self):
        el = self.get_element(self.__locators['搜索'])
        self.press(el)
