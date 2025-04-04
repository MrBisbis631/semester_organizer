from typing import List, Set
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from src.data.day import Day
from src.data.degree import Degree
from src.data.output_format import OutputFormat
from src.data.semester import Semester
from src.data.language import Language
from src import utils


@dataclass_json
@dataclass
class Settings:
    attendance_required_all_courses: bool = True
    campus_name: str = ""
    year: int = utils.get_current_hebrew_year()
    semester: Semester = utils.get_current_semester()
    _degree: str = "COMPUTER_SCIENCE"
    _degrees: List[str] = field(default_factory=lambda: [degree.name for degree in Degree.get_defaults()])
    show_hertzog_and_yeshiva: bool = False
    show_only_courses_with_free_places: bool = False
    show_only_courses_active_classes: bool = True
    show_only_courses_with_the_same_actual_number: bool = True
    dont_show_courses_already_done: bool = True
    show_only_classes_in_days: List[Day] = field(default_factory=lambda: list(Day))
    output_formats: List[OutputFormat] = field(default_factory=lambda: [OutputFormat.IMAGE])
    show_only_classes_can_enroll: bool = True
    show_only_courses_with_prerequisite_done: bool = False
    language: Language = Language.get_current()
    force_update_data: bool = True
    show_english_speaker_courses: bool = False

    @property
    def degrees(self) -> Set[Degree]:
        return {Degree[degree] for degree in self._degrees}

    @degrees.setter
    def degrees(self, degrees: Set[Degree]):
        self._degrees = [degree.name for degree in degrees]

    @property
    def degree(self) -> Degree:
        return Degree[self._degree]

    @degree.setter
    def degree(self, degree: Degree):
        self._degree = degree.name
