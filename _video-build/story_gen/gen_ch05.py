"""Authoring helper: writes _video-build/scripts/ch05.json (story format).

Coordinates for the Huffman tree, the LBG scatter and the arithmetic-coding intervals are computed here
so the JSON stays consistent with the numbers checked in verify_examples.py.
"""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "scripts" / "ch05.json"

CHAIN = ["Entropy", "Huffman", "Mã số học", "BTC", "VQ / LBG", "JPEG", "Wavelet / JPEG2000", "Hậu xử lý",
         "Đa phổ & học sâu"]


def P(say, text=None, reveal=None, ask=False):
    point = {"say": say}
    if text:
        point["text"] = text
    if reveal is not None:
        point["reveal"] = reveal
    if ask:
        point["ask"] = True
    return point


def S(kicker, title, points, **extra):
    return {"kicker": kicker, "title": title, "points": points, **extra}


def traps(rows, says):
    return S("Bẫy thi", "Bẫy thi", [P(s) for s in says], table={"headers": ["Câu hỏi", "Đáp án"], "rows": rows})


def limit(title, points, next_index):
    return S("Hạn chế", title, points, chain={"items": CHAIN, "current": next_index})


def pipeline(labels, steps):
    nodes = [{"id": f"n{i}", "label": label, "x": 0, "y": i, "shape": "box", "step": step}
             for i, (label, step) in enumerate(zip(labels, steps))]
    edges = [{"a": f"n{i}", "b": f"n{i + 1}", "step": steps[i + 1]} for i in range(len(labels) - 1)]
    return {"nodes": nodes, "edges": edges, "arrows": True}


# ---------- Huffman tree (slide example) ----------
LEAVES = {"a2": ("a2 · 0,4", 8, 1), "a6": ("a6 · 0,3", 1, 2), "a1": ("a1 · 0,1", 7, 3), "a4": ("a4 · 0,1", 2.5, 4),
          "a3": ("a3 · 0,06", 4.5, 5), "a5": ("a5 · 0,04", 6.5, 5)}
MERGED = {"X1": ("0,1", 5.5, 4, 1), "X2": ("0,2", 4, 3, 2), "X3": ("0,3", 5, 2, 3), "X4": ("0,6", 3, 1, 4),
          "R": ("1", 5, 0, 5)}
# parent: (left child -> bit 0, right child -> bit 1)
CHILDREN = {"X1": ("a3", "a5"), "X2": ("a4", "X1"), "X3": ("X2", "a1"), "X4": ("a6", "X3"), "R": ("X4", "a2")}


def huffman_build():
    nodes = [{"id": k, "label": lab, "x": x, "y": y, "shape": "box"} for k, (lab, x, y) in LEAVES.items()]
    nodes += [{"id": k, "label": lab, "x": x, "y": y, "shape": "box", "step": st} for k, (lab, x, y, st) in MERGED.items()]
    edges = [{"a": parent, "b": child, "step": MERGED[parent][3]} for parent, kids in CHILDREN.items() for child in kids]
    return {"nodes": nodes, "edges": edges, "caption": "Mỗi lần ghép hai nút nhỏ nhất thành một nút mới"}


def huffman_codes():
    order = {"a2": 1, "a6": 2, "a1": 3, "a4": 4, "a3": 5, "a5": 5}
    parent_of = {child: parent for parent, kids in CHILDREN.items() for child in kids}
    first_use: dict[tuple[str, str], int] = {}
    for leaf, step in order.items():
        node = leaf
        while node in parent_of:
            key = (parent_of[node], node)
            first_use[key] = min(first_use.get(key, 99), step)
            node = parent_of[node]
    nodes = [{"id": k, "label": lab, "x": x, "y": y, "shape": "box", "marks": [{"step": order[k], "style": "accent"}]}
             for k, (lab, x, y) in LEAVES.items()]
    nodes += [{"id": k, "label": lab, "x": x, "y": y, "shape": "box"} for k, (lab, x, y, _) in MERGED.items()]
    edges = [{"a": parent, "b": child, "label": str(bit), "marks": [{"step": first_use[(parent, child)], "style": "accent"}]}
             for parent, kids in CHILDREN.items() for bit, child in enumerate(kids)]
    return {"nodes": nodes, "edges": edges, "caption": "Trái = 0, phải = 1"}


# ---------- arithmetic coding (slide example) ----------
PROBS = [("a1", 0.0, 0.2), ("a2", 0.2, 0.4), ("a3", 0.4, 0.8), ("a4", 0.8, 1.0)]


def intervals():
    rows, low, high = [], 0.0, 1.0
    for step, symbol in enumerate(["a1", "a2", "a3", "a3", "a4"], start=1):
        width = high - low
        parts = [[name, round(low + width * a, 6), round(low + width * b, 6)] for name, a, b in PROBS]
        rows.append({"low": round(low, 6), "high": round(high, 6), "parts": parts, "pick": symbol, "step": step})
        a, b = next((a, b) for name, a, b in PROBS if name == symbol)
        low, high = low + width * a, low + width * b
    rows.append({"low": round(low, 6), "high": round(high, 6), "parts": [["cả thông điệp", round(low, 6), round(high, 6)]],
                 "step": 6})
    return {"rows": rows, "caption": "Mỗi tầng phóng to phần vừa chọn"}


# ---------- LBG on 8 two-pixel blocks ----------
DARK = [(1, 2), (2, 1), (2, 3), (3, 2)]
BRIGHT = [(6, 7), (7, 6), (8, 7), (7, 8)]


def lbg():
    def at(v):  # y grows downward on screen: flip so brighter blocks sit at the top right
        return {"x": v[0], "y": 9 - v[1]}

    points = DARK + BRIGHT
    first = {(1, 2): 1, (2, 1): 1}  # cell of c1 after the first assignment; everything else goes to c2
    nodes = []
    for i, v in enumerate(points):
        style1 = "accent" if v in first else "warn"
        marks = [{"step": 2, "style": style1}]
        if v in [(2, 3), (3, 2)]:
            marks.append({"step": 4, "style": "accent"})
        nodes.append({"id": f"p{i}", "shape": "dot", **at(v), "marks": marks})
    codewords = [("c1a", "c1", (2, 1), 1, 3), ("c2a", "c2", (3, 2), 1, 3), ("c1b", "c1", (1.5, 1.5), 3, 5),
                 ("c2b", "c2", (5.5, 5.5), 3, 5), ("c1c", "c1", (2, 2), 5, None), ("c2c", "c2", (7, 7), 5, None)]
    for cid, label, v, step, dim in codewords:
        node = {"id": cid, "label": label, **at(v), "step": step, "marks": [{"step": step, "style": "accent" if label == "c1" else "warn"}]}
        if dim:
            node["marks"].append({"step": dim, "style": "dim"})
        nodes.append(node)
    edges = []
    for i, v in enumerate(points):  # first assignment, to the initial codewords
        edges.append({"a": f"p{i}", "b": "c1a" if v in first else "c2a", "step": 2, "marks": [{"step": 3, "style": "dim"}]})
    for i, v in enumerate(points):  # second assignment, to the first centroids
        edges.append({"a": f"p{i}", "b": "c1b" if v in DARK else "c2b", "step": 4, "marks": [{"step": 5, "style": "dim"}]})
    return {"nodes": nodes, "edges": edges, "caption": "Trục: giá trị pixel 1 và pixel 2 của mỗi khối"}


BLOCK = [[121, 114, 56, 47], [37, 200, 247, 255], [16, 0, 12, 169], [43, 5, 7, 251]]
BITMAP = [[1 if v >= 98.75 else 0 for v in row] for row in BLOCK]
ONES = [[r, c] for r, row in enumerate(BITMAP) for c, v in enumerate(row) if v]
DECODED = [[204 if v else 17 for v in row] for row in BITMAP]

stories = []

# ---------------- 00 intro ----------------
stories.append({"id": "mo-dau", "title": "Mở đầu: gửi một tấm ảnh qua mạng chậm", "kind": "intro", "scenes": [
    S("Mở đầu", "Một tấm ảnh 256 KB và một đường mạng chậm", [
        P("Chào các bạn. Chương năm xoay quanh một câu hỏi duy nhất, và cả chương sẽ trả lời nó từng bước. "
          "Hãy tưởng tượng các bạn cần gửi một tấm ảnh bầu trời, ảnh xám năm trăm mười hai nhân năm trăm mười hai pixel, mỗi pixel tám bit.",
          "Ảnh bầu trời 512×512, 8 bit/pixel"),
        P("Tính nhanh: khoảng hai trăm sáu mươi hai nghìn pixel, mỗi pixel một byte, tức là khoảng hai trăm năm mươi sáu kilobyte. "
          "Qua một đường mạng chậm, người nhận phải chờ khá lâu.", "≈ 262 144 byte = 256 KB"),
        P("Câu hỏi của cả chương: làm sao gửi ít bit hơn, mà người nhận vẫn thấy đúng tấm ảnh đó? Các bạn thử nghĩ trước một giây.",
          "Gửi ít bit hơn mà vẫn thấy đúng ảnh?", ask=True),
    ]),
    S("Mở đầu", "Hai con đường, chín phương pháp", [
        P("Có hai con đường. Con đường thứ nhất giữ nguyên từng bit, gọi là nén không mất dữ liệu. "
          "Ta sẽ đi qua entropy, mã Huffman và mã số học.", "Lossless: giữ nguyên từng bit"),
        P("Nhưng con đường này chạm trần ở khoảng hai đến ba lần. Muốn nén mạnh hơn, ta phải chấp nhận bỏ đi những thứ mắt không thấy. "
          "Đó là con đường thứ hai, nén có mất dữ liệu: BTC, lượng tử hóa vector, JPEG và wavelet.", "Lossy: bỏ thứ mắt không thấy"),
        P("Mỗi video tiếp theo là một phương pháp, và mỗi phương pháp ra đời để vá chỗ hụt của phương pháp trước. "
          "Vì vậy các bạn hãy xem theo đúng thứ tự.", "Mỗi phương pháp vá chỗ hụt của cái trước"),
    ], chain={"items": CHAIN, "current": 0}),
]})

