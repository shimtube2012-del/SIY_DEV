"""
탐색 알고리즘 비교 프로그램
- 선형 탐색 (Linear Search)
- 이진 탐색 (Binary Search)
- 점프 탐색 (Jump Search)
- 보간 탐색 (Interpolation Search)

Made by IYShim
"""

import time
import random
import math


def linear_search(arr, target):
    """선형 탐색: 처음부터 끝까지 하나씩 확인"""
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    return -1, comparisons


def binary_search(arr, target):
    """이진 탐색: 정렬된 배열에서 중간값 비교로 범위를 절반씩 줄임"""
    comparisons = 0
    left, right = 0, len(arr) - 1

    while left <= right:
        comparisons += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1, comparisons


def jump_search(arr, target):
    """점프 탐색: 블록 단위로 점프하며 탐색"""
    comparisons = 0
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0

    # 블록 단위로 점프
    while prev < n and arr[min(step, n) - 1] < target:
        comparisons += 1
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1, comparisons

    # 블록 내에서 선형 탐색
    while prev < min(step, n):
        comparisons += 1
        if arr[prev] == target:
            return prev, comparisons
        prev += 1

    return -1, comparisons


def interpolation_search(arr, target):
    """보간 탐색: 값의 위치를 예측하여 탐색 (균등 분포에 효과적)"""
    comparisons = 0
    low, high = 0, len(arr) - 1

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1

        if arr[high] == arr[low]:
            if arr[low] == target:
                return low, comparisons
            break

        # 위치 예측 공식
        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])

        if pos < low or pos > high:
            break

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def demonstrate_search(arr, target, search_func, name):
    """탐색 알고리즘 실행 및 결과 출력"""
    start_time = time.perf_counter()
    index, comparisons = search_func(arr, target)
    end_time = time.perf_counter()

    elapsed = (end_time - start_time) * 1000000  # 마이크로초

    if index != -1:
        print(f"\n[{name}]")
        print(f"  찾은 위치: {index}번 인덱스")
        print(f"  비교 횟수: {comparisons}회")
        print(f"  소요 시간: {elapsed:.2f} μs")
    else:
        print(f"\n[{name}]")
        print(f"  결과: 찾지 못함")
        print(f"  비교 횟수: {comparisons}회")

    return comparisons


def visualize_binary_search(arr, target):
    """이진 탐색 과정 시각화"""
    print("\n[이진 탐색 과정 시각화]")
    left, right = 0, len(arr) - 1
    step = 1

    while left <= right:
        mid = (left + right) // 2

        # 현재 범위 표시
        visual = ""
        for i in range(len(arr)):
            if i == mid:
                visual += f"[{arr[i]:2d}]"
            elif left <= i <= right:
                visual += f" {arr[i]:2d} "
            else:
                visual += "  · "

        print(f"  {step}단계: {visual}")
        print(f"         범위: [{left}~{right}], 중간: {mid}, 값: {arr[mid]}")

        if arr[mid] == target:
            print(f"  → 찾음!")
            break
        elif arr[mid] < target:
            print(f"  → {arr[mid]} < {target}, 오른쪽으로 이동")
            left = mid + 1
        else:
            print(f"  → {arr[mid]} > {target}, 왼쪽으로 이동")
            right = mid - 1

        step += 1
        print()


def main():
    print_header("탐색 알고리즘 비교 프로그램")
    print("\nMade by IYShim")

    while True:
        print("\n" + "-" * 50)
        print("메뉴:")
        print("  1. 작은 배열로 시각화 보기")
        print("  2. 큰 배열로 성능 비교")
        print("  3. 직접 배열 입력하기")
        print("  4. 종료")
        print("-" * 50)

        choice = input("선택: ").strip()

        if choice == "1":
            # 작은 배열로 시각화
            arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
            print(f"\n배열: {arr}")

            try:
                target = int(input("찾을 숫자 입력: "))
            except ValueError:
                print("숫자를 입력해주세요!")
                continue

            visualize_binary_search(arr, target)

            print("\n--- 모든 알고리즘 비교 ---")
            demonstrate_search(arr, target, linear_search, "선형 탐색")
            demonstrate_search(arr, target, binary_search, "이진 탐색")
            demonstrate_search(arr, target, jump_search, "점프 탐색")
            demonstrate_search(arr, target, interpolation_search, "보간 탐색")

        elif choice == "2":
            # 큰 배열로 성능 비교
            try:
                size = int(input("배열 크기 입력 (예: 10000): "))
            except ValueError:
                size = 10000

            arr = sorted(random.sample(range(size * 10), size))
            target = random.choice(arr)  # 배열에서 무작위 선택

            print(f"\n배열 크기: {size}개")
            print(f"찾을 값: {target}")

            results = {}
            results["선형 탐색"] = demonstrate_search(arr, target, linear_search, "선형 탐색")
            results["이진 탐색"] = demonstrate_search(arr, target, binary_search, "이진 탐색")
            results["점프 탐색"] = demonstrate_search(arr, target, jump_search, "점프 탐색")
            results["보간 탐색"] = demonstrate_search(arr, target, interpolation_search, "보간 탐색")

            # 결과 요약
            print("\n--- 비교 횟수 요약 ---")
            min_comp = min(results.values())
            for name, comp in sorted(results.items(), key=lambda x: x[1]):
                bar = "█" * (comp // max(1, min_comp))
                best = " ★ 최소" if comp == min_comp else ""
                print(f"  {name}: {comp}회 {bar}{best}")

        elif choice == "3":
            # 직접 입력
            try:
                nums = input("숫자들을 공백으로 구분해서 입력: ").split()
                arr = sorted([int(x) for x in nums])
                print(f"정렬된 배열: {arr}")

                target = int(input("찾을 숫자 입력: "))

                demonstrate_search(arr, target, linear_search, "선형 탐색")
                demonstrate_search(arr, target, binary_search, "이진 탐색")
                demonstrate_search(arr, target, jump_search, "점프 탐색")
                demonstrate_search(arr, target, interpolation_search, "보간 탐색")

            except ValueError:
                print("올바른 숫자를 입력해주세요!")

        elif choice == "4":
            print("\n프로그램을 종료합니다. 감사합니다!")
            break
        else:
            print("1, 2, 3, 4 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
