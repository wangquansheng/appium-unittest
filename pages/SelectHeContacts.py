from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectHeContactsPage(BasePage):
    """选择和通讯录页面"""
    """选择和通讯录联系人页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseContactSelectActivity'

    __locators = {
                  '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_action_bar_title'),
                  'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity'),
                  '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity'),
                  'com.chinasofti.rcs:id/lv_data_enterprise_fragment': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/lv_data_enterprise_fragment'),
                  'com.chinasofti.rcs:id/img_icon_department': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_department'),
                  'myteam': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  'com.chinasofti.rcs:id/img_right_department': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_right_department'),
                  'Superman': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  'myteam02': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  '团队名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
                  '清空搜索框': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),

                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待选择团队页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['团队名称'])
            )
        except:
            message = "页面在{}s内，没有加载成功，或者在和通讯录没有团队".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("点击搜索第一个联系人")
    def click_search_phone_contacts(self):
        self.wait_until(
            condition=lambda x: self.get_elements(self.__class__.__locators["联系人名"])[0],
            auto_accept_permission_alert=False
        ).click()

    @TestLogger.log()
    def input_search_contact_message(self, message):
        """输入查询联系人查询信息"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def get_team_names(self):
        """获取团队名字"""
        els = self.get_elements(self.__class__.__locators['团队名称'])
        team_names = []
        if els:
            for el in els:
                team_names.append(el.text)
        return team_names

    @TestLogger.log("获取所有团队名称")
    def get_all_group_name(self):
        """获取所有团队名"""
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["团队名称"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(self.__class__.__locators["团队名称"])
        group_name = []
        if els:
            for el in els:
                group_name.append(el.text)
        else:
            raise AssertionError("No m005_group, please add m005_group in address book.")
        return group_name


    @TestLogger.log()
    def select_one_team_by_name(self, name):
        """选择一个团队"""
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % name))

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def get_element_text(self,locator='选择联系人'):
        """获取元素文本"""
        return self.get_text(self.__class__.__locators[locator])

    @TestLogger.log()
    def click_input_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators['搜索或输入手机号'])

    @TestLogger.log()
    def input_search_keywords(self,text):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators['搜索或输入手机号'],text)

    @TestLogger.log()
    def clear_input_box(self):
        """清空搜索框"""
        self.click_element(self.__class__.__locators['清空搜索框'])

    @TestLogger.log()
    def is_element_present(self,locator='清空搜索框'):
        """判断元素是否存在"""
        return self._is_element_present(self.__class__.__locators[locator])