# ---------------- 01 entropy ----------------
stories.append({"id": "entropy", "title": "Vì sao ảnh nén được: dư thừa và entropy", "kind": "method", "scenes": [
    S("Vấn đề", "Mỗi pixel tám bit: có phí không?", [
        P("Quay lại tấm ảnh bầu trời. Hiện giờ pixel nào cũng tốn đúng tám bit, dù đó là pixel trời xanh xuất hiện khắp nơi, "
          "hay một pixel cánh chim hiếm hoi.", "Pixel nào cũng 8 bit, hay gặp hay hiếm như nhau"),
        P("Thêm nữa, một pixel trời gần như giống hệt pixel bên cạnh nó. Ta đang gửi đi gửi lại gần cùng một thông tin.",
          "Pixel cạnh nhau gần giống nhau"),
        P("Vậy trong tám bit đó, bao nhiêu bit là thông tin thật, và bao nhiêu bit là thừa?", "Bao nhiêu bit là thông tin thật?",
          ask=True),
    ]),
    S("Cách cũ", "Mã độ dài cố định", [
        P("Để dễ tính, giả sử ảnh trời chỉ còn bốn mức xám, gọi là A, B, C và D. Histogram cho thấy A chiếm bốn mươi phần trăm số pixel, "
          "B ba mươi, C hai mươi, còn D chỉ mười phần trăm.", "4 mức: A 40%, B 30%, C 20%, D 10%"),
        P("Cách cũ là mã độ dài cố định. Bốn ký hiệu thì mỗi ký hiệu hai bit: A là không không, B là không một, và cứ thế.",
          "Mã cố định: mỗi ký hiệu 2 bit"),
        P("Chỗ hụt nằm ở đây: A xuất hiện gần một nửa thời gian mà vẫn tốn hai bit, ngang với D hiếm nhất. "
          "Ta đối xử mọi ký hiệu như nhau, trong khi chúng không hề như nhau.", "A hay gặp vẫn tốn bằng D hiếm"),
    ], histogram={"bars": [{"label": "A", "value": 40}, {"label": "B", "value": 30}, {"label": "C", "value": 20},
                           {"label": "D", "value": 10}], "caption": "Ảnh trời rút gọn còn 4 mức xám (% số pixel)"}),
    S("Ý tưởng", "Viết tắt thứ hay dùng, đừng gửi thứ đoán được", [
        P("Ý tưởng rất đời thường. Khi nhắn tin, từ nào dùng nhiều các bạn viết tắt, từ hiếm thì viết đủ. "
          "Tin nhắn ngắn đi mà người đọc vẫn hiểu đúng hoàn toàn.", "Như nhắn tin: từ hay dùng thì viết tắt"),
        P("Áp vào ảnh: ký hiệu hay gặp nhận mã ngắn, ký hiệu hiếm nhận mã dài.", "Ký hiệu hay gặp → mã ngắn"),
        P("Ý thứ hai: thứ gì đoán được thì không cần gửi. Pixel trời đoán được từ pixel bên cạnh, đó là tương quan không gian. "
          "Với video còn có tương quan thời gian giữa các khung hình liên tiếp. Slide gọi chung là sự dư thừa trong tín hiệu ảnh.",
          "Dư thừa: tương quan không gian (ảnh), thêm thời gian (video)"),
    ]),
    S("Cách làm", "Ba khối của một bộ mã không mất dữ liệu", [
        P("Một bộ mã không mất dữ liệu gồm ba khối nối tiếp. Khối một là biến đổi, ví dụ lấy hiệu giữa pixel và giá trị dự đoán từ hàng xóm, "
          "hoặc DCT. Ảnh trời sau bước này toàn những số gần không, rất dễ nén.", "1. Biến đổi: dự đoán, DCT, băng con", reveal=1),
        P("Khối hai ánh xạ dữ liệu thành các ký hiệu, ví dụ từng giá trị, hoặc cặp số lần lặp và giá trị.",
          "2. Ánh xạ dữ liệu → ký hiệu", reveal=2),
        P("Khối ba gán từ mã nhị phân cho từng ký hiệu. Huffman và mã số học trong hai video sau nằm ở khối này.",
          "3. Mã hóa ký hiệu: Huffman, mã số học", reveal=3),
        P("Khi chọn bộ mã, đừng chỉ nhìn tỉ lệ nén. Slide liệt kê năm tiêu chí: hiệu suất nén, độ trễ mã hóa, độ phức tạp triển khai, "
          "độ bền với lỗi, và khả năng mở rộng theo lớp.", "Chọn bộ mã: tỉ lệ nén, độ trễ, độ phức tạp, chịu lỗi, mở rộng", reveal=3),
    ], graph=pipeline(["Ảnh", "Biến đổi", "Ánh xạ ký hiệu", "Mã hóa ký hiệu", "Chuỗi bit"], [0, 1, 2, 3, 3])),
    S("Công thức", "Entropy: đếm số bit thông tin thật", [
        P("Giờ ta đo xem có bao nhiêu bit là thông tin thật. Phần bên phải công thức là lượng thông tin của một ký hiệu: "
          "càng hiếm, càng bất ngờ, thì càng nhiều thông tin. Phần bên trái lấy trung bình theo xác suất.",
          "Ký hiệu càng hiếm càng nhiều thông tin"),
        P("Thử đoán trước: với bốn mức A, B, C, D ở trên, entropy lớn hơn hay nhỏ hơn hai bit?", "Thử đoán: lớn hơn hay nhỏ hơn 2 bit?",
          ask=True),
        P("Tính ra, A đáng khoảng một phẩy ba hai bit, D đáng khoảng ba phẩy ba hai bit. Lấy trung bình theo xác suất, "
          "entropy chỉ khoảng một phẩy tám lăm bit, nhỏ hơn hai bit của mã cố định.",
          "H ≈ 0,4·1,32 + 0,3·1,74 + 0,2·2,32 + 0,1·3,32 ≈ 1,85 bit"),
        P("Và đây là điều quan trọng nhất của video: entropy là cận dưới. Không có bộ mã không mất dữ liệu nào, giải mã được duy nhất, "
          "mà có số bit trung bình nhỏ hơn entropy.", "Entropy = cận DƯỚI của mọi mã lossless"),
    ], formula=r"H = \underbrace{\sum_{i} p_i}_{\text{trung bình theo xác suất}} \; \underbrace{\log_2 \frac{1}{p_i}}_{\text{thông tin của ký hiệu } i} \quad \text{(bit / ký hiệu)}"),
    S("So sánh", "Lossless, perceptually lossless và lossy", [
        P("Nén không mất dữ liệu buộc ảnh giải mã giống hệt ảnh gốc đến từng con số, nên tỉ lệ nén chỉ khoảng hai đến ba lần."),
        P("Muốn hơn thế, slide nói đến không mất dữ liệu theo cảm nhận, perceptually lossless: bỏ thêm thông tin mắt không nhận ra. "
          "Ảnh nhìn vẫn y hệt, dù số liệu đã khác."),
        P("Còn nén có mất dữ liệu chấp nhận sai khác nhỏ để đổi lấy tỉ lệ nén cao nhất. Ta sẽ đi con đường này từ video BTC."),
    ], table={"headers": ["Kiểu nén", "Ảnh giải mã", "Tỉ lệ nén"],
              "rows": [["Lossless", "Giống hệt từng con số", "≈ 2–3 lần"],
                       ["Perceptually lossless", "Nhìn giống hệt, số liệu khác", "Cao hơn"],
                       ["Lossy", "Có sai khác, chấp nhận được", "Cao nhất"]]}),
    S("Ứng dụng", "Khi nào bắt buộc phải lossless", [
        P("Ảnh y tế, ảnh tài liệu, ảnh khoa học: một pixel sai có thể đổi cả kết luận, nên phải giữ nguyên từng bit.",
          "Ảnh y tế, tài liệu, khoa học: không được sai một bit"),
        P("Ngay trong đời thường, file ZIP và ảnh PNG đều nén không mất dữ liệu.", "ZIP, PNG: nén không mất dữ liệu"),
        P("Và ngay cả JPEG, một chuẩn có mất dữ liệu, cũng kết thúc bằng một bước mã hóa không mất dữ liệu.",
          "Bước cuối của JPEG cũng là lossless"),
    ]),
    limit("Biết giới hạn, nhưng chưa có bộ mã", [
        P("Entropy cho ta biết đích đến: khoảng một phẩy tám lăm bit mỗi ký hiệu. Nhưng nó không nói phải gán bit cho từng ký hiệu thế nào.",
          "Entropy chỉ là giới hạn, chưa phải bộ mã"),
        P("Có cách nào tự động tạo ra một bộ mã tiến sát entropy không? Câu trả lời là mã Huffman, ở video tiếp theo.",
          "→ Huffman: tự động dựng bộ mã sát entropy"),
    ], 2),
    traps([["Entropy là cận trên hay cận dưới?", "Cận DƯỚI của số bit trung bình"],
           ["Vì sao ảnh nén được?", "Dư thừa: tương quan không gian, thêm thời gian ở video"],
           ["Lossless nén được khoảng bao nhiêu?", "Khoảng 2–3 lần"]],
          ["Bẫy một: entropy là cận dưới, không phải cận trên. Mọi mã lossless giải mã duy nhất đều tốn ít nhất bằng entropy.",
           "Bẫy hai: ảnh nén được nhờ dư thừa, tức tương quan giữa các mẫu. Ảnh tĩnh có tương quan không gian, video có thêm tương quan thời gian.",
           "Bẫy ba: nén không mất dữ liệu chỉ đạt khoảng hai đến ba lần. Con số này hay xuất hiện trong đề."]),
]})

