import math

x = 1.2756981093162
y = 0.000000000000001
while True:
    ans = 3*x-4*math.sin(x)
    if ans < y and ans > -y:
        print(x, ans)
    x += y
    if x > 1.2756981093164:
        break
