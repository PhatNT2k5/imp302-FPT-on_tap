import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, chain, limit, pipeline, story, traps, write  # noqa: E402

CHAIN = ["Khoảng cách tối thiểu", "Bayes", "Perceptron", "Mạng nơ-ron", "CNN kinh điển"]
EX = "Máy phân loại hoa trong vườn ươm: đo cánh hoa rồi cho biết thuộc giống nào"


def min_distance_graph():
    def at(x, y):
        return {"x": x, "y": 2 - y}
    return {"nodes": [{"id": "m1", "label": "m1", **at(4.3, 1.3), "note": "lớp 1 (4,3; 1,3)", "marks": [{"step": 2, "style": "accent"}]},
                      {"id": "m2", "label": "m2", **at(1.5, 0.3), "note": "lớp 2 (1,5; 0,3)"},
                      {"id": "x", "label": "x", **at(3, 1), "shape": "box", "note": "hoa mới (3; 1)"}],
            "edges": [{"a": "x", "b": "m1", "label": "1,33", "step": 1, "marks": [{"step": 2, "style": "accent"}]},
                      {"a": "x", "b": "m2", "label": "1,66", "step": 1}],
            "caption": "Trục: chiều dài và chiều rộng cánh hoa"}


def perceptron_graph():
    pts = [("a", (0, 0), 1), ("b", (0, 1), 1), ("c", (1, 0), 2), ("d", (1, 1), 2)]
    nodes = [{"id": pid, "label": f"({x},{y})", "x": x * 4, "y": (1 - y) * 4, "shape": "dot",
              "marks": [{"step": 1, "style": "accent" if cls == 1 else "warn"}]} for pid, (x, y), cls in pts]
    nodes += [{"id": "top", "x": 2, "y": -0.8, "shape": "dot", "step": 2}, {"id": "bot", "x": 2, "y": 4.8, "shape": "dot", "step": 2,
                                                                            "note": "biên: x₁ = 0,5"}]
    return {"nodes": nodes, "edges": [{"a": "top", "b": "bot", "step": 2, "marks": [{"step": 2, "style": "cut"}]}],
            "caption": "Xanh: lớp 1 · cam: lớp 2 · nét đứt: biên quyết định học được"}


