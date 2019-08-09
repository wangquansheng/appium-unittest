import time
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from pages import *

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        # one_key.click_read_agreement_detail()
        #
        # # 同意协议
        # agreement = AgreementDetailPage()
        # agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_for_page_load(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()


# class MeMobilehall(TestCase):
#     """我的 - 移动厅模块"""
#
#     def setUp_test_Me_Mobilehall_0001(self):
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_already_in_message_page()
#         pass
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_Me_Mobilehall_0001(self):
#         """001移动厅页面校验"""
#         # Preconditions.make_already_in_message_page()
#         currentpage = MePage()
#         currentpage.open_me_page()
#         currentpage.click_mobile_hall_butten()
#         mg=MeMobileHallPage()
#         mg.assert_enterprise_account_list_is_empty()
#         mg.rallbackto_mobile()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_Me_Mobilehall_0002(self):
#         """003移动厅页面充话费页面校验"""
#         Preconditions.make_already_in_message_page()
#         currentpage = MePage()
#         currentpage.open_me_page()
#         currentpage.click_mobile_hall_butten()
#         mg = MeMobileHallPage()
#         # 进入账号余额详情页面
#         mg.click_mobile_account()
#         ag = MeMobileAccuntPage()
#         # 进入充话费页面
#         ag.click_chargrmobile()
#         cg=MeMobileChargePage()
#         cg.click_contants_mobile()
#         dg=SelectHeContactsDetailPage()
#         dg.select_one_linkman("和飞信电话")
#         cg.input_passwod_text("12345678912345678912345")
#         cg.click_mobile_chargesoon()
#         cg.click_mobile_chargesoon_back()