# ---------------- 02 Huffman ----------------
stories.append({"id": "huffman", "title": "Mã Huffman", "kind": "method", "scenes": [
    S("Vấn đề", "Cần một bộ mã cụ thể, sát entropy", [
        P("Video trước để lại một câu hỏi: entropy nói rằng chỉ cần ít bit hơn, nhưng làm sao tạo ra một bộ mã cụ thể đạt gần con số đó?",
          "Cần bộ mã cụ thể, sát entropy"),
        P("Bộ mã đó còn phải giải mã được duy nhất: đọc một chuỗi bit liền nhau, không có dấu cách, mà vẫn tách đúng từng ký hiệu.",
          "Giải mã duy nhất, không cần dấu phân cách"),
    ]),
    S("Cách cũ", "Mã cố định cho sáu ký hiệu", [
        P("Ta dùng đúng ví dụ trong slide: sáu ký hiệu. a hai chiếm bốn mươi phần trăm, a sáu ba mươi, a một và a bốn mỗi ký hiệu mười, "
          "a ba sáu phần trăm, và a năm bốn phần trăm."),
        P("Mã cố định cần ba bit cho mỗi ký hiệu, vì hai bit chỉ đủ cho bốn ký hiệu. Nghĩa là a hai, chiếm gần một nửa, vẫn tốn ba bit."),
    ], histogram={"bars": [{"label": "a2", "value": 40}, {"label": "a6", "value": 30}, {"label": "a1", "value": 10},
                           {"label": "a4", "value": 10}, {"label": "a3", "value": 6}, {"label": "a5", "value": 4}],
                  "caption": "Xác suất 6 ký hiệu (%), ví dụ trong slide"}),
    S("Ý tưởng", "Ghép hai thứ hiếm nhất", [
        P("Ý tưởng của Huffman: hai ký hiệu hiếm nhất nên nhận mã dài nhất. Vậy ta ghép chúng thành một ký hiệu mới, cộng xác suất lại, "
          "rồi lặp lại với nguồn nhỏ hơn. Slide gọi đây là rút gọn nguồn.", "Ghép 2 ký hiệu xác suất NHỎ nhất, lặp lại"),
        P("Mỗi lần ghép là thêm một tầng cho cây. Ký hiệu bị ghép sớm nằm sâu dưới đáy cây nên có mã dài. "
          "Ký hiệu hay gặp được ghép muộn, nằm gần gốc, mã ngắn.", "Ghép sớm → nằm sâu → mã dài"),
        P("Thử đoán: trong sáu ký hiệu, cặp nào sẽ được ghép đầu tiên?", "Thử đoán: cặp nào ghép trước?", ask=True),
    ]),
    S("Cách làm", "Bước 1: rút gọn nguồn, dựng cây", [
        P("Hai ký hiệu nhỏ nhất là a ba và a năm, sáu và bốn phần trăm. Ghép lại được một nút mười phần trăm.", "a3 + a5 = 0,1", reveal=1),
        P("Giờ có ba thứ cùng mười phần trăm: a một, a bốn, và nút vừa ghép. Slide chọn a bốn với nút mới, được hai mươi phần trăm. "
          "Chọn cặp khác cũng hợp lệ, và độ dài trung bình không đổi.", "a4 + (0,1) = 0,2", reveal=2),
        P("Tiếp theo, hai thứ nhỏ nhất là nút hai mươi phần trăm và a một, ghép được ba mươi phần trăm.", "(0,2) + a1 = 0,3", reveal=3),
        P("Còn lại a sáu ba mươi và nút ba mươi. Ghép lại được sáu mươi phần trăm.", "a6 + (0,3) = 0,6", reveal=4),
        P("Cuối cùng, ghép nút sáu mươi với a hai bốn mươi, được gốc một trăm phần trăm. Cây đã xong.", "(0,6) + a2 = 1", reveal=5),
    ], graph=huffman_build()),
    S("Cách làm", "Bước 2: đi từ gốc xuống để gán mã", [
        P("Bước hai đi theo chiều ngược lại, từ gốc xuống lá. Quy ước: nhánh trái là bit không, nhánh phải là bit một. "
          "Mã của một ký hiệu là dãy bit trên đường đi từ gốc đến nó.", "Trái = 0, phải = 1; mã = đường đi từ gốc", reveal=0),
        P("Thử đoán: a hai, ký hiệu hay gặp nhất, có mã dài mấy bit?", "Thử đoán: mã a2 dài mấy bit?", reveal=0, ask=True),
        P("Chỉ một bit. Từ gốc rẽ phải là tới a hai ngay, nên mã của a hai là một.", "a2 = 1", reveal=1),
        P("a sáu: rẽ trái rồi rẽ trái, mã là không không.", "a6 = 00", reveal=2),
        P("a một: trái, phải, phải, được không một một.", "a1 = 011", reveal=3),
        P("a bốn: trái, phải, trái, trái, được không một không không.", "a4 = 0100", reveal=4),
        P("Hai ký hiệu hiếm nhất nằm sâu nhất: a ba là không một không một không, a năm là không một không một một. "
          "Năm bit, đúng như ta đoán: ghép sớm thì mã dài.", "a3 = 01010 · a5 = 01011", reveal=5),
    ], graph=huffman_codes()),
    S("Công thức", "Độ dài trung bình: 2,2 bit", [
        P("Để biết bộ mã tốt cỡ nào, ta tính độ dài trung bình: mỗi ký hiệu lấy xác suất nhân số bit, rồi cộng lại.",
          "Xác suất × số bit, rồi cộng"),
        P("Thử đoán: kết quả sẽ gần ba bit của mã cố định, hay gần entropy?", "Thử đoán: gần 3 bit hay gần entropy?", ask=True),
        P("Không phẩy bốn nhân một, cộng không phẩy ba nhân hai, cộng không phẩy một nhân ba, cộng không phẩy một nhân bốn, "
          "cộng hai ký hiệu cuối mỗi ký hiệu năm bit. Tổng là hai phẩy hai bit mỗi ký hiệu.",
          "0,4·1 + 0,3·2 + 0,1·3 + 0,1·4 + 0,06·5 + 0,04·5 = 2,2"),
        P("Entropy của nguồn này khoảng hai phẩy một bốn bit. Huffman chỉ cao hơn giới hạn lý thuyết chưa tới một phần mười bit, "
          "trong khi mã cố định tốn ba bit.", "Entropy ≈ 2,14 · Huffman 2,2 · cố định 3"),
    ], formula=r"L_{avg} = \sum_i \underbrace{p_i}_{\text{xác suất}} \; \underbrace{l_i}_{\text{số bit của mã}}"),
    S("So sánh", "Huffman so với mã cố định", [
        P("Về số bit, Huffman thắng rõ: hai phẩy hai so với ba."),
        P("Đổi lại, từ mã dài ngắn khác nhau, nên bộ giải mã phải đọc từng bit để biết một từ mã kết thúc ở đâu. "
          "Huffman làm được vì không từ mã nào là phần đầu của từ mã khác. Người ta gọi đó là mã tiền tố."),
        P("Huffman phải biết trước xác suất, và bên nhận phải có cùng bảng mã. Slide nêu câu hỏi thảo luận: Huffman thích nghi, "
          "tức là cập nhật bảng mã khi xác suất thay đổi."),
        P("Và vì độ dài thay đổi, một bit lỗi có thể làm lệch ranh giới, kéo theo sai các ký hiệu phía sau. "
          "Với mã cố định, lỗi chỉ hỏng đúng một ký hiệu."),
    ], table={"headers": ["", "Mã cố định", "Huffman"],
              "rows": [["Bit trung bình", "3", "2,2"], ["Độ dài từ mã", "Bằng nhau", "Theo xác suất; mã tiền tố"],
                       ["Cần biết trước", "Không", "Xác suất; gửi kèm bảng mã"],
                       ["Lỗi 1 bit", "Hỏng 1 ký hiệu", "Có thể lệch các ký hiệu sau"]]}),
    S("Ứng dụng", "Huffman ở quanh ta", [
        P("Bước cuối của JPEG mã hóa các hệ số đã lượng tử bằng Huffman.", "Bước cuối của JPEG"),
        P("File ZIP và ảnh PNG dùng thuật toán DEFLATE, trong đó có mã Huffman.", "ZIP, PNG (DEFLATE)"),
        P("Nhạc MP3 cũng dùng mã Huffman ở bước cuối.", "MP3"),
    ]),
    limit("Mỗi ký hiệu ít nhất một bit", [
        P("Nhưng Huffman có một giới hạn cứng: mỗi ký hiệu nhận một từ mã riêng, nên tốn ít nhất một bit nguyên.", "Mỗi ký hiệu ≥ 1 bit"),
        P("Thử nghĩ một ảnh trời gần như một màu, ký hiệu chính chiếm chín mươi phần trăm. Entropy chỉ khoảng không phẩy bốn bảy bit, "
          "nhưng Huffman vẫn phải trả một bit cho mỗi ký hiệu, gấp đôi.", "p = 0,9: entropy ≈ 0,47 bit, Huffman = 1 bit"),
        P("Muốn trả ít hơn một bit cho mỗi ký hiệu, ta phải mã cả thông điệp cùng lúc. Đó là mã số học.", "→ Mã số học"),
    ], 3),
    traps([["Huffman ghép hai ký hiệu nào?", "Hai ký hiệu xác suất NHỎ nhất"],
           ["Huffman tối ưu khi nào?", "Khi mỗi ký hiệu được mã riêng"],
           ["Có nhiều cây Huffman hợp lệ?", "Có, khi trùng xác suất; cùng độ dài trung bình"],
           ["Vì sao giải mã không cần dấu cách?", "Không mã nào là tiền tố của mã khác"]],
          ["Bẫy một: Huffman ghép hai ký hiệu có xác suất nhỏ nhất, không phải lớn nhất.",
           "Bẫy hai: Huffman tối ưu với ràng buộc mỗi ký hiệu nguồn được mã riêng. Bỏ ràng buộc đó thì mã số học có thể tốt hơn.",
           "Bẫy ba: khi trùng xác suất có nhiều cây hợp lệ, mã từng ký hiệu khác nhau nhưng độ dài trung bình như nhau.",
           "Bẫy bốn: giải mã không cần dấu phân cách vì không từ mã nào là tiền tố của từ mã khác."]),
]})

