from typing import Optional


def create_staircase(nums: list[int]) -> Optional[list[list[int]]]:
    step = 1
    subsets: list[list[int]] = []
    remaining = list(nums)

    while remaining:
        if len(remaining) >= step:
            subset = remaining[:step]
            subsets.append(subset)
            remaining = remaining[step:]
            step += 1
        else:
            return None

    return subsets
