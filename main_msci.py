#!/usr/bin/env python3

from typing import List

from object_definitions import Assignment, Course
from lib import parse_ndp, parse_normal, interpret_result, calculate_msci


l3: List[Assignment] = parse_ndp("y3.txt")
l4: List[Course] = parse_normal("y4.txt")
l5: List[Course] = parse_normal("y5.txt")

interpret_result(calculate_msci(l3=l3, l4=l4, l5=l5))
