"""Recompute every number used in the worked examples of chapters 5-12.

Usage: python -I verify_examples.py   -> prints each result; exits non-zero if a value in a script is wrong.
The asserted values are the ones shown on slides / spoken in scripts/ch05..ch12.json.
"""
import math
import sys
from itertools import product

import numpy as np


def close(actual: float, expected: float, tol: float = 5e-3) -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"expected {expected}, computed {actual}")


def ch05() -> None:
    # Huffman, slide example
    p = {"a2": 0.4, "a6": 0.3, "a1": 0.1, "a4": 0.1, "a3": 0.06, "a5": 0.04}
    code = {"a2": "1", "a6": "00", "a1": "011", "a4": "0100", "a3": "01010", "a5": "01011"}
    words = list(code.values())
    assert not any(a != b and b.startswith(a) for a, b in product(words, words)), "not a prefix code"
    l_avg = sum(p[s] * len(code[s]) for s in p)
    entropy = -sum(q * math.log2(q) for q in p.values())
    close(l_avg, 2.2)
    close(entropy, 2.14)
    close(-math.log2(0.4), 1.32)
    close(-math.log2(0.04), 4.64)
    print(f"ch05 Huffman: L_avg={l_avg:.2f} bits, H={entropy:.3f} bits, fixed=3 bits")

    # BTC on a 4x4 block
    block = np.array([[121, 114, 56, 47], [37, 200, 247, 255], [16, 0, 12, 169], [43, 5, 7, 251]], dtype=float)
    k = block.size
    m1, m2 = block.mean(), (block ** 2).mean()
    sigma = math.sqrt(m2 - m1 ** 2)
    bitmap = (block >= m1).astype(int)
    q = int(bitmap.sum())
    a = m1 - sigma * math.sqrt(q / (k - q))
    b = m1 + sigma * math.sqrt((k - q) / q)
    close(m1, 98.75)
    close(sigma, 92.95, 0.01)
    assert q == 7 and bitmap.tolist() == [[1, 1, 0, 0], [0, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    close(a, 16.8, 0.06)
    close(b, 204.1, 0.06)
    decoded = np.where(bitmap == 1, round(b), round(a))
    close(decoded.mean(), 98.8, 0.1)
    print(f"ch05 BTC: mean={m1}, sigma={sigma:.2f}, q={q}, a={a:.2f}, b={b:.2f}, bits={k + 16} vs {k * 8}")
    assert k + 16 == 32 and k * 8 == 128

    # Arithmetic coding, slide example a1 a2 a3 a3 a4
    ranges = {"a1": (0.0, 0.2), "a2": (0.2, 0.4), "a3": (0.4, 0.8), "a4": (0.8, 1.0)}
    low, high, steps = 0.0, 1.0, []
    for symbol in ["a1", "a2", "a3", "a3", "a4"]:
        width = high - low
        low, high = low + width * ranges[symbol][0], low + width * ranges[symbol][1]
        steps.append((round(low, 5), round(high, 5)))
    assert steps == [(0.0, 0.2), (0.04, 0.08), (0.056, 0.072), (0.0624, 0.0688), (0.06752, 0.0688)], steps
    close(high - low, 0.2 * 0.2 * 0.4 * 0.4 * 0.2, 1e-9)
    print("ch05 arithmetic:", steps)

    # JPEG quantisation of three coefficients
    for coeff, step, level, back in [(236, 16, 15, 240), (-23, 11, -2, -22), (12, 99, 0, 0)]:
        assert round(coeff / step) == level and level * step == back
    print("ch05 JPEG quantisation ok")


def ch06() -> None:
    bytes_per_frame = 352 * 288 * 1.5
    mbps = bytes_per_frame * 8 * 30 / 1e6
    assert bytes_per_frame == 152064
    close(mbps, 36.5, 0.01)
    close(mbps / 1.5, 24.3, 0.05)
    print(f"ch06 raw CIF: {mbps:.2f} Mbps")

    ref = np.array([[1, 1, 2, 2], [1, 9, 8, 2], [1, 7, 9, 2], [1, 1, 2, 2]])
    cur = np.array([[9, 8], [7, 10]])  # block located at rows 1-2, cols 2-3 of the current frame
    sad = {name: int(np.abs(ref[r:r + 2, c:c + 2] - cur).sum())
           for name, (r, c) in {"same": (1, 2), "left1": (1, 1), "up1": (0, 2), "left1up1": (0, 1)}.items()}
    assert sad == {"same": 17, "left1": 1, "up1": 22, "left1up1": 18}, sad
    residual = cur - ref[1:3, 1:3]
    assert residual.tolist() == [[0, 0], [0, 1]]
    print("ch06 block matching SAD:", sad)


def ch07() -> None:
    f, c = 0.4, 2
    after = f * c
    alias = abs(after - round(after))
    close(after, 0.8)
    close(alias, 0.2)
    close(1 / (2 * c), 0.25)
    top = 10 + 0.25 * (20 - 10)
    bottom = 30 + 0.25 * (40 - 30)
    value = top + 0.75 * (bottom - top)
    assert (top, bottom, value) == (12.5, 32.5, 27.5)
    up = np.zeros(5)
    up[::2] = [10, 20, 30]
    smooth = np.convolve(up, [0.5, 1, 0.5], mode="same")
    assert smooth.tolist() == [10, 15, 20, 25, 30]
    print("ch07 aliasing 0.4 -> 0.8 -> 0.2; bilinear 27.5; upsample", smooth.tolist())


def ch08() -> None:
    thresholds = np.array([[32, 159], [223, 96]])
    out = (np.full((2, 2), 100) > thresholds).astype(int)
    assert out.tolist() == [[1, 0], [0, 1]]
    close(out.mean() * 255, 127.5)

    error, outputs, states = 0, [], []
    for pixel in [100, 100, 100, 100]:
        u = pixel + error
        b = 255 if u >= 128 else 0
        error = u - b
        outputs.append(b)
        states.append((u, b, error))
    assert states == [(100, 0, 100), (200, 255, -55), (45, 0, 45), (145, 255, -110)], states
    print("ch08 dithering", out.tolist(), "| error diffusion", states)

    colours = sorted([10, 12, 20, 22, 100, 110, 200, 220])
    boxes = [colours[:2], colours[2:4], colours[4:6], colours[6:]]
    assert [sum(b) / 2 for b in boxes] == [11, 21, 105, 210]

    x = np.array([100, 110, 100, 110], dtype=float)
    for name, y, s_expected, ssim_expected in [("shift", x + 10, 1.0, 0.996), ("flip", x + np.array([10, -10, 10, -10]), -1.0, -1.0)]:
        mse = ((x - y) ** 2).mean()
        assert mse == 100
        lum = 2 * x.mean() * y.mean() / (x.mean() ** 2 + y.mean() ** 2)
        con = 2 * x.std(ddof=1) * y.std(ddof=1) / (x.var(ddof=1) + y.var(ddof=1))
        struct = np.cov(x, y, ddof=1)[0, 1] / (x.std(ddof=1) * y.std(ddof=1))
        close(struct, s_expected)
        close(lum * con * struct, ssim_expected, 2e-3)
        print(f"ch08 {name}: MSE={mse}, l={lum:.4f}, c={con:.2f}, s={struct:.2f}, SSIM={lum * con * struct:.4f}")
    close(2 * 105 * 115 / (105 ** 2 + 115 ** 2), 0.996, 1e-3)


def ch09() -> None:
    values = np.array([1, 2, 3, 10, 11, 12], dtype=float)
    centres, history = np.array([1.0, 2.0]), []
    while True:
        labels = np.abs(values[:, None] - centres[None, :]).argmin(axis=1)
        updated = np.array([values[labels == j].mean() for j in range(2)])
        history.append((labels.tolist(), updated.tolist()))
        if np.allclose(updated, centres):
            break
        centres = updated
    assert history[0] == ([0, 1, 1, 1, 1, 1], [1.0, 7.6]), history
    assert history[1] == ([0, 0, 0, 1, 1, 1], [2.0, 11.0]), history
    assert len(history) == 3 and history[2][1] == [2.0, 11.0]
    print("ch09 k-means:", history)

    def slic(dc: float, ds: float, c: float, s: float = 10) -> float:
        return math.sqrt(dc ** 2 + (ds / s) ** 2 * c ** 2)
    close(slic(4, 8, 1), 4.08)
    close(slic(8, 2, 1), 8.00)
    close(slic(4, 8, 20), 16.49)
    close(slic(8, 2, 20), 8.94)

    w = np.zeros((5, 5))
    for (i, j), weight in {(0, 1): 9, (2, 3): 8, (0, 2): 1, (1, 3): 2, (3, 4): 1}.items():
        w[i, j] = w[j, i] = weight
    degree = w.sum(axis=1)
    assert degree.tolist() == [10, 11, 9, 11, 1]

    def ncut(a: list[int]) -> tuple[float, float]:
        b = [n for n in range(5) if n not in a]
        cut = w[np.ix_(a, b)].sum()
        return cut, cut / degree[a].sum() + cut / degree[b].sum()
    cut_small, ncut_small = ncut([4])
    cut_good, ncut_good = ncut([0, 1])
    assert (cut_small, cut_good) == (1, 3)
    close(ncut_small, 1.02)
    close(ncut_good, 0.29)
    nassoc = (21 - 3) / 21 + (21 - 3) / 21
    close(2 - nassoc, ncut_good, 1e-9)
    close(nassoc, 1.71)
    print(f"ch09 graph: cut {{5}}={cut_small}, Ncut={ncut_small:.3f}; cut {{1,2}}={cut_good}, Ncut={ncut_good:.3f}")

    f1 = np.array([[10, 10, 10], [10, 200, 10], [10, 10, 10]])
    f2 = np.array([[10, 10, 10], [10, 12, 200], [10, 10, 10]])
    diff = (np.abs(f1 - f2) > 20).astype(int)
    assert diff.tolist() == [[0, 0, 0], [0, 1, 1], [0, 0, 0]]


def ch10() -> None:
    def first_difference(chain: list[int]) -> list[int]:
        return [(chain[i] - chain[i - 1]) % 4 for i in range(len(chain))]

    def shape_number(chain: list[int]) -> list[int]:
        diff = first_difference(chain)
        return min(diff[i:] + diff[:i] for i in range(len(diff)))
    assert first_difference([0, 3, 2, 1]) == [3, 3, 3, 3]
    assert first_difference([0, 0, 3, 2, 2, 1]) == [3, 0, 3, 3, 0, 3]
    assert shape_number([0, 0, 3, 2, 2, 1]) == [0, 3, 3, 0, 3, 3]
    assert shape_number([3, 3, 2, 1, 1, 0]) == [0, 3, 3, 0, 3, 3]  # same rectangle rotated by 90 degrees

    s = np.array([0, 1, 1 + 1j, 1j])
    a = np.fft.fft(s)
    assert np.allclose(a, [2 + 2j, -2 - 2j, 0, 0])
    moved = np.fft.fft(s + 3)
    assert np.allclose(moved, [14 + 2j, -2 - 2j, 0, 0])
    scaled = np.fft.fft(2 * s)
    assert np.allclose(np.abs(scaled[1]) / np.abs(a[1]), 2)
    close(abs(a[1]), 2.83)
    print("ch10 Fourier descriptors:", np.round(a, 3).tolist())

    close(16 ** 2 / 16, 16)
    close(4 * math.pi, 12.57)
    close(20 ** 2 / 16, 25)

    image = [[1, 1, 2], [1, 2, 2], [3, 3, 1]]
    g = np.zeros((3, 3), dtype=int)
    for row in image:
        for left, right in zip(row, row[1:]):
            g[left - 1, right - 1] += 1
    assert g.tolist() == [[1, 2, 0], [0, 1, 0], [1, 0, 1]] and g.sum() == 6
    print("ch10 GLCM:", g.tolist())

    pts = [(1, 1), (2, 1), (3, 1), (2, 2)]
    m00, m10, m01 = len(pts), sum(x for x, _ in pts), sum(y for _, y in pts)
    assert (m00, m10, m01) == (4, 8, 5)
    xc, yc = m10 / m00, m01 / m00
    assert (xc, yc) == (2, 1.25)
    mu20 = sum((x - xc) ** 2 for x, _ in pts)
    mu02 = sum((y - yc) ** 2 for _, y in pts)
    assert (mu20, mu02) == (2, 0.75)
    shifted = [(x + 5, y + 3) for x, y in pts]
    xs = sum(x for x, _ in shifted) / 4
    assert sum((x - xs) ** 2 for x, _ in shifted) == mu20


def ch11() -> None:
    def iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, float]:
        iw = max(0, min(a[2], b[2]) - max(a[0], b[0]))
        ih = max(0, min(a[3], b[3]) - max(a[1], b[1]))
        inter = iw * ih
        union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
        return inter, union, inter / union
    assert iou((0, 0, 4, 4), (2, 2, 6, 6))[:2] == (4, 28)
    close(iou((0, 0, 4, 4), (2, 2, 6, 6))[2], 0.14)
    assert iou((0, 0, 4, 4), (1, 0, 5, 4))[:2] == (12, 20)
    close(iou((0, 0, 4, 4), (1, 0, 5, 4))[2], 0.6)

    hits, truths = [1, 0, 1, 1, 0], 4
    tp, precision, recall = 0, [], []
    for n, hit in enumerate(hits, start=1):
        tp += hit
        precision.append(tp / n)
        recall.append(tp / truths)
    assert [round(v, 2) for v in precision] == [1.0, 0.5, 0.67, 0.75, 0.6]
    assert recall == [0.25, 0.25, 0.5, 0.75, 0.75]
    ap, previous = 0.0, 0.0
    for level in sorted(set(recall)):
        best = max(p for p, r in zip(precision, recall) if r >= level)
        ap += (level - previous) * best
        previous = level
    close(ap, 0.625, 1e-9)
    close((0.625 + 0.875) / 2, 0.75, 1e-9)
    windows = ((640 - 64) // 8 + 1) * ((480 - 64) // 8 + 1)
    assert windows == 73 * 53 == 3869
    print(f"ch11 IoU 4/28, 12/20; AP={ap}; windows={windows}")


def ch12() -> None:
    m1, m2, x = np.array([4.3, 1.3]), np.array([1.5, 0.3]), np.array([3.0, 1.0])
    close(np.linalg.norm(x - m1), 1.33)
    close(np.linalg.norm(x - m2), 1.66)
    d1 = m1 @ x - 0.5 * m1 @ m1
    d2 = m2 @ x - 0.5 * m2 @ m2
    close(0.5 * m1 @ m1, 10.09)
    close(0.5 * m2 @ m2, 1.17)
    close(d1, 4.11)
    close(d2, 3.63)

    close(0.2 * 0.7, 0.14, 1e-9)
    close(0.6 * 0.3, 0.18, 1e-9)
    close(0.14 / 0.32, 0.4375, 1e-9)
    close(0.18 / 0.32, 0.5625, 1e-9)

    # Perceptron rule from the slide, alpha = 1, start at zero; class c1 wants a positive output
    samples = [((0, 0), 1), ((0, 1), 1), ((1, 0), 2), ((1, 1), 2)]
    w, bias, log = np.zeros(2), 0.0, []
    for _epoch in range(20):
        changed = False
        for point, label in samples:
            out = w @ np.array(point) + bias
            if label == 1 and out <= 0:
                w, bias, changed = w + np.array(point), bias + 1, True
            elif label == 2 and out >= 0:
                w, bias, changed = w - np.array(point), bias - 1, True
            log.append((point, label, float(out), w.tolist(), bias))
        if not changed:
            break
    first = [(entry[2], entry[3], entry[4]) for entry in log[:4]]
    assert first == [(0.0, [0.0, 0.0], 1.0), (1.0, [0.0, 0.0], 1.0), (1.0, [-1.0, 0.0], 0.0), (-1.0, [-1.0, 0.0], 0.0)], first
    assert (w.tolist(), bias) == ([-2.0, 0.0], 1.0), (w, bias)
    updates = sum(1 for i, e in enumerate(log) if (e[3], e[4]) != ((log[i - 1][3], log[i - 1][4]) if i else ([0.0, 0.0], 0.0)))
    print(f"ch12 perceptron: final w={w.tolist()}, bias={bias}, checks={len(log)}, updates={updates}")
    for step in log[4:]:
        print("   ", step)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for check in (ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12):
        check()
    print("all worked-example numbers verified")
