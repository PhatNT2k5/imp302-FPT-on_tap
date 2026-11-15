import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, story, traps, write  # noqa: E402

CHAIN = ["Ordered dithering", "Error diffusion", "Median cut", "Minkowski / MSE", "Mắt người", "SSIM"]
EX = "Một bức ảnh chân dung: in ra máy in đen trắng, hiển thị trên màn hình ít màu, rồi chấm điểm chất lượng sau khi xử lý"


def median_cut_hist():
    values = [10, 12, 20, 22, 100, 110, 200, 220]
    bars = [{"label": str(v), "value": v} for v in values]
    lines = [{"at": 4, "label": "cắt 1", "step": 1}, {"at": 2, "label": "cắt 2", "step": 2}, {"at": 6, "label": "cắt 2", "step": 2}]
    for i in range(8):
        bars[i]["marks"] = [{"step": 3, "style": "accent" if i < 4 else "warn"}]
    return {"bars": bars, "lines": lines, "caption": "8 pixel đã sắp xếp; vạch cam = chỗ cắt theo trung vị (số pixel)"}


stories = [
    intro("mo-dau", "Mở đầu: hiển thị ảnh và chấm điểm chất lượng", "Một bức chân dung đi qua nhiều thiết bị", [
        P("Chào các bạn. Chương tám là hiển thị và đánh giá ảnh. Ví dụ của cả chương: một bức ảnh chân dung hai trăm năm mươi sáu mức xám.",
          "Ví dụ: ảnh chân dung 256 mức"),
        P("Ta cần in nó ra máy in laser chỉ có mực đen và giấy trắng, hiển thị bản màu trên một màn hình ít màu, rồi chấm điểm xem ảnh sau xử lý còn tốt đến đâu.",
          "In 2 mức · hiển thị ít màu · chấm điểm"),
        P("Thử nghĩ trước: máy in chỉ có mực đen, làm sao in ra được màu xám?", "Mực đen thì in xám thế nào?", ask=True),
    ], CHAIN, [
        P("Phần một: hiển thị với ít mức. Ordered dithering, error diffusion cho ảnh xám, và median cut cho ảnh màu.", "Hiển thị: dithering → error diffusion → median cut"),
        P("Phần hai: chấm điểm. Từ độ đo Minkowski, qua đặc tính mắt người, đến SSIM.", "Đánh giá: Minkowski → mắt người → SSIM"),
        P("Mỗi phương pháp vá chỗ hụt của phương pháp trước, các bạn xem theo thứ tự.", "Xem theo thứ tự"),
    ]),

    story("ordered-dithering", "Halftoning và ordered dithering", "method", [
        S("Vấn đề", "In màu xám bằng mực đen", [
            P("Máy in laser chỉ có hai trạng thái: có mực hoặc không. Bức chân dung có hai trăm năm mươi sáu mức xám.", "Máy in: 2 trạng thái · ảnh: 256 mức"),
            P("Phát biểu trong slide: lượng tử mỗi pixel từ D mức về K mức, K nhỏ hơn D, sao cho tiêu chí méo nhỏ nhất. K bằng hai chính là halftoning, hai mức là không và D trừ một.",
              "K = 2 → halftoning: 0 và D−1"),
        ]),
        S("Cách cũ", "Ngưỡng hóa thường", [
            P("Cách đơn giản nhất là ngưỡng hóa ở một trăm hai mươi tám: sáng hơn thì trắng, tối hơn thì đen.", "Một ngưỡng 128"),
            P("Vùng má có mức xám một trăm sẽ thành đen kịt. Mọi sắc độ trung gian biến mất.", "Vùng xám 100 → đen kịt"),
        ]),
        S("Ý tưởng", "Lừa mắt bằng các chấm", [
            P("Nhìn sát một bức ảnh trên báo giấy, chỉ có chấm mực đen trên nền trắng. Nhìn từ xa, ta vẫn thấy đủ sắc xám.", "Báo giấy: chỉ có chấm đen"),
            P("Mắt hoạt động như bộ lọc thông thấp, tự lấy trung bình trên vùng nhỏ. Nhiều chấm thì tối, ít chấm thì sáng.", "Mắt lấy trung bình"),
            P("Ordered dithering thay một ngưỡng duy nhất bằng một ma trận ngưỡng, mỗi vị trí một ngưỡng riêng, lặp lại như lát gạch trên khắp ảnh.",
              "Ma trận ngưỡng lặp như lát gạch"),
        ]),
        S("Cách làm", "Dithering một vùng xám", [
            P("Vùng bốn pixel, mức xám một trăm.", reveal=1),
            P("Ma trận ngưỡng: ba mươi hai, một trăm năm mươi chín, hai trăm hai mươi ba, chín mươi sáu.", reveal=2),
            P("Thử đoán: có mấy pixel được bật sáng?", reveal=2, ask=True),
            P("Một trăm lớn hơn ba mươi hai, bật. Nhỏ hơn một trăm năm mươi chín, tắt. Nhỏ hơn hai trăm hai mươi ba, tắt. Lớn hơn chín mươi sáu, bật. Hai trên bốn pixel sáng.",
              reveal=3),
            P("Nhìn từ xa mắt thấy khoảng một trăm hai mươi bảy, gần một trăm hơn nhiều so với màu đen. Vùng càng sáng, càng nhiều pixel vượt ngưỡng.", reveal=3),
        ], grid=[{"label": "Vùng ảnh xám", "cells": [[100, 100], [100, 100]]}, {"label": "Ma trận ngưỡng", "cells": [[32, 159], [223, 96]]},
                 {"label": "Halftone (1 = bật)", "cells": [[1, 0], [0, 1]], "accent": [[0, 0], [1, 1]]}]),
        S("So sánh", "Ordered dithering so với ngưỡng hóa thường", [
            P("Ngưỡng hóa thường dùng một ngưỡng, vùng xám trung gian thành đen hoặc trắng hoàn toàn."),
            P("Ordered dithering dùng ma trận ngưỡng, giữ được sắc độ khi nhìn từ xa."),
            P("Cả hai đều xử lý từng pixel độc lập, rất nhanh."),
        ], table={"headers": ["", "Ngưỡng hóa thường", "Ordered dithering"],
                  "rows": [["Ngưỡng", "Một ngưỡng 128", "Ma trận ngưỡng lặp tuần hoàn"], ["Vùng xám 100", "Đen kịt (0)", "≈ 127 khi nhìn từ xa"],
                           ["Xử lý", "Từng pixel độc lập", "Từng pixel độc lập"]]}),
        S("Ứng dụng", "Dithering ở đâu", [
            P("Máy in laser, máy in phun, báo in, và màn hình ít màu đều dùng các biến thể của dithering.", "Máy in, báo, màn hình ít màu"),
        ]),
        limit("Sai số bị vứt đi, hoa văn lặp lại", [
            P("Ordered dithering làm tròn rồi bỏ luôn phần sai số. Ma trận lặp lại còn để lộ những hoa văn đều đặn trên ảnh.", "Bỏ sai số, lộ hoa văn"),
            P("Nếu giữ lại sai số và bù cho các pixel sau thì sao? Đó là error diffusion.", "→ Error diffusion"),
        ], CHAIN, 2),
        traps([["Halftoning ứng với K bằng mấy?", "K = 2, hai mức 0 và D−1"], ["Ordered dithering so pixel với gì?", "Ma trận ngưỡng cố định, lặp tuần hoàn"],
               ["Vì sao nhìn xa thấy xám?", "Mắt như bộ lọc thông thấp, lấy trung bình"]],
              ["Bẫy một: halftoning là trường hợp K bằng hai, hai mức không và D trừ một.",
               "Bẫy hai: ordered dithering so mỗi pixel với ma trận ngưỡng cố định lặp tuần hoàn.",
               "Bẫy ba: nhìn từ xa thấy xám vì mắt như bộ lọc thông thấp."]),
    ]),

    story("error-diffusion", "Error diffusion", "method", [
        S("Vấn đề", "Giữ sắc độ thật sát", [
            P("Ảnh in cần sát ảnh gốc hơn, đặc biệt trên máy in độ phân giải thấp và trung bình, không để lộ hoa văn lặp.", "Sát ảnh gốc, không hoa văn lặp"),
        ]),
        S("Cách cũ", "Ordered dithering", [
            P("Ordered dithering làm tròn từng pixel rồi bỏ phần sai số, và ma trận lặp lại tạo hoa văn.", "Bỏ sai số, hoa văn lặp"),
        ]),
        S("Ý tưởng", "Ghi nợ sai số, trả cho hàng xóm", [
            P("Giống trả tiền thiếu: lần này làm tròn thiếu bao nhiêu thì ghi nợ, lần sau bù lại.", "Như ghi nợ rồi trả sau"),
            P("Mỗi pixel trước khi ngưỡng hóa được cộng thêm sai số các pixel trước chuyển sang, gọi là đầu vào đã điều chỉnh u. Sai số e bằng u trừ đầu ra b.",
              "u = f + sai số nhận được · e = u − b"),
            P("Sai số chia cho các hàng xóm chưa xử lý theo trọng số của nhân khuếch tán h. Về lâu dài, sai số trung bình xấp xỉ không.", "Chia e qua nhân h"),
        ]),
        S("Cách làm", "Một hàng bốn pixel xám một trăm", [
            P("Dùng nhân đơn giản nhất: toàn bộ sai số đẩy sang pixel bên phải. Pixel một: u bằng một trăm, dưới ngưỡng, ra không, nợ cộng một trăm.", reveal=1),
            P("Thử đoán: pixel hai nhận món nợ đó, sẽ ra đen hay trắng?", reveal=1, ask=True),
            P("Một trăm cộng một trăm bằng hai trăm, vượt ngưỡng, ra hai trăm năm mươi lăm. Trả dư, sai số âm năm mươi lăm.", reveal=2),
            P("Pixel ba: một trăm trừ năm mươi lăm còn bốn mươi lăm, ra không, sai số cộng bốn mươi lăm.", reveal=3),
            P("Pixel bốn: một trăm bốn mươi lăm, ra hai trăm năm mươi lăm. Cả hàng đen, trắng, đen, trắng, trung bình khoảng một trăm hai mươi bảy, trong khi ngưỡng hóa thường cho toàn đen.",
              reveal=4),
        ], table={"headers": ["Pixel", "f", "u = f + e trước", "b (ngưỡng 128)", "e = u − b"],
                  "rows": [["1", "100", "100", "0", "+100"], ["2", "100", "100 + 100 = 200", "255", "−55"], ["3", "100", "100 − 55 = 45", "0", "+45"],
                           ["4", "100", "100 + 45 = 145", "255", "−110"]]}),
        S("Cách làm", "Mã giả error diffusion", [
            P("Đi qua từng pixel theo thứ tự quét, cộng phần sai số đã nhận được giá trị u.", reveal=[1, 2]),
            P("Ngưỡng hóa u để có đầu ra, tính sai số bằng u trừ đầu ra.", reveal=[3, 4]),
            P("Chia sai số cho các hàng xóm chưa xử lý theo nhân h. Vì chỉ chia cho pixel chưa xử lý, chỉ cần quét ảnh một lượt.", reveal=[5, 6]),
        ], code={"lines": ["for mỗi pixel (x, y) theo thứ tự quét:", "    u ← f(x, y) + sai số nhận từ các pixel trước", "    b(x, y) ← 255 nếu u ≥ 128, ngược lại 0",
                           "    e ← u − b(x, y)", "    for mỗi hàng xóm chưa xử lý (m, n):", "        cộng h(m, n) · e vào pixel đó"]}),
        S("So sánh", "Ba nhóm halftoning", [
            P("Ordered dithering so với ma trận ngưỡng cố định, mỗi pixel độc lập, đơn giản nhất."),
            P("Error diffusion ngưỡng hóa rồi khuếch tán sai số, pixel sau phụ thuộc pixel trước, chất lượng cao hơn."),
            P("Kỹ thuật tối ưu hóa tìm trực tiếp ảnh halftone làm nhỏ nhất tiêu chí méo, tốt nhất nhưng tốn nhất."),
        ], table={"headers": ["Phương pháp", "Cách làm", "Độ phức tạp"],
                  "rows": [["Ordered dithering", "Ma trận ngưỡng cố định, lặp tuần hoàn", "Thấp nhất"],
                           ["Error diffusion", "Ngưỡng hóa + khuếch tán sai số qua nhân h", "Trung bình"], ["Optimization", "Tối thiểu trực tiếp tiêu chí méo", "Cao nhất"]]}),
        S("Ứng dụng", "Error diffusion ở đâu", [
            P("Error diffusion phổ biến trong máy in phun và khi giảm số màu của ảnh, nhờ cho chất lượng cao mà không lộ hoa văn lặp.", "Máy in phun, giảm số màu"),
        ]),
        limit("Ảnh màu thì sao?", [
            P("Ta mới xử lý ảnh xám. Ảnh màu hai mươi bốn bit có hàng triệu màu, nhưng màn hình chỉ hiển thị được vài trăm màu. Chọn những màu nào?",
              "Hàng triệu màu → vài trăm màu"),
            P("Video sau: lượng tử hóa màu và median cut.", "→ Median cut"),
        ], CHAIN, 3),
        traps([["Sai số e tính thế nào?", "e = u − b (u: đầu vào đã điều chỉnh)"], ["Sai số chia cho ai?", "Hàng xóm CHƯA xử lý, theo nhân h"],
               ["Độ phức tạp tăng dần?", "Ordered dithering → error diffusion → optimization"]],
              ["Bẫy một: sai số bằng đầu vào đã điều chỉnh trừ đầu ra nhị phân.",
               "Bẫy hai: sai số chỉ chia cho hàng xóm chưa xử lý, theo nhân h.",
               "Bẫy ba: độ phức tạp tăng dần là ordered dithering, error diffusion, rồi tối ưu hóa."]),
    ]),

    story("median-cut", "Lượng tử hóa màu: median cut", "method", [
        S("Vấn đề", "Hàng triệu màu, màn hình vài trăm màu", [
            P("Ảnh chân dung màu có hai mươi bốn bit mỗi pixel, nhưng thiết bị chỉ có L bit, tức hai mũ L màu.", "K bit → L bit"),
            P("Phải làm hai việc: thiết kế bảng màu, và quyết định mỗi pixel dùng màu nào trong bảng.", "Thiết kế bảng màu + ánh xạ pixel"),
        ]),
        S("Cách cũ", "Chia đều không gian màu", [
            P("Cách ngây thơ là chia đều dải màu thành các khoảng bằng nhau. Nhưng ảnh chân dung chủ yếu là màu da và tóc, nhiều khoảng màu chẳng có pixel nào, bị lãng phí.",
              "Chia đều: phí màu cho vùng trống"),
        ]),
        S("Ý tưởng", "Mỗi màu đại diện số pixel bằng nhau", [
            P("Median cut thiết kế bảng màu theo nguyên tắc công bằng: mỗi màu trong bảng đại diện cho số pixel xấp xỉ bằng nhau.", "Mỗi màu ~ cùng số pixel"),
            P("Vùng màu nào nhiều pixel, như màu da, thì được chia nhiều màu hơn.", "Vùng đông pixel → nhiều màu hơn"),
        ]),
        S("Cách làm", "Các bước median cut", [
            P("Tính histogram màu: ảnh hai mươi bốn bit có tới mười sáu triệu màu.", "Histogram màu: tới 16 triệu"),
            P("Tiền lượng tử xuống mười lăm bit, mỗi kênh năm bit, còn ba mươi hai nghìn bảy trăm sáu mươi tám màu.", "Tiền lượng tử 15 bit: 32 768 màu"),
            P("Tìm hộp chữ nhật bao khít mọi màu có trong ảnh, cắt tại trung vị để mỗi nửa có khoảng nửa số pixel, rồi lặp đến khi đủ số màu.",
              "Hộp bao khít → cắt tại trung vị → lặp"),
        ]),
        S("Cách làm", "Từ tám giá trị xuống bốn màu", [
            P("Một kênh màu, tám pixel đã sắp xếp: mười, mười hai, hai mươi, hai mươi hai, một trăm, một trăm mười, hai trăm, hai trăm hai mươi.", reveal=0),
            P("Thử đoán: lần cắt đầu tiên sẽ nằm ở giá trị nào?", reveal=0, ask=True),
            P("Cắt tại trung vị, mỗi bên bốn pixel: giữa hai mươi hai và một trăm. Không phải giữa dải giá trị, vì cắt theo số pixel chứ không theo khoảng giá trị.", reveal=1),
            P("Cắt lần hai, mỗi hộp chia đôi tại trung vị của nó. Bốn hộp, mỗi hộp hai pixel.", reveal=2),
            P("Màu đại diện là trung bình mỗi hộp: mười một, hai mươi mốt, một trăm lẻ năm, hai trăm mười. Vùng tối nhiều pixel được hẳn hai màu.", reveal=3),
        ], histogram=median_cut_hist()),
        S("So sánh", "Chia đều so với median cut", [
            P("Chia đều cắt theo khoảng giá trị, dễ phí màu cho vùng không có pixel.", reveal=[1]),
            P("Median cut cắt theo số pixel, dồn màu vào nơi ảnh thật sự dùng. Sau đó mỗi pixel ánh xạ về màu gần nhất, hoặc dùng error diffusion với bảng màu làm codebook.",
              reveal=[2, 3]),
        ], table={"headers": ["", "Chia đều", "Median cut"],
                  "rows": [["Cắt theo", "Khoảng giá trị", "Số pixel (trung vị)"], ["Màu dồn vào", "Đều mọi nơi", "Vùng có nhiều pixel"],
                           ["Ánh xạ pixel", "Màu gần nhất", "Màu gần nhất hoặc error diffusion"]]}),
        S("Ứng dụng", "Bảng màu ở đâu", [
            P("Ảnh GIF chỉ có tối đa hai trăm năm mươi sáu màu, nên phải chọn bảng màu; median cut là một cách cổ điển để chọn.", "Ảnh GIF 256 màu"),
        ]),
        limit("Xử lý xong, chấm điểm thế nào?", [
            P("Dithering, error diffusion, median cut, cùng với nén ở chương năm, đều làm ảnh khác ảnh gốc. Ảnh nào tốt hơn? Cần một con số để chấm.",
              "Cần chấm điểm chất lượng"),
            P("Con số đầu tiên ai cũng nghĩ tới: so từng pixel. Đó là độ đo Minkowski.", "→ Minkowski"),
        ], CHAIN, 4),
        traps([["Median cut cắt hộp ở đâu?", "Tại trung vị: hai nửa có số pixel xấp xỉ bằng nhau"], ["Tiền lượng tử xuống mấy bit?", "15 bit: 32 768 màu"],
               ["Mỗi màu trong bảng đại diện gì?", "Số pixel xấp xỉ bằng nhau"]],
              ["Bẫy một: median cut cắt tại trung vị theo số pixel, không phải giữa dải giá trị.",
               "Bẫy hai: trước khi cắt, tiền lượng tử xuống mười lăm bit, ba mươi hai nghìn bảy trăm sáu mươi tám màu.",
               "Bẫy ba: mỗi màu trong bảng đại diện cho số pixel xấp xỉ bằng nhau."]),
    ]),

    story("minkowski", "Độ đo Minkowski", "method", [
        S("Vấn đề", "Ảnh nào giống ảnh gốc hơn?", [
            P("Có ảnh chân dung gốc, coi là hoàn hảo, và vài ảnh đã qua xử lý. Cần một con số cho biết mỗi ảnh lệch bao nhiêu.", "Một con số đo độ lệch"),
        ]),
        S("Cách cũ", "Hỏi người xem", [
            P("Cách chắc chắn nhất là mời nhiều người xem và chấm điểm. Nhưng tốn thời gian, tốn công, không làm tự động được.", "Người chấm: chắc nhưng tốn"),
        ]),
        S("Ý tưởng", "So từng pixel", [
            P("Ý tưởng tự nhiên nhất: lấy độ chênh lệch tại từng pixel giữa ảnh gốc và ảnh méo, rồi gộp lại thành một con số.", "Gộp chênh lệch từng pixel"),
        ]),
        S("Công thức", "Độ đo Minkowski", [
            P("Lấy chênh lệch từng pixel, nâng lũy thừa p, cộng lại, rồi lấy căn bậc p.", "Lũy thừa p, cộng, căn bậc p"),
            P("p bằng một là tổng sai khác tuyệt đối. p bằng hai gắn với sai số bình phương trung bình, MSE. p càng lớn, lỗi lớn càng chi phối.",
              "p = 1: tổng |sai| · p = 2: MSE"),
        ], formula=r"E_p = \Big( \sum_{i=1}^{N} \underbrace{|x_i - y_i|^{p}}_{\text{sai khác tại pixel } i} \Big)^{1/p}"),
        S("Cách làm", "Tính cho bốn pixel", [
            P("Ảnh gốc bốn pixel: một trăm, một trăm mười, một trăm, một trăm mười. Ảnh méo sáng hơn mười ở mọi pixel. Mỗi pixel chênh đúng mười.", reveal=1),
            P("Với p bằng một: cộng bốn lần mười, được bốn mươi.", reveal=2),
            P("Thử đoán: với p bằng hai, kết quả là bao nhiêu?", reveal=2, ask=True),
            P("Bình phương mỗi chênh lệch được một trăm, cộng lại bốn trăm, căn bậc hai được hai mươi. Còn MSE chia bốn trăm cho bốn pixel, bằng một trăm.", reveal=3),
        ], table={"headers": ["Đại lượng", "Phép tính", "Kết quả"],
                  "rows": [["Chênh lệch mỗi pixel", "|x − y|", "10"], ["p = 1", "10 + 10 + 10 + 10", "40"],
                           ["p = 2 và MSE", "√(4 · 10²) ; 400 / 4", "20 ; MSE = 100"]]}),
        S("So sánh", "Minkowski so với người chấm", [
            P("Người chấm phản ánh đúng cảm nhận nhưng tốn kém.", reveal=[1]),
            P("Minkowski tự động, nhanh, đơn giản, nhưng coi mỗi pixel độc lập.", reveal=[2]),
        ], table={"headers": ["", "Người chấm", "Minkowski / MSE"],
                  "rows": [["Phản ánh cảm nhận", "Đúng", "Không phải lúc nào cũng đúng"], ["Chi phí", "Cao", "Rất thấp, tự động"]]}),
        S("Ứng dụng", "MSE ở đâu", [
            P("MSE và các độ đo dựa trên nó có mặt khắp nơi: làm hàm mất mát khi huấn luyện, chấm điểm nén ảnh, so sánh bộ lọc khử nhiễu.", "Hàm mất mát, chấm nén, khử nhiễu"),
        ]),
        limit("Cùng sai số, khác hẳn cảm nhận", [
            P("Slide hỏi: độ đo này có thật sự tốt không? Không. Nó không biết gì về cấu trúc ảnh. Hai ảnh méo cùng sai số có thể trông khác nhau một trời một vực.",
              "Không hiểu cấu trúc ảnh"),
            P("Muốn đo đúng, trước hết phải hiểu mắt người nhìn ảnh thế nào.", "→ Mắt người"),
        ], CHAIN, 5),
        traps([["p = 2 gắn với độ đo nào?", "Sai số bình phương trung bình (MSE)"], ["Minkowski có phản ánh tốt cảm nhận?", "Không: bỏ qua cấu trúc"]],
              ["Bẫy một: Minkowski với p bằng hai gắn với sai số bình phương trung bình.",
               "Bẫy hai: Minkowski không phản ánh tốt cảm nhận thị giác vì coi pixel độc lập."]),
    ]),

    story("mat-nguoi", "Mắt người và tiêu chí cảm nhận", "extra", [
        S("Vấn đề", "Mắt người thấy gì, bỏ qua gì?", [
            P("Một độ đo cảm nhận phải tìm ra khác biệt giữa hai ảnh mà mắt người thật sự nhận thấy. Vậy mắt nhạy với gì?", "Đo khác biệt mắt thấy được"),
        ]),
        S("Ý tưởng", "Bốn đặc tính của hệ thị giác", [
            P("Hàm độ nhạy tương phản, CSF, mô tả đáp ứng tần số của mắt, có dạng bộ lọc thông dải: nhạy nhất với chi tiết cỡ vừa. Đo bằng ngưỡng nhìn thấy lưới sóng sin.",
              "CSF: bộ lọc thông dải"),
            P("Thích nghi ánh sáng: mắt cảm nhận tương phản so với nền, không cảm nhận độ sáng tuyệt đối.", "Thích nghi ánh sáng"),
            P("Che lấp tương phản: nhiễu trên nền trời phẳng rất dễ thấy, nhưng cùng lượng nhiễu trên bãi cỏ thì gần như vô hình.", "Che lấp tương phản"),
            P("Che lấp thời gian, quan trọng với video: cảm nhận vật chuyển động phụ thuộc mắt có đang bám theo vật hay không.", "Che lấp thời gian"),
        ]),
        S("Cách làm", "Ba điều kiện của một độ đo cảm nhận", [
            P("Hiệu chỉnh: ảnh đến từ nhiều thiết bị, qua nhiều phép biến đổi, phải quy về cùng thang đo.", reveal=1),
            P("Đăng ký: hai ảnh phải khớp từng điểm. Lệch một pixel là mọi so sánh theo pixel vô nghĩa.", reveal=2),
            P("Mô hình hiển thị: mắt chỉ thấy những gì màn hình hay máy in tái tạo được.", reveal=3),
        ], table={"headers": ["Điều kiện", "Vì sao cần"],
                  "rows": [["Hiệu chỉnh (calibration)", "Ảnh từ nhiều thiết bị, nhiều phép biến đổi"], ["Đăng ký (registration)", "Cần tương ứng điểm–điểm"],
                           ["Mô hình hiển thị", "Mắt chỉ thấy thứ thiết bị tái tạo"]]}),
        traps([["CSF có dạng bộ lọc gì?", "Thông dải (bandpass)"], ["Ba điều kiện của độ đo cảm nhận?", "Hiệu chỉnh, đăng ký, mô hình hiển thị"]],
              ["Bẫy một: hàm độ nhạy tương phản có dạng thông dải, không phải thông thấp hay thông cao.",
               "Bẫy hai: ba điều kiện là hiệu chỉnh, đăng ký và mô hình hiển thị."]),
    ]),

    story("ssim", "Chỉ số tương đồng cấu trúc SSIM", "method", [
        S("Vấn đề", "Đo theo cách mắt nhìn", [
            P("Mắt người nhạy với cấu trúc: cạnh, hoa văn, chi tiết khuôn mặt. Ta cần độ đo chú ý đến cấu trúc chứ không chỉ cộng sai số.", "Đo theo cấu trúc"),
        ]),
        S("Cách cũ", "Minkowski, MSE", [
            P("Minkowski coi mỗi pixel độc lập, không biết pixel nào đi cùng pixel nào.", "Pixel độc lập, không cấu trúc"),
        ]),
        S("Ý tưởng", "Ba câu hỏi gần như độc lập", [
            P("SSIM tách sự giống nhau thành ba câu hỏi. Độ chói: hai ảnh sáng như nhau không? Ước lượng bằng trung bình.", "Độ chói: trung bình"),
            P("Tương phản: dao động mạnh như nhau không? Ước lượng bằng độ lệch chuẩn.", "Tương phản: độ lệch chuẩn"),
            P("Cấu trúc: sau khi trừ trung bình và chia độ lệch chuẩn, hai tín hiệu có lên xuống cùng nhau không?", "Cấu trúc: lên xuống cùng nhau?"),
        ]),
        S("Công thức", "SSIM", [
            P("Ba thành phần nhân lại thành một chỉ số.", "SSIM = l · c · s"),
            P("Thực tế SSIM tính cục bộ qua cửa sổ Gauss đối xứng tròn trượt trên ảnh, tạo bản đồ chất lượng, rồi lấy trung bình làm điểm cuối.",
              "Cửa sổ Gauss trượt → bản đồ → trung bình"),
        ], formula=r"S(x,y) = \underbrace{l(x,y)}_{\text{độ chói: } \mu} \cdot \underbrace{c(x,y)}_{\text{tương phản: } \sigma} \cdot \underbrace{s(x,y)}_{\text{cấu trúc}}"),
        S("Cách làm", "Cùng MSE nhưng SSIM khác hẳn", [
            P("Ảnh gốc là kết cấu sọc: một trăm, một trăm mười, lặp lại. Méo cách một: cộng mười mọi pixel, ảnh chỉ sáng hơn. Méo cách hai: cộng trừ xen kẽ, đảo sọc sáng thành tối.",
              reveal=1),
            P("Mỗi pixel đều lệch đúng mười, nên MSE của cả hai đều bằng một trăm. Theo MSE, hai ảnh tệ như nhau.", reveal=2),
            P("Thử đoán: SSIM có cho hai ảnh này cùng điểm không?", reveal=2, ask=True),
            P("Độ chói: ảnh một khoảng không phẩy chín chín sáu, ảnh hai bằng một. Tương phản: cả hai bằng một.", reveal=[3, 4]),
            P("Cấu trúc: ảnh một lên xuống cùng nhịp, bằng một; ảnh hai lên đúng lúc gốc xuống, bằng âm một.", reveal=5),
            P("SSIM: ảnh một xấp xỉ một, gần hoàn hảo; ảnh hai âm một, tệ nhất. Cùng MSE, nhưng SSIM phân biệt được ảnh chỉ sáng lên với ảnh bị phá cấu trúc.", reveal=6),
        ], table={"headers": ["Với x = 100, 110, 100, 110", "y₁ = x + 10 (sáng hơn)", "y₂ (sọc bị đảo)"],
                  "rows": [["Giá trị", "110, 120, 110, 120", "110, 100, 110, 100"], ["MSE", "100", "100"], ["Độ chói l", "0,996", "1"],
                           ["Tương phản c", "1", "1"], ["Cấu trúc s", "1", "−1"], ["SSIM = l·c·s", "0,996", "−1"]]}),
        S("So sánh", "MSE so với SSIM", [
            P("MSE cộng sai số từng pixel, không biết cấu trúc.", reveal=[1]),
            P("SSIM so độ chói, tương phản và cấu trúc, khớp với cảm nhận của mắt hơn.", reveal=[2, 3]),
        ], table={"headers": ["", "MSE / Minkowski", "SSIM"],
                  "rows": [["Nhìn vào", "Sai khác từng pixel", "Độ chói, tương phản, cấu trúc"], ["Ví dụ sọc", "100 và 100: như nhau", "0,996 và −1: khác hẳn"],
                           ["Khớp cảm nhận", "Kém", "Tốt hơn"]]}),
        S("Ứng dụng", "SSIM ở đâu", [
            P("SSIM được dùng rộng rãi để chấm chất lượng ảnh và video nén, đánh giá bộ khử nhiễu, phục hồi và siêu phân giải ảnh.", "Chấm nén, khử nhiễu, phục hồi"),
        ]),
        limit("Vẫn cần ảnh gốc", [
            P("SSIM cần ảnh tham chiếu hoàn hảo và hai ảnh phải được đăng ký khớp nhau. Ở các chương sau, ta chuyển từ làm đẹp ảnh sang hiểu ảnh.",
              "Cần ảnh gốc, cần đăng ký"),
        ], CHAIN, 6),
        traps([["Ba thành phần của SSIM?", "Độ chói (trung bình), tương phản (độ lệch chuẩn), cấu trúc"], ["SSIM tính cục bộ bằng gì?", "Cửa sổ Gauss đối xứng tròn"],
               ["Cùng MSE thì cùng SSIM?", "Không: ví dụ sọc 0,996 và −1"]],
              ["Bẫy một: SSIM gồm độ chói đo bằng trung bình, tương phản đo bằng độ lệch chuẩn, và cấu trúc.",
               "Bẫy hai: SSIM tính cục bộ qua cửa sổ Gauss đối xứng tròn, rồi lấy trung bình.",
               "Bẫy ba: cùng MSE chưa chắc cùng SSIM."]),
    ]),

    story("tong-ket", "Tổng kết chương 8", "summary", [
        S("Tổng kết", "Hiển thị và đánh giá", [
            P("Nhìn lại bức chân dung. Ordered dithering in xám bằng ma trận ngưỡng, error diffusion giữ và bù sai số, median cut chọn bảng màu theo số pixel."),
            P("Minkowski chấm bằng sai số từng pixel, mắt người cho ta các đặc tính CSF và che lấp, và SSIM chấm theo độ chói, tương phản, cấu trúc."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: halftoning là K bằng hai."), P("Hai: độ phức tạp tăng dần là ordered dithering, error diffusion, tối ưu hóa."),
            P("Ba: median cut cắt tại trung vị."), P("Bốn: CSF là thông dải."), P("Năm: SSIM gồm độ chói, tương phản và cấu trúc."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Halftoning?", "K = 2: 0 và D−1"], ["Độ phức tạp tăng dần?", "Dithering → error diffusion → optimization"],
                           ["Median cut cắt ở đâu?", "Trung vị (số pixel)"], ["CSF?", "Thông dải"], ["SSIM?", "Độ chói, tương phản, cấu trúc"]]}),
        S("Tổng kết", "Sang chương 9", [
            P("Sang chương chín, ta bắt đầu phần hiểu ảnh với bài toán phân đoạn: chia ảnh thành các vùng có ý nghĩa.", "Chương 9: phân đoạn ảnh"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–2", "Chân dung 256 mức: in, hiển thị, chấm điểm", "—", "Hiển thị ít mức + đánh giá", "→ Ordered dithering"],
    ["Ordered dithering", "3–6", "In xám bằng mực đen", "Ngưỡng hóa thường: xám → đen", "Ma trận ngưỡng lặp; mắt lấy trung bình", "Bỏ sai số → error diffusion"],
    ["Error diffusion", "7–9", "Sát ảnh gốc, không hoa văn", "Ordered dithering", "Ghi nợ sai số, chia cho hàng xóm qua h", "Ảnh màu → median cut"],
    ["Median cut", "10–12", "Triệu màu → vài trăm màu", "Chia đều không gian màu", "Cắt hộp tại trung vị theo số pixel", "Chấm điểm → Minkowski"],
    ["Minkowski", "17", "Ảnh nào giống gốc hơn", "Người chấm: tốn kém", "Chuẩn Lp của sai khác", "Bỏ qua cấu trúc → mắt người"],
    ["Mắt người", "13–16", "Mắt thấy gì", "—", "CSF, thích nghi, che lấp; 3 điều kiện", "→ SSIM"],
    ["SSIM", "18–20", "Đo theo cấu trúc", "Minkowski", "Độ chói × tương phản × cấu trúc", "→ Chương 9"],
    ["Tổng kết", "—", "—", "—", "Bẫy chung", "→ Chương 9"],
]
write(8, "Hiển thị & đánh giá", EX, stories, MAP)
