import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, pipeline, story, traps, write  # noqa: E402

CHAIN = ["Sai khác khung", "Bù chuyển động", "Vòng lặp H.261", "MPEG-1 / MPEG-2", "MC-EZBC khả mở", "Chuyển mã"]
EX = "Phát trực tiếp một bản tin thời sự 352×288, 30 khung/giây qua đường truyền chỉ 1,5 Mbps"


def gop_graph():
    pos = {"I1": (0, 0, 1), "P4": (3, 0, 2), "B2": (1, 1.6, 3), "B3": (2, 1.6, 3), "P7": (6, 0, 4), "B5": (4, 1.6, 5), "B6": (5, 1.6, 5)}
    nodes = [{"id": k, "label": k.replace("1", "₁").replace("2", "₂").replace("3", "₃").replace("4", "₄").replace("5", "₅").replace("6", "₆").replace("7", "₇"),
              "x": x, "y": y, "shape": "box", "step": st,
              "marks": [{"step": st, "style": "accent" if k[0] == "I" else "warn"}] if k[0] in "IP" else []}
             for k, (x, y, st) in pos.items()]
    refs = [("I1", "P4", 2), ("I1", "B2", 3), ("P4", "B2", 3), ("I1", "B3", 3), ("P4", "B3", 3), ("P4", "P7", 4),
            ("P4", "B5", 5), ("P7", "B5", 5), ("P4", "B6", 5), ("P7", "B6", 5)]
    edges = [{"a": a, "b": b, "step": st} for a, b, st in refs]
    return {"nodes": nodes, "edges": edges, "arrows": True,
            "caption": "Hàng trên: khung I, P · hàng dưới: khung B · mũi tên: tham chiếu · thứ tự hiện ra = thứ tự mã hóa"}


