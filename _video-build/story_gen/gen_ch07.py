import math
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, story, traps, write  # noqa: E402

CHAIN = ["Lấy mẫu & Nyquist", "Giảm mẫu", "Tăng mẫu", "Nearest & bilinear", "Lấy mẫu video", "Đổi tốc độ khung"]
EX = "Điện thoại chụp một chiếc áo sơ mi kẻ sọc: thu nhỏ để gửi tin nhắn, phóng to để in, và đổi video phim 24 lên 60 khung/giây"

STRIPE = [round(50 + 40 * math.cos(2 * math.pi * 0.4 * n)) for n in range(10)]  # 0,4 chu kỳ/pixel
KEPT = STRIPE[::2]


def stripe_hist(values, label_step=1):
    return {"bars": [{"label": str(i * label_step), "value": v} for i, v in enumerate(values)]}


def ball(cells, label, accent=None, warn=None):
    grid = {"label": label, "cells": [cells]}
    if accent:
        grid["accent"] = [[0, c] for c in accent]
    if warn:
        grid["warn"] = [[0, c] for c in warn]
    return grid


stories = [
    intro("mo-dau", "Mở đầu: từ thế giới liên tục đến mảng số", "Chiếc áo kẻ sọc trước ống kính", [
        P("Chào các bạn. Chương bảy quay về điểm xuất phát của mọi thứ: thu nhận ảnh. Ví dụ của cả chương: điện thoại chụp một chiếc áo sơ mi kẻ sọc nhỏ.",
          "Ví dụ: áo sơ mi kẻ sọc"),
        P("Sau đó ta thu nhỏ ảnh để gửi tin nhắn, phóng to để in, và đổi một đoạn phim từ hai mươi bốn lên sáu mươi khung mỗi giây.", "Thu nhỏ, phóng to, đổi tốc độ khung"),
        P("Thử nghĩ: chụp áo kẻ sọc rồi thu nhỏ, đôi khi trên ảnh hiện ra những vân lạ không có trên áo. Vân đó từ đâu ra?", "Vân lạ từ đâu ra?", ask=True),
    ], CHAIN, [
        P("Ta bắt đầu từ lấy mẫu, lượng tử và điều kiện Nyquist, rồi giảm mẫu và tăng mẫu.", "Lấy mẫu → giảm mẫu → tăng mẫu"),
        P("Tiếp theo là hai cách nội suy ảnh, lấy mẫu video bằng lưới, và đổi tốc độ khung hình.", "Nội suy → lưới video → tốc độ khung"),
        P("Mỗi bước vá chỗ hụt của bước trước, các bạn xem theo thứ tự.", "Xem theo thứ tự"),
    ]),

    story("lay-mau", "Lấy mẫu, lượng tử hóa và Nyquist", "method", [
        S("Vấn đề", "Thế giới liên tục, máy tính rời rạc", [
            P("Ánh sáng trên chiếc áo thay đổi liên tục theo vị trí, độ sáng cũng là số thực. Máy tính chỉ lưu được hữu hạn con số.", "Liên tục → hữu hạn con số"),
        ]),
        S("Cách cũ", "Ghi liên tục là không thể", [
            P("Không thiết bị nào ghi được giá trị tại vô số vị trí với độ chính xác vô hạn. Phải chọn đo ở đâu và làm tròn đến đâu.", "Phải chọn: đo ở đâu, làm tròn đến đâu"),
        ]),
        S("Ý tưởng", "Đo theo lưới, làm tròn theo bậc", [
            P("Ghi nhiệt độ trong ngày, các bạn đo mỗi giờ một lần: đó là lấy mẫu, rời rạc hóa vị trí. Với ảnh, các vị trí đó là lưới pixel.", "Lấy mẫu: rời rạc hóa vị trí"),
            P("Mỗi lần đo làm tròn đến một độ: đó là lượng tử hóa, rời rạc hóa biên độ. Ảnh tám bit có hai trăm năm mươi sáu mức.", "Lượng tử: rời rạc hóa biên độ"),
            P("Đo quá thưa thì bỏ sót, tệ hơn còn thấy quy luật giả: bánh xe trong phim quay ngược, áo kẻ sọc hiện vân lạ. Đó là aliasing.", "Đo thưa → aliasing"),
        ]),
        S("Công thức", "Điều kiện Nyquist", [
            P("Muốn ghi một sọc sáng tối, mỗi chu kỳ cần ít nhất hai mẫu, một cho sáng và một cho tối. Tần số lấy mẫu phải ít nhất gấp đôi tần số cao nhất.",
              "Ít nhất 2 mẫu mỗi chu kỳ"),
            P("Fourier của ảnh liên tục đo tần số theo chu kỳ trên đơn vị khoảng cách; của ảnh rời rạc theo chu kỳ trên pixel. Tần số cao nhất biểu diễn được là không phẩy năm chu kỳ mỗi pixel.",
              "CSFT: chu kỳ/khoảng cách · DSFT: chu kỳ/pixel · tối đa 0,5"),
            P("Lấy mẫu làm phổ bị lặp lại theo chu kỳ. Đủ dày thì các bản sao tách nhau; thưa thì chồng lên nhau, và phần chồng chính là aliasing.",
              "Bản sao phổ chồng nhau = aliasing"),
        ], formula=r"\underbrace{f_s}_{\text{tần số lấy mẫu}} \;\ge\; 2 \times \underbrace{f_{max}}_{\text{chi tiết nhanh nhất}}"),
        S("Cách làm", "Sọc 0,4 chu kỳ mỗi pixel", [
            P("Sọc trên áo có tần số không phẩy bốn chu kỳ mỗi pixel, cứ hai pixel rưỡi hết một chu kỳ sáng tối. Mười mẫu đầu tiên trông như hình.", reveal=0),
            P("Thử đoán: không phẩy bốn có thỏa điều kiện Nyquist không?", reveal=0, ask=True),
            P("Có, vì nhỏ hơn không phẩy năm. Mỗi chu kỳ có hai phẩy năm mẫu, nhiều hơn hai, nên ảnh gốc biểu diễn đúng sọc.", reveal=0),
        ], histogram={**stripe_hist(STRIPE), "caption": "Độ sáng của 10 pixel đầu trên sọc 0,4 chu kỳ/pixel"}),
        S("So sánh", "Lấy mẫu so với lượng tử hóa", [
            P("Lấy mẫu rời rạc hóa vị trí, tức tham số; lượng tử hóa rời rạc hóa biên độ.", reveal=[1]),
            P("Lấy mẫu thưa sinh aliasing; lượng tử thô sinh sai số lượng tử, như các dải màu loang.", reveal=[2]),
        ], table={"headers": ["", "Lấy mẫu", "Lượng tử hóa"],
                  "rows": [["Rời rạc hóa", "Vị trí (tham số)", "Biên độ"], ["Làm thô quá thì", "Aliasing", "Sai số lượng tử, dải loang"]]}),
        S("Ứng dụng", "Nyquist ở đâu", [
            P("Âm thanh CD lấy mẫu bốn mươi bốn phẩy một kilohertz, hơn gấp đôi giới hạn nghe khoảng hai mươi kilohertz. Máy ảnh có bộ lọc chống răng cưa trước cảm biến cũng vì Nyquist.",
              "CD 44,1 kHz; bộ lọc chống răng cưa trong máy ảnh"),
        ]),
        limit("Ảnh đã chụp, giờ phải thu nhỏ", [
            P("Ảnh gốc ổn. Nhưng để gửi tin nhắn, ta phải thu nhỏ, tức là giảm số mẫu. Liệu sọc có còn thỏa Nyquist?", "Thu nhỏ có còn thỏa Nyquist?"),
        ], CHAIN, 2),
        traps([["Lấy mẫu và lượng tử khác nhau thế nào?", "Lấy mẫu: vị trí · lượng tử: biên độ"], ["Đơn vị tần số DSFT?", "Chu kỳ / pixel"],
               ["Tần số cao nhất biểu diễn được?", "0,5 chu kỳ / pixel"]],
              ["Bẫy một: lấy mẫu rời rạc hóa vị trí, lượng tử hóa rời rạc hóa biên độ. Đề rất hay đảo.",
               "Bẫy hai: biến đổi Fourier rời rạc dùng chu kỳ trên pixel, liên tục dùng chu kỳ trên đơn vị khoảng cách.",
               "Bẫy ba: tần số cao nhất biểu diễn được là không phẩy năm chu kỳ mỗi pixel."]),
    ]),

    story("giam-mau", "Giảm mẫu và decimator", "method", [
        S("Vấn đề", "Thu nhỏ ảnh để gửi tin nhắn", [
            P("Ảnh áo quá lớn để gửi. Ta muốn thu nhỏ một nửa mỗi chiều.", "Thu nhỏ một nửa"),
        ]),
        S("Cách cũ", "Bỏ bớt pixel trực tiếp", [
            P("Cách nhanh nhất: giữ một pixel, bỏ một pixel. Đơn giản, nhưng có an toàn không?", "Giữ một, bỏ một"),
        ]),
        S("Ý tưởng", "Giữ mỗi mẫu thứ C, nhưng lọc trước", [
            P("Giảm mẫu theo hệ số nguyên C và D: giữ mỗi mẫu thứ C theo chiều ngang, thứ D theo chiều dọc.", "Giữ mỗi mẫu thứ C, thứ D"),
            P("Trong miền tần số, phổ giãn ra C lần. Ảnh nhỏ đi một nửa thì mỗi sọc chỉ còn nửa số pixel, nên tính theo pixel nó dao động nhanh gấp đôi.", "Phổ giãn C lần"),
            P("Muốn an toàn, lọc thông thấp trước để bỏ chi tiết quá mịn, rồi mới giảm. Bộ lọc trước cộng bộ giảm mẫu gọi là decimator.", "Lọc trước + giảm mẫu = decimator"),
        ]),
        S("Cách làm", "Giảm mẫu hai lần một ảnh sọc", [
            P("Bên trái là mười mẫu của sọc không phẩy bốn. Giảm mẫu hai lần: chỉ giữ mẫu số không, hai, bốn, sáu, tám.", reveal=1),
            P("Thử đoán: năm mẫu còn lại trông giống sọc nhanh hay sọc chậm?", reveal=1, ask=True),
            P("Sọc chậm hẳn: chín mươi, sáu mươi hai, mười tám, mười tám, sáu mươi hai, năm mẫu mới hết một chu kỳ. Tần số thật thành không phẩy tám, vượt không phẩy năm, bị gập lại thành không phẩy hai. Đó là sọc giả.",
              reveal=2),
        ], compare={"left": {"label": "Gốc: 0,4 chu kỳ/pixel", "histogram": stripe_hist(STRIPE)},
                    "right": {"label": "Giữ mỗi mẫu thứ 2: sọc giả 0,2", "histogram": stripe_hist(KEPT, 2)},
                    "arrow": "bỏ một, giữ một"}),
        S("Cách làm", "Giới hạn an toàn và lọc trước", [
            P("Ảnh gốc có sọc không phẩy bốn chu kỳ mỗi pixel.", reveal=1),
            P("Giảm hai lần, tần số theo pixel mới thành không phẩy tám.", reveal=2),
            P("Vượt không phẩy năm, gập lại thành không phẩy hai: sọc giả.", reveal=3),
            P("Muốn an toàn khi giảm C lần, tần số gốc phải nhỏ hơn một chia hai C, tức không phẩy hai lăm với C bằng hai.", reveal=4),
            P("Sọc không phẩy bốn vượt giới hạn, nên lọc thông thấp bỏ nó đi rồi mới giảm. Ảnh nhỏ mất sọc mịn nhưng không có sọc giả. Thà mất chi tiết còn hơn chi tiết sai.",
              reveal=5),
        ], table={"headers": ["Bước", "Phép tính", "Kết quả"],
                  "rows": [["Ảnh gốc", "sọc 0,4 chu kỳ/pixel", "< 0,5 → đúng"], ["Giảm mẫu C = 2", "0,4 × 2", "0,8 chu kỳ/pixel"],
                           ["Vượt 0,5 → gập lại", "|0,8 − 1|", "sọc giả 0,2"], ["Giới hạn an toàn", "1 / (2C)", "0,25 chu kỳ/pixel"],
                           ["Lọc trước rồi giảm", "bỏ phần trên 0,25", "không còn sọc giả"]]}),
        S("So sánh", "Bỏ pixel trực tiếp so với decimator", [
            P("Bỏ pixel trực tiếp nhanh nhưng có thể sinh sọc giả.", reveal=[1]), P("Decimator lọc trước nên chặn được aliasing, đổi lại ảnh mềm hơn.", reveal=[2]),
        ], table={"headers": ["", "Bỏ pixel trực tiếp", "Decimator (lọc trước)"],
                  "rows": [["Aliasing", "Có thể xảy ra", "Bị chặn"], ["Chi tiết mịn", "Thành sọc giả", "Bị lọc mất, không sai"]]}),
        S("Ứng dụng", "Giảm mẫu ở đâu", [
            P("Tạo ảnh thu nhỏ, giảm độ phân giải video cho điện thoại, xây kim tự tháp ảnh nhiều tầng: đều cần lọc trước khi giảm.", "Ảnh thu nhỏ, video độ phân giải thấp"),
        ]),
        limit("Giờ phải phóng to để in", [
            P("Giảm mẫu xong, ta lại cần phóng to ảnh để in khổ lớn. Phải tạo thêm những pixel chưa từng được đo.", "Tạo thêm pixel"),
        ], CHAIN, 3),
        traps([["Giảm mẫu làm phổ thế nào?", "Giãn ra C lần → có thể aliasing"], ["Bộ lọc đặt ở đâu?", "TRƯỚC bộ giảm mẫu (prefilter)"],
               ["Giới hạn an toàn khi giảm C lần?", "f < 1/(2C)"]],
              ["Bẫy một: giảm mẫu làm phổ giãn ra, có thể gây aliasing.",
               "Bẫy hai: bộ lọc thông thấp đặt trước bộ giảm mẫu; ghép lại gọi là decimator.",
               "Bẫy ba: khi giảm C lần, tần số gốc phải nhỏ hơn một chia hai C."]),
    ]),

    story("tang-mau", "Tăng mẫu và interpolator", "method", [
        S("Vấn đề", "Phóng to ảnh để in", [
            P("Ta cần ảnh to gấp đôi mỗi chiều. Các pixel mới phải có giá trị hợp lý.", "Cần thêm pixel hợp lý"),
        ]),
        S("Cách cũ", "Chèn số không", [
            P("Bước đầu của tăng mẫu là chèn C trừ một số không vào giữa các mẫu. Hiển thị ngay thì thấy các vạch đen xen kẽ.", "Chèn 0 → vạch đen xen kẽ"),
        ]),
        S("Ý tưởng", "Chèn rồi lọc để lấp lỗ", [
            P("Tăng mẫu làm phổ co lại, không bỏ mẫu nào nên không mất thông tin, không có aliasing.", "Phổ co lại, không aliasing"),
            P("Nhưng số không tạo ra bản sao phổ thừa, chính là các lỗ đen. Bộ lọc thông thấp phía sau xóa bản sao, tức lấp lỗ. Tăng mẫu cộng bộ lọc là interpolator.",
              "Tăng mẫu + lọc sau = interpolator"),
        ]),
        S("Cách làm", "Tăng mẫu một hàng pixel", [
            P("Hàng gốc ba pixel: mười, hai mươi, ba mươi.", reveal=1),
            P("Chèn một số không vào giữa mỗi cặp: mười, không, hai mươi, không, ba mươi.", reveal=2),
            P("Thử đoán: bộ lọc nên điền gì vào chỗ số không?", reveal=2, ask=True),
            P("Trung bình hai bên: mười, mười lăm, hai mươi, hai mươi lăm, ba mươi. Hàng dài gấp đôi và mượt. Đó là nội suy tuyến tính.", reveal=3),
        ], table={"headers": ["Bước", "Dãy giá trị"],
                  "rows": [["Hàng gốc", "10, 20, 30"], ["Chèn số 0 xen kẽ", "10, 0, 20, 0, 30"], ["Lọc: số 0 = trung bình hai bên", "10, 15, 20, 25, 30"]]}),
        S("Cách làm", "Decimator và interpolator", [
            P("Decimator: lọc thông thấp trước với tần số cắt một chia hai C, rồi giữ mỗi mẫu thứ C.", reveal=[1, 2, 3]),
            P("Interpolator ngược thứ tự: chèn số không trước, lọc sau. Mẹo nhớ: giảm mẫu lọc trước, tăng mẫu lọc sau.", reveal=[5, 6, 7]),
        ], code={"lines": ["# Decimator: giảm mẫu C lần", "g ← lowpass(f, cutoff = 1/(2C))     # lọc TRƯỚC", "out[m] ← g[C·m]                     # giữ mỗi mẫu thứ C", "",
                           "# Interpolator: tăng mẫu C lần", "up[C·m] ← f[m], vị trí khác ← 0    # chèn số 0", "out ← lowpass(up, cutoff = 1/(2C))  # lọc SAU"]}),
        S("So sánh", "Giảm mẫu so với tăng mẫu", [
            P("Giảm mẫu giữ mỗi mẫu thứ C, phổ giãn, có thể aliasing, lọc trước.", reveal=[1, 2, 3]),
            P("Tăng mẫu chèn C trừ một số không, phổ co, không aliasing, lọc sau.", reveal=[4, 5]),
        ], table={"headers": ["Tiêu chí", "Giảm mẫu", "Tăng mẫu"],
                  "rows": [["Thao tác", "Giữ mỗi mẫu thứ C", "Chèn C−1 số 0"], ["Phổ", "Giãn C lần", "Co C lần"], ["Aliasing", "Có thể", "Không"],
                           ["Bộ lọc", "TRƯỚC (prefilter)", "SAU"], ["Hệ ghép", "Decimator", "Interpolator"]]}),
        S("Ứng dụng", "Tăng mẫu ở đâu", [
            P("Phóng to ảnh, tăng độ phân giải video, đổi tần số lấy mẫu âm thanh: đều chèn mẫu rồi lọc.", "Phóng to ảnh, video, âm thanh"),
        ]),
        limit("Bộ lọc cụ thể nào?", [
            P("Bộ lọc phía sau có thể đơn giản hay phức tạp. Slide nêu hai cách nội suy ảnh phổ biến nhất. Video sau.", "→ Nearest và bilinear"),
        ], CHAIN, 4),
        traps([["Tăng mẫu có gây aliasing?", "Không, vì không mất thông tin"], ["Bộ lọc của interpolator đặt đâu?", "SAU bộ tăng mẫu"],
               ["Chèn bao nhiêu số 0?", "C − 1 giữa hai mẫu"]],
              ["Bẫy một: tăng mẫu không gây aliasing vì không bỏ mẫu nào.",
               "Bẫy hai: bộ lọc của interpolator đặt sau bộ tăng mẫu, ngược với decimator.",
               "Bẫy ba: tăng C lần thì chèn C trừ một số không giữa hai mẫu."]),
    ]),

    story("noi-suy", "Nội suy nearest neighbor và bilinear", "method", [
        S("Vấn đề", "Giá trị tại một điểm lẻ", [
            P("Khi phóng to hay xoay ảnh, điểm cần tính rơi vào giữa các pixel, tọa độ lẻ. Lấy giá trị nào?", "Tọa độ lẻ: lấy giá trị nào?"),
        ]),
        S("Cách cũ", "Lấy pixel gần nhất", [
            P("Nội suy lân cận gần nhất, còn gọi là bậc không hay lặp pixel: làm tròn tọa độ về pixel gần nhất rồi lấy giá trị của nó. Rẻ nhất về tính toán.",
              "Nearest: làm tròn về pixel gần nhất"),
            P("Nhưng phóng to thì hiện rõ khối vuông và răng cưa ở cạnh.", "Khối vuông, răng cưa"),
        ]),
        S("Ý tưởng", "Pha trộn theo khoảng cách", [
            P("Nội suy song tuyến, bậc một, dùng bốn pixel bao quanh. Pixel càng gần thì trọng số càng lớn, như pha màu theo tỉ lệ.", "Bilinear: 4 pixel, gần thì nặng hơn"),
        ]),
        S("Cách làm", "Nội suy song tuyến tại một điểm", [
            P("Bốn pixel: hàng trên mười và hai mươi, hàng dưới ba mươi và bốn mươi. Điểm cần tính cách mép trái một phần tư ô, cách hàng trên ba phần tư ô.", reveal=1),
            P("Bước một, hàng trên: đi một phần tư từ mười tới hai mươi, được mười hai phẩy năm.", reveal=1),
            P("Bước hai, hàng dưới: một phần tư từ ba mươi tới bốn mươi, được ba mươi hai phẩy năm.", reveal=1),
            P("Thử đoán: kết quả cuối gần mười hai phẩy năm hay gần ba mươi hai phẩy năm?", reveal=1, ask=True),
            P("Bước ba, theo chiều dọc: ba phần tư từ mười hai phẩy năm tới ba mươi hai phẩy năm, được hai mươi bảy phẩy năm, gần hàng dưới vì điểm nằm gần hàng dưới.",
              reveal=1),
            P("Nearest chỉ lấy pixel gần nhất là ba mươi. Hai mươi bảy phẩy năm phản ánh cả bốn hàng xóm, ba mươi chỉ phản ánh một.", reveal=1),
        ], grid={"label": "4 pixel bao quanh; ô cam = pixel gần nhất", "cells": [[10, 20], [30, 40]], "warn": [[1, 0]]}),
        S("So sánh", "Nearest so với bilinear", [
            P("Nearest là bậc không, lặp pixel; bilinear là bậc một.", reveal=[1]), P("Nearest dùng một pixel, bilinear dùng bốn.", reveal=[2]),
            P("Nearest rẻ nhất; bilinear tốn thêm vài phép nhân.", reveal=[3]), P("Nearest ra khối vuông và răng cưa; bilinear mượt hơn.", reveal=[4]),
        ], table={"headers": ["Tiêu chí", "Nearest neighbor", "Bilinear"],
                  "rows": [["Tên khác", "Zero-order, pixel replication", "First-order"], ["Số pixel dùng", "1", "4 bao quanh"],
                           ["Chi phí", "Thấp nhất", "Cao hơn một chút"], ["Kết quả", "Khối vuông, răng cưa", "Mượt hơn"]]}),
        S("Ứng dụng", "Nội suy ở đâu", [
            P("Nearest được dùng khi cần giữ đúng giá trị pixel, như ảnh nhãn phân đoạn hay ảnh điểm ảnh nghệ thuật. Bilinear là mặc định khi phóng to ảnh thường.",
              "Nearest: ảnh nhãn, pixel art · bilinear: phóng to thường"),
        ]),
        limit("Ảnh tĩnh xong, còn video", [
            P("Đến giờ ta chỉ lấy mẫu theo không gian. Video còn lấy mẫu theo thời gian, và cách quét quyết định thông tin nào được ghi lại.", "Video: lấy mẫu theo thời gian"),
        ], CHAIN, 5),
        traps([["Nearest còn gọi là gì?", "Zero-order, pixel replication"], ["Bilinear dùng mấy pixel?", "4 pixel bao quanh"],
               ["Ví dụ: bilinear và nearest cho bao nhiêu?", "27,5 và 30"]],
              ["Bẫy một: nearest neighbor còn gọi là nội suy bậc không hay lặp pixel.",
               "Bẫy hai: bilinear là bậc một và dùng bốn pixel bao quanh.",
               "Bẫy ba: trong ví dụ, bilinear cho hai mươi bảy phẩy năm, nearest cho ba mươi."]),
    ]),

    story("lay-mau-video", "Lấy mẫu video và cấu trúc lưới", "extra", [
        S("Vấn đề", "Video lấy mẫu cả không gian lẫn thời gian", [
            P("Video không chỉ có lưới pixel mà còn có chuỗi khung theo thời gian. Bước thu nhận và quét ban đầu quyết định thông tin nào có trong dữ liệu.",
              "Quét ban đầu quyết định thông tin có trong dữ liệu"),
        ]),
        S("Ý tưởng", "Lọc trước rồi lấy mẫu trên một lưới", [
            P("Thu nhận được mô hình hóa thành hai phần: bộ lọc trước theo không gian và thời gian, rồi lấy mẫu lý tưởng trên một cấu trúc lấy mẫu.", "Lọc trước + lấy mẫu lý tưởng"),
            P("Cấu trúc lấy mẫu quyết định lượng thông tin không gian thời gian; bộ lọc trước giới hạn aliasing.", "Cấu trúc → thông tin · lọc → aliasing"),
        ]),
        S("Cách làm", "Lưới", [
            P("Lưới D chiều là tập điểm tạo bởi tổ hợp tuyến tính hệ số nguyên của các vector độc lập tuyến tính. Nói đơn giản, một mẫu điểm lặp đều đặn.", "Lattice: mẫu điểm lặp đều"),
            P("Lấy mẫu theo thời gian là lưới một chiều, xác định bởi chu kỳ khung hình T.", "1D: chu kỳ khung T"),
            P("Lấy mẫu dọc và thời gian là lưới hai chiều, ví dụ quét xen kẽ: lượt này ghi dòng lẻ, lượt sau ghi dòng chẵn.", "2D: quét xen kẽ"),
        ]),
        traps([["Lưới D chiều là gì?", "Tổ hợp tuyến tính hệ số nguyên của vector độc lập"], ["Quét xen kẽ là lưới mấy chiều?", "2 chiều (dọc – thời gian)"]],
              ["Bẫy một: lưới là tập điểm tạo bởi tổ hợp tuyến tính với hệ số nguyên của các vector độc lập tuyến tính.",
               "Bẫy hai: quét xen kẽ là lưới hai chiều theo dọc và thời gian; lấy mẫu thời gian thuần là lưới một chiều."]),
    ]),

    story("toc-do-khung", "Chuyển đổi tốc độ khung hình", "method", [
        S("Vấn đề", "Phim 24 khung, màn hình 60 khung", [
            P("Phim điện ảnh quay hai mươi bốn khung mỗi giây. Muốn chiếu mượt ở bốn mươi tám hay sáu mươi khung, phải tạo thêm khung chưa từng được quay.",
              "24 → 48 hoặc 60 khung/giây"),
        ]),
        S("Cách cũ", "Nội suy thời gian thuần túy", [
            P("Cách đơn giản: khung mới tính từ các khung lân cận tại cùng vị trí pixel. Nếu phổ thời gian thỏa Nyquist, có thể dùng nội suy sinc lý tưởng.", "Nội suy tại cùng vị trí"),
        ]),
        S("Ý tưởng", "Nội suy dọc theo quỹ đạo", [
            P("Vật chuyển động không đứng yên ở một pixel. Hãy ước lượng chuyển động trước, như chương sáu, rồi nội suy dọc theo quỹ đạo của vật.", "Ước lượng chuyển động, nội suy theo quỹ đạo"),
        ]),
        S("Cách làm", "Quả bóng giữa hai khung", [
            P("Khung trước: quả bóng ở ô số một.", reveal=1),
            P("Khung sau: quả bóng ở ô số ba.", reveal=2),
            P("Thử đoán: lấy trung bình hai khung tại từng pixel, khung giữa trông thế nào?", reveal=2, ask=True),
            P("Hai quả bóng mờ, mỗi quả một nửa độ sáng, ở ô một và ô ba. Đó là bóng ma, ghosting.", reveal=3),
            P("Nội suy có bù chuyển động biết bóng đi từ ô một sang ô ba, nên đặt một quả bóng rõ nét ở ô hai.", reveal=4),
        ], grid=[ball([0, 100, 0, 0, 0], "Khung trước", accent=[1]), ball([0, 0, 0, 100, 0], "Khung sau", accent=[3]),
                 ball([0, 50, 0, 50, 0], "Trung bình: bóng ma", warn=[1, 3]), ball([0, 0, 100, 0, 0], "Bù chuyển động", accent=[2])]),
        S("So sánh", "Nội suy thuần so với bù chuyển động", [
            P("Nội suy thuần đơn giản, nhưng gây bóng ma khi vật chuyển động nhanh.", reveal=[1]),
            P("Bù chuyển động tốn công ước lượng, nhưng đặt vật đúng chỗ.", reveal=[2]),
        ], table={"headers": ["", "Nội suy thời gian thuần", "Có bù chuyển động"],
                  "rows": [["Vật nhanh", "Bóng ma (ghosting)", "Đúng vị trí"], ["Chi phí", "Thấp", "Cần ước lượng chuyển động"]]}),
        S("Ứng dụng", "Đổi tốc độ khung ở đâu", [
            P("Chế độ làm mượt chuyển động trên TV, chuyển phim hai mươi bốn khung sang chuẩn truyền hình, tạo video chuyển động chậm từ video thường.",
              "Làm mượt trên TV, slow motion"),
        ]),
        limit("Ảnh thu được, giờ phải hiển thị", [
            P("Thu nhận và lấy mẫu xong. Đầu bên kia của đường ống là hiển thị ảnh lên thiết bị ít mức xám, và đo xem ảnh đẹp hay xấu. Đó là chương tám.",
              "→ Chương 8: hiển thị và đánh giá"),
        ], CHAIN, 6),
        traps([["Vì sao cần nội suy có bù chuyển động?", "Nội suy thuần gây ghosting khi chuyển động nhanh"], ["Ví dụ trong slide?", "Phim 24 → 48 hoặc 60 khung/giây"]],
              ["Bẫy một: nội suy thời gian thuần túy gây bóng ma khi vật chuyển động nhanh, nên cần bù chuyển động.",
               "Bẫy hai: ví dụ trong slide là tăng phim từ hai mươi bốn lên bốn mươi tám hoặc sáu mươi khung mỗi giây."]),
    ]),

    story("tong-ket", "Tổng kết chương 7", "summary", [
        S("Tổng kết", "Thu nhận ảnh trong một mạch", [
            P("Nhìn lại chiếc áo kẻ sọc. Lấy mẫu rời rạc hóa vị trí, lượng tử rời rạc hóa biên độ, và Nyquist đòi ít nhất hai mẫu mỗi chu kỳ."),
            P("Giảm mẫu cần lọc trước để tránh sọc giả; tăng mẫu chèn số không rồi lọc sau; nearest và bilinear là hai cách nội suy."),
            P("Video lấy mẫu trên lưới, và đổi tốc độ khung nên bù chuyển động để tránh bóng ma."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: lấy mẫu là vị trí, lượng tử là biên độ."), P("Hai: DSFT dùng chu kỳ trên pixel."), P("Ba: giảm mẫu phổ giãn, lọc trước."),
            P("Bốn: tăng mẫu không aliasing, lọc sau."), P("Năm: nội suy thuần gây bóng ma."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Lấy mẫu / lượng tử?", "Vị trí / biên độ"], ["Đơn vị DSFT?", "Chu kỳ / pixel"], ["Giảm mẫu?", "Phổ giãn, lọc TRƯỚC"],
                           ["Tăng mẫu?", "Không aliasing, lọc SAU"], ["Đổi tốc độ khung?", "Bù chuyển động tránh ghosting"]]}),
        S("Tổng kết", "Sang chương 8", [
            P("Chương tám đi tới đầu bên kia: hiển thị ảnh lên thiết bị ít mức xám, và đo chất lượng ảnh.", "Chương 8: hiển thị và đánh giá"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–2", "Áo kẻ sọc: chụp, thu nhỏ, phóng to, đổi tốc độ khung", "—", "Liên tục → rời rạc", "→ Lấy mẫu"],
    ["Lấy mẫu & Nyquist", "3–8", "Liên tục → hữu hạn số", "Ghi liên tục là không thể", "Lấy mẫu vị trí, lượng tử biên độ; ≥ 2 mẫu/chu kỳ", "Thu nhỏ → giảm mẫu"],
    ["Giảm mẫu", "9–14", "Thu nhỏ gửi tin nhắn", "Bỏ pixel trực tiếp", "Giữ mỗi mẫu thứ C, lọc trước; sọc 0,4 → giả 0,2", "Phóng to → tăng mẫu"],
    ["Tăng mẫu", "15–17", "Phóng to để in", "Chèn số 0", "Chèn 0 rồi lọc sau", "Bộ lọc nào → nội suy"],
    ["Nearest & bilinear", "18–21", "Giá trị tại điểm lẻ", "Nearest: khối vuông", "Bilinear: 4 pixel theo khoảng cách", "Video → lưới"],
    ["Lấy mẫu video", "22–28", "Lấy mẫu thời gian", "—", "Lọc trước + lưới; quét xen kẽ", "→ Tốc độ khung"],
    ["Đổi tốc độ khung", "29–33", "24 → 60 khung/giây", "Nội suy thuần", "Bù chuyển động, tránh ghosting", "→ Chương 8"],
    ["Tổng kết", "—", "—", "—", "Bẫy chung", "→ Chương 8"],
]
write(7, "Thu nhận ảnh", EX, stories, MAP)
