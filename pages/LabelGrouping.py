import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components import ContactsSelector


class LabelGroupingPage(ContactsSelector, BasePage):
    """标签分组页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.group.GroupListActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/label_group_toolbar': (
            MobileBy.ID, 'com.chinasofti.rcs:id/label_group_toolbar'),
        '返回': (MobileBy.XPATH, '//*[contains(@resource-id,"back")]'),
        '页面标题': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_toolbar_title'),

        '分组列表': (MobileBy.ID, 'com.chinasofti.rcs:id/group_list'),
        '分组根节点': (MobileBy.ID, 'com.chinasofti.rcs:id/group_list_item'),
        '分组图标': (MobileBy.ID, 'com.chinasofti.rcs:id/asp_group_icon'),
        '新建分组': (MobileBy.XPATH, '//*[@text="新建分组"]'),
        '分组右侧箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_icon'),
        'com.chinasofti.rcs:id/textView': (MobileBy.ID, 'com.chinasofti.rcs:id/textView'),
        'biao': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
        'mylab(5)': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
        '标签分组名字': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
        '标签分组成员数量': (MobileBy.ID, 'com.chinasofti.rcs:id/group_member_num'),
        # 新建分组页面
        '新建分组页面': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
        '新建分组页面返回': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '为你的分组创建一个名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sub_title'),
        '请输入标签分组名称': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_group_name'),
        '标签人员列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recycleview'),
        '列表': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'),
        # 6.3.1版本
        '飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_third_item'),
        '多方视频': (MobileBy.XPATH, '//*[@text="多方视频"]'),
        '添加成员': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_first_item'),
        '联系人输入': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
    }

    @TestLogger.log('删除全部标签分组')
    def delete_all_label(self):
        """
        一键删除全部分组
        :return:
        """
        from pages import LableGroupDetailPage
        groups = self.get_elements(self.__locators['分组根节点'])[1:]
        while groups:
            groups[0].click()
            # 删除标签
            detail = LableGroupDetailPage()
            try:
                self.click_element(['xpath', '//*[@text="我知道了"]'], 1)
            except:
                pass
            detail.open_setting_menu()
            detail.click_delete_label_menu()
            detail.click_delete()
            self.wait_for_page_load()
            # 刷新group
            groups = self.get_elements(self.__locators['分组根节点'])[1:]

    @TestLogger.log('删除指定分组')
    def delete_label_groups(self, *groups):
        """
        一键批量删除
        :param groups: 要删除的分组名称数组
        :return:
        """
        from pages import LableGroupDetailPage
        for name in groups:
            if isinstance(name,(list,tuple)) and len(name) >0:
                name = name[0]
            if self.click_label_group(name):
                detail = LableGroupDetailPage()
                try:
                    self.click_element(['xpath', '//*[@text="知道了"]'], 1)
                except:
                    pass
                detail.open_setting_menu()
                detail.click_delete_label_menu()
                detail.click_delete()
                self.wait_for_page_load()

    @TestLogger.log('删除指定分组点击取消')
    def cancel_delete_label_groups(self, *groups):
        """
        删除指定分组点击取消
        :param groups: 要删除的分组名称数组
        :return:
        """
        from pages import LableGroupDetailPage
        for name in groups:
            if isinstance(name,(list,tuple)) and len(name) >0:
                name = name[0]
            if self.click_label_group(name):
                detail = LableGroupDetailPage()
                try:
                    self.click_element(['xpath', '//*[@text="知道了"]'], 1)
                except:
                    pass
                detail.open_setting_menu()
                detail.click_delete_label_menu()
                detail.click_cancel()
                self.click_back()
                try:
                    self.click_element(['xpath', '//*[@text="知道了"]'], 1)
                except:
                    pass
                self.click_back()
                self.wait_for_page_load()

    @TestLogger.log('点击分组')
    def click_label_group(self, name):
        """
        点击进入分组
        :param name: 分组名字
        :return:
        """
        import re
        index = 0
        for group in self.mobile.list_iterator(self.__locators['分组列表'], self.__locators['分组根节点']):
            if index < 1:
                index += 1
                continue
            else:
                group_name = group.find_element(*self.__locators['标签分组名字']).text

                # 页面改动，分组名和成员数量已经不是在一个元素的文本里面了
                # result = re.findall(r'(.+)\((\d+)\)$', group_name)[0]
                total_text = group.find_element(*self.__locators['标签分组成员数量']).text
                total = re.findall(r'\d+', total_text)[0]
                # group_name, total = result

                if group_name == name:
                    group.click()
                    return group_name, int(total)
                index += 1
        return

    @TestLogger.log('重命名分组')
    def rename_label_group(self, old_name, new_name):
        """
        重命名分组
        :param old_name: 要修改的分组
        :param new_name: 将赋予的分组名
        :return:
        """
        from pages import LableGroupDetailPage

        if self.click_label_group(old_name):
            detail = LableGroupDetailPage()
            try:
                self.click_element(['xpath', '//*[@text="知道了"]'], 1)
            except:
                pass
            detail.open_setting_menu()
            detail.rename_group_name(new_name)
            import time
            time.sleep(2)
            self.click_back()
            detail.wait_for_page_load()
            actual = detail.get_group_name()
            self.click_back()
            self.wait_for_page_load()
            return actual

    @TestLogger.log('移除成员')
    def remove_group_members(self, group, *members):
        from pages import LableGroupDetailPage

        if self.click_label_group(group):
            detail = LableGroupDetailPage()

            try:
                self.click_element(['xpath', '//*[@text="知道了"]'], 1)
            except:
                pass

            detail.open_setting_menu()
            detail.remove_members(*members)

            self.click_back()

            try:
                self.click_element(['xpath', '//*[@text="知道了"]'], 1)
            except:
                pass

            detail.wait_for_page_load()
            try:
                self.click_element(['xpath', '//*[@text="知道了"]'], 1)
            except:
                pass
            self.click_back()
            self.wait_for_page_load()

    @TestLogger.log('检查空白分组列表默认文案')
    def assert_default_status_is_right(self):
        self.mobile.assert_screen_contain_text('暂无分组')

    @TestLogger.log('获取标签分组成员数量')
    def get_group_member_count(self, name):
        """
        获取标签分组成员数量
        :param name: 分组名字
        :return:
        """
        import re
        index = 0
        for group in self.mobile.list_iterator(self.__locators['分组列表'], self.__locators['分组根节点']):
            if index < 1:
                index += 1
                continue
            else:
                group_name = group.find_element(*self.__locators['标签分组名字']).text

                # 页面改动，分组名和成员数量已经不是在一个元素的文本里面了
                # result = re.findall(r'(.+)\((\d+)\)$', group_name)[0]
                total_text = group.find_element(*self.__locators['标签分组成员数量']).text
                total = re.findall(r'\d+', total_text)[0]
                # group_name, total = result

                if group_name == name:
                    return int(total)
                index += 1
        return

    @TestLogger.log('获取标签分组名字')
    def get_label_grouping_names(self):
        """获取标签分组名字"""
        els = self.get_elements(self.__class__.__locators["标签分组名字"])
        names = []
        for el in els:
            names.append(el.text)
        if "新建分组" in names:
            names.remove("新建分组")
        return names

    @TestLogger.log('点击新建分组')
    def click_new_create_group(self):
        """点击新建分组"""
        self.click_element(self.__class__.__locators["新建分组"])

    @TestLogger.log('选择分组')
    def select_group(self, name):
        """选择分组"""
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % name))

    @TestLogger.log('输入标签分组名称')
    def input_label_grouping_name(self, name):
        """
        输入标签分组名称
        业务规则：
            1、名称长度不能大于30字节
        :param name:传入的分组名
        :return: 实际填入的分组名
        """
        byte_len = len(name.encode())
        if byte_len > 30:
            origin_len = len(name)
            left = ''
            right = ''
            for i in range(origin_len):
                if len(name[:i + 1].encode()) <= 30:
                    left = name[:i + 1]
                    right = name[i + 1:]
                else:
                    break
            print('传入的分组名大于30字节，为防止崩溃，已经自动取小于30字节的部分（{}）输入，舍弃大于30字节部分（{}）'.format(left, right))
            name = left

        self.input_text(self.__locators["请输入标签分组名称"], name)
        actual = self.get_text(self.__locators['请输入标签分组名称'])
        return actual

    @TestLogger.log('点击确定')
    def click_sure(self):
        """点击确定"""
        self.mobile.click_element(self.__locators['确定'])

    @TestLogger.log('等待标签分组页面加载')
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待标签分组页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["页面标题"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log('等待新建标签分组页面加载')
    def wait_for_create_label_grouping_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待新建标签分组页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新建分组页面"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log('创建分组')
    def create_group(self, group_name, *member_list):
        """
        一键创建分组
        :param group_name: 分组名
        :param member_list: 成员列表
        :return:
        """
        self.click_new_create_group()
        self.wait_for_create_label_grouping_page_load()
        actual = self.input_label_grouping_name(group_name)
        self.click_sure()

        if self.is_group_exist_tips_popup():
            print('群组："{}" 已存在'.format(group_name))
            self.click_back()
            return

        # 增加等待步骤，防止点击确定后，系统权限弹窗阻塞下一步操作
        self.wait_for_contacts_selector_page_load()
        if not member_list:
            self.click_back()
            self.click_back()
            return actual
        self.select_local_contacts(*member_list)
        return actual

    @TestLogger.log('创建分组')
    def create_a_group(self, group_name):
        """
        创建分组
        :param group_name: 分组名
        :return:
        """
        self.click_new_create_group()
        self.wait_for_create_label_grouping_page_load()
        self.input_label_grouping_name(group_name)
        self.click_sure()
        if self.is_text_present('群组已存在'):
            self.click_back()
        else:
            self.click_back_by_android(times=2)



    @TestLogger.log('判断点击确定后“群组已存在”提示是否弹出')
    def is_group_exist_tips_popup(self):
        try:
            self.wait_condition_and_listen_unexpected(
                condition=lambda d: self.is_text_present('新建分组'),
                unexpected=lambda: self.get_elements(['xpath', '//*[@text="群组已存在"]']),
            )
            return False
        except AssertionError:
            return True

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('新建分组页面返回')
    def new_group_click_back(self):
        self.click_element(self.__locators['新建分组页面返回'])

    @TestLogger.log()
    def page_contain_title(self):
        """页面应该包含的元素-标题"""
        return self.page_should_contain_element(self.__locators['新建分组页面'])

    @TestLogger.log()
    def page_contain_title(self):
        """页面应该包含的元素-标题"""
        return self.page_should_contain_element(self.__locators['确定'])

    @TestLogger.log()
    def sure_btn_is_clickable(self):
        return self._is_clickable(self.__class__.__locators["确定"])

    @TestLogger.log()
    def is_contacter_in_lable(self, name):
        """人员列表是否在标签中"""
        time.sleep(1)
        groups = self.mobile.list_iterator(self.__locators['标签人员列表'], self.__locators['列表'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log()
    def create_group1(self, group_name, *member_list):
        """
        """
        self.click_new_create_group()
        self.wait_for_create_label_grouping_page_load()
        actual = self.input_label_grouping_name(group_name)
        self.click_sure()

        if self.is_group_exist_tips_popup():
            print('群组："{}" 已存在'.format(group_name))
            self.click_back()
            return

        # 增加等待步骤，防止点击确定后，系统权限弹窗阻塞下一步操作
        self.wait_for_contacts_selector_page_load()
        if not member_list:
            self.click_back()
            self.click_back()
            return actual
        self.select_local_contacts(*member_list)
        return actual

    @TestLogger.log('标签分组详情页点击第三个图标多方通话')
    def click_third_image_call(self):
        self.click_element(self.__locators['飞信电话'])

    @TestLogger.log('选择指定成员进行多方通话')
    def select_number_call(self, *member_list):
        self.click_element(self.__locators['多方电话'])
        from pages import MultiPartyVideoPage
        multiparty = MultiPartyVideoPage()
        member_list = list(member_list)
        # multiparty.input_contact_search(member_list)
        multiparty.click_one_contact(member_list)

    @TestLogger.log('标签分组详情页点击第四个图标多方视频')
    def click_four_image_call(self):
        self.click_element(self.__locators['多方视频'])

    @TestLogger.log('创建分组')
    def create_group_631(self, group_name, *member_list):
        """
        一键创建分组
        :param group_name: 分组名
        :param member_list: 成员列表
        :return:
        """
        self.click_new_create_group()
        self.wait_for_create_label_grouping_page_load()
        actual = self.input_label_grouping_name(group_name)
        self.click_sure()

        # 增加等待步骤，防止点击确定后，系统权限弹窗阻塞下一步操作
        self.wait_for_contacts_selector_page_load()
        if not member_list:
            self.click_back()
            self.click_back()
            return actual
        self.select_local_contacts(*member_list)
        return actual

    @TestLogger.log('点击元素')
    def click_element_c(self, locator, default_timeout=5, auto_accept_permission_alert=True):
        self.click_element(self.__locators[locator], default_timeout=default_timeout, auto_accept_permission_alert=auto_accept_permission_alert)

    @TestLogger.log('创建分组')
    def is_sure(self, locator):
        if self.get_element_attribute(self.__locators[locator], 'enabled') == 'true':
            return True
        return False


