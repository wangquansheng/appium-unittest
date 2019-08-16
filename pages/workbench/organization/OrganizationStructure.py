import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class OrganizationStructurePage(BasePage):
    """组织架构首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5Activity'

    __locators = {
        '组织架构': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text ="组织架构"]'),
        '返回': (MobileBy.ID, "com.chinasofti.rcs:id/btn_back_actionbar"),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '添加子部门': (MobileBy.XPATH, '//*[@text ="添加子部门"]'),
        '分享': (MobileBy.XPATH, '//*[@resource-id ="code_qrcodeInner_share"]'),
        '保存二维码': (MobileBy.XPATH, '//*[@resource-id ="code_qrcodeInner_save"]'),
        '访客模式开关': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View[1]'),
        '点击右上角即可分享': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[6]/android.view.View'),
        '子部门名称输入框': (MobileBy.XPATH, '//*[@resource-id ="department_add_name_input"]'),
        '部门排序输入框': (MobileBy.XPATH, '//*[@resource-id ="department_add_sort_input"]'),
        '当前组织联系人': (MobileBy.XPATH, '//*[@class ="android.widget.CheckBox"]'),
        '确定删除成员': (MobileBy.XPATH, '//*[@resource-id ="contact_del_confirm"]'),
        '搜索框': (MobileBy.XPATH, '//*[@resource-id ="c_com_search_input_own"]'),
        '完成': (MobileBy.XPATH, '//*[@text="完成"]'),
        '删除': (MobileBy.XPATH, '//*[@text="删除"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '联系人名称输入框': (MobileBy.XPATH, '//*[@resource-id ="contact_add_name_input"]'),
        '联系人号码输入框': (MobileBy.XPATH, '//*[@resource-id ="contact_add_mobile_input"]'),
        '确定删除部门': (MobileBy.XPATH, '//*[@resource-id ="c_com_confirm"]'),
        '关闭返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '我知道了': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待组织架构首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("添加联系人")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_exist_specify_element_by_name(self, name):
        """是否存在指定元素"""
        locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def click_specify_element_by_name(self, name):
        """点击指定元素"""
        try:
            locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]' % name)
            self.click_element(locator)
        except:
            # 华为note 8手机-content-desc
            locator = (MobileBy.XPATH, '//*[contains(@content-desc,"%s")]' % name)
            self.click_element(locator)

    @TestLogger.log()
    def click_specify_element_by_name2(self, name):
        """点击指定元素"""
        try:
            locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]' % name)
            self.click_element(locator)
        except:
            # 华为note 8手机-content-desc
            locator = (MobileBy.XPATH, '//*[contains(@content-desc,"%s")]' % name)
            self.click_element(locator)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在组织架构页"""
        el = self.get_elements(self.__class__.__locators['添加子部门'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_invite_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待邀请伙伴页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("扫一扫")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_invite_share(self):
        """点击分享"""
        self.click_element(self.__class__.__locators["分享"])

    @TestLogger.log()
    def click_invite_save(self):
        """点击保存二维码"""
        self.click_element(self.__class__.__locators["保存二维码"])

    @TestLogger.log()
    def click_invite_mode_switch(self):
        """点击访客模式开关"""
        self.click_element(self.__class__.__locators["访客模式开关"])

    @TestLogger.log()
    def is_exist_element_by_locatorname(self, locatorname):
        """是否存在指定定位器名称的元素"""
        return self._is_element_present(self.__class__.__locators[locatorname])

    @TestLogger.log()
    def wait_for_sub_department_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待子部门创建页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("部门属性")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def input_sub_department_name(self, name):
        """输入子部门名称"""
        self.input_text(self.__class__.__locators["子部门名称输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_sub_department_sort(self, number):
        """输入子部门排序"""
        self.input_text(self.__class__.__locators["部门排序输入框"], number)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def get_contacts_in_organization(self):
        """获取组织联系人"""
        els = self.get_elements(self.__class__.__locators['当前组织联系人'])
        return els


    @TestLogger.log()
    def wait_for_delete_contacts_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待批量删除成员页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("请选择联系人")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def input_search_box(self, name):
        """输入搜索框信息"""
        self.input_text(self.__class__.__locators["搜索框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_confirm(self):
        """点击完成"""
        self.click_element(self.__class__.__locators["完成"])

    @TestLogger.log()
    def input_contacts_name(self, name):
        """输入联系人名称"""
        self.input_text(self.__class__.__locators["联系人名称输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_contacts_number(self, name):
        """输入联系人号码"""
        self.input_text(self.__class__.__locators["联系人号码输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def swipe_and_find_element(self, text):
        """滑动并查找特定元素"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % text))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_element_present_by_name(self, text):
        """判断元素是否存在"""
        time=0
        times=10
        while time < times :
            if self.is_text_present(text):
                return True
            time += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def click_cancle(self):
        """点击关闭返回"""
        self.click_element(self.__class__.__locators["关闭返回"])

    @TestLogger.log("点击我知道了")
    def click_i_know(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['我知道了']):
            self.click_element(self.__class__.__locators['我知道了'])
        return True
