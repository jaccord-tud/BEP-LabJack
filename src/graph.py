import time
import u6
import csv
import matplotlib.pyplot as plt
from collections import deque

# Connect to LabJack U6
d = u6.U6()
print("Connected to U6\n")

# Define voltage and force range
V_min = 0.0048
V_max = 10
F_max = 10

# Convert voltage (V) to force (N)
def volt_to_newton(V):
    return (V - V_min) / (V_max - V_min) * F_max

# Rolling window
max_points = 200
times = deque(maxlen=max_points)
forces = deque(maxlen=max_points)

# Set up graph
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Force (N)")
ax.set_title("Loadcell")
ax.set_ylim(-0.5, F_max + 0.5)

# Define filename
filename = f"data/loadcell_{time.strftime('%Y%m%dT%H%M%S')}.csv"

# Log loop
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time (s)", "voltage (V)", "force (N)"])

    print(f"Logging to {filename}. Ctrl+C to stop.\n")
    t_start = time.time()

    try:
        while True:
            # Read AIN0 input voltage
            voltage = d.getAIN(0)
            # Calculate force
            force = volt_to_newton(voltage)
            # Calculate time
            t = time.time() - t_start

            # Write values to file
            writer.writerow([f"{t:.4f}", f"{voltage:.4f}", f"{force:.4f}"])
            print(f"t={t:.4f} V={force:.4f} F={force:.4f}")

            # Append values to array
            times.append(t)
            forces.append(force)

            # Plot data
            line.set_data(times, forces)
            ax.set_xlim(max(0, t - 10), t + 1)
            plt.pause(0.1)

            # Sleep
            # time.sleep(0.1) # 100 ms sample rate

    except KeyboardInterrupt:
        print("\nStopping...")
        print(f"\nSaved to {filename}")
    finally:
        d.close()
        plt.ioff()
        plt.show()
