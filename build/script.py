import time

counter = 0
# while True:
for _ in range(10):
    print(counter, flush=True)
    counter = counter + 1
    time.sleep(0.1)
