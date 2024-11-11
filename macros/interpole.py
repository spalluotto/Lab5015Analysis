def interpolate(x1, y1, x2, y2, x):
    y = y1 + ((y2 - y1) / (x2 - x1)) * (x - x1)
    return y

x1, y1 = 0.80, 47.41
x2, y2 = 1.00, 41.29
x = 0.95

y = interpolate(x1, y1, x2, y2, x)
print(f"Il valore di y per x = {x} è: {y}")
