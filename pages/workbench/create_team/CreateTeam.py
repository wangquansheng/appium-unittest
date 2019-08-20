from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

class CreateTeamPage(BasePage):
    """创建团队页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/rl_webview_content': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_webview_content'),
        'com.chinasofti.rcs:id/actionbar_main_enterprise': (
        MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_main_enterprise'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '创建团队': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '请输入团队名称': (MobileBy.XPATH,'//*[@resource-id="qy_name"]'),
        # '请输入团队名称': (MobileBy.XPATH, '//*[@text="请输入团队名称"  or @content-desc="请输入团队名称"]'),
        '选择行业': (MobileBy.XPATH, '//*[@resource-id="xzhy"]'),
        '选择所在地': (MobileBy.XPATH, '//*[@resource-id="xzszd"]'),
        '请务必填写真实姓名': (MobileBy.XPATH,'//*[@resource-id="gly_name"]'),
        # '请务必填写真实姓名': (MobileBy.XPATH, '//*[@text="请务必填写真实姓名" or @content-desc="请务必填写真实姓名" ]'),
        # '14775290489@139.com': (MobileBy.ID, 'gly_email'),
        '邮箱': (MobileBy.XPATH, '//*[@resource-id="gly_email"]'),
        '立即创建团队': (MobileBy.XPATH, '//*[@text="立即创建团队" or @content-desc="立即创建团队"]'),
        # 点击创建团队后，设置工作台
        '完成设置工作台': (MobileBy.XPATH, '//*[@text="完成设置工作台" or @content-desc="完成设置工作台"]'),
        # 创建成功后页面
        '创建成功': (MobileBy.XPATH, '//*[@content-desc="创建成功"]'),
        '登录后台可体验更全面的管理功能': (MobileBy.XPATH, '//*[@content-desc="登录后台可体验更全面的管理功能"]'),
        '进入工作台': (MobileBy.XPATH, '//*[@text="直接进入工作台" or @content-desc="直接进入工作台"]'),
        # 未输入姓名时的弹窗提示
        '请输入管理员姓名': (MobileBy.XPATH, '//*[@content-desc="请输入管理员姓名"]'),
        '确定': (MobileBy.XPATH, '//*[contains(@text,"确定")]'),
        '公告首页': (MobileBy.XPATH, '//*[@content-desc="向团队所有成员发出第一条公告"]'),
        '发布公告': (MobileBy.XPATH, '//*[@content-desc="发布公告"]'),
        '未发公告': (MobileBy.XPATH, '//*[@content-desc="未发公告"]'),
        #  '公告标题': (MobileBy.ID,'title'),
        '公告标题': (MobileBy.XPATH, '//*[@content-desc="请输入公告标题"]'),
        '公告内容': (MobileBy.XPATH, '//*[@content-desc="请输入公告内容"]'),
        '发布': (MobileBy.XPATH, '//*[@content-desc="发布"]'),
        '保存': (MobileBy.XPATH, '//*[@content-desc="保存"]'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '公告信息': (MobileBy.XPATH, '//*[@text="公告信息"]'),
        '下线': (MobileBy.XPATH, '//*[@content-desc="下线"]'),
        '搜索框': (MobileBy.XPATH, '//*[@content-desc="搜索"]'),
        '天气预报': (MobileBy.XPATH, '//*[@content-desc="天气预报"]'),
        '删除': (MobileBy.XPATH, '//*[@content-desc="删除"]'),
        '邀请成员': (MobileBy.XPATH, '//*[@text="邀请成员"]'),
        '选择城市': (MobileBy.XPATH, '//*[@text="北京市"or @content-desc="北京市"]'),
        '选择城市城区': (MobileBy.XPATH, '//*[@text="西城" or @content-desc="西城"]'),
        '计算机软件': (MobileBy.XPATH, '//*[@text="计算机软件" or @content-desc="计算机软件"]'),

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 创建团队页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("立即创建团队")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_enter_workbench(self):
        """点击直接进入工作台"""
        self.click_element(self.__class__.__locators['进入工作台'])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def choose_location(self, city="北京市", area="西城"):
        """选择所在地"""
        self.click_element(self.__class__.__locators['选择所在地'])
        try:
            self.click_element(self.__class__.__locators['选择城市'])
        except:
            # self.click_element((MobileBy.XPATH, '//*[@text="选择地区"]/../android.view.View/android.view.View[1]'))
            self.click_element((MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[15]/android.view.View[2]/android.view.View[1]'))
        try:
            self.click_element(self.__class__.__locators['选择城市城区'])
        except:
            # self.click_element((MobileBy.XPATH, '//*[@text="上一级"]/../android.view.View/android.view.View[1]'))
            self.click_element((MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[16]/android.view.View[4]/android.view.View[1]'))

    @TestLogger.log()
    def choose_industry(self, hy="计算机软件"):
        """选择行业"""
        self.click_element(self.__class__.__locators['选择行业'])
        time.sleep(1)
        try:
            # self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % hy))
            self.click_element(self.__class__.__locators['计算机软件'])
        except:
            # self.click_element((MobileBy.XPATH, '//*[@text="选择行业"]/../android.view.View/android.view.View[2]'))
            self.click_element((MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[15]/android.view.View[2]/android.view.View[3]'))

    @TestLogger.log()
    def input_team_name(self, name):
        """输入团队名字"""
        self.input_text(self.__class__.__locators["请输入团队名称"], name)

    @TestLogger.log()
    def input_real_name(self, name):
        """输入真实姓名"""
        self.input_text(self.__class__.__locators["请务必填写真实姓名"], name)

    @TestLogger.log()
    def click_immediately_create_team(self):
        """点击立即创建团队"""
        self.click_element(self.__class__.__locators['立即创建团队'])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在创建团队页面"""
        try:
            self.wait_until(
                timeout=8,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["立即创建团队"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_finish_setting_workbench(self):
        """点击 完成设置工作台"""
        self.click_element(self.__class__.__locators['完成设置工作台'])

    @TestLogger.log()
    def wait_for_create_team_success_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待 创建团队 成功页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("创建成功")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def input_email(self, email):
        """输入邮箱名字"""
        self.input_text(self.__class__.__locators["邮箱"], email)

    @TestLogger.log()
    def search_team_name(self, name):
        """输入团队名字"""
        self.input_text(self.__class__.__locators["请输入团队名称"], name)

    @TestLogger.log()
    def click_enter_search(self):
        """搜索内容"""
        self.click_element(self.__class__.__locators['搜索'])

    @TestLogger.log('创建公告')
    def create_team_message(self,title='天气预报',content='晴天转多云'):
        self.click_element(self.__class__.__locators['发布公告'])
        self.input_text(self.__class__.__locators['公告标题'],title)
        self.input_text(self.__class__.__locators['公告内容'],content)
        self.click_element(self.__class__.__locators['发布'])
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log('创建草稿公告')
    def save_team__message(self, title='天气预报', content='晴天转多云'):
        self.click_element(self.__class__.__locators['发布公告'])
        self.input_text(self.__class__.__locators['公告标题'], title)
        self.input_text(self.__class__.__locators['公告内容'], content)
        self.click_element(self.__class__.__locators['保存'])
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log('判断是否存在公告信息')
    def is_team_message_exist(self):
        return self.is_text_present(self.__class__.__locators['公告首页'])

    @TestLogger.log()
    def click_enter_search(self):
        """搜索内容"""
        self.click_element(self.__class__.__locators['搜索'])

    @TestLogger.log()
    def click_workbeanch_button(self):
        """工作台"""
        self.click_element(self.__class__.__locators['工作台'])



    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)



    @TestLogger.log("进入公告")
    def click_public_message(self):
        """点击不同意"""
        self.click_element(self.__class__.__locators['公告信息'])

    @TestLogger.log()
    def input_search_text(self, text='天气'):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators["搜索框"], text)
        time.sleep(1)
        self.click_element(self.__class__.__locators['搜索'])
        time.sleep(1)
        self.click_element(self.__class__.__locators['搜索框'])

    @TestLogger.log()
    def click_list_message(self, text='天气预报'):
        "选择列表中信息"
        self.click_element(self.__class__.__locators['天气预报'])

    @TestLogger.log()
    def click_remove_message(self):
        "选择列表中信息"
        self.click_element(self.__class__.__locators['下线'])
        self.click_element(self.__class__.__locators['确定'])


    @TestLogger.log('未发布')
    def click_no_publish(self):
        self.click_element(self.__class__.__locators['未发公告'])

    @TestLogger.log("删除信息")
    def remove_message(self):
        "选择列表中信息"
        if self.is_text_present('天气预报'):
            self.click_element(self.__class__.__locators['天气预报'])
            time.sleep(1)
            if self.is_text_present('删除'):
                self.click_element(self.__class__.__locators['删除'])
                self.click_element(self.__class__.__locators['确定'])
            elif self.is_text_present('下线'):
                self.click_element(self.__class__.__locators['下线'])
                self.click_element(self.__class__.__locators['确定'])
            else:
                print("无删除按钮")
                return True
        else:
            print("无此信息")

    @TestLogger.log('发布')
    def click_publish(self):
        self.click_element(self.__class__.__locators['发布'])

    @TestLogger.log()
    def wait_for_setting_workbench_page_load(self):
        """当前页面是否在设置工作台页面"""
        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["完成设置工作台"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def choose_location_without_city(self, province="河北省"):
        """选择所在地"""
        self.click_element(self.__class__.__locators['选择所在地'])
        try:
            self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % province))
        except:
            self.click_element((MobileBy.XPATH, '//*[@text="选择地区"]/../android.view.View/android.view.View[1]'))

    @TestLogger.log()
    def get_email_text(self):
        """获取团队名字"""
        el=self.get_element(self.__class__.__locators["邮箱"])
        return el.text

    @TestLogger.log()
    def click_invite_member(self):
        """点击邀请成员"""
        self.click_element(self.__class__.__locators['邀请成员'])


