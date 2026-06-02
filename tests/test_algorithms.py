from src.algorithms import (
    two_sum,
    remove_duplicates,
    max_sum_subarray,
    longest_unique_substring,
    chunked,
    pairwise,
    group_by,
    flatten,
    is_palindrome,
    merge_sorted,
)


class TestTwoSum:
    def test_basic(self):
        assert two_sum([2, 7, 11, 15], 9) == (0, 1)

    def test_no_solution(self):
        assert two_sum([1, 2, 3], 10) is None

    def test_empty(self):
        assert two_sum([], 5) is None


class TestRemoveDuplicates:
    def test_basic(self):
        nums = [1, 1, 2]
        k = remove_duplicates(nums)
        assert k == 2
        assert sorted(nums[:k]) == [1, 2]

    def test_all_unique(self):
        nums = [1, 2, 3]
        assert remove_duplicates(nums) == 3


class TestMaxSumSubarray:
    def test_basic(self):
        assert max_sum_subarray([1, 2, 3, 4, 5], 2) == 9

    def test_smaller_than_k(self):
        assert max_sum_subarray([1], 2) is None


class TestLongestUniqueSubstring:
    def test_basic(self):
        assert longest_unique_substring("abcabcbb") == 3

    def test_repeat(self):
        assert longest_unique_substring("bbbbb") == 1


class TestChunked:
    def test_basic(self):
        assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


class TestPairwise:
    def test_basic(self):
        assert list(pairwise([1, 2, 3])) == [(1, 2), (2, 3)]


class TestGroupBy:
    def test_basic(self):
        result = group_by([1, 2, 3, 4, 5, 6], lambda x: x % 2)
        assert result == {1: [1, 3, 5], 0: [2, 4, 6]}


class TestFlatten:
    def test_basic(self):
        assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

    def test_empty(self):
        assert flatten([]) == []


class TestIsPalindrome:
    def test_valid(self):
        assert is_palindrome("A man, a plan, a canal: Panama") is True

    def test_invalid(self):
        assert is_palindrome("hello") is False


class TestMergeSorted:
    def test_basic(self):
        assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

    def test_empty(self):
        assert merge_sorted([], [1, 2]) == [1, 2]
