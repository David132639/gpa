from typing import Callable, List, Tuple, TypeVar

from object_definitions import Assignment, Grade, Course, Result

T = TypeVar("T")


def __split_on_predicate(
    predicate: Callable[[T], bool], items: List[T]
) -> Tuple[List[T], List[T]]:
    result: Tuple[List[T], List[T]] = ([], [])
    for item in items:
        if predicate(item):
            result[0].append(item)
        else:
            result[1].append(item)
    return result


def __truthify(inp: str) -> bool:
    norm = inp.lower()
    return norm in ["ndp", "t", "y", "1"]


def gpa_to_degree(gpa: float) -> str:
    if gpa >= 17.5:
        res = "a First Class Degree"
    elif gpa >= 14.5:
        res = "a 2:1 Degree"
    elif gpa >= 11.5:
        res = "a 2:2 Degree"
    elif gpa >= 8.5:
        res = "a Third Class Degree"
    else:
        res = "no Honours Degree"

    if 17.0 < gpa < 17.5 or 14.0 < gpa < 14.5 or 11.0 < gpa < 11.5 or 11.0 < gpa < 11.5:
        res += " (with a possibility of a higher classification under COVID discretion rules)"

    return res


def parse_ndp(filename: str) -> List[Assignment]:
    output = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                line_array = line.strip().split(",")
                if len(line_array) != 5 or len(line_array[3]) != 2:
                    continue
                output.append(
                    Assignment(
                        f"{line_array[0]}:{line_array[1]}",
                        float(line_array[2]),
                        Grade[line_array[3].upper()],
                        __truthify(line_array[4]),
                    )
                )
    except Exception as e:
        print(f'Failed to pass {filename}, with error:\n"{e}"')
        return []
    return output


def parse_normal(filename: str) -> List[Course]:
    output = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                line_array = line.strip().split(",")
                if len(line_array) != 3 or len(line_array[2]) != 2:
                    continue
                output.append(
                    Course(
                        line_array[0],
                        float(line_array[1]),
                        Grade[line_array[2].upper()],
                    )
                )
    except Exception as e:
        print(f'Failed to pass {filename}, with error:\n"{e}"')
        return []
    return output


def calculate_bsc(l3, l4):
    return calculate(l3, l4, [], 0.4, 0.6, 0)


def calculate_placement(l3, l4, l5):
    return calculate(l3, l4, l5, 0.3, 0.2, 0.5)


def calculate_msci(l3, l4, l5):
    return calculate(l3, l4, l5, 0.24, 0.36, 0.4)


def calculate(
    l3: List[Assignment],
    l4: List[Course],
    l5: List[Course],
    l3_weight: float,
    l4_weight: float,
    l5_weight: float,
) -> Result:

    l3_ndp, l3_pre = __split_on_predicate(lambda x: x.NDP, l3)

    cred_base = (
        l5_weight * sum([x.credits for x in l5])
        + l4_weight * sum([x.credits for x in l4])
        + l3_weight * sum([x.credits for x in l3_pre])
    )
    points_base = (
        l5_weight * sum([x.points for x in l5])
        + l4_weight * sum([x.points for x in l4])
        + l3_weight * sum([x.points for x in l3_pre])
    )

    assert cred_base > 0, "No valid credits found, probably a parse error occurred."

    baseline_gpa = round(points_base / cred_base, 1)

    l3_ndp_good, l3_ndp_bad = __split_on_predicate(
        lambda x: (x.points / x.credits >= baseline_gpa), l3_ndp
    )

    cred_final = cred_base + l3_weight * sum([x.credits for x in l3_ndp_good])
    points_final = points_base + l3_weight * sum([x.points for x in l3_ndp_good])

    final_gpa = round(points_final / cred_final, 1)

    credits_used_unweighted = sum(
        [x.credits for x in l5]
        + [x.credits for x in l4]
        + [x.credits for x in l3_pre]
        + [x.credits for x in l3_ndp_good]
    )

    credits_unused_unweighted = sum([x.credits for x in l3_ndp_bad])

    return Result(
        final_gpa=final_gpa,
        baseline_gpa=baseline_gpa,
        credits_used_unweighted=credits_used_unweighted,
        credits_unused_unweighted=credits_unused_unweighted,
        excluded_assignments=l3_ndp_bad,
    )


def interpret_result(result):
    total_credits = result.credits_unused_unweighted + result.credits_used_unweighted

    threshold = 0.65 * total_credits

    if result.credits_used_unweighted < threshold:
        print("Too few credits, can't complete calculation")

    else:
        print(
            f"Final GPA is {result.final_gpa} "
            f"(from a baseline GPA of {result.baseline_gpa})"
        )
        print(
            f"This is based on {result.credits_used_unweighted} unweighted credits, "
            f"which exceeds the {threshold} (65% of {total_credits}) required threshold.\n"
            f"A total of {result.credits_unused_unweighted} credits "
            "was excluded under NDP, from a total of "
            f"{total_credits} "
            "honours credits."
        )
        print(f"You are predicted to receive {gpa_to_degree(result.final_gpa)}.")

        if result.excluded_assignments:
            print("\nAssessments excluded under NDP are:")
            for assessment in result.excluded_assignments:
                print(f"'{assessment.name}' worth {assessment.credits} credits")
