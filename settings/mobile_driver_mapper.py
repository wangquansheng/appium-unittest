from library.core.common.supportedmodel import SupportedModel
from mobileimplements import *

MOBILE_DRIVER_CREATORS = {
    SupportedModel.MI6['Model']: lambda kw: MI6(**kw),
    SupportedModel.MEIZU_PRO_6_PLUS['Model']: lambda kw: MXPro6Plus(**kw),
    SupportedModel.RED_MI_NOTE_4X['Model']: lambda kw: RedmiNote4X(**kw),
    SupportedModel.HUAWEI_P20['Model']: lambda kw: HuaweiP20(**kw),
    SupportedModel.HUAWEI_N8['Model']: lambda kw: HuaweiP20(**kw),
}
