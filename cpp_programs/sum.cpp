#include <iostream>
#include <locale>
#include <windows.h>

int main() {
    SetConsoleOutputCP(949);
    SetConsoleCP(949);

    int sum = 0;

    for (int i = 1; i <= 100; i++) {
        sum += i;
    }

    std::cout << "1부터 100까지의 합: " << sum << std::endl;

    std::cout << "\n종료하려면 Enter를 누르세요...";
    std::cin.get();

    return 0;
}