# ---------------- 03 arithmetic ----------------
stories.append({"id": "ma-so-hoc", "title": "Mã số học", "kind": "method", "scenes": [
    S("Vấn đề", "Ký hiệu rất hay gặp vẫn tốn trọn một bit", [
        P("Video trước dừng ở một chỗ khó chịu: ký hiệu chiếm chín mươi phần trăm chỉ mang khoảng không phẩy một lăm bit thông tin, "
          "mà Huffman vẫn bắt trả trọn một bit.", "Ký hiệu p = 0,9 chỉ mang ≈ 0,15 bit"),
        P("Ảnh trời gần một màu có hàng nghìn ký hiệu như vậy liên tiếp. Mỗi ký hiệu phí gần một bit, cộng lại rất lớn.",
          "Hàng nghìn ký hiệu → phí rất lớn"),
    ]),
    S("Cách cũ", "Huffman: một ký hiệu, một từ mã", [
        P("Gốc của vấn đề: Huffman là mã khối. Mỗi ký hiệu nguồn ánh xạ sang một từ mã cố định, nên độ dài luôn là số nguyên bit.",
          "Mã khối: số bit nguyên cho mỗi ký hiệu"),
        P("Muốn trả phân số bit, ta phải thôi mã từng ký hiệu riêng lẻ.", "Muốn phân số bit → thôi mã từng ký hiệu"),
    ]),
    S("Ý tưởng", "Cả thông điệp là một khoảng số", [
        P("Ý tưởng của mã số học: cả thông điệp được gán một từ mã duy nhất, là một khoảng số nằm giữa không và một.",
          "Cả thông điệp → một khoảng trong [0; 1)"),
        P("Hãy nghĩ đến một địa chỉ: tỉnh, rồi quận, rồi đường, rồi số nhà. Mỗi cấp thu hẹp vùng tìm kiếm. "
          "Ở đây mỗi ký hiệu thu hẹp khoảng hiện tại theo đúng xác suất của nó.", "Như địa chỉ: mỗi ký hiệu thu hẹp khoảng"),
        P("Ký hiệu hay gặp chiếm phần lớn, nên khoảng co ít, tốn ít bit. Ký hiệu hiếm chiếm phần nhỏ, khoảng co mạnh, tốn nhiều bit.",
          "Hay gặp → co ít → ít bit"),
    ]),
    S("Cách làm", "Mã chuỗi a1 a2 a3 a3 a4 (ví dụ trong slide)", [
        P("Ví dụ trong slide có bốn ký hiệu: a một và a hai mỗi ký hiệu hai mươi phần trăm, a ba bốn mươi, a bốn hai mươi. "
          "Ban đầu khoảng là từ không đến một, chia theo đúng các tỉ lệ đó. Ký hiệu đầu là a một, ta giữ phần của a một.",
          "a1 → [0; 0,2)", reveal=1),
        P("Phóng to phần đó lên và chia lại theo cùng tỉ lệ. Ký hiệu thứ hai là a hai, lấy đoạn từ hai mươi đến bốn mươi phần trăm, "
          "được từ không phẩy không bốn đến không phẩy không tám.", "a2 → [0,04; 0,08)", reveal=2),
        P("Ký hiệu tiếp theo là a ba, chiếm bốn mươi phần trăm. Thử đoán: khoảng mới dài bao nhiêu?", "Thử đoán: khoảng mới dài bao nhiêu?",
          reveal=2, ask=True),
        P("Khoảng hiện tại dài không phẩy không bốn, a ba giữ bốn mươi phần trăm, nên khoảng mới dài không phẩy không một sáu, "
          "từ không phẩy không năm sáu đến không phẩy không bảy hai.", "a3 → [0,056; 0,072)", reveal=3),
        P("Lại là a ba. Làm y hệt, được từ không phẩy không sáu hai bốn đến không phẩy không sáu tám tám.", "a3 → [0,0624; 0,0688)",
          reveal=4),
        P("Cuối cùng là a bốn, hai mươi phần trăm cuối. Khoảng kết quả là từ không phẩy không sáu bảy năm hai đến không phẩy không sáu tám tám.",
          "a4 → [0,06752; 0,0688)", reveal=5),
        P("Bất kỳ số nào trong khoảng này, ví dụ không phẩy không sáu tám, đều đại diện cho cả năm ký hiệu. "
          "Bên giải mã chỉ việc xem số đó rơi vào phần nào, lần lượt từng tầng.", "Gửi một số trong khoảng, ví dụ 0,068", reveal=6),
    ], intervals=intervals()),
    S("Công thức", "Khoảng càng hẹp, càng cần nhiều bit", [
        P("Độ rộng khoảng cuối bằng tích xác suất các ký hiệu đã gặp: không phẩy không không một hai tám.", "Độ rộng = tích các xác suất"),
        P("Để chỉ ra một số nằm trong khoảng rộng như vậy, cần khoảng log cơ số hai của một chia độ rộng, tức gần mười bit cho năm ký hiệu.",
          "≈ log₂(1/độ rộng) ≈ 9,6 → cỡ 10 bit"),
        P("Đó chính là lượng thông tin của cả thông điệp. Mã số học trả đúng phần đó cho cả chuỗi, không làm tròn lên từng ký hiệu một.",
          "Không làm tròn bit theo từng ký hiệu"),
        P("Thông điệp càng dài thì khoảng càng hẹp và số bit càng tăng, nhưng tăng đúng theo thông tin thật.",
          "Thông điệp dài → khoảng hẹp → nhiều bit"),
    ], formula=r"\underbrace{0{,}2 \cdot 0{,}2 \cdot 0{,}4 \cdot 0{,}4 \cdot 0{,}2}_{\text{độ rộng khoảng}} = 0{,}00128 \;\Rightarrow\; \log_2 \tfrac{1}{0{,}00128} \approx 9{,}6 \text{ bit}"),
    S("So sánh", "Huffman hay mã số học?", [
        P("Huffman là mã khối, mỗi ký hiệu một từ mã. Mã số học là mã không khối, cả thông điệp một từ mã."),
        P("Câu hỏi thảo luận trong slide: theo lý thuyết thông tin, cái nào ít bit hơn? Mã số học, vì nó không phải làm tròn lên một bit nguyên "
          "cho từng ký hiệu, nên tiến sát entropy hơn."),
        P("Đổi lại, nó tính toán nặng hơn, phải liên tục chia khoảng và giữ độ chính xác số học."),
        P("Nhưng nó dễ thích nghi: slide nói đến ước lượng xác suất thích nghi theo ngữ cảnh, chỉ cần cập nhật bảng xác suất sau mỗi ký hiệu."),
    ], table={"headers": ["", "Huffman", "Mã số học"],
              "rows": [["Loại mã", "Mã khối", "Không khối: cả thông điệp một từ mã"],
                       ["Bit / ký hiệu", "Số nguyên, ≥ 1", "Có thể là phân số, sát entropy hơn"],
                       ["Tính toán", "Đơn giản, tra bảng", "Nặng hơn: chia khoảng liên tục"],
                       ["Thích nghi", "Phải dựng lại cây", "Dễ: cập nhật xác suất theo ngữ cảnh"]]}),
    S("Ứng dụng", "Mã số học ở đâu?", [
        P("JPEG2000 dùng một bộ mã số học thích nghi ở bước cuối.", "JPEG2000"),
        P("Chuẩn nén video H.264 có chế độ CABAC, cũng là mã số học thích nghi theo ngữ cảnh. "
          "Chuẩn JPEG gốc cũng có tùy chọn mã số học bên cạnh Huffman.", "H.264 (CABAC), tùy chọn của JPEG"),
    ]),
    limit("Vẫn chỉ là nén không mất dữ liệu", [
        P("Dù là Huffman hay mã số học, ta vẫn đang ở con đường không mất dữ liệu. Ảnh giải mã giống hệt từng bit, "
          "nên trần nén vẫn chỉ khoảng hai đến ba lần.", "Vẫn lossless: trần ≈ 2–3 lần"),
        P("Hai trăm năm mươi sáu kilobyte chia ba vẫn còn hơn tám mươi kilobyte. Muốn nhỏ hơn nữa, ta phải chấp nhận bỏ đi một phần thông tin. "
          "Video tiếp theo là BTC, phương pháp có mất dữ liệu đầu tiên.", "→ BTC: chấp nhận mất dữ liệu"),
    ], 4),
    traps([["Mã số học là mã khối?", "Sai: không khối, cả thông điệp một từ mã"],
           ["Thông điệp dài thì khoảng thế nào?", "Hẹp lại, cần nhiều bit hơn"],
           ["Theo lý thuyết, cái nào ít bit hơn?", "Mã số học: không làm tròn bit từng ký hiệu"]],
          ["Bẫy một: mã số học là mã không khối. Huffman mới là mã khối.",
           "Bẫy hai: thông điệp càng dài, khoảng càng hẹp, số bit cần để biểu diễn khoảng càng tăng.",
           "Bẫy ba: về lý thuyết thông tin, mã số học tiến sát entropy hơn Huffman."]),
]})

