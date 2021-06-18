from enum import Enum
from dataclasses import dataclass, field
from typing import List


class Grade(Enum):
    H0 = 0
    G2 = 1
    G1 = 2
    F3 = 3
    F2 = 4
    F1 = 5
    E3 = 6
    E2 = 7
    E1 = 8
    D3 = 9
    D2 = 10
    D1 = 11
    C3 = 12
    C2 = 13
    C1 = 14
    B3 = 15
    B2 = 16
    B1 = 17
    A5 = 18
    A4 = 19
    A3 = 20
    A2 = 21
    A1 = 22


@dataclass
class Course:
    name: str
    credits: float
    grade: Grade

    points: float = field(init=False)

    def __post_init__(self):
        self.points = self.credits * self.grade.value


@dataclass
class Assignment(Course):
    NDP: bool


@dataclass
class Result:
    final_gpa: float
    baseline_gpa: float
    credits_used_unweighted: float
    credits_unused_unweighted: float
    excluded_assignments: List[Assignment]
