from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SuperMeetingPage(BasePage):
    """超级会议页面"""
    ACTIVITY = ''

    __locators = {
        '？': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '创建语音通知': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[5]/android.view.View'),
        # '预约会议': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.view.View[1]'),
        '预约会议': (MobileBy.XPATH, '//*[contains(@text,"预约会议")]'),
        '马上开会': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.view.View[2]'),
        '下三角': (MobileBy.XPATH, '//*[@text="ic_arrow_%20down"]'),
        '上三角': (MobileBy.XPATH, '//*[@text="ic_arrow_upward"]'),
        '(2人)': (MobileBy.XPATH, '//*[@text="（2人）"]'),
        '(3人)': (MobileBy.XPATH, '//*[@text="（3人）"]'),
        '去掉会议人员X': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.ListView/android.view.View[2]/android.view.View[1]/android.view.View/android.widget.Image'),
        '查询文本删除X': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '右三角': (MobileBy.ID, 'com.chinasofti.rcs:id/img_right_department'),
        '会议开始日期': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.view.View[1]'),
        '减号5': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.ListView/android.view.View[5]/android.widget.Image'),
        '加号': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.ListView/android.view.View[3]/android.widget.Image'),
        '确定删除所有记录': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]'),
        '确定取消此次会议': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[4]/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]'),

    }

    @TestLogger.log()
    def wait_for_page_loads(self, text="预约会议", timeout=60):
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
    def click_enter_more(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['？'])

    @TestLogger.log()
    def click_close_more(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['X'])

    def swipe_half_page_up(self):
        """向上滑动半页"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)

    def swipe_half_page_down(self):
        """向下滑动半页"""
        self.swipe_by_percent_on_screen(50, 30, 50, 80, 800)

    def find_els_h5(self, location):
        """查找元素"""
        els = self.get_elements(self.__locators[location])
        if len(els) > 0:
            return True
        else:
            raise AssertionError("该页面没有定位到该元素")

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在超级会议页"""
        el = self.get_elements(self.__class__.__locators['预约会议'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def input_notice_text(self, name):
        """输入通知信息"""
        self.input_text(self.__class__.__locators["通知内容输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_add(self):
        """点击加号"""
        self.click_element(self.__class__.__locators['+号'])

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators['发送语音通知'])

    @TestLogger.log()
    def click_element_(self,text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_element_(self, text,times):
        """点击元素"""
        el=self.get_element(self.__class__.__locators[text])
        self.press(el,times)

    @TestLogger.log()
    def is_element_exit(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def swipe_by_up(self):
        """滑动会议日期"""
        self.press_and_move_to_up(self.__class__.__locators['会议开始日期'])


