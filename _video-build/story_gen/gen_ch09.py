import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, pipeline, story, traps, write  # noqa: E402

CHAIN = ["K-means", "SLIC", "Cắt đồ thị", "Normalized Cut", "Ảnh sai khác", "Phân đoạn video", "Theo dõi & học sâu"]
EX = "Camera giao thông ở một ngã tư: tách bầu trời, mặt đường và từng chiếc xe"


def kmeans_graph():
    values = [1, 2, 3, 10, 11, 12]
    first_a = {1}
    nodes = []
    for v in values:
        marks = [{"step": 2, "style": "accent" if v in first_a else "warn"}]
        if v in (2, 3):
            marks.append({"step": 4, "style": "accent"})
        nodes.append({"id": f"p{v}", "label": str(v), "x": v, "y": 2, "shape": "dot", "marks": marks})
    centres = [("a1", "A", 1, 1, 3), ("b1", "B", 2, 1, 3), ("a2", "A", 1, 3, 5), ("b2", "B", 7.6, 3, 5),
               ("a3", "A", 2, 5, None), ("b3", "B", 11, 5, None)]
    for cid, label, x, step, dim in centres:
        node = {"id": cid, "label": label, "x": x, "y": 0, "step": step,
                "marks": [{"step": step, "style": "accent" if label == "A" else "warn"}]}
        if dim:
            node["marks"].append({"step": dim, "style": "dim"})
        node["note"] = str(x).replace(".", ",")
        nodes.append(node)
    return {"nodes": nodes, "caption": "Hàng dưới: 6 pixel (mức xám) · hàng trên: tâm cụm A, B qua từng vòng"}


def slic_graph():
    return {"nodes": [{"id": "p", "label": "pixel", "x": 3, "y": 3},
                      {"id": "a", "label": "A: cùng màu, ở xa", "x": 6, "y": 0, "shape": "box", "note": "khác màu 4 · xa 8"},
                      {"id": "b", "label": "B: khác màu, ở gần", "x": 0, "y": 0, "shape": "box", "note": "khác màu 8 · xa 2"}],
            "edges": [{"a": "p", "b": "a", "label": "c=1: 4,08 · c=20: 16,49", "marks": [{"step": 1, "style": "accent"}, {"step": 2, "style": "dim"}]},
                      {"a": "p", "b": "b", "label": "c=1: 8,00 · c=20: 8,94", "marks": [{"step": 2, "style": "accent"}]}],
            "caption": "s = 10; cạnh xanh = tâm được chọn (D nhỏ hơn)"}


GRAPH_NODES = [("1", 0, 0), ("2", 0, 2), ("3", 3, 0), ("4", 3, 2), ("5", 5.5, 2)]
GRAPH_EDGES = [("1", "2", 9), ("3", "4", 8), ("1", "3", 1), ("2", "4", 2), ("4", "5", 1)]


def five_node_graph(cuts):
    """cuts: {step: [edge keys cut at that step]}; an edge cut at an earlier step is dimmed when a later cut appears."""
    edges = []
    for a, b, w in GRAPH_EDGES:
        marks = []
        for step, keys in sorted(cuts.items()):
            if (a, b) in keys:
                marks.append({"step": step, "style": "cut"})
            elif marks:
                marks.append({"step": step, "style": "dim"})
        edges.append({"a": a, "b": b, "label": str(w), "marks": marks})
    nodes = [{"id": n, "label": n, "x": x, "y": y} for n, x, y in GRAPH_NODES]
    return {"nodes": nodes, "edges": edges, "caption": "Số trên cạnh = độ giống nhau w; nét đứt cam = cạnh bị cắt"}


