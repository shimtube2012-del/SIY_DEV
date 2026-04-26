import random

def play_game():
    """숫자 맞추기 게임"""
    print("=" * 40)
    print("       숫자 맞추기 게임")
    print("=" * 40)

    # 난이도 선택
    print("\n난이도를 선택하세요:")
    print("1. 쉬움 (1~50, 10번 기회)")
    print("2. 보통 (1~100, 7번 기회)")
    print("3. 어려움 (1~200, 5번 기회)")

    while True:
        choice = input("\n선택 (1/2/3): ").strip()
        if choice == '1':
            max_num, max_tries = 50, 10
            break
        elif choice == '2':
            max_num, max_tries = 100, 7
            break
        elif choice == '3':
            max_num, max_tries = 200, 5
            break
        else:
            print("1, 2, 3 중에서 선택해주세요.")

    # 정답 생성
    answer = random.randint(1, max_num)
    tries = 0

    print(f"\n1부터 {max_num} 사이의 숫자를 맞춰보세요!")
    print(f"기회: {max_tries}번\n")

    while tries < max_tries:
        tries += 1
        remaining = max_tries - tries

        # 사용자 입력
        try:
            guess = int(input(f"[{tries}/{max_tries}] 숫자 입력: "))
        except ValueError:
            print("숫자를 입력해주세요!")
            tries -= 1
            continue

        # 정답 체크
        if guess == answer:
            print(f"\n정답입니다! {tries}번 만에 맞추셨습니다!")
            return True
        elif guess < answer:
            print(f"UP! 더 큰 숫자입니다. (남은 기회: {remaining}번)")
        else:
            print(f"DOWN! 더 작은 숫자입니다. (남은 기회: {remaining}번)")

    print(f"\n게임 오버! 정답은 {answer}였습니다.")
    return False


def main():
    """메인 함수"""
    wins = 0
    games = 0

    while True:
        games += 1
        if play_game():
            wins += 1

        print(f"\n전적: {wins}승 / {games}게임")

        again = input("\n다시 하시겠습니까? (y/n): ").strip().lower()
        if again != 'y':
            print("\n게임을 종료합니다. 감사합니다!")
            break
        print()


if __name__ == '__main__':
    main()
