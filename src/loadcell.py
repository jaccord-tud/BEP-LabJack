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
PRECISION = 4

def voltage_to_force(voltage):
    return (voltage - V_MIN) / (V_MAX - V_MIN) * F_MAX

def calibrate(v):
    global V_MIN
    V_MIN = v

def print_line(t, voltage, force):
    print(f"t={t:.{PRECISION}f} s, V={voltage:.{PRECISION}f} V, F={force:.{PRECISION}f} N")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", action="store_true", help="show live graph")
    parser.add_argument("-f", "--file", nargs="?", const="", default=None, metavar="PATH", help="save to CSV file (omit PATH for datetime-stamped filename)")
    parser.add_argument("-d", "--detached", action="store_true", help="don't write data to stdout")
    parser.add_argument("-p", "--precision", type=int, default=PRECISION, help="decimal places (default: %(default)s)")
    parser.add_argument("-c", "--channel", type=int, default=CHANNEL, help="AIN channel (default: %(default)s)")
    parser.add_argument("-r", "--rate", type=float, default=RATE, help="sample rate in Hz (default: %(default)s)")
    parser.add_argument("--v-min", type=float, default=V_MIN, help="min voltage (default: %(default)s)")
    parser.add_argument("--v-max", type=float, default=V_MAX, help="max voltage (default: %(default)s)")
    return parser.parse_args()

def setup_plot():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Force (N)")
    ax.set_title("Load Cell")
    ax.set_ylim(-0.5, F_MAX + 0.5)
    return plt, ax, line

def update_plot(plt, ax, line, times, forces, t, force):
    times.append(t)
    forces.append(force)
    line.set_data(times, forces)
    ax.set_xlim(max(0, t - WINDOW), t + 1)
    plt.pause(0.0001)

def write_row(writer, t, voltage, force, p):
    writer.writerow([f"{t:0{p+3}.{p}f}", f"{voltage:0{p+3}.{p}f}", f"{force:0{p+3}.{p}f}"])

def main():
    global CHANNEL, RATE, V_MIN, V_MAX, PRECISION
    args = parse_args()
    CHANNEL = args.channel
    RATE = args.rate
    V_MIN = args.v_min
    V_MAX = args.v_max
    PRECISION = args.precision

    save_file = args.file is not None
    csv_file = args.file or f"data/loadcell_{time.strftime('%Y%m%dT%H%M%S')}.csv"

    max_points = int(WINDOW * RATE)
    times = deque(maxlen=max_points)
    forces = deque(maxlen=max_points)

    plt, ax, line = setup_plot() if args.graph else (None, None, None)

    d = u6.U6()
    print(f"Connected: AIN{CHANNEL} @ {RATE} Hz.")
    if save_file: print(f"Logging to {csv_file}.")
    print("Starting measurement (Ctrl+C to stop)...\n")

    def run(writer=None):
        t_start = time.time()
        while True:
            voltage = d.getAIN(CHANNEL)
            force = voltage_to_force(voltage)
            t = time.time() - t_start

            if not args.detached:
                print_line(t, voltage, force)

            if writer:
                write_row(writer, t, voltage, force, PRECISION)

            if args.graph:
                update_plot(plt, ax, line, times, forces, t, force)

            time.sleep(1.0 / RATE)

    try:
        if save_file:
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
        if args.graph:
            plt.ioff()
            plt.show()
        if save_file:
            print(f"CSV saved to {csv_file}")

if __name__ == "__main__":
    main()
