#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <windows.h>

using namespace std;

bool playGame() {
    cout << "========================================" << endl;
    cout << "       숫자 맞추기 게임" << endl;
    cout << "========================================" << endl;

    // 난이도 선택
    cout << "\n난이도를 선택하세요:" << endl;
    cout << "1. 쉬움 (1~50, 10번 기회)" << endl;
    cout << "2. 보통 (1~100, 7번 기회)" << endl;
    cout << "3. 어려움 (1~200, 5번 기회)" << endl;

    int maxNum, maxTries;
    string choice;

    while (true) {
        cout << "\n선택 (1/2/3): ";
        cin >> choice;

        if (choice == "1") {
            maxNum = 50;
            maxTries = 10;
            break;
        } else if (choice == "2") {
            maxNum = 100;
            maxTries = 7;
            break;
        } else if (choice == "3") {
            maxNum = 200;
            maxTries = 5;
            break;
        } else {
            cout << "1, 2, 3 중에서 선택해주세요." << endl;
        }
    }

    // 정답 생성
    int answer = rand() % maxNum + 1;
    int tries = 0;

    cout << "\n1부터 " << maxNum << " 사이의 숫자를 맞춰보세요!" << endl;
    cout << "기회: " << maxTries << "번\n" << endl;

    while (tries < maxTries) {
        tries++;
        int remaining = maxTries - tries;

        cout << "[" << tries << "/" << maxTries << "] 숫자 입력: ";
        int guess;

        if (!(cin >> guess)) {
            cout << "숫자를 입력해주세요!" << endl;
            cin.clear();
            cin.ignore(10000, '\n');
            tries--;
            continue;
        }

        if (guess == answer) {
            cout << "\n정답입니다! " << tries << "번 만에 맞추셨습니다!" << endl;
            return true;
        } else if (guess < answer) {
            cout << "UP! 더 큰 숫자입니다. (남은 기회: " << remaining << "번)" << endl;
        } else {
            cout << "DOWN! 더 작은 숫자입니다. (남은 기회: " << remaining << "번)" << endl;
        }
    }

    cout << "\n게임 오버! 정답은 " << answer << "였습니다." << endl;
    return false;
}

int main() {
    SetConsoleOutputCP(949);
    SetConsoleCP(949);

    srand(time(0));

    int wins = 0;
    int games = 0;

    while (true) {
        games++;
        if (playGame()) {
            wins++;
        }

        cout << "\n전적: " << wins << "승 / " << games << "게임" << endl;

        cout << "\n다시 하시겠습니까? (y/n): ";
        string again;
        cin >> again;

        if (again != "y" && again != "Y") {
            cout << "\n게임을 종료합니다. 감사합니다!" << endl;
            break;
        }
        cout << endl;
    }

    cout << "\n종료하려면 Enter를 누르세요...";
    cin.ignore();
    cin.get();

    return 0;
}