# ---------------- 04 BTC ----------------
stories.append({"id": "btc", "title": "BTC: mã hóa cắt khối", "kind": "method", "scenes": [
    S("Vấn đề", "Cần nén mạnh hơn hai đến ba lần", [
        P("Ta đã chạm trần của nén không mất dữ liệu: tấm ảnh trời vẫn còn gần trăm kilobyte.", "Lossless: vẫn gần 100 KB"),
        P("Nhưng mắt người không cần từng con số chính xác. Một pixel tám mươi hay tám mươi hai, nhìn như nhau. "
          "Nếu chấp nhận ảnh giải mã khác đi một chút, ta có thể nén mạnh hơn nhiều.", "Mắt không phân biệt 80 với 82"),
        P("Câu hỏi: nếu được phép bỏ bớt, ta nên giữ lại những gì của một khối ảnh?", "Giữ lại gì của một khối?", ask=True),
    ]),
    S("Cách cũ", "Lossless phải giữ mọi thứ", [
        P("Huffman và mã số học không được phép bỏ gì, nên bị chặn bởi entropy.", "Bị chặn bởi entropy"),
        P("Muốn vượt qua, ta phải đổi luật chơi: không giữ nguyên ảnh nữa, mà giữ những đặc trưng quan trọng của ảnh.",
          "Đổi luật: giữ đặc trưng quan trọng"),
    ]),
    S("Ý tưởng", "Tóm tắt mỗi khối bằng trung bình và độ lệch", [
        P("Hình dung các bạn mô tả chiều cao một lớp học mà không đọc từng người. Các bạn nói: trung bình bao nhiêu, chênh lệch nhiều hay ít, "
          "và ai cao hơn trung bình.", "Như mô tả chiều cao cả lớp"),
        P("BTC làm đúng như vậy với từng khối n nhân n: giữ trung bình, giữ độ lệch chuẩn, và một bản đồ một bit cho biết pixel nào sáng hơn trung bình.",
          "Giữ: trung bình, độ lệch chuẩn, bitmap 1 bit"),
        P("Khi giải mã, mỗi pixel chỉ còn một trong hai mức: a cho pixel tối, b cho pixel sáng, chọn sao cho trung bình và độ lệch chuẩn "
          "của khối vẫn được giữ nguyên.", "Giải mã: 2 mức a, b giữ nguyên 2 moment"),
    ]),
    S("Cách làm", "Bước 1: trung bình và bitmap", [
        P("Lấy khối bốn nhân bốn trong slide, mười sáu pixel. Trung bình là chín mươi tám phẩy bảy lăm, "
          "độ lệch chuẩn khoảng chín mươi hai phẩy chín lăm.", reveal=1),
        P("Thử đoán: có bao nhiêu pixel lớn hơn hoặc bằng trung bình?", reveal=1, ask=True),
        P("Đánh dấu một cho pixel lớn hơn hoặc bằng trung bình, không cho phần còn lại. Có bảy pixel sáng, gọi số đó là q, bằng bảy. "
          "Bitmap này tốn đúng mười sáu bit.", reveal=2),
    ], compare={"left": {"label": "Khối gốc · trung bình 98,75", "grid": {"cells": BLOCK}},
                "right": {"label": "Bitmap · q = 7", "grid": {"cells": BITMAP, "accent": ONES}},
                "arrow": "≥ trung bình → 1"}),
    S("Công thức", "Bước 2: chọn hai mức a và b", [
        P("Hai mức giải mã được tính từ trung bình, độ lệch chuẩn, số pixel k và số pixel sáng q, "
          "sao cho khối giải mã giữ nguyên hai moment đó.", "k = 16 pixel, q = 7 pixel sáng"),
        P("Thay số: a khoảng mười sáu phẩy tám, b khoảng hai trăm lẻ bốn phẩy một.", "a ≈ 16,8 · b ≈ 204,1"),
        P("Để ý: chỉ có bảy pixel sáng nên b phải lớn hơn trung bình nhiều, còn chín pixel tối kéo a xuống thấp. "
          "Nhờ vậy trung bình của khối giải mã vẫn đúng.", "Ít pixel sáng → b xa trung bình hơn"),
    ], formula=r"a = m - \sigma\sqrt{\frac{q}{k-q}} \qquad b = m + \sigma\sqrt{\frac{k-q}{q}}"),
    S("Cách làm", "Bước 3: giải mã", [
        P("Bên nhận có bitmap mười sáu bit, cùng trung bình và độ lệch chuẩn, mỗi số tám bit.", reveal=1),
        P("Pixel nào là một nhận b, làm tròn là hai trăm lẻ bốn. Pixel nào là không nhận a, làm tròn là mười bảy. "
          "Khối giải mã thô hơn, nhưng sáng tối đúng chỗ, và trung bình vẫn xấp xỉ chín mươi tám phẩy tám.", reveal=2),
        P("Tổng cộng ba mươi hai bit thay vì một trăm hai mươi tám bit: nén bốn lần, tức hai bit mỗi pixel, và khối nào cũng như nhau.",
          reveal=2),
    ], compare={"left": {"label": "Bitmap", "grid": {"cells": BITMAP, "accent": ONES}},
                "right": {"label": "Khối giải mã · 32 bit thay vì 128", "grid": {"cells": DECODED, "accent": ONES}},
                "arrow": "1 → b, 0 → a"}),
    S("So sánh", "BTC so với nén không mất dữ liệu", [
        P("Nén không mất dữ liệu giữ ảnh giống hệt. BTC chỉ giữ gần đúng, mỗi khối hai mức."),
        P("Đổi lại, BTC nén bốn lần với khối bốn nhân bốn, vượt qua trần hai đến ba lần."),
        P("BTC là nén có mất dữ liệu với độ dài cố định: khối nào cũng ba mươi hai bit, dễ dự trù băng thông."),
        P("Và nó cực kỳ đơn giản: giải mã chỉ là đọc bitmap rồi điền a hoặc b."),
    ], table={"headers": ["", "Lossless (Huffman…)", "BTC"],
              "rows": [["Ảnh giải mã", "Giống hệt", "Gần đúng, 2 mức mỗi khối"],
                       ["Tỉ lệ nén", "≈ 2–3 lần, tùy ảnh", "Cố định: 4 lần (khối 4×4)"],
                       ["Độ dài mã", "Thay đổi", "Cố định: 32 bit / khối"],
                       ["Tính toán", "Cần thống kê xác suất", "Rất đơn giản, giải mã cực nhanh"]]}),
    S("Ứng dụng", "BTC được dùng ở đâu", [
        P("Theo slide, BTC từng được so sánh với DCT và mã lai cho ảnh trinh sát trên không độ phân giải cao. "
          "Ở tốc độ từ một đến ba bit mỗi pixel, BTC cho kết quả rất tốt.", "Ảnh trinh sát trên không: tốt ở 1–3 bit/pixel"),
        P("Slide cũng nêu biến thể dùng moment tuyệt đối thay cho độ lệch chuẩn, cho sai số bình phương trung bình tốt hơn BTC chuẩn.",
          "Biến thể: moment tuyệt đối → sai số tốt hơn"),
    ]),
    limit("Mỗi pixel vẫn được xét riêng", [
        P("Hạn chế của BTC: mỗi pixel chỉ còn một trong hai mức, nên khối nhiều chi tiết bị vẽ thô.", "Mỗi khối chỉ 2 mức"),
        P("Sâu hơn, BTC vẫn lượng tử từng pixel riêng lẻ, chỉ là theo ngưỡng của khối. "
          "Nó không tận dụng việc các khối ảnh thường lặp lại thành những mẫu giống nhau.", "Vẫn lượng tử từng pixel"),
        P("Nếu ta lượng tử cả khối như một đơn vị thì sao? Đó là lượng tử hóa vector.", "→ Lượng tử hóa vector"),
    ], 5),
    traps([["BTC là lossless hay lossy?", "Lossy, độ dài cố định"],
           ["BTC bảo toàn gì?", "Trung bình và độ lệch chuẩn (không phải trung vị)"],
           ["Bitmap tốn bao nhiêu?", "1 bit / pixel với bộ lượng tử 2 mức"]],
          ["Bẫy một: BTC là nén có mất dữ liệu, với độ dài cố định.",
           "Bẫy hai: BTC bảo toàn trung bình và độ lệch chuẩn của khối, không phải trung vị.",
           "Bẫy ba: với bộ lượng tử hai mức, bitmap tốn một bit cho mỗi pixel."]),
]})

# ---------------- 05 VQ ----------------
stories.append({"id": "vq-lbg", "title": "Lượng tử hóa vector và thuật toán LBG", "kind": "method", "scenes": [
    S("Vấn đề", "Ảnh lặp lại những kiểu khối giống nhau", [
        P("Nhìn kỹ tấm ảnh trời: có những khối trời phẳng, khối mây sáng, khối viền mây. Những kiểu khối này lặp đi lặp lại khắp ảnh.",
          "Ảnh có những kiểu khối lặp lại"),
        P("Nếu cả hai bên đều có sẵn một danh sách các kiểu khối mẫu, ta chỉ cần gửi số thứ tự của mẫu gần nhất, thay vì gửi cả khối.",
          "Gửi số thứ tự thay cho cả khối?"),
    ]),
    S("Cách cũ", "Lượng tử vô hướng: xét từng mẫu", [
        P("Lượng tử hóa là ánh xạ một tập giá trị lớn sang một tập nhỏ hơn, ví dụ làm tròn số thực về số nguyên. "
          "Làm khéo thì sai số được giữ ở mức nhỏ.", "Lượng tử: tập lớn → tập nhỏ"),
        P("BTC và cách làm tròn thông thường xét từng pixel một. Mỗi pixel quyết định riêng, không biết hàng xóm của nó thế nào.",
          "Từng pixel quyết định riêng"),
    ]),
    S("Ý tưởng", "Làm tròn cả khối về mẫu gần nhất", [
        P("Lượng tử hóa vector, viết tắt VQ, gom một khối mẫu thành một vector và làm tròn cả vector cùng lúc.", "VQ: lượng tử cả khối"),
        P("Giống như bảng màu sơn: thay vì đọc mã màu chính xác, các bạn chỉ nói số của ô màu gần nhất. Bảng đó gọi là codebook.",
          "Như bảng màu: gửi số của mẫu gần nhất"),
        P("Bên mã hóa tìm code vector gần nhất rồi gửi chỉ số. Bên giải mã có cùng codebook, tra chỉ số là dựng lại được khối.",
          "Mã hóa gửi chỉ số, giải mã tra bảng"),
    ]),
    S("Cách làm", "Thiết kế codebook bằng LBG", [
        P("Ví dụ nhỏ: mỗi khối chỉ có hai pixel, nên mỗi khối là một điểm trên mặt phẳng. "
          "Tập huấn luyện có tám khối: bốn khối tối ở góc dưới, bốn khối sáng ở góc trên.", "8 khối 2 pixel = 8 điểm", reveal=0),
        P("Thuật toán của Linde, Buzo và Gray, gọi tắt là LBG. Bước một: chọn ngẫu nhiên N code vector từ tập huấn luyện. "
          "Ở đây N bằng hai, và không may cả hai đều rơi vào nhóm tối.", "1. Chọn ngẫu nhiên N code vector", reveal=1),
        P("Bước hai: gán mỗi vector huấn luyện cho code vector gần nhất, theo quy tắc lân cận gần nhất. "
          "c hai ở gần nhóm sáng hơn, nên ôm luôn cả bốn khối sáng.", "2. Gán theo lân cận gần nhất", reveal=2),
        P("Thử đoán: khi dời mỗi code vector về tâm nhóm của nó, c hai sẽ đi về đâu?", "Thử đoán: c2 đi về đâu?", reveal=2, ask=True),
        P("Bước ba: tính tâm mỗi nhóm và dùng làm codebook mới. c một về một phẩy năm, một phẩy năm. "
          "c hai bị kéo ra giữa, năm phẩy năm, năm phẩy năm.", "3. Code vector ← tâm nhóm", reveal=3),
        P("Lặp lại phép gán. Giờ hai khối tối đã gần c một hơn, nên mỗi nhóm đúng là một cụm.", "Lặp: gán lại", reveal=4),
        P("Tính tâm lần nữa: c một về hai, hai, còn c hai về bảy, bảy. Gán lại thì không còn gì thay đổi: thuật toán đã hội tụ.",
          "Hội tụ: codebook không đổi", reveal=5),
    ], graph=lbg()),
    S("Cách làm", "Mã giả LBG, mã hóa và giải mã", [
        P("Tóm lại thành mã giả. Khởi tạo codebook ngẫu nhiên từ tập huấn luyện.", reveal=[1]),
        P("Lặp hai việc, gán theo lân cận gần nhất rồi dời về tâm, cho đến khi codebook gần như không đổi.", reveal=[2, 3, 4, 5]),
        P("Khi nén, mỗi khối ảnh được thay bằng chỉ số của code vector gần nhất. Với codebook hai trăm năm mươi sáu mục, "
          "mỗi khối mười sáu pixel chỉ tốn tám bit.", reveal=[6]),
        P("Bên giải mã giữ cùng codebook và chỉ việc tra bảng, rất nhanh. Phần nặng nằm ở bên mã hóa, phải tìm vector gần nhất.",
          reveal=[7]),
    ], code={"lines": ["codebook ← N vector ngẫu nhiên từ tập huấn luyện", "repeat:",
                       "    gán mỗi vector vào code vector gần nhất", "    mỗi code vector ← tâm nhóm của nó",
                       "until codebook gần như không đổi", "mã hóa: mỗi khối → chỉ số code vector gần nhất",
                       "giải mã: chỉ số → tra codebook"]}),
    S("So sánh", "VQ so với BTC", [
        P("BTC lượng tử từng pixel theo ngưỡng của khối. VQ lượng tử cả khối như một vector."),
        P("BTC gửi trung bình, độ lệch và bitmap. VQ chỉ gửi một chỉ số."),
        P("BTC gần như không tốn chi phí chuẩn bị. VQ phải huấn luyện codebook, và mỗi lần mã hóa phải tìm vector gần nhất."),
        P("Cả hai đều giải mã rất nhanh."),
    ], table={"headers": ["", "BTC", "VQ"],
              "rows": [["Đơn vị lượng tử", "Từng pixel (ngưỡng khối)", "Cả khối (vector)"],
                       ["Gửi đi", "Trung bình, độ lệch, bitmap", "Chỉ số trong codebook"],
                       ["Chi phí", "Rất rẻ", "Huấn luyện codebook, tìm kiếm"],
                       ["Giải mã", "Điền a / b", "Tra bảng"]]}),
    S("Ứng dụng", "Codebook ở đâu?", [
        P("Ý tưởng codebook có trong nén giọng nói: các bộ mã thoại kiểu CELP dùng codebook để mã hóa tín hiệu.", "Mã thoại CELP"),
        P("Và các bạn sẽ gặp lại đúng thuật toán này ở chương chín, với tên K-means, để phân đoạn ảnh.", "Chương 9: K-means"),
    ]),
    limit("Codebook tốn kém, vẫn làm trên pixel", [
        P("Codebook phải được huấn luyện, tốn thời gian, và chỉ tốt với loại ảnh giống tập huấn luyện.", "Codebook tốn công huấn luyện"),
        P("Mã hóa phải so khối với mọi code vector, rất nặng khi codebook lớn.", "Tìm kiếm nặng"),
        P("Và cả BTC lẫn VQ đều làm trực tiếp trên pixel. Có cách nào biến đổi ảnh trước, để thông tin dồn vào vài con số, rồi mới bỏ bớt không? "
          "Đó chính là cách JPEG làm.", "→ JPEG: biến đổi rồi mới lượng tử"),
    ], 6),
    traps([["VQ lượng tử cái gì?", "Cả khối mẫu (vector), không phải từng mẫu"],
           ["LBG gồm những bước nào?", "Khởi tạo ngẫu nhiên → gán lân cận gần nhất → tính tâm → lặp"],
           ["Bên mã hóa gửi gì?", "Chỉ số của code vector gần nhất"]],
          ["Bẫy một: VQ lượng tử cả khối mẫu cùng lúc, không phải từng mẫu riêng.",
           "Bẫy hai: thứ tự của LBG là khởi tạo ngẫu nhiên, gán theo lân cận gần nhất, tính tâm, rồi lặp đến khi hội tụ.",
           "Bẫy ba: bên mã hóa chỉ gửi chỉ số, codebook đã có sẵn ở cả hai bên."]),
]})

