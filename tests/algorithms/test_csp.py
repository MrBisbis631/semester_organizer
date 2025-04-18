import pytest

from src.algorithms.csp import CSP, Status
from src.data.academic_activity import AcademicActivity
from src.data.activity import Activity
from src.data.course_choice import CourseChoice
from src.data.day import Day
from src.data.degree import Degree
from src.data.meeting import Meeting
from src.data.schedule import Schedule
from src.data.settings import Settings
from src.data.type import Type


class TestCsp:

    def test_is_consist_itself_option(self):
        activities = []
        csp = CSP()
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a", "1")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LAB, True, "a", 1, 1, "a", "2")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:20", "11:00"))
        activities.append(academic_activity)

        activities_ids_groups = {
            "1": {1},
            "2": {2}
        }

        for schedules in [csp.extract_schedules(activities),
                          csp.extract_schedules_minimal_consists(activities, activities_ids_groups)]:
            assert len(schedules) == 0

    def test_zero_from_one_option(self):
        activities = []
        csp = CSP()
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a", "1")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        with pytest.raises(RuntimeError):
            academic_activity.add_slot(Meeting(Day.SUNDAY, "10:20", "10:40"))
        activities.append(academic_activity)

        academic_activity = AcademicActivity("b", Type.LECTURE, True, "b", 1, 1, "b", "2")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:30", "14:30"))
        activities.append(academic_activity)

        activities_ids_groups = {
            "1": {1},
            "2": {1},
        }

        for schedules in [csp.extract_schedules(activities),
                          csp.extract_schedules_minimal_consists(activities, activities_ids_groups)]:
            assert len(schedules) == 0

    def test_one_from_one_option(self):
        activities = []
        csp = CSP()
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a", "1")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)

        academic_activity = AcademicActivity("b", Type.LAB, True, "b", 1, 1, "b", "2")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "12:00", "14:30"))
        activities.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(activity)

        schedule = Schedule("Option 0", "option_0", "", activities)
        activities_ids_groups = {
            "1": {1},
            "2": {1},
        }

        for schedules in [csp.extract_schedules(activities),
                          csp.extract_schedules_minimal_consists(activities, activities_ids_groups)]:
            assert len(schedules) == 1
            assert any(schedule.contains(activities) for schedule in schedules)
            assert schedule in schedules

    def test_two_from_two_options(self):
        activities_option_1 = []
        activities_option_2 = []

        activities = []
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, Meeting.str_to_time("10:00"), Meeting.str_to_time("11:00")))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, Meeting.str_to_time("12:00"), Meeting.str_to_time("14:30")))
        activities.append(academic_activity)
        activities_option_2.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, Meeting.str_to_time("12:00"), Meeting.str_to_time("14:30")))
        activities.append(activity)
        activities_option_1.append(activity)
        activities_option_2.append(activity)

        schedules = CSP().extract_schedules(activities)
        assert len(schedules) == 2
        assert any(schedule.contains(activities_option_1) for schedule in schedules)
        assert any(schedule.contains(activities_option_2) for schedule in schedules)

    def test_one_from_two_options(self):
        activities_option_1 = []

        activities = []
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, Meeting.str_to_time("10:00"), Meeting.str_to_time("11:00")))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, Meeting.str_to_time("12:00"), Meeting.str_to_time("14:30")))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.MONDAY, Meeting.str_to_time("13:00"), Meeting.str_to_time("13:30")))
        activities.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, Meeting.str_to_time("12:00"), Meeting.str_to_time("14:30")))
        activities.append(activity)
        activities_option_1.append(activity)

        schedules = CSP().extract_schedules(activities)
        assert len(schedules) == 1
        assert any(schedule.contains(activities_option_1) for schedule in schedules)

    def test_no_option(self):
        activities = []
        csp = CSP()
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LAB, True, "a", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.MONDAY, "12:00", "13:30"))
        activities.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(activity)

        schedules = csp.extract_schedules(activities)
        assert len(schedules) == 0
        assert csp.get_status() is Status.FAILED

        schedules = csp.extract_schedules_minimal_consists(activities)
        assert len(schedules) == 0
        assert csp.get_status() is Status.FAILED
        assert csp.get_last_activities_crashed() == ("a", "c")

    def test_one_option_favorite_one_teacher(self):
        activities_option = []

        activities = []
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "Mike", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "15:00", "17:30"))
        activities.append(academic_activity)
        activities_option.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(activity)
        activities_option.append(activity)

        course_choice = CourseChoice("a", 1, {"Mike"}, set())

        schedules = CSP().extract_schedules(activities, {"a": course_choice})
        assert len(schedules) == 1
        assert schedules[0].contains(activities_option)

    def test_one_option_no_options_for_favorite_teacher(self):
        activities_option = []

        activities = []
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)
        activities_option.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "Mike", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(activity)
        activities_option.append(activity)

        course_choice = CourseChoice("a", 1, {"Mike"}, set())

        schedules = CSP().extract_schedules(activities, {"a": course_choice})
        assert len(schedules) == 1
        assert schedules[0].contains(activities_option)

    def test_one_option_only_parts_options_for_favorite_teacher(self):
        activities_option = []
        csp = CSP()

        activities = []
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)
        activities_option.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "Mike", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "12:00", "14:30"))
        activities.append(academic_activity)
        activities_option.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.add_slot(Meeting(Day.MONDAY, "18:00", "20:30"))
        activities.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(activity)
        activities_option.append(activity)

        course_choice = CourseChoice("a", 1, set(), {"Mike"})

        schedules = csp.extract_schedules(activities, {"a": course_choice})
        assert len(schedules) == 1
        assert schedules[0].contains(activities_option)
        assert csp.get_status() is Status.SUCCESS

    def test_one_option_capacity_consist(self):
        activities_option = []

        activities = []
        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)
        activities_option.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.set_capacity(13, 30)
        academic_activity.add_slot(Meeting(Day.SUNDAY, "12:00", "14:30"))
        activities.append(academic_activity)
        activities_option.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.set_capacity(10, 10)
        academic_activity.add_slot(Meeting(Day.MONDAY, "18:00", "20:30"))
        activities.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(activity)
        activities_option.append(activity)

        settings = Settings()
        settings.show_only_courses_with_free_places = True

        schedules = CSP().extract_schedules(activities, settings=settings)
        assert len(schedules) == 1
        assert schedules[0].contains(activities_option)

    def test_two_options_by_actual_course_number(self):
        activities_option_1 = []
        activities_option_2 = []
        activities = []

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.actual_course_number = 1
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a")
        academic_activity.actual_course_number = 2
        academic_activity.add_slot(Meeting(Day.FRIDAY, "10:00", "11:00"))
        activities.append(academic_activity)
        activities_option_2.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.actual_course_number = 1
        academic_activity.add_slot(Meeting(Day.MONDAY, "12:00", "14:30"))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a")
        academic_activity.actual_course_number = 2
        academic_activity.add_slot(Meeting(Day.MONDAY, "18:00", "20:30"))
        activities.append(academic_activity)
        activities_option_2.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.THURSDAY, "12:00", "14:30"))
        activities.append(activity)
        activities_option_1.append(activity)
        activities_option_2.append(academic_activity)

        settings = Settings()
        settings.show_only_courses_with_the_same_actual_number = True

        schedules = CSP().extract_schedules(activities, settings=settings)
        assert len(schedules) == 2
        assert any(schedule.contains(activities_option_1) for schedule in schedules)
        assert any(schedule.contains(activities_option_2) for schedule in schedules)

    def test_only_activities_ids_can_enroll(self):
        activities_ids_can_enroll = {
            "1": {1, 2},
            "2": {1, 2},
            "3": {1},
        }
        activities_option_1 = []
        activities_option_2 = []
        activities = []
        csp = CSP()

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, activity_id="1")
        academic_activity.add_slot(Meeting(Day.SUNDAY, "10:00", "11:00"))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.LECTURE, True, "a", 1, 1, "a", activity_id="5")
        academic_activity.add_slot(Meeting(Day.MONDAY, "10:00", "11:00"))
        activities.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a", activity_id="2")
        academic_activity.add_slot(Meeting(Day.THURSDAY, "12:00", "14:30"))
        activities.append(academic_activity)
        activities_option_2.append(academic_activity)

        academic_activity = AcademicActivity("a", Type.PRACTICE, True, "a", 2, 2, "a", activity_id="3")
        academic_activity.add_slot(Meeting(Day.TUESDAY, "18:00", "20:30"))
        activities.append(academic_activity)
        activities_option_1.append(academic_activity)

        activity = Activity("c", Type.PERSONAL, True)
        activity.add_slot(Meeting(Day.WEDNESDAY, "12:00", "14:30"))
        activities.append(activity)
        activities_option_1.append(activity)
        activities_option_2.append(activity)

        settings = Settings()
        settings.show_only_classes_in_days = [Day.SUNDAY, Day.MONDAY, Day.THURSDAY, Day.TUESDAY, Day.WEDNESDAY]
        settings.show_only_classes_can_enroll = True

        schedules = csp.extract_schedules(activities, None, settings, activities_ids_can_enroll)
        assert len(schedules) == 2
        assert any(schedule.contains(activities_option_1) for schedule in schedules)
        assert any(schedule.contains(activities_option_2) for schedule in schedules)

        courses_degrees = {
            1: {Degree.SOFTWARE_ENGINEERING},
        }
        schedules = csp.extract_schedules(activities, None, settings, activities_ids_can_enroll, courses_degrees)
        assert len(schedules) == 4
