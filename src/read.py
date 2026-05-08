import argparse
import time
import u6

CHANNEL = 0
RATE = 20.0
V_MIN = 0.0
V_MAX = 10.0
F_MAX = 10.0
PRECISION = 4

def voltage_to_force(V):
    return (V - V_MIN) / (V_MAX - V_MIN) * F_MAX

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--precision", type=int, default=PRECISION, help="decimal places (default: %(default)s)")
    parser.add_argument("-c", "--channel", type=int, default=CHANNEL, help="AIN channel (default: %(default)s)")
    parser.add_argument("-r", "--rate", type=float, default=RATE, help="sample rate in Hz (default: %(default)s)")
    parser.add_argument("--v-min", type=float, default=V_MIN, help="min voltage (default: %(default)s)")
    parser.add_argument("--v-max", type=float, default=V_MAX, help="max voltage (default: %(default)s)")
    args = parser.parse_args()
    p = args.precision

    d = u6.U6()
    print(f"Connected: AIN{args.channel} @ {args.rate} Hz. Press Ctrl+C to stop.\n")

    t_start = time.time()
    try:
        while True:
            voltage = d.getAIN(args.channel)
            force = (voltage - args.v_min) / (args.v_max - args.v_min) * F_MAX
            t = time.time() - t_start
            print(f"\rt={t:0{p+3}.{p}f} s  V={voltage:0{p+3}.{p}f} V  F={force:0{p+3}.{p}f} N    ", end="", flush=True)
            time.sleep(1.0 / args.rate)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        d.close()

if __name__ == "__main__":
    main()
