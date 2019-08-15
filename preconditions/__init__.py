"""通用预置条件封装方法"""

from selenium.common.exceptions import TimeoutException
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from pages import *
import time

def connect_mobile(category):
    """选择手机手机"""
    client = switch_to_mobile(category)
    client.connect_mobile()
    return client


def make_already_in_one_key_login_page():
    """
    1、已经进入一键登录页
    :return:
    """
    # 如果当前页面已经是一键登录页，不做任何操作
    one_key = OneKeyLoginPage()
    if one_key.is_on_this_page():
        return

    # 如果当前页不是引导页第一页，重新启动app
    guide_page = GuidePage()
    if not guide_page.is_on_the_first_guide_page():
        current_mobile().launch_app()
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
    permission_list.click_permission_button()
    one_key.wait_for_page_load(30)


def login_by_one_key_login():
    """
    从一键登录页面登录
    :return:
    """
    # 等待号码加载完成后，点击一键登录
    one_key = OneKeyLoginPage()
    one_key.wait_for_tell_number_load(60)
    login_number = one_key.get_login_number()
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
    message_page.wait_login_success(60)
    return login_number


def take_logout_operation_if_already_login():
    """已登录状态，执行登出操作"""
    message_page = MessagePage()
    message_page.wait_for_page_load()
    message_page.open_me_page()

    me = MePage()
    me.scroll_to_bottom()
    me.scroll_to_bottom()
    me.scroll_to_bottom()
    me.click_setting_menu()

    setting = SettingPage()
    setting.scroll_to_bottom()
    setting.click_logout()
    setting.click_ok_of_alert()


def reset_and_relaunch_app():
    """首次启动APP（使用重置APP代替）"""
    app_package = 'com.chinasofti.rcs'
    current_driver().activate_app(app_package)
    current_mobile().reset_app()


def terminate_app():
    """
    强制关闭app,退出后台
    :return:
    """
    app_id = current_driver().desired_capability['appPackage']
    current_mobile().termiate_app(app_id)


def force_close_and_launch_app():
    "强制关闭应用，然后重启"
    terminate_app()
    time.sleep(10)
    current_mobile().launch_app()


def background_app():
    """后台运行"""
    current_mobile().press_home_key()

def launch_app():
#     """ 启动应用"""
     current_mobile().launch_app()


def make_already_in_message_page(reset_required=False):
    """
    前置条件：
    1.已登录客户端
    2.当前在消息页面
    """
    if not reset_required:
        message_page = MessagePage()
        if message_page.is_on_this_page():
            return
        else:
            try:
                current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
            except:
                pass
            current_mobile().launch_app()
        try:
            message_page.wait_until(
                condition=lambda d: message_page.is_on_this_page(),
                timeout=3
            )
            return
        except TimeoutException:
            pass
    reset_and_relaunch_app()
    make_already_in_one_key_login_page()
    login_num = login_by_one_key_login()
    return login_num