# ---------------- 06 JPEG ----------------
stories.append({"id": "jpeg", "title": "Chuẩn JPEG", "kind": "method", "scenes": [
    S("Vấn đề", "Cần một chuẩn chung", [
        P("Các phương pháp đến giờ mỗi cái một kiểu. Để gửi ảnh cho bất kỳ ai, máy ảnh, điện thoại và trình duyệt phải cùng hiểu một định dạng.",
          "Mọi thiết bị phải hiểu chung một định dạng"),
        P("Chuẩn đó còn phải nén tốt, chạy nhanh trên cả phần cứng lẫn phần mềm, và cho chọn giữa dung lượng với chất lượng.",
          "Nén tốt, chạy nhanh, chỉnh được chất lượng"),
    ]),
    S("Cách cũ", "BTC và VQ làm trực tiếp trên pixel", [
        P("BTC và VQ làm việc trên giá trị pixel. Trong miền pixel, thông tin trải đều mọi điểm, khó biết bỏ chỗ nào mà mắt không thấy.",
          "Miền pixel: thông tin trải đều"),
        P("Ở chương bốn ta đã có câu trả lời: phép biến đổi DCT dồn phần lớn năng lượng của khối vào vài hệ số tần số thấp.",
          "Chương 4: DCT dồn năng lượng"),
    ]),
    S("Ý tưởng", "Biến đổi, bỏ phần mắt ít nhạy, rồi mã hóa", [
        P("JPEG ghép những gì ta đã học: biến đổi để thông tin dồn lại, lượng tử để bỏ phần mắt ít nhạy, rồi mã không mất dữ liệu phần còn lại.",
          "Biến đổi → lượng tử → mã entropy"),
        P("Mắt người nhạy với mảng sáng tối lớn, kém nhạy với chi tiết rất mịn. Vậy ta lượng tử thô các tần số cao, giữ kỹ tần số thấp.",
          "Tần số cao: lượng tử thô"),
    ]),
    S("Cách làm", "Bốn bước mã hóa JPEG", [
        P("Bước một, chia ảnh thành các khối tám nhân tám pixel liền kề.", "1. Chia khối 8×8", reveal=1),
        P("Bước hai, biến đổi DCT từng khối. Hệ số góc trên bên trái là độ sáng trung bình, càng xa càng là chi tiết tần số cao. "
          "DCT khả nghịch, nên chưa mất gì.", "2. DCT: chưa mất gì", reveal=2),
        P("Bước ba, chia mỗi hệ số cho một số trong bảng lượng tử rồi làm tròn. Đây là bước duy nhất làm mất dữ liệu, "
          "và bảng này dùng chung cho mọi khối.", "3. Lượng tử: bước DUY NHẤT mất dữ liệu", reveal=3),
        P("Bước bốn, mã các hệ số đã lượng tử, phần lớn là số không, bằng Huffman. "
          "Bên giải mã làm ngược lại: giải Huffman, nhân lại với bảng lượng tử, rồi DCT ngược từng khối.",
          "4. Huffman · giải mã: làm ngược lại", reveal=4),
    ], graph=pipeline(["Ảnh", "Chia khối 8×8", "DCT", "Lượng tử Q(u,v)", "Huffman", "Chuỗi bit"], [0, 1, 2, 3, 4, 4])),
    S("Cách làm", "Lượng tử làm mất gì?", [
        P("Thử đoán trước: hệ số nào sẽ mất nhiều nhất, hệ số DC lớn nhất, hay một hệ số tần số cao nhỏ?", reveal=0, ask=True),
        P("Hệ số DC bằng hai trăm ba mươi sáu, bước lượng tử mười sáu. Chia ra rồi làm tròn được mười lăm. "
          "Bộ giải mã nhân lại được hai trăm bốn mươi, sai lệch chỉ bốn.", reveal=1),
        P("Hệ số tần số thấp bằng âm hai mươi ba, bước lượng tử mười một. Làm tròn được âm hai, giải mã ra âm hai mươi hai, sai lệch một.",
          reveal=2),
        P("Hệ số tần số cao bằng mười hai, nhưng bước lượng tử ở đó rất lớn, chín mươi chín. Chia ra chưa tới một nửa nên làm tròn thành không. "
          "Hệ số này biến mất hoàn toàn. Đó là cách JPEG bỏ chi tiết mịn, và cũng là lý do sau lượng tử có rất nhiều số không.", reveal=3),
    ], table={"headers": ["Hệ số", "F", "Q", "round(F/Q)", "Giải mã", "Sai số"],
              "rows": [["DC (0,0)", "236", "16", "15", "240", "4"], ["Tần số thấp (0,1)", "−23", "11", "−2", "−22", "1"],
                       ["Tần số cao (7,7)", "12", "99", "0", "0", "12"]]}),
    S("So sánh", "JPEG so với BTC và VQ", [
        P("BTC và VQ làm trên pixel, JPEG làm trên hệ số DCT."),
        P("Nhờ vậy JPEG bỏ thông tin đúng chỗ mắt ít nhạy, thay vì bỏ đều mọi nơi."),
        P("JPEG là chuẩn chung, độ phức tạp thấp, chạy được trên cả phần cứng lẫn phần mềm, và hỗ trợ mọi loại ảnh."),
        P("JPEG có nhiều chế độ: tuần tự quét một lượt từ trái sang phải, trên xuống dưới; lũy tiến gửi bản thô trước rồi tinh dần; "
          "phân cấp đa độ phân giải. Độ sâu từ tám đến mười hai bit, và JPEG định nghĩa cả thuật toán không mất dữ liệu."),
    ], table={"headers": ["", "BTC / VQ", "JPEG"],
              "rows": [["Miền làm việc", "Pixel", "Hệ số DCT"], ["Bỏ thông tin ở đâu", "Đều mọi pixel", "Chủ yếu tần số cao"],
                       ["Chuẩn hóa", "Không", "Chuẩn quốc tế"],
                       ["Chế độ", "Một kiểu", "Tuần tự, lũy tiến, phân cấp, lossless"]]}),
    S("Ứng dụng", "JPEG ở khắp nơi", [
        P("JPEG là định dạng ảnh phổ biến nhất: ảnh chụp bằng điện thoại, máy ảnh, ảnh trên web.", "Ảnh điện thoại, máy ảnh, web"),
        P("Chế độ lũy tiến là lý do một số ảnh trên web hiện mờ trước rồi nét dần.", "Lũy tiến: ảnh hiện mờ rồi nét dần"),
    ]),
    limit("Nén mạnh thì vỡ ô vuông", [
        P("Vì mỗi khối tám nhân tám được lượng tử độc lập với khối bên cạnh, khi nén mạnh, ranh giới giữa các khối lộ ra thành những ô vuông. "
          "Đó là méo khối, blocking.", "Lượng tử độc lập từng khối → méo khối"),
        P("Ảnh bầu trời là nạn nhân điển hình: vùng trời chuyển màu mượt bị vỡ thành từng bậc ô vuông.", "Trời chuyển màu mượt → vỡ ô"),
        P("Muốn hết ô vuông, phải bỏ cách chia khối. Phép biến đổi wavelet làm trên toàn ảnh, ở video tiếp theo.",
          "→ Wavelet: biến đổi toàn ảnh"),
    ], 7),
    traps([["Bước nào của JPEG làm mất dữ liệu?", "Chỉ lượng tử hóa; DCT, Huffman không mất"],
           ["Vì sao có méo khối?", "Lượng tử độc lập từng khối 8×8"],
           ["JPEG chỉ có chế độ lossy?", "Sai: có cả lossless"],
           ["Bảng lượng tử Q dùng thế nào?", "Giống nhau cho mọi khối"]],
          ["Bẫy một: trong JPEG chỉ lượng tử hóa làm mất dữ liệu. DCT khả nghịch, Huffman không mất gì.",
           "Bẫy hai: méo khối sinh ra vì mỗi khối được lượng tử độc lập.",
           "Bẫy ba: JPEG định nghĩa cả thuật toán có mất lẫn không mất dữ liệu.",
           "Bẫy bốn: bảng lượng tử dùng chung cho mọi khối."]),
]})

