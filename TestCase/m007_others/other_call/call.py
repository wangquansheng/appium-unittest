import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.utils.applicationcache import current_mobile
from pages import ChatAudioPage
from pages import ChatWindowPage
from pages import GrantPemissionsPage
from pages import GroupChatPage
from pages import GroupChatSetFindChatContentPage
from pages import GroupChatSetPage
from pages import GroupNamePage
from pages import SelectContactPage
from pages.call.multipartycall import MultipartyCallPage
from pages.components import ChatNoticeDialog
from pages.components import ContactsSelector
from pages.components import SearchBar
from pages.components.SearchGroup import SearchGroupPage
from pages.message.FreeMsg import FreeMsgPage
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage, MessagePage, SearchPage, LabelGroupingPage, GroupListPage, \
    GroupListSearchPage, LableGroupDetailPage, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, \
     CalllogBannerPage, ContactListSearchPage, CallContactDetailPage, SingleChatPage, ContactDetailsPage\
     , CallTypeSelectPage


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    contacts_name_1 = LoginPreconditions.get_contacts_by_row_linename(0, 'contacts_name')
    telephone_num_1 = LoginPreconditions.get_contacts_by_row_linename(0, 'telephone_num')
    contacts_name_2 = LoginPreconditions.get_contacts_by_row_linename(1, 'contacts_name')
    telephone_num_2 = LoginPreconditions.get_contacts_by_row_linename(1, 'telephone_num')

