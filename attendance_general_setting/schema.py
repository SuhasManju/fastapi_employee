from pydantic import BaseModel
from typing import Optional,Union,List


class Working_Hours(BaseModel):
    total_hour_calculation:Optional[str]
    minimum_hours_required:Optional[str]
    strict_mode_manual:Optional[bool]=False
    strict_mode_full_day:Optional[str]
    strict_mode_half_day:Optional[str]
    strict_shift_hours_full_day:Optional[str]
    strict_shift_hour_half_day:Optional[str]
    lenient_mode_manual:Optional[bool]=False
    lenient_mode_per_day:Optional[str]
    lenient_mode_shift:Optional[str]
    show_overtime_deveation:Optional[bool]=False
    maximum_hours_required:Optional[bool]=False
    round_off:Optional[bool]=False
    first_check_in:Optional[str]
    last_check_out:Optional[str]
    worked_hours:Optional[str]



class Late_night_work(BaseModel):
    enable_tracking:Optional[bool]=False
    location:Optional[List[str]]
    start_time:Optional[str]
    end_time:Optional[str]
    shift_margin_enable:Optional[bool]=False


class Permissions(BaseModel):
    web_check_in_out:Optional[bool]=False
    mobile_check_in_out:Optional[bool]=False
    show_all_check_in_out:Optional[bool]=False
    view_report_entries:Optional[bool]=False
    edit_report_entries:Optional[bool]=False
    edit_own_entries:Optional[bool]=False
    show_attendance_report:Optional[List[str]]
    show_balance_over_time:Optional[List[str]]
    edit_balance_over_time:Optional[List[str]]
    track_in_out_location:Optional[bool]=False
    restrict_in_out_entries:Optional[bool]=False


class Shift_Settings(BaseModel):
    view_emp_shift_map:Optional[List[str]]
    edit_emp_shift_map:Optional[List[str]]
    allow_changing_shifts:Optional[bool]=False
    email_notification_modify:Optional[bool]=False
    feeds_notification_modify:Optional[bool]=False
    eligibility_shift_allowence:Optional[str]
    make_reason_mandatory:Optional[bool]=False


class Attendance_General_SettingIn(BaseModel):
    effictive_from:str
    default_shift_time:str
    scale_view:Optional[bool]=False
    working_hours:Optional[Working_Hours]
    late_night_work:Optional[Late_night_work]
    permissions:Optional[Permissions]
    shift_settings:Optional[Shift_Settings]


class Attendance_General_settingsOut(BaseModel):
    effictive_from:str
    default_shift_time:str
    scale_view:Optional[bool]
    total_hour_calculation:Optional[str]
    minimum_hours_required:Optional[str]
    strict_mode_manual:Optional[bool]
    strict_mode_full_day:Optional[str]
    strict_mode_half_day:Optional[str]
    strict_shift_hours_full_day:Optional[str]
    strict_shift_hour_half_day:Optional[str]
    lenient_mode_manual:Optional[bool]
    lenient_mode_per_day:Optional[str]
    lenient_mode_shift:Optional[str]
    show_overtime_deveation:Optional[bool]
    maximum_hours_required:Optional[bool]
    round_off:Optional[bool]
    first_check_in:Optional[str]
    last_check_out:Optional[str]
    worked_hours:Optional[str]

