import threading
import time

class ComplexObject:
    def __init__(self):
        self.data = {"a": 0, "b": 0, "c": 0}

    def unsafe_update(self, key):
        old_value = self.data.get(key, 0)
        time.sleep(0)          # 强制切换点
        new_value = old_value + 1
        self.data[key] = new_value

obj = ComplexObject()
n_threads = 20
n_iterations = 50000
key = "a"

def complex_worker():
    for _ in range(n_iterations):
        obj.unsafe_update(key)

threads = [threading.Thread(target=complex_worker) for _ in range(n_threads)]

t0 = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
t1 = time.perf_counter()

expected = n_threads * n_iterations
actual = obj.data[key]
print(f"Key '{key}' - Expected: {expected}, Actual: {actual}")
print(f"Lost updates: {expected - actual}")
print(f"Time: {t1 - t0:.3f}s")