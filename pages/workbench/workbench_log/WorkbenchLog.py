from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class WorkbenchLogPage(BasePage):
    """工作台日志页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '日志': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '我发出的': (MobileBy.XPATH, '//*[@text="我发出的"]'),
        '我收到的': (MobileBy.XPATH, '//*[@text="我收到的"]'),
        '写日志': (MobileBy.XPATH, '//*[@text="写日志"]'),
        '没有找到你想要的结果': (MobileBy.XPATH, '//*[@text="没有找到你想要的结果"]'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '日报': (MobileBy.XPATH, '//*[@text="日报"]'),
        '周报': (MobileBy.XPATH, '//*[@text="周报"]'),
        '月报': (MobileBy.XPATH, '//*[@text="月报"]'),
        '今日工作总结输入框': (MobileBy.XPATH, '//*[@text="今日工作总结"]/following-sibling::*[1]/android.widget.EditText'),
        '明日工作计划输入框': (MobileBy.XPATH, '//*[@text="明日工作计划"]/following-sibling::*[1]/android.widget.EditText'),
        '需要协调与帮助输入框': (MobileBy.XPATH, '//*[@text="需要协调与帮助"]/following-sibling::*[1]/android.widget.EditText'),
        '备注输入框': (MobileBy.XPATH, '//*[@text="备注"]/following-sibling::*[1]/android.widget.EditText'),
        '标题': (MobileBy.XPATH, '//*[@text="标题"]/following-sibling::*[1]/android.widget.EditText'),
        '+': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[11]/android.view.View/android.view.View/android.view.View'),
        '添加上次联系人': (MobileBy.XPATH, '//*[@text="添加上次联系人"]'),
        '存草稿': (MobileBy.XPATH, '//*[@text="存草稿"]'),
        # '提交': (MobileBy.XPATH, '//*[@text="提交"]'),
        '提交': (MobileBy.XPATH, '//*[@resource-id="save"]'),
        '头像': (MobileBy.XPATH, '//*[@resource-id="man.userId"]'),
        '删除': (MobileBy.XPATH, '//*[@text="删除"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
        '评论': (MobileBy.XPATH, '//*[contains(@resource-id,"report_")]/android.view.View[last()-1]'),
        '点赞': (MobileBy.XPATH, '(//android.widget.Image)[2]'),
        '点赞信息': (MobileBy.XPATH, '//*[contains(@resource-id,"report_")]/android.view.View[last()-2]'),
        '点赞人信息': (MobileBy.ID, 'man.userId'),
        '点赞人数量': (MobileBy.XPATH, "//*[contains(@text, '人点赞')]"),
        '发布': (MobileBy.XPATH, '//*[@text="发布"]'),
        '评论输入框': (MobileBy.XPATH, '(//android.widget.EditText)'),
        '当前页面第一条日报': (MobileBy.XPATH, '//*[contains(@resource-id,"data_")][1]'),

    }

    @TestLogger.log()
    def wait_for_page_loads(self, text="写日志", timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present(text),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_create_new_log(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['写日志'])

    @TestLogger.log()
    def click_day_news(self):
        """点击日报"""
        self.click_element(self.__class__.__locators['日报'])

    @TestLogger.log()
    def click_week_news(self):
        """点击周报"""
        self.click_element(self.__class__.__locators['周报'])

    @TestLogger.log()
    def click_month_news(self):
        """点击月报"""
        self.click_element(self.__class__.__locators['月报'])

    @TestLogger.log()
    def input_title(self, title):
        """输入标题"""
        self.input_text(self.__class__.__locators["标题"], title)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_work_summary(self, work_summary):
        """输入今日工作总结"""
        self.input_text(self.__class__.__locators["今日工作总结输入框"], work_summary)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_work_plan(self, work_plan):
        """输入明日工作计划"""
        self.input_text(self.__class__.__locators["明日工作计划输入框"], work_plan)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_coordination_help(self, coordinate_help):
        """输入需要协调与帮助"""
        self.input_text(self.__class__.__locators["需要协调与帮助输入框"], coordinate_help)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_remark(self, remark):
        """输入备注"""
        self.input_text(self.__class__.__locators["备注输入框"], remark)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_add_last_contact(self):
        """点击添加上次联系人"""
        self.click_element(self.__class__.__locators['添加上次联系人'])

    @TestLogger.log()
    def click_add_contact(self):
        """点击添加联系人"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(self.__class__.__locators['+'])

    @TestLogger.log()
    def click_save_draft(self):
        """点击存草稿"""
        self.click_element(self.__class__.__locators['存草稿'])

    @TestLogger.log()
    def click_submit(self):
        """点击提交"""
        self.click_element(self.__class__.__locators['提交'])

    @TestLogger.log()
    def wait_for_input_page_loads(self, timeout=60):
        """等待日志编辑页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["标题"]),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_avatar_delete(self):
        """点击头像删除"""
        self.click_element(self.__class__.__locators['头像'])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators['删除'])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def click_like(self):
        """点击点赞"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(self.__class__.__locators['点赞'])

    @TestLogger.log()
    def click_comment(self):
        """点击评论"""
        self.click_element(self.__class__.__locators['评论'])

    @TestLogger.log()
    def click_like_information(self):
        """点击点赞信息"""
        self.click_element(self.__class__.__locators['点赞信息'])

    @TestLogger.log()
    def is_exist_like(self):
        """是否存在点赞"""
        return self._is_element_present(self.__class__.__locators["点赞信息"])

    @TestLogger.log()
    def is_exist_like_information(self):
        """是否存在点赞人信息"""
        return self._is_element_present(self.__class__.__locators["点赞人信息"])

    @TestLogger.log()
    def is_exist_like_number(self):
        """是否存在点赞人数量"""
        return self._is_element_present(self.__class__.__locators["点赞人数量"])

    @TestLogger.log()
    def click_release(self):
        """点击发布"""
        self.click_element(self.__class__.__locators['发布'])

    @TestLogger.log()
    def input_comment(self, comment):
        """输入标题"""
        self.input_text(self.__class__.__locators["评论输入框"], comment)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_first_news(self):
        """点击当前页面第一条日报"""
        self.click_element(self.__class__.__locators['当前页面第一条日报'])