import time

import u6

d = u6.U6()

# === Pin map: verify against the perfboard before running ===
PIN_START = 0   # FIO0 → AZD CN4 START
PIN_M0    = 2   # FIO2 → AZD CN4 M0  (op# bit 0)
PIN_M1    = 3   # FIO3 → AZD CN4 M1  (op# bit 1)
PIN_M2    = 4   # FIO4 → AZD CN4 M2  (op# bit 2)
PIN_STOP  = 1   # FIO1 → AZD CN4 STOP

PULSE_S = 0.05  # START pulse width (≥ 1 ms per AZ manual; 50 ms is generous)