class MsgAllPrior(TestCase):
    """通话---和飞信电话会控页"""

    @staticmethod
    def setUp_test_call_wangqiong_0057():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0057(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        # contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('联系人3')
        SelectContactsPage().click_one_contact_631('联系人4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))
        time.sleep(3)
        # 接听和飞信电话  为自动接听
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(6)
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0059(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        # contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('联系人3')
        SelectContactsPage().click_one_contact_631('联系人4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))
        time.sleep(5)
        # 接听和飞信电话  为自动接听
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(3)
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(4)
        # 挂断电话返回到通话页面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0063(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        # contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('大佬1')
        SelectContactsPage().click_one_contact_631('大佬2')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 点击多方通话详情
        call_page.click_element((MobileBy.XPATH,
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout[2]'),
                                auto_accept_permission_alert=False)

        time.sleep(3)
        # 再次呼叫并接听和飞信电话
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/call_again'))
        time.sleep(5)
        # 挂断电话
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(3)
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @staticmethod
    def setUp_test_call_wangqiong_0071():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0071(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('联系人3')
                if not b:
                    SelectContactsPage().click_one_contact_631('联系人4')
                labellist.click_sure()
        else:
            SelectContactsPage().click_one_contact_631('联系人3')
            SelectContactsPage().click_one_contact_631('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        SelectContactsPage().click_one_contact_631('联系人3')
        SelectContactsPage().click_one_contact_631('联系人4')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0073():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0073(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('联系人3')
                if not b:
                    SelectContactsPage().click_one_contact_631('联系人4')
                labellist.click_sure()
        else:
            SelectContactsPage().click_one_contact_631('联系人3')
            SelectContactsPage().click_one_contact_631('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 进入群发消息界面并点击多方通话

        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_second_colum'),
                                auto_accept_permission_alert=False)
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                                auto_accept_permission_alert=False)
        labellist.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and ' + '@text="多方电话"]'))
        time.sleep(3)
        SelectContactsPage().click_one_contact_631('联系人3')
        SelectContactsPage().click_one_contact_631('联系人4')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0080():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0080(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("联系人3")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '联系人3')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0081():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18351994357')
        contactspage.create_contacts_if_not_exits('联系人4', '18351994307')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0081(self):
        """ 通讯录界面搜索姓名"""
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("联系人")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '联系人3')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0086():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0086(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("18311111111")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18311111111')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))
        call_page.click_back()
        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('18311111111')
        self.assertTrue(current_mobile().is_text_present('联系人3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="联系人3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0087():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0087(self):
        # 通讯录界面搜索姓名
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '1')
        call_page.hide_keyboard()

        # 输入11位数字进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18311111111')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))
        # 点击搜素到的结果
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))

        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('18311111111')
        self.assertTrue(current_mobile().is_text_present('联系人3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="联系人3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0088():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0088(self):
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18312345678')
        call_page.hide_keyboard()

        # 校验是否搜索到未知号码
        SelectContactsPage().is_present_unknown_member()
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="18312345678(未知号码)"]'))
        time.sleep(3)
        call_page.click_back()

    @staticmethod
    def setUp_test_call_wangqiong_0119():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0119(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('联系人3')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0120():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0120(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('联系人')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0126():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0126(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('18311111111')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0127():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0127(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        # 输入9位数 查看是否正匹配到数据
        contact_search.input_search_keyword('18311111')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0145(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('联系人3')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        time.sleep(4)
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(2)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' +
                                       '@text="联系人3"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0146(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')
        contactspage.create_contacts_if_not_exits('联系人2', '18323456789')
        contactspage.create_contacts_if_not_exits('联系人3', '13812345678')
        contactspage.create_contacts_if_not_exits('联系人4', '13823456789')
        contactspage.create_contacts_if_not_exits('联系人5', '13811111111')
        contactspage.create_contacts_if_not_exits('联系人6', '13822222222')
        contactspage.create_contacts_if_not_exits('联系人7', '13833333333')
        contactspage.create_contacts_if_not_exits('联系人8', '13844444444')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('联系人2')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人2"]'))
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人3"]'))
        selectcontacts.search('联系人4')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人4"]'))
        selectcontacts.search('联系人5')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人5"]'))
        selectcontacts.search('联系人6')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人6"]'))
        selectcontacts.search('联系人7')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人7"]'))
        selectcontacts.search('联系人8')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人8"]'))
        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(3)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0147(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        time.sleep(4)
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('18311111111')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18322222222')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333333')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333333')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18344444444')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18355555555')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18366666666')
        selectcontacts.click_unknown_member()

        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(4)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @staticmethod
    def setUp_test_call_wangqiong_0155():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入群聊分组页签
        contactspage.open_group_chat_list()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0155(self):
        # 创建标签分组
        grouppage = GroupListPage()
        # 创建群聊1
        grouppage.create_group_chats_if_not_exits('群聊1', ["联系人3", "联系人4"])
        # 进入群聊的多方电话
        grouppage.click_group('群聊1')
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方电话']"))

        # 选择成员进行多方电话

        time.sleep(10)

    @staticmethod
    def setUp_test_call_wangqiong_0157():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入群聊分组页签
        contactspage.open_group_chat_list()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0157(self):
        # 创建标签分组
        grouppage = GroupListPage()
        # 创建群聊1
        grouppage.create_group_chats_if_not_exits('群聊1', ["联系人3", "联系人4"])
        # 进入群聊的多方电话
        grouppage.click_search_input()
        groupserch = GroupListSearchPage()
        groupserch.input_search_keyword('群聊1')
        # 点击群聊1
        groupserch.click_group('群聊1')
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方电话']"))

        contactselect = ContactsSelector()
        # 选择自己进行多方电话,弹框该联系人不可选择,呼叫按钮任然置灰
        contactselect.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/index_text'))
        current_mobile().assert_element_should_be_disabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

    @staticmethod
    def setUp_test_call_wangqiong_0171():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits('A联系人', '18311111111')
        # contactspage.create_contacts_if_not_exits('B联系人', '18322222222')
        # contactspage.create_contacts_if_not_exits('C联系人', '18333333333')
        # contactspage.create_contacts_if_not_exits('D联系人', '18344444444')
        # contactspage.create_contacts_if_not_exits('E联系人', '18355555555')
        # contactspage.create_contacts_if_not_exits('F联系人', '18366666666')
        # contactspage.create_contacts_if_not_exits('G联系人', '18377777777')
        # contactspage.create_contacts_if_not_exits('H联系人', '18388888888')
        # contactspage.create_contacts_if_not_exits('I联系人', '18399999999')
        # contactspage.create_contacts_if_not_exits('J联系人', '13822222222')
        # contactspage.create_contacts_if_not_exits('K联系人', '13811111111')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0171(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组A')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组A')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('联系人3')
                if not b:
                    SelectContactsPage().click_one_contact_631('联系人4')
                labellist.click_sure()

        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.create_group('分组A', ["A联系人", "B联系人", "C联系人"])
        # labellist.create_group('分组A', ['A联系人', 'B联系人', 'C联系人', 'D联系人', 'E联系人', 'F联系人', 'G联系人', 'H联系人', 'I联系人', 'J联系人', 'K联系人'])
        labellist.click_label_group('分组A')
        # 进入多方通话
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        # 查看时长
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs: id/multi_time_tip'))
        self.assertTrue(labellist.is_text_present((MobileBy.XPATH, '//*[contains(@text, "分钟")]')))

        # 按照字母滑动
        contact = ContactsPage()
        contact.click_element(
            ('xpath', '//*[@resource-id="com.chinasofti.rcs:id/indexbarview"]'))
        elements = contact.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'))
        for i in range(len(elements)):
            elements[i].click()
        # 判断右侧字符是否按顺序排列
        current_mobile().is_right_letters_sorted()

    @staticmethod
    def setUp_test_call_wangqiong_0179():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0179(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('联系人3')
                if not b:
                    SelectContactsPage().click_one_contact_631('联系人4')
                labellist.click_sure()
        else:
            # 新建分组 选择分组成员
            SelectContactsPage().click_one_contact_631('联系人3')
            SelectContactsPage().click_one_contact_631('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 点击多方电话
        labeldeatilpage = LableGroupDetailPage()
        labeldeatilpage.click_multi_tel()

        # 通过11位号码选择联系人 看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage

        selectpage = SelectLocalContactsPage()
        selectpage.search('18311111111')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0180():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0180(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                SelectContactsPage().click_one_contact_631('联系人3')
            if not b:
                SelectContactsPage().click_one_contact_631('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入1位数 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('1')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0181():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0181(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                SelectContactsPage().click_one_contact_631('联系人3')
            if not b:
                SelectContactsPage().click_one_contact_631('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入全名 查看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人3')
        time.sleep(3)
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0182():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0182(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                SelectContactsPage().click_one_contact_631('联系人3')
            if not b:
                SelectContactsPage().click_one_contact_631('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入非全名 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0193():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0193(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_element((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"))
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
            callcontact.get_source()
        if not callcontact._is_element_present((MobileBy.XPATH, "//*[contains(@text, '我')]")):
            callcontact.click_element((MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'), 1,
                                      False)

        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(6)
        callpage = CallPage()
        callpage.hang_up_hefeixin_call()
        time.sleep(3)
        #
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @staticmethod
    def setUp_test_call_wangqiong_0033():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0033(self):
        """本网用户各和飞信电话入口，可成功发起呼叫"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        # 1.在通讯录（群聊、单聊/标签分组）profile页，点击：和飞信电话（免费），发起呼叫（呼叫成功后挂断）
        contactspage.click_search_box()
        contact = ContactListSearchPage()
        contact.input_search_keyword(contactname1)
        contact.click_contact(contactname1)
        # 点击和飞信电话,呼叫成功后挂断
        callcontactdetail = CallContactDetailPage()
        callcontactdetail.call_fetion_call()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断和飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()
        time.sleep(2)
        # 2.在通讯录（群聊、单聊/标签分组）profile页，进入消息页面发起和飞信电话
        callcontactdetail.click_normal_message()
        # 存在用户须知？ 存在则同意
        time.sleep(2)
        from pages.components import ChatNoticeDialog
        chatnotice = ChatNoticeDialog()
        if chatnotice.is_exist_tips():
            chatnotice.accept_and_close_tips_alert()
        singlechat = SingleChatPage()
        time.sleep(2)
        singlechat.click_action_call()
        singlechat.click_hefeixinfree_call_631()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断和飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()
        time.sleep(2)
        # 返回到联系页面
        singlechat.click_back()
        contactdetail = ContactDetailsPage()
        contactdetail.click_back_icon()
        # 返回到联系人页面
        contact.click_back()
        time.sleep(2)

        # 3.进入通话页签 输入数字进行拨打和飞信电话
        Preconditions.enter_call_page()

        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击拨号键，输入号码并拨打,选择'和飞信电话（免费）'
        callpage.click_call()
        callpage.dial_number('18311111111')
        time.sleep(2)
        callpage.click_call_phone()
        calltype = CallTypeSelectPage()
        calltype.click_call_by_app_631()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断和飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()
        time.sleep(2)
        callpage.click_call()

        # Checkpoint：拨打的通话记录为飞信通话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(5)
        callpage.click_ganggang_call_time()
        # 查看详情页面是否是飞信电话？
        time.sleep(5)
        callpage.is_hefeixin_page('飞信电话')

    @staticmethod
    def setUp_test_call_wangqiong_0172():
        """标签分组-多方电话选择器-支持组员名称号码搜索"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        contactname4 = Preconditions.contacts_name_4
        contactnum4 = Preconditions.telephone_num_4
        contactname5 = Preconditions.contacts_name_5
        contactnum5 = Preconditions.telephone_num_5
        contactname6 = Preconditions.contacts_name_6
        contactnum6 = Preconditions.telephone_num_6
        contactname7 = Preconditions.contacts_name_7
        contactnum7 = Preconditions.telephone_num_7
        contactname8 = Preconditions.contacts_name_8
        contactnum8 = Preconditions.telephone_num_8
        contactname9 = Preconditions.contacts_name_9
        contactnum9 = Preconditions.telephone_num_9
        contactname10 = Preconditions.contacts_name_10
        contactnum10 = Preconditions.telephone_num_10
        contactname11 = Preconditions.contacts_name_11
        contactnum11 = Preconditions.telephone_num_11
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)
        contactspage.create_contacts_if_not_exits_631(contactname4, contactnum4)
        contactspage.create_contacts_if_not_exits_631(contactname5, contactnum5)
        contactspage.create_contacts_if_not_exits_631(contactname6, contactnum6)
        contactspage.create_contacts_if_not_exits_631(contactname7, contactnum7)
        contactspage.create_contacts_if_not_exits_631(contactname8, contactnum8)
        contactspage.create_contacts_if_not_exits_631(contactname9, contactnum9)
        contactspage.create_contacts_if_not_exits_631(contactname10, contactnum10)
        contactspage.create_contacts_if_not_exits_631(contactname11, contactnum11)
        # 进入标签分组页签
        contactspage.click_label_grouping_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0172(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        # 存在老的分组 则删除
        labellist.delete_label_groups('分组A')
        time.sleep(2)
        labellist.create_group('分组A', Preconditions.contacts_name_1, Preconditions.contacts_name_2,
                               Preconditions.contacts_name_3, Preconditions.contacts_name_4, Preconditions.contacts_name_5,
                               Preconditions.contacts_name_6, Preconditions.contacts_name_7, Preconditions.contacts_name_8,
                               Preconditions.contacts_name_9, Preconditions.contacts_name_10, Preconditions.contacts_name_11)
        labellist.click_label_group('分组A')
        # 选择成员进行多方通话
        labellist.click_third_image_call()
        # CheckPoint： 选择成员成功发起呼叫
        labellist.select_local_contacts(Preconditions.contacts_name_1, Preconditions.contacts_name_2)
        # 存在悬浮权限提醒，暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断多方通话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_call_wangqiong_0194():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0194(self):
        """多方电话联系人选择器支持搜索正确陌生内地固号"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        # callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 点击搜索框搜索联系人 查看搜索结果，点击呼叫
        contactselect = SelectContactsPage()
        contactselect.search('+860206631888')
        # checkpoint： 查看+860206631888 匹配结果，没有匹配结果
        contactselect.page_should_not_contain_text('未知号码')
        # 清空搜索栏
        contactselect.clear_serchbar_keyword()
        # checkpoint： 搜索0206631885 查看匹配结果“未知号码”、并点击呼叫
        contactselect.search('0206631885')
        contactselect.is_present_unknown_member()
        contactselect.click_unknown_member()
        # 呼叫
        time.sleep(2)
        contactselect.click_sure_bottom()
        # 是否存在‘我知道了’ ，点击
        time.sleep(2)
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()

        # checkpoint: 可以正常可以挂断飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0204():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0204(self):
        """网络信号正常，发起多方电话流程正常"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2, contactname3)
        #  调试用，可删除
        # contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前页面是否是系统通话页面 如果是返回到主界面
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，未接听前，联系人状态为呼叫中
        callpage.click_back_to_call_631()
        time.sleep(2)
        # 当前页面呼叫人状态为‘呼叫中’
        multipage = MultipartyCallPage()
        multipage.assert_caller_status_is_display()
        # 挂断和飞信
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0210():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0210(self):
        """多方电话呼叫中---网络正常下，会控界面显示正常"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2, contactname3)
        # 调试用，可删除
        # contactselect.select_local_contacts(contactname1)

        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，未接听前，联系人状态为呼叫中
        callpage.click_back_to_call_631()
        time.sleep(1)
        # Checkpoint：1.当前页面呼叫人状态为‘呼叫中’
        multipage = MultipartyCallPage()
        multipage.assert_caller_status_is_display()
        # Checkpoint：2.右上角存在隐藏符号
        multipage.assert_hide_icon_is_display()
        # Checkpoint：3.+号展示最多9人
        multipage.assert_caller_max_count_is_display()
        # Checkpoint：4.展示我（主叫）
        multipage.assert_caller_me_is_display()
        time.sleep(1)
        # 挂断和飞信
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0211():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0211(self):
        """多方电话呼叫中时--网络正常下，会控界面点击顶部可返回至系统通话页"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2, contactname3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前页面是否是系统通话页面 如果是返回手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，未接听前，联系人状态为呼叫中
        callpage.click_back_to_call_631()
        time.sleep(1)
        # 当前页面呼叫人状态为‘呼叫中’
        multipage = MultipartyCallPage()
        multipage.assert_caller_status_is_display()
        # 挂断和飞信
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0262():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0262(self):
        """会控界面：“未接听”状态的成员，可支持重新拨号、移除成员、取消成功"""
        """前置条件：保证contactnum1为真实号码 ，contactnum2为非真实现网手机"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631('联系人2', '18311111111')

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search(contactname1)
        selectcontacts.click_contact_by_name(contactname1)
        selectcontacts.search('联系人2')
        selectcontacts.click_contact_by_name('联系人2')
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 判断当前是否在系统通话界面,是的话进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        time.sleep(2)
        # checkpoint1：点击未接通 展示页面含有未接通
        multipage = MultipartyCallPage()
        multipage.click_not_access()
        multipage.page_should_contain_text('联系人2 未接通')
        # checkpoint2: 点击取消,回收弹框
        multipage.click_cancel()
        multipage.page_should_not_contain_text('联系人2 未接通')
        # checkpoint3: 再次点击未接通,点击重新呼叫，回到会控页面，且联系人2状态变为呼叫中
        multipage.click_not_access()
        multipage.click_call_again()

        # checkpoint3: 点击取消
        multipage.click_not_access()
        multipage.click_cancel()

    @staticmethod
    def setUp_test_call_wangqiong_0266():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0266(self):
        """发起多方电话呼叫邀请中，可点击会控界面挂断按钮，结束多方电话通话"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search(contactname1)
        selectcontacts.click_contact_by_name(contactname1)
        selectcontacts.search(contactname2)
        selectcontacts.click_contact_by_name(contactname2)
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 判断当前是否在系统通话界面,是的话进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        time.sleep(2)
        # checkpoint1：会控页面飞信电话挂断，系统电话也挂断
        callpage.hang_up_hefeixin_call_631()
        time.sleep(6)
        message = MessagePage()
        self.assertTrue(message.is_on_this_page())

    @staticmethod
    def setUp_test_call_wangqiong_0267():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0267(self):
        """发起多方电话呼叫邀请中，可点击系统电话挂断，结束多方电话通话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话图标
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前页面是否是系统通话页面 如果是挂断，多方通话一起挂断，返回到通话页签
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 挂断之后回到通话页面
        time.sleep(2)
        callpage.hang_up_the_call()
        time.sleep(5)
        self.assertTrue(callpage.is_on_the_call_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0288(self):
        """多人的多方电话--通话记录详情页各信息显示正常。"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信电话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是多方电话？
        callpage.is_hefeixin_page('飞信电话')
        time.sleep(3)
        # Checkpoint：详情页是否有‘再次呼叫’、‘一键建群’
        self.assertTrue(callpage.page_should_contain_text('再次呼叫'))
        self.assertTrue(callpage.page_should_contain_text('一键建群'))

    @staticmethod
    def setUp_test_call_wangqiong_0289():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0289(self):
        """发起1人的多方电话--通话记录详情页各信息显示正常。"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话图标
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信电话通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是和飞信电话？
        callpage.is_hefeixin_page('飞信电话')
        time.sleep(3)
        # Checkpoint：详情页是否有‘再次呼叫’
        self.assertTrue(callpage.page_should_contain_text('再次呼叫'))

    @staticmethod
    def setUp_test_call_wangqiong_0291():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0291(self):
        """多方通话记录详情页--再次呼叫，网络正常重新呼叫多方电话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为多方电话 进入通话详情页，标题为多方电话通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是多方电话？
        callpage.is_hefeixin_page('飞信电话')

        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前是否是和飞信通话会控页
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0292():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0292(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.is_hefeixin_page('飞信电话')

        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前是否是和飞信通话会控页
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0282():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('Aweqwqw', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0282(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('Aweqwqw')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('Aweqwqw'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0283():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0283(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('fFOWEPQPW')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0289():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0289(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('84949498416418')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0290():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试!@#测试', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0290(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('测试!@#测试')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('测试!@#测试'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0284():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('带空格  的群组', "测试短信1", "测试短信2")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0284(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('带空格  的群组')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('带空格  的群组'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0285():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0285(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('测  试  空  格')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0291():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0291(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('测试%^&%&*飞')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')


    @staticmethod
    def setUp_test_msg_xiaoqiu_0400():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_631('测试群组1', "测试短信1", "测试短信2")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0400(self):
        """验证群主A或群成员B在设置页面——点击+邀请群成员C后——发起人收到的群消息"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在群会话窗口页面
        mess = MessagePage()
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        # Step 1、群主A或群成员吧在群设置页面点击+添加C
        GroupChatSetPage().click_add_number2()
        # Checkpoint 跳转到联系人选择器页面
        # Step 任意选中一个联系人，点击右上角的确定按钮
        ContactsSelector().select_local_contacts('测试短信1')
        # Step A或B返回到会话窗口页面查看
        time.sleep(2)
        # Checkpoint 收到群消息：你向C发出群邀请
        mess.page_should_contain_text("你向 测试短信1... 发出群邀请")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0286():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('12321431413', "测试短信1", "测试短信2")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0286(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('12321431413')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('12321431413'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0402():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.delete_group_if_exist('测试群组88')


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0402(self):
        """验证群主A点击消息列表右上角的+——发起群聊/点对点建群/点击通讯录右上角，创建群后A收到的群消息"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在群会话窗口页面
        mess = MessagePage()
        # Step 1、A选择联系人后进行创建群
        mess.click_add_icon()
        mess.click_group_chat()
        select_cont = SelectContactsPage()
        # Step 选择手机联系人
        select_cont.select_local_contacts()
        ContactsSelector().click_local_contacts('测试短信1')
        ContactsSelector().click_local_contacts('测试短信2')
        select_cont.click_sure_bottom()
        # Checkpoint 跳转到群名称设置页面
        GroupNamePage().wait_for_page_load_631()
        groupname = GroupNamePage()
        groupname.wait_for_page_load_631()
        groupname.clear_input_group_name()
        groupname.input_group_name_631('测试群组88')
        groupname.click_sure()
        # Step  A返回到会话窗口页面查看群消息
        GroupChatPage().wait_for_page_load()
        # Checkpoint 群消息显示：你向“XX, XX, XX...”发出群邀请（逗号为中文字符；提示语姓名不加双引号，前后用空格；...省略号后加一个空格）
        GroupChatPage().page_should_contain_text('你向 +86138********,+86138********... 发出群邀请')


    @staticmethod
    def setUp_test_msg_xiaoqiu_0404():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0404(self):
        """在全局搜索搜索群聊时——点击进入到群会话窗口——群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在消息列表页面
        mess = MessagePage()
        # Step 1、在消息列表页点击全局搜索框，进行群聊搜索
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0405():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.delete_group_if_exist('测试群组88')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0405(self):
        """在点击消息列表右上角的+，选择发起群聊，新成功创建的群会话窗口和群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在群会话窗口页面
        mess = MessagePage()
        # Step 1、在消息列表页点击右上角的+选择发起群聊进行建群
        mess.click_add_icon()
        mess.click_group_chat()
        select_cont = SelectContactsPage()
        select_cont.select_local_contacts()
        ContactsSelector().click_local_contacts('测试短信1')
        ContactsSelector().click_local_contacts('测试短信2')
        select_cont.click_sure_bottom()
        GroupNamePage().wait_for_page_load_631()
        groupname = GroupNamePage()
        groupname.wait_for_page_load_631()
        groupname.clear_input_group_name()
        groupname.input_group_name_631('测试群组88')
        groupname.click_sure()
        # Checkpoint 1、建群成功返回到会话窗口页面
        GroupChatPage().wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        GroupChatPage().click_setting()
        # Checkpoint 2、进入到群设置页面
        GroupChatSetPage().wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0406():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0406(self):
        """在点击消息列表右上角的+，选择发起群聊选择已有群进入到群会话窗口和群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在消息列表页面
        mess = MessagePage()
        # Step 1、在消息列表页点击右上角的+选择发起群聊，选择已有群，点击任意群聊
        mess.click_add_icon()
        mess.click_group_chat()
        select_cont = SelectContactsPage()
        select_cont.click_select_one_group()
        SearchGroupPage().click_group('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # Checkpoint 1、进入会话窗口页面
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0408():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0408(self):
        """点击通讯录——点击群聊——任意选中一个群——进入到群会话窗口和群设置页面"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在通讯录群聊页面
        # Step 1、在群聊页面点击任意群聊
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        SearchGroupPage().click_group('测试群组1')
        groupchat = GroupChatPage()
        # Checkpoint 1、进入会话窗口页面
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        GroupChatSetPage().wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0409():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])
        Preconditions.delete_group_if_exist('测试群组88')


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0409(self):
        """点击通讯录——点击群聊——点击右上角创建群聊按钮——进入到会话窗口和群设置页面"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前通讯录群聊页面
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_create_group()
        # Step 选择手机联系人
        select_cont = SelectContactsPage()
        select_cont.select_local_contacts()
        ContactsSelector().click_local_contacts('测试短信1')
        select_cont.click_back()
        select_cont.click_search_keyword()
        select_cont.input_search_keyword('13901390144')
        select_cont.select_one_contact_by_name('13901390144(未知号码)')
        select_cont.click_sure_bottom()
        # Checkpoint 跳转到群名称设置页面
        groupname = GroupNamePage()
        groupname.wait_for_page_load_631()
        groupname.clear_input_group_name()
        groupname.input_group_name_631('测试群组88')
        groupname.click_sure()
        # Checkpoint 可以创建普通群聊成功
        GroupChatPage().wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        GroupChatPage().click_setting()
        # Checkpoint 2、进入到群设置页面
        GroupChatSetPage().wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0534():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0534(self):
        """创建一个普通群"""
        # 1、网络正常
        # 2、已登录和飞信
        # 4、当前用户未创建任何群聊
        mess = MessagePage()
        # Step 使用创建群聊功能，创建1个普通群
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组5', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组5')
        groupchat = GroupChatPage()
        # Checkpoint 可以正常创建一个普通群
        groupchat.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0534():
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # 建群完成以后删除
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_group_manage()
        groupset.wait_exist_and_delete_confirmation_box_load()
        groupset.click_group_manage_disband_button()
        SingleChatPage().click_sure()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0548():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0548(self):
        """ 普通群，分享群聊邀请口令"""
        # 1、网络正常
        # 2、已加入或创建普通群
        # 3、已消除红点
        # 4、群主、群成员
        # 5、仅限大陆本网和异网号码
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 在群聊设置页面，点击邀请微信或QQ好友进群入口
        groupset.click_avetor_qq_wechat_friend()
        # Checkpoint 小于等于15秒内加载成功，弹出：群口令分享弹窗
        groupset.wait_for_share_group_load()
        # Step 点击下次再次按钮
        groupset.click_say_next()
        # Checkpoint 弹窗消失并且返回到群聊设置页面
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0605():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0605(self):
        """开启免打扰后，在聊天页面在输入框输入内容-返回到消息列表页时，该消息列表窗口直接展示：草稿"""
        # 1、当前在群聊（普通群/企业群）会话窗口页面
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 在当前页面点击右上角的设置按钮
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 消息免打扰开启状态
        if not groupset.get_switch_undisturb_status():
            # Checkpoint 2、开启成功
            groupset.click_switch_undisturb()
        groupset.click_back()
        # Step 返回到会话窗口，在输入框中进行输入内容，然后点击左上角的返回按钮
        groupchat.input_text_message('呵呵呵1')
        groupchat.send_text()
        groupchat.input_text_message('呵呵呵2')
        groupchat.click_back()
        SearchPage().click_back_button()
        # Step 查看该消息列表窗口显示
        mess.page_should_contain_text('测试群组1')
        # Checkpoint 该消息列表窗口直接展示：草稿
        mess.page_should_contain_text('[草稿] ')
        mess.page_should_contain_text('呵呵呵2')
        mess.delete_message_record_by_name("测试群组1")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0613():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0613(self):
        """首次创建群聊桌面快捷方式"""
        # 1、手机存在桌面快捷方式权限
        # 2、已开启此权限或者此权限默认为开启状态
        # 3、登录和飞信
        # 4、进入到群聊设置页面
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset = GroupChatSetPage()
        # Step 点击创建桌面快捷方式入口，弹窗展示
        groupset.click_add_destop_link()
        # Checkpoint 弹窗内容展示为，标题：已尝试添加桌面，内容：若添加失败，请在手机系统设置中，为和飞信打开“创建桌面快捷方式”的权限，复选框选择项：不再提醒，可点击按钮我知道了
        groupset.check_element_for_add_destop_link()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0614():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0614(self):
        """首次创建群聊桌面快捷方式"""
        # 1、手机存在桌面快捷方式权限
        # 2、已开启此权限或者此权限默认为开启状态
        # 3、登录和飞信
        # 4、进入到群聊设置页面
        # 5、不勾选弹窗中复选框
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")

        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset = GroupChatSetPage()
        # Step 点击创建桌面快捷方式入口，弹窗展示
        groupset.click_add_destop_link()
        # Step 不勾选弹窗复选框，点击：我知道了
        groupset.check_element_for_add_destop_link()
        groupset.click_iknow_but()
        # Step 3、重复进行1，2.步骤
        groupset.click_add_destop_link()
        # Checkpoint 桌面快捷方式创建成功校验
        groupset.check_element_for_add_destop_link()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0427():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        # Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0427(self):
        """聊天会话页面——长按——撤回——发送失败的文本消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，存在发送失败的消息
        # 5、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        mess.search_and_enter('测试群组1')
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()

        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        time.sleep(60)
        single.press_mess("测试一个呵呵")
        single.click_recall()
        single.if_exist_i_know_click()
        time.sleep(3)
        # Checkpoint 可以成功撤回此条消息并且在会话窗口展示：你撤回了一条消息
        mess.page_should_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0496():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0496(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        # 点击语音
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'))
        time.sleep(3)
        try:
            ok_buttons = chat_window_page.get_elements(MobileBy.XPATH,
                                                       '//*[@resource-id="android:id/button1" and @text ="允许"]')
            if len(ok_buttons) > 0:
                ok_buttons[0].click()
        except BaseException as e:
            print(e)
        time.sleep(1)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0504():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0504(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_expression()
        time.sleep(3)
        element = chat_window_page.get_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/vp_expression'))
        for i in range(5):
            time.sleep(3)
            expression_images = chat_window_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_expression_image"]'))
            for expression_image in expression_images:
                expression_image.click()
            chat_window_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/vp_expression'), 'left')

        chat_window_page.click_send_button()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0528():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0528(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        # 点击语音
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'))
        time.sleep(3)
        try:
            ok_buttons = chat_window_page.get_elements(MobileBy.XPATH,
                                                       '//*[@resource-id="android:id/button1" and @text ="允许"]')
            if len(ok_buttons) > 0:
                ok_buttons[0].click()
        except BaseException as e:
            print(e)
        time.sleep(3)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'))
        time.sleep(3)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0531():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0531(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        # 点击语音
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'))
        time.sleep(3)
        try:
            ok_buttons = chat_window_page.get_elements(MobileBy.XPATH,
                                                       '//*[@resource-id="android:id/button1" and @text ="允许"]')
            if len(ok_buttons) > 0:
                ok_buttons[0].click()
        except BaseException as e:
            print(e)
        time.sleep(3)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'))
        time.sleep(11)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0001():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0001(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击新建消息
        mess.click_new_message()
        freemsg = FreeMsgPage()
        select_page = SelectContactPage()
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        # 判断存在选择团队联系人按钮
        freemsg.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择团队联系人"]'))
        # 判断存在手机联系人列表
        freemsg.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0044():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0044(self):
        mess = MessagePage()
        mess.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0001():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0001(self):
        mess = MessagePage()
        mess.assert_search_box_is_display()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0006():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('转发短信1', '13800138112')
        contactspage.create_contacts_if_not_exits('转发短信2', '13800138113')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0006(self):
        mess = MessagePage()
        mess.click_search()
        searchbar = SearchBar()
        searchbar.input_search_keyword('转发短信1')
        search = SearchPage()
        search.assert_contact_name_display('转发短信1')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0007():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('转发短信1', '13800138112')
        contactspage.create_contacts_if_not_exits('转发短信2', '13800138113')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0007(self):
        mess = MessagePage()
        mess.click_search()
        searchbar = SearchBar()
        searchbar.input_search_keyword('转发')
        search = SearchPage()
        search.assert_contact_name_display('转发短信1')
        search.assert_contact_name_display('转发短信2')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0433():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0433(self):
        """聊天会话页面——长按——撤回——不足一分钟的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        # 5、存在发送成功时间，小于1分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(1)
        # Step 1、长按发送成功的消息
        groupchat.press_voice_message()
        # Checkpoint 弹出的功能列表中，存在撤回功能
        groupchat.click_recall()
        groupchat.if_exist_i_know_click()
        time.sleep(3)
        # Checkpoint 可以成功撤回此条消息并且在会话窗口展示：你撤回了一条消息
        mess.page_should_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0434():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0434(self):
        """聊天会话页面——长按撤回——超过一分钟的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        # 5、存在发送成功时间，小于1分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(60)
        # Step 1、长按发送成功的消息
        groupchat.press_voice_message()
        # Checkpoint 弹出的功能列表中，存在撤回功能
        groupchat.click_recall()
        groupchat.if_exist_i_know_click()
        time.sleep(3)
        # Checkpoint 可以成功撤回此条消息并且在会话窗口展示：你撤回了一条消息
        mess.page_should_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0436():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0436(self):
        """聊天会话页面——长按撤回——大于10分钟的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        # 5、存在发送成功时间，小于1分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        time.sleep(3)
        chataudio.click_send_bottom()
        a = 10 * 60
        while a > 0:
            time.sleep(1)
            a -= 1
        time.sleep(2)
        # Step 1、长按发送成功的消息
        groupchat.press_voice_message()
        # Checkpoint 不可以成功此条消息（超过10分钟的消息，不能被撤回）
        mess.page_should_not_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0439():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0439(self):
        """聊天会话页面——长按——不支持撤回的消息体"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，
        # 5、存在发送成功时间小于10分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        current_mobile().set_network_status(1)
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(1)
        # Step 1、长按发送失败的消息
        groupchat.press_voice_message()
        # Checkpoint 2、弹出的功能列表中，不存在撤回功能（发送失败的消息，不允许进行撤回操作）
        mess.page_should_not_contain_text('撤回')

    def tearDown_msg_xiaoqiu_0439(self):
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0440():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0440(self):
        """聊天会话页面——在10分钟内长按——弹出功能菜单列表——10分钟后撤回"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，
        # 5、存在发送成功时间小于10分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_input_box()
        # Step 1、成功发送一条消息
        groupchat.input_text_message('测试撤回了')
        groupchat.send_text()
        # Step 2、在10分钟内，长按弹出功能菜单列表
        groupchat.press_text_message()
        # Checkpoint 2、在10分钟内，长按弹出功能菜单列表
        mess.page_should_contain_text('撤回')
        # Step 3、在超过10分钟后，点击撤回功能，是否可以撤回此条消息
        a = 10 * 60
        while a > 0:
            time.sleep(1)
            a -= 1
        time.sleep(2)
        groupchat.click_recall()
        groupchat.if_exist_i_know_click()
        # Checkpoint 3、在超过10分钟后，点击撤回功能，不可以撤回此条消息
        mess.page_should_not_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0441():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0441(self):
        """（普通消息体）聊天会话页面——5分钟内——连续发送文本消息体"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_input_box()
        # Step 1、5分钟内，发送方连续发送文本消息，是否不出现重复头像，消息聚合展示
        groupchat.input_text_message('测试聚合消息1')
        groupchat.send_text()
        groupchat.input_text_message('测试聚合消息2')
        groupchat.send_text()
        # Checkpoint 不出现重复头像，消息聚合展示
        self.assertTrue(groupchat.is_multi_show())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0465():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0465(self):
        """查找聊天内容页-选择搜索结果-定位到的搜索结果展示页-输入框会自动填充上一次发送出去的内容"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、已加入普通群
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_input_box()
        # Step 1、在群聊会话页，发送一条消息
        groupchat.input_text_message('测试聚合消息1')
        groupchat.send_text()
        # Step 2、再在输入框中，录入内容
        groupchat.input_text_message('测试聚合消息2')
        # Step 3、去到群聊设置-查找聊天内容——选择搜索结果——定位到搜索结果页
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 在查找聊天内容页面，输入框中，输入中文搜索条件
        search.search('测试聚合消息1')
        # Step 任意选中一条聊天记录
        search.click_search_result('测试聚合消息1')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()
        # Checkpoint 搜索结果展示页的输入框中，不会自动填充内容
        mess.page_should_contain_text('说点什么...')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0469():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        # Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0469(self):
        """在消息列表——长按置顶的会话窗口——检查弹出窗口"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、已加入普通群
        # 4、置顶聊天开关，开启状态（安卓）
        mess = MessagePage()
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        if not groupset.get_chat_set_to_top_switch_status():
            groupset.click_chat_set_to_top_switch()
        groupset.click_back()
        groupchat.click_back()
        ContactListSearchPage().click_back()
        mess.wait_for_page_load()
        # Step 1、在消息列表长按置顶成功的会话窗口，弹出的功能列表中是否存在展示为：取消置顶的功能
        mess.cancel_message_record_stick()
        mess.search_and_enter('测试群组1')
        # Step 2、点击取消置顶，取消置顶成功后，去到群聊设置页面，置顶聊天的开关是否已被关闭
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Checkpoint 置顶聊天的开关已被关闭
        self.assertFalse(groupset.get_chat_set_to_top_switch_status())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0550():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0550(self):
        """普通群，点击口令弹窗的立即分享按钮，分享群口令"""
        # 1、网络正常
        # 2、已加入或创建普通群
        # 3、已消除红点
        # 4、群主、群成员
        # 5、仅限大陆本网和异网号码
        mess = MessagePage()
        # Step 1、在群聊设置页面，群口令生成成功后
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_avetor_qq_wechat_friend()
        # 2、android点击下载再说或者空白处，弹窗是否会消失
        groupset.wait_for_share_group_load()
        groupset.click_say_next()
        # Checkpoint 弹窗消失并且返回到群聊设置页面
        groupset.wait_for_page_load()