stories = [
    intro("mo-dau", "Mở đầu: video lớn đến mức nào", "Bản tin thời sự qua đường truyền 1,5 Mbps", [
        P("Chào các bạn. Chương sáu là nén video. Ví dụ của cả chương: phát trực tiếp một bản tin thời sự, khung ba trăm năm mươi hai nhân hai trăm tám mươi tám, ba mươi khung mỗi giây.",
          "Ví dụ: bản tin thời sự 352×288, 30 khung/s"),
        P("Mỗi khung khoảng một trăm linh một nghìn pixel. Mỗi macroblock gồm một khối độ chói mười sáu nhân mười sáu và hai khối màu tám nhân tám, trung bình một phẩy năm byte mỗi pixel, tức khoảng một trăm năm mươi hai nghìn byte mỗi khung.",
          "≈ 152 064 byte mỗi khung"),
        P("Nhân tám bit, nhân ba mươi khung mỗi giây: khoảng ba mươi sáu phẩy năm megabit mỗi giây. Đường truyền chỉ một phẩy năm, nên phải nén khoảng hai mươi bốn lần.",
          "≈ 36,5 Mbps → cần nén ≈ 24 lần"),
        P("Thử nghĩ: nén không mất dữ liệu chỉ được hai đến ba lần. Video còn dư thừa ở đâu mà ảnh tĩnh không có?", "Dư thừa nào chỉ video mới có?", ask=True),
    ], CHAIN, [
        P("Câu trả lời là thời gian: các khung liên tiếp rất giống nhau. Ta đi từ gửi phần sai khác, đến bù chuyển động, rồi vòng lặp của bộ mã hóa H.261.",
          "Sai khác → bù chuyển động → H.261"),
        P("Sau đó là MPEG-1 với khung I, P, B, mã hóa khả mở MC-EZBC, và chuyển mã video.", "MPEG-1/2 → MC-EZBC → chuyển mã"),
        P("Mỗi bước vá chỗ hụt của bước trước, các bạn xem theo thứ tự.", "Xem theo thứ tự"),
    ]),

    story("sai-khac-khung", "Chỉ gửi những gì thay đổi", "method", [
        S("Vấn đề", "Phông nền đứng yên suốt mấy phút", [
            P("Trong bản tin, phông nền phía sau đứng yên suốt mấy phút, chỉ có khuôn mặt người dẫn cử động chút ít. Gửi lại toàn bộ phông nền ba mươi lần mỗi giây là lãng phí.",
              "Phông nền lặp lại 30 lần/giây"),
        ]),
        S("Cách cũ", "Nén từng khung như ảnh tĩnh", [
            P("Cách đầu tiên là nén mỗi khung như một ảnh JPEG riêng. Nhưng làm vậy chỉ khai thác dư thừa không gian bên trong mỗi khung.", "Mỗi khung một JPEG"),
            P("Tương quan thời gian giữa các khung liên tiếp hoàn toàn bị bỏ qua.", "Bỏ qua tương quan thời gian"),
        ]),
        S("Ý tưởng", "Bên nhận đã có khung trước", [
            P("Bên nhận đã có khung trước. Vậy chỉ cần gửi phần khác biệt giữa khung hiện tại và khung trước.", "Gửi phần khác biệt"),
            P("Phần khác biệt phần lớn là số không, nên nén rất tốt.", "Phần lớn là 0 → nén tốt"),
        ]),
        S("Cách làm", "Khung hiệu", [
            P("Khung trước: phông nền mười, người dẫn ở giữa có giá trị năm mươi.", reveal=1),
            P("Thử đoán: khung sau người dẫn chỉ hơi đổi sắc mặt, khung hiệu sẽ trông thế nào?", reveal=1, ask=True),
            P("Gần như toàn số không, chỉ ô người dẫn khác đi hai đơn vị. Chỉ cần gửi vài con số nhỏ thay vì cả khung.", reveal=2),
        ], compare={"left": {"label": "Khung trước", "grid": {"cells": [[10, 10, 10], [10, 50, 10], [10, 10, 10]], "accent": [[1, 1]]}},
                    "right": {"label": "Hiệu = khung sau − khung trước", "grid": {"cells": [[0, 0, 0], [0, 2, 0], [0, 0, 0]], "warn": [[1, 1]]}},
                    "arrow": "lấy hiệu"}),
        S("So sánh", "Nén từng khung so với gửi sai khác", [
            P("Nén từng khung chỉ dùng dư thừa không gian.", reveal=[1]),
            P("Gửi sai khác dùng thêm dư thừa thời gian, rất hiệu quả khi cảnh ít thay đổi.", reveal=[2]),
        ], table={"headers": ["", "Nén từng khung", "Gửi sai khác khung"],
                  "rows": [["Khai thác", "Dư thừa không gian", "+ dư thừa thời gian"], ["Cảnh tĩnh", "Vẫn gửi đủ mỗi khung", "Gần như không tốn bit"]]}),
        S("Ứng dụng", "Ý tưởng sai khác ở đâu", [
            P("Gọi video, chia sẻ màn hình, camera giám sát: cảnh phần lớn đứng yên, nên gửi phần thay đổi tiết kiệm cực nhiều.", "Gọi video, chia sẻ màn hình"),
        ]),
        limit("Vật di chuyển thì hiệu không còn nhỏ", [
            P("Khi người dẫn quay đầu hay camera lia, mọi thứ dịch đi vài pixel. Hiệu giữa hai khung lại lớn ở khắp các cạnh.", "Vật dịch chuyển → hiệu lớn"),
            P("Thay vì trừ ở đúng vị trí cũ, hãy tìm xem vật đã dịch đi đâu. Đó là bù chuyển động.", "→ Bù chuyển động"),
        ], CHAIN, 2),
        traps([["Video khai thác thêm dư thừa nào?", "Thời gian: giữa các khung liên tiếp"], ["Vì sao khung hiệu nén tốt?", "Phần lớn là số không"]],
              ["Bẫy một: so với ảnh tĩnh, video có thêm dư thừa thời gian giữa các khung liên tiếp.",
               "Bẫy hai: khung hiệu nén tốt vì phần lớn là số không khi cảnh ít thay đổi."]),
    ]),

    story("bu-chuyen-dong", "Ước lượng và bù chuyển động", "method", [
        S("Vấn đề", "Người dẫn quay đầu, camera lia", [
            P("Khi vật dịch đi vài pixel, trừ hai khung ở đúng vị trí cũ cho ra hiệu lớn, mất hết lợi ích.", "Dịch vài pixel → hiệu lớn"),
        ]),
        S("Cách cũ", "Trừ ở đúng vị trí cũ", [
            P("Sai khác khung luôn so pixel với pixel cùng vị trí ở khung trước, không biết vật đã đi đâu.", "So cùng vị trí"),
        ]),
        S("Ý tưởng", "Ghi món đồ dời đi đâu", [
            P("Khi chuyển nhà, các bạn không mua lại đồ, chỉ ghi món nào dời đi đâu. Với video: lấy khối này ở khung trước rồi dời sang phải ba pixel.",
              "Như chuyển nhà: ghi món nào dời đi đâu"),
            P("Lời chỉ dẫn đó là vector chuyển động. Ước lượng chuyển động là đi tìm vector; bù chuyển động là dùng vector và khung trước để dựng khung dự đoán.",
              "Ước lượng = tìm vector · bù = dùng vector"),
            P("Giả định đằng sau: khác biệt giữa các khung chủ yếu do vật thể cứng chuyển động.", "Giả định: vật cứng chuyển động"),
        ]),
        S("Cách làm", "So khớp khối", [
            P("Bên trái là khung tham chiếu bốn nhân bốn. Ở giữa là một khối hai nhân hai của khung hiện tại, nằm ở cột ba, bốn. Tìm vùng nào trong khung tham chiếu giống khối này nhất.",
              reveal=2),
            P("Thử vùng đúng vị trí cũ: tám, hai, chín, hai. Tổng sai khác tuyệt đối là mười bảy, khá lớn.", reveal=2),
            P("Thử đoán: vùng nào trong khung tham chiếu khớp nhất?", reveal=2, ask=True),
            P("Vùng lệch trái một pixel, được tô sáng, chín, tám, bảy, chín, cho tổng sai khác chỉ một. Hai vị trí khác cho mười tám và hai mươi hai. Vậy vật đã đi sang phải một pixel: đó là vector chuyển động.",
              reveal=[1, 2]),
            P("Lấy khối hiện tại trừ vùng tìm được, phần dư là ba số không và một số một. Chỉ cần gửi vector và phần dư gần như toàn không.", reveal=3),
        ], grid=[{"label": "Khung tham chiếu", "cells": [[1, 1, 2, 2], [1, 9, 8, 2], [1, 7, 9, 2], [1, 1, 2, 2]], "accent": [[1, 1], [1, 2], [2, 1], [2, 2]]},
                 {"label": "Khối hiện tại (cột 3–4)", "cells": [[9, 8], [7, 10]]},
                 {"label": "Phần dư", "cells": [[0, 0], [0, 1]], "warn": [[1, 1]]}]),
        S("So sánh", "Sai khác thô so với bù chuyển động", [
            P("Sai khác thô so cùng vị trí; bù chuyển động so với vị trí vật đã dịch tới.", reveal=[1]),
            P("Trong ví dụ, cùng vị trí cho tổng sai khác mười bảy, sau khi bù chỉ còn một.", reveal=[2]),
            P("Đổi lại phải gửi thêm vector chuyển động, và tìm kiếm tốn tính toán ở bên mã hóa.", reveal=[3]),
        ], table={"headers": ["", "Sai khác thô", "Bù chuyển động"],
                  "rows": [["So với", "Cùng vị trí", "Vị trí vật đã dịch tới"], ["Ví dụ (SAD)", "17", "1"], ["Gửi thêm", "—", "Vector chuyển động; tìm kiếm tốn tính toán"]]}),
        S("Ứng dụng", "Bù chuyển động ở đâu", [
            P("Mọi chuẩn nén video phổ biến, từ H.261, MPEG đến các chuẩn hiện đại, đều xây quanh ước lượng và bù chuyển động.", "Mọi chuẩn nén video"),
        ]),
        limit("Bên mã hóa và giải mã phải khớp nhau", [
            P("Bên giải mã chỉ có khung đã bị lượng tử, không có khung gốc. Nếu bên mã hóa dự đoán từ khung gốc, hai bên sẽ lệch nhau dần.", "Hai bên lệch nhau dần"),
            P("Cần một vòng lặp hoàn chỉnh trong bộ mã hóa. Video sau: hệ thống H.261.", "→ Vòng lặp H.261"),
        ], CHAIN, 3),
        traps([["Ước lượng khác bù chuyển động?", "Ước lượng tìm vector; bù dùng vector dựng khung dự đoán"],
               ["Giả định của ước lượng chuyển động?", "Khác biệt do vật thể cứng chuyển động"], ["Gửi đi gì?", "Vector chuyển động + phần dư"]],
              ["Bẫy một: ước lượng chuyển động là đi tìm vector; bù chuyển động là dùng vector để dựng khung dự đoán. Đề hay đảo hai định nghĩa.",
               "Bẫy hai: giả định là khác biệt giữa các khung do vật thể cứng chuyển động.",
               "Bẫy ba: bộ mã hóa gửi vector chuyển động và phần dư."]),
    ]),

    story("h261", "Hệ thống nén video và vòng lặp H.261", "method", [
        S("Vấn đề", "Ghép mọi thứ thành một bộ mã hóa", [
            P("Ta có dự đoán bằng bù chuyển động, có biến đổi và lượng tử từ chương năm. Cần ghép thành một hệ thống mà bên mã hóa và giải mã luôn đồng bộ.",
              "Ghép thành hệ thống đồng bộ"),
        ]),
        S("Cách cũ", "Dự đoán từ khung gốc", [
            P("Nếu dự đoán từ khung gốc, sai số lượng tử ở bên giải mã cộng dồn qua từng khung, ảnh trôi dần.", "Sai số cộng dồn, ảnh trôi"),
        ]),
        S("Ý tưởng", "Bộ mã hóa tự giải mã chính nó", [
            P("Bộ mã hóa tự giải mã lại khung vừa mã hóa và lưu làm tham chiếu. Như vậy nó dự đoán từ đúng khung mà bên giải mã có.", "Tự giải mã, lưu làm tham chiếu"),
        ]),
        S("Cách làm", "Sơ đồ hệ thống nén video", [
            P("Khối dự đoán: dự đoán trong khung dùng pixel lân cận, dự đoán liên khung dùng khung khác qua bù chuyển động.", reveal=1),
            P("Phần sai khác đi qua biến đổi: một phép biến đổi tuyến tính đơn vị hai chiều dồn năng lượng vào ít hệ số.", reveal=2),
            P("Rồi lượng tử hóa, mã entropy, và định dạng dòng bit.", reveal=4),
        ], graph=pipeline(["Khung vào", "Dự đoán trong / liên khung", "Biến đổi", "Lượng tử hóa", "Mã entropy", "Dòng bit"], [0, 1, 2, 4, 4, 4])),
        S("Cách làm", "Vòng lặp của bộ mã hóa", [
            P("Với khung I, không dự đoán gì, nén như ảnh tĩnh.", reveal=[2]),
            P("Với các khung khác, ước lượng chuyển động để có vector, rồi bù chuyển động để dựng khung dự đoán.", reveal=[3, 4, 5]),
            P("Phần sai khác được biến đổi, lượng tử; hệ số và vector được mã entropy.", reveal=[6, 7]),
            P("Thử đoán: dòng cuối cùng làm gì, và vì sao không được bỏ?", reveal=[7], ask=True),
            P("Giải lượng tử, biến đổi ngược, cộng khung dự đoán để có khung tái tạo, lưu làm tham chiếu. Đó là vai trò của toán tử ngược và bộ nhớ khung.", reveal=[8]),
        ], code={"lines": ["for mỗi khung hình F:", "    if F là khung I:  P ← 0   (không dự đoán)", "    else:", "        mv ← motion_estimation(F, ref)",
                           "        P  ← motion_compensation(ref, mv)", "    c ← quantize( transform(F − P) )", "    xuất entropy_encode(c, mv)",
                           "    ref ← P + inverse_transform( dequantize(c) )"]}),
        S("Cách làm", "Chọn bộ mã hóa video", [
            P("Ngoài tỉ lệ nén, phải cân nhắc đánh đổi giữa tốc độ bit và độ méo: càng ít bit hình càng xấu.", "Tốc độ bit ↔ độ méo"),
            P("Độ phức tạp và tính đối xứng: phim mã hóa một lần, giải mã hàng triệu lần, nên bộ mã hóa được phép nặng, bộ giải mã phải nhẹ.", "Độ phức tạp, tính đối xứng"),
            P("Còn có đặc tính kênh truyền, thống kê nguồn video, tốc độ cố định hay biến đổi, và tương thích chuẩn.", "Kênh truyền, nguồn, tốc độ, chuẩn"),
        ]),
        S("So sánh", "Có và không có vòng tái tạo", [
            P("Dự đoán từ khung gốc: bên giải mã lệch dần.", reveal=[1]),
            P("Dự đoán từ khung tái tạo: hai bên dùng đúng một tham chiếu, không trôi.", reveal=[2]),
        ], table={"headers": ["Tham chiếu dùng để dự đoán", "Kết quả"],
                  "rows": [["Khung gốc", "Bộ giải mã lệch dần, ảnh trôi"], ["Khung tái tạo (sau lượng tử)", "Hai bên đồng bộ"]]}),
        S("Ứng dụng", "H.261 ở đâu", [
            P("H.261 là chuẩn nền tảng cho hội nghị truyền hình qua đường điện thoại số. Các chuẩn sau đều kế thừa vòng lặp này.", "Hội nghị truyền hình; nền tảng cho MPEG"),
        ]),
        limit("Chỉ nhìn về quá khứ", [
            P("H.261 chỉ dự đoán tiến từ khung trước, với vector nguyên pixel. Khi một người bước ra từ sau cánh cửa, vùng mới lộ ra không hề có trong khung trước.",
              "Chỉ dự đoán tiến, nguyên pixel"),
            P("MPEG-1 cho phép nhìn cả về tương lai.", "→ MPEG-1"),
        ], CHAIN, 4),
        traps([["Vì sao bộ mã hóa có toán tử ngược?", "Tự tái tạo khung giống bộ giải mã để làm tham chiếu"],
               ["Khung I được dự đoán từ đâu?", "Không dự đoán: nén như ảnh tĩnh"], ["Tính đối xứng nghĩa là gì?", "Độ phức tạp mã hóa so với giải mã"]],
              ["Bẫy một: bộ mã hóa có toán tử ngược và bộ nhớ khung để tự tái tạo đúng khung mà bộ giải mã có.",
               "Bẫy hai: khung I không dự đoán, nén như ảnh tĩnh.",
               "Bẫy ba: tính đối xứng so độ phức tạp giữa mã hóa và giải mã."]),
    ]),

    story("mpeg", "MPEG-1 và MPEG-2", "method", [
        S("Vấn đề", "Vùng mới lộ ra và chuyển động lẻ pixel", [
            P("Một người bước ra từ sau cánh cửa: vùng vừa lộ ra không có trong khung quá khứ. Và vật thật không dịch chuyển đúng số nguyên pixel.",
              "Vùng mới lộ ra; chuyển động lẻ pixel"),
        ]),
        S("Cách cũ", "H.261: dự đoán tiến, nguyên pixel", [
            P("H.261 chỉ dự đoán từ khung trước, vector chính xác đến nguyên pixel.", "Chỉ quá khứ, nguyên pixel"),
        ]),
        S("Ý tưởng", "Nhìn cả về tương lai", [
            P("MPEG-1 cho phép dự đoán hai chiều: dùng cả khung tương lai làm tham chiếu. Vùng mới lộ ra có sẵn ở khung tương lai, và kết hợp hai chiều còn giúp giảm nhiễu.",
              "Dự đoán hai chiều"),
            P("Vector chuyển động chính xác đến nửa pixel, dự đoán tốt hơn nguyên pixel.", "Nửa pixel"),
            P("MPEG phát triển qua ba giai đoạn: xác định yêu cầu, cạnh tranh công nghệ, và hội tụ về một giải pháp thống nhất.", "Yêu cầu → cạnh tranh → hội tụ"),
        ]),
        S("Cách làm", "Bốn loại khung trong nhóm ảnh", [
            P("Chuỗi video chia thành các nhóm ảnh, GOP. Khung I mã hóa độc lập, nén kém nhất nhưng là điểm truy cập ngẫu nhiên.", reveal=1),
            P("Khung P dự đoán tiến có bù chuyển động từ khung I hoặc P phía trước, nén tốt hơn I.", reveal=2),
            P("Khung B dự đoán hai chiều từ khung I hoặc P ở cả quá khứ lẫn tương lai.", reveal=3),
            P("Khung D chỉ giải mã hệ số DC, độ phân giải thấp, hiếm dùng, chỉ để tìm kiếm nhanh.", reveal=4),
        ], table={"headers": ["Loại", "Dự đoán từ đâu", "Mức nén", "Vai trò"],
                  "rows": [["I (intra)", "Không tham chiếu", "Thấp nhất", "Truy cập ngẫu nhiên"], ["P (predictive)", "I/P phía trước", "Cao hơn I", "Dự đoán tiến"],
                           ["B (bi-directional)", "I/P quá khứ và tương lai", "Cao nhất", "Dự đoán hai chiều"], ["D (dc)", "Chỉ hệ số DC", "—", "Tìm kiếm nhanh, hiếm dùng"]]}),
        S("Cách làm", "Thứ tự mã hóa khác thứ tự hiển thị", [
            P("Nhóm ảnh hiển thị theo thứ tự I một, B hai, B ba, P bốn, B năm, B sáu, P bảy. Mã hóa trước tiên là I một.", reveal=1),
            P("Thử đoán: khung nào được mã hóa tiếp theo?", reveal=1, ask=True),
            P("P bốn. Vì B hai và B ba cần cả I một lẫn P bốn, nên P bốn phải đi trước chúng.", reveal=2),
            P("Rồi mới đến B hai và B ba, mỗi khung có hai mũi tên tham chiếu.", reveal=3),
            P("Tương tự, P bảy đi trước B năm và B sáu. Thứ tự mã hóa: I một, P bốn, B hai, B ba, P bảy, B năm, B sáu. Khung tham chiếu luôn đi trước khung B dựa vào nó.",
              reveal=5),
        ], graph=gop_graph()),
        S("Cách làm", "Slice, macroblock và MPEG-2", [
            P("Mỗi ảnh chia thành các slice, mỗi slice là dãy macroblock liền nhau theo thứ tự quét. Mỗi macroblock gồm một khối độ chói mười sáu nhân mười sáu và hai khối màu tám nhân tám.",
              "Slice → macroblock (16×16 + 2 khối 8×8)"),
            P("MPEG-2 nhắm tới chất lượng cao hơn: video theo yêu cầu, truyền hình số, DVD, HDTV. Truy cập ngẫu nhiên và chuyển kênh nhanh vẫn dựa vào khung I.",
              "MPEG-2: DVD, HDTV, truyền hình số"),
        ]),
        S("So sánh", "H.261, MPEG-1 và MPEG-2", [
            P("H.261 đặt nền tảng với dự đoán tiến.", reveal=[1]), P("MPEG-1 thêm dự đoán hai chiều, nửa pixel, nhóm ảnh I, P, B, D.", reveal=[2]),
            P("MPEG-2 kế thừa và nhắm tới chất lượng cao.", reveal=[3]),
        ], table={"headers": ["Chuẩn", "Dự đoán chuyển động", "Điểm cần nhớ"],
                  "rows": [["H.261", "Tiến, từ khung trước", "Nền tảng: ME + MC + biến đổi + lượng tử + entropy"], ["MPEG-1", "Hai chiều, nửa pixel", "GOP với I, P, B, D"],
                           ["MPEG-2", "Kế thừa MPEG-1", "DVD, HDTV, truyền hình số"]]}),
        S("Ứng dụng", "MPEG ở đâu", [
            P("MPEG-1 dùng cho đĩa video CD, MPEG-2 cho DVD và truyền hình số. Khi tua video, trình phát nhảy tới khung I gần nhất.", "VCD, DVD, truyền hình số; tua tới khung I"),
        ]),
        limit("Một dòng bit, một chất lượng", [
            P("Một dòng bit MPEG được mã hóa cho một tốc độ bit cố định. Người xem trên điện thoại mạng yếu và người xem trên TV lớn cần những phiên bản khác nhau.",
              "Một dòng bit cho một tốc độ"),
            P("Có cách nào mã hóa một lần mà cắt bớt được tùy ý? Đó là mã hóa khả mở.", "→ MC-EZBC khả mở"),
        ], CHAIN, 5),
        traps([["Khung nào cho truy cập ngẫu nhiên?", "Khung I"], ["Khung B tham chiếu khung nào?", "I/P quá khứ VÀ tương lai, không phải B"],
               ["MPEG-1 chính xác đến đâu?", "Nửa pixel"], ["Khung D dùng làm gì?", "Tìm kiếm nhanh; chỉ DC, hiếm dùng"]],
              ["Bẫy một: khung cho truy cập ngẫu nhiên là khung I.",
               "Bẫy hai: khung B tham chiếu khung I hoặc P ở cả quá khứ và tương lai, không tham chiếu khung B.",
               "Bẫy ba: MPEG-1 cho vector chuyển động chính xác nửa pixel.",
               "Bẫy bốn: khung D chỉ có hệ số DC, dùng để tìm kiếm nhanh."]),
    ]),

    story("mc-ezbc", "Mã hóa wavelet khả mở MC-EZBC", "method", [
        S("Vấn đề", "Một bản tin, nhiều kiểu người xem", [
            P("Cùng bản tin, người xem trên điện thoại mạng yếu, người xem trên TV lớn. Mã hóa riêng cho từng người thì quá tốn.", "Nhiều thiết bị, nhiều băng thông"),
        ]),
        S("Cách cũ", "Dòng bit một lớp", [
            P("Dòng bit MPEG được tối ưu cho một tốc độ. Cắt bớt thì không giải mã được.", "Cắt bớt là hỏng"),
        ]),
        S("Ý tưởng", "Mã hóa một lần, cắt đâu cũng được", [
            P("Mã hóa khả mở: chỉ mã hóa một lần, dòng bit có thể bị cắt bớt mà vẫn giải mã được, ở chất lượng, độ phân giải hoặc tốc độ khung thấp hơn.",
              "Cắt bớt vẫn giải mã được"),
            P("Như một bài báo viết theo kiểu tháp ngược: đọc đoạn đầu đã nắm ý chính, đọc thêm thì thêm chi tiết.", "Như bài báo tháp ngược"),
        ]),
        S("Cách làm", "MC-EZBC và bộ lọc MCTF", [
            P("MC-EZBC là họ bộ mã băng con và wavelet có bù chuyển động. Nó vẫn khai thác tương quan thời gian, nhưng khả mở hoàn toàn.", "Wavelet có bù chuyển động"),
            P("Khả mở theo ba chiều: chất lượng hay tốc độ bit, độ phân giải không gian, và tốc độ khung hình.", "Khả mở: chất lượng, độ phân giải, tốc độ khung"),
            P("Cốt lõi là bộ lọc thời gian có bù chuyển động, MCTF, thường cài bằng kỹ thuật nâng lifting, tạo hệ số thông thấp và thông cao theo trục thời gian.",
              "MCTF qua lifting: thông thấp + thông cao theo thời gian"),
        ]),
        S("So sánh", "MPEG so với MC-EZBC", [
            P("MPEG cho một dòng bit ở một tốc độ.", reveal=[1]), P("MC-EZBC cho một dòng bit cắt được theo chất lượng, độ phân giải và tốc độ khung.", reveal=[2]),
        ], table={"headers": ["", "MPEG-1 / MPEG-2", "MC-EZBC"],
                  "rows": [["Dòng bit", "Một tốc độ cố định", "Nhúng, cắt được tùy ý"], ["Biến đổi", "DCT theo khối", "Wavelet + MCTF theo thời gian"]]}),
        S("Ứng dụng", "Khả mở ở đâu", [
            P("Phát video tới nhiều thiết bị cùng lúc, mạng có băng thông thay đổi: bên nhận lấy phần dòng bit vừa với mình.", "Nhiều thiết bị, băng thông thay đổi"),
        ]),
        limit("Video đã nén sẵn bằng chuẩn khác", [
            P("Phần lớn video đã có sẵn được nén bằng chuẩn không khả mở. Muốn đưa chúng tới thiết bị khác, phải đổi dạng.", "Video có sẵn, chuẩn khác"),
            P("Video sau: chuyển mã.", "→ Chuyển mã"),
        ], CHAIN, 6),
        traps([["MC-EZBC khả mở theo gì?", "Chất lượng/tốc độ bit, độ phân giải, tốc độ khung"], ["MCTF cài bằng gì?", "Kỹ thuật nâng (lifting)"]],
              ["Bẫy một: MC-EZBC khả mở hoàn toàn theo chất lượng, độ phân giải không gian và tốc độ khung hình.",
               "Bẫy hai: MCTF thường được cài bằng kỹ thuật nâng lifting, cho hệ số thông thấp và thông cao theo thời gian."]),
    ]),

    story("chuyen-ma", "Chuyển mã video", "method", [
        S("Vấn đề", "Video đã nén, thiết bị không hợp", [
            P("Bản tin đã nén chất lượng cao cho truyền hình. Giờ cần một bản nhẹ cho điện thoại, hoặc một bản theo chuẩn khác mà thiết bị cũ đọc được.", "Cần bản nhẹ hoặc chuẩn khác"),
        ]),
        S("Cách cũ", "Mã hóa lại từ đầu", [
            P("Cách thô là tìm lại video gốc chưa nén rồi mã hóa lại. Nhưng thường không còn video gốc, và mã hóa lại toàn bộ rất tốn.", "Không còn gốc, tốn kém"),
        ]),
        S("Ý tưởng", "Đổi dạng, không quay lại phim", [
            P("Chuyển mã là đổi một video đã nén sang dạng nén khác, như phát hành thêm bản nhẹ cho điện thoại mà không cần quay lại phim.", "Đổi dạng nén → dạng nén"),
        ]),
        S("Cách làm", "Ba ứng dụng chính", [
            P("Giảm tốc độ bit cho hợp băng thông.", reveal=1), P("Giảm độ phân giải không gian hoặc tốc độ khung cho hợp thiết bị.", reveal=2),
            P("Chuyển đổi giữa các chuẩn mã hóa. Chuyển mã dị thể là khi chuẩn vào khác chuẩn ra: cho phép truy cập đa phương tiện trên mọi thiết bị, nhưng cần một vòng giải mã và một vòng mã hóa riêng.",
              reveal=3),
        ], table={"headers": ["Ứng dụng", "Thay đổi gì"],
                  "rows": [["Giảm tốc độ bit", "Bit/giây cho hợp kênh truyền"], ["Giảm độ phân giải", "Không gian và/hoặc thời gian"], ["Đổi chuẩn (dị thể)", "Chuẩn vào ≠ chuẩn ra"]]}),
        S("So sánh", "Khả mở so với chuyển mã", [
            P("Mã hóa khả mở chuẩn bị trước một dòng bit cắt được.", reveal=[1]), P("Chuyển mã xử lý sau, với video đã nén sẵn ở bất kỳ chuẩn nào.", reveal=[2]),
        ], table={"headers": ["", "Mã hóa khả mở", "Chuyển mã"],
                  "rows": [["Khi nào", "Lúc mã hóa", "Sau khi đã nén"], ["Chi phí", "Cắt dòng bit, rất nhẹ", "Giải mã + mã hóa lại"]]}),
        S("Ứng dụng", "Chuyển mã ở đâu", [
            P("Các nền tảng video tạo nhiều phiên bản độ phân giải cho cùng một video để người xem chọn hoặc tự động chuyển theo tốc độ mạng.", "Nhiều độ phân giải trên nền tảng video"),
        ]),
        limit("Pipeline do con người thiết kế", [
            P("Mọi khối từ ước lượng chuyển động đến mã entropy đều do con người thiết kế. Cuối chương, slide giới thiệu hướng dùng mạng nơ-ron sâu thay hoặc bổ trợ từng khối, tiến tới nén video học từ đầu đến cuối.",
              "Học sâu: nén video end-to-end"),
        ], CHAIN, 6),
        traps([["Ba ứng dụng của chuyển mã?", "Giảm bit, giảm độ phân giải, đổi chuẩn"], ["Chuyển mã dị thể là gì?", "Chuẩn vào khác chuẩn ra"]],
              ["Bẫy một: ba ứng dụng là giảm tốc độ bit, giảm độ phân giải không gian hoặc thời gian, và đổi chuẩn mã hóa.",
               "Bẫy hai: chuyển mã dị thể là khi chuẩn đầu vào khác chuẩn đầu ra."]),
    ]),

    story("tong-ket", "Tổng kết chương 6", "summary", [
        S("Tổng kết", "Nén video trong một mạch", [
            P("Nhìn lại bản tin thời sự. Video bắt buộc nén khoảng hai mươi bốn lần, nên phải khai thác dư thừa thời gian."),
            P("Gửi sai khác khung, rồi bù chuyển động bằng vector, ghép thành vòng lặp H.261 với bộ mã hóa tự tái tạo khung tham chiếu."),
            P("MPEG-1 thêm khung B và nửa pixel, MPEG-2 cho chất lượng cao, MC-EZBC cho dòng bit khả mở, và chuyển mã đổi dạng video đã nén."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: khung I cho truy cập ngẫu nhiên."), P("Hai: khung B tham chiếu I hoặc P ở cả quá khứ và tương lai."),
            P("Ba: ước lượng tìm vector, bù dùng vector."), P("Bốn: MPEG-1 chính xác nửa pixel."), P("Năm: khung D chỉ có DC, để tìm kiếm nhanh."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Truy cập ngẫu nhiên?", "Khung I"], ["Khung B tham chiếu?", "I/P quá khứ và tương lai"], ["ME và MC?", "Tìm vector / dùng vector"],
                           ["MPEG-1?", "Nửa pixel"], ["Khung D?", "Chỉ DC, tìm kiếm nhanh"]]}),
        S("Tổng kết", "Sang chương 7", [
            P("Chương bảy quay về điểm xuất phát: ảnh và video được thu nhận, lấy mẫu như thế nào.", "Chương 7: thu nhận ảnh"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–3", "Bản tin 36,5 Mbps qua 1,5 Mbps", "—", "Cần nén ~24 lần → dư thừa thời gian", "→ Sai khác khung"],
    ["Sai khác khung", "5–7", "Phông nền lặp lại", "Nén từng khung", "Gửi khung hiệu", "Vật dịch → hiệu lớn → bù chuyển động"],
    ["Bù chuyển động", "7–10", "Vật dịch vài pixel", "Trừ cùng vị trí", "So khớp khối, vector chuyển động", "Hai bên lệch → vòng lặp H.261"],
    ["H.261", "4–12", "Ghép thành hệ thống", "Dự đoán từ khung gốc", "Tự tái tạo khung tham chiếu; yếu tố chọn codec", "Chỉ quá khứ → MPEG-1"],
    ["MPEG-1/2", "22–33", "Vùng mới lộ ra", "Dự đoán tiến, nguyên pixel", "B hai chiều, nửa pixel, GOP; MPEG-2", "Một tốc độ → khả mở"],
    ["MC-EZBC", "13–17", "Nhiều thiết bị", "Dòng bit một lớp", "Wavelet + MCTF, cắt được", "Video có sẵn → chuyển mã"],
    ["Chuyển mã", "18–21", "Video đã nén không hợp thiết bị", "Mã hóa lại từ gốc", "Đổi dạng; dị thể", "→ Học sâu, tổng kết"],
    ["Tổng kết", "—", "—", "—", "Bẫy chung", "→ Chương 7"],
]
write(6, "Nén video", EX, stories, MAP)