stories = [
    intro("mo-dau", "Mở đầu: từ pixel đến vùng có nghĩa", "Một khung hình, hàng trăm nghìn pixel", [
        P("Chào các bạn. Chương chín là phân đoạn ảnh và video. Ta sẽ đi theo một ví dụ: camera giao thông ở một ngã tư. "
          "Trong mỗi khung hình có bầu trời, mặt đường, vạch kẻ, và những chiếc xe đang chạy.", "Ví dụ: camera giao thông ở ngã tư"),
        P("Máy tính chỉ thấy hàng trăm nghìn con số rời rạc. Muốn đếm xe hay đo tốc độ, trước hết phải gom pixel thành những vùng có nghĩa. "
          "Đó là phân đoạn: chia ảnh thành các vùng thỏa một số điều kiện.", "Phân đoạn: chia ảnh thành các vùng có nghĩa"),
        P("Có hai cách nhìn. Dựa vào sự gián đoạn: tìm chỗ cường độ đổi đột ngột, tức là đường biên. "
          "Dựa vào sự tương đồng: gom những pixel giống nhau thành vùng. Phần lớn chương này đi theo cách thứ hai.",
          "Gián đoạn → biên · tương đồng → vùng"),
    ], CHAIN, [
        P("Ở chương một ta đã có ngưỡng hóa và Otsu, nhưng chúng chỉ chia được hai lớp. Chương này đi tiếp: K-means chia nhiều lớp, "
          "SLIC thêm vị trí, cắt đồ thị và Normalized Cut nhìn quan hệ giữa từng cặp pixel.", "Ảnh tĩnh: K-means → SLIC → cắt đồ thị → Ncut"),
        P("Rồi ta thêm thời gian: ảnh sai khác để bắt vật chuyển động, phân đoạn video, theo dõi đối tượng và học sâu.",
          "Thêm thời gian: ảnh sai khác → video → theo dõi"),
        P("Mỗi video sau là một phương pháp, và mỗi phương pháp sinh ra để vá chỗ hụt của phương pháp trước.", "Xem theo thứ tự"),
    ]),

    story("k-means", "K-means: gom pixel theo màu", "method", [
        S("Vấn đề", "Ảnh ngã tư có nhiều hơn hai vùng", [
            P("Nhìn khung hình ngã tư: trời sáng, đường xám, xe nhiều màu. Ta muốn chia ảnh thành vài vùng, mỗi vùng một kiểu màu.",
              "Trời, đường, xe: nhiều hơn 2 vùng"),
            P("Và ta không muốn tự đặt ngưỡng bằng tay cho từng ảnh.", "Không muốn tự đặt ngưỡng"),
        ]),
        S("Cách cũ", "Ngưỡng hóa và Otsu", [
            P("Ở chương một, ngưỡng hóa và Otsu chia ảnh thành nền và vật thể bằng một ngưỡng mức xám.", "Chương 1: một ngưỡng, hai lớp"),
            P("Chỗ hụt: chỉ được hai lớp, và chỉ nhìn mức xám. Ảnh màu với trời, đường và xe thì không đủ.", "Chỉ 2 lớp, chỉ mức xám"),
        ]),
        S("Ý tưởng", "Mỗi pixel đi về tâm gần nhất", [
            P("Ý tưởng của K-means: chọn trước k tâm cụm. Mỗi pixel đi về tâm giống nó nhất. Rồi dời mỗi tâm về giữa nhóm của nó, và lặp lại.",
              "Gán về tâm gần nhất ↔ dời tâm về trung bình"),
            P("Giống như chia học sinh thành k nhóm theo chiều cao: ai gần trưởng nhóm nào thì về nhóm đó, rồi chọn lại trưởng nhóm là người ở giữa nhóm.",
              "Như chia nhóm theo chiều cao"),
            P("Các bạn đã gặp đúng thuật toán này ở chương năm, dưới tên LBG khi thiết kế codebook.", "Chương 5: LBG"),
        ]),
        S("Cách làm", "Sáu pixel, k bằng hai", [
            P("Lấy sáu pixel có mức xám một, hai, ba, mười, mười một, mười hai. Mắt ta thấy ngay hai nhóm tối và sáng.",
              "6 pixel: 1, 2, 3, 10, 11, 12", reveal=0),
            P("Để thấy thuật toán tự sửa sai, ta cố tình khởi tạo hai tâm rất tệ: một và hai.", "Khởi tạo tệ: A = 1, B = 2", reveal=1),
            P("Vòng một: pixel một gần tâm A nhất, mọi pixel còn lại đều gần B hơn.", "Gán: A = {1}, B = phần còn lại", reveal=2),
            P("Thử đoán: khi dời tâm về trung bình nhóm, tâm B sẽ đi về đâu?", "Thử đoán: B đi về đâu?", reveal=2, ask=True),
            P("Tâm A vẫn là một. Tâm B là trung bình của hai, ba, mười, mười một, mười hai, tức bảy phẩy sáu.", "Tâm mới: 1 và 7,6", reveal=3),
            P("Vòng hai: pixel hai và ba giờ gần A hơn, nên chuyển sang cụm A.", "Gán lại: A = {1, 2, 3}", reveal=4),
            P("Tâm mới là hai và mười một. Vòng ba không pixel nào đổi cụm, thuật toán dừng với đúng hai vùng tối và sáng.",
              "Tâm 2 và 11 → hội tụ", reveal=5),
        ], graph=kmeans_graph()),
        S("Cách làm", "Thuật toán K-means", [
            P("Với ảnh xám, mỗi pixel là một con số. Với ảnh màu, đó là một vector ba chiều.", reveal=[1]),
            P("Chọn trước số cụm k, khởi tạo k tâm.", reveal=[2]),
            P("Lặp hai bước: gán mỗi pixel về cụm có tâm gần nhất, rồi cập nhật tâm bằng trung bình các pixel vừa gán.", reveal=[3, 4, 5]),
            P("Dừng khi sai số dư, tức khoảng cách giữa tâm mới và tâm cũ, nhỏ hơn một ngưỡng cho trước.", reveal=[6]),
        ], code={"lines": ["mỗi pixel → vector đặc trưng (xám: 1 số, màu: 3 số)", "khởi tạo k tâm cụm", "repeat:",
                           "    gán mỗi pixel vào cụm có tâm gần nhất", "    tâm mới ← trung bình các pixel trong cụm",
                           "until ‖tâm mới − tâm cũ‖ < ngưỡng (residual error)"]}),
        S("So sánh", "K-means so với ngưỡng hóa", [
            P("Ngưỡng hóa cho hai lớp, K-means cho k lớp tùy chọn."),
            P("Ngưỡng hóa chỉ nhìn mức xám, K-means nhận cả vector màu."),
            P("Đổi lại, K-means phải chọn trước k, và kết quả phụ thuộc cách khởi tạo: khởi tạo khác có thể dừng ở kết quả kém hơn."),
        ], table={"headers": ["", "Ngưỡng hóa / Otsu", "K-means"],
                  "rows": [["Số lớp", "2", "k tùy chọn"], ["Nhìn vào", "Mức xám", "Vector màu / đặc trưng"],
                           ["Điểm yếu", "Chỉ 2 lớp", "Chọn k, phụ thuộc khởi tạo"]]}),
        S("Ứng dụng", "K-means ở đâu", [
            P("K-means được dùng để giảm số màu của ảnh, gom vùng màu trong ảnh vệ tinh, và làm bước khởi đầu cho nhiều thuật toán phân đoạn khác.",
              "Giảm số màu, ảnh vệ tinh, bước khởi đầu"),
            P("Và ngay video sau, SLIC chính là một biến thể của K-means.", "SLIC là biến thể của K-means"),
        ]),
        limit("Hai pixel cùng màu ở hai góc ảnh", [
            P("K-means chỉ nhìn màu, bỏ qua vị trí. Một chiếc xe xám ở góc trái và mặt đường xám ở góc phải bị gom vào cùng một cụm.",
              "Bỏ qua vị trí"),
            P("Nó còn phải so mọi pixel với mọi tâm trên toàn ảnh, rất chậm với ảnh lớn. Video sau: siêu điểm ảnh SLIC.",
              "So toàn ảnh: chậm → SLIC"),
        ], CHAIN, 2),
        traps([["K-means lặp hai bước nào?", "Gán vào tâm gần nhất, cập nhật tâm = trung bình"],
               ["Khi nào dừng?", "Residual error (tâm mới − tâm cũ) < ngưỡng"],
               ["Kết quả có luôn tốt nhất?", "Không: phụ thuộc khởi tạo"]],
              ["Bẫy một: K-means lặp hai bước, gán về tâm gần nhất rồi cập nhật tâm bằng trung bình.",
               "Bẫy hai: điều kiện dừng là sai số dư giữa tâm mới và tâm cũ nhỏ hơn ngưỡng.",
               "Bẫy ba: kết quả phụ thuộc khởi tạo, không phải lúc nào cũng tốt nhất."]),
    ]),

    story("slic", "Siêu điểm ảnh và SLIC", "method", [
        S("Vấn đề", "Hàng triệu pixel, hàng triệu phép so sánh", [
            P("Ảnh camera có hàng triệu pixel. Thuật toán nào xử lý từng pixel một cũng nặng nề, và phải gánh cả những chi tiết vụn vặt.",
              "Quá nhiều pixel, quá nhiều chi tiết vụn"),
            P("Ta muốn gom pixel thành những mảnh nhỏ trước, rồi mới phân đoạn trên các mảnh đó.", "Gom thành mảnh nhỏ trước"),
        ]),
        S("Cách cũ", "K-means bỏ qua vị trí và quét cả ảnh", [
            P("K-means gom theo màu, nên một mảnh có thể rải rác khắp ảnh.", "Mảnh rải rác khắp ảnh"),
            P("Và mỗi tâm phải so với mọi pixel trên toàn ảnh.", "So với mọi pixel: chậm"),
        ]),
        S("Ý tưởng", "Mảnh ghép nhỏ: gần nhau và giống nhau", [
            P("Siêu điểm ảnh thay lưới pixel bằng những vùng nhỏ có ý nghĩa cảm nhận hơn từng pixel, giống các mảnh ghép xếp hình.",
              "Superpixel: vùng nhỏ thay cho pixel"),
            P("Mục tiêu là giảm tính toán và bỏ chi tiết thừa, nhưng bắt buộc giữ ranh giới thật giữa các vùng.",
              "Giảm tính toán, giữ ranh giới thật"),
            P("SLIC làm điều đó bằng K-means với vector năm chiều: ba thành phần màu và hai tọa độ. Pixel phải vừa giống màu, vừa ở gần.",
              "SLIC: K-means 5 chiều = 3 màu + 2 tọa độ"),
        ]),
        S("Công thức", "Khoảng cách kết hợp màu và vị trí", [
            P("Khoảng cách từ pixel đến tâm có hai phần: phần khác màu, và phần xa về vị trí.", "Khác màu + xa vị trí"),
            P("Phần vị trí được chia cho s, khoảng cách giữa các tâm trên lưới ban đầu, để hai phần cùng thang đo.", "Chia cho s: cùng thang đo"),
            P("Hằng số c quyết định bên nào nặng hơn. c lớn: vị trí quan trọng, mảnh gọn và đều. c nhỏ: màu quan trọng, mảnh bám ranh giới nhưng méo hơn.",
              "c lớn → gọn · c nhỏ → bám ranh giới"),
        ], formula=r"D = \sqrt{ \underbrace{d_c^2}_{\text{khác màu}} + \underbrace{\left(\frac{d_s}{s}\right)^2}_{\text{xa vị trí}} \underbrace{c^2}_{\text{trọng số}} }"),
        S("Cách làm", "Trọng số c đổi quyết định", [
            P("Một pixel phân vân giữa hai tâm. Tâm A cùng màu nhưng ở xa: khoảng cách màu bốn, khoảng cách không gian tám. "
              "Tâm B khác màu nhưng ở gần: màu tám, không gian hai. Lưới s bằng mười.", reveal=0),
            P("Thử đoán: với c bằng một, pixel chọn tâm nào?", reveal=0, ask=True),
            P("Với c bằng một, phần vị trí gần như không đáng kể. Khoảng cách tới A là bốn phẩy không tám, tới B là tám. Pixel chọn A, tức là chọn theo màu.",
              reveal=1),
            P("Với c bằng hai mươi, phần vị trí bị nhân lên rất mạnh. Tới A là mười sáu phẩy bốn chín, tới B chỉ tám phẩy chín bốn. Pixel chọn B, tức là chọn theo vị trí.",
              reveal=2),
        ], graph=slic_graph()),
        S("Cách làm", "Thuật toán SLIC", [
            P("Đặt các tâm trên lưới đều cách nhau s pixel, rồi dời mỗi tâm tới điểm gradient thấp nhất trong ô ba nhân ba, để tâm không rơi trúng cạnh hay nhiễu.",
              reveal=[1, 2]),
            P("Khác biệt quan trọng nhất so với K-means: mỗi tâm chỉ xét pixel trong vùng hai s nhân hai s quanh nó, không quét cả ảnh.", reveal=[4]),
            P("Gán pixel về tâm có khoảng cách D nhỏ nhất, cập nhật tâm, lặp đến hội tụ.", reveal=[3, 5, 6, 7]),
            P("Cuối cùng hậu xử lý: mỗi pixel trong một vùng được thay bằng giá trị trung bình của vùng.", reveal=[8]),
        ], code={"lines": ["đặt tâm cụm trên lưới đều, cách nhau s pixel", "dời mỗi tâm đến điểm gradient thấp nhất trong ô 3×3",
                           "repeat:", "    với mỗi tâm: chỉ xét pixel trong vùng 2s × 2s", "    gán pixel vào tâm có D nhỏ nhất",
                           "    cập nhật tâm = trung bình vector 5 chiều", "until hội tụ",
                           "hậu xử lý: pixel ← giá trị trung bình vùng của nó"]}),
        S("So sánh", "SLIC so với K-means", [
            P("K-means dùng vector màu, SLIC thêm hai tọa độ thành năm chiều."),
            P("K-means quét cả ảnh, SLIC chỉ tìm trong vùng hai s nhân hai s, nên nhanh hơn rất nhiều."),
            P("Kết quả của SLIC là các mảnh nhỏ gọn bám ranh giới, nhưng chưa phải đối tượng hoàn chỉnh."),
        ], table={"headers": ["", "K-means", "SLIC"],
                  "rows": [["Đặc trưng", "Màu", "Màu + vị trí (5 chiều)"], ["Vùng tìm", "Toàn ảnh", "2s × 2s quanh tâm"],
                           ["Kết quả", "Cụm màu, có thể rải rác", "Mảnh nhỏ gọn, giữ ranh giới"]]}),
        S("Ứng dụng", "Siêu điểm ảnh dùng làm gì", [
            P("Siêu điểm ảnh là bước tiền xử lý phổ biến: thay vì phân đoạn trên hàng triệu pixel, các thuật toán sau chỉ làm trên vài trăm mảnh.",
              "Tiền xử lý: triệu pixel → vài trăm mảnh"),
            P("Ví dụ cắt đồ thị ở video sau có thể dùng mỗi siêu điểm ảnh làm một nút, đồ thị nhỏ đi rất nhiều.", "Mỗi mảnh làm một nút đồ thị"),
        ]),
        limit("Mảnh nhỏ, chưa phải đối tượng", [
            P("SLIC cho ra các mảnh nhỏ, chưa phải chiếc xe hay mặt đường hoàn chỉnh.", "Mảnh nhỏ, chưa phải đối tượng"),
            P("Và cả K-means lẫn SLIC chỉ so mỗi pixel với tâm cụm, không xét trực tiếp từng cặp pixel giống nhau đến đâu. "
              "Video sau nhìn ảnh như một đồ thị: cắt đồ thị.", "Chưa xét quan hệ từng cặp pixel → cắt đồ thị"),
        ], CHAIN, 3),
        traps([["Vector đặc trưng SLIC mấy chiều?", "5: ba màu + hai tọa độ"],
               ["SLIC tìm pixel trong vùng nào?", "2s × 2s quanh tâm"], ["c lớn thì sao?", "Siêu điểm ảnh gọn hơn (ưu tiên vị trí)"]],
              ["Bẫy một: vector của SLIC có năm chiều, ba cho màu và hai cho tọa độ.",
               "Bẫy hai: SLIC chỉ tìm trong vùng hai s nhân hai s quanh mỗi tâm, đó là lý do nó nhanh.",
               "Bẫy ba: c lớn làm mảnh gọn hơn, c nhỏ làm mảnh bám ranh giới hơn. Đề hay đảo hai vế này."]),
    ]),

    story("cat-do-thi", "Phân đoạn bằng cắt đồ thị", "method", [
        S("Vấn đề", "Ranh giới nằm ở đâu giữa xe và đường?", [
            P("Giữa chiếc xe và mặt đường, đâu là ranh giới tốt nhất? Câu trả lời phụ thuộc vào từng cặp pixel kề nhau giống nhau đến mức nào.",
              "Ranh giới phụ thuộc từng cặp pixel"),
        ]),
        S("Cách cũ", "So pixel với tâm cụm", [
            P("K-means và SLIC chỉ so mỗi pixel với tâm cụm. Quan hệ trực tiếp giữa hai pixel cạnh nhau không được dùng đến.",
              "Chỉ so với tâm, không so từng cặp"),
        ]),
        S("Ý tưởng", "Ảnh là một lưới dây chun", [
            P("Coi mỗi pixel là một nút. Hai nút nối bằng một cạnh có trọng số w, càng giống nhau trọng số càng lớn.",
              "Nút = pixel · cạnh w = độ giống nhau"),
            P("Hình dung những sợi dây chun: pixel giống nhau nối bằng dây dày, pixel khác nhau nối bằng dây mảnh. Phân đoạn là cầm kéo cắt mạng lưới thành hai phần.",
              "Như lưới dây chun: cắt chỗ dây mảnh"),
            P("Chi phí nhát cắt là tổng trọng số các dây bị cắt. Ta muốn cắt những dây mảnh nhất.", "Chi phí = tổng w các cạnh bị cắt"),
        ]),
        S("Cách làm", "Nguồn, đích và cắt cực tiểu", [
            P("Đồ thị vô hướng G gồm tập nút V và tập cạnh E, trọng số cạnh nằm trong ma trận W.", "G = (V, E), ma trận trọng số W"),
            P("Thêm hai nút đặc biệt là nguồn và đích, đại diện cho tiền cảnh và hậu cảnh. Mỗi pixel nối với chúng theo khả năng nó là xe hay là nền.",
              "Thêm nút nguồn (tiền cảnh) và đích (hậu cảnh)"),
            P("Cắt cực tiểu là nhát cắt có tổng trọng số nhỏ nhất mà tách được nguồn khỏi đích.", "Min cut: tổng w nhỏ nhất, tách nguồn khỏi đích"),
        ]),
        S("Cách làm", "Cắt cực tiểu trên đồ thị năm nút", [
            P("Xét đồ thị năm nút. Nút một và hai nối rất chặt, trọng số chín. Ba và bốn cũng chặt, trọng số tám. "
              "Giữa hai nhóm chỉ có hai dây mảnh, một và hai. Nút năm treo vào nút bốn bằng một dây trọng số một.", reveal=0),
            P("Thử đoán: nhát cắt rẻ nhất là nhát nào?", reveal=0, ask=True),
            P("Nhát cắt tách riêng nút năm chỉ cắt một dây, chi phí bằng một. Đó là nhát rẻ nhất, nên cắt cực tiểu chọn nó.", reveal=1),
        ], graph=five_node_graph({1: [("4", "5")]})),
        S("So sánh", "Cắt đồ thị so với K-means, SLIC", [
            P("K-means và SLIC so pixel với tâm. Cắt đồ thị nhìn độ giống nhau giữa từng cặp pixel."),
            P("Nhờ vậy cắt đồ thị thường cho kết quả tốt hơn các phương pháp khác."),
            P("Cái giá là cài đặt phức tạp hơn và chạy chậm hơn."),
        ], table={"headers": ["", "K-means / SLIC", "Cắt đồ thị"],
                  "rows": [["So sánh", "Pixel với tâm cụm", "Từng cặp pixel"], ["Chất lượng", "Khá", "Thường tốt hơn"],
                           ["Chi phí", "Nhẹ", "Phức tạp, chậm hơn"]]}),
        S("Ứng dụng", "Cắt đồ thị ở đâu", [
            P("Kiểu tách tiền cảnh khỏi nền như công cụ chọn vùng thông minh trong phần mềm chỉnh ảnh dựa trên ý tưởng nguồn và đích này: người dùng đánh dấu vài pixel là vật, vài pixel là nền.",
              "Tách tiền cảnh trong phần mềm chỉnh ảnh"),
        ]),
        limit("Cắt cực tiểu thích cắt nút lẻ loi", [
            P("Ví dụ vừa rồi lộ ra tật xấu: cắt cực tiểu thích tách riêng một nút lẻ loi, vì nút đó ít dây nên cắt rẻ. Kết quả là những vùng một hai pixel, vô nghĩa.",
              "Thích cắt nút lẻ → vùng vô nghĩa"),
            P("Mắt ta thấy hai nhóm một hai và ba bốn năm. Muốn thuật toán thấy giống vậy, cần chuẩn hóa chi phí cắt. Đó là Normalized Cut.",
              "→ Normalized Cut"),
        ], CHAIN, 4),
        traps([["Trọng số w(i,j) nói gì?", "Độ tương đồng giữa nút i và j"], ["Cut là gì?", "Phân hoạch V thành A, B; chi phí = tổng w bị cắt"],
               ["Nút nguồn và đích?", "Đại diện tiền cảnh và hậu cảnh"]],
              ["Bẫy một: trọng số cạnh tỉ lệ thuận với độ giống nhau, không phải khoảng cách.",
               "Bẫy hai: một nhát cắt chia tập nút thành hai tập A và B, chi phí là tổng trọng số các cạnh bị cắt.",
               "Bẫy ba: hai nút thêm vào là nguồn và đích, đại diện cho tiền cảnh và hậu cảnh."]),
    ]),

    story("ncut", "Normalized Cut", "method", [
        S("Vấn đề", "Nhát cắt rẻ nhất lại vô nghĩa", [
            P("Cắt cực tiểu tách riêng nút năm vì chỉ tốn một. Nhưng một vùng một pixel không phải chiếc xe nào cả.", "Rẻ nhất nhưng vô nghĩa"),
        ]),
        S("Cách cũ", "Chi phí cắt tuyệt đối", [
            P("Cắt cực tiểu dùng tổng trọng số tuyệt đối. Phần càng nhỏ thì càng ít dây, càng rẻ, nên luôn bị ưu tiên.",
              "Giá trị tuyệt đối → ưu tiên phần nhỏ"),
        ]),
        S("Ý tưởng", "Tính chi phí theo tỉ lệ", [
            P("Normalized Cut chia chi phí cắt cho tổng mức độ kết nối của mỗi phần với toàn đồ thị.", "Chia cho tổng kết nối mỗi phần"),
            P("Giống như phạt theo phần trăm chứ không theo số tuyệt đối: một phần nhỏ xíu mất một dây là mất gần hết kết nối của nó, nên bị phạt nặng.",
              "Như phạt theo phần trăm"),
        ]),
        S("Công thức", "Công thức Ncut", [
            P("Mỗi phân số là chi phí cắt chia cho tổng nối của một phần. Phần nào nhỏ xíu thì mẫu số nhỏ, phân số lớn.", "Phần nhỏ → phân số lớn"),
            P("Slide còn cho đẳng thức: Ncut bằng hai trừ Nassoc, trong đó Nassoc đo liên kết bên trong mỗi phần. Làm nhỏ Ncut cũng là làm lớn liên kết bên trong.",
              "Ncut = 2 − Nassoc"),
        ], formula=r"Ncut(A,B) = \frac{cut(A,B)}{\underbrace{assoc(A,V)}_{\text{tổng nối của } A}} + \frac{cut(A,B)}{assoc(B,V)}"),
        S("Cách làm", "Ncut trên đồ thị năm nút", [
            P("Quay lại đồ thị năm nút. Tổng nối của nút năm chỉ là một, phần còn lại là bốn mươi mốt.", reveal=0),
            P("Nhát cắt tách nút năm: phân số đầu bằng một chia một, phân số sau một chia bốn mươi mốt. Ncut xấp xỉ một phẩy không hai, rất lớn.",
              reveal=1),
            P("Thử đoán: nhát cắt chia một hai khỏi ba bốn năm, đắt hơn với chi phí ba, sẽ có Ncut lớn hay nhỏ?", reveal=1, ask=True),
            P("Mỗi bên có tổng nối hai mươi mốt, nên Ncut chỉ khoảng không phẩy hai chín. Ncut chọn nhát này, đúng với hai nhóm mắt ta thấy.", reveal=2),
            P("Kiểm tra đẳng thức: Nassoc khoảng một phẩy bảy một, và hai trừ một phẩy bảy một đúng bằng không phẩy hai chín.", reveal=2),
        ], graph=five_node_graph({1: [("4", "5")], 2: [("1", "3"), ("2", "4")]})),
        S("Cách làm", "Giải bằng trị riêng", [
            P("Thử mọi cách cắt là không khả thi, nên ta dùng đại số tuyến tính. Dựng đồ thị, tính ma trận trọng số W và ma trận đường chéo D chứa tổng nối mỗi nút.",
              reveal=[1]),
            P("Giải bài toán trị riêng trong slide, rồi lấy vector riêng ứng với trị riêng nhỏ thứ hai. Không phải nhỏ nhất, vì trị riêng nhỏ nhất ứng với nghiệm tầm thường không chia gì cả.",
              reveal=[2, 3]),
            P("Dùng vector riêng đó chia đôi đồ thị sao cho Ncut nhỏ nhất. Nếu chưa đủ K phần, chia đệ quy các phần nếu cần.", reveal=[4, 5]),
        ], code={"lines": ["dựng G = (V, E); tính ma trận W và D", "giải (D − W) y = λ D y",
                           "lấy vector riêng ứng với trị riêng NHỎ THỨ HAI", "chia đôi đồ thị sao cho Ncut(A, B) nhỏ nhất",
                           "nếu chưa đủ K phần: chia đệ quy nếu cần"]}),
        S("So sánh", "Min cut so với Ncut", [
            P("Min cut tính chi phí tuyệt đối nên thiên vị phần nhỏ. Ncut tính theo tỉ lệ tổng kết nối nên tránh được thiên vị đó."),
            P("Trong ví dụ, min cut chọn nhát chi phí một, Ncut chọn nhát chi phí ba nhưng hợp lý."),
            P("Ncut giải bằng trị riêng, nặng hơn nhưng không cần thử mọi cách cắt."),
        ], table={"headers": ["", "Min cut", "Normalized Cut"],
                  "rows": [["Chi phí", "Tổng w tuyệt đối", "Chia cho tổng nối mỗi phần"], ["Ví dụ 5 nút", "Tách {5}, cut = 1", "{1,2} | {3,4,5}, Ncut ≈ 0,29"],
                           ["Cách giải", "Luồng cực đại / cắt cực tiểu", "Trị riêng nhỏ thứ hai"]]}),
        S("Ứng dụng", "Ncut được dùng ở đâu", [
            P("Normalized Cut là nền tảng của nhóm phương pháp phân cụm phổ, dùng để phân đoạn ảnh và gom nhóm dữ liệu nói chung.",
              "Phân cụm phổ, phân đoạn ảnh"),
        ]),
        limit("Ảnh tĩnh không thấy chuyển động", [
            P("Mọi phương pháp đến giờ chỉ nhìn một ảnh. Chiếc xe xám trên mặt đường xám rất khó tách nếu chỉ dựa vào màu.", "Xe cùng màu đường: khó tách"),
            P("Nhưng camera quay liên tục, và chiếc xe thì di chuyển. Video sau dùng chính chuyển động đó: ảnh sai khác.", "→ Dùng chuyển động"),
        ], CHAIN, 5),
        traps([["Vì sao Ncut tốt hơn min cut?", "Chuẩn hóa, tránh tách phần quá nhỏ"], ["Ncut liên hệ Nassoc thế nào?", "Ncut = 2 − Nassoc"],
               ["Dùng vector riêng nào?", "Ứng với trị riêng NHỎ THỨ HAI"]],
              ["Bẫy một: Ncut chuẩn hóa chi phí theo tổng kết nối để tránh các phân hoạch quá nhỏ.",
               "Bẫy hai: Ncut bằng hai trừ Nassoc, nên làm nhỏ Ncut là làm lớn liên kết bên trong.",
               "Bẫy ba: dùng vector riêng của trị riêng nhỏ thứ hai, không phải nhỏ nhất."]),
    ]),

    story("anh-sai-khac", "Dùng chuyển động: ảnh sai khác", "method", [
        S("Vấn đề", "Xe xám trên đường xám", [
            P("Một chiếc xe xám chạy trên mặt đường xám. Nhìn một khung hình, màu gần như không khác. Nhưng qua hai khung liên tiếp, chiếc xe đã dời chỗ.",
              "Màu giống nhau, nhưng xe có di chuyển"),
        ]),
        S("Cách cũ", "Chỉ nhìn một ảnh", [
            P("K-means, SLIC hay Ncut đều chỉ dựa vào màu và vị trí trong một ảnh, bỏ qua thông tin thời gian.", "Bỏ qua thời gian"),
        ]),
        S("Ý tưởng", "Thứ gì thay đổi thì là vật chuyển động", [
            P("Ý tưởng đơn giản nhất: so trực tiếp hai khung hình từng pixel một. Chỗ nào thay đổi đáng kể là chỗ có vật chuyển động.",
              "So từng pixel giữa hai khung"),
            P("Giống trò chơi tìm điểm khác nhau giữa hai bức tranh.", "Như trò tìm điểm khác nhau"),
        ]),
        S("Cách làm", "Ảnh sai khác từng bước", [
            P("Khung một có một chấm sáng giá trị hai trăm ở giữa.", reveal=1),
            P("Ở khung hai, chấm sáng dịch sang phải một pixel. Pixel ở giữa cũng đổi nhẹ từ mười lên mười hai do nhiễu.", reveal=2),
            P("Thử đoán: sau khi lấy chênh lệch và ngưỡng hóa với ngưỡng hai mươi, có mấy pixel được đánh dấu?", reveal=2, ask=True),
            P("Hai pixel: vị trí cũ và vị trí mới của chấm. Thay đổi nhỏ do nhiễu bị loại. Lưu ý ảnh sai khác đánh dấu cả chỗ vật vừa rời đi.", reveal=3),
        ], grid=[{"label": "Khung 1", "cells": [[10, 10, 10], [10, 200, 10], [10, 10, 10]], "accent": [[1, 1]]},
                 {"label": "Khung 2", "cells": [[10, 10, 10], [10, 12, 200], [10, 10, 10]], "accent": [[1, 2]]},
                 {"label": "|khác| > 20", "cells": [[0, 0, 0], [0, 1, 1], [0, 0, 0]], "warn": [[1, 1], [1, 2]]}]),
        S("Cách làm", "ADI và miền tần số", [
            P("Ảnh sai khác tích lũy, ADI, so một ảnh tham chiếu với mọi khung tiếp theo và cộng dồn, nên thấy được cả quỹ đạo của vật.",
              "ADI: tham chiếu so với mọi khung sau, cộng dồn"),
            P("Trong miền tần số: nếu vật đi đều một pixel mỗi khung, phép chiếu tổng cường độ qua các khung tạo ra một sóng sin phức có tần số tỉ lệ với vận tốc.",
              "Vật đi đều → sóng sin phức"),
            P("Tìm đỉnh trong phổ Fourier là biết vật đi nhanh cỡ nào.", "Đỉnh phổ Fourier → vận tốc"),
        ]),
        S("So sánh", "Ảnh sai khác so với phân đoạn ảnh tĩnh", [
            P("Phân đoạn ảnh tĩnh nhìn màu và vị trí; ảnh sai khác nhìn sự thay đổi theo thời gian."),
            P("Ảnh sai khác tách được vật chuyển động dù cùng màu nền, nhưng cần ít nhất hai khung và nhạy với nhiễu."),
            P("Ảnh sai khác đơn giản, chạy rất nhanh."),
        ], table={"headers": ["", "Phân đoạn ảnh tĩnh", "Ảnh sai khác"],
                  "rows": [["Thông tin", "Màu, vị trí", "Thay đổi theo thời gian"], ["Cần", "1 ảnh", "≥ 2 khung"],
                           ["Điểm yếu", "Vật cùng màu nền", "Nhạy nhiễu, đánh dấu cả chỗ vật rời đi"]]}),
        S("Ứng dụng", "Ảnh sai khác ở đâu", [
            P("Camera an ninh phát hiện có người đi vào khung hình, camera giao thông đếm xe chạy qua: đều bắt đầu từ việc so các khung liên tiếp.",
              "Camera an ninh, đếm xe"),
        ]),
        limit("Camera rung, ánh sáng đổi", [
            P("Nếu camera rung hay quay ngang, mọi pixel đều đổi, ảnh sai khác sáng trắng cả khung. Nếu đèn bật tắt, cũng vậy.",
              "Camera di chuyển, ánh sáng đổi → sai khắp nơi"),
            P("Ta cần những kỹ thuật bền vững hơn cho cả đoạn video. Video sau: phân đoạn video.", "→ Phân đoạn video"),
        ], CHAIN, 6),
        traps([["Ảnh sai khác đánh dấu gì?", "Cả vị trí cũ lẫn vị trí mới của vật"], ["ADI là gì?", "So ảnh tham chiếu với mọi khung sau, cộng dồn"],
               ["Miền tần số cho biết gì?", "Vận tốc: tần số sóng sin tỉ lệ vận tốc"]],
              ["Bẫy một: ảnh sai khác đánh dấu cả chỗ vật vừa rời đi, không chỉ chỗ vật đang đứng.",
               "Bẫy hai: ADI so một ảnh tham chiếu với mọi khung tiếp theo, không phải từng cặp khung liền nhau.",
               "Bẫy ba: trong miền tần số, tần số của sóng sin phức tỉ lệ với vận tốc của vật."]),
    ]),

    story("phan-doan-video", "Phân đoạn video", "method", [
        S("Vấn đề", "Cả một đoạn video dài", [
            P("Camera ghi suốt cả ngày. Ta cần biết lúc nào cảnh thay đổi, vùng nào trong mỗi khung đang chuyển động, và những vật nào chuyển động độc lập với nhau.",
              "Khi nào đổi cảnh? Vùng nào chuyển động?"),
        ]),
        S("Cách cũ", "Ảnh sai khác thô", [
            P("Ảnh sai khác đơn thuần so từng pixel, nên nhạy với nhiễu, ánh sáng và camera di chuyển.", "Nhạy nhiễu, ánh sáng, camera"),
        ]),
        S("Ý tưởng", "Phân đoạn theo cả không gian và thời gian", [
            P("Phân đoạn video là thành phần cốt lõi của tóm tắt, lập chỉ mục, truy xuất, mã hóa và biên tập video.",
              "Cốt lõi của tóm tắt, truy xuất, mã hóa video"),
            P("Ý tưởng là so ở mức thô hơn và bền hơn: so khối, so histogram, xử lý nhiều độ phân giải, và nhớ những gì đã xảy ra ở các khung trước.",
              "So thô hơn, bền hơn, có trí nhớ"),
        ]),
        S("Cách làm", "Phát hiện chuyển cảnh", [
            P("Phát hiện chuyển cảnh là phân đoạn một chiều theo trục thời gian. Ta tính độ khác biệt giữa các khung liên tiếp.", reveal=0),
            P("Thử đoán: điểm chuyển cảnh trông như thế nào trên biểu đồ này?", reveal=0, ask=True),
            P("Đó là đỉnh nhọn đột ngột: khác biệt lớn trong không gian đặc trưng, thường kết hợp màu và chuyển động.", reveal=1),
            P("Muốn bền hơn: chia khung thành khối rồi so thống kê từng khối, lọc thông thấp trước, hoặc so histogram thay vì so từng pixel.", reveal=1),
        ], histogram={"bars": [{"label": str(i + 1), "value": v, **({"marks": [{"step": 1, "style": "warn"}]} if v > 20 else {})}
                               for i, v in enumerate([3, 4, 2, 5, 3, 38, 4, 3, 5, 2])],
                      "caption": "Khác biệt giữa các khung liên tiếp (minh họa)"}),
        S("Cách làm", "Phát hiện thay đổi không gian–thời gian", [
            P("Tách mỗi khung thành vùng thay đổi, tức tiền cảnh, và vùng không đổi, tức hậu cảnh, bằng cách ngưỡng hóa ảnh sai khác khung.",
              "Ngưỡng hóa frame difference → tiền cảnh / hậu cảnh"),
            P("Cải thiện bằng kim tự tháp Gauss đa độ phân giải, xử lý từ độ phân giải thấp nhất trở lên.", "Kim tự tháp Gauss"),
            P("Và tích hợp thời gian: thêm trí nhớ để vùng thay đổi liên tục qua các khung.", "Tích hợp thời gian"),
        ]),
        S("Cách làm", "Phân đoạn chuyển động và thống kê vùng", [
            P("Phân đoạn chuyển động gán nhãn pixel theo những phần chuyển động độc lập. Khi camera di chuyển, ước lượng chuyển động trội của cả khung trước.",
              "Ước lượng chuyển động trội"),
            P("Đăng ký hai ảnh theo chuyển động trội, tìm vùng không khớp, rồi lặp với mô hình bậc cao hơn như affine hay phối cảnh.",
              "Đăng ký ảnh → vùng không khớp → affine, phối cảnh"),
            P("Phương pháp thống kê mô tả vùng bằng bốn nhóm: thống kê Gauss, Fourier, hiệp phương sai và nhãn. Ứng dụng gồm phân đoạn xe, ảnh chụp trên không và phục vụ nén ảnh.",
              "Thống kê: Gauss, Fourier, hiệp phương sai, nhãn"),
        ]),
        S("So sánh", "Ba bài toán phân đoạn video", [
            P("Phát hiện chuyển cảnh chia theo thời gian: tìm thời điểm đổi cảnh."),
            P("Phát hiện thay đổi không gian thời gian chia mỗi khung thành tiền cảnh và hậu cảnh."),
            P("Phân đoạn chuyển động tách những vật chuyển động độc lập, kể cả khi camera cũng di chuyển."),
        ], table={"headers": ["Bài toán", "Chia theo", "Kết quả"],
                  "rows": [["Chuyển cảnh", "Thời gian (1 chiều)", "Thời điểm đổi cảnh"], ["Không gian–thời gian", "Pixel trong khung", "Tiền cảnh / hậu cảnh"],
                           ["Chuyển động", "Chuyển động độc lập", "Nhãn theo từng vật chuyển động"]]}),
        S("Ứng dụng", "Phân đoạn video ở đâu", [
            P("Tóm tắt và lập chỉ mục video, mã hóa video tiên tiến, biên tập và sản xuất video, cải thiện ước lượng luồng quang học, ước lượng cấu trúc ba chiều.",
              "Tóm tắt, mã hóa, biên tập, luồng quang, 3D"),
        ]),
        limit("Tìm thấy vùng, nhưng chưa bám theo", [
            P("Phân đoạn video cho biết vùng nào chuyển động ở mỗi khung, nhưng chưa nói chiếc xe ở khung này là chiếc xe nào ở khung sau.",
              "Chưa nối vật qua các khung"),
            P("Và kết quả tự động chưa chắc có ý nghĩa ngữ nghĩa. Video sau: theo dõi đối tượng và học sâu.", "→ Theo dõi & học sâu"),
        ], CHAIN, 7),
        traps([["Phát hiện chuyển cảnh là phân đoạn mấy chiều?", "Một chiều, theo thời gian"],
               ["Làm chuyển cảnh bền hơn bằng cách nào?", "So khối, lọc thông thấp, so histogram"],
               ["Kết quả tự động có luôn mang nghĩa?", "Không: vùng có nghĩa có thể nhiều màu, nhiều chuyển động"]],
              ["Bẫy một: phát hiện chuyển cảnh là phân đoạn một chiều theo trục thời gian.",
               "Bẫy hai: muốn bền hơn thì so theo khối, lọc thông thấp trước, hoặc so histogram thay vì so từng pixel.",
               "Bẫy ba: không gì đảm bảo kết quả phân đoạn tự động có ý nghĩa ngữ nghĩa."]),
    ]),

    story("theo-doi-hoc-sau", "Theo dõi đối tượng và phân đoạn bằng học sâu", "extra", [
        S("Vấn đề", "Chiếc xe này ở khung sau đi đâu?", [
            P("Để đo tốc độ một chiếc xe, ta phải bám theo đúng chiếc xe đó qua từng khung hình.", "Bám theo một vật qua các khung"),
            P("Và để biết vùng nào là xe, vùng nào là người, máy cần hiểu nghĩa của vùng, không chỉ màu hay chuyển động.", "Cần hiểu nghĩa của vùng"),
        ]),
        S("Ý tưởng", "Dự đoán rồi sửa", [
            P("Theo dõi theo Bayes giống đoán vị trí một chiếc xe trong sương mù: dựa vào vị trí và vận tốc trước để dự đoán, rồi khi nhìn thấy lờ mờ thì sửa lại.",
              "Như đoán vị trí xe trong sương mù"),
        ]),
        S("Cách làm", "Theo dõi theo Bayes", [
            P("Hậu nghiệm ở bước k trừ một là hiểu biết hiện tại về trạng thái vật.", "Trạng thái bước k−1", reveal=1),
            P("Lan truyền tiến theo thời gian bằng mô hình hệ thống để dự đoán.", "Dự đoán bằng mô hình hệ thống", reveal=2),
            P("Mô hình đo lường liên kết phép đo có nhiễu với vector trạng thái.", "Phép đo có nhiễu", reveal=3),
            P("Rồi dùng định lý Bayes để tính hậu nghiệm mới ở bước k.", "Cập nhật bằng định lý Bayes", reveal=4),
        ], graph=pipeline(["Trạng thái k−1", "Dự đoán (mô hình hệ thống)", "Đo (có nhiễu)", "Cập nhật Bayes", "Trạng thái k"], [1, 2, 3, 4, 4])),
        S("Cách làm", "Theo dõi 2D, 3D và mạng nơ-ron", [
            P("Theo dõi vật cứng hai chiều có bốn hướng: dựa trên vùng, đường biên, đặc trưng, hoặc mẫu.", "2D: vùng, đường biên, đặc trưng, mẫu"),
            P("Theo dõi ba chiều ước lượng sáu tham số: ba cho vị trí tâm, ba cho hướng. Ứng dụng chính là ước lượng tư thế đầu người, coi đầu như vật cứng.",
              "3D: 6 tham số, tư thế đầu người"),
            P("Phương pháp nơ-ron cổ điển gồm mạng truyền thẳng một lớp ẩn, mạng RBFN, và mạng SAWTA dùng bộ lọc Gabor cho ảnh có kết cấu.",
              "Mạng truyền thẳng, RBFN, SAWTA (Gabor)"),
        ]),
        S("Cách làm", "Phân đoạn bằng học sâu", [
            P("Phân đoạn ngữ nghĩa gán nhãn lớp cho mỗi pixel, chia theo mức giám sát: đầy đủ, bán giám sát, yếu, và không giám sát.",
              "Semantic: chia theo mức giám sát"),
            P("Phân đoạn thực thể tách riêng từng đối tượng, chia theo kiến trúc đa giai đoạn hay đơn giai đoạn. Mask R-CNN là đại diện tiêu biểu.",
              "Instance: đa / đơn giai đoạn, Mask R-CNN"),
            P("Các backbone tiêu biểu là VGG mười sáu và ResNet năm mươi.", "Backbone: VGG16, ResNet50"),
        ]),
        traps([["Theo dõi 3D ước lượng mấy tham số?", "6: vị trí tâm (3) + hướng (3)"],
               ["Bayes tracking gồm những mô hình nào?", "Mô hình hệ thống và mô hình đo lường"],
               ["Semantic và instance khác gì?", "Semantic: nhãn lớp mỗi pixel; instance: tách từng đối tượng"]],
              ["Bẫy một: theo dõi ba chiều có sáu tham số, ba vị trí và ba hướng.",
               "Bẫy hai: theo dõi Bayes dùng mô hình hệ thống để dự đoán và mô hình đo lường để liên kết phép đo với trạng thái.",
               "Bẫy ba: phân đoạn ngữ nghĩa gán lớp cho pixel, phân đoạn thực thể tách riêng từng đối tượng, ví dụ Mask R-CNN."]),
    ]),

    story("tong-ket", "Tổng kết chương 9", "summary", [
        S("Tổng kết", "Từ pixel đến vật thể", [
            P("Nhìn lại cả chương với camera ngã tư. K-means gom pixel theo màu, SLIC thêm vị trí để tạo mảnh nhỏ gọn và nhanh."),
            P("Cắt đồ thị xét từng cặp pixel, Normalized Cut chuẩn hóa để tránh vùng quá nhỏ."),
            P("Ảnh sai khác dùng chuyển động, phân đoạn video làm việc trên cả đoạn phim, và theo dõi cùng học sâu bám theo, hiểu nghĩa từng vật."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Tổng kết", "Bảng so sánh nhanh", [
            P("K-means và SLIC so pixel với tâm cụm; SLIC nhanh nhờ chỉ tìm trong vùng hai s nhân hai s.", reveal=[1, 2]),
            P("Cắt đồ thị và Ncut nhìn từng cặp pixel, cho kết quả tốt nhưng chậm hơn.", reveal=[3, 4]),
            P("Ảnh sai khác dùng thời gian để tách vật chuyển động, nhưng nhạy nhiễu.", reveal=[5]),
        ], table={"headers": ["Phương pháp", "Nhìn vào", "Điểm mạnh", "Điểm yếu"],
                  "rows": [["K-means", "Màu", "Đơn giản, k lớp", "Bỏ qua vị trí, phụ thuộc khởi tạo"],
                           ["SLIC", "Màu + vị trí", "Nhanh (2s × 2s)", "Mảnh nhỏ, chưa phải vật"],
                           ["Min cut", "Từng cặp pixel", "Tốt hơn", "Thích cắt nút lẻ"],
                           ["Ncut", "Từng cặp, chuẩn hóa", "Tránh vùng quá nhỏ", "Phức tạp, chậm"],
                           ["Ảnh sai khác", "Thay đổi theo thời gian", "Tách vật chuyển động", "Nhạy nhiễu"]]}),
        S("Bẫy thi", "Năm bẫy chung của chương", [
            P("Một: hai đặc tính nền tảng là gián đoạn, dẫn tới dựa trên biên, và tương đồng, dẫn tới dựa trên vùng."),
            P("Hai: vector của SLIC có năm chiều."),
            P("Ba: SLIC chỉ tìm trong vùng hai s nhân hai s."),
            P("Bốn: c lớn làm siêu điểm ảnh gọn hơn."),
            P("Năm: cắt đồ thị dùng vector riêng của trị riêng nhỏ thứ hai."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Hai đặc tính nền tảng?", "Gián đoạn (biên) và tương đồng (vùng)"], ["SLIC mấy chiều?", "5"],
                           ["SLIC tìm ở đâu?", "2s × 2s quanh tâm"], ["c lớn?", "Gọn hơn"], ["Vector riêng nào?", "Trị riêng nhỏ thứ hai"]]}),
        S("Tổng kết", "Sang chương 10", [
            P("Khi đã có các vùng, câu hỏi tiếp theo là mô tả mỗi vùng bằng những con số nào để máy nhận ra nó. Đó là trích xuất đặc trưng, chương mười.",
              "Chương 10: mô tả vùng bằng đặc trưng"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–4, 58", "Camera ngã tư: hàng trăm nghìn pixel", "—", "Phân đoạn: gián đoạn (biên) và tương đồng (vùng)", "→ K-means"],
    ["K-means", "9–10", "Ảnh có nhiều hơn 2 vùng", "Ngưỡng/Otsu: 2 lớp, chỉ mức xám", "Gán về tâm gần nhất ↔ dời tâm", "Bỏ qua vị trí, quét cả ảnh → SLIC"],
    ["SLIC", "11–13", "Quá nhiều pixel, chi tiết vụn", "K-means rải rác, chậm", "K-means 5 chiều, vùng tìm 2s×2s, trọng số c", "Mảnh nhỏ, chưa xét cặp pixel → cắt đồ thị"],
    ["Cắt đồ thị", "14–22", "Ranh giới giữa xe và đường", "So pixel với tâm", "Nút = pixel, w = độ giống, cắt dây mảnh; nguồn/đích", "Thích cắt nút lẻ → Ncut"],
    ["Normalized Cut", "20–23", "Nhát rẻ nhất vô nghĩa", "Chi phí tuyệt đối", "Chia cho tổng nối; trị riêng nhỏ thứ hai", "Ảnh tĩnh không thấy chuyển động → ảnh sai khác"],
    ["Ảnh sai khác", "24–29", "Xe xám trên đường xám", "Chỉ nhìn một ảnh", "So hai khung; ADI; Fourier → vận tốc", "Camera rung, ánh sáng đổi → video"],
    ["Phân đoạn video", "30–45", "Video dài: đổi cảnh, vùng chuyển động", "Ảnh sai khác thô", "Chuyển cảnh, thay đổi không gian–thời gian, phân đoạn chuyển động, thống kê", "Chưa bám vật qua khung → theo dõi"],
    ["Theo dõi & học sâu", "46–57", "Bám một vật, hiểu nghĩa vùng", "—", "Bayes: dự đoán rồi sửa; Mask R-CNN", "→ Tổng kết"],
    ["Tổng kết", "58", "—", "—", "Bảng so sánh, bẫy chung", "→ Chương 10"],
]
write(9, "Phân đoạn ảnh", EX, stories, MAP)
