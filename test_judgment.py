from app.core.judgment import Judgment


judgment = Judgment()


# =====================================
# Limit MODEL-A
# =====================================

voltage_lower = 23.00
voltage_upper = 25.00

current_lower = 0.100
current_upper = 0.200


# =====================================
# Test 1
# =====================================

result = judgment.check(
    voltage=24.00,
    current=0.150,
    voltage_lower=voltage_lower,
    voltage_upper=voltage_upper,
    current_lower=current_lower,
    current_upper=current_upper
)

print("Test 1:")
print("Voltage = 24.00 V")
print("Current = 0.150 A")
print("Judgment =", result)


# =====================================
# Test 2
# =====================================

result = judgment.check(
    voltage=22.50,
    current=0.150,
    voltage_lower=voltage_lower,
    voltage_upper=voltage_upper,
    current_lower=current_lower,
    current_upper=current_upper
)

print("\nTest 2:")
print("Voltage = 22.50 V")
print("Current = 0.150 A")
print("Judgment =", result)


# =====================================
# Test 3
# =====================================

result = judgment.check(
    voltage=24.00,
    current=0.250,
    voltage_lower=voltage_lower,
    voltage_upper=voltage_upper,
    current_lower=current_lower,
    current_upper=current_upper
)

print("\nTest 3:")
print("Voltage = 24.00 V")
print("Current = 0.250 A")
print("Judgment =", result)


# =====================================
# Test 4 - boundary
# =====================================

result = judgment.check(
    voltage=23.00,
    current=0.100,
    voltage_lower=voltage_lower,
    voltage_upper=voltage_upper,
    current_lower=current_lower,
    current_upper=current_upper
)

print("\nTest 4:")
print("Voltage = 23.00 V")
print("Current = 0.100 A")
print("Judgment =", result)