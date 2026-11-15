import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, story, traps, write  # noqa: E402

CHAIN = ["Shape number", "Fourier descriptors", "Đặc trưng vùng", "Moment bất biến", "Kết cấu", "Đặc trưng toàn ảnh", "Đặc trưng học được"]
EX = "Băng chuyền trong xưởng cơ khí: nhận ra cờ lê, ốc vít, vòng đệm dù chúng nằm ở đâu, xoay góc nào"


def chain_code_graph():
    pts = {"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (2, 1), "e": (1, 1), "f": (0, 1)}
    path = [("a", "b", "0"), ("b", "c", "0"), ("c", "d", "3"), ("d", "e", "2"), ("e", "f", "2"), ("f", "a", "1")]
    nodes = [{"id": k, "label": "bắt đầu" if k == "a" else "", "x": x * 3, "y": y * 3, "shape": "dot"}
             for k, (x, y) in pts.items()]
    edges = [{"a": a, "b": b, "label": code, "step": n + 1} for n, (a, b, code) in enumerate(path)]
    return {"nodes": nodes, "edges": edges, "arrows": True, "caption": "Freeman 4 hướng: 0 phải · 1 lên · 2 trái · 3 xuống"}


def hist(values, labels, caption=None):
    data = {"bars": [{"label": lab, "value": v} for lab, v in zip(labels, values)]}
    if caption:
        data["caption"] = caption
    return data


stories = [
    intro("mo-dau", "Mở đầu: mô tả một vật bằng vài con số", "Cờ lê nằm đâu, xoay góc nào cũng phải nhận ra", [
        P("Chào các bạn. Chương mười là trích xuất đặc trưng. Ví dụ của cả chương: một băng chuyền trong xưởng cơ khí. "
          "Camera phải nhận ra cờ lê, ốc vít, vòng đệm, dù chúng nằm ở đâu, xoay góc nào, gần hay xa.", "Ví dụ: băng chuyền cơ khí"),
        P("Chương chín đã tách được từng vùng. Giờ phải mô tả mỗi vùng bằng vài con số cô đọng để bộ phân loại ở chương mười hai dùng.",
          "Mô tả vùng bằng vài con số"),
        P("Khi tả một người bạn, các bạn nói cao, tóc xoăn, đeo kính, chứ không nói bạn ấy đang đứng ở góc phòng. "
          "Đặc trưng tốt cũng vậy: không đổi khi vật dời chỗ, xoay, hay co giãn. Đó là tính bất biến.", "Đặc trưng tốt = bất biến"),
    ], CHAIN, [
        P("Ta đi từ đường biên: shape number, rồi Fourier descriptors.", "Đường biên: shape number → Fourier"),
        P("Rồi cả vùng: độ compact, moment bất biến, kết cấu bề mặt. Sau đó là đặc trưng toàn ảnh như góc và vùng ổn định, và cuối cùng là đặc trưng do mạng tự học.",
          "Vùng → kết cấu → toàn ảnh → học được"),
        P("Với mỗi đặc trưng, hãy tự hỏi: nó bất biến với phép biến đổi nào? Đề thi hỏi đúng câu đó.", "Câu hỏi xuyên suốt: bất biến với gì?"),
    ]),

    story("shape-number", "Đường biên và shape number", "method", [
        S("Vấn đề", "Mô tả hình dạng đường viền", [
            P("Cờ lê và vòng đệm có đường viền rất khác nhau. Ta muốn một mô tả đường viền không đổi khi vật xoay hay khi ta bắt đầu đi từ điểm khác.",
              "Mô tả viền, không đổi khi xoay"),
        ]),
        S("Cách cũ", "Độ dài, đường kính, độ cong", [
            P("Mô tả đơn giản nhất: độ dài biên xấp xỉ bằng số pixel dọc biên. Đường kính là khoảng cách lớn nhất giữa hai điểm trên biên.", "Độ dài, đường kính"),
            P("Đoạn nối hai điểm xa nhất là trục chính; trục phụ vuông góc với nó. Độ cong đo qua mã chuỗi độ dốc, tổng trị tuyệt đối của chuỗi đo độ ngoằn ngoèo.",
              "Trục chính, trục phụ, độ cong"),
            P("Chỗ hụt: vài con số đó không ghi lại được hình dạng cụ thể của đường viền.", "Chưa tả được hình dạng"),
        ]),
        S("Ý tưởng", "Ghi lại hướng đi quanh biên", [
            P("Đi một vòng quanh biên và ghi lại hướng của từng bước, như ghi đường đi: phải, phải, xuống, trái, trái, lên. Đó là mã chuỗi Freeman bốn hướng.",
              "Ghi hướng từng bước: mã chuỗi"),
            P("Nhưng xoay vật thì mọi hướng đổi. Nên ta ghi số lần rẽ, không ghi hướng tuyệt đối. Rẽ thì vẫn là rẽ, dù vật quay về phía nào.",
              "Ghi số lần rẽ, không ghi hướng"),
        ]),
        S("Cách làm", "Mã chuỗi của một hình chữ nhật", [
            P("Hình chữ nhật trong slide. Bắt đầu ở góc trên trái, đi sang phải: mã không.", reveal=1),
            P("Sang phải tiếp: không.", reveal=2),
            P("Đi xuống: ba.", reveal=3),
            P("Sang trái hai bước: hai, hai.", reveal=5),
            P("Đi lên về điểm đầu: một. Mã chuỗi là không, không, ba, hai, hai, một.", reveal=6),
        ], graph=chain_code_graph()),
        S("Cách làm", "Từ mã chuỗi đến shape number", [
            P("Bước một, mã chuỗi: không không ba hai hai một. Xoay hình chín mươi độ thì mọi số đều đổi.", reveal=1),
            P("Bước hai, hiệu sai bậc một: với mỗi bước, đếm số lần quay ngược chiều kim đồng hồ chín mươi độ từ hướng trước sang hướng này, phần tử đầu so với phần tử cuối. "
              "Được ba không ba ba không ba.", reveal=2),
            P("Thử đoán: dãy này còn phụ thuộc vào điều gì?", reveal=2, ask=True),
            P("Còn phụ thuộc điểm bắt đầu. Bước ba: xoay vòng dãy và chọn cách viết nhỏ nhất, được không ba ba không ba ba. Đó là shape number, bậc của hình là sáu.", reveal=3),
        ], table={"headers": ["Bước", "Dãy số", "Bất biến với"],
                  "rows": [["Mã chuỗi 4 hướng", "0 0 3 2 2 1", "—"], ["Hiệu sai bậc một", "3 0 3 3 0 3", "Xoay bội 90°"],
                           ["Shape number (xoay vòng nhỏ nhất)", "0 3 3 0 3 3", "+ điểm bắt đầu"]]}),
        S("So sánh", "Shape number so với độ dài, đường kính", [
            P("Độ dài và đường kính chỉ là vài con số tổng quát."),
            P("Shape number mô tả cả dáng đường viền, và bất biến với điểm bắt đầu và phép xoay bội chín mươi độ."),
        ], table={"headers": ["", "Độ dài / đường kính", "Shape number"],
                  "rows": [["Mô tả", "Kích thước tổng quát", "Dáng đường viền"], ["Bất biến xoay", "Có", "Chỉ bội 90°"]]}),
        S("Ứng dụng", "Mã chuỗi ở đâu", [
            P("Mã chuỗi được dùng để lưu và so khớp đường viền gọn nhẹ, ví dụ nhận dạng ký tự hay đối chiếu biên dạng chi tiết máy.", "Ký tự, biên dạng chi tiết"),
        ]),
        limit("Chỉ bất biến với góc vuông", [
            P("Shape number chỉ bất biến với phép xoay bội chín mươi độ, và nhạy với nhiễu trên biên. Chiếc cờ lê xoay ba mươi độ thì sao?",
              "Chỉ bội 90°, nhạy nhiễu"),
            P("Video sau biến đường biên thành tín hiệu và nhìn nó qua biến đổi Fourier.", "→ Fourier descriptors"),
        ], CHAIN, 2),
        traps([["Shape number dựa trên mã chuỗi mấy hướng?", "4 hướng (Freeman)"], ["Shape number là gì?", "Hiệu sai bậc một có độ lớn nhỏ nhất"],
               ["Bậc của shape number?", "Số chữ số"]],
              ["Bẫy một: shape number dùng mã chuỗi Freeman bốn hướng.",
               "Bẫy hai: định nghĩa là hiệu sai bậc một có độ lớn nhỏ nhất, gói cả bước hiệu sai và bước xoay vòng.",
               "Bẫy ba: bậc của hình là số chữ số của shape number."]),
    ]),

    story("fourier", "Fourier descriptors", "method", [
        S("Vấn đề", "Cờ lê xoay một góc bất kỳ", [
            P("Trên băng chuyền, cờ lê nằm nghiêng ba mươi độ, ở xa hơn, lệch sang trái. Mô tả đường viền vẫn phải nhận ra nó.", "Xoay bất kỳ, co giãn, tịnh tiến"),
        ]),
        S("Cách cũ", "Shape number", [
            P("Shape number chỉ chịu được phép xoay bội chín mươi độ.", "Chỉ bội 90°"),
        ]),
        S("Ý tưởng", "Biến đường biên thành tín hiệu", [
            P("Mẹo: mỗi điểm biên có hai tọa độ, gộp thành một số phức, hoành độ là phần thực, tung độ là phần ảo. Đường biên thành một dãy số một chiều.",
              "s(k) = x(k) + j·y(k)"),
            P("Lấy biến đổi Fourier của dãy đó. Vài hệ số tần số thấp mô tả dáng tổng thể, hệ số cao mô tả góc nhọn và chi tiết nhỏ.", "Tần số thấp = dáng · cao = chi tiết"),
        ]),
        S("Công thức", "Hệ số Fourier của đường biên", [
            P("Công thức chỉ nói: đem đường biên so với từng sóng tần số u, xem biên chứa bao nhiêu phần sóng đó. Các hệ số a của u là Fourier descriptors.",
              "a(u): biên chứa bao nhiêu sóng tần số u"),
            P("Giữ vài hệ số đầu rồi biến đổi ngược, ta được hình đã bo tròn. Thêm hệ số thì chi tiết hiện dần.", "Giữ ít hệ số → hình bo tròn"),
        ], formula=r"a(u) = \sum_{k=0}^{K-1} \underbrace{s(k)}_{x(k) + j\,y(k)} \; \underbrace{e^{-j 2\pi u k / K}}_{\text{sóng tần số } u}"),
        S("Cách làm", "Hình vuông bốn điểm", [
            P("Hình vuông đơn vị: bốn điểm là không, một, một cộng j, và j. Hệ số a không bằng hai cộng hai j, chia bốn ra trọng tâm. a một bằng âm hai trừ hai j, hai hệ số còn lại bằng không.",
              reveal=1),
            P("Thử đoán: dời hình sang phải ba đơn vị thì hệ số nào thay đổi?", reveal=1, ask=True),
            P("Chỉ a không, thành mười bốn cộng hai j. Muốn bất biến với tịnh tiến thì bỏ a không.", reveal=2),
            P("Phóng to gấp đôi, mọi hệ số nhân hai. Muốn bất biến với co giãn thì chia cho độ lớn của a một. Xoay hay đổi điểm bắt đầu chỉ đổi pha, nên dùng độ lớn là bất biến.",
              reveal=3),
        ], table={"headers": ["Trường hợp", "a(0)", "a(1)", "a(2), a(3)"],
                  "rows": [["Gốc: (0,0) (1,0) (1,1) (0,1)", "2 + 2j", "−2 − 2j", "0"], ["Tịnh tiến sang phải 3", "14 + 2j", "−2 − 2j", "0"],
                           ["Phóng to gấp 2", "4 + 4j", "−4 − 4j", "0"]]}),
        S("So sánh", "Chuẩn hóa Fourier descriptors", [
            P("Tịnh tiến chỉ ảnh hưởng a không: bỏ a không."),
            P("Xoay và đổi điểm bắt đầu chỉ đổi pha: dùng độ lớn."),
            P("Co giãn nhân mọi hệ số: chia cho độ lớn a một."),
        ], table={"headers": ["Phép biến đổi", "Ảnh hưởng", "Chuẩn hóa"],
                  "rows": [["Tịnh tiến", "Chỉ a(0)", "Bỏ a(0)"], ["Xoay, điểm bắt đầu", "Chỉ đổi pha", "Dùng |a(u)|"], ["Co giãn", "Nhân mọi hệ số", "Chia cho |a(1)|"]]}),
        S("Ứng dụng", "Fourier descriptors ở đâu", [
            P("Fourier descriptors được dùng để so khớp hình dạng, nhận dạng dáng vật thể, lá cây, chữ viết, vì vài hệ số đầu đã tóm tắt được dáng tổng thể.",
              "So khớp hình dạng"),
        ]),
        limit("Chỉ nhìn đường viền", [
            P("Fourier descriptors chỉ nhìn đường viền. Vòng đệm có lỗ ở giữa, cờ lê thì đặc. Phần bên trong vùng bị bỏ qua.", "Bỏ qua bên trong vùng"),
            P("Video sau mô tả cả vùng.", "→ Đặc trưng vùng"),
        ], CHAIN, 3),
        traps([["Tịnh tiến ảnh hưởng hệ số nào?", "Chỉ a(0)"], ["Muốn bất biến co giãn?", "Chia cho |a(1)|"], ["Điểm biên biểu diễn thế nào?", "Số phức x + jy"]],
              ["Bẫy một: tịnh tiến chỉ làm đổi hệ số a không.",
               "Bẫy hai: chia cho độ lớn a một để bất biến với co giãn; dùng độ lớn để bất biến với xoay và điểm bắt đầu.",
               "Bẫy ba: mỗi điểm biên là một số phức, hoành độ phần thực, tung độ phần ảo."]),
    ]),

    story("dac-trung-vung", "Đặc trưng vùng: compactness và độ lệch tâm", "method", [
        S("Vấn đề", "Mô tả cả vùng, không chỉ viền", [
            P("Ta muốn một con số nói nhanh vùng tròn trịa hay dài dẹt, để tách vòng đệm tròn khỏi chiếc cờ lê dài.", "Tròn hay dài?"),
        ]),
        S("Cách cũ", "Diện tích và chu vi riêng lẻ", [
            P("Diện tích là số pixel trong vùng, chu vi là độ dài biên. Nhưng chụp gần thì cả hai đều tăng, nên riêng lẻ chúng ít ý nghĩa.",
              "Diện tích, chu vi đổi theo khoảng cách"),
        ]),
        S("Ý tưởng", "Ghép thành tỉ số", [
            P("Ghép hai số lại để bỏ ảnh hưởng của kích thước: độ compact là chu vi bình phương chia diện tích.", "Compactness = p² / A"),
            P("Phóng hình to gấp đôi, chu vi bình phương tăng bốn lần, diện tích cũng tăng bốn lần, nên tỉ số không đổi.", "Bất biến với co giãn"),
        ]),
        S("Cách làm", "Ba hình cùng diện tích", [
            P("Ba hình cùng diện tích mười sáu.", reveal=0),
            P("Hình tròn luôn có độ compact bằng bốn pi, khoảng mười hai phẩy năm bảy, bất kể bán kính. Đây là giá trị nhỏ nhất có thể.", reveal=0),
            P("Thử đoán: hình vuông bốn nhân bốn và hình chữ nhật tám nhân hai, hình nào compact lớn hơn?", reveal=0, ask=True),
            P("Hình vuông có chu vi mười sáu, compact bằng mười sáu. Hình chữ nhật có chu vi hai mươi, compact bằng hai mươi lăm. Càng dài, càng lồi lõm thì càng lớn.",
              reveal=0),
        ], histogram=hist([12.57, 16, 25], ["Tròn (4π)", "Vuông 4×4", "Chữ nhật 8×2"], "p² / A của ba hình cùng diện tích 16")),
        S("Cách làm", "Độ lệch tâm", [
            P("Độ lệch tâm đo vùng dẹt đến mức nào. Nó được định nghĩa qua một ellipse có cùng moment trung tâm bậc hai với vùng.", "Ellipse cùng moment bậc hai"),
            P("Tính từ trị riêng của ma trận hiệp phương sai các tọa độ. Hình tròn có độ lệch tâm bằng không, càng dài thì càng gần một.", "Tròn = 0 · càng dài → 1"),
        ]),
        S("So sánh", "Diện tích, chu vi và compactness", [
            P("Diện tích và chu vi riêng lẻ đổi theo kích thước.", reveal=[1]),
            P("Compactness và độ lệch tâm bất biến với tịnh tiến, xoay và co giãn.", reveal=[2, 3]),
        ], table={"headers": ["Đặc trưng", "Tịnh tiến", "Xoay", "Co giãn"],
                  "rows": [["Diện tích, chu vi", "✓", "✓", "✗"], ["Compactness p²/A", "✓", "✓", "✓"], ["Độ lệch tâm", "✓", "✓", "✓"]]}),
        S("Ứng dụng", "Đặc trưng vùng ở đâu", [
            P("Kiểm tra hạt, tế bào, viên thuốc trên dây chuyền: một con số compact là đủ để phát hiện viên méo hay vỡ.", "Phát hiện viên méo, hạt vỡ"),
        ]),
        limit("Một con số là quá ít", [
            P("Compactness chỉ là một con số. Nhiều hình khác nhau có thể cùng compact.", "Một con số: dễ trùng"),
            P("Cần một bộ số giàu hơn mà vẫn bất biến. Đó là moment bất biến.", "→ Moment bất biến"),
        ], CHAIN, 4),
        traps([["Compactness nhỏ nhất với hình nào?", "Hình tròn: 4π"], ["Độ lệch tâm tính từ đâu?", "Trị riêng ma trận hiệp phương sai"],
               ["Diện tích có bất biến co giãn?", "Không"]],
              ["Bẫy một: compactness nhỏ nhất với hình tròn, bằng bốn pi.",
               "Bẫy hai: độ lệch tâm định nghĩa qua ellipse cùng moment bậc hai, tính từ trị riêng ma trận hiệp phương sai.",
               "Bẫy ba: diện tích và chu vi riêng lẻ không bất biến với co giãn."]),
    ]),

    story("moment", "Moment và moment bất biến", "method", [
        S("Vấn đề", "Một bộ số giàu thông tin mà vẫn bất biến", [
            P("Ta cần nhiều con số mô tả hình dạng vùng, và tất cả không đổi khi vật dời, xoay, co giãn.", "Nhiều số, đều bất biến"),
        ]),
        S("Cách cũ", "Compactness", [
            P("Compactness chỉ là một con số, nhiều hình khác nhau dễ trùng giá trị.", "Một số, dễ trùng"),
        ]),
        S("Ý tưởng", "Đo vùng từ trọng tâm của nó", [
            P("Moment là tổng các pixel nhân với lũy thừa tọa độ. Moment bậc thấp rất quen: moment không không là diện tích, moment một không và không một chia diện tích cho ra trọng tâm.",
              "m00 = diện tích · m10, m01 → trọng tâm"),
            P("Đo tọa độ từ trọng tâm thay vì từ góc ảnh: vật dời đi đâu thì trọng tâm dời theo, nên con số không đổi.", "Đo từ trọng tâm → bất biến tịnh tiến"),
        ]),
        S("Công thức", "Moment và moment trung tâm", [
            P("Moment thường đo từ gốc ảnh. Moment trung tâm đo từ trọng tâm, nên bất biến với tịnh tiến.", "μ_pq: bất biến tịnh tiến"),
            P("Chia moment trung tâm cho lũy thừa thích hợp của diện tích, được moment trung tâm chuẩn hóa, thêm bất biến với co giãn.", "Chuẩn hóa: + bất biến co giãn"),
            P("Từ moment chuẩn hóa bậc hai và bậc ba suy ra bộ bảy moment bất biến: không đổi khi tịnh tiến, co giãn, xoay; phản chiếu gương thì chỉ sai một dấu.",
              "7 moment bất biến; gương: sai một dấu"),
        ], formula=r"m_{pq} = \sum_x \sum_y x^p y^q f(x,y) \qquad \mu_{pq} = \sum_x \sum_y \underbrace{(x-\bar{x})^p (y-\bar{y})^q}_{\text{đo từ trọng tâm}} f(x,y)"),
        S("Cách làm", "Moment của một vùng bốn pixel", [
            P("Vùng hình chữ T ngược gồm bốn pixel. Moment không không bằng bốn. Dời vùng năm ngang, ba dọc, vẫn là bốn.", reveal=1),
            P("Moment một không bằng tám, không một bằng năm. Sau khi dời thành hai mươi tám và mười bảy: moment thường không bất biến.", reveal=2),
            P("Trọng tâm hai và một phẩy hai lăm, sau khi dời cũng dời đúng năm và ba.", reveal=3),
            P("Thử đoán: moment trung tâm bậc hai có đổi sau khi dời không?", reveal=3, ask=True),
            P("Không đổi chút nào: hai và không phẩy bảy lăm ở cả hai cột. Ngang lớn hơn dọc cho biết vùng trải rộng theo chiều ngang.", reveal=4),
        ], table={"headers": ["Đại lượng", "Vùng gốc: (1,1) (2,1) (3,1) (2,2)", "Dời (+5, +3)"],
                  "rows": [["m00", "4", "4"], ["m10, m01", "8 và 5", "28 và 17"], ["Trọng tâm", "(2; 1,25)", "(7; 4,25)"], ["μ20, μ02", "2 và 0,75", "2 và 0,75"]]}),
        S("So sánh", "Ba loại moment", [
            P("Moment thường không bất biến.", reveal=[1]), P("Moment trung tâm bất biến với tịnh tiến; chuẩn hóa thì thêm co giãn.", reveal=[2, 3]),
            P("Bảy moment bất biến chịu được tịnh tiến, co giãn và xoay.", reveal=[4]),
        ], table={"headers": ["Loại", "Tịnh tiến", "Co giãn", "Xoay"],
                  "rows": [["m_pq", "✗", "✗", "✗"], ["μ_pq", "✓", "✗", "✗"], ["μ chuẩn hóa", "✓", "✓", "✗"], ["7 moment bất biến", "✓", "✓", "✓ (gương: sai dấu)"]]}),
        S("Ứng dụng", "Moment bất biến ở đâu", [
            P("Bảy moment bất biến là đặc trưng hình dạng kinh điển, dùng nhận dạng ký tự, chi tiết máy, vật thể đơn giản dù xoay hay co giãn.",
              "Nhận dạng ký tự, chi tiết máy"),
        ]),
        limit("Hình dạng không nói về bề mặt", [
            P("Một con ốc mạ bóng và một con ốc gỉ sét có cùng hình dạng, cùng moment. Thứ khác nhau là bề mặt.", "Cùng hình, khác bề mặt"),
            P("Video sau mô tả bề mặt: đặc trưng kết cấu.", "→ Kết cấu"),
        ], CHAIN, 5),
        traps([["Có bao nhiêu moment bất biến?", "7, từ moment chuẩn hóa bậc 2 và 3"], ["Moment trung tâm bất biến với gì?", "Tịnh tiến"],
               ["Phản chiếu gương?", "Moment bất biến chỉ sai một dấu"]],
              ["Bẫy một: có bảy moment bất biến, suy ra từ moment trung tâm chuẩn hóa bậc hai và bậc ba.",
               "Bẫy hai: moment trung tâm bất biến với tịnh tiến; cần chuẩn hóa mới bất biến với co giãn.",
               "Bẫy ba: với phản chiếu gương, moment bất biến chỉ sai một dấu."]),
    ]),

    story("ket-cau", "Đặc trưng kết cấu", "method", [
        S("Vấn đề", "Ốc bóng hay ốc gỉ?", [
            P("Hai con ốc cùng hình dạng, nhưng một con bề mặt bóng mịn, một con gỉ sét sần sùi. Cần đặc trưng đo độ mịn, độ thô, độ đều của bề mặt.",
              "Đo mịn, thô, đều"),
        ]),
        S("Cách cũ", "Đặc trưng hình dạng", [
            P("Shape number, Fourier hay moment bất biến chỉ tả đường viền và hình dạng, không nói gì về bề mặt bên trong.", "Chỉ tả hình dạng"),
        ]),
        S("Ý tưởng", "Thống kê cường độ trong vùng", [
            P("Bề mặt mịn thì các pixel có cường độ gần nhau, bề mặt thô thì chênh lệch nhiều. Nhìn phân bố cường độ là biết.", "Mịn: gần nhau · thô: chênh nhiều"),
        ]),
        S("Cách làm", "Moment của histogram", [
            P("Bề mặt mịn có histogram hẹp, bề mặt thô có histogram rộng.", reveal=1),
            P("Thử đoán: moment bậc mấy của histogram đo được sự khác biệt này?", reveal=1, ask=True),
            P("Moment bậc hai, tức phương sai, đo độ tương phản cường độ và dùng để mô tả độ mịn. Moment bậc ba đo độ lệch, bậc bốn đo độ phẳng.", reveal=2),
            P("Thêm độ đồng nhất, lớn khi vùng đều màu, và entropy trung bình, lớn khi vùng lộn xộn. Nhược điểm: histogram không biết pixel nằm ở đâu, sọc ngang và sọc dọc cho cùng kết quả.",
              reveal=2),
        ], compare={"left": {"label": "Bề mặt mịn: histogram hẹp", "histogram": hist([0, 2, 10, 30, 10, 2, 0], [str(v) for v in range(1, 8)]) | {"top": 30}},
                    "right": {"label": "Bề mặt thô: histogram rộng", "histogram": hist([7, 8, 8, 8, 8, 8, 7], [str(v) for v in range(1, 8)]) | {"top": 30}},
                    "arrow": "phương sai tăng"}),
        S("Cách làm", "Ma trận đồng hiện", [
            P("Ma trận đồng hiện đếm cặp pixel để biết vị trí. Chọn toán tử Q mô tả vị trí tương đối, ở đây là pixel ngay bên phải. Ảnh có ba mức xám.", reveal=1),
            P("Phần tử hàng i cột j đếm số lần pixel mức i có pixel mức j ngay bên phải. Cặp một rồi hai xuất hiện hai lần, nên ô hàng một cột hai bằng hai.", reveal=2),
            P("Tổng các phần tử là sáu, chia cho sáu ra xác suất từng cặp, rồi tính đặc trưng như độ tương quan. Đổi Q thành pixel bên dưới thì G khác, nên phân biệt được sọc ngang và sọc dọc.",
              reveal=2),
        ], grid=[{"label": "Ảnh f (3 mức xám)", "cells": [[1, 1, 2], [1, 2, 2], [3, 3, 1]], "accent": [[0, 1], [0, 2], [1, 0], [1, 1]]},
                 {"label": "G: hàng = pixel trái, cột = pixel phải", "cells": [[1, 2, 0], [0, 1, 0], [1, 0, 1]], "warn": [[0, 1]]}]),
        S("Cách làm", "Phương pháp phổ", [
            P("Với kết cấu lặp lại như vải dệt hay ren ốc, phổ Fourier rất hợp. Đỉnh nổi bật cho biết hướng chính của mẫu.", "Đỉnh phổ → hướng chính"),
            P("Vị trí đỉnh cho biết chu kỳ không gian cơ bản. Lọc bỏ thành phần tuần hoàn thì còn lại phần không tuần hoàn.", "Vị trí đỉnh → chu kỳ"),
            P("Viết phổ trong tọa độ cực: cố định góc để xem dọc một tia, cố định bán kính để xem quanh một vòng.", "Tọa độ cực S(r, θ)"),
        ]),
        S("So sánh", "Ba cách đo kết cấu", [
            P("Moment histogram đơn giản nhưng không biết vị trí pixel."), P("Ma trận đồng hiện biết vị trí tương đối qua Q."),
            P("Phương pháp phổ hợp với kết cấu tuần hoàn, cho hướng và chu kỳ."),
        ], table={"headers": ["Cách", "Đo gì", "Điểm yếu / lưu ý"],
                  "rows": [["Moment histogram", "Tương phản, độ lệch, độ phẳng", "Không biết vị trí pixel"],
                           ["Ma trận đồng hiện", "Tần suất cặp mức xám theo Q", "Phụ thuộc Q"], ["Phổ Fourier", "Hướng, chu kỳ", "Hợp kết cấu tuần hoàn"]]}),
        S("Ứng dụng", "Kết cấu ở đâu", [
            P("Kiểm tra bề mặt vải, gỗ, kim loại; phân loại đất trong ảnh vệ tinh; phân biệt mô lành và mô bệnh trong ảnh y tế.", "Kiểm tra bề mặt, ảnh vệ tinh, y tế"),
        ]),
        limit("Phải phân đoạn trước", [
            P("Mọi đặc trưng đến giờ đều cần tách vùng trước. Nếu phân đoạn sai, đặc trưng cũng sai.", "Cần phân đoạn trước"),
            P("Có những đặc trưng tìm thẳng trên toàn ảnh, không cần phân đoạn. Video sau.", "→ Đặc trưng toàn ảnh"),
        ], CHAIN, 6),
        traps([["Moment histogram bậc 2, 3, 4 đo gì?", "Tương phản, độ lệch, độ phẳng"], ["Co-occurrence cần xác định gì trước?", "Toán tử vị trí Q"],
               ["Phổ: vị trí đỉnh cho biết gì?", "Chu kỳ không gian cơ bản"]],
              ["Bẫy một: moment histogram bậc hai đo tương phản, bậc ba đo độ lệch, bậc bốn đo độ phẳng.",
               "Bẫy hai: ma trận đồng hiện phụ thuộc toán tử vị trí Q.",
               "Bẫy ba: đỉnh phổ cho hướng chính, vị trí đỉnh cho chu kỳ không gian cơ bản."]),
    ]),

    story("toan-anh", "PCA và đặc trưng toàn ảnh", "method", [
        S("Vấn đề", "Tìm điểm mốc mà không cần phân đoạn", [
            P("Muốn ghép hai ảnh băng chuyền chụp lệch nhau, hay đối chiếu một chi tiết với ảnh mẫu, ta cần những điểm mốc nổi bật tìm được trên toàn ảnh.",
              "Điểm mốc trên toàn ảnh"),
            P("Và với ảnh nhiều băng phổ, cần cách giảm số chiều dữ liệu.", "Giảm chiều ảnh nhiều băng"),
        ]),
        S("Cách cũ", "Đặc trưng vùng cần phân đoạn", [
            P("Đặc trưng biên, vùng, kết cấu đều mô tả một vùng đã tách sẵn. Phân đoạn sai thì đặc trưng hỏng theo.", "Phụ thuộc phân đoạn"),
        ]),
        S("Ý tưởng", "Tìm chỗ đặc biệt ngay trên ảnh", [
            P("Góc là chỗ đặc biệt nhất: dịch một cửa sổ nhỏ theo hướng nào cũng thấy thay đổi mạnh. Vùng ổn định là vùng giữ nguyên qua nhiều mức ngưỡng.",
              "Góc: đổi mạnh mọi hướng · vùng ổn định qua ngưỡng"),
        ]),
        S("Cách làm", "Bộ dò góc Harris–Stephens", [
            P("Trượt một cửa sổ nhỏ. Ở vùng phẳng, dịch hướng nào cũng không đổi.", reveal=1),
            P("Ở cạnh, chỉ đổi khi dịch vuông góc với cạnh.", reveal=2),
            P("Thử đoán: ở góc thì sao?", reveal=2, ask=True),
            P("Ở góc, dịch hướng nào cũng đổi mạnh. Đó là dấu hiệu Harris dùng để tìm góc.", reveal=3),
        ], table={"headers": ["Vị trí cửa sổ", "Dịch theo mọi hướng", "Kết luận"],
                  "rows": [["Vùng phẳng", "Không đổi", "Không phải đặc trưng"], ["Cạnh", "Chỉ đổi khi dịch vuông góc cạnh", "Cạnh"],
                           ["Góc", "Đổi mạnh mọi hướng", "Góc ✓"]]}),
        S("Cách làm", "MSER và PCA", [
            P("MSER, vùng cực trị ổn định cực đại, là những vùng gần như không đổi khi thay ngưỡng qua nhiều mức, nên rất bền cho đối sánh ảnh.",
              "MSER: ổn định qua nhiều ngưỡng"),
            P("PCA: với n ảnh đã đăng ký khớp nhau, như các băng phổ, mỗi vị trí cho một vector n chiều. Tính trung bình, ma trận hiệp phương sai, vector riêng.",
              "PCA: vector n chiều mỗi vị trí"),
            P("Xếp vector riêng thành ma trận biến đổi A để chiếu sang không gian thành phần chính. Vài thành phần đầu giữ gần hết phương sai: giảm chiều.",
              "Ma trận A từ vector riêng → giảm chiều"),
        ]),
        S("So sánh", "Đặc trưng vùng so với toàn ảnh", [
            P("Đặc trưng vùng cần phân đoạn trước; Harris và MSER tìm thẳng trên ảnh.", reveal=[1, 2]), P("PCA giảm chiều cho dữ liệu nhiều băng, không phải để tìm điểm mốc.", reveal=[3]),
        ], table={"headers": ["Kỹ thuật", "Tìm gì", "Cần phân đoạn?"],
                  "rows": [["Harris–Stephens", "Góc", "Không"], ["MSER", "Vùng ổn định", "Không"], ["PCA", "Thành phần chính (giảm chiều)", "Không"]]}),
        S("Ứng dụng", "Đặc trưng toàn ảnh ở đâu", [
            P("Ghép ảnh toàn cảnh, đối sánh ảnh, theo dõi điểm qua video đều dựa vào các điểm mốc như góc. PCA dùng nhiều cho ảnh vệ tinh đa phổ.",
              "Ghép ảnh, đối sánh, ảnh vệ tinh"),
        ]),
        limit("Vẫn do con người thiết kế", [
            P("Từ shape number đến Harris, mọi đặc trưng đều do con người nghĩ ra công thức. Chọn sai đặc trưng thì bộ phân loại cũng bó tay.",
              "Đặc trưng thủ công"),
            P("Video sau: để mạng tự học đặc trưng.", "→ Đặc trưng học được"),
        ], CHAIN, 7),
        traps([["Harris phát hiện gì?", "Góc (đổi mạnh mọi hướng)"], ["MSER là gì?", "Vùng ổn định qua nhiều mức ngưỡng"],
               ["PCA dùng ma trận gì làm biến đổi?", "Ma trận các vector riêng của hiệp phương sai"]],
              ["Bẫy một: Harris Stephens là bộ dò góc.",
               "Bẫy hai: MSER là các vùng gần như không đổi qua nhiều mức ngưỡng.",
               "Bẫy ba: PCA dùng ma trận các vector riêng của ma trận hiệp phương sai làm ma trận biến đổi."]),
    ]),

    story("hoc-duoc", "Đặc trưng học được", "extra", [
        S("Vấn đề", "Không biết nên thiết kế đặc trưng nào", [
            P("Với hàng trăm loại dụng cụ, không ai biết trước đặc trưng thủ công nào là đủ.", "Đặc trưng nào là đủ?"),
        ]),
        S("Ý tưởng", "Để mạng tự học", [
            P("Các lớp tích chập của một mạng CNN đã huấn luyện sẵn như VGG mười sáu tự sinh ra bản đồ đặc trưng ở nhiều mức trừu tượng.",
              "CNN tự sinh bản đồ đặc trưng"),
        ]),
        S("Cách làm", "Từ cạnh đến bộ phận", [
            P("Lớp đầu học những thứ như cạnh và góc, gần giống các bộ lọc thủ công.", "Lớp đầu: cạnh, góc"),
            P("Lớp sâu hơn ghép chúng thành hình dạng, rồi thành bộ phận của vật thể.", "Lớp sâu: hình dạng, bộ phận"),
            P("Đây là bước chuyển từ đặc trưng thủ công sang đặc trưng học được, nền tảng cho chương mười một và mười hai.", "Thủ công → học được"),
        ]),
        S("So sánh", "Thủ công so với học được", [
            P("Đặc trưng thủ công như shape number hay moment có công thức rõ ràng, dễ giải thích, cần ít dữ liệu, nhưng do con người chọn.", reveal=[1, 2]),
            P("Đặc trưng học được tự thích nghi với dữ liệu và thường mạnh hơn trên ảnh thật, đổi lại cần nhiều dữ liệu, tính toán, và khó giải thích hơn.", reveal=[3]),
        ], table={"headers": ["", "Thủ công", "Học được (CNN)"],
                  "rows": [["Ai thiết kế", "Con người", "Mạng tự học"], ["Giải thích", "Dễ, có công thức", "Khó hơn"],
                           ["Dữ liệu cần", "Ít", "Nhiều"]]}),
        S("Ứng dụng", "Đặc trưng học được ở đâu", [
            P("Các bộ phát hiện đối tượng ở chương mười một và bộ phân loại CNN ở chương mười hai đều dùng mạng như VGG hay ResNet làm phần trích đặc trưng, gọi là backbone.",
              "Backbone cho chương 11 và 12"),
        ]),
        traps([["Mạng nào được slide dùng làm ví dụ?", "VGG16"], ["Lớp đầu của CNN học gì?", "Đặc trưng cấp thấp: cạnh, góc"]],
              ["Bẫy một: slide dùng VGG mười sáu đã huấn luyện sẵn để trích đặc trưng.",
               "Bẫy hai: lớp đầu học đặc trưng cấp thấp như cạnh và góc, lớp sâu học bộ phận."]),
    ]),

    story("tong-ket", "Tổng kết chương 10", "summary", [
        S("Tổng kết", "Đặc trưng nào bất biến với cái gì", [
            P("Độ dài biên và diện tích không đổi khi dời hay xoay, nhưng đổi theo kích thước.", reveal=[1]),
            P("Shape number bất biến với điểm bắt đầu và xoay bội chín mươi độ. Fourier descriptors phải chuẩn hóa mới bất biến.", reveal=[2, 3]),
            P("Compactness và bảy moment bất biến chịu được cả tịnh tiến, xoay và co giãn.", reveal=[4, 5]),
        ], table={"headers": ["Đặc trưng", "Tịnh tiến", "Xoay", "Co giãn"],
                  "rows": [["Độ dài biên, diện tích", "✓", "✓", "✗"], ["Shape number", "✓", "✓ (bội 90°)", "—"],
                           ["Fourier descriptors", "bỏ a(0)", "dùng |a(u)|", "chia |a(1)|"], ["Compactness p²/A", "✓", "✓", "✓"], ["7 moment bất biến", "✓", "✓", "✓"]]}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: shape number dùng mã chuỗi bốn hướng."), P("Hai: tịnh tiến chỉ đổi a không."),
            P("Ba: moment histogram hai, ba, bốn đo tương phản, độ lệch, độ phẳng."), P("Bốn: có bảy moment bất biến."),
            P("Năm: ma trận đồng hiện phụ thuộc toán tử Q."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Shape number?", "Chain code 4 hướng, first difference nhỏ nhất"], ["Tịnh tiến đổi hệ số nào?", "a(0)"],
                           ["Moment histogram 2, 3, 4?", "Tương phản, độ lệch, độ phẳng"], ["Bao nhiêu moment bất biến?", "7"], ["Co-occurrence cần?", "Toán tử Q"]]}),
        S("Tổng kết", "Cả chương trong một mạch", [
            P("Ta đi từ đường viền với shape number và Fourier descriptors, sang cả vùng với compactness và moment bất biến, rồi bề mặt với kết cấu.",
              "Viền → vùng → bề mặt"),
            P("Sau đó là điểm mốc trên toàn ảnh với Harris, MSER, giảm chiều với PCA, và cuối cùng là đặc trưng do CNN tự học.", "Toàn ảnh → học được"),
        ]),
        S("Tổng kết", "Sang chương 11", [
            P("Có đặc trưng rồi, chương mười một dùng chúng để trả lời hai câu hỏi cùng lúc: trong ảnh có gì, và nó nằm ở đâu.", "Chương 11: phát hiện đối tượng"),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
    ]),
]

MAP = [
    ["Mở đầu", "1–3", "Băng chuyền: nhận ra dụng cụ dù xoay, co giãn", "—", "Đặc trưng tốt = bất biến", "→ Shape number"],
    ["Shape number", "4–6", "Mô tả viền, không đổi khi xoay", "Độ dài, đường kính, độ cong", "Mã chuỗi 4 hướng → hiệu sai → xoay vòng nhỏ nhất", "Chỉ bội 90° → Fourier"],
    ["Fourier descriptors", "7–9", "Xoay góc bất kỳ", "Shape number", "Biên = số phức → DFT; chuẩn hóa", "Bỏ qua bên trong → vùng"],
    ["Đặc trưng vùng", "11–13", "Tròn hay dài", "Diện tích, chu vi riêng lẻ", "p²/A; độ lệch tâm", "Một số dễ trùng → moment"],
    ["Moment bất biến", "21–23", "Bộ số giàu, bất biến", "Compactness", "Moment trung tâm, chuẩn hóa, 7 moment", "Không tả bề mặt → kết cấu"],
    ["Kết cấu", "14–20", "Ốc bóng hay gỉ", "Đặc trưng hình dạng", "Moment histogram, co-occurrence, phổ", "Cần phân đoạn → toàn ảnh"],
    ["Toàn ảnh", "24–28", "Điểm mốc không cần phân đoạn", "Đặc trưng vùng", "Harris, MSER, PCA", "Thủ công → học được"],
    ["Đặc trưng học được", "29–30", "Không biết thiết kế gì", "—", "CNN (VGG16) tự học", "→ Tổng kết"],
    ["Tổng kết", "—", "—", "—", "Bảng bất biến, bẫy chung", "→ Chương 11"],
]
write(10, "Trích xuất đặc trưng", EX, stories, MAP)
