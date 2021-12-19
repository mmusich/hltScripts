#include <iostream>
#include <atomic>

int main(int argc, char** argv){

  std::atomic<uint64_t> maxPrescale = 10;

  uint64_t dynPrescale = 100;

  auto tMaxPrescale = maxPrescale.load();
  while (maxPrescale < dynPrescale) {
    std::cout << "A " <<
      maxPrescale << " " << tMaxPrescale << " " << dynPrescale
      << std::endl;

    maxPrescale.compare_exchange_strong(tMaxPrescale, dynPrescale);

    std::cout << "B " <<
      maxPrescale << " " << tMaxPrescale << " " << dynPrescale
      << std::endl;
  }

  return 0;
}
