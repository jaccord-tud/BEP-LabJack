"""
"""

import argparse
import csv
import time
from collections import deque

import u6

CHANNEL = 0     # AIN channel
RATE = 20.0     # Hz
WINDOW = 10     # seconds, rolling plot
V_MIN = 0.0     # Volts
V_MAX = 10.0
F_MAX = 10.0    # Newton

def voltage_to_force(V):
    return (V - V_MIN) / (V_MAX - V_MIN) * F_MAX

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", action="store_true", help="show live graph")
    parser.add_argument("-f", action="store_true", help="save to CSV file")
    parser.add_argument("-d", action="store_true", help="detached: don't write data to stdout")
    return parser.parse_args()

def main():
    args = parse_args()

    file_stem = f"loadcell_{time.strftime('%Y%m%dT%H%M%S')}"
    csv_file = f"{file_stem}.csv"

    max_points = int(WINDOW * RATE)
    times = deque(maxlen=max_points)
    forces = deque(maxlen=max_points)
    all_times = []
    all_forces = []

    if args.g:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        line, = ax.plot([], [])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Force (N)")
        ax.set_title("Load Cell")
        ax.set_ylim(-0.5, F_MAX + 0.5)

    d = u6.U6()
    print(f"Connected: AIN{CHANNEL} @ {RATE} Hz.")

    if args.f: print(f"Logging to {csv_file}.")

    print("Starting measurement (Ctrl+C to stop)...\n")

    def run(writer=None):
        t_start = time.time()
        while True:
            voltage = d.getAIN(CHANNEL)
            force = voltage_to_force(voltage)
            t = time.time() - t_start

            if not args.d:
                print(f"t={t:.4f} s, V={voltage:.4f} V, F={force:.4f} N")

            if writer:
                writer.writerow([f"{t:.4f}", f"{voltage:.4f}", f"{force:.4f}"])

            all_times.append(t)
            all_forces.append(force)

            if args.g:
                times.append(t)
                forces.append(force)
                line.set_data(times, forces)
                ax.set_xlim(max(0, t - WINDOW), t + 1)
                plt.pause(0.0001)

            time.sleep(1.0 / RATE)

    try:
        if args.f:
            with open(csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["time (s)", "voltage (V)", "force (N)"])
                run(writer)
        else:
            run()

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        d.close()
        if args.g:
            plt.ioff()
            plt.show()

        if args.f:
            print(f"CSV saved to {csv_file}")

if __name__ == "__main__":
    main()

