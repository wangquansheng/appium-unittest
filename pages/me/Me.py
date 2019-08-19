from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
import time
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class MePage(FooterPage):
    """ 我 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/titleBar': (MobileBy.ID, 'com.chinasofti.rcs:id/titleBar'),
        '页头-我': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '页脚-我': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvMe" and @selected="true"]'),
        '二维码入口': (MobileBy.ID, 'com.chinasofti.rcs:id/qr_code_imageview'),
        'com.chinasofti.rcs:id/rl_person': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_person'),
        'com.chinasofti.rcs:id/fl_name': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_name'),
        '请完善名片': (MobileBy.ID, 'com.chinasofti.rcs:id/card_name_hint'),
        '电话号码': (MobileBy.ID, 'com.chinasofti.rcs:id/card_photo_num'),
        '查看并编辑个人资料': (MobileBy.ID, 'com.chinasofti.rcs:id/check_user_profile'),
        'com.chinasofti.rcs:id/profile_photo_out': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo_out'),
        '个人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/card_head_photo'),
        'com.chinasofti.rcs:id/layout_for_mall': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_mall'),
        'com.chinasofti.rcs:id/internet_mutil_call_layout_id': (
            MobileBy.ID, 'com.chinasofti.rcs:id/internet_mutil_call_layout_id'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_name_text'),
        '300': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_number_text'),
        '分钟': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_unit'),
        'com.chinasofti.rcs:id/user_money': (MobileBy.ID, 'com.chinasofti.rcs:id/user_money'),
        '账户余额': (MobileBy.ID, 'com.chinasofti.rcs:id/money_name_text'),
        '12.20': (MobileBy.ID, 'com.chinasofti.rcs:id/money_number_text'),
        '元': (MobileBy.ID, 'com.chinasofti.rcs:id/money_unit'),
        'com.chinasofti.rcs:id/layout_flow': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_flow'),
        '可用流量': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_name_text'),
        '40.98': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_number_text'),
        'G': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_unit'),
        'com.chinasofti.rcs:id/redpager': (MobileBy.ID, 'com.chinasofti.rcs:id/redpager'),
        '钱包': (MobileBy.ID, 'com.chinasofti.rcs:id/repager_text'),
        'com.chinasofti.rcs:id/welfare': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare'),
        '福利': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare_text'),
        '多重好礼等你来领': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
        'com.chinasofti.rcs:id/wfSpace': (MobileBy.ID, 'com.chinasofti.rcs:id/wfSpace'),
        'com.chinasofti.rcs:id/welfareArrow': (MobileBy.ID, 'com.chinasofti.rcs:id/welfareArrow'),
        'com.chinasofti.rcs:id/collect': (MobileBy.ID, 'com.chinasofti.rcs:id/collect'),
        '收藏': (MobileBy.ID, 'com.chinasofti.rcs:id/collect_text'),
        'com.chinasofti.rcs:id/about_app': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app'),
        '关于和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app_text'),
        'com.chinasofti.rcs:id/about_right_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/about_right_arrow'),
        'com.chinasofti.rcs:id/share_app': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app'),
        'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
        'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        'com.chinasofti.rcs:id/rnMessageBadge': (MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
        'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground'),
        '推荐好友，赚现金红包': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
        '分享客户端': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app_text'),
        'com.chinasofti.rcs:id/feedback': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback'),
        '帮助与反馈': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback_text'),
        'com.chinasofti.rcs:id/setting': (MobileBy.ID, 'com.chinasofti.rcs:id/setting'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/setting'),
        '移动营业厅': (MobileBy.ID, 'com.chinasofti.rcs:id/onlinehall_text'),
        '姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/card_name'),
        '联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_setting_text'),
        "联系人管理": (MobileBy.ID,'com.chinasofti.rcs:id/manage_contact_text'),
        '取消退出': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定退出': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '和包支付': (MobileBy.ID, 'com.chinasofti.rcs:id/redpager'),
        '和包支付卡片': (MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_name'),
        '请输入银行卡号': (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
        '请输入持卡人姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_userName_edit'),
        '请输入身份证号': (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_idCard'),
        '请输入银行预留手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_mobile'),
        '下一步1': (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'),
        '下一步2': (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_nextBtn'),
        '发红包': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_red_packet_send_btn'),
        '红包金额': (MobileBy.ID, 'com.chinasofti.rcs:id/edt_red_packet_num'),
    }

    @TestLogger.log('点击个人名片头像')
    def click_head(self):
        self.click_element(self.__locators['个人头像'])

    @TestLogger.log()
    def click_hebao_pay(self):
        """点击 和包支付"""
        self._find_menu(self.__locators['和包支付'])
        self.click_element(self.__locators['和包支付'])

    @TestLogger.log()
    def click_hebao_pay_card(self, card):
        """点击 和包支付"""
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % card))

    @TestLogger.log()
    def input_text_cardno(self, message):
        """请输入银行卡号"""
        self.input_text(self.__class__.__locators["请输入银行卡号"], message)
        return self

    @TestLogger.log()
    def input_text_red_packet_num(self, message):
        """红包金额"""
        self.input_text(self.__class__.__locators["红包金额"], message)
        return self

    @TestLogger.log()
    def input_text_card_person_name(self, message):
        """请输入持卡人姓名"""
        self.input_text(self.__class__.__locators["请输入持卡人姓名"], message)
        return self

    @TestLogger.log()
    def input_text_card_id(self, message):
        """请输入身份证号"""
        self.input_text(self.__class__.__locators["请输入身份证号"], message)
        return self

    @TestLogger.log()
    def input_text_phoneno(self, message):
        """请输入银行预留手机号"""
        self.input_text(self.__class__.__locators["请输入银行预留手机号"], message)
        return self

    @TestLogger.log()
    def is_enabled_next_btn(self):
        """下一步1"""
        return self._is_enabled(self.__class__.__locators['下一步1'])

    @TestLogger.log()
    def is_enabled_next_btn2(self):
        """下一步2"""
        return self._is_enabled(self.__class__.__locators['下一步2'])

    @TestLogger.log()
    def is_enabled_red_packet_send(self):
        """发红包"""
        return self._is_enabled(self.__class__.__locators['发红包'])

    @TestLogger.log()
    def is_enabled_sms_send_btn(self):
        """短信发送按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators['短信发送按钮'])

    @TestLogger.log('点击联系人管理')
    def click_manage_contact(self):
        self.click_element(self.__class__.__locators['联系人管理'])

    @TestLogger.log('点击联系人')
    def click_manage_contact2(self):
        self.click_element(self.__class__.__locators['联系人'])
        time.sleep(1)

    @TestLogger.log('发红包')
    def click_red_packet_send(self):
        self.click_element(self.__class__.__locators['发红包'])

    @TestLogger.log('点击确认退出')
    def click_sure_drop(self):
        self.click_element(self.__locators['确定退出'])

    @TestLogger.log()
    def wait_for_head_load(self, timeout=60, auto_accept_alerts=True):
        """等待个人名片头像加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["个人头像"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('点击二维码图标')
    def click_qr_code_icon(self):
        self.click_element(self.__locators['二维码入口'])

    @TestLogger.log('点击移动营业厅')
    def click_mobile_hall_butten(self):
        self.click_element(self.__locators['移动营业厅'])

    @TestLogger.log("点击菜单项")
    def click_menu(self, menu):
        locator = [MobileBy.XPATH, '//*[@text="{}"]'.format(menu)]
        self._find_menu(locator)
        self.click_element(locator)

    @TestLogger.log("回到列表顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        # 如果找到“短信设置”菜单，则当作已经滑到底部
        if self._is_on_the_start_of_menu_view():
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_on_the_start_of_menu_view():
                break
        return True

    @TestLogger.log("滑到菜单底部")
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['页头-我'])
        )

        # 如果找到“设置”菜单，则当作已经滑到底部
        if self._is_on_the_end_of_menu_view():
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_down()
            if self._is_on_the_end_of_menu_view():
                break
        return True

    @TestLogger.log("点击设置菜单")
    def click_setting_menu(self):
        """点击设置菜单"""
        self.scroll_to_bottom()
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['设置'])
        ).click()
        time.sleep(1)

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """判断页面是否包含选中状态的“我”页脚标签"""
        try:
            self.wait_until(
                condition=lambda d: self.get_element(self.__locators['页脚-我']),
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("下一页")
    def page_down(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')

    @TestLogger.log("下一页")
    def page_up(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'down')

    @TestLogger.log()
    def _find_menu(self, locator):
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            max_try = 5
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if self._is_on_the_end_of_menu_view():
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    def _is_on_the_start_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['电话号码'])

    def _is_on_the_end_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['设置'])

    @TestLogger.log()
    def click_help_menu(self, timeout=60):
        """点击帮助与反馈菜单"""
        self.scroll_to_bottom()
        self.wait_until(
            timeout=timeout,
            condition=lambda d: self.get_element(self.__locators['帮助与反馈'])
        ).click()

    @TestLogger.log()
    def click_collection(self):
        """点击收藏按钮"""
        if self._is_element_present(self.__locators['收藏']):
            self.click_element(self.__locators['收藏'])
        else:
            self.page_down()
            self.click_element(self.__locators['收藏'])

    @TestLogger.log()
    def click_collection2(self):
        """点击收藏按钮"""
        self._find_menu(self.__locators['收藏'])
        self.click_element(self.__locators['收藏'])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在我的页面"""
        el = self.get_elements(self.__locators['查看并编辑个人资料'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])

    @TestLogger.log()
    def is_text_exist(self, text):
        """当前页面是否包含此元素"""
        return self.is_text_present(text)

    @TestLogger.log()
    def click_view_edit(self):
        """点击查看并编辑资料按钮"""
        self.click_element(self.__locators['查看并编辑个人资料'])

    @TestLogger.log()
    def wait_for_me_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待我页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["二维码入口"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_call_multiparty(self, timeout=60):
        """点击多方电话"""
        self.wait_until(
            timeout=timeout,
            condition=lambda d: self.get_element(self.__locators['多方电话'])
        ).click()

    @TestLogger.log()
    def click_welfare(self):
        """点击收藏按钮"""
        self.click_element(self.__locators['福利'])

    @TestLogger.log()
    def _find_text_menu(self, locator):
        import time
        if not self.is_text_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            time.sleep(1.5)
            if self.is_text_present(locator):
                return True
            max_try = 5
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                time.sleep(1.5)
                if self.is_text_present(locator):
                    return True
                if self._is_on_the_end_of_menu_view():
                    return False

    @TestLogger.log("点击设置菜单")
    def click_setting_menu_631(self):
        """点击设置菜单"""
        self.click_element(self.__locators['设置'])
