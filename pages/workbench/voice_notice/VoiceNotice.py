from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class VoiceNoticePage(BasePage):
    """语音通知页面/超级会议页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        # 语音通知页面
        '语音通知标题': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '？': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '创建语音通知': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[5]/android.view.View'),
        '我创建的': (MobileBy.XPATH, '//*[@text="我创建的"]'),
        '我接受的': (MobileBy.XPATH, '//*[@text="我接受的"]'),
        # 打开语音通知使用指引页面
        '语音通知使用指导': (MobileBy.XPATH, '//*[@text="语音通知使用指导"]'),
        '发起语音通知': (MobileBy.XPATH, '//*[@text="发起语音通知"]'),
        '接听通知': (MobileBy.XPATH,  "//*[contains(@text,'3、接听通知')]"),
        '查看通知详情': (MobileBy.XPATH, '//*[@text="查看通知详情"]'),
        # 超级会议页面
        '超级会议': (MobileBy.XPATH, '//*[@text="超级会议"]'),
        '会场管理': (MobileBy.XPATH, "//*[contains(@text,'4、会场管理')]"),
        # '通知内容输入框': (MobileBy.XPATH, "//*[@resourceId='b'undefined--undefined-63883'']"),
        '通知内容输入框': (MobileBy.XPATH, "//*[@class='android.widget.EditText']"),
        '+号': (MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[3]"),
        '发送语音通知': (MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[10]/android.view.View"),
        '上三角': (MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[8]"),
        '如何申请认证X号': (MobileBy.XPATH, '//*[@text="javascript:closeTips();"]'),
        '语音话筒按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/record_audio'),
        '语音按钮': (MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View[4]/android.widget.Image"),
        # '语音按钮': (MobileBy.XPATH, "//android.view.View[@content-desc='会议通知活动通知投票通知']/following-sibling::android.view.View[2]"),
        '已录制的语音': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]'),
        '已录制语音删除按钮': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[3]/android.widget.Image'),
        '语音话筒删除': (MobileBy.ID, 'com.chinasofti.rcs:id/image_cancel'),
        '键盘': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View[2]/android.widget.Image'),
        '创建通知语音': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View[4]/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View'),
        '查询文本删除X': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),

    }

    @TestLogger.log()
    def wait_for_page_loads(self, text="创建语音通知", timeout=60):
        """等待 语音通知页面加载"""
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
        """当前页面是否在语音通知页"""
        el = self.get_elements(self.__class__.__locators['？'])
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

