"""通用预置条件封装方法"""

import time

from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from pages import *



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


def terminate_app():
    """强制关闭app,退出后台"""
    app_id = current_driver().desired_capability['appPackage']
    current_mobile().termiate_app(app_id)


def force_close_and_launch_app():
    """强制关闭应用，然后重启"""
    terminate_app()
    time.sleep(10)
    current_mobile().launch_app()


def background_app():
    """后台运行"""
    current_mobile().press_home_key()


def launch_app():
    """ 启动应用"""
    current_mobile().launch_app()

