import time

import u6

# (CN4, perfboard connector, LabJack DSUB, Python IO pin)
# labjack in
# 9 -> 5 -> EIO2 -> 10
# labjack out
# 1 -> 1 -> EIO7 -> 15
# 13 -> 2 -> EIO6 -> 14
# 2 -> 3 -> EIO5 -> 13
# 14 -> 4 -> EIO4 -> 12

d = u6.U6()
print("Press Ctrl+C to stop.\n")

try:
    while True:
        # p1  = d.getDIOState(15)
        # p2  = d.getDIOState(13)
        # p9  = d.getDIOState(10)
        # p13 = d.getDIOState(14)
        # p14 = d.getDIOState(12)
        # print(f"\r1={p1}  2={p2}  9={p9}  13={p13}  14={p14}    ", end="", flush=True)
        states = [d.getDIOState(i) for i in range(16)]
        print(f"\r{'  '.join(f'{i}={states[i]}' for i in range(16))}    ", end="", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    d.close()