stories = [
    story("mo-dau", "Mở đầu: bước cuối của nhận dạng", "intro", [
        S("Mở đầu", "Một bông hoa, thuộc giống nào?", [
            P("Chào các bạn, đây là chương cuối: phân loại ảnh. Ví dụ của cả chương là một chiếc máy trong vườn ươm. "
              "Nó đo chiều dài và chiều rộng cánh hoa, rồi phải nói bông hoa thuộc giống nào.", "Ví dụ: máy phân loại hoa"),
            P("Một mẫu là sự sắp xếp các đặc trưng, viết thành vector x gồm n descriptor. Một lớp mẫu là tập các mẫu có chung tính chất. "
              "Khi đối tượng mô tả bằng cấu trúc như chuỗi ký hiệu, ta dùng mẫu cấu trúc thay cho vector.", "Mẫu = vector đặc trưng · lớp = tập mẫu chung tính chất"),
            P("Thử nghĩ: nếu các bạn là chiếc máy, các bạn sẽ quyết định bằng cách nào?", "Các bạn sẽ quyết định thế nào?", ask=True),
        ]),
        S("Mở đầu", "Bốn giai đoạn nhận dạng", [
            P("Nhận dạng gồm bốn giai đoạn: cảm biến tạo tín hiệu, tiền xử lý giảm nhiễu và phân đoạn, trích đặc trưng, rồi phân loại.", reveal=1),
            P("Các chương trước đã lo ba giai đoạn đầu. Chương này là bước cuối: gán nhãn cho mẫu dựa trên đặc trưng của nó.", reveal=2),
        ], graph=pipeline(["Cảm biến", "Tiền xử lý", "Trích đặc trưng (ch. 10)", "Phân loại (ch. 12)"], [0, 0, 1, 2])),
        S("Mở đầu", "Ba hướng phân loại", [
            P("Có ba hướng. Đối sánh với nguyên mẫu: so với một mẫu điển hình của mỗi lớp.", "1. Đối sánh nguyên mẫu"),
            P("Bộ phân loại thống kê tối ưu: Bayes, dùng xác suất.", "2. Thống kê tối ưu: Bayes"),
            P("Và mạng nơ-ron, từ perceptron đến CNN sâu. Mỗi hướng ra đời để vá chỗ hụt của hướng trước.", "3. Mạng nơ-ron"),
        ], chain=chain(CHAIN, 0)),
    ]),

    story("khoang-cach", "Đối sánh nguyên mẫu: khoảng cách tối thiểu", "method", [
        S("Vấn đề", "Bông hoa mới giống lớp nào hơn?", [
            P("Máy đo được một bông hoa mới: cánh dài ba, rộng một. Nó giống giống hoa thứ nhất hay thứ hai hơn?", "Hoa mới (3; 1): lớp nào?"),
        ]),
        S("Cách cũ", "Nhớ từng bông đã gặp", [
            P("Cách ngây thơ là nhớ mọi bông hoa từng gặp rồi so với từng bông một. Tốn bộ nhớ và chậm.", "So với từng mẫu đã gặp: tốn và chậm"),
        ]),
        S("Ý tưởng", "Một mẫu điển hình cho mỗi lớp", [
            P("Mỗi lớp được đại diện bằng một nguyên mẫu, chính là vector trung bình của mọi mẫu trong lớp. Như hình dung một quả táo điển hình.",
              "Nguyên mẫu = trung bình lớp"),
            P("Mẫu mới đi về lớp có nguyên mẫu gần nhất theo khoảng cách Euclid.", "Gán vào lớp gần nhất"),
        ]),
        S("Công thức", "Nguyên mẫu và khoảng cách", [
            P("Nguyên mẫu là trung bình các mẫu của lớp j. Khoảng cách là độ dài vector từ x đến nguyên mẫu.", "m_j = trung bình · D_j = ‖x − m_j‖"),
            P("Slide còn viết tương đương bằng hàm quyết định d: chọn khoảng cách nhỏ nhất tương đương với chọn hàm quyết định lớn nhất.",
              "Khoảng cách NHỎ nhất ⇔ hàm quyết định LỚN nhất"),
        ], formula=r"\underbrace{m_j = \frac{1}{n_j} \sum_{x \in c_j} x}_{\text{nguyên mẫu}} \qquad \underbrace{d_j(x) = m_j^T x - \tfrac{1}{2} m_j^T m_j}_{\text{hàm quyết định}}"),
        S("Cách làm", "Phân loại bông hoa mới", [
            P("Lớp một có nguyên mẫu bốn phẩy ba và một phẩy ba. Lớp hai có nguyên mẫu một phẩy năm và không phẩy ba. Hoa mới ở ba và một.", reveal=0),
            P("Thử đoán: nhìn hình, hoa mới gần lớp nào hơn?", reveal=0, ask=True),
            P("Khoảng cách tới lớp một khoảng một phẩy ba ba, tới lớp hai khoảng một phẩy sáu sáu.", reveal=1),
            P("Lớp một gần hơn, nên bông hoa thuộc lớp một.", reveal=2),
        ], graph=min_distance_graph()),
        S("Cách làm", "Cách thứ hai: hàm quyết định", [
            P("Tích vô hướng của nguyên mẫu với x: lớp một được mười bốn phẩy hai, lớp hai được bốn phẩy tám.", reveal=1),
            P("Một nửa bình phương độ dài nguyên mẫu, không phụ thuộc x nên tính sẵn: lớp một khoảng mười phẩy không chín, lớp hai khoảng một phẩy mười bảy.", reveal=2),
            P("Trừ ra: lớp một khoảng bốn phẩy một một, lớp hai khoảng ba phẩy sáu ba. Lớn nhất là lớp một, trùng kết luận. Ưu điểm: chỉ cần nhân và cộng, không cần khai căn.",
              reveal=3),
        ], table={"headers": ["Với x = (3; 1)", "Lớp 1: m1 = (4,3; 1,3)", "Lớp 2: m2 = (1,5; 0,3)"],
                  "rows": [["mᵀx", "14,2", "4,8"], ["½ mᵀm", "≈ 10,09", "≈ 1,17"], ["d(x)", "≈ 4,11 ✓", "≈ 3,63"]]}),
        S("Cách làm", "Đối sánh tương quan", [
            P("Cũng thuộc hướng nguyên mẫu, đối sánh tương quan làm việc trực tiếp với ảnh. Có một ảnh con nguyên mẫu w, ví dụ hình một chữ cái.",
              "Ảnh con nguyên mẫu w"),
            P("Trượt w trên ảnh, tại mỗi vị trí tính hệ số tương quan. Nơi tương quan lớn nhất là nơi giống mẫu nhất. Còn gọi là template matching.",
              "Tương quan lớn nhất → giống nhất"),
        ]),
        S("So sánh", "Khoảng cách và hàm quyết định", [
            P("Hai cách cho cùng kết luận: khoảng cách lấy nhỏ nhất, hàm quyết định lấy lớn nhất."),
            P("Hàm quyết định chỉ cần nhân và cộng; khoảng cách cần khai căn."),
            P("Đối sánh tương quan làm trên ảnh, lấy hệ số tương quan lớn nhất."),
        ], table={"headers": ["Cách", "Chọn lớp có", "Ghi chú"],
                  "rows": [["Khoảng cách D_j", "Giá trị NHỎ nhất", "Cần khai căn"], ["Hàm quyết định d_j", "Giá trị LỚN nhất", "Chỉ nhân và cộng"],
                           ["Tương quan (template)", "Tương quan LỚN nhất", "Làm trực tiếp trên ảnh"]]}),
        S("Ứng dụng", "Nguyên mẫu ở đâu", [
            P("Đối sánh mẫu được dùng để tìm logo, ký tự, linh kiện trên dây chuyền: những thứ có hình dạng gần như cố định.", "Tìm ký tự, logo, linh kiện"),
        ]),
        limit("Chỉ nhìn trung bình", [
            P("Khoảng cách tối thiểu chỉ nhìn trung bình mỗi lớp. Nó bỏ qua lớp nào trải rộng, lớp nào co cụm, và lớp nào phổ biến hơn.",
              "Bỏ qua độ trải và tần suất"),
            P("Hướng thống kê dùng xác suất để tính cả hai điều đó: bộ phân loại Bayes.", "→ Bayes"),
        ], CHAIN, 2),
        traps([["Khoảng cách và hàm quyết định chọn thế nào?", "Khoảng cách NHỎ nhất ⇔ d LỚN nhất"], ["Nguyên mẫu là gì?", "Vector trung bình của lớp"],
               ["Template matching tên khác?", "Đối sánh tương quan (correlation)"]],
              ["Bẫy một: khoảng cách chọn nhỏ nhất, hàm quyết định chọn lớn nhất. Đề hay đảo chiều.",
               "Bẫy hai: nguyên mẫu là vector trung bình của lớp.",
               "Bẫy ba: template matching chính là đối sánh tương quan."]),
    ]),

    story("bayes", "Bộ phân loại Bayes", "method", [
        S("Vấn đề", "Giống hiếm hay giống phổ biến?", [
            P("Trong vườn ươm, giống thứ nhất chiếm bảy mươi phần trăm số cây, giống thứ hai chỉ ba mươi. Bông hoa mới lại rất giống giống thứ hai. Máy nên chọn gì?",
              "Phổ biến hơn hay giống hơn?"),
        ]),
        S("Cách cũ", "Khoảng cách tới trung bình", [
            P("Khoảng cách tối thiểu chỉ so với trung bình, không biết lớp nào phổ biến, cũng không biết lớp nào trải rộng.", "Không biết tần suất, độ trải"),
        ]),
        S("Ý tưởng", "Như một bác sĩ chẩn đoán", [
            P("Một bệnh nhân sốt và ho. Triệu chứng khớp cả cảm cúm lẫn một bệnh hiếm. Bác sĩ cân nhắc: triệu chứng giống bệnh nào hơn, và bệnh nào phổ biến hơn.",
              "Như bác sĩ: triệu chứng + độ phổ biến"),
            P("Bayes làm đúng vậy. Hàm mật độ cho biết mẫu giống lớp j đến đâu, xác suất tiên nghiệm cho biết lớp j phổ biến đến đâu.",
              "Mật độ p(x|c) × tiên nghiệm P(c)"),
            P("Mỗi lần gán sai sinh ra một tổn thất. Bộ phân loại làm nhỏ nhất tổng tổn thất trung bình gọi là bộ phân loại Bayes.", "Tối thiểu tổn thất trung bình"),
        ]),
        S("Công thức", "Hàm quyết định với tổn thất 0–1", [
            P("Với tổn thất không một, đúng mất không, sai mất một, hàm quyết định là tích của hai phần. Chọn lớp có tích lớn nhất.", "Chọn lớp có tích lớn nhất"),
            P("Để đạt tối ưu, phải biết hàm mật độ và xác suất của mỗi lớp. Thực tế phải ước lượng từ dữ liệu, và chỉ tối ưu khi ước lượng đúng.",
              "Phải biết, hoặc ước lượng đúng, p và P"),
        ], formula=r"d_j(x) = \underbrace{p(x \mid c_j)}_{\text{giống lớp } j \text{ đến đâu}} \cdot \underbrace{P(c_j)}_{\text{lớp } j \text{ phổ biến đến đâu}}"),
        S("Cách làm", "Lớp phổ biến chưa chắc thắng", [
            P("Lớp một phổ biến, tiên nghiệm không phẩy bảy, nhưng mẫu không giống lắm, mật độ không phẩy hai. Tích là không phẩy một bốn.", reveal=1),
            P("Thử đoán: lớp hai hiếm, tiên nghiệm không phẩy ba, nhưng mật độ không phẩy sáu. Lớp nào thắng?", reveal=1, ask=True),
            P("Tích của lớp hai là không phẩy một tám, lớn hơn. Bayes chọn lớp hai, dù lớp một phổ biến gấp hơn hai lần.", reveal=2),
            P("Chia mỗi tích cho tổng không phẩy ba hai được xác suất hậu nghiệm: khoảng bốn mươi bốn và năm mươi sáu phần trăm.", reveal=2),
        ], table={"headers": ["Lớp", "p(x|c)", "P(c)", "d = p·P", "Hậu nghiệm"],
                  "rows": [["c1", "0,2", "0,7", "0,14", "≈ 0,44"], ["c2", "0,6", "0,3", "0,18 ✓", "≈ 0,56"]]}),
        S("Cách làm", "Bayes cho lớp phân phối Gauss", [
            P("Khi các lớp có phân phối Gauss, lấy logarit tự nhiên của hàm quyết định. Logarit biến tích thành tổng mà không đổi thứ tự lớn nhỏ.",
              "Lấy ln: tích → tổng, giữ thứ tự"),
            P("Số hạng giống nhau ở mọi lớp, n chia hai nhân logarit hai pi, được bỏ đi.", "Bỏ hằng số chung"),
            P("Phần còn lại gồm logarit tiên nghiệm, logarit định thức ma trận hiệp phương sai, và khoảng cách tới trung bình có tính hình dạng phân bố.",
              "ln P, ln|C|, khoảng cách tới trung bình"),
            P("Vì x xuất hiện ở dạng bình phương, các hàm quyết định là siêu mặt bậc hai, hyperquadrics.", "→ Siêu mặt bậc hai"),
        ]),
        S("So sánh", "Bayes so với khoảng cách tối thiểu", [
            P("Khoảng cách tối thiểu chỉ dùng trung bình."),
            P("Bayes dùng cả độ giống và độ phổ biến, tối ưu theo nghĩa tổn thất trung bình nhỏ nhất."),
            P("Đổi lại, Bayes cần biết hoặc ước lượng được phân phối của từng lớp."),
        ], table={"headers": ["", "Khoảng cách tối thiểu", "Bayes"],
                  "rows": [["Dùng", "Trung bình lớp", "Mật độ p(x|c) và tiên nghiệm P(c)"], ["Tối ưu?", "Không đảm bảo", "Tối thiểu tổn thất trung bình"],
                           ["Cần", "Ít dữ liệu", "Phân phối của từng lớp"]]}),
        S("Ứng dụng", "Bayes ở đâu", [
            P("Lọc thư rác, chẩn đoán y khoa, và nhiều hệ thống ra quyết định dựa trên xác suất đều dùng tư duy Bayes.", "Lọc thư rác, chẩn đoán"),
        ]),
        limit("Phải biết phân phối", [
            P("Bayes chỉ tối ưu khi biết đúng phân phối. Với ảnh thật, phân phối rất phức tạp và khó ước lượng.", "Phân phối khó ước lượng"),
            P("Có cách nào học thẳng biên quyết định từ dữ liệu, không cần biết phân phối? Đó là perceptron.", "→ Perceptron"),
        ], CHAIN, 3),
        traps([["Hàm quyết định Bayes (0–1)?", "p(x|c_j)·P(c_j), chọn lớn nhất"], ["Hạn chế của Bayes?", "Phải biết / ước lượng đúng p và P"],
               ["Bayes Gauss cho biên dạng gì?", "Siêu mặt bậc hai (hyperquadrics)"]],
              ["Bẫy một: với tổn thất không một, chọn lớp có tích mật độ nhân tiên nghiệm lớn nhất.",
               "Bẫy hai: hạn chế của Bayes là phải biết hàm mật độ và xác suất của từng lớp.",
               "Bẫy ba: với lớp Gauss, hàm quyết định là siêu mặt bậc hai."]),
    ]),

    story("perceptron", "Perceptron", "method", [
        S("Vấn đề", "Học biên quyết định từ ví dụ", [
            P("Ta không biết phân phối của từng giống hoa, nhưng có sẵn nhiều bông đã gán nhãn. Có thể học thẳng ranh giới từ chúng không?",
              "Có ví dụ gán nhãn, không biết phân phối"),
        ]),
        S("Cách cũ", "Bayes cần phân phối", [
            P("Bayes chỉ tối ưu khi biết đúng hàm mật độ và tiên nghiệm. Ước lượng sai thì không còn tối ưu.", "Bayes: cần phân phối đúng"),
        ]),
        S("Ý tưởng", "Một đường thẳng tự sửa sai", [
            P("Perceptron nhân mỗi đặc trưng với một trọng số, cộng lại, cộng bias, rồi qua hàm kích hoạt ra cộng một hoặc trừ một.",
              "Tổng có trọng số + bias → ±1"),
            P("Các điểm có tổng bằng không tạo thành một siêu phẳng, trong hai chiều là một đường thẳng chia mặt phẳng làm hai.", "Biên: siêu phẳng"),
            P("Nó học như người tập ném phi tiêu: ném lệch bên nào thì chỉnh tay một chút. Sai thì xê dịch trọng số một bước alpha, đúng thì giữ nguyên.",
              "Sai thì chỉnh một bước α"),
        ]),
        S("Cách làm", "Thuật toán perceptron", [
            P("Chọn hệ số học alpha dương, khởi tạo trọng số và bias tùy ý.", reveal=[1]),
            P("Lớp một muốn đầu ra dương. Nếu mẫu lớp một cho đầu ra nhỏ hơn hoặc bằng không, cộng alpha nhân mẫu vào trọng số và alpha vào bias.", reveal=[3, 4]),
            P("Lớp hai muốn đầu ra âm. Nếu mẫu lớp hai cho đầu ra lớn hơn hoặc bằng không, trừ đi.", reveal=[5, 6]),
            P("Lặp đến khi đi hết một vòng không phải sửa lần nào.", reveal=[7, 8]),
        ], code={"lines": ["chọn α > 0; w và bias tùy ý", "for từng mẫu x(k):", "    if x(k) ∈ c1 và wᵀx + b ≤ 0:", "        w ← w + α·x;  b ← b + α",
                           "    elif x(k) ∈ c2 và wᵀx + b ≥ 0:", "        w ← w − α·x;  b ← b − α", "    else: giữ nguyên",
                           "dừng khi một vòng không sửa mẫu nào"]}),
        S("Cách làm", "Chạy perceptron bằng tay", [
            P("Bốn mẫu: lớp một gồm không không và không một, lớp hai gồm một không và một một. Bắt đầu từ không, alpha bằng một. "
              "Mẫu không không cho đầu ra không, không dương, nên sai: bias tăng lên một.", reveal=1),
            P("Mẫu không một cho đầu ra một, dương, đúng.", reveal=2),
            P("Mẫu một không cho đầu ra một, không âm, sai: trọng số thành âm một và không, bias về không.", reveal=3),
            P("Mẫu một một cho âm một, đúng. Hết vòng một, sửa hai lần.", reveal=4),
            P("Thử đoán: thuật toán còn phải sửa thêm mấy lần nữa?", reveal=4, ask=True),
            P("Vòng hai và ba sửa thêm ba lần. Trọng số dừng ở âm hai và không, bias bằng một. Vòng bốn không sai mẫu nào, dừng.", reveal=6),
        ], table={"headers": ["Bước", "Mẫu", "Đầu ra", "Kết luận", "w và b sau bước"],
                  "rows": [["1", "(0,0) lớp 1", "0 ≤ 0", "Sai → cộng", "w = (0, 0), b = 1"], ["2", "(0,1) lớp 1", "1 > 0", "Đúng", "giữ nguyên"],
                           ["3", "(1,0) lớp 2", "1 ≥ 0", "Sai → trừ", "w = (−1, 0), b = 0"], ["4", "(1,1) lớp 2", "−1 < 0", "Đúng", "giữ nguyên"],
                           ["Vòng 2–3", "cả 4 mẫu", "—", "Sửa thêm 3 lần", "w = (−2, 0), b = 1"], ["Vòng 4", "cả 4 mẫu", "—", "Không sai", "Dừng"]]}),
        S("Cách làm", "Biên quyết định học được", [
            P("Bốn mẫu trên mặt phẳng: hai mẫu lớp một bên trái, hai mẫu lớp hai bên phải.", reveal=1),
            P("Biên là âm hai nhân x một cộng một bằng không, tức đường thẳng đứng x một bằng không phẩy năm, nằm đúng giữa hai lớp. "
              "Năm lần sửa là đủ, đúng như định lý hội tụ hứa hẹn, vì hai lớp khả phân tuyến tính.", reveal=2),
        ], graph=perceptron_graph()),
        S("So sánh", "Perceptron so với Bayes", [
            P("Bayes cần phân phối của lớp; perceptron chỉ cần ví dụ có nhãn."),
            P("Perceptron chỉ học được biên tuyến tính, và chỉ hội tụ chắc chắn khi hai lớp khả phân tuyến tính."),
            P("Bayes cho biên bậc hai với lớp Gauss, perceptron cho một siêu phẳng."),
        ], table={"headers": ["", "Bayes", "Perceptron"],
                  "rows": [["Cần", "Phân phối p, P", "Ví dụ có nhãn"], ["Biên", "Bậc hai (lớp Gauss)", "Siêu phẳng tuyến tính"],
                           ["Đảm bảo", "Tối ưu nếu biết đúng phân phối", "Hội tụ nếu khả phân tuyến tính"]]}),
        S("Ứng dụng", "Perceptron là viên gạch đầu tiên", [
            P("Perceptron là đơn vị nhỏ nhất của mọi mạng nơ-ron hiện đại. Mỗi nơ-ron trong mạng sâu vẫn làm đúng việc: tổng có trọng số cộng bias, rồi qua hàm kích hoạt.",
              "Viên gạch của mạng nơ-ron"),
        ]),
        limit("Một đường thẳng là không đủ", [
            P("Một perceptron chỉ vẽ được một đường thẳng. Nếu các giống hoa xen kẽ nhau, không đường thẳng nào tách được.", "Chỉ một siêu phẳng"),
            P("Ghép nhiều perceptron thành nhiều lớp thì sao? Đó là mạng nơ-ron.", "→ Mạng nơ-ron"),
        ], CHAIN, 4),
        traps([["Perceptron hội tụ khi nào?", "Hai lớp khả phân tuyến tính → hữu hạn bước"], ["Mẫu lớp 1 bị sai khi nào?", "Đầu ra ≤ 0"],
               ["Perceptron học biên gì?", "Siêu phẳng tuyến tính"]],
              ["Bẫy một: định lý hội tụ chỉ đảm bảo khi hai lớp khả phân tuyến tính.",
               "Bẫy hai: mẫu lớp một bị coi là sai khi đầu ra nhỏ hơn hoặc bằng không, kể cả bằng không.",
               "Bẫy ba: một perceptron chỉ học được biên tuyến tính."]),
    ]),

    story("mang-no-ron", "Mạng nơ-ron và lan truyền ngược", "method", [
        S("Vấn đề", "Các lớp không tách được bằng một đường thẳng", [
            P("Ảnh thật phức tạp hơn bốn điểm. Các lớp đan xen, cần những biên cong và phức tạp.", "Cần biên phức tạp"),
        ]),
        S("Cách cũ", "Một perceptron", [
            P("Một perceptron chỉ vẽ một siêu phẳng.", "Một siêu phẳng"),
        ]),
        S("Ý tưởng", "Ghép nhiều nơ-ron thành nhiều lớp", [
            P("Ghép nhiều nơ-ron thành nhiều lớp. Mỗi nơ-ron ở lớp l vẫn làm việc cũ: tổng có trọng số các đầu vào cộng bias, rồi qua hàm kích hoạt.",
              "Nhiều lớp nơ-ron"),
            P("Lớp sau xây trên kết quả của lớp trước, nên mạng ghép được nhiều đường thẳng thành biên phức tạp.", "Ghép nhiều biên đơn giản"),
        ]),
        S("Cách làm", "Lan truyền ngược bốn bước", [
            P("Một: đưa các vector mẫu vào mạng.", "1. Đưa mẫu vào", reveal=1),
            P("Hai: lan truyền tiến qua từng lớp để phân loại toàn bộ mẫu huấn luyện và tính sai số.", "2. Lan truyền tiến, tính sai số", reveal=2),
            P("Ba: lan truyền ngược sai số đầu ra qua mạng để tính lượng thay đổi cần cho từng tham số.", "3. Lan truyền ngược sai số", reveal=3),
            P("Bốn: cập nhật trọng số và bias. Về tinh thần vẫn là quy tắc sửa sai của perceptron, áp cho nhiều lớp cùng lúc.", "4. Cập nhật w và bias",
              reveal=4),
        ], graph=pipeline(["Mẫu huấn luyện", "Lan truyền tiến", "Sai số đầu ra", "Lan truyền ngược", "Cập nhật w, b"], [1, 2, 2, 3, 4])),
        S("So sánh", "Perceptron so với mạng nhiều lớp", [
            P("Perceptron: một nơ-ron, một siêu phẳng, quy tắc sửa sai đơn giản."),
            P("Mạng nhiều lớp: nhiều nơ-ron, biên phức tạp, huấn luyện bằng lan truyền ngược."),
        ], table={"headers": ["", "Perceptron", "Mạng nhiều lớp"],
                  "rows": [["Biên", "Siêu phẳng", "Phức tạp, phi tuyến"], ["Huấn luyện", "Sửa sai từng mẫu", "Lan truyền ngược"]]}),
        S("Ứng dụng", "Mạng nơ-ron ở đâu", [
            P("Mọi hệ thống nhận dạng hiện đại, từ nhận dạng chữ viết tay đến nhận diện khuôn mặt, đều là mạng nơ-ron huấn luyện bằng lan truyền ngược.",
              "Nhận dạng chữ, khuôn mặt"),
        ]),
        limit("Ảnh có quá nhiều pixel", [
            P("Đưa thẳng mọi pixel của ảnh vào một mạng kết nối đầy đủ thì số trọng số khổng lồ, và mạng không tận dụng việc pixel gần nhau liên quan với nhau.",
              "Quá nhiều trọng số, bỏ qua cấu trúc ảnh"),
            P("Mạng nơ-ron tích chập giải quyết điều đó. Video sau: các kiến trúc CNN kinh điển.", "→ CNN"),
        ], CHAIN, 5),
        traps([["Bốn bước lan truyền ngược?", "Đưa mẫu → lan truyền tiến, tính sai số → lan truyền ngược → cập nhật"],
               ["Nơ-ron lớp l làm gì?", "Tổng có trọng số + bias → hàm kích hoạt"]],
              ["Bẫy một: thứ tự bốn bước là đưa mẫu vào, lan truyền tiến và tính sai số, lan truyền ngược sai số, rồi cập nhật trọng số và bias.",
               "Bẫy hai: mỗi nơ-ron tính tổng có trọng số cộng bias rồi qua hàm kích hoạt."]),
    ]),

    story("cnn", "Các kiến trúc CNN kinh điển", "method", [
        S("Vấn đề", "Phân loại thẳng từ ảnh", [
            P("Thay vì tự thiết kế đặc trưng như chương mười, ta muốn mạng nhìn thẳng vào ảnh cánh hoa và tự học đặc trưng.", "Tự học đặc trưng từ ảnh"),
        ]),
        S("Cách cũ", "Đặc trưng thủ công + bộ phân loại", [
            P("Trước đây đặc trưng do con người thiết kế, rồi mới đưa vào bộ phân loại. Đặc trưng chọn kém thì bộ phân loại tốt mấy cũng không cứu được.",
              "Đặc trưng tay quyết định chất lượng"),
        ]),
        S("Ý tưởng", "Tích chập và pooling lặp lại", [
            P("CNN dùng các bộ lọc tích chập nhỏ trượt trên ảnh, giống các bộ lọc ở chương hai, nhưng hệ số được học. Pooling thu nhỏ bản đồ đặc trưng.",
              "Bộ lọc tích chập được học + pooling"),
            P("Các khối tích chập và pooling lặp lại: lớp đầu học cạnh, lớp sau học hình dạng, lớp sâu học bộ phận.", "Cạnh → hình dạng → bộ phận"),
        ]),
        S("Cách làm", "Bốn kiến trúc, mỗi đời một bước", [
            P("LeNet năm là kiến trúc kinh điển đầu tiên: ảnh vào cố định, khối tích chập pooling lặp lại, số bộ lọc tăng theo độ sâu, tách phần trích đặc trưng khỏi phần phân loại.",
              reveal=1),
            P("AlexNet mang đến ReLU sau tích chập, softmax ở đầu ra, max pooling thay average pooling, dropout, cho tích chập nối thẳng tích chập, và tăng cường dữ liệu.",
              reveal=2),
            P("VGG mười sáu dùng bộ lọc rất nhỏ ba nhân ba và một nhân một với bước trượt một, max pooling hai nhân hai, xếp chồng nhiều tích chập trước mỗi pooling, sâu mười sáu và mười chín lớp.",
              reveal=3),
            P("Thử đoán: mạng càng sâu càng khó huấn luyện vì gradient yếu dần. ResNet giải quyết thế nào?", reveal=3, ask=True),
            P("ResNet thêm kết nối tắt, cho gradient đi thẳng qua nhiều lớp, và lặp lại các khối residual. Nhờ vậy huấn luyện được tới một trăm năm mươi hai lớp.",
              reveal=4),
        ], table={"headers": ["Mạng", "Điểm mới cần nhớ"],
                  "rows": [["LeNet-5", "CNN kinh điển đầu tiên; khối conv–pool lặp lại; tách trích đặc trưng và phân loại"],
                           ["AlexNet", "ReLU, softmax, max pooling, dropout, data augmentation; conv nối conv"],
                           ["VGG16", "Bộ lọc 3×3 và 1×1, stride 1; max pool 2×2; 16 và 19 lớp"],
                           ["ResNet50", "Kết nối tắt + khối residual; tới 152 lớp, chống vanishing gradient"]]}),
        S("So sánh", "CNN so với đặc trưng thủ công", [
            P("Đặc trưng thủ công do con người chọn; CNN tự học từ dữ liệu."),
            P("CNN cần nhiều dữ liệu và tính toán, nhưng cho kết quả vượt trội trên ảnh thật."),
        ], table={"headers": ["", "Đặc trưng thủ công + phân loại", "CNN"],
                  "rows": [["Đặc trưng", "Người thiết kế", "Mạng tự học"], ["Cần", "Ít dữ liệu", "Nhiều dữ liệu, GPU"]]}),
        S("Ứng dụng", "CNN ở khắp nơi", [
            P("Các mạng này làm backbone cho phát hiện đối tượng ở chương mười một và phân đoạn ở chương chín: VGG, ResNet xuất hiện ở khắp nơi.",
              "Backbone cho phát hiện, phân đoạn"),
        ]),
        limit("Cần rất nhiều dữ liệu", [
            P("CNN mạnh nhưng đói dữ liệu và tính toán. Đây là điểm dừng của môn học, và là điểm khởi đầu của học sâu.", "Đói dữ liệu, tính toán"),
        ], CHAIN, 5),
        traps([["AlexNet mang đến gì?", "ReLU, softmax, max pooling, dropout, augmentation"], ["VGG16 dùng bộ lọc cỡ nào?", "3×3 và 1×1, stride 1"],
               ["ResNet giải quyết gì?", "Vanishing gradient nhờ kết nối tắt"]],
              ["Bẫy một: AlexNet dùng ReLU, softmax, max pooling, dropout và tăng cường dữ liệu.",
               "Bẫy hai: VGG mười sáu dùng bộ lọc ba nhân ba và một nhân một, bước trượt một.",
               "Bẫy ba: ResNet chống suy giảm gradient bằng kết nối tắt, sâu tới một trăm năm mươi hai lớp."]),
    ]),

    story("tong-ket", "Tổng kết chương 12 và toàn môn", "summary", [
        S("Tổng kết", "Ba hướng phân loại", [
            P("Nhìn lại chiếc máy phân loại hoa. Khoảng cách tối thiểu so với trung bình mỗi lớp."),
            P("Bayes thêm độ phổ biến và độ trải, tối ưu nếu biết phân phối."),
            P("Perceptron học thẳng biên từ ví dụ, mạng nơ-ron ghép nhiều perceptron, và CNN tự học đặc trưng từ ảnh."),
        ], chain=chain(CHAIN, len(CHAIN))),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: khoảng cách chọn nhỏ nhất, hàm quyết định chọn lớn nhất."), P("Hai: Bayes với tổn thất không một chọn tích mật độ nhân tiên nghiệm lớn nhất."),
            P("Ba: Bayes Gauss cho siêu mặt bậc hai."), P("Bốn: perceptron hội tụ khi khả phân tuyến tính."),
            P("Năm: ResNet dùng kết nối tắt chống suy giảm gradient."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Khoảng cách / hàm quyết định?", "Nhỏ nhất / lớn nhất"], ["Bayes 0–1?", "max p(x|c)·P(c)"], ["Bayes Gauss?", "Siêu mặt bậc hai"],
                           ["Perceptron hội tụ?", "Khi khả phân tuyến tính"], ["ResNet?", "Kết nối tắt, chống vanishing gradient"]]}),
        S("Tổng kết", "Toàn môn trong một mạch", [
            P("Cả môn học là một chuỗi: xử lý ảnh mức xám và lọc ảnh ở chương một, hai; phục hồi và biến đổi ở chương ba, bốn; "
              "nén ảnh và video ở chương năm, sáu; thu nhận và hiển thị ở chương bảy, tám; rồi phân đoạn, đặc trưng, phát hiện và phân loại ở chương chín đến mười hai.",
              "Xử lý → nén → thu nhận, hiển thị → hiểu ảnh"),
            P("Chúc các bạn ôn tập tốt và thi thật tốt.", "Chúc các bạn thi tốt!"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–8", "Máy phân loại hoa", "—", "Mẫu, lớp mẫu, 4 giai đoạn, 3 hướng", "→ Khoảng cách tối thiểu"],
    ["Khoảng cách tối thiểu", "9–12", "Hoa mới giống lớp nào", "Nhớ từng mẫu", "Nguyên mẫu = trung bình; hàm quyết định; template matching", "Bỏ qua tần suất, độ trải → Bayes"],
    ["Bayes", "13–20", "Giống hiếm hay phổ biến", "Chỉ trung bình", "p(x|c)·P(c); Gauss → siêu mặt bậc hai", "Cần phân phối → perceptron"],
    ["Perceptron", "21–25", "Học biên từ ví dụ", "Bayes cần phân phối", "Sửa sai bước α; hội tụ nếu khả phân tuyến tính", "Một đường thẳng → mạng nơ-ron"],
    ["Mạng nơ-ron", "26–28", "Biên phức tạp", "Một perceptron", "Nhiều lớp; lan truyền ngược 4 bước", "Quá nhiều trọng số → CNN"],
    ["CNN kinh điển", "29–34", "Tự học đặc trưng từ ảnh", "Đặc trưng thủ công", "LeNet → AlexNet → VGG16 → ResNet50", "→ Tổng kết môn"],
    ["Tổng kết", "—", "—", "—", "Ba hướng, bẫy chung, toàn môn", "—"],
]
write(12, "Phân loại ảnh", EX, stories, MAP)
