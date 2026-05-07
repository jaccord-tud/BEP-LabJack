import time
import u6

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

# Read loop
try:
    while True:
        # Read AIN0 input voltage
        voltage = d.getAIN(0)
        # Calculate force
        force = volt_to_newton(voltage)
        # Print values
        print(f"AIN0: {voltage:.4f} V    {force:.4f} N")
        # Sleep
        time.sleep(0.1) # 100 ms sample rate

except KeyboardInterrupt:
    print("\n Stopping...")
finally:
    d.close()

