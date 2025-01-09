import time

try:
    for i in range(100):
        print(f"Đang xử lý phần tử {i}")
        time.sleep(1)  # Mô phỏng công việc mất thời gian
except KeyboardInterrupt:
    print("\nĐã dừng vòng lặp do bạn nhấn Ctrl+C!")
