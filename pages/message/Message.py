from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
import time
from pages.contacts.Contacts import ContactsPage


class MessagePage(FooterPage):
    """主页 - 消息页"""

    ACTIVITY = 'com.cmic.module_main.ui.activity.HomeActivity'

    __locators = {
        "+号": (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/itemLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/itemLayout'),
        'com.chinasofti.rcs:id/pop_item_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_item_layout'),
        'com.chinasofti.rcs:id/iconIV': (MobileBy.ID, 'com.chinasofti.rcs:id/iconIV'),
        '新建消息': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="新建消息"]'),
        '免费短信': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="免费短信"]'),
        '发起群聊': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="发起群聊"]'),
        '分组群发': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="分组群发"]'),
        '群发助手': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="群发助手"]'),

        '扫一扫': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="扫一扫"]'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '页头-消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        '消息列表': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_conv_list'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/search_edit'),
        '消息项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        '消息头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '消息名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        '消息简要内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        '消息免打扰': (MobileBy.XPATH,
                  '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="%s"]/../../*[@resource-id="com.chinasofti.rcs:id/ll_unread"]'),
        '置顶群': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name"]'),
        '消息发送失败感叹号': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_fail_status'),
        '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
        '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
        '删除聊天': (MobileBy.XPATH, "//*[contains(@text, '删除聊天')]"),
        # 消息页中点击已发送文件
        '文件': (MobileBy.XPATH, "//*[contains(@text, '文件')]"),
        '位置': (MobileBy.XPATH, "//*[contains(@text, '位置')]"),
        '发送名片': (MobileBy.XPATH, "//*[contains(@text, '发送名片')]"),
        '名片': (MobileBy.XPATH, "//*[contains(@text, '名片')]"),
        "未读消息气泡": (MobileBy.ID, "com.chinasofti.rcs:id/rnMessageBadge"),
        '页面文案': (MobileBy.XPATH, "//*[contains(@text, '图文消息，一触即发')]"),
        '置顶聊天': (MobileBy.XPATH, '//*[@text="置顶聊天"]'),
        '取消置顶': (MobileBy.XPATH, '//*[@text="取消置顶"]'),
        "消息免打扰图标": (MobileBy.ID, "com.chinasofti.rcs:id/iv_conv_slient"),
        "消息红点": (MobileBy.ID, "com.chinasofti.rcs:id/red_dot_silent"),
        "版本更新": (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_title'),
        "以后再说": (MobileBy.ID, "com.chinasofti.rcs:id/btn_cancel"),
        '立即更新': (MobileBy.ID, "com.chinasofti.rcs:id/btn_ok"),
        '创建群聊': (MobileBy.ID, "com.chinasofti.rcs:id/creategroup"),
        "选择手机联系人": (MobileBy.XPATH, "//*[contains(@text,'选择手机联系人')]"),
        "确定2": (MobileBy.ID, "com.chinasofti.rcs:id/tv_sure"),
        "群聊名": (MobileBy.ID, "com.chinasofti.rcs:id/et_group_name"),
        "有人@我": (MobileBy.XPATH, "//*[contains(@text,'有人@我')]"),
        "草稿": (MobileBy.ID, "com.chinasofti.rcs:id/tv_msg_draft_hint"),
        "手机联系人": (MobileBy.ID, "com.chinasofti.rcs:id/first_item"),

        "欢迎使用群发助手": (MobileBy.XPATH, "//*[contains(@text,'欢迎使用群发助手')]"),
        "群发助手欢迎页确定": (MobileBy.ID, "com.chinasofti.rcs:id/confirm_btn"),
        "搜索输入框": (MobileBy.ID, "com.chinasofti.rcs:id/edit_query01"),
        '我的电脑': (MobileBy.XPATH, '//*[@text="我的电脑"]'),

        '企业头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '企业标识': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head_EP_type'),
        '企业群名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '企业成员数量': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_member_count'),
        '搜索我的电脑': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '相册': (MobileBy.ID, 'com.chinasofti.rcs:id/capture_scan_photo'),
        '全部团队': (MobileBy.ID, 'com.chinasofti.rcs:id/all_team'),
        '创建团队': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_group_chat_item_id'),
        '和飞信号': (MobileBy.ID, 'com.chinasofti.rcs:id/card_photo_num'),

    }

    @TestLogger.log()
    def page_should_contain_my_computer(self):
        """检查是否存在我的电脑"""
        if not self._is_element_present(self.__class__.__locators["我的电脑"]):
            raise AssertionError('没有我的电脑选项,请先登录和飞信电脑版!')
        return True

    @TestLogger.log("点击我的电脑")
    def click_my_computer(self):
        self.click_element(self.__locators["我的电脑"])
        time.sleep(1)

    @TestLogger.log("点击搜索到我的电脑")
    def click_search_my_computer(self):
        self.click_element(self.__locators["搜索我的电脑"])
        time.sleep(1)

    @TestLogger.log()
    def action_welcome_groupsmspage(self):
        """群发助手欢迎页处理"""
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators["欢迎使用群发助手"]):
            self.click_element(self.__locators["群发助手欢迎页确定"])

    @TestLogger.log("点击创建群聊")
    def click_create_group(self):
        self.click_element(self.__locators["创建群聊"])
        time.sleep(1)

    @TestLogger.log("点击选择手机联系人")
    def click_contact_group(self):
        self.click_element(self.__locators["选择手机联系人"])
        time.sleep(1)

    @TestLogger.log("点击手机联系人")
    def click_phone_contact(self):
        self.click_element(self.__locators["手机联系人"])
        time.sleep(1)

    @TestLogger.log("点击群聊名")
    def click_group_name(self):
        self.click_element(self.__locators["群聊名"])
        time.sleep(1)

    @TestLogger.log("检查群聊名是否存在")
    def check_group_name_exist(self):
        return self.page_should_not_contain_element(self.__locators["群聊名"])

    @TestLogger.log("设置群聊名")
    def set_group_name(self, text='aaa'):
        self.input_text(self.__locators["群聊名"], text)
        time.sleep(1)

    @TestLogger.log("点击确定")
    def click_sure_button(self):
        self.click_element(self.__locators["确定2"])
        time.sleep(1)

    @TestLogger.log("点击通话")
    def click_calls(self):
        self.click_element(self.__locators["通话"])
        time.sleep(1)

    @TestLogger.log("判断未进群提示次数")
    def check_group_toast_num(self):
        from unittest import TestCase
        TestCase().assertEqual
        return TestCase().assertEqual(len(self.get_elements((MobileBy.XPATH, '//*[@text ="还有人未进群,再次邀请"]'))), 3)

    @TestLogger.log('检查顶部搜索框是否显示')
    def assert_search_box_is_display(self, max_wait_time=5):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['搜索']),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('搜索框没有显示：{}'.format(self.__locators['搜索']))

    @TestLogger.log('检查顶部搜索框是否显示')
    def assert_search_box_text_is(self, text):
        self.mobile.assert_element_text_should_be(self.__locators['搜索'], text, '搜索框文本与"{}"不匹配'.format(text))

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在消息页"""

        # mark=10
        # while mark>0:
        #     time.sleep(1)
        #     if (self._is_element_present(self.__class__.__locators["版本更新"])):
        #         self.click_element(self.__class__.__locators["以后再说"])
        #         break
        #     mark-=1
        # locator = (MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/btn_cancel" and @text ="以后再说"]')
        # if self._is_element_present(locator):
        #     self.click_element(locator)

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_add_icon(self):
        """点击加号图标"""
        self.click_element(self.__locators['+号'])
        time.sleep(1)

    @TestLogger.log()
    def click_new_message(self):
        """点击新建消息"""
        self.click_element(self.__locators['新建消息'])

    @TestLogger.log()
    def assert_new_message_text_equal_to(self, expect):
        """检查新建消息菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['新建消息'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_free_sms(self):
        """点击免费短信"""
        self.click_element(self.__locators['免费短信'])

    @TestLogger.log()
    def assert_free_sms_text_equal_to(self, expect):
        """检查免费短信菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['免费短信'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log('点击发起群聊')
    def click_group_chat(self):
        """点击发起群聊"""
        self.click_element(self.__locators['发起群聊'])
        time.sleep(1)

    @TestLogger.log()
    def click_contacts(self):
        """点击通讯录"""
        self.click_element(self.__locators['通讯录'])
        if ContactsPage().is_text_present('始终允许'):
            ContactsPage().click_always_allowed()
        time.sleep(1)
        if ContactsPage().is_text_present('发现SIM卡联系人'):
            ContactsPage().click_sim_contact_ok()
        time.sleep(2)

    @TestLogger.log()
    def click_contacts_only(self):
        """只点击通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log()
    def assert_group_chat_text_equal_to(self, expect):
        """检查发起群聊菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['发起群聊'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_group_mass(self):
        """点击分组群发"""
        self.click_element(self.__locators['分组群发'])

    @TestLogger.log()
    def click_mass_assistant(self):
        """点击群发助手"""
        self.click_element(self.__locators['群发助手'])

    @TestLogger.log()
    def assert_group_mass_text_equal_to(self, expect):
        """检查分组群发菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['分组群发'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_take_a_scan(self):
        """点击扫一扫"""
        self.click_element(self.__locators['扫一扫'])

    @TestLogger.log()
    def assert_take_a_scan_text_equal_to(self, expect):
        """检查扫一扫菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['扫一扫'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_search(self):
        """搜索"""
        self.click_element(self.__locators['搜索'])

    @TestLogger.log()
    def input_search_message(self, message):
        """输入查询内容"""
        self.input_text(self.__class__.__locators["搜索"], message)

    @TestLogger.log()
    def input_search_message_631(self, message):
        """输入查询内容"""
        self.input_text(self.__class__.__locators["搜索输入框"], message)

    @TestLogger.log()
    def search_and_enter(self, point):
        """消息页全局搜索内容并进入"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % point)
        self.click_search()
        from pages import SearchPage
        sp = SearchPage()
        sp.input_search_keyword(point)
        time.sleep(1)
        sp.click_element_c('团队联系人文本')
        time.sleep(2)
        self.find_element_by_swipe(locator)
        self.click_element(locator)

    @TestLogger.log()
    def search_and_enter2(self, point):
        """消息页全局搜索内容并进入"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % point)
        from pages import SearchPage
        sp = SearchPage()
        self.click_search()
        sp.input_search_keyword(point)
        time.sleep(1)
        sp.click_element_c('团队联系人文本')
        time.sleep(2)
        self.find_element_by_swipe(locator)
        self.click_element(locator)

    @TestLogger.log()
    def search_and_enter_631(self, point):
        """消息页全局搜索内容并进入"""
        self.click_search()
        from pages import SearchPage
        SearchPage().input_search_keyword(point)
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % point))

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        time.sleep(3)
        # mark=10
        # while mark>0:
        #     time.sleep(1)
        #     if (self._is_element_present(self.__class__.__locators["版本更新"])):
        #         self.click_element(self.__class__.__locators["以后再说"])
        #         break
        #     mark-=1

        # locator = (MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/btn_cancel" and @text ="以后再说"]')
        # if self._is_element_present(locator):
        #     self.click_element(locator)

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_login_success(self, timeout=8, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        # time.sleep(15)
        # locator = (MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/btn_cancel" and @text ="以后再说"]')
        # if self._is_element_present(locator):
        #     self.click_element(locator)
        self.__unexpected_info = None

        def unexpected():
            result = self.get_text(
                [MobileBy.XPATH,
                 '//*[@text="当前网络不可用(102101)，请检查网络设置" or' +
                 ' @text="服务器繁忙或加载超时,请耐心等待" or' +
                 ' contains(@text,"一键登录暂时无法使用") or' +
                 ' contains(@text,"登录失败") or' +
                 ' @text="网络连接超时(102102)，请使用短信验证码登录" or' +
                 ' @text="立即更新" or' +
                 ']'])
            self.__unexpected_info = result
            return result

        # mark = 10
        # while mark > 0:
        #     time.sleep(1)
        #     if (self._is_element_present(self.__class__.__locators["版本更新"])):
        #         self.click_element(self.__class__.__locators["以后再说"])
        #         break
        #     mark -= 1

        try:
            self.wait_condition_and_listen_unexpected(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["+号"]),
                unexpected=unexpected
            )
        except TimeoutException:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        except AssertionError:
            raise AssertionError("检查到页面报错：{}".format(self.__unexpected_info))
        return self

    @TestLogger.log('检查是否收到某个号码的短信')
    def assert_get_sms_of(self, phone_number, content, max_wait_time=30):
        try:
            self.click_message(phone_number, max_wait_time)
        except NoSuchElementException:
            raise AssertionError('没有收到{}的消息'.format(phone_number))

    @TestLogger.log("检查列表第一项消息标题")
    def assert_first_message_title_in_list_is(self, title, max_wait_time=5):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['消息名称']) == title,
                timeout=max_wait_time,
                auto_accept_permission_alert=False
            )
        except TimeoutException:
            raise AssertionError('"{} != {}"'.format(self.get_text(self.__locators['消息名称']), title))

    @TestLogger.log('检查页面有没有出现139邮箱消息')
    def assert_139_message_not_appear(self, max_wait_time=30):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.is_text_present('139邮箱助手'),
                timeout=max_wait_time
            )
        except TimeoutException:
            return
        raise AssertionError('消息列表中不应该显示139邮箱消息，但实际上有显示')

    @TestLogger.log('点击消息')
    def click_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        self.find_message(title, max_wait_time)
        self.click_element(locator)

    @TestLogger.log('置顶消息')
    def set_top_for_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        self.find_message(title, max_wait_time)
        message = self.get_element(locator)
        position_x, position_y = message.location.get('x'), message.location.get('y')
        self.mobile.tap([(position_x, position_y)], 1000)
        if self.is_text_present('取消置顶'):
            el = self.get_element([MobileBy.XPATH, '//*[@text="取消置顶"]'])
            position_y, position_y = el.location.get('x'), el.location.get('y') - 100
            self.mobile.tap([(position_x, position_y)])
            return
        if self.is_text_present('置顶聊天'):
            self.click_text('置顶聊天')
        else:
            raise NoSuchElementException('没找到“置顶消息”菜单')

    @TestLogger.log("检查最新的一条消息的Title")
    def assert_the_first_message_is(self, title, max_wait_time=5):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['消息名称']) == title,
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('{}秒内没有找到"{}"的最新消息'.format(max_wait_time, title))

    @TestLogger.log("寻找定位消息")
    def find_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            if not self.get_elements(self.__locators['消息项']):
                try:
                    self.wait_until(
                        condition=lambda d: self.get_element(locator),
                        timeout=max_wait_time,
                        auto_accept_permission_alert=False
                    )
                    return
                except TimeoutException:
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))
            max_try = 20
            current = 0
            while current < max_try:
                first_item = self.get_element(self.__locators['消息项'])
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if not ec.staleness_of(first_item)(True):
                    break
            self.scroll_to_top()
            try:
                self.wait_until(
                    condition=lambda d: self.get_element(locator),
                    timeout=max_wait_time,
                    auto_accept_permission_alert=False
                )
                return
            except TimeoutException:
                raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    @TestLogger.log("回到列表顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        # 如果找到“短信设置”菜单，则当作已经滑到底部
        if self._is_on_the_start_of_list_view():
            return True
        max_try = 50
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_on_the_start_of_list_view():
                break
        return True

    @TestLogger.log("下一页")
    def page_down(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        self.swipe_by_direction(self.__locators['消息列表'], 'up')

    @TestLogger.log("下一页")
    def page_up(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        self.swipe_by_direction(self.__locators['消息列表'], 'down')

    def _is_on_the_start_of_list_view(self):
        """判断是否列表开头"""
        return self._is_element_present(self.__locators['搜索'])

    @TestLogger.log()
    def is_exist_undisturb(self, group_name):
        """某群是否存在消息免打扰标志"""
        path = self.__class__.__locators["消息免打扰"][1]
        self.__class__.__locators["xpath"] = (self.__class__.__locators["消息免打扰"][0], path % group_name)
        return self._is_element_present(self.__class__.__locators["xpath"])

    @TestLogger.log()
    def get_top_news_name(self):
        """获取置顶群的名字"""
        return self.get_element(self.__class__.__locators['置顶群']).text

    @TestLogger.log()
    def click_element_by_text(self, text):
        """点击指定元素"""
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % text))

    @TestLogger.log()
    def is_iv_fail_status_present(self):
        """判断消息发送失败“！”标致是否存在"""
        return self._is_element_present(self.__locators['消息发送失败感叹号'])

    @TestLogger.log()
    def is_message_fail_status_present(self):
        """判断某条消息,消息发送失败“！”标致是否存在"""
        return self._is_element_present(self.__locators['消息发送失败感叹号'])

    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        time.sleep(2)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def look_detail_news_by_name(self, name):
        """查看详细消息"""
        self.click_element((MobileBy.XPATH, "//*[@text='%s']" % name))

    @TestLogger.log()
    def click_msg_by_content(self, text):
        """点击消息"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_content" and @text="%s"]' % text))

    @TestLogger.log('判断该页面是否有元素')
    def page_contain_element(self, locator):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log("判断消息列表的消息是否包含省略号")
    def msg_is_contain_ellipsis(self):
        contents = []
        els = self.get_elements(self.__locators['消息简要内容'])
        for el in els:
            contents.append(el.text)
        for msg in contents:
            if "…" in msg:
                return True
        raise AssertionError("消息列表的消息无省略号")

    @TestLogger.log("判断消息列表的消息是否包含省略号")
    def msg_is_contain_text(self, text):
        contents = []
        els = self.get_elements(self.__locators['消息简要内容'])
        for el in els:
            contents.append(el.text)
        for msg in contents:
            if text in msg:
                return True
        raise AssertionError("消息列表的消息无指定文本")

    @TestLogger.log()
    def click_set_message(self, locator):
        """点击已发文件类型"""
        self.click_element(self.__locators[locator])

    @TestLogger.log()
    def choose_chat_by_name(self, name, max_try=20):
        """通过名字选择一个聊天"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def choose_enter_chat(self, name):
        """通过名字选择一个聊天"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_workbench(self):
        """点击工作台"""
        self.click_element(self.__class__.__locators["工作台"])

    @TestLogger.log()
    def search_box_is_enabled(self):
        """页面搜索框是否可点击"""
        return self._is_enabled(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def add_icon_is_enabled(self):
        """+号图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["+号"])

    @TestLogger.log()
    def is_exist_network_anomaly(self):
        """是否存在网络异常"""
        return self.is_text_present("网络连接异常，请检查你的无线网络设置")

    @TestLogger.log()
    def is_exist_network_anomaly2(self):
        """是否存在网络异常"""
        return self.is_text_present("当前网络不可用，请检查网络设置")

    @TestLogger.log()
    def is_exist_unread_messages(self):
        """是否存在未读消息"""
        els = self.get_elements(self.__class__.__locators["未读消息气泡"])
        return len(els) > 0

    @TestLogger.log()
    def clear_up_unread_messages(self):
        """清空未读消息"""
        els = self.get_elements(self.__class__.__locators["未读消息气泡"])
        rect = els[-1].rect
        x = int(rect["x"]) + int(rect["width"]) / 2
        y = -(int(rect["y"]) - 20)
        TouchAction(self.driver).long_press(els[-1], duration=3000).move_to(els[-1], x,
                                                                            y).wait(3).release().perform()

    @TestLogger.log()
    def wait_for_message_list_load(self, timeout=60, auto_accept_alerts=True):
        """等待消息列表加载"""
        # locator = (MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/btn_cancel" and @text ="以后再说"]')
        # if self._is_element_present(locator):
        #     self.click_element(locator)
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["消息名称"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def clear_fail_in_send_message(self):
        """清除发送失败消息记录"""
        current = 0
        while self._is_element_present(self.__class__.__locators["消息发送失败感叹号"]):
            current += 1
            if current > 5:
                return
            els = self.get_elements(self.__class__.__locators["消息发送失败感叹号"])
            for el in els:
                time.sleep(1)
                self.press(el)
                time.sleep(1)
                self.click_element(self.__class__.__locators["删除聊天"])

    @TestLogger.log()
    def is_exist_search_box(self):
        """是否存在消息搜索框"""
        return self._is_element_present(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def is_exist_add_icon(self):
        """是否存在+号图标"""
        return self._is_element_present(self.__class__.__locators["+号"])

    @TestLogger.log()
    def is_exist_words(self):
        """是否存在页面文案"""
        return self._is_element_present(self.__class__.__locators["页面文案"])

    @TestLogger.log()
    def slide_to_the_top(self):
        """滑到消息记录顶端"""
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["搜索"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 30, 50, 70, 800)

    @TestLogger.log()
    def top_message_recording_by_number(self, number):
        """置顶某一条消息记录"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        name = els[number].text
        self.press(els[number])
        if self._is_element_present(self.__class__.__locators["置顶聊天"]):
            self.click_element(self.__class__.__locators["置顶聊天"])
        else:
            self.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        return name

    @TestLogger.log()
    def cancel_stick_message_recording_by_number(self, number):
        """取消置顶某一条消息记录"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        name = els[number].text
        self.press(els[number])
        if self._is_element_present(self.__class__.__locators["取消置顶"]):
            self.click_element(self.__class__.__locators["取消置顶"])
        else:
            self.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        return name

    @TestLogger.log()
    def get_message_name_by_number(self, number):
        """获取消息名称"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        name = els[number].text
        return name

    @TestLogger.log()
    def is_exist_message_name(self):
        """是否存在消息名称"""
        return self._is_element_present(self.__class__.__locators["消息名称"])

    @TestLogger.log()
    def is_exist_message_record(self):
        """是否存在消息记录"""
        return self._is_element_present(self.__class__.__locators["消息项"])

    @TestLogger.log()
    def is_exist_message_img(self):
        """是否存在消息头像"""
        return self._is_element_present(self.__class__.__locators["消息头像"])

    @TestLogger.log()
    def is_exist_message_time(self):
        """是否存在消息时间"""
        return self._is_element_present(self.__class__.__locators["消息时间"])

    @TestLogger.log()
    def is_exist_the_element(self, content):
        """是否存在指定元素"""
        return self._is_element_present(self.__class__.__locators[content])

    @TestLogger.log()
    def is_exist_message_content(self):
        """是否存在消息内容"""
        return self._is_element_present(self.__class__.__locators["消息简要内容"])

    @TestLogger.log()
    def cancel_message_record_stick(self):
        """取消当前页消息记录所有已置顶"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        for el in els:
            self.press(el)
            if self._is_element_present(self.__class__.__locators["取消置顶"]):
                self.click_element(self.__class__.__locators["取消置顶"])
            else:
                self.tap_coordinate([(100, 20), (100, 60), (100, 100)])

    @TestLogger.log()
    def clear_message_record(self):
        """清空消息列表聊天记录"""
        current = 0
        while self._is_element_present(self.__class__.__locators["消息名称"]):
            current += 1
            if current > 5:
                return
            els = self.get_elements(self.__class__.__locators["消息名称"])
            for el in els:
                self.press(el)
                time.sleep(1)
                if self._is_element_present(self.__class__.__locators["删除聊天"]):
                    self.click_element(self.__class__.__locators["删除聊天"])
                else:
                    self.click_back_by_android()
                    # self.tap_coordinate([(100, 20), (100, 60), (100, 100)])

    @TestLogger.log()
    def is_slide_message_list(self):
        """验证消息列表是否可滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return self._is_element_present(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def message_list_is_exist_name(self, name, max_try=20):
        """消息列表是否存在指定人名称"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                return True
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def delete_message_record_by_name(self, name):
        """删除指定消息记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        time.sleep(2)
        el = self.get_element(locator)
        self.press(el)
        self.click_element(self.__class__.__locators['删除聊天'])

    @TestLogger.log()
    def current_message_list_is_exist_name(self, name):
        """当前消息列表是否存在指定人名称"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_exist_no_disturb_icon(self):
        """是否存在消息免打扰图标"""
        return self._is_element_present(self.__class__.__locators["消息免打扰图标"])

    @TestLogger.log()
    def is_clear_no_disturb_icon(self):
        """拖拽后免打扰图标是否消除"""
        self.swipe_by_direction(self.__class__.__locators["消息免打扰图标"], "up", 800)
        if self._is_element_present(self.__class__.__locators["消息免打扰图标"]):
            return False
        return True

    @TestLogger.log()
    def is_exist_news_red_dot(self):
        """是否存在消息红点"""
        return self._is_element_present(self.__class__.__locators["消息红点"])

    @TestLogger.log()
    def is_clear_news_red_dot(self):
        """拖拽后消息红点是否消除"""
        self.swipe_by_direction(self.__class__.__locators["消息红点"], "up", 800)
        if self._is_element_present(self.__class__.__locators["消息红点"]):
            return False
        return True

    @TestLogger.log()
    def is_message_content_match_file_name(self, file_name):
        """查看刚刚发送消息的窗口消息内容是否显示文件+文件名"""
        els = self.get_elements(self.__class__.__locators["消息简要内容"])
        text = els[0].text
        if "[文件]%s" % file_name in text:
            return True
        return False

    @TestLogger.log()
    def is_message_content_match_picture(self):
        """查看刚刚发送消息的窗口消息内容是否显示图片"""
        els = self.get_elements(self.__class__.__locators["消息简要内容"])
        text = els[0].text
        if "[图片]" in text:
            return True
        return False

    @TestLogger.log()
    def is_message_content_match_video(self):
        """查看刚刚发送消息的窗口消息内容是否显示视频"""

        els = self.get_elements(self.__class__.__locators["消息简要内容"])
        text = els[0].text
        if "[视频]" in text:
            return True
        return False

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def selecting_one_group_press_by_name(self, name):
        """根据群名 长按 群"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        # self.click_element(locator)
        el = self.get_element(locator)
        self.press(el)

    @TestLogger.log()
    def press_groupname_to_do(self, text):
        """弹出框 进行操作 置顶聊天 删除聊天 标为已读"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def selecting_one_group_scroll_by_name(self, name):
        """根据群名 长按 群"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        # self.click_element(locator)
        # el = self.get_element(locator)
        # self.press(el)
        self.swipe_by_direction(locator, "left")

    def selecting_one_group_click_by_name(self, name):
        """根据群名 选择群"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def is_exists_group_by_name(self, name):
        """消息页面是否存在指定群名字会话窗口"""
        locator = (
        MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and contains(@text, "%s")]' % name)
        return self._is_element_present(locator)

    @TestLogger.log('点击全部团队')
    def click_all_team(self):
        """点击全部团队"""
        self.click_element(self.__class__.__locators["全部团队"])

    @TestLogger.log('点击创建团队')
    def click_create_team(self):
        """点击创建团队"""
        self.click_element(self.__class__.__locators["创建团队"])

    @TestLogger.log('获取和飞信号')
    def get_number(self):
        """获取和飞信号"""
        el = self.get_element(self.__class__.__locators["和飞信号"])
        return el.text

    @TestLogger.log("点击页头-消息")
    def click_tag_messages(self):
        self.click_element(self.__locators["页头-消息"])
        time.sleep(1)

    @TestLogger.log('点击我')
    def click_me(self):
        """点击我"""
        self.click_element(self.__class__.__locators["我"])

    @TestLogger.log()
    def click_me_icon(self):
        """点击我"""
        self.click_element(self.__locators['我'])

    @TestLogger.log()
    def click_enter_photo(self):
        self.wait_until(
            condition=lambda d: self.is_text_present('将二维码放入扫描框内,即可自动扫描')
        )
        self.click_element(self.__locators['相册'])

    @TestLogger.log()
    def click_qecode_photo(self):
        self.wait_until(
            condition=lambda d: self.is_text_present('选择图片')
        )
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/album_picture"]')
        aphone_all = self.get_elements(locator)
        aphone_all[0].click()
