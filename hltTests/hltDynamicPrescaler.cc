#include <iostream>
#include <cmath>
#include <vector>
#include <chrono>
#include <atomic>

void impl1(uint const evtn, std::vector<bool>& ret){
  std::vector<bool> res(evtn);

  std::atomic<uint> m_count = 0;
  std::atomic<uint> m_scale = 1;

  for(uint idx=0; idx<evtn; ++idx){
    ++m_count;

    if (m_count % m_scale){
      res[idx] = false;
      continue;
    }

    if (m_count == m_scale * 10){
      m_scale = m_scale * 10;
    }

    res[idx] = true;
  }

  ret = std::move(res);
}

void impl2(uint const evtn, std::vector<bool>& ret){
  std::vector<bool> res(evtn);

  std::atomic<uint> m_count = 0;

  for(uint idx=0; idx<evtn; ++idx){
    auto count = ++m_count;

    uint dynamicScale = 1;
    while (count > dynamicScale * 10) {
      dynamicScale *= 10;
    }

    res[idx] = (0 == count % dynamicScale);
  }

  ret = std::move(res);
}

void impl3(uint const evtn, std::vector<bool>& ret){
  std::vector<bool> res(evtn);

  uint m_count = 0;

  for(uint idx=0; idx<evtn; ++idx){
    auto count = ++m_count;

    uint const dynamicScale = powf(10.f, int(log10f(count)));

    res[idx] = (0 == count % dynamicScale);
  }

  ret = std::move(res);
}

int main(int argc, char** argv){
  if(argc != 2) return 1;

  auto const evtN = atoi(argv[1]);

  auto t0 = std::chrono::steady_clock::now();

  std::vector<bool> ret1;
  impl1(evtN, ret1);
  auto t1 = std::chrono::steady_clock::now();

  std::vector<bool> ret2;
  impl2(evtN, ret2);
  auto t2 = std::chrono::steady_clock::now();

//  std::vector<bool> ret3;
//  impl3(evtN, ret3);
//  auto t3 = std::chrono::steady_clock::now();

  std::chrono::duration<double> const t10 = t1-t0;
  std::chrono::duration<double> const t21 = t2-t1;
//  std::chrono::duration<double> const t32 = t3-t2;
  std::cout << "t1 - t0 [sec]: " << t10.count() << std::endl;
  std::cout << "t2 - t1 [sec]: " << t21.count() << std::endl;
//  std::cout << "t3 - t2 [sec]: " << t32.count() << std::endl;

  for(uint idx=0; idx<evtN; ++idx){
    if (ret1[idx] == ret2[idx] //and ret1[idx] == ret3[idx]
    ) continue;

    std::cout << idx << " " << ret1[idx] << " " << ret2[idx]
//      << " " << ret3[idx]
      << std::endl;
    break;
  }

  std::cout << "Done: " << evtN << std::endl;

  return 0;
}
