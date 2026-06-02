from typing import Any, Callable, Generator, Iterator, Optional, TypeVar

T = TypeVar("T")


def two_sum(nums: list[int], target: int) -> Optional[tuple[int, int]]:
    seen: dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    return None


def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def max_sum_subarray(nums: list[int], k: int) -> Optional[int]:
    if len(nums) < k:
        return None
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum


def longest_unique_substring(s: str) -> int:
    seen: dict[str, int] = {}
    left = max_len = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len


def chunked(iterable: list[T], size: int) -> Generator[list[T], None, None]:
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def pairwise(iterable: list[T]) -> Generator[tuple[T, T], None, None]:
    for i in range(len(iterable) - 1):
        yield (iterable[i], iterable[i + 1])


def group_by(
    iterable: list[T], key_func: Callable[[T], Any]
) -> dict[Any, list[T]]:
    result: dict[Any, list[T]] = {}
    for item in iterable:
        key = key_func(item)
        result.setdefault(key, []).append(item)
    return result


def flatten(nested: list[Any]) -> list[Any]:
    result: list[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def is_palindrome(s: str) -> bool:
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result
