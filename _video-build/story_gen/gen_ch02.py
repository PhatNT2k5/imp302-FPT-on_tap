import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, pipeline, story, traps, write  # noqa: E402

CHAIN = ["Tích chập & lọc hộp", "Lọc Gauss", "Lọc trung vị", "Hình thái học", "Làm nét", "Lọc miền tần số"]
EX = "Ảnh chụp một trang sách bằng điện thoại: nhiễu hạt, vài điểm lấm tấm, chữ hơi nhòe — làm sạch mà vẫn giữ nét chữ"


def hist(values, labels, **extra):
    return {"bars": [{"label": lab, "value": v} for lab, v in zip(labels, values)], **extra}


def row(cells, label, accent=None, warn=None):
    grid = {"label": label, "cells": [cells]}
    if accent:
        grid["accent"] = [[0, c] for c in accent]
    if warn:
        grid["warn"] = [[0, c] for c in warn]
    return grid


stories = [
    intro("mo-dau", "Mở đầu: làm sạch mà vẫn giữ nét", "Trang sách chụp bằng điện thoại", [
        P("Chào các bạn. Chương hai là lọc ảnh, nền tảng của tăng cường, khử nhiễu, làm nét và trích đặc trưng. Ví dụ của cả chương: một trang sách chụp bằng điện thoại.",
          "Ví dụ: trang sách chụp bằng điện thoại"),
        P("Ảnh có nhiễu hạt li ti, vài điểm lấm tấm trắng đen, và chữ hơi nhòe. Ta muốn làm sạch mà vẫn giữ nét chữ.", "Nhiễu hạt, điểm lấm tấm, chữ nhòe"),
        P("Thử nghĩ: làm mờ ảnh thì nhiễu giảm, nhưng chữ cũng mờ theo. Có cách nào chỉ xóa nhiễu mà giữ cạnh?", "Xóa nhiễu mà giữ cạnh?", ask=True),
    ], CHAIN, [
        P("Ta bắt đầu với lọc tuyến tính: tích chập và lọc hộp, rồi lọc Gauss. Sau đó là lọc phi tuyến: trung vị và hình thái học.", "Tuyến tính → phi tuyến"),
        P("Tiếp theo là làm nét bằng đạo hàm và unsharp masking, và cuối cùng là lọc trong miền tần số.", "Làm nét → miền tần số"),
        P("Mỗi bộ lọc vá chỗ hụt của bộ lọc trước, các bạn xem theo thứ tự.", "Xem theo thứ tự"),
    ]),

    story("tich-chap", "Lọc không gian: tích chập và lọc hộp", "method", [
        S("Vấn đề", "Nhiễu hạt khắp trang", [
            P("Mỗi pixel nền giấy lệch đi một chút ngẫu nhiên. Ta muốn kéo mỗi pixel về gần giá trị của hàng xóm.", "Kéo pixel về gần hàng xóm"),
        ]),
        S("Cách cũ", "Xử lý từng pixel riêng lẻ", [
            P("Ở chương một, phép toán điểm chỉ nhìn chính pixel đó. Nó không biết hàng xóm, nên không phân biệt được nhiễu với chi tiết thật.", "Phép toán điểm: không biết hàng xóm"),
        ]),
        S("Ý tưởng", "Thay pixel bằng một hàm của vùng lân cận", [
            P("Lọc không gian thay mỗi pixel bằng một hàm của chính nó và các pixel lân cận. Hàm tuyến tính thì gọi là lọc không gian tuyến tính.", "Hàm của vùng lân cận"),
            P("Một hệ tuyến tính thỏa tính cộng và tính đồng nhất. Nếu còn bất biến theo không gian, gọi là hệ LSI, đầu ra là tích chập ảnh vào với đáp ứng xung.",
              "LSI: đầu ra = tích chập với đáp ứng xung"),
        ]),
        S("Cách làm", "Tương quan và tích chập", [
            P("Tương quan trượt tâm kernel qua ảnh, tính tổng các tích. Tích chập giống hệt, nhưng kernel xoay một trăm tám mươi độ.", reveal=1),
            P("Thử với một xung đơn vị: không, không, một, không, không, và kernel một, hai, ba.", reveal=1),
            P("Thử đoán: tương quan cho ra dãy nào?", reveal=1, ask=True),
            P("Tương quan cho không, ba, hai, một, không: kernel hiện ra bị lật ngược.", reveal=2),
            P("Tích chập cho không, một, hai, ba, không: đúng kernel. Vì vậy đáp ứng xung của hệ LSI chính là kernel tích chập. Kernel đối xứng thì hai phép cho cùng kết quả.",
              reveal=3),
        ], grid=[row([0, 0, 1, 0, 0], "Xung đơn vị", accent=[2]), row([0, 3, 2, 1, 0], "Tương quan với 1, 2, 3", warn=[1, 2, 3]),
                 row([0, 1, 2, 3, 0], "Tích chập với 1, 2, 3", accent=[1, 2, 3])]),
        S("Cách làm", "Lọc hộp", [
            P("Bộ lọc làm mượt đơn giản nhất là lọc hộp: lấy trung bình cộng cửa sổ. Kernel chuẩn hóa tổng hệ số bằng một, để không đổi độ sáng tổng thể.",
              "Box filter: trung bình, tổng hệ số = 1"),
            P("Nhiễu hạt bị trung bình hóa và giảm hẳn.", "Nhiễu hạt giảm"),
        ]),
        S("So sánh", "Tương quan so với tích chập", [
            P("Tương quan không lật kernel; tích chập lật kernel một trăm tám mươi độ.", reveal=[1]),
            P("Với xung đơn vị, tích chập trả lại đúng kernel. Kernel đối xứng qua tâm thì hai phép như nhau.", reveal=[2, 3]),
        ], table={"headers": ["", "Tương quan", "Tích chập"],
                  "rows": [["Kernel", "Giữ nguyên", "Xoay 180°"], ["Với xung đơn vị", "Kernel bị lật", "Đúng kernel"], ["Kernel đối xứng", "Như nhau", "Như nhau"]]}),
        S("Ứng dụng", "Tích chập ở đâu", [
            P("Mọi bộ lọc tuyến tính, từ làm mờ, làm nét đến phát hiện cạnh, và cả lớp tích chập trong mạng CNN, đều là phép tổng tích này.", "Mọi bộ lọc tuyến tính, CNN"),
        ]),
        limit("Lọc hộp làm mờ có góc cạnh", [
            P("Lọc hộp đối xử mọi hàng xóm như nhau, dù gần hay xa, và cắt đột ngột ở mép cửa sổ. Chữ bị mờ khá thô.", "Mọi hàng xóm như nhau, cắt đột ngột"),
            P("Video sau: lọc Gauss, hàng xóm gần quan trọng hơn hàng xóm xa.", "→ Gauss"),
        ], CHAIN, 2),
        traps([["Tích chập khác tương quan?", "Kernel xoay 180°"], ["Khi nào hai phép như nhau?", "Kernel đối xứng qua tâm"],
               ["Vì sao chuẩn hóa kernel?", "Tổng hệ số = 1, giữ độ sáng"]],
              ["Bẫy một: tích chập giống tương quan nhưng kernel xoay một trăm tám mươi độ.",
               "Bẫy hai: kernel đối xứng qua tâm thì hai phép cho cùng kết quả.",
               "Bẫy ba: kernel làm mượt được chuẩn hóa tổng bằng một để giữ độ sáng."]),
    ]),

    story("gauss", "Lọc thông thấp lý tưởng và lọc Gauss", "method", [
        S("Vấn đề", "Làm mượt mà không sinh viền lạ", [
            P("Ta muốn bỏ các thành phần tần số cao, tức nhiễu hạt, mà không sinh ra những viền lặp lại quanh chữ.", "Bỏ tần số cao, không sinh viền"),
        ]),
        S("Cách cũ", "Lọc lý tưởng: cắt phắt", [
            P("Bộ lọc thông thấp lý tưởng giữ nguyên mọi tần số trong một ngưỡng cắt, ép toàn bộ tần số ngoài ngưỡng về không, vùng giữ hình tròn hoặc chữ nhật.",
              "Giữ trong ngưỡng, ép về 0 ngoài ngưỡng"),
            P("Nhưng bước cắt đột ngột trong miền tần số gây gợn sóng, ringing, trong miền không gian: các viền lặp lại quanh cạnh chữ.", "Cắt đột ngột → ringing"),
        ]),
        S("Ý tưởng", "Giảm dần thay vì cắt phắt", [
            P("Bộ lọc Gauss có đáp ứng tần số cũng là hình Gauss, giảm dần mượt mà, nên không gây ringing.", "Gauss: giảm dần, không ringing"),
            P("Trong không gian, hàng xóm càng gần trọng số càng lớn. Tham số sigma lớn thì lọc mạnh, ảnh mờ hơn; sigma nhỏ chỉ khử nhiễu mịn.",
              "σ lớn → mờ hơn"),
        ]),
        S("Cách làm", "Đáp ứng tần số của hai bộ lọc", [
            P("Bên trái là bộ lọc lý tưởng với ngưỡng cắt ở tần số ba: giữ nguyên rồi rơi thẳng xuống không.", reveal=1),
            P("Thử đoán: bộ lọc Gauss với sigma bằng hai trông thế nào?", reveal=1, ask=True),
            P("Giảm dần: một, không phẩy tám tám, không phẩy sáu một, không phẩy ba hai, không phẩy một bốn, không phẩy không bốn. Không có vách đứng nào, nên không có gợn sóng.",
              reveal=2),
        ], compare={"left": {"label": "Lý tưởng: cắt phắt ở tần số 3", "histogram": hist([1, 1, 1, 0, 0, 0], ["0", "1", "2", "3", "4", "5"], top=1)},
                    "right": {"label": "Gauss σ = 2: giảm dần", "histogram": hist([1, 0.88, 0.61, 0.32, 0.14, 0.04], ["0", "1", "2", "3", "4", "5"], top=1)},
                    "arrow": "cùng mục tiêu"}),
        S("So sánh", "Lý tưởng so với Gauss", [
            P("Lý tưởng cắt đột ngột, gây ringing.", reveal=[1]), P("Gauss giảm dần, không ringing; độ mạnh chỉnh bằng sigma.", reveal=[2]),
        ], table={"headers": ["", "Lý tưởng", "Gauss"],
                  "rows": [["Đáp ứng tần số", "Vách đứng tại ngưỡng cắt", "Giảm dần hình chuông"], ["Ringing", "Có", "Không"]]}),
        S("Ứng dụng", "Gauss ở đâu", [
            P("Lọc Gauss là bước làm mượt mặc định trước khi phát hiện cạnh, giảm mẫu, hay xây kim tự tháp ảnh.", "Làm mượt trước khi xử lý tiếp"),
        ]),
        limit("Điểm lấm tấm bị lem chứ không mất", [
            P("Gauss và lọc hộp đều là trung bình có trọng số. Một điểm trắng lấm tấm không biến mất mà lem ra thành đốm mờ, và cạnh chữ cũng mờ theo.",
              "Nhiễu xung bị lem, cạnh mờ"),
            P("Video sau dùng lọc phi tuyến: trung vị.", "→ Trung vị"),
        ], CHAIN, 3),
        traps([["Lọc lý tưởng gây hiện tượng gì?", "Ringing (gợn sóng)"], ["Đáp ứng tần số của Gauss?", "Cũng là Gauss, giảm mượt"], ["σ lớn thì sao?", "Lọc mạnh, ảnh mờ hơn"]],
              ["Bẫy một: lọc lý tưởng gây ringing vì cắt đột ngột trong miền tần số.",
               "Bẫy hai: đáp ứng tần số của lọc Gauss cũng là hàm Gauss.",
               "Bẫy ba: sigma càng lớn, ảnh càng mờ."]),
    ]),

    story("trung-vi", "Lọc trung vị và trung vị có trọng số", "method", [
        S("Vấn đề", "Điểm lấm tấm trên nền giấy", [
            P("Trang sách có vài điểm trắng lấm tấm, là nhiễu xung. Ta muốn xóa sạch chúng mà không làm mờ nét chữ.", "Xóa nhiễu xung, giữ nét"),
        ]),
        S("Cách cũ", "Trung bình bị ngoại lai kéo lệch", [
            P("Bộ lọc trung bình bị giá trị ngoại lai kéo lệch: một điểm hai trăm năm mươi lăm giữa vùng mười làm cả vùng sáng lên.", "Ngoại lai kéo lệch trung bình"),
        ]),
        S("Ý tưởng", "Sắp xếp rồi chọn giữa", [
            P("Lọc trung vị sắp xếp các giá trị trong cửa sổ rồi chọn giá trị ở giữa. Ngoại lai nằm ở hai đầu dãy nên không ảnh hưởng.", "Sắp xếp, chọn giữa"),
            P("Lọc phi tuyến bảo toàn cạnh và chi tiết tốt hơn, ít bị nhiễu ảnh hưởng hơn lọc tuyến tính.", "Phi tuyến: giữ cạnh tốt hơn"),
        ]),
        S("Cách làm", "Cửa sổ có một điểm muối", [
            P("Cửa sổ năm giá trị: mười, mười hai, mười một, hai trăm năm mươi lăm, mười ba.", "Cửa sổ: 10, 12, 11, 255, 13", reveal=1),
            P("Trung bình cộng khoảng sáu mươi: ảnh bị lem một đốm sáng.", "Trung bình ≈ 60,2", reveal=1),
            P("Thử đoán: trung vị là bao nhiêu?", "Thử đoán: trung vị?", reveal=1, ask=True),
            P("Sắp xếp: mười, mười một, mười hai, mười ba, hai trăm năm mươi lăm. Giá trị giữa là mười hai, điểm nhiễu bị bỏ qua hoàn toàn.", "Trung vị = 12", reveal=2),
        ], grid=[row([10, 12, 11, 255, 13], "Cửa sổ", warn=[3]), row([10, 11, 12, 13, 255], "Sau sắp xếp", accent=[2], warn=[4])]),
        S("Cách làm", "Trung vị có trọng số", [
            P("Gán trọng số cho mỗi mẫu, ví dụ một, hai, ba, hai, một. Ngưỡng bằng nửa tổng trọng số, tức bốn phẩy năm.", reveal=1),
            P("Sắp xếp giảm dần rồi cộng dồn trọng số từ mẫu lớn nhất: hai trăm năm mươi lăm được hai, mười ba được ba.", reveal=2),
            P("Đến mười hai tổng thành năm, vượt bốn phẩy năm. Đầu ra là mười hai.", reveal=3),
        ], table={"headers": ["Mẫu (giảm dần)", "Trọng số", "Cộng dồn", "≥ 4,5?"],
                  "rows": [["255", "2", "2", "Chưa"], ["13", "1", "3", "Chưa"], ["12", "2", "5", "Đạt → đầu ra 12"]]}),
        S("So sánh", "Trung bình so với trung vị", [
            P("Trung bình là tuyến tính, bị ngoại lai kéo lệch, làm mờ cạnh.", reveal=[1]), P("Trung vị là phi tuyến, bỏ qua ngoại lai, giữ cạnh.", reveal=[2]),
        ], table={"headers": ["", "Trung bình", "Trung vị"],
                  "rows": [["Ví dụ 10, 12, 11, 255, 13", "≈ 60,2", "12"], ["Nhiễu xung", "Lem ra", "Xóa sạch"]]}),
        S("Ứng dụng", "Trung vị ở đâu", [
            P("Khử nhiễu muối tiêu, nhiễu hạt phim. Slide nêu thêm trung vị có trọng số để phóng to ảnh ít bị khối hơn nội suy tuyến tính, và để làm nét ảnh.",
              "Muối tiêu; phóng to ít khối; làm nét"),
        ]),
        limit("Cần hình dạng, không chỉ giá trị", [
            P("Trên ảnh nhị phân của chữ, ta còn muốn xóa đốm nhỏ, lấp lỗ trong nét chữ, nối chỗ đứt. Đó là bài toán về hình dạng.", "Bài toán hình dạng"),
            P("Video sau: hình thái học.", "→ Hình thái học"),
        ], CHAIN, 4),
        traps([["Trung vị hiệu quả với nhiễu gì?", "Nhiễu xung (muối tiêu)"], ["Ngưỡng trung vị có trọng số?", "Nửa tổng trọng số"],
               ["Lọc phi tuyến hơn tuyến tính ở đâu?", "Giữ cạnh, ít bị nhiễu ảnh hưởng"]],
              ["Bẫy một: lọc trung vị rất hiệu quả với nhiễu xung.",
               "Bẫy hai: trung vị có trọng số dùng ngưỡng bằng nửa tổng trọng số, cộng dồn từ mẫu lớn nhất.",
               "Bẫy ba: lọc phi tuyến giữ cạnh tốt hơn và ít bị nhiễu ảnh hưởng."]),
    ]),

    story("hinh-thai", "Lọc hình thái học", "method", [
        S("Vấn đề", "Đốm nhỏ, lỗ thủng, nét đứt", [
            P("Sau khi nhị phân hóa trang sách, có đốm đen nhỏ trên nền, lỗ thủng trong nét chữ, và nét bị đứt.", "Đốm, lỗ, nét đứt"),
        ]),
        S("Cách cũ", "Lọc theo giá trị", [
            P("Lọc tuyến tính hay trung vị xử lý giá trị pixel, không mô tả trực tiếp cấu trúc hình học như kích thước hay độ liền mạch của vật.", "Không mô tả hình dạng"),
        ]),
        S("Ý tưởng", "Thăm dò bằng một phần tử cấu trúc", [
            P("Hình thái học toán học là phương pháp phi tuyến dựa trên lý thuyết tập hợp và lý thuyết dàn, mô tả định lượng cấu trúc hình học của vật.", "Lý thuyết tập hợp, dàn"),
            P("Đặt một phần tử cấu trúc lên từng vị trí. Erosion chỉ giữ một nếu toàn bộ vùng bên dưới đều là một; dilation chỉ cần ít nhất một pixel bên dưới là một.",
              "Erosion: tất cả là 1 · Dilation: ít nhất một 1"),
        ]),
        S("Cách làm", "Opening trên một hàng nhị phân", [
            P("Hàng nhị phân: một khối ba pixel liền nhau, và một đốm nhiễu đơn lẻ ở bên phải. Phần tử cấu trúc rộng ba.", reveal=1),
            P("Erosion: chỉ pixel giữa khối còn đủ ba hàng xóm là một. Đốm nhiễu biến mất.", reveal=2),
            P("Thử đoán: dilation tiếp theo trả lại gì?", reveal=2, ask=True),
            P("Khối ba pixel trở về nguyên kích thước, đốm nhiễu thì không quay lại. Erosion rồi dilation là opening: xóa nhiễu nhỏ, giữ hình dạng.", reveal=3),
        ], grid=[row([0, 1, 1, 1, 0, 0, 1, 0], "Gốc: khối + đốm nhiễu", accent=[1, 2, 3], warn=[6]),
                 row([0, 0, 1, 0, 0, 0, 0, 0], "Erosion", accent=[2]), row([0, 1, 1, 1, 0, 0, 0, 0], "Dilation → opening", accent=[1, 2, 3])]),
        S("So sánh", "Bốn phép cơ bản", [
            P("Erosion co vật, xóa pixel biên. Dilation giãn vật, thêm pixel biên.", reveal=[1, 2]),
            P("Opening, erosion rồi dilation, xóa nhiễu nhỏ. Closing, dilation rồi erosion, lấp lỗ nhỏ và nối chỗ đứt.", reveal=[3, 4]),
        ], table={"headers": ["Phép", "Định nghĩa", "Tác dụng"],
                  "rows": [["Erosion", "Giữ 1 nếu tất cả bên dưới là 1", "Co vật"], ["Dilation", "Giữ 1 nếu có ít nhất một 1", "Giãn vật"],
                           ["Opening", "Erosion → dilation", "Xóa nhiễu nhỏ"], ["Closing", "Dilation → erosion", "Lấp lỗ, nối chỗ đứt"]]}),
        S("Ứng dụng", "Hình thái học ở đâu", [
            P("Làm sạch ảnh văn bản trước khi nhận dạng chữ, tách vật trong ảnh công nghiệp, phát hiện đặc trưng hình dạng.", "Làm sạch văn bản, ảnh công nghiệp"),
        ]),
        limit("Ảnh sạch nhưng chữ vẫn nhòe", [
            P("Khử nhiễu xong, nét chữ vẫn hơi nhòe. Giờ phải làm ngược lại: làm nét.", "→ Làm nét"),
        ], CHAIN, 5),
        traps([["Opening là gì?", "Erosion rồi dilation"], ["Closing dùng để làm gì?", "Lấp lỗ, nối chỗ đứt"], ["Erosion giữ 1 khi nào?", "Toàn bộ vùng dưới SE là 1"]],
              ["Bẫy một: opening là erosion rồi dilation; closing là dilation rồi erosion.",
               "Bẫy hai: closing lấp lỗ nhỏ và nối chỗ đứt; opening xóa nhiễu nhỏ.",
               "Bẫy ba: erosion chỉ giữ một khi toàn bộ vùng dưới phần tử cấu trúc là một."]),
    ]),

    story("lam-net", "Làm nét: đạo hàm, Laplacian và unsharp masking", "method", [
        S("Vấn đề", "Chữ nhòe, cạnh không sắc", [
            P("Cạnh chữ là chỗ cường độ thay đổi. Muốn làm nét, phải làm nổi những chỗ thay đổi đó.", "Làm nổi chỗ thay đổi"),
        ]),
        S("Cách cũ", "Lọc làm mượt", [
            P("Mọi bộ lọc đến giờ đều làm mượt, tức là xóa bớt thay đổi. Làm nét cần đúng chiều ngược lại.", "Làm mượt: xóa thay đổi"),
        ]),
        S("Ý tưởng", "Dùng đạo hàm để tìm chỗ thay đổi", [
            P("Đạo hàm bậc một bằng không ở vùng hằng số, khác không tại đầu bước nhảy và dọc theo độ dốc.", "Bậc một: khác 0 dọc độ dốc"),
            P("Đạo hàm bậc hai bằng không ở vùng hằng số và dọc độ dốc tuyến tính, chỉ khác không tại đầu và cuối thay đổi. Toán tử Laplacian dựa trên nó.",
              "Bậc hai: khác 0 tại đầu và cuối"),
        ]),
        S("Cách làm", "Đạo hàm trên một mép chữ", [
            P("Một mép chữ: mười, mười, mười, hai mươi, ba mươi, ba mươi, ba mươi. Một vùng phẳng, một dốc, rồi phẳng.", reveal=1),
            P("Đạo hàm bậc một: không, không, mười, mười, không, không. Khác không suốt dọc độ dốc.", reveal=2),
            P("Thử đoán: đạo hàm bậc hai khác không ở đâu?", reveal=2, ask=True),
            P("Chỉ ở đầu dốc, cộng mười, và cuối dốc, trừ mười; dọc dốc bằng không. Laplacian đánh dấu đúng hai mép của cạnh.", reveal=3),
        ], table={"headers": ["Vị trí", "f", "Bậc một", "Bậc hai"],
                  "rows": [["Phẳng", "10, 10, 10", "0, 0", "0"], ["Dốc", "10 → 20 → 30", "10, 10", "+10 (đầu), 0, −10 (cuối)"], ["Phẳng", "30, 30, 30", "0, 0", "0"]]}),
        S("Cách làm", "Unsharp masking và highboost", [
            P("Bước một: làm mờ ảnh gốc bằng lọc hộp ba điểm: mười, mười ba phẩy ba ba, hai mươi, hai mươi sáu phẩy sáu bảy, ba mươi.", reveal=[1]),
            P("Bước hai: lấy gốc trừ ảnh mờ được mặt nạ, chỉ còn thành phần tần số cao: âm ba phẩy ba ba ở đầu dốc, cộng ba phẩy ba ba ở cuối dốc.", reveal=[2]),
            P("Bước ba: cộng mặt nạ trở lại ảnh gốc: đầu dốc tối hơn, sáu phẩy sáu bảy; cuối dốc sáng hơn, ba mươi ba phẩy ba ba. Cạnh trông sắc hơn.", reveal=[3]),
            P("Nhân mặt nạ với hệ số lớn hơn một trước khi cộng là highboost, làm nét mạnh hơn.", reveal=[4]),
        ], code={"lines": ["mờ ← lọc_hộp(f)                 # 10; 13,33; 20; 26,67; 30", "mặt_nạ ← f − mờ                 # 0; −3,33; 0; +3,33; 0",
                           "nét ← f + mặt_nạ                # 10; 6,67; 20; 33,33; 30", "highboost: nét ← f + k·mặt_nạ, k > 1"]}),
        S("So sánh", "Bậc một, bậc hai và unsharp", [
            P("Đạo hàm bậc một phản ứng suốt dọc độ dốc.", reveal=[1]), P("Đạo hàm bậc hai, Laplacian, chỉ phản ứng ở đầu và cuối, cho cạnh mảnh hơn.", reveal=[2]),
            P("Unsharp masking dùng ảnh mờ để lấy phần chi tiết rồi cộng lại.", reveal=[3]),
        ], table={"headers": ["Kỹ thuật", "Phản ứng ở", "Ghi chú"],
                  "rows": [["Đạo hàm bậc một", "Dọc độ dốc", "Gradient"], ["Đạo hàm bậc hai", "Đầu và cuối thay đổi", "Laplacian"],
                           ["Unsharp / highboost", "Chỗ gốc khác ảnh mờ", "k > 1 là highboost"]]}),
        S("Ứng dụng", "Làm nét ở đâu", [
            P("Chế độ làm nét trong phần mềm chỉnh ảnh, máy in và máy quét tài liệu thường là unsharp masking.", "Phần mềm ảnh, máy quét"),
        ]),
        limit("Kernel lớn thì tính chậm", [
            P("Lọc với kernel lớn trong không gian rất tốn phép tính, và thiết kế đúng đáp ứng tần số mong muốn bằng kernel là khó.", "Kernel lớn: chậm, khó thiết kế"),
            P("Video sau: lọc thẳng trong miền tần số.", "→ Miền tần số"),
        ], CHAIN, 6),
        traps([["Đạo hàm bậc hai dọc độ dốc tuyến tính?", "Bằng 0"], ["Mặt nạ unsharp là gì?", "Ảnh gốc − ảnh mờ"], ["Highboost?", "Nhân mặt nạ với k > 1"]],
              ["Bẫy một: đạo hàm bậc hai bằng không dọc độ dốc tuyến tính, khác không ở đầu và cuối thay đổi.",
               "Bẫy hai: mặt nạ unsharp bằng ảnh gốc trừ ảnh mờ.",
               "Bẫy ba: highboost là nhân mặt nạ với hệ số lớn hơn một."]),
    ]),

    story("mien-tan-so", "Lọc trong miền tần số", "method", [
        S("Vấn đề", "Thiết kế bộ lọc theo tần số", [
            P("Ta muốn nói thẳng: giữ tần số thấp đến mức này, bỏ tần số cao từ mức kia. Làm vậy bằng kernel không gian vừa khó vừa chậm.", "Muốn thiết kế theo tần số"),
        ]),
        S("Cách cũ", "Tích chập trong không gian", [
            P("Kernel lớn tốn rất nhiều phép nhân cho mỗi pixel.", "Kernel lớn: tốn kém"),
        ]),
        S("Ý tưởng", "Tích chập thành phép nhân", [
            P("Tích chập trong không gian tương ứng với phép nhân trong miền tần số. Chuyển sang tần số, lọc chỉ còn là nhân từng phần tử.", "Tích chập ⇔ nhân"),
            P("DFT hai chiều và IDFT chuyển ảnh qua lại. Dạng cực cho phổ biên độ và góc pha; phổ công suất là biên độ bình phương. Gần tâm phổ là tần số thấp, xa tâm là tần số cao.",
              "Phổ biên độ, pha; công suất = biên độ²"),
        ]),
        S("Cách làm", "Các bước lọc trong miền tần số", [
            P("Đệm ảnh, bằng số không, phản chiếu hoặc lặp biên, để tránh hiệu ứng bao quanh khi tích chập tuần hoàn.", "1. Đệm ảnh", reveal=1),
            P("Nhân ảnh với trừ một mũ x cộng y để dời tâm phổ, rồi tính DFT.", "2. Dời tâm, DFT", reveal=2),
            P("Thử đoán: bộ lọc được áp dụng bằng phép toán gì?", "Thử đoán: áp bộ lọc bằng gì?", reveal=2, ask=True),
            P("Nhân từng phần tử với hàm truyền H đối xứng quanh tâm: G bằng H nhân F.", "3. G = H · F", reveal=3),
            P("Lấy IDFT, rồi cắt lại phần M nhân N tương ứng ảnh gốc.", "4. IDFT, cắt M × N", reveal=4),
        ], graph=pipeline(["Ảnh f", "Đệm + dời tâm (−1)^(x+y)", "DFT → F", "G = H · F", "IDFT, cắt M × N"], [0, 1, 2, 3, 4])),
        S("Cách làm", "Các bộ lọc trong miền tần số", [
            P("Thông thấp có ba loại: lý tưởng, Gauss, và Butterworth. Butterworth có tham số bậc điều khiển độ dốc, cân bằng giữa lý tưởng và Gauss.",
              "Thông thấp: lý tưởng, Gauss, Butterworth"),
            P("Thông cao có lý tưởng, Gauss, Butterworth và Laplacian trong miền tần số, dùng để làm nét, khử nhiễu tuần hoàn hay nền biến thiên chậm.",
              "Thông cao: + Laplacian; làm nét"),
        ]),
        S("So sánh", "Ba bộ lọc thông thấp", [
            P("Lý tưởng cắt đột ngột, ringing mạnh.", reveal=[1]), P("Gauss mượt, không ringing.", reveal=[2]),
            P("Butterworth nằm giữa, chỉnh độ dốc bằng bậc của nó.", reveal=[3]),
        ], table={"headers": ["Bộ lọc", "Chuyển tiếp", "Ringing"],
                  "rows": [["Lý tưởng", "Vách đứng", "Mạnh"], ["Gauss", "Mượt nhất", "Không"], ["Butterworth", "Chỉnh bằng bậc n", "Ít, tùy bậc"]]}),
        S("Ứng dụng", "Lọc tần số ở đâu", [
            P("Khử nhiễu tuần hoàn bằng notch ở chương ba, làm nét, và mọi bộ lọc kernel lớn đều nhanh hơn khi làm qua FFT.", "Notch, làm nét, kernel lớn qua FFT"),
        ]),
        limit("Ảnh sạch nhưng vẫn có thể bị suy giảm", [
            P("Lọc giúp tăng cường ảnh. Nhưng khi ảnh bị suy giảm theo một mô hình biết trước, như mờ do chuyển động, ta cần phục hồi có cơ sở. Đó là chương ba.",
              "→ Chương 3: phục hồi ảnh"),
        ], CHAIN, 6),
        traps([["Tích chập trong không gian tương ứng gì?", "Phép nhân trong miền tần số"], ["Vì sao phải đệm ảnh?", "Tránh wrap-around khi tích chập tuần hoàn"],
               ["Butterworth là gì?", "Cân bằng giữa lý tưởng và Gauss, chỉnh bằng bậc"]],
              ["Bẫy một: tích chập trong không gian tương ứng phép nhân trong miền tần số.",
               "Bẫy hai: phải đệm ảnh để tránh hiệu ứng bao quanh.",
               "Bẫy ba: Butterworth cân bằng giữa lý tưởng và Gauss, chỉnh bằng bậc."]),
    ]),

    story("tong-ket", "Tổng kết chương 2", "summary", [
        S("Tổng kết", "Lọc ảnh trong một mạch", [
            P("Nhìn lại trang sách. Tích chập và lọc hộp làm mượt; Gauss giảm dần nên không ringing."),
            P("Trung vị xóa nhiễu xung mà giữ cạnh; hình thái học xử lý hình dạng với erosion, dilation, opening, closing."),
            P("Đạo hàm, Laplacian và unsharp masking làm nét; lọc miền tần số biến tích chập thành phép nhân."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: tích chập là tương quan với kernel xoay một trăm tám mươi độ."), P("Hai: lọc lý tưởng gây ringing."),
            P("Ba: trung vị diệt nhiễu xung."), P("Bốn: opening là erosion rồi dilation."), P("Năm: đạo hàm bậc hai bằng không dọc độ dốc."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Tích chập?", "Tương quan với kernel xoay 180°"], ["Lọc lý tưởng?", "Gây ringing"], ["Trung vị?", "Diệt nhiễu xung"],
                           ["Opening?", "Erosion → dilation"], ["Bậc hai dọc độ dốc?", "Bằng 0"]]}),
        S("Tổng kết", "Sang chương 3", [
            P("Chương ba đi tiếp: phục hồi ảnh bị suy giảm theo một mô hình biết trước.", "Chương 3: phục hồi ảnh"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–3", "Trang sách: nhiễu, lấm tấm, nhòe", "—", "Làm sạch mà giữ nét", "→ Tích chập"],
    ["Tích chập & lọc hộp", "4–7, 28–34", "Nhiễu hạt", "Phép toán điểm", "LSI; tương quan/tích chập; box filter", "Mờ thô → Gauss"],
    ["Gauss", "8–11", "Mượt không viền", "Lọc lý tưởng: ringing", "Đáp ứng Gauss giảm dần; σ", "Nhiễu xung lem → trung vị"],
    ["Trung vị", "12–21", "Điểm lấm tấm", "Trung bình bị kéo lệch", "Sắp xếp chọn giữa; trung vị có trọng số", "Hình dạng → hình thái học"],
    ["Hình thái học", "22–27", "Đốm, lỗ, nét đứt", "Lọc theo giá trị", "SE; erosion/dilation/opening/closing", "Chữ nhòe → làm nét"],
    ["Làm nét", "34–40", "Cạnh không sắc", "Lọc làm mượt", "Đạo hàm bậc 1, 2; Laplacian; unsharp, highboost", "Kernel lớn → tần số"],
    ["Miền tần số", "41–48", "Thiết kế theo tần số", "Tích chập không gian", "Nhân H·F; các bước; ideal/Gauss/Butterworth", "→ Chương 3"],
    ["Tổng kết", "—", "—", "—", "Bẫy chung", "→ Chương 3"],
]
write(2, "Lọc ảnh", EX, stories, MAP)
