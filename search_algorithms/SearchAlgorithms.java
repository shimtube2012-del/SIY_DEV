/**
 * 탐색 알고리즘 비교 프로그램
 * - 선형 탐색 (Linear Search)
 * - 이진 탐색 (Binary Search)
 * - 점프 탐색 (Jump Search)
 * - 보간 탐색 (Interpolation Search)
 *
 * Made by IYShim
 */

import java.util.*;

public class SearchAlgorithms {

    // 탐색 결과를 담는 클래스
    static class SearchResult {
        int index;
        int comparisons;

        SearchResult(int index, int comparisons) {
            this.index = index;
            this.comparisons = comparisons;
        }
    }

    // 선형 탐색: 처음부터 끝까지 하나씩 확인
    public static SearchResult linearSearch(int[] arr, int target) {
        int comparisons = 0;
        for (int i = 0; i < arr.length; i++) {
            comparisons++;
            if (arr[i] == target) {
                return new SearchResult(i, comparisons);
            }
        }
        return new SearchResult(-1, comparisons);
    }

    // 이진 탐색: 정렬된 배열에서 중간값 비교로 범위를 절반씩 줄임
    public static SearchResult binarySearch(int[] arr, int target) {
        int comparisons = 0;
        int left = 0, right = arr.length - 1;

        while (left <= right) {
            comparisons++;
            int mid = (left + right) / 2;

            if (arr[mid] == target) {
                return new SearchResult(mid, comparisons);
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return new SearchResult(-1, comparisons);
    }

    // 점프 탐색: 블록 단위로 점프하며 탐색
    public static SearchResult jumpSearch(int[] arr, int target) {
        int comparisons = 0;
        int n = arr.length;
        int step = (int) Math.sqrt(n);
        int prev = 0;

        // 블록 단위로 점프
        while (prev < n && arr[Math.min(step, n) - 1] < target) {
            comparisons++;
            prev = step;
            step += (int) Math.sqrt(n);
            if (prev >= n) {
                return new SearchResult(-1, comparisons);
            }
        }

        // 블록 내에서 선형 탐색
        while (prev < Math.min(step, n)) {
            comparisons++;
            if (arr[prev] == target) {
                return new SearchResult(prev, comparisons);
            }
            prev++;
        }

        return new SearchResult(-1, comparisons);
    }

    // 보간 탐색: 값의 위치를 예측하여 탐색 (균등 분포에 효과적)
    public static SearchResult interpolationSearch(int[] arr, int target) {
        int comparisons = 0;
        int low = 0, high = arr.length - 1;

        while (low <= high && arr[low] <= target && target <= arr[high]) {
            comparisons++;

            if (arr[high] == arr[low]) {
                if (arr[low] == target) {
                    return new SearchResult(low, comparisons);
                }
                break;
            }

            // 위치 예측 공식
            int pos = low + ((target - arr[low]) * (high - low)) / (arr[high] - arr[low]);

            if (pos < low || pos > high) {
                break;
            }

            if (arr[pos] == target) {
                return new SearchResult(pos, comparisons);
            } else if (arr[pos] < target) {
                low = pos + 1;
            } else {
                high = pos - 1;
            }
        }

        return new SearchResult(-1, comparisons);
    }

    public static void printHeader(String title) {
        System.out.println();
        System.out.println("==================================================");
        System.out.println("  " + title);
        System.out.println("==================================================");
    }

    public static int demonstrateSearch(int[] arr, int target, String name,
            java.util.function.BiFunction<int[], Integer, SearchResult> searchFunc) {
        long startTime = System.nanoTime();
        SearchResult result = searchFunc.apply(arr, target);
        long endTime = System.nanoTime();

        double elapsed = (endTime - startTime) / 1000.0; // 마이크로초

        if (result.index != -1) {
            System.out.println("\n[" + name + "]");
            System.out.println("  찾은 위치: " + result.index + "번 인덱스");
            System.out.println("  비교 횟수: " + result.comparisons + "회");
            System.out.printf("  소요 시간: %.2f μs%n", elapsed);
        } else {
            System.out.println("\n[" + name + "]");
            System.out.println("  결과: 찾지 못함");
            System.out.println("  비교 횟수: " + result.comparisons + "회");
        }

        return result.comparisons;
    }

    public static void visualizeBinarySearch(int[] arr, int target) {
        System.out.println("\n[이진 탐색 과정 시각화]");
        int left = 0, right = arr.length - 1;
        int step = 1;

        while (left <= right) {
            int mid = (left + right) / 2;

            // 현재 범위 표시
            StringBuilder visual = new StringBuilder();
            for (int i = 0; i < arr.length; i++) {
                if (i == mid) {
                    visual.append(String.format("[%2d]", arr[i]));
                } else if (left <= i && i <= right) {
                    visual.append(String.format(" %2d ", arr[i]));
                } else {
                    visual.append("  · ");
                }
            }

            System.out.println("  " + step + "단계: " + visual);
            System.out.println("         범위: [" + left + "~" + right + "], 중간: " + mid + ", 값: " + arr[mid]);

            if (arr[mid] == target) {
                System.out.println("  → 찾음!");
                break;
            } else if (arr[mid] < target) {
                System.out.println("  → " + arr[mid] + " < " + target + ", 오른쪽으로 이동");
                left = mid + 1;
            } else {
                System.out.println("  → " + arr[mid] + " > " + target + ", 왼쪽으로 이동");
                right = mid - 1;
            }

            step++;
            System.out.println();
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        printHeader("탐색 알고리즘 비교 프로그램");
        System.out.println("\nMade by IYShim");

        while (true) {
            System.out.println("\n--------------------------------------------------");
            System.out.println("메뉴:");
            System.out.println("  1. 작은 배열로 시각화 보기");
            System.out.println("  2. 큰 배열로 성능 비교");
            System.out.println("  3. 직접 배열 입력하기");
            System.out.println("  4. 종료");
            System.out.println("--------------------------------------------------");

            System.out.print("선택: ");
            String choice = scanner.nextLine().trim();

            if (choice.equals("1")) {
                // 작은 배열로 시각화
                int[] arr = {2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91};
                System.out.println("\n배열: " + Arrays.toString(arr));

                System.out.print("찾을 숫자 입력: ");
                int target;
                try {
                    target = Integer.parseInt(scanner.nextLine().trim());
                } catch (NumberFormatException e) {
                    System.out.println("숫자를 입력해주세요!");
                    continue;
                }

                visualizeBinarySearch(arr, target);

                System.out.println("\n--- 모든 알고리즘 비교 ---");
                demonstrateSearch(arr, target, "선형 탐색", (a, t) -> linearSearch(a, t));
                demonstrateSearch(arr, target, "이진 탐색", (a, t) -> binarySearch(a, t));
                demonstrateSearch(arr, target, "점프 탐색", (a, t) -> jumpSearch(a, t));
                demonstrateSearch(arr, target, "보간 탐색", (a, t) -> interpolationSearch(a, t));

            } else if (choice.equals("2")) {
                // 큰 배열로 성능 비교
                System.out.print("배열 크기 입력 (예: 10000): ");
                int size;
                try {
                    size = Integer.parseInt(scanner.nextLine().trim());
                } catch (NumberFormatException e) {
                    size = 10000;
                }

                // 중복 없는 랜덤 배열 생성
                Set<Integer> set = new LinkedHashSet<>();
                Random random = new Random();
                while (set.size() < size) {
                    set.add(random.nextInt(size * 10));
                }
                int[] arr = set.stream().mapToInt(Integer::intValue).sorted().toArray();
                int target = arr[random.nextInt(arr.length)]; // 배열에서 무작위 선택

                System.out.println("\n배열 크기: " + size + "개");
                System.out.println("찾을 값: " + target);

                Map<String, Integer> results = new LinkedHashMap<>();
                results.put("선형 탐색", demonstrateSearch(arr, target, "선형 탐색", (a, t) -> linearSearch(a, t)));
                results.put("이진 탐색", demonstrateSearch(arr, target, "이진 탐색", (a, t) -> binarySearch(a, t)));
                results.put("점프 탐색", demonstrateSearch(arr, target, "점프 탐색", (a, t) -> jumpSearch(a, t)));
                results.put("보간 탐색", demonstrateSearch(arr, target, "보간 탐색", (a, t) -> interpolationSearch(a, t)));

                // 결과 요약
                System.out.println("\n--- 비교 횟수 요약 ---");
                int minComp = Collections.min(results.values());
                results.entrySet().stream()
                    .sorted(Map.Entry.comparingByValue())
                    .forEach(entry -> {
                        int barCount = entry.getValue() / Math.max(1, minComp);
                        StringBuilder bar = new StringBuilder();
                        for (int i = 0; i < barCount; i++) bar.append("█");
                        String best = entry.getValue() == minComp ? " ★ 최소" : "";
                        System.out.println("  " + entry.getKey() + ": " + entry.getValue() + "회 " + bar + best);
                    });

            } else if (choice.equals("3")) {
                // 직접 입력
                try {
                    System.out.print("숫자들을 공백으로 구분해서 입력: ");
                    String[] nums = scanner.nextLine().split("\\s+");
                    int[] arr = Arrays.stream(nums)
                        .mapToInt(Integer::parseInt)
                        .sorted()
                        .toArray();
                    System.out.println("정렬된 배열: " + Arrays.toString(arr));

                    System.out.print("찾을 숫자 입력: ");
                    int target = Integer.parseInt(scanner.nextLine().trim());

                    demonstrateSearch(arr, target, "선형 탐색", (a, t) -> linearSearch(a, t));
                    demonstrateSearch(arr, target, "이진 탐색", (a, t) -> binarySearch(a, t));
                    demonstrateSearch(arr, target, "점프 탐색", (a, t) -> jumpSearch(a, t));
                    demonstrateSearch(arr, target, "보간 탐색", (a, t) -> interpolationSearch(a, t));

                } catch (NumberFormatException e) {
                    System.out.println("올바른 숫자를 입력해주세요!");
                }

            } else if (choice.equals("4")) {
                System.out.println("\n프로그램을 종료합니다. 감사합니다!");
                break;
            } else {
                System.out.println("1, 2, 3, 4 중에서 선택해주세요.");
            }
        }

        scanner.close();
    }
}
