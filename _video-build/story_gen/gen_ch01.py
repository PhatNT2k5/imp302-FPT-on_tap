import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, story, traps, write  # noqa: E402

CHAIN = ["Histogram", "Kéo giãn tuyến tính", "Cân bằng histogram", "Trung bình nhiều ảnh", "Phép toán hình học", "Ngưỡng & Otsu", "Gán nhãn vùng", "Hình thái nhị phân"]
EX = "Ảnh chụp tế bào dưới kính hiển vi: tối, kém tương phản, có nhiễu — cần làm rõ rồi đếm xem có bao nhiêu tế bào"


def hist(values, labels, **extra):
    return {"bars": [{"label": lab, "value": v} for lab, v in zip(labels, values)], **extra}


LABEL_GRID = [["1", "1", "·", "2", "2", "·"], ["1", "·", "·", "·", "2", "·"], ["1", "1", "1", "1", "1*", "·"], ["·", "·", "·", "·", "·", "3"]]

stories = [
    intro("mo-dau", "Mở đầu: nền móng của mọi phép xử lý", "Ảnh kính hiển vi tối và kém tương phản", [
        P("Xin chào các bạn, chào mừng đến với môn xử lý ảnh và video. Chương một đặt nền móng cho cả môn. Ví dụ của chương: ảnh chụp tế bào dưới kính hiển vi, "
          "tối, kém tương phản và có nhiễu. Ta muốn làm rõ ảnh rồi đếm xem có bao nhiêu tế bào.", "Ví dụ: ảnh tế bào dưới kính hiển vi"),
        P("Ba nhóm phép toán trên ảnh xám. Phép toán điểm chỉ nhìn giá trị từng pixel. Phép toán số học kết hợp nhiều ảnh cùng kích thước. "
          "Phép toán hình học dời vị trí pixel mà không đổi giá trị.", "Điểm · số học · hình học"),
        P("Thử nghĩ: muốn đếm tế bào, máy cần biết pixel nào là tế bào, pixel nào là nền. Bắt đầu từ đâu?", "Pixel nào là tế bào?", ask=True),
    ], CHAIN, [
        P("Phần một: ảnh xám. Histogram, kéo giãn tuyến tính, cân bằng histogram, trung bình nhiều ảnh, và phép toán hình học.", "Ảnh xám"),
        P("Phần hai: ảnh nhị phân. Ngưỡng hóa và Otsu, gán nhãn vùng để đếm, và hình thái học để làm sạch hình dạng.", "Ảnh nhị phân"),
        P("Mỗi bước vá chỗ hụt của bước trước, các bạn xem theo thứ tự.", "Xem theo thứ tự"),
    ]),

    story("histogram", "Histogram ảnh", "method", [
        S("Vấn đề", "Ảnh tối đến mức nào?", [
            P("Trước khi sửa ảnh, cần một cách nhìn tổng quát: ảnh dùng những mức xám nào, nhiều hay ít.", "Ảnh dùng những mức xám nào?"),
        ]),
        S("Cách cũ", "Nhìn bằng mắt", [
            P("Nhìn bằng mắt chỉ cho cảm giác tối hay sáng, không cho con số để máy quyết định.", "Mắt: cảm giác, không phải số"),
        ]),
        S("Ý tưởng", "Đếm số pixel ở mỗi mức xám", [
            P("Histogram là hàm một chiều: với mỗi mức xám k từ không đến K trừ một, đếm có bao nhiêu pixel mang đúng mức đó.", "Đếm pixel mỗi mức k"),
            P("Giống thống kê điểm thi của một lớp: biết bao nhiêu bạn được mỗi mức điểm, nhưng không biết ai ngồi ở đâu.", "Như phổ điểm của lớp"),
        ]),
        S("Cách làm", "Histogram mất thông tin vị trí", [
            P("Ảnh bên trái là bàn cờ trắng đen xen kẽ. Ảnh bên phải chia đôi: nửa trên trắng, nửa dưới đen.", reveal=1),
            P("Thử đoán: hai ảnh này có cùng histogram không?", reveal=1, ask=True),
            P("Có. Cả hai có tám pixel trắng và tám pixel đen. Histogram chỉ đếm, không lưu vị trí, nên ảnh rất khác nhau vẫn có thể cùng histogram.", reveal=2),
        ], compare={"left": {"label": "Bàn cờ: 8 trắng, 8 đen", "grid": {"cells": [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]],
                                                                             "accent": [[r, c] for r in range(4) for c in range(4) if (r + c) % 2 == 0]}},
                    "right": {"label": "Chia đôi: 8 trắng, 8 đen", "grid": {"cells": [[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
                                                                              "accent": [[r, c] for r in range(2) for c in range(4)]}},
                    "arrow": "cùng histogram"}),
        S("So sánh", "Histogram cho biết gì, không cho biết gì", [
            P("Histogram cho biết phân bố độ sáng: ảnh tối, sáng, hay tương phản thấp.", reveal=[1]),
            P("Nó không cho biết vị trí pixel, nên không phân biệt được bàn cờ với ảnh chia đôi.", reveal=[2]),
        ], table={"headers": ["Histogram cho biết", "Histogram không cho biết"],
                  "rows": [["Ảnh tối hay sáng, dải mức xám", "Pixel nằm ở đâu"], ["Tương phản cao hay thấp", "Hình dạng, cấu trúc không gian"]]}),
        S("Ứng dụng", "Histogram ở đâu", [
            P("Slide nêu AOD, mật độ quang trung bình, một chỉ số đơn giản ước lượng tâm của phân bố mức xám, tức ảnh nhìn chung sáng hay tối.", "AOD: tâm phân bố mức xám"),
            P("Máy ảnh hiển thị histogram để người chụp biết ảnh có bị quá tối hay cháy sáng không.", "Máy ảnh hiển thị histogram"),
        ]),
        limit("Biết ảnh tối rồi, sửa thế nào?", [
            P("Histogram cho thấy ảnh tế bào chỉ dùng một dải mức xám hẹp. Video sau: kéo giãn tuyến tính.", "→ Kéo giãn tuyến tính"),
        ], CHAIN, 2),
        traps([["Histogram đếm gì?", "Số pixel có mỗi mức xám k"], ["Hai ảnh khác nhau có thể cùng histogram?", "Có: histogram mất thông tin vị trí"],
               ["AOD là gì?", "Mật độ quang trung bình: tâm phân bố mức xám"]],
              ["Bẫy một: histogram đếm số pixel ở mỗi mức xám.",
               "Bẫy hai: histogram không lưu vị trí, nên ảnh khác nhau có thể cùng histogram.",
               "Bẫy ba: AOD là mật độ quang trung bình, ước lượng tâm phân bố mức xám."]),
    ]),

    story("keo-gian", "Phép toán điểm tuyến tính và FSHS", "method", [
        S("Vấn đề", "Ảnh chỉ dùng dải 80 đến 150", [
            P("Histogram ảnh tế bào dồn trong dải tám mươi đến một trăm năm mươi, bỏ phí cả hai đầu không đến hai trăm năm mươi lăm. Ảnh xám đục, tế bào khó thấy.",
              "Dải 80–150: xám đục"),
        ]),
        S("Cách cũ", "Để nguyên ảnh", [
            P("Không xử lý thì các mức xám tế bào và nền quá gần nhau, mắt khó phân biệt.", "Tế bào và nền quá gần nhau"),
        ]),
        S("Ý tưởng", "Nhân rồi cộng", [
            P("Phép toán điểm tuyến tính: pixel mới bằng P nhân pixel cũ cộng L.", "g = P·f + L"),
            P("L dịch độ sáng lên hay xuống. P lớn hơn một giãn histogram, ảnh tương phản hơn; P nhỏ hơn một nén histogram.", "L: dịch sáng · P > 1: giãn"),
            P("FSHS, kéo giãn toàn dải, chọn P và L sao cho dải đang có phủ kín từ không đến K trừ một.", "FSHS: phủ kín 0 → K−1"),
        ]),
        S("Cách làm", "Kéo giãn 80–150 thành 0–255", [
            P("Trừ tám mươi rồi nhân hai trăm năm mươi lăm chia bảy mươi. Mức tám mươi thành không.", reveal=1),
            P("Thử đoán: mức một trăm mười lăm, chính giữa dải cũ, thành bao nhiêu?", reveal=1, ask=True),
            P("Một trăm hai mươi bảy phẩy năm, chính giữa dải mới. Mức một trăm năm mươi thành hai trăm năm mươi lăm. Histogram giãn ra phủ kín, tế bào nổi bật hơn hẳn.", reveal=2),
        ], compare={"left": {"label": "Trước: dồn trong 80–150", "histogram": hist([0, 0, 3, 8, 6, 2, 0, 0], ["0", "", "80", "", "", "150", "", "255"], top=8)},
                    "right": {"label": "Sau FSHS: phủ 0–255", "histogram": hist([3, 3, 4, 4, 3, 3, 2, 1], ["0", "", "", "", "", "", "", "255"], top=8)},
                    "arrow": "g = (f − 80) · 255 / 70"}),
        S("So sánh", "Offset L so với hệ số P", [
            P("L chỉ dịch histogram sang trái hay phải, không đổi độ rộng.", reveal=[1]),
            P("P đổi độ rộng: lớn hơn một giãn, nhỏ hơn một nén. FSHS chọn cả hai cho vừa khít dải.", reveal=[2, 3]),
        ], table={"headers": ["Tham số", "Tác dụng lên histogram", "Ảnh"],
                  "rows": [["L (offset)", "Dịch trái / phải", "Sáng lên / tối đi"], ["P > 1", "Giãn ra", "Tương phản hơn"], ["P < 1", "Nén lại", "Kém tương phản hơn"]]}),
        S("Ứng dụng", "Kéo giãn ở đâu", [
            P("Nút chỉnh độ sáng và độ tương phản trong mọi phần mềm ảnh chính là chỉnh L và P.", "Nút độ sáng, độ tương phản"),
        ]),
        limit("Khi dải đã đầy mà vẫn dồn cục", [
            P("Nếu ảnh có vài điểm cực tối và cực sáng, dải đã phủ từ không đến hai trăm năm mươi lăm nhưng phần lớn pixel vẫn dồn một chỗ. FSHS không đổi gì cả.",
              "Dải đầy nhưng dồn cục → FSHS vô dụng"),
            P("Video sau: cân bằng histogram.", "→ Cân bằng histogram"),
        ], CHAIN, 3),
        traps([["Phép toán điểm tuyến tính?", "g = P·f + L"], ["P > 1 làm gì?", "Giãn histogram, tăng tương phản"], ["FSHS?", "Kéo dải hiện có phủ kín 0 → K−1"]],
              ["Bẫy một: phép toán điểm tuyến tính là pixel mới bằng P nhân pixel cũ cộng L.",
               "Bẫy hai: P lớn hơn một giãn histogram; L chỉ dịch độ sáng.",
               "Bẫy ba: FSHS kéo dải mức xám hiện có phủ kín từ không đến K trừ một."]),
    ]),

    story("can-bang", "Phép toán phi tuyến và cân bằng histogram", "method", [
        S("Vấn đề", "Pixel dồn cục giữa dải đã đầy", [
            P("Ảnh tế bào có vài điểm bụi đen và vài điểm sáng chói, nên dải đã phủ kín, nhưng phần lớn pixel dồn vào một mức.", "Dải đầy, pixel dồn cục"),
        ]),
        S("Cách cũ", "FSHS", [
            P("FSHS chỉ kéo hai đầu dải ra hai biên. Dải đã đầy thì nó không làm gì.", "FSHS: dải đầy thì vô dụng"),
        ]),
        S("Ý tưởng", "Dùng chính histogram tích lũy làm hàm ánh xạ", [
            P("Phép toán phi tuyến: logarit nén vùng sáng, giãn vùng tối, hợp với ảnh dải động lớn như phổ Fourier.", "Logarit: nén sáng, giãn tối"),
            P("Cân bằng histogram: mức xám nào đông pixel thì được dành nhiều chỗ trên thang mới, đẩy các mức đông ra xa nhau. Hoàn toàn tự động, không cần chọn tham số.",
              "Mức đông pixel → được nhiều chỗ"),
        ]),
        S("Cách làm", "Bốn mức xám, mười sáu pixel", [
            P("Bước một, chuẩn hóa: số pixel ở bốn mức là hai, mười, hai, hai; chia mười sáu được không phẩy một hai lăm, không phẩy sáu hai lăm, và hai lần không phẩy một hai lăm.",
              reveal=1),
            P("Bước hai, tích lũy: không phẩy một hai lăm, không phẩy bảy lăm, không phẩy tám bảy lăm, một.", reveal=2),
            P("Thử đoán: mức một, mức đông nhất, sẽ được ánh xạ sang mức nào?", reveal=2, ask=True),
            P("Bước ba, nhân tích lũy với ba rồi làm tròn: mức không thành không, mức một thành hai, mức hai và ba thành ba. Mức đông bị đẩy lên giữa thang, tách xa mức tối.",
              reveal=[2, 3, 4]),
        ], table={"headers": ["Mức k", "Số pixel", "Chuẩn hóa", "Tích lũy", "Mức mới = round(3 · tích lũy)"],
                  "rows": [["0", "2", "0,125", "0,125", "0"], ["1", "10", "0,625", "0,75", "2"], ["2", "2", "0,125", "0,875", "3"], ["3", "2", "0,125", "1", "3"]]}),
        S("So sánh", "FSHS so với cân bằng histogram", [
            P("FSHS là tuyến tính, chỉ kéo hai đầu dải.", reveal=[1]),
            P("Cân bằng là phi tuyến, phân phối lại theo số pixel, cho histogram gần đồng đều hơn, kể cả khi dải đã đầy.", reveal=[2, 3]),
        ], table={"headers": ["", "FSHS", "Cân bằng histogram"],
                  "rows": [["Loại", "Tuyến tính", "Phi tuyến"], ["Dải đã đầy", "Không đổi gì", "Vẫn tách mức đông"], ["Tham số", "Từ min, max", "Tự động từ tích lũy"]]}),
        S("Ứng dụng", "Cân bằng histogram ở đâu", [
            P("Ảnh y tế, ảnh vệ tinh, ảnh camera thiếu sáng: tăng tương phản tự động trước khi người hoặc máy phân tích.", "Y tế, vệ tinh, thiếu sáng"),
        ]),
        limit("Tương phản tốt, nhưng nhiễu cũng rõ hơn", [
            P("Tăng tương phản làm cả nhiễu hạt cũng nổi rõ. Các phép toán điểm không phân biệt được tế bào với nhiễu.", "Nhiễu cũng nổi rõ"),
            P("Video sau dùng nhiều ảnh để giảm nhiễu: phép toán số học.", "→ Trung bình nhiều ảnh"),
        ], CHAIN, 4),
        traps([["Ba bước cân bằng histogram?", "Chuẩn hóa → tích lũy → dùng tích lũy làm ánh xạ"], ["Phép logarit làm gì?", "Nén vùng sáng, giãn vùng tối"],
               ["Cân bằng có cần chọn tham số?", "Không, tự động"]],
              ["Bẫy một: cân bằng histogram gồm chuẩn hóa, tính tích lũy chuẩn hóa, rồi dùng tích lũy làm hàm ánh xạ.",
               "Bẫy hai: logarit nén vùng sáng, giãn vùng tối, hợp với ảnh dải động lớn.",
               "Bẫy ba: cân bằng histogram hoàn toàn tự động."]),
    ]),

    story("trung-binh-anh", "Phép toán số học: trung bình nhiều ảnh", "method", [
        S("Vấn đề", "Nhiễu hạt trên ảnh tế bào", [
            P("Nhiễu đến từ nhiều nguồn: tán xạ bức xạ trước cảm biến, nhiễu điện tử trong camera, nhiễu kênh truyền, lỗi bit sau số hóa.", "Nhiều nguồn nhiễu"),
        ]),
        S("Cách cũ", "Chụp một lần", [
            P("Với một ảnh duy nhất, ta không phân biệt được phần nào là tế bào, phần nào là nhiễu.", "Một ảnh: không tách được nhiễu"),
        ]),
        S("Ý tưởng", "Chụp nhiều lần rồi lấy trung bình", [
            P("Chụp cùng cảnh nhiều lần. Tín hiệu không đổi qua các lần chụp, còn nhiễu thì ngẫu nhiên. Lấy trung bình từng pixel, nhiễu dương và âm triệt tiêu nhau.",
              "Tín hiệu giữ nguyên, nhiễu triệt tiêu"),
            P("Điều kiện: nhiễu có trung bình bằng không và độc lập giữa các lần chụp. Càng nhiều ảnh, nhiễu càng giảm.", "Điều kiện: trung bình 0, độc lập"),
        ]),
        S("Cách làm", "Bốn lần chụp một pixel", [
            P("Pixel thật bằng một trăm. Bốn lần chụp có nhiễu cộng tám, trừ sáu, cộng ba, trừ năm: ra một trăm lẻ tám, chín mươi tư, một trăm lẻ ba, chín mươi lăm.", reveal=1),
            P("Thử đoán: trung bình bốn lần chụp là bao nhiêu?", reveal=1, ask=True),
            P("Đúng một trăm: nhiễu đã triệt tiêu. Với nhiễu thật, kết quả không khít như vậy, nhưng càng nhiều ảnh càng gần giá trị thật.", reveal=2),
        ], grid=[{"label": "4 lần chụp (thật = 100)", "cells": [[108, 94, 103, 95]], "warn": [[0, 0], [0, 1], [0, 2], [0, 3]]},
                 {"label": "Trung bình", "cells": [[100]], "accent": [[0, 0]]}]),
        S("So sánh", "Các phép toán số học giữa ảnh", [
            P("Cộng và lấy trung bình: giảm nhiễu.", reveal=[1]), P("Trừ hai khung liên tiếp: phát hiện chuyển động, như tế bào đang bơi.", reveal=[2]),
        ], table={"headers": ["Phép", "Dùng để"], "rows": [["Cộng / trung bình", "Giảm nhiễu"], ["Trừ", "Phát hiện thay đổi, chuyển động"]]}),
        S("Ứng dụng", "Trung bình ảnh ở đâu", [
            P("Chụp thiên văn, chụp đêm trên điện thoại ghép nhiều khung, kính hiển vi huỳnh quang: đều lấy trung bình nhiều ảnh để giảm nhiễu.", "Thiên văn, chụp đêm, hiển vi"),
        ]),
        limit("Ảnh chụp lệch góc", [
            P("Nếu các lần chụp bị lệch hay xoay so với nhau, trung bình từng pixel sẽ làm nhòe. Phải dời ảnh về đúng vị trí trước.", "Lệch góc → phải dời ảnh"),
            P("Video sau: phép toán hình học.", "→ Phép toán hình học"),
        ], CHAIN, 5),
        traps([["Điều kiện trung bình hóa?", "Nhiễu trung bình 0, độc lập giữa các lần chụp"], ["Trừ hai ảnh dùng để?", "Phát hiện chuyển động"]],
              ["Bẫy một: trung bình hóa cần nhiễu có trung bình không và độc lập giữa các lần chụp.",
               "Bẫy hai: trừ hai khung liên tiếp dùng để phát hiện chuyển động."]),
    ]),

    story("hinh-hoc", "Phép toán hình học", "method", [
        S("Vấn đề", "Dời và xoay ảnh", [
            P("Các lần chụp lệch nhau vài pixel và hơi xoay. Ta cần dời và xoay ảnh cho khớp.", "Dời, xoay cho khớp"),
        ]),
        S("Cách cũ", "Phép toán điểm", [
            P("Phép toán điểm chỉ đổi giá trị pixel tại chỗ, không đổi vị trí.", "Đổi giá trị, không đổi vị trí"),
        ]),
        S("Ý tưởng", "Ánh xạ tọa độ rồi nội suy", [
            P("Phép toán hình học thay đổi quan hệ không gian giữa các pixel, như xoay, tịnh tiến, biến đổi phối cảnh, mà không đổi giá trị mức xám.",
              "Đổi vị trí, không đổi mức xám"),
            P("Hai bước: ánh xạ tọa độ từ ảnh gốc sang ảnh mới, rồi nội suy các tọa độ không nguyên về lưới hàng cột.", "1. Ánh xạ · 2. Nội suy"),
        ]),
        S("Cách làm", "Một pixel sau khi xoay nhẹ", [
            P("Tịnh tiến là cộng một hằng số vào tọa độ; xoay là nhân tọa độ với ma trận xoay. Sau khi ánh xạ, phần lớn tọa độ mới không còn là số nguyên.",
              "Tịnh tiến: cộng · xoay: nhân ma trận"),
            P("Sau phép xoay, pixel ở hàng hai cột ba được ánh xạ tới tọa độ ba phẩy bốn và hai phẩy sáu, không phải số nguyên.", "(2, 3) → (3,4 ; 2,6)"),
            P("Thử đoán: nội suy lân cận gần nhất đưa nó về ô nào?", "Thử đoán: về ô nào?", ask=True),
            P("Làm tròn về ô gần nhất: hàng ba, cột ba. Nhanh nhất, nhưng cạnh có thể bị răng cưa.", "Nearest → (3, 3); có thể răng cưa"),
        ]),
        S("So sánh", "Phép toán điểm so với hình học", [
            P("Phép toán điểm đổi giá trị, giữ vị trí.", reveal=[1]), P("Phép toán hình học đổi vị trí, giữ giá trị, và cần nội suy.", reveal=[2]),
        ], table={"headers": ["", "Phép toán điểm", "Phép toán hình học"],
                  "rows": [["Đổi", "Giá trị mức xám", "Vị trí pixel"], ["Cần nội suy", "Không", "Có (tọa độ không nguyên)"]]}),
        S("Ứng dụng", "Phép toán hình học ở đâu", [
            P("Căn chỉnh nhiều ảnh trước khi ghép hay lấy trung bình, xoay ảnh tài liệu bị nghiêng, sửa méo phối cảnh.", "Căn chỉnh, xoay tài liệu, sửa phối cảnh"),
        ]),
        limit("Ảnh đẹp rồi, giờ đếm tế bào", [
            P("Ảnh đã rõ, sạch và thẳng. Để đếm tế bào, trước hết phải quyết định pixel nào là tế bào, pixel nào là nền. Phần hai: ảnh nhị phân.", "→ Ngưỡng hóa"),
        ], CHAIN, 6),
        traps([["Phép toán hình học đổi gì?", "Vị trí pixel, không đổi giá trị"], ["Hai bước?", "Ánh xạ tọa độ, rồi nội suy"], ["Nội suy đơn giản nhất?", "Lân cận gần nhất"]],
              ["Bẫy một: phép toán hình học đổi vị trí pixel, không đổi giá trị cường độ.",
               "Bẫy hai: gồm hai bước, ánh xạ tọa độ rồi nội suy.",
               "Bẫy ba: nội suy đơn giản nhất là lân cận gần nhất."]),
    ]),

    story("nguong-otsu", "Ngưỡng hóa và phương pháp Otsu", "method", [
        S("Vấn đề", "Pixel nào là tế bào?", [
            P("Để đếm, ta cần ảnh nhị phân: tế bào là một, nền là không. Ảnh nhị phân mỗi pixel chỉ một bit, xử lý cực nhanh bằng phép logic.", "Ảnh nhị phân: 1 bit, phép logic"),
        ]),
        S("Cách cũ", "Chọn ngưỡng bằng tay", [
            P("Ngưỡng hóa so mỗi pixel với ngưỡng T: lớn hơn thì một, còn lại không. Nhưng T chọn tay thì mỗi ảnh một kiểu, và kết quả rất nhạy với T.", "Chọn T bằng tay: nhạy"),
        ]),
        S("Ý tưởng", "Chọn ngưỡng tách hai lớp xa nhau nhất", [
            P("Otsu thử mọi ngưỡng t. Mỗi t chia pixel thành hai lớp, nền và vật thể.", "Thử mọi ngưỡng t"),
            P("Ngưỡng tối ưu là ngưỡng làm phương sai giữa hai lớp lớn nhất: hai lớp vừa đông vừa xa nhau.", "Max phương sai giữa hai lớp"),
        ]),
        S("Cách làm", "Histogram có hai đỉnh", [
            P("Mười bốn pixel trên tám mức xám: một đỉnh tối quanh mức hai, một đỉnh sáng quanh mức sáu.", reveal=0),
            P("Thử đoán: ngưỡng nên đặt ở đâu?", reveal=0, ask=True),
            P("Otsu cho ngưỡng bằng bốn: dưới bốn là nền, từ bốn trở lên là tế bào, đúng thung lũng giữa hai đỉnh.", reveal=1),
        ], histogram=hist([0, 2, 4, 1, 0, 1, 4, 2], [str(v) for v in range(8)], lines=[{"at": 4, "label": "T = 4", "step": 1}],
                          caption="Histogram 14 pixel, mức 0–7")),
        S("Cách làm", "Phương sai giữa hai lớp theo từng ngưỡng", [
            P("Ngưỡng hai: lớp tối quá ít, phương sai giữa lớp chỉ một phẩy năm.", reveal=1),
            P("Ngưỡng ba: tăng lên bốn phẩy không tám.", reveal=2),
            P("Ngưỡng bốn và năm: lớn nhất, bốn phẩy năm chín. Hai ngưỡng bằng nhau vì mức bốn không có pixel nào.", reveal=3),
            P("Ngưỡng sáu và bảy giảm lại. Vậy chọn ngưỡng bốn.", reveal=4),
        ], table={"headers": ["Ngưỡng t", "2", "3", "4", "5", "6", "7"],
                  "rows": [["ω₀ (tỉ lệ lớp tối)", "0,14", "0,43", "0,50", "0,50", "0,57", "0,86"], ["μ₀ / μ₁", "1 / 4,5", "1,67 / 5,75", "1,86 / 6,14", "1,86 / 6,14", "2,25 / 6,33", "3,5 / 7"],
                           ["σ²B (giữa hai lớp)", "1,50", "4,08", "4,59 ✓", "4,59 ✓", "4,08", "1,50"], ["Kết luận", "", "", "Chọn T = 4", "", "", ""]]}),
        S("So sánh", "Ngưỡng tay so với Otsu", [
            P("Ngưỡng tay phụ thuộc người chọn.", reveal=[1]), P("Otsu tự động, chọn theo phương sai giữa hai lớp lớn nhất.", reveal=[2]),
        ], table={"headers": ["", "Ngưỡng chọn tay", "Otsu"],
                  "rows": [["Cách chọn T", "Thử bằng mắt", "Max phương sai giữa hai lớp"], ["Tự động", "Không", "Có"]]}),
        S("Ứng dụng", "Ngưỡng hóa ở đâu", [
            P("Ưu điểm: giảm mạnh dung lượng, đơn giản hóa dữ liệu, làm nổi vật so với nền. Nhược điểm: mất chi tiết gradient, nhạy với ngưỡng, kém với ảnh sáng thay đổi từ từ.",
              "Gọn, nổi vật · mất chi tiết, nhạy T"),
            P("Quét tài liệu thành đen trắng, tách tế bào, tách vật trên băng chuyền.", "Tài liệu, tế bào, băng chuyền"),
        ]),
        limit("Có ảnh nhị phân, nhưng bao nhiêu tế bào?", [
            P("Ảnh nhị phân chỉ cho biết pixel nào là tế bào, chưa cho biết pixel nào thuộc tế bào nào. Video sau: gán nhãn vùng.", "→ Gán nhãn vùng"),
        ], CHAIN, 7),
        traps([["Otsu chọn ngưỡng theo gì?", "Phương sai GIỮA hai lớp LỚN nhất"], ["Ngưỡng hóa gán 1 khi nào?", "Pixel > T"],
               ["Nhược điểm ngưỡng hóa?", "Mất chi tiết, nhạy T, kém với sáng thay đổi từ từ"]],
              ["Bẫy một: Otsu chọn ngưỡng làm phương sai giữa hai lớp lớn nhất. Nhớ chữ giữa và chữ lớn nhất.",
               "Bẫy hai: pixel lớn hơn ngưỡng thì gán một.",
               "Bẫy ba: ngưỡng hóa mất chi tiết gradient và rất nhạy với ngưỡng."]),
    ]),

    story("gan-nhan", "Gán nhãn vùng", "method", [
        S("Vấn đề", "Đếm số tế bào", [
            P("Ảnh nhị phân có nhiều cụm pixel trắng. Mỗi cụm liền nhau là một tế bào. Cần đánh số từng cụm để đếm.", "Đánh số từng cụm liền nhau"),
        ]),
        S("Cách cũ", "Ảnh nhị phân chưa có nhãn", [
            P("Ảnh nhị phân chỉ có không và một, không biết hai pixel trắng có thuộc cùng một tế bào hay không.", "Không biết pixel thuộc cụm nào"),
        ]),
        S("Ý tưởng", "Quét và kế thừa nhãn từ hàng xóm", [
            P("Quét từ trái sang phải, trên xuống dưới. Với mỗi pixel một, nhìn pixel bên trái và bên trên.", "Nhìn trái và trên"),
            P("Cả hai là nền: gán nhãn mới. Một bên có nhãn: kế thừa nhãn đó. Hai bên có nhãn khác nhau: ghi nhận hai nhãn tương đương.", "Mới · kế thừa · tương đương"),
        ]),
        S("Cách làm", "Gán nhãn một ảnh nhỏ", [
            P("Hàng đầu: hai pixel bên trái nhận nhãn một. Hai pixel tiếp theo không nối với nhãn một, nên nhận nhãn mới là hai.", reveal=1),
            P("Hàng hai và hàng ba kế thừa nhãn từ bên trên và bên trái, dần nối thành hình chữ U.", reveal=1),
            P("Thử đoán: ô có dấu sao, bên trái là nhãn một, bên trên là nhãn hai, thì sao?", reveal=1, ask=True),
            P("Gán nhãn một và ghi nhận một tương đương hai: thật ra cùng một vật hình chữ U. Pixel lẻ ở góc dưới nhận nhãn ba. Gộp tương đương, ta đếm được hai vật.",
              reveal=1),
        ], grid={"label": "Nhãn sau lượt quét; * = chỗ ghi nhận 1 ≡ 2", "cells": LABEL_GRID, "warn": [[2, 4]],
                 "accent": [[0, 0], [0, 1], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3]]}),
        S("So sánh", "Ba trường hợp khi gặp pixel 1", [
            P("Trái và trên đều là nền: nhãn mới.", reveal=[1]), P("Một bên có nhãn: kế thừa.", reveal=[2]),
            P("Hai bên khác nhãn: lấy một nhãn, ghi nhận tương đương, gộp ở cuối.", reveal=[3]),
        ], table={"headers": ["Trái / trên", "Hành động"],
                  "rows": [["Cả hai là nền", "Gán nhãn mới"], ["Một bên có nhãn", "Kế thừa nhãn đó"], ["Hai nhãn khác nhau", "Ghi nhận tương đương, gộp sau"]]}),
        S("Ứng dụng", "Gán nhãn vùng ở đâu", [
            P("Đếm tế bào, đếm hạt, đếm xe; đo diện tích từng vật; là bước trước khi trích đặc trưng ở chương mười.", "Đếm vật, đo diện tích"),
        ]),
        limit("Đốm nhiễu cũng bị đếm", [
            P("Một đốm nhiễu nhỏ cũng nhận một nhãn và bị đếm như tế bào. Tế bào có lỗ thủng có thể bị tách đôi. Cần làm sạch hình dạng trước.", "Nhiễu bị đếm nhầm"),
            P("Video sau: hình thái học ảnh nhị phân.", "→ Hình thái học"),
        ], CHAIN, 8),
        traps([["Gán nhãn xét pixel nào?", "Bên trái và bên trên"], ["Hai nhãn khác nhau gặp nhau?", "Ghi nhận tương đương"], ["Thứ tự quét?", "Trái → phải, trên → dưới"]],
              ["Bẫy một: thuật toán xét pixel bên trái và bên trên.",
               "Bẫy hai: hai nhãn khác nhau gặp nhau thì ghi nhận tương đương, vì cùng một vật.",
               "Bẫy ba: quét từ trái sang phải, từ trên xuống dưới."]),
    ]),

    story("hinh-thai", "Hình thái học ảnh nhị phân", "method", [
        S("Vấn đề", "Đốm nhiễu và lỗ thủng", [
            P("Ảnh nhị phân của tế bào có đốm nhiễu nhỏ trên nền và lỗ thủng trong tế bào.", "Đốm nhiễu, lỗ thủng"),
        ]),
        S("Cách cũ", "Đếm thẳng", [
            P("Đếm thẳng thì đốm nhiễu bị tính là tế bào, lỗ thủng có thể tách một tế bào làm hai.", "Đếm sai"),
        ]),
        S("Ý tưởng", "Phép logic qua cửa sổ trượt", [
            P("Hình thái học nhị phân dùng các toán tử logic NOT, AND, OR và MAJ, tức phép đa số, áp qua một cửa sổ trượt.", "NOT, AND, OR, MAJ qua cửa sổ"),
            P("Erosion co vật, loại pixel biên. Dilation giãn vật, thêm pixel biên. Opening là erosion rồi dilation; closing là dilation rồi erosion.",
              "Erosion co · dilation giãn"),
        ]),
        S("Cách làm", "Closing lấp một lỗ thủng", [
            P("Một hàng có lỗ thủng một pixel giữa tế bào: không, một, một, không, một, một, không.", reveal=1),
            P("Dilation, OR qua cửa sổ ba: lỗ được lấp, nhưng tế bào cũng phình ra tới mép.", reveal=2),
            P("Thử đoán: erosion tiếp theo, AND qua cửa sổ ba, cho gì?", reveal=2, ask=True),
            P("Hai mép co về như cũ, lỗ vẫn được lấp: không, một, một, một, một, một, không. Đó là closing.", reveal=3),
        ], grid=[{"label": "Gốc: có lỗ", "cells": [[0, 1, 1, 0, 1, 1, 0]], "accent": [[0, 1], [0, 2], [0, 4], [0, 5]], "warn": [[0, 3]]},
                 {"label": "Dilation (OR)", "cells": [[1, 1, 1, 1, 1, 1, 1]], "accent": [[0, c] for c in range(7)]},
                 {"label": "Erosion (AND) → closing", "cells": [[0, 1, 1, 1, 1, 1, 0]], "accent": [[0, c] for c in range(1, 6)]}]),
        S("So sánh", "Opening và closing", [
            P("Opening, erosion rồi dilation, xóa đốm nhiễu nhỏ, giữ hình vật lớn.", reveal=[1]),
            P("Closing, dilation rồi erosion, lấp lỗ và khe nhỏ. Mẹo nhớ: opening mở ra để xóa đốm, closing đóng lại để lấp lỗ.", reveal=[2]),
        ], table={"headers": ["Phép", "Thứ tự", "Tác dụng"],
                  "rows": [["Opening", "Erosion → dilation", "Xóa đốm nhỏ"], ["Closing", "Dilation → erosion", "Lấp lỗ, khe nhỏ"]]}),
        S("Ứng dụng", "Hình thái học ở đâu", [
            P("Làm sạch ảnh nhị phân trước khi đếm và đo, trong kính hiển vi, kiểm tra linh kiện, nhận dạng chữ.", "Làm sạch trước khi đếm"),
        ]),
        limit("Xong nền móng", [
            P("Giờ ta đếm đúng số tế bào. Chương hai mở rộng sang lọc ảnh: không chỉ nhìn từng pixel mà nhìn cả vùng lân cận.", "→ Chương 2: lọc ảnh"),
        ], CHAIN, 8),
        traps([["Opening là gì?", "Erosion rồi dilation: xóa đốm"], ["Closing là gì?", "Dilation rồi erosion: lấp lỗ"], ["MAJ là phép gì?", "Phép đa số"]],
              ["Bẫy một: opening là erosion rồi dilation, dùng để xóa đốm nhỏ.",
               "Bẫy hai: closing là dilation rồi erosion, dùng để lấp lỗ.",
               "Bẫy ba: MAJ là phép đa số."]),
    ]),

    story("tong-ket", "Tổng kết chương 1", "summary", [
        S("Tổng kết", "Nền móng trong một mạch", [
            P("Nhìn lại ảnh tế bào. Histogram cho biết phân bố độ sáng; FSHS kéo giãn dải; cân bằng histogram phân phối lại khi dải đã đầy."),
            P("Trung bình nhiều ảnh giảm nhiễu; phép toán hình học dời và xoay cho khớp."),
            P("Ngưỡng hóa và Otsu tạo ảnh nhị phân; hình thái học làm sạch; gán nhãn vùng đếm số tế bào."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: phép toán hình học đổi vị trí, không đổi giá trị."), P("Hai: histogram mất thông tin vị trí."),
            P("Ba: cân bằng histogram dùng tích lũy làm ánh xạ."), P("Bốn: Otsu chọn phương sai giữa hai lớp lớn nhất."),
            P("Năm: opening xóa đốm, closing lấp lỗ."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Phép toán hình học?", "Đổi vị trí, giữ giá trị"], ["Histogram?", "Mất vị trí"], ["Cân bằng histogram?", "Tích lũy làm ánh xạ"],
                           ["Otsu?", "Max phương sai giữa hai lớp"], ["Opening / closing?", "Xóa đốm / lấp lỗ"]]}),
        S("Tổng kết", "Sang chương 2", [
            P("Chương hai: lọc ảnh, nhìn cả vùng lân cận của mỗi pixel.", "Chương 2: lọc ảnh"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–3", "Ảnh tế bào tối, nhiễu; cần đếm", "—", "Ba nhóm phép toán", "→ Histogram"],
    ["Histogram", "4–5", "Ảnh tối đến mức nào", "Nhìn bằng mắt", "Đếm pixel mỗi mức; mất vị trí; AOD", "→ Kéo giãn"],
    ["Kéo giãn", "6–9", "Dải 80–150", "Để nguyên", "g = P·f + L; FSHS", "Dải đầy, dồn cục → cân bằng"],
    ["Cân bằng histogram", "10", "Dồn cục giữa dải đầy", "FSHS", "Log; tích lũy làm ánh xạ", "Nhiễu nổi rõ → trung bình ảnh"],
    ["Trung bình ảnh", "11–13", "Nhiễu hạt", "Chụp một lần", "Trung bình nhiều lần chụp", "Lệch góc → hình học"],
    ["Phép toán hình học", "14–18", "Dời, xoay", "Phép toán điểm", "Ánh xạ tọa độ + nội suy", "→ Ngưỡng hóa"],
    ["Ngưỡng & Otsu", "19–24", "Pixel nào là tế bào", "Ngưỡng tay", "Max phương sai giữa hai lớp", "Chưa đếm → gán nhãn"],
    ["Gán nhãn vùng", "25–27", "Đếm tế bào", "Ảnh nhị phân chưa nhãn", "Quét, kế thừa, tương đương", "Nhiễu bị đếm → hình thái"],
    ["Hình thái nhị phân", "28–31", "Đốm, lỗ", "Đếm thẳng", "NOT/AND/OR/MAJ; opening, closing", "→ Chương 2"],
    ["Tổng kết", "—", "—", "—", "Bẫy chung", "→ Chương 2"],
]
write(1, "Xử lý ảnh cơ bản", EX, stories, MAP)
