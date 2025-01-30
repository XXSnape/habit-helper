from .create import (register_get_count, register_get_description,
                     register_get_hour, register_get_name, register_mark_habit,
                     register_save_habit)
from .delete import register_delete_habit
from .read import (register_calendar, register_get_habit_details,
                   register_get_habits)
from .update import (register_change_count, register_change_description,
                     register_change_frozen, register_change_name,
                     register_change_time, register_provide_with_choosing,
                     register_resume_habits)
