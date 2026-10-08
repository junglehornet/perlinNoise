import math
import random

from PIL import Image
import numpy as np

def lerp(a, b, t):
    return a + (b - a) * t

def smootherstep(t):
    return t*t*t*(6*t*t - 15*t + 10)

def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

print("(1/3) Generating gradient vectors... ", end="", flush=True)
grid = [[[] for i in range(17)] for x in range(17)]
for i in range(17):
    for x in range(17):
        theta = random.randint(0, 360)
        grid[i][x] = [math.cos(math.radians(theta)), math.sin(math.radians(theta))]

print("done!")
print("(2/3) Calculating Height Map... ", end="", flush=True)
bitmap = [[0 for x in range(4096)] for y in range(4096)]
for y in range(4096):
    for x in range(4096):
        gx = x // 256
        gy = y // 256

        offset1 = [(x - gx * 256) / 256,       (y - gy * 256) / 256]
        offset2 = [(x - (gx + 1) * 256) / 256, (y - gy * 256) / 256]
        offset3 = [(x - gx * 256) / 256,       (y - (gy + 1) * 256) / 256]
        offset4 = [(x - (gx + 1) * 256) / 256, (y - (gy + 1) * 256) / 256]

        dp1 = dot_product(grid[gy][gx], offset1)
        dp2 = dot_product(grid[gy][gx + 1], offset2)
        dp3 = dot_product(grid[gy + 1][gx], offset3)
        dp4 = dot_product(grid[gy + 1][gx + 1], offset4)

        xt = (x - gx * 256) / 256
        yt = (y - gy * 256) / 256
        a = lerp(dp1, dp2, smootherstep(xt))
        b = lerp(dp3, dp4, smootherstep(xt))
        v = lerp(a, b, smootherstep(yt))
        bitmap[y][x] = int((v + 1) * 255/2)
print("done!")
print("(3/3) Rendering Image... ", end="", flush=True)
array = np.array(bitmap, np.uint8)
img = Image.fromarray(array, "L")
img.save("perlin-noise.png", format="PNG")
print("done!")
print("image saved as perlin-noise.png")