# ---------------- 07 wavelet ----------------
DEADZONE = [2, 4, 9, 20, 40, 20, 9, 4, 2]
stories.append({"id": "wavelet", "title": "Nén wavelet và JPEG2000", "kind": "method", "scenes": [
    S("Vấn đề", "Nén mạnh mà không vỡ ô vuông", [
        P("Ta muốn nén ảnh trời mạnh hơn nữa mà không bị những ô vuông của JPEG.", "Nén mạnh nhưng không ô vuông"),
        P("Ô vuông sinh ra từ việc chia ảnh thành khối và xử lý mỗi khối riêng.", "Gốc rễ: chia khối"),
    ]),
    S("Cách cũ", "DCT theo khối 8×8", [
        P("JPEG chỉ nhìn ảnh qua những ô tám nhân tám. Mỗi ô không biết ô bên cạnh, nên không có gì bảo đảm biên giữa hai ô liền mạch.",
          "Mỗi khối không biết khối bên cạnh"),
    ]),
    S("Ý tưởng", "Biến đổi cả ảnh, giữ vài hệ số lớn", [
        P("Nén wavelet dựa trên một ý: các hệ số của một phép biến đổi giải tương quan được mã hóa hiệu quả hơn chính các pixel.",
          "Mã hệ số đã giải tương quan > mã pixel"),
        P("Wavelet biến đổi toàn ảnh theo nhiều mức, tách ra một ảnh thu nhỏ và các ảnh chi tiết. "
          "Thông tin thị giác quan trọng dồn vào số ít hệ số.", "Toàn ảnh, nhiều mức: thông tin dồn vào ít hệ số"),
        P("Các hệ số còn lại rất nhỏ, có thể lượng tử thô hoặc cho bằng không mà ảnh gần như không đổi.",
          "Hệ số nhỏ → lượng tử thô hoặc về 0"),
    ]),
    S("Cách làm", "Bộ mã hóa wavelet", [
        P("Bộ mã hóa gồm ba khối. Khối một là biến đổi wavelet nhiều mức.", "1. Biến đổi wavelet", reveal=1),
        P("Khối hai lượng tử các hệ số. Đây là nơi mất dữ liệu.", "2. Lượng tử: nơi mất dữ liệu", reveal=2),
        P("Khối ba mã hóa ký hiệu không mất dữ liệu. Bộ giải mã làm ngược lại: giải mã ký hiệu, rồi biến đổi wavelet ngược.",
          "3. Mã hóa ký hiệu · giải mã: ngược lại", reveal=3),
    ], graph=pipeline(["Ảnh", "Biến đổi wavelet", "Lượng tử", "Mã hóa ký hiệu", "Chuỗi bit"], [0, 1, 2, 3, 3])),
    S("Cách làm", "Dead zone: ép hệ số nhỏ về 0", [
        P("Hình này là phân bố các hệ số chi tiết sau biến đổi: phần lớn nằm rất gần không.", "Hệ số chi tiết dồn quanh 0", reveal=0),
        P("Bộ lượng tử thường là lượng tử đều: mọi khoảng rộng như nhau. Chỉ những hệ số thật sát không mới bị ép về không.",
          "Lượng tử đều: các khoảng bằng nhau", reveal=1),
        P("Thử đoán: nếu nới rộng riêng khoảng quanh số không thì được gì?", "Thử đoán: nới rộng khoảng quanh 0?", reveal=1, ask=True),
        P("Mẹo của slide: nới rộng khoảng lượng tử quanh không, gọi là dead zone. Nhiều hệ số nhỏ hơn bị ép về không, "
          "mà đó lại là chi tiết mắt ít thấy. Nhiều số không liên tiếp thì mã hóa rất rẻ.",
          "Dead zone: khoảng quanh 0 rộng hơn → nhiều số 0", reveal=2),
        P("Slide còn nêu: có thể đổi kích thước khoảng lượng tử theo từng mức tỉ lệ, và các khoảng đã chọn phải gửi kèm cho bộ giải mã.",
          "Đổi bước theo tỉ lệ; gửi kèm cho bộ giải mã", reveal=2),
    ], histogram={"bars": [{"label": str(v), "value": c, **({"marks": [{"step": 1, "style": "accent"}]} if v == 0 else
                                                            {"marks": [{"step": 2, "style": "accent"}]} if abs(v) == 1 else {})}
                           for v, c in zip(range(-4, 5), DEADZONE)],
                  "bands": [{"start": 4, "end": 5, "label": "khoảng thường", "step": 1},
                            {"start": 3, "end": 6, "label": "dead zone", "step": 2, "marks": [{"step": 2, "style": "warn"}]}],
                  "caption": "Phân bố hệ số chi tiết (minh họa); cột xanh = bị ép về 0"}),
    S("Cách làm", "Ba yếu tố ảnh hưởng tỉ lệ nén", [
        P("Một: loại hàm wavelet. Nó ảnh hưởng độ phức tạp tính toán và khả năng nén mà sai số vẫn chấp nhận được. "
          "Slide có bảng so sánh vài họ wavelet thường dùng.", "1. Loại hàm wavelet"),
        P("Hai: số mức phân rã. Càng nhiều mức thì số phép tính của biến đổi xuôi và ngược càng tăng.", "2. Số mức phân rã"),
        P("Thử đoán: có phải càng nhiều mức phân rã thì càng tốt?", "Thử đoán: càng nhiều mức càng tốt?", ask=True),
        P("Không hẳn. Lượng tử các hệ số ở tỉ lệ ngày càng thấp ảnh hưởng đến vùng ảnh ngày càng rộng, nên sai số tái tạo có thể tăng. "
          "Slide minh họa bằng ví dụ nén một ảnh năm trăm mười hai nhân năm trăm mười hai.", "Mức thấp ảnh hưởng vùng rộng → sai số tăng"),
        P("Ba: thiết kế bộ lượng tử, như dead zone vừa rồi.", "3. Thiết kế bộ lượng tử"),
    ]),
    S("So sánh", "JPEG so với wavelet / JPEG2000", [
        P("JPEG biến đổi theo khối tám nhân tám. Wavelet biến đổi toàn ảnh, nhiều mức."),
        P("Méo đặc trưng của JPEG là méo khối. Wavelet hết méo khối, nhưng khi nén mạnh có gợn sóng quanh cạnh, gọi là ringing."),
        P("Đổi lại, wavelet tính toán nặng hơn."),
        P("Cả hai đều có chế độ không mất dữ liệu. Trong sơ đồ JPEG2000 ở slide, đường nét đứt là chế độ lossless."),
    ], table={"headers": ["", "JPEG (DCT)", "Wavelet / JPEG2000"],
              "rows": [["Phạm vi biến đổi", "Khối 8×8", "Toàn ảnh, nhiều mức"],
                       ["Méo đặc trưng", "Méo khối (blocking)", "Gợn sóng quanh cạnh (ringing)"],
                       ["Độ phức tạp", "Thấp", "Cao hơn"], ["Chế độ lossless", "Có", "Có (đường nét đứt)"]]}),
    S("Ứng dụng", "JPEG2000 được dùng ở đâu", [
        P("Chuẩn JPEG2000 dùng biến đổi wavelet thay cho DCT theo khối.", "JPEG2000: wavelet"),
        P("JPEG2000 được dùng trong rạp chiếu phim kỹ thuật số và trong ảnh y tế theo chuẩn DICOM.", "Rạp phim số, ảnh y tế DICOM"),
    ]),
    limit("Vẫn còn gợn sóng, và JPEG cũ vẫn còn đó", [
        P("Wavelet hết ô vuông, nhưng nén rất mạnh vẫn có gợn sóng quanh các cạnh. "
          "Mọi bộ mã dựa trên biến đổi đều gặp hiện tượng này ở tỉ lệ nén cao.", "Nén mạnh → ringing"),
        P("Còn hàng tỉ ảnh JPEG có sẵn vẫn mang méo khối, không thể bắt ai mã hóa lại. Có sửa được ở phía người nhận không? "
          "Đó là hậu xử lý.", "→ Hậu xử lý ở phía nhận"),
    ], 8),
    traps([["Dead zone là gì?", "Khoảng lượng tử quanh 0 rộng hơn"],
           ["Nhiều mức phân rã luôn tốt hơn?", "Sai: thêm phép tính, sai số có thể tăng"],
           ["Wavelet loại bỏ méo nào của JPEG?", "Méo khối (nhưng vẫn có ringing)"]],
          ["Bẫy một: dead zone là khoảng lượng tử quanh số không được nới rộng hơn các khoảng khác.",
           "Bẫy hai: nhiều mức phân rã không phải lúc nào cũng tốt hơn. Phép tính tăng, sai số tái tạo có thể tăng.",
           "Bẫy ba: wavelet bỏ được méo khối, nhưng vẫn có ringing ở tỉ lệ nén cao."]),
]})

