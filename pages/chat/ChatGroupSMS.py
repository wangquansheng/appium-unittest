from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupSMSPage(BasePage):
    """群短信编辑页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSMSEditActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '群短信': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/context_fragment': (MobileBy.ID, 'com.chinasofti.rcs:id/context_fragment'),
                  '接收人：': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_sendee'),
                  'com.chinasofti.rcs:id/select_sendee': (MobileBy.ID, 'com.chinasofti.rcs:id/select_sendee'),
                  'com.chinasofti.rcs:id/layout_for_sms': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_sms'),
                  'com.chinasofti.rcs:id/sms_direction': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'),
                  '您正在使用群短信功能': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_isFree'),
                  'com.chinasofti.rcs:id/layout_sms_pannel': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_sms_pannel'),
                  '发送短信...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_edit'),
                  'com.chinasofti.rcs:id/tv_send': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '收件人': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_sendee'),
                  '群成员列表': (MobileBy.ID, 'com.chinasofti.rcs:id/select_sendee'),
                  '搜索成员': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  '选择群成员_确定': (MobileBy.ID, 'com.chinasofti.rcs:id/sure_text'),
                  '全选': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_check_all'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send'),
                  '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '键盘': (MobileBy.ID, 'com.chinasofti.rcs:id/conversation_bottom_showCustomMenuView'),
                  '记录': (MobileBy.ID, 'com.chinasofti.rcs:id/context_view'),
                  '+': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_normal_edit'),
                  '欢迎使用群短信': (MobileBy.XPATH, '//android.widget.FrameLayout[count(*)=0]'),
                  '选择群成员列表第一个': (MobileBy.XPATH, '//*[contains(@resource-id,"com.chinasofti.rcs:id/root_view")][1]'),
                  '选择群成员列表第二个': (MobileBy.XPATH, '//*[contains(@resource-id,"com.chinasofti.rcs:id/root_view")][2]'),
                  '已选择人数和可选择的最高上限人数': (MobileBy.XPATH, "//*[contains(@text, '确定(1/500)')]"),
                  '可重新选择联系人': (MobileBy.XPATH, "//*[contains(@text, '确定(2/500)')]"),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待群短信页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("收件人")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def input_text_message(self, message):
        """输入文本信息"""
        self.input_text(self.__class__.__locators["发送短信..."], message)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        return self

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_send_message(self):
        """点击发送短信..."""
        self.click_element(self.__class__.__locators["发送短信..."])

    @TestLogger.log()
    def is_exist_mass_record(self):
        """判断是否存在记录"""
        el = self.get_elements(self.__class__.__locators["记录"])
        if len(el) > 0:
            return True
        else:
            return False

    def is_on_message_edit_this_page(self):
        """当前页面是否在群发短信编辑页面"""
        el = self.get_elements(self.__locators['发送短信...'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_add(self):
        """点击'+'进入群发短信编辑页面"""
        self.click_element(self.__class__.__locators["+"])

    def is_on_message_record_this_page(self):
        """当前页面是否在群发短信记录页面"""
        el = self.get_elements(self.__locators['+'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('使用坐标点击群短信-确定')
    def click_coordinate(self, x=0.74, y=0.78):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        print("width : ", width, height)
        x_start = width*x
        y_end = height*y
        self.tap_coordinate([(x_start, y_end)])

    def is_on_this_page(self):
        """当前页面是否在群短信"""
        el = self.get_elements(self.__locators['欢迎使用群短信'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_add_contact(self):
        """点击添加收件人"""
        self.click_element(self.__class__.__locators["群成员列表"])

    @TestLogger.log()
    def click_first_contact(self):
        """点击选择群成员列表第一个"""
        self.click_element(self.__class__.__locators["选择群成员列表第一个"])

    @TestLogger.log()
    def click_contact_sure(self):
        """点击选择群成员确定"""
        self.click_element(self.__class__.__locators["选择群成员_确定"])

    @TestLogger.log()
    def wait_for_record_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待群短信记录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["记录"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_exist_select_all(self):
        """判断是否存在全选按钮"""
        el = self.get_elements(self.__class__.__locators["全选"])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def is_exist_select_and_all(self):
        """判断是否存在已选择人数和可选择的最高上限人数"""
        el = self.get_elements(self.__class__.__locators["已选择人数和可选择的最高上限人数"])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_select_contact_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待选择群成员列表加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["搜索成员"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_select_all(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["全选"])

    @TestLogger.log()
    def click_second_contact(self):
        """点击选择群成员列表第二个"""
        self.click_element(self.__class__.__locators["选择群成员列表第二个"])

    @TestLogger.log()
    def is_exist_renew_select(self):
        """判断是否可重新选择联系人"""
        el = self.get_elements(self.__class__.__locators["可重新选择联系人"])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def input_search_message(self, message):
        """输入搜索成员信息"""
        self.input_text(self.__class__.__locators["搜索成员"], message)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        return self





