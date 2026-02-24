#include <iostream>
#include <chrono>
#include <thread>
#include <random>

struct Tick {
    double bid;
    double ask;
    double last;
    long long ts;
};

inline long long now_ns() {
    return std::chrono::high_resolution_clock::now()
        .time_since_epoch().count();
}

inline Tick generate_tick() {
    static std::mt19937_64 rng(42);
    static std::uniform_real_distribution<double> dist(6800.0, 6900.0);

    double px = dist(rng);

    Tick t;
    t.bid = px - 0.25;
    t.ask = px + 0.25;
    t.last = px;
    t.ts = now_ns();

    return t;
}

inline void normalize_and_dispatch(const Tick& t) {
    std::cout << "SPX | "
              << t.bid << " / "
              << t.ask << " | "
              << t.last << " | "
              << t.ts << "\n";
}

int main() {
    while (true) {
        Tick t = generate_tick();
        normalize_and_dispatch(t);
        std::this_thread::sleep_for(std::chrono::microseconds(50));
    }
}