# ---------------- 08 postprocessing ----------------
stories.append({"id": "hau-xu-ly", "title": "Hậu xử lý ảnh nén", "kind": "extra", "scenes": [
    S("Vấn đề", "Ảnh giải mã mang sẵn méo", [
        P("Ảnh giải mã từ bộ nén có mất dữ liệu mang hai loại méo. Loại một là ringing, gợn sóng quanh cạnh. "
          "Nó xuất hiện ở tỉ lệ nén cao trong mọi bộ mã dựa trên biến đổi, do bản chất thông thấp của hệ thống.",
          "Ringing: do bản chất thông thấp"),
        P("Loại hai là blocking, méo khối, do lượng tử độc lập các hệ số DCT theo từng khối.", "Blocking: lượng tử DCT độc lập từng khối"),
    ]),
    S("Cách cũ", "Chấp nhận méo", [
        P("Cách cũ là chấp nhận: muốn ít méo thì nén nhẹ tay, tức là tốn thêm dung lượng.", "Muốn ít méo → nén nhẹ, tốn dung lượng"),
    ]),
    S("Ý tưởng", "Sửa ở phía người nhận", [
        P("Ý tưởng: không đổi chuẩn nén, không đổi chuỗi bit. Sau khi giải mã xong, ta xử lý thêm để giảm méo.",
          "Không đổi chuẩn, xử lý sau giải mã"),
        P("Slide nhắc lại từng bước của JPEG, từ chia khối, DCT, lượng tử đến DCT ngược, để chỉ ra chính xác thông tin bị mất ở đâu. "
          "Biết méo sinh ra ở bước nào thì biết cần phục hồi cái gì.", "Biết méo sinh ở bước nào → biết sửa gì"),
    ]),
    S("Cách làm", "Chèn một bước sau bộ giải mã", [
        P("Bộ giải mã chuẩn làm việc như bình thường.", "Giải mã chuẩn, không đổi", reveal=1),
        P("Khối hậu xử lý chen vào trước khi hiển thị: làm mượt ranh giới khối và gợn sóng, nhưng phải giữ các cạnh thật của ảnh.",
          "Làm mượt biên khối, giữ cạnh thật", reveal=2),
    ], graph=pipeline(["Chuỗi bit", "Giải mã JPEG", "Hậu xử lý", "Ảnh hiển thị"], [0, 1, 2, 2])),
    S("Ứng dụng", "Ở đâu có hậu xử lý", [
        P("Nhiều trình xem ảnh và video có bộ lọc khử méo khối. Ở video cuối chương, các bạn sẽ thấy học sâu cũng được dùng để khử vết nén, "
          "ví dụ mạng CAS-CNN.", "Bộ lọc khử khối; CAS-CNN"),
    ]),
    limit("Chỉ đoán lại phần đã mất", [
        P("Hậu xử lý chỉ đoán lại phần đã mất, không lấy lại được thông tin thật. Và đến giờ ta vẫn chỉ nói về ảnh hai chiều thông thường.",
          "Không lấy lại thông tin thật · ảnh không chỉ 2D"),
    ], 9),
    traps([["Ringing do đâu?", "Bản chất thông thấp của codec dựa trên biến đổi, ở tỉ lệ nén cao"],
           ["Blocking do đâu?", "Lượng tử độc lập hệ số DCT từng khối"]],
          ["Bẫy một: ringing do bản chất thông thấp, có ở mọi codec dựa trên biến đổi khi nén mạnh.",
           "Bẫy hai: blocking do lượng tử độc lập các hệ số DCT của từng khối."]),
]})

# ---------------- 09 multispectral & deep learning ----------------
stories.append({"id": "da-pho-hoc-sau", "title": "Mở rộng: ảnh đa phổ và nén bằng học sâu", "kind": "extra", "scenes": [
    S("Vấn đề", "Ảnh không chỉ có hai chiều", [
        P("Ảnh vệ tinh viễn thám chụp cùng một vùng đất ở nhiều dải phổ. Ảnh y tế ghép nhiều phương thức như MRI, CT, X quang. "
          "Đó là ảnh đa phổ, một khối dữ liệu ba chiều.", "Ảnh đa phổ: viễn thám, y tế đa phương thức"),
        P("Chiều thứ ba, chiều phổ, có bản chất khác hẳn hai chiều không gian, nên các kỹ thuật nén ảnh hai chiều thường không phù hợp.",
          "Chiều phổ khác chiều không gian"),
    ]),
    S("Ý tưởng", "Giải tương quan cả chiều phổ", [
        P("Các dải phổ của cùng một vùng rất giống nhau. Ngoài tương quan không gian, ta khai thác thêm tương quan giữa các dải phổ.",
          "Khai thác thêm tương quan giữa các dải"),
    ]),
    S("Cách làm", "Ba lớp bộ mã dựa trên biến đổi", [
        P("Lớp phổ không gian: áp dụng biến đổi KL trên chiều phổ trước, rồi nén từng thành phần đã giải tương quan bằng mã hóa dựa trên biến đổi."),
        P("Lớp không gian phổ: biến đổi không gian trước, như DCT khối hoặc wavelet, rồi giải tương quan chiều phổ của mỗi băng bằng biến đổi KL."),
        P("Lớp không gian phổ phức: khi các mặt phẳng ảnh không khớp nhau, cần biến đổi tần số phức để giữ thông tin pha."),
    ], table={"headers": ["Lớp", "Cách làm"],
              "rows": [["Phổ – không gian", "KL trên chiều phổ trước, rồi mã biến đổi từng thành phần"],
                       ["Không gian – phổ", "Biến đổi không gian trước (DCT, wavelet), rồi KL theo chiều phổ"],
                       ["Không gian – phổ phức", "Ảnh không khớp nhau: biến đổi tần số phức, giữ pha"]]}),
    S("Cách làm", "Nén bằng học sâu", [
        P("Hướng mới nhất thay cả chuỗi biến đổi, lượng tử và mã entropy bằng mạng nơ ron học từ đầu đến cuối.",
          "Học end-to-end thay pipeline cổ điển"),
        P("Slide nêu ba hướng. Hướng CNN, ví dụ CAS-CNN dùng mạng tích chập sâu để khử vết nén.", "CNN: CAS-CNN khử vết nén"),
        P("Hướng RNN, ví dụ mô hình nén ảnh độ phân giải đầy đủ bằng mạng hồi quy của Toderici và cộng sự.", "RNN: nén ảnh độ phân giải đầy đủ"),
        P("Và hướng GAN, nén thích ứng bằng cách bù phần dư ngữ nghĩa và cảm nhận qua mạng đối sinh.", "GAN: bù phần dư ngữ nghĩa – cảm nhận"),
    ]),
    traps([["Vì sao không nén ảnh đa phổ như ảnh 2D?", "Chiều phổ có bản chất khác chiều không gian"],
           ["Phổ – không gian làm gì trước?", "Biến đổi KL trên chiều phổ"],
           ["Ba hướng học sâu trong slide?", "CNN, RNN, GAN"]],
          ["Bẫy một: ảnh đa phổ không nén như ảnh hai chiều được, vì chiều phổ khác bản chất với chiều không gian.",
           "Bẫy hai: lớp phổ không gian biến đổi KL trên chiều phổ trước, lớp không gian phổ thì ngược lại.",
           "Bẫy ba: ba hướng học sâu trong slide là CNN, RNN và GAN."]),
]})

# ---------------- 10 summary ----------------
stories.append({"id": "tong-ket", "title": "Tổng kết chương 5", "kind": "summary", "scenes": [
    S("Tổng kết", "Chín phương pháp, một mạch", [
        P("Cùng nhìn lại cả chương. Câu hỏi ban đầu: gửi tấm ảnh trời hai trăm năm mươi sáu kilobyte bằng ít bit hơn."),
        P("Entropy cho biết giới hạn. Huffman tạo bộ mã sát giới hạn đó, mã số học vượt qua ràng buộc một bit mỗi ký hiệu của Huffman."),
        P("Chạm trần hai đến ba lần, ta chấp nhận mất dữ liệu. BTC giữ trung bình và độ lệch của khối, VQ thay cả khối bằng chỉ số trong codebook."),
        P("JPEG ghép DCT, lượng tử và Huffman thành chuẩn chung nhưng sinh méo khối. Wavelet bỏ chia khối, còn lại ringing. "
          "Hậu xử lý sửa méo ở phía nhận, còn ảnh đa phổ và học sâu mở rộng bài toán."),
    ], chain={"items": CHAIN, "current": len(CHAIN)}),
    S("Tổng kết", "Bảng so sánh nhanh", [
        P("Hai phương pháp không mất dữ liệu: Huffman ghép hai xác suất nhỏ nhất, mã số học biến cả thông điệp thành một khoảng.", reveal=[1, 2]),
        P("Hai phương pháp có mất dữ liệu làm trên pixel: BTC giữ hai moment, VQ gửi chỉ số code vector.", reveal=[3, 4]),
        P("Hai phương pháp dựa trên biến đổi: JPEG chỉ mất dữ liệu ở bước lượng tử, wavelet biến đổi toàn ảnh và dùng dead zone.", reveal=[5, 6]),
    ], table={"headers": ["Phương pháp", "Mất dữ liệu?", "Ý chính"],
              "rows": [["Huffman", "Không", "Ghép 2 xác suất nhỏ nhất"], ["Mã số học", "Không", "Cả thông điệp = một khoảng"],
                       ["BTC", "Có", "Giữ trung bình + độ lệch chuẩn"], ["VQ / LBG", "Có", "Chỉ số code vector gần nhất"],
                       ["JPEG", "Có", "Chỉ mất ở bước lượng tử"], ["Wavelet", "Có", "Toàn ảnh, dead zone"]]}),
    S("Bẫy thi", "Năm bẫy chung của chương", [
        P("Một: Huffman gộp hai ký hiệu có xác suất nhỏ nhất."),
        P("Hai: entropy là cận dưới của số bit trung bình."),
        P("Ba: trong JPEG, chỉ lượng tử hóa làm mất dữ liệu."),
        P("Bốn: BTC bảo toàn trung bình và độ lệch chuẩn của khối."),
        P("Năm: mã số học là mã không khối."),
    ], table={"headers": ["Câu hỏi", "Đáp án"],
              "rows": [["Huffman gộp hai ký hiệu nào?", "Hai ký hiệu xác suất NHỎ nhất"],
                       ["Entropy là cận trên hay cận dưới?", "Cận DƯỚI"], ["Bước nào của JPEG làm mất dữ liệu?", "Lượng tử hóa"],
                       ["BTC bảo toàn gì?", "Trung bình và độ lệch chuẩn"], ["Mã số học là mã khối?", "Sai: không khối"]]}),
    S("Tổng kết", "Sang chương 6", [
        P("Chương sau, tấm ảnh trời bắt đầu chuyển động. Video có thêm tương quan thời gian giữa các khung hình, "
          "và các bạn sẽ gặp lại DCT, lượng tử và Huffman bên trong các chuẩn MPEG.", "Chương 6: nén video, tương quan thời gian"),
    ]),
]})

script = {"title": "Nén ảnh", "example": "Gửi ảnh bầu trời xám 512×512, 8 bit/pixel (256 KB) qua mạng chậm",
          "stories": stories}
OUT.write_text(json.dumps(script, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT} with {len(stories)} stories")
