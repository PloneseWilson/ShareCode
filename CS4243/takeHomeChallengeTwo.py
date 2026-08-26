# Modify input_path="takeHomeTwo.jpg" in main function for your data path

import cv2
import numpy as np


def non_max_suppression(magnitude, angle):
    H, W = magnitude.shape
    out = np.zeros((H, W), dtype=np.float32)
    angle = angle % 180

    for y in range(1, H - 1):
        for x in range(1, W - 1):
            a = angle[y, x]
            m = magnitude[y, x]

            if (0 <= a < 22.5) or (157.5 <= a <= 180):
                n1, n2 = magnitude[y, x - 1], magnitude[y, x + 1]
            elif 22.5 <= a < 67.5:
                n1, n2 = magnitude[y - 1, x + 1], magnitude[y + 1, x - 1]
            elif 67.5 <= a < 112.5:
                n1, n2 = magnitude[y - 1, x], magnitude[y + 1, x]
            else:
                n1, n2 = magnitude[y - 1, x - 1], magnitude[y + 1, x + 1]

            if m >= n1 and m >= n2:
                out[y, x] = m

    return out


def hysteresis_threshold_link(nms, low_threshold, high_threshold):
    strong = 255
    weak = 75

    result = np.zeros_like(nms, dtype=np.uint8)
    result[nms >= high_threshold] = strong
    result[(nms >= low_threshold) & (nms < high_threshold)] = weak

    H, W = result.shape
    stack = list(zip(*np.where(result == strong)))
    visited = np.zeros_like(result, dtype=bool)
    visited[result == strong] = True

    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),         (0, 1),
                 (1, -1),  (1, 0), (1, 1)]

    while stack:
        y, x = stack.pop()
        for dy, dx in neighbors:
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                if result[ny, nx] == weak:
                    result[ny, nx] = strong
                    visited[ny, nx] = True
                    stack.append((ny, nx))

    result[result != strong] = 0
    return result


def make_coloring_page_canny(input_path, output_path,
                              low_threshold=50, high_threshold=150,
                              blur_ksize=5):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, h = 10)

    clahe = cv2.createCLAHE(clipLimit=10, tileGridSize=(8, 8))
    contrasted = clahe.apply(denoised)

    blurred = cv2.GaussianBlur(contrasted, (blur_ksize, blur_ksize), 0)

    gx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.hypot(gx, gy)
    angle = np.degrees(np.arctan2(gy, gx))

    nms = non_max_suppression(magnitude, angle)
    edges = hysteresis_threshold_link(nms, low_threshold, high_threshold)

    cv2.imwrite(output_path, edges)
    return output_path


if __name__ == "__main__":
    make_coloring_page_canny(
        input_path="takeHomeTwo.jpg",
        output_path="output.png",
        low_threshold=50,
        high_threshold=150,
        blur_ksize=5
    )
