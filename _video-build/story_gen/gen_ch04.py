import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, story, traps, write  # noqa: E402

CHAIN = ["DHT", "DCT", "DST", "Walsh-Hadamard", "Wavelet", "Wavelet 2D"]
EX = "Một hàng pixel trên má của bức chân dung: 10, 11, 12, 13 — đổi sang hệ số nào để dễ nén và dễ phân tích nhất?"


def hist(values, labels, **extra):
    return {"bars": [{"label": lab, "value": v} for lab, v in zip(labels, values)], **extra}


stories = [
    intro("mo-dau", "Mở đầu: nhìn ảnh qua các bộ cơ sở", "Một hàng pixel 10, 11, 12, 13", [
        P("Chào các bạn. Chương bốn là các phép biến đổi ảnh. Ví dụ của cả chương: một hàng bốn pixel trên má của bức chân dung, mười, mười một, mười hai, mười ba.",
          "Ví dụ: hàng pixel 10, 11, 12, 13"),
        P("Một phép biến đổi phân tách ảnh thành tổng có trọng số của các hàm cơ sở trực giao. Mọi biến đổi của cùng một ảnh chứa cùng thông tin và tổng năng lượng, đều khả nghịch.",
          "Cùng thông tin, cùng năng lượng, khả nghịch"),
        P("Chúng chỉ khác nhau ở cách phân bố năng lượng giữa các hệ số. Thử nghĩ: cách phân bố nào là tốt nhất để nén?", "Khác nhau ở cách phân bố năng lượng", ask=True),
    ], CHAIN, [
        P("Ta đã gặp DFT ở chương hai. Chương này đi qua DHT với số thực, DCT dồn năng lượng giỏi, DST đối xứng lẻ, Walsh Hadamard chỉ cộng trừ.",
          "DFT → DHT → DCT → DST → WHT"),
        P("Rồi wavelet biết cả tần số lẫn vị trí, và wavelet hai chiều cho ảnh.", "→ Wavelet → Wavelet 2D"),
        P("Mỗi biến đổi vá một chỗ hụt của biến đổi trước, các bạn xem theo thứ tự.", "Xem theo thứ tự"),
    ]),

    story("dht", "Biến đổi Hartley rời rạc (DHT)", "method", [
        S("Vấn đề", "Tính toán với số phức thì nặng", [
            P("Biến đổi Fourier rời rạc cho ra số phức. Với ảnh lớn, mỗi hệ số có hai phần thực và ảo, tính và lưu đều tốn gấp đôi.", "DFT: số phức, tốn gấp đôi"),
        ]),
        S("Cách cũ", "DFT", [
            P("DFT của hàng mười, mười một, mười hai, mười ba là bốn mươi sáu, âm hai cộng hai j, âm hai, và âm hai trừ hai j. Ba trên bốn hệ số là số phức.",
              "DFT: 46, −2+2j, −2, −2−2j"),
        ]),
        S("Ý tưởng", "Dùng cos cộng sin thay cho số mũ phức", [
            P("DHT dùng hàm cas, tức cos cộng sin, thay cho e mũ trừ j. Kết quả luôn là số thực.", "cas = cos + sin → luôn số thực"),
            P("Hệ số Hartley bằng phần thực trừ phần ảo của hệ số Fourier, nên mang thông tin tương đương DFT.", "H = Re(F) − Im(F)"),
        ]),
        S("Cách làm", "DHT của hàng pixel", [
            P("Lấy phần thực trừ phần ảo từng hệ số DFT.", reveal=1),
            P("Thử đoán: hệ số thứ hai, âm hai cộng hai j, thành bao nhiêu?", reveal=1, ask=True),
            P("Âm hai trừ hai bằng âm bốn. Kết quả: bốn mươi sáu, âm bốn, âm hai, không. Toàn số thực.", reveal=[2, 3, 4]),
        ], table={"headers": ["k", "DFT F(k)", "DHT = Re − Im"],
                  "rows": [["0", "46", "46"], ["1", "−2 + 2j", "−4"], ["2", "−2", "−2"], ["3", "−2 − 2j", "0"]]}),
        S("So sánh", "DHT so với DFT", [
            P("DFT cho số phức, DHT cho số thực.", reveal=[1]),
            P("DHT đối xứng: H tại u v bằng H tại trừ u trừ v. Ma trận biến đổi thực, trực giao và đối xứng; biến đổi ngược cùng dạng với biến đổi thuận.", reveal=[2, 3]),
            P("Cả hai bảo toàn năng lượng.", reveal=[4]),
        ], table={"headers": ["", "DFT", "DHT"],
                  "rows": [["Hệ số", "Số phức", "Số thực"], ["Ma trận", "Phức", "Thực, trực giao, đối xứng"], ["Biến đổi ngược", "Khác dạng", "Cùng dạng"],
                           ["Năng lượng", "Bảo toàn", "Bảo toàn"]]}),
        S("Ứng dụng", "DHT ở đâu", [
            P("DHT được dùng thay DFT khi muốn tính toán hoàn toàn bằng số thực, ví dụ trên phần cứng đơn giản, vì từ DHT suy ra được DFT.", "Thay DFT khi muốn toàn số thực"),
        ]),
        limit("Vẫn giả định tuần hoàn chu kỳ N", [
            P("Cả DFT và DHT coi hàng pixel lặp lại nguyên xi: mười ba nhảy về mười. Bước nhảy đó sinh ra thành phần tần số cao giả.", "Bước nhảy ở biên"),
            P("Video sau: DCT xóa bước nhảy đó.", "→ DCT"),
        ], CHAIN, 2),
        traps([["DHT cho số gì?", "Số thực"], ["Ma trận DHT có tính chất gì?", "Thực, trực giao, đối xứng"], ["Liên hệ với DFT?", "H = Re(F) − Im(F)"]],
              ["Bẫy một: DHT luôn cho số thực, DFT cho số phức.",
               "Bẫy hai: ma trận DHT là thực, trực giao và đối xứng.",
               "Bẫy ba: hệ số Hartley bằng phần thực trừ phần ảo của hệ số Fourier."]),
    ]),

    story("dct", "Biến đổi Cosin rời rạc (DCT)", "method", [
        S("Vấn đề", "Dồn năng lượng vào thật ít hệ số", [
            P("Để nén, ta muốn gần hết năng lượng nằm ở vài hệ số đầu, còn lại gần không để bỏ đi được.", "Năng lượng dồn vào ít hệ số"),
        ]),
        S("Cách cũ", "DFT, DHT và bước nhảy ở biên", [
            P("DFT giả định tín hiệu tuần hoàn chu kỳ N, không đối xứng. Hàng mười đến mười ba lặp lại thì mười ba nhảy xuống mười.", "Chu kỳ N: 13 nhảy về 10"),
            P("Bước nhảy giả đó đẩy năng lượng sang tần số cao.", "Bước nhảy → tần số cao giả"),
        ]),
        S("Ý tưởng", "Soi gương để không còn bước nhảy", [
            P("DCT giả định tín hiệu tuần hoàn chu kỳ hai N và đối xứng chẵn: ghép hàng pixel với ảnh gương của nó, mười, mười một, mười hai, mười ba, mười ba, mười hai, mười một, mười.",
              "Chu kỳ 2N, đối xứng chẵn: soi gương"),
            P("Không còn bước nhảy ở biên, nên giảm gián đoạn và nhiễu tần số cao. Phổ của DCT tương tự DFT nhưng độ phân giải tần số gấp đôi.", "Hết bước nhảy; độ phân giải gấp đôi"),
        ]),
        S("Cách làm", "DCT và DFT của cùng hàng pixel", [
            P("Năng lượng của hàng là năm trăm ba mươi tư. Cả hai biến đổi đều đặt năm trăm hai mươi chín vào hệ số đầu, khoảng chín mươi chín phần trăm.", reveal=1),
            P("Thử đoán: năm đơn vị năng lượng còn lại, DCT và DFT đặt vào đâu?", reveal=1, ask=True),
            P("DCT dồn gần hết vào hệ số tần số thấp nhất, bốn phẩy chín bảy, hệ số cao nhất chỉ không phẩy không hai lăm. "
              "DFT rải đều, kể cả hệ số tần số cao nhất cũng nhận một, vì bước nhảy ở biên.", reveal=2),
        ], compare={"left": {"label": "DFT: năng lượng ngoài DC rải tới tần số cao", "histogram": hist([2, 1, 2], ["k=1", "k=2 (cao nhất)", "k=3"], top=5)},
                    "right": {"label": "DCT: dồn vào tần số thấp nhất", "histogram": hist([4.97, 0, 0.03], ["k=1", "k=2", "k=3 (cao nhất)"], top=5)},
                    "arrow": "cùng hàng 10–13"}),
        S("Cách làm", "Hệ số DC và khối tám nhân tám", [
            P("Hệ số đầu tiên là hệ số DC, tỉ lệ với độ sáng trung bình. Với khối tám nhân tám của ảnh tự nhiên, năng lượng tập trung ở góc trên bên trái.", "DC = độ sáng trung bình"),
            P("Hệ số tần số cao nhỏ, mắt lại kém nhạy với chi tiết mịn, nên có thể lượng tử thô hoặc bỏ đi mà ảnh gần như không đổi. Đó là bí mật của JPEG.",
              "Tần số cao nhỏ → lượng tử thô → JPEG"),
        ]),
        S("So sánh", "DFT so với DCT", [
            P("DFT giả định chu kỳ N, không đối xứng; DCT chu kỳ hai N, đối xứng chẵn.", reveal=[1]),
            P("DFT có bước nhảy ở biên, DCT thì không. DCT cho số thực và độ phân giải tần số gấp đôi.", reveal=[2, 3]),
        ], table={"headers": ["", "DFT", "DCT"],
                  "rows": [["Giả định", "Chu kỳ N", "Chu kỳ 2N, đối xứng chẵn"], ["Biên", "Bước nhảy → tần số cao giả", "Liền mạch"],
                           ["Hệ số", "Phức", "Thực, độ phân giải gấp đôi"]]}),
        S("Ứng dụng", "DCT ở đâu", [
            P("JPEG, MPEG và hầu hết các chuẩn nén ảnh, video đều dùng DCT trên từng khối. Ta sẽ gặp lại nó ở chương năm và sáu.", "JPEG, MPEG"),
        ]),
        limit("Còn có DST", [
            P("DCT dùng cosin và đối xứng chẵn. Nếu dùng sin và đối xứng lẻ thì sao? Đó là DST, người anh em của DCT.", "→ DST"),
        ], CHAIN, 3),
        traps([["DCT giả định gì?", "Chu kỳ 2N, đối xứng chẵn"], ["Vì sao JPEG chọn DCT?", "Giảm gián đoạn biên, dồn năng lượng"],
               ["Độ phân giải tần số DCT so với DFT?", "Gấp đôi"]],
              ["Bẫy một: DCT giả định tuần hoàn chu kỳ hai N và đối xứng chẵn.",
               "Bẫy hai: JPEG chọn DCT vì giảm gián đoạn ở biên và dồn năng lượng tốt.",
               "Bẫy ba: DCT có độ phân giải tần số gấp đôi DFT."]),
    ]),

    story("dst", "Biến đổi Sin rời rạc (DST)", "extra", [
        S("Vấn đề", "Nếu dùng sin thay cosin?", [
            P("DST cũng có độ phân giải tần số gấp đôi DFT. Nhưng nó có dồn năng lượng tốt như DCT không?", "DST có tốt như DCT?"),
        ]),
        S("Ý tưởng", "Đối xứng lẻ, trung bình bằng không", [
            P("DST giả định tín hiệu tuần hoàn chu kỳ hai nhân N cộng một và đối xứng lẻ: tín hiệu soi gương đổi dấu, giá trị trung bình bằng không.",
              "Chu kỳ 2(N+1), đối xứng lẻ"),
            P("Vì vậy DST không có thành phần DC tại u bằng không.", "Không có thành phần DC"),
        ]),
        S("Cách làm", "Một vùng phẳng", [
            P("Lấy một vùng phẳng, bốn pixel cùng bằng năm.", reveal=0),
            P("Thử đoán: DCT cần mấy hệ số khác không để biểu diễn vùng này?", reveal=0, ask=True),
            P("DCT chỉ cần một: hệ số DC bằng mười, còn lại bằng không.", reveal=1),
            P("DST không có DC, nên phải dùng hai hệ số khác không, mười lăm phẩy ba chín và ba phẩy sáu ba, kể cả một hệ số tần số cao hơn.", reveal=2),
        ], table={"headers": ["Vùng phẳng 5, 5, 5, 5", "k = 0", "k = 1", "k = 2", "k = 3"],
                  "rows": [["DCT", "10 (DC)", "0", "0", "0"], ["DST", "15,39", "0", "3,63", "0"]]}),
        S("So sánh", "DCT so với DST", [
            P("DCT đối xứng chẵn, có DC, giảm gián đoạn biên.", reveal=[1]), P("DST đối xứng lẻ, không có DC, không giảm gián đoạn biên như DCT.", reveal=[2]),
        ], table={"headers": ["", "DCT", "DST"],
                  "rows": [["Đối xứng", "Chẵn, chu kỳ 2N", "Lẻ, chu kỳ 2(N+1)"], ["Thành phần DC", "Có", "Không"]]}),
        traps([["DST có thành phần DC không?", "Không (trung bình bằng 0)"], ["DST giảm gián đoạn biên như DCT?", "Không"]],
              ["Bẫy một: DST không có thành phần DC vì đối xứng lẻ, trung bình bằng không.",
               "Bẫy hai: DST không giảm gián đoạn biên như DCT. Câu so sánh này rất hay gặp."]),
    ]),

    story("wht", "Biến đổi Walsh–Hadamard (WHT)", "method", [
        S("Vấn đề", "Biến đổi trên phần cứng rất yếu", [
            P("Trên vi mạch đơn giản, phép nhân với cosin là đắt. Ta muốn một biến đổi chỉ cần cộng và trừ.", "Chỉ cộng và trừ"),
        ]),
        S("Cách cũ", "DCT cần nhân với cosin", [
            P("DCT phải nhân mỗi pixel với các giá trị cosin số thực.", "Nhân với cosin"),
        ]),
        S("Ý tưởng", "Hàm cơ sở hình chữ nhật cộng một, trừ một", [
            P("WHT là biến đổi phi sin: hàm cơ sở là các hàm Walsh hình chữ nhật, chỉ nhận cộng một hoặc trừ một.", "Hàm Walsh: chỉ ±1"),
            P("Thay cho tần số, dùng sequency: số lần hàm đổi dấu. Đổi dấu càng nhiều thì càng chi tiết.", "Sequency: số lần đổi dấu"),
            P("Ma trận Hadamard xây đệ quy: cấp hai là một, một ở trên và một, trừ một ở dưới; cấp hai N ghép từ bốn bản cấp N, góc dưới phải mang dấu trừ.",
              "Ma trận Hadamard ghép đệ quy"),
        ]),
        S("Cách làm", "WHT của hàng pixel", [
            P("Nhân hàng mười, mười một, mười hai, mười ba với ma trận Hadamard bốn nhân bốn. Hàng đầu toàn cộng một: tổng bằng bốn mươi sáu.", reveal=1),
            P("Hàng hai cộng trừ xen kẽ: âm hai. Hàng ba: âm bốn.", reveal=3),
            P("Thử đoán: hàng bốn, cộng trừ trừ cộng, cho bao nhiêu?", reveal=3, ask=True),
            P("Mười trừ mười một trừ mười hai cộng mười ba bằng không. Toàn phép cộng trừ. Biến đổi ngược dùng chính ma trận đó rồi chia bốn, ra đúng hàng ban đầu.", reveal=4),
        ], table={"headers": ["Hàng Hadamard", "Phép tính", "Hệ số"],
                  "rows": [["+ + + +", "10 + 11 + 12 + 13", "46"], ["+ − + −", "10 − 11 + 12 − 13", "−2"], ["+ + − −", "10 + 11 − 12 − 13", "−4"],
                           ["+ − − +", "10 − 11 − 12 + 13", "0"]]}),
        S("So sánh", "WHT so với DCT", [
            P("DCT dùng cosin và phép nhân; WHT chỉ cộng trừ.", reveal=[1]),
            P("WHT không mất mát, khả nghịch, biến đổi ngược giống hệt biến đổi thuận. Bản nhanh FWHT có độ phức tạp N M log N M, tương đương FFT.", reveal=[2, 3]),
        ], table={"headers": ["", "DCT", "WHT"],
                  "rows": [["Hàm cơ sở", "Cosin", "Hình chữ nhật ±1"], ["Phép tính", "Nhân, cộng", "Chỉ cộng, trừ"], ["Bản nhanh", "Như FFT", "FWHT: O(NM log NM)"]]}),
        S("Ứng dụng", "WHT ở đâu", [
            P("Nén ảnh, vì nó cũng dồn năng lượng vào ít hệ số mà tính đơn giản hơn; nhận dạng mẫu; xử lý tín hiệu số.", "Nén ảnh, nhận dạng mẫu, xử lý tín hiệu"),
        ]),
        limit("Biết tần số nào, không biết ở đâu", [
            P("Mọi biến đổi đến giờ dùng hàm cơ sở trải trên cả tín hiệu. Chúng cho biết có thành phần nào, nhưng không nói thành phần đó nằm ở đâu.", "Không biết vị trí"),
            P("Video sau: wavelet.", "→ Wavelet"),
        ], CHAIN, 5),
        traps([["Hàm Walsh nhận giá trị gì?", "Chỉ +1 hoặc −1"], ["Biến đổi ngược WHT?", "Giống hệt biến đổi thuận"], ["Độ phức tạp FWHT?", "O(NM log NM)"]],
              ["Bẫy một: hàm Walsh chỉ nhận cộng một hoặc trừ một, nên WHT chỉ cần cộng trừ.",
               "Bẫy hai: biến đổi ngược của WHT giống hệt biến đổi thuận.",
               "Bẫy ba: FWHT có độ phức tạp N M log N M, tương đương FFT."]),
    ]),

    story("wavelet", "Biến đổi wavelet và đa phân giải", "method", [
        S("Vấn đề", "Một vết xước ở đâu?", [
            P("Trên bức chân dung có một vết xước nhỏ ở góc. Ta muốn biết không chỉ ảnh có chi tiết sắc, mà chi tiết đó nằm ở đâu.", "Biết cả chi tiết lẫn vị trí"),
        ]),
        S("Cách cũ", "Hàm cơ sở trải khắp tín hiệu", [
            P("Fourier dùng sóng sin kéo dài vô hạn, nên biết có tần số nào nhưng không biết ở đâu. DCT, WHT cũng vậy trên mỗi khối.", "Sóng dài vô hạn: không biết ở đâu"),
        ]),
        S("Ý tưởng", "Sóng nhỏ, nhiều tỉ lệ", [
            P("Wavelet là những sóng nhỏ có độ dài hữu hạn, nên cho biết cả tần số lẫn vị trí.", "Sóng nhỏ: tần số + vị trí"),
            P("Nó là nền tảng của lý thuyết đa phân giải, hợp nhất mã hóa băng con, lọc gương cầu phương trong xử lý tiếng nói, và xử lý ảnh kim tự tháp.", "Đa phân giải"),
            P("DWT dựa trên hàm tỉ lệ cha, trực giao với các phép tịnh tiến nguyên của nó, và hàm wavelet mẹ. Mỗi mức tách tín hiệu thành hệ số xấp xỉ và hệ số chi tiết.",
              "Hàm tỉ lệ cha + wavelet mẹ → xấp xỉ + chi tiết"),
        ]),
        S("Cách làm", "Wavelet Haar trên hàng pixel", [
            P("Wavelet đơn giản nhất là Haar: ghép từng cặp, lấy trung bình làm xấp xỉ, lấy nửa hiệu làm chi tiết. Cặp mười, mười một và cặp mười hai, mười ba.", reveal=1),
            P("Xấp xỉ: mười phẩy năm và mười hai phẩy năm, một bản thu nhỏ của hàng.", reveal=2),
            P("Thử đoán: chi tiết của một hàng thay đổi đều như vậy lớn hay nhỏ?", reveal=2, ask=True),
            P("Rất nhỏ: âm không phẩy năm và âm không phẩy năm. Nếu có vết xước, chi tiết sẽ lớn đúng tại vị trí đó.", reveal=3),
            P("Mức hai chỉ tiếp tục chia phần xấp xỉ: được mười một phẩy năm và chi tiết âm một. Kết quả là một kim tự tháp: mức thô chứa cấu trúc lớn, mức mịn chứa chi tiết nhỏ.",
              reveal=4),
        ], table={"headers": ["Mức", "Xấp xỉ (trung bình)", "Chi tiết (nửa hiệu)"],
                  "rows": [["Gốc", "10, 11, 12, 13", "—"], ["Mức 1", "10,5 ; 12,5", "—"], ["Mức 1 (chi tiết)", "—", "−0,5 ; −0,5"], ["Mức 2", "11,5", "−1"]]}),
        S("So sánh", "Fourier so với wavelet; DWT so với CWT", [
            P("Fourier biết tần số nào; wavelet biết tần số nào ở đâu.", reveal=[1]),
            P("CWT cho tỉ lệ và vị trí thay đổi liên tục, rất dư thừa, hợp để phân tích. DWT gọn, khả nghịch, hợp để nén và khử nhiễu.", reveal=[2]),
        ], table={"headers": ["", "Fourier / DCT", "Wavelet"],
                  "rows": [["Hàm cơ sở", "Sóng dài (trên cả tín hiệu/khối)", "Sóng nhỏ, hữu hạn"], ["Biết", "Tần số nào", "Tần số nào, ở đâu"]]}),
        S("Ứng dụng", "Wavelet ở đâu", [
            P("JPEG hai nghìn, khử nhiễu ở chương ba, phân tích tín hiệu có biến cố đột ngột như nhịp tim, động đất.", "JPEG2000, khử nhiễu, tín hiệu đột biến"),
        ]),
        limit("Ảnh có hai chiều", [
            P("Ta mới làm trên một hàng. Ảnh có hai chiều, và chi tiết có thể nằm ngang, dọc hay chéo. Video sau: wavelet hai chiều.", "→ Wavelet 2D"),
        ], CHAIN, 6),
        traps([["Wavelet hơn Fourier ở đâu?", "Định vị được cả tần số và vị trí"], ["Phân rã nhiều mức chia phần nào?", "Chỉ phần xấp xỉ"],
               ["CWT khác DWT?", "CWT liên tục, dư thừa; DWT gọn, khả nghịch"]],
              ["Bẫy một: wavelet định vị được cả tần số lẫn vị trí, Fourier chỉ biết tần số.",
               "Bẫy hai: phân rã nhiều mức chỉ tiếp tục chia phần xấp xỉ.",
               "Bẫy ba: CWT liên tục và dư thừa, hợp phân tích; DWT gọn và khả nghịch, hợp nén."]),
    ]),

    story("wavelet-2d", "Wavelet hai chiều", "method", [
        S("Vấn đề", "Chi tiết ngang, dọc, chéo", [
            P("Trong ảnh, mép tóc nằm ngang, sống mũi thẳng đứng, vành kính chéo. Cần biết chi tiết đi theo hướng nào.", "Chi tiết theo nhiều hướng"),
        ]),
        S("Cách cũ", "Wavelet một chiều", [
            P("Wavelet một chiều chỉ xử lý một hàng, không phân biệt hướng trong ảnh.", "Một hàng, không có hướng"),
        ]),
        S("Ý tưởng", "Một hàm tỉ lệ và ba wavelet nhạy hướng", [
            P("Trong hai chiều cần một hàm tỉ lệ hai chiều và ba hàm wavelet hai chiều tách được.", "1 hàm tỉ lệ + 3 wavelet tách được"),
            P("Ba wavelet nhạy hướng: đo biến thiên cường độ theo cột, theo hàng và theo đường chéo.", "Nhạy hướng: cột, hàng, chéo"),
        ]),
        S("Cách làm", "Bốn băng con sau một mức", [
            P("Lọc theo hàng rồi theo cột, ảnh tách thành bốn băng con. Băng xấp xỉ là ảnh thu nhỏ một nửa mỗi chiều.", reveal=1),
            P("Ba băng chi tiết theo phương ngang, dọc và chéo.", reveal=[2, 3, 4]),
            P("Thử đoán: tổng số hệ số bốn băng có nhiều hơn số pixel không?", reveal=[2, 3, 4], ask=True),
            P("Không, đúng bằng số pixel, nên không tăng dữ liệu. Phần lớn hệ số chi tiết gần không, cơ hội để nén. Muốn phân rã tiếp thì chỉ chia băng xấp xỉ.", reveal=4),
        ], table={"headers": ["Băng con", "Chứa gì"],
                  "rows": [["Xấp xỉ (LL)", "Ảnh thu nhỏ ½ mỗi chiều"], ["Chi tiết theo hàng", "Biến thiên một hướng"], ["Chi tiết theo cột", "Biến thiên hướng còn lại"],
                           ["Chi tiết chéo (HH)", "Biến thiên theo đường chéo"]]}),
        S("So sánh", "Wavelet 1D so với 2D", [
            P("Một chiều: xấp xỉ và một loại chi tiết.", reveal=[1]), P("Hai chiều: xấp xỉ và ba loại chi tiết theo ba hướng.", reveal=[2]),
        ], table={"headers": ["", "Wavelet 1D", "Wavelet 2D"],
                  "rows": [["Hàm", "1 tỉ lệ + 1 wavelet", "1 tỉ lệ + 3 wavelet tách được"], ["Mỗi mức cho", "Xấp xỉ + chi tiết", "4 băng con"]]}),
        S("Ứng dụng", "Wavelet 2D ở đâu", [
            P("Biến đổi wavelet nhanh và biến đổi ngược được cài bằng tích chập với các bộ lọc, rất hiệu quả. Dùng trong JPEG hai nghìn và khử nhiễu ảnh.", "Fast Wavelet Transform; JPEG2000"),
            P("Phần cuối slide giới thiệu học sâu: thay vì chọn cơ sở cố định như cosin hay wavelet, mạng nơ-ron tự học biểu diễn từ dữ liệu.", "Học sâu: tự học biểu diễn"),
        ]),
        limit("Đến lúc dùng biến đổi để nén", [
            P("Ta đã có đủ công cụ biến đổi. Chương năm dùng chúng để nén ảnh: DCT trong JPEG, wavelet trong JPEG hai nghìn.", "→ Chương 5: nén ảnh"),
        ], CHAIN, 6),
        traps([["Wavelet 2D cần mấy hàm wavelet?", "3, tách được, nhạy hướng"], ["Một mức cho mấy băng con?", "4: LL và 3 băng chi tiết"],
               ["Tổng số hệ số so với số pixel?", "Bằng nhau"]],
              ["Bẫy một: wavelet hai chiều cần một hàm tỉ lệ và ba hàm wavelet tách được, nhạy hướng cột, hàng, chéo.",
               "Bẫy hai: một mức phân rã cho bốn băng con.",
               "Bẫy ba: tổng số hệ số bằng số pixel, không tăng dữ liệu."]),
    ]),

    story("tong-ket", "Tổng kết chương 4", "summary", [
        S("Tổng kết", "Các phép biến đổi cạnh nhau", [
            P("DFT cho số phức, giả định chu kỳ N. DHT cho số thực với ma trận thực, trực giao, đối xứng.", reveal=[1, 2]),
            P("DCT chu kỳ hai N đối xứng chẵn, dồn năng lượng tốt nhất trong thực tế. DST đối xứng lẻ, không có DC.", reveal=[3, 4]),
            P("WHT chỉ cộng trừ, rất nhanh. Wavelet định vị được cả không gian lẫn tần số.", reveal=[5, 6]),
        ], table={"headers": ["Biến đổi", "Hệ số", "Điểm cần nhớ"],
                  "rows": [["DFT", "Phức", "Chu kỳ N"], ["DHT", "Thực", "Thực, trực giao, đối xứng"], ["DCT", "Thực", "2N, đối xứng chẵn → JPEG"],
                           ["DST", "Thực", "Đối xứng lẻ, không DC"], ["WHT", "±1", "Chỉ cộng trừ, FWHT"], ["Wavelet", "Thực", "Tần số + vị trí, đa phân giải"]]}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: mọi biến đổi cùng thông tin, cùng năng lượng, khả nghịch."), P("Hai: DHT cho số thực."), P("Ba: DCT chu kỳ hai N, đối xứng chẵn."),
            P("Bốn: DST không có DC."), P("Năm: wavelet hai chiều nhạy ba hướng."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Các biến đổi khác nhau ở đâu?", "Cách phân bố năng lượng"], ["DHT?", "Số thực"], ["DCT?", "2N, đối xứng chẵn"],
                           ["DST?", "Không có DC"], ["Wavelet 2D?", "3 hướng: cột, hàng, chéo"]]}),
        S("Tổng kết", "Sang chương 5", [
            P("Chương năm dùng các biến đổi này để nén ảnh.", "Chương 5: nén ảnh"),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
    ]),
]

MAP = [
    ["Mở đầu", "1–3", "Hàng pixel 10–13", "—", "Cùng thông tin, khác phân bố năng lượng", "→ DHT"],
    ["DHT", "4–6", "Số phức tốn kém", "DFT", "cas = cos + sin → số thực; H = Re − Im", "Bước nhảy biên → DCT"],
    ["DCT", "7–9", "Dồn năng lượng", "DFT/DHT: chu kỳ N", "Chu kỳ 2N, đối xứng chẵn", "→ DST"],
    ["DST", "10–11", "Dùng sin?", "—", "Đối xứng lẻ, không DC", "→ WHT"],
    ["WHT", "12–16", "Chỉ cộng trừ", "DCT nhân cosin", "Hàm Walsh ±1; Hadamard đệ quy", "Không biết vị trí → wavelet"],
    ["Wavelet", "17–21", "Chi tiết ở đâu", "Sóng dài vô hạn", "Sóng nhỏ, đa phân giải; Haar", "Ảnh 2 chiều → wavelet 2D"],
    ["Wavelet 2D", "22–25", "Chi tiết theo hướng", "Wavelet 1D", "1 tỉ lệ + 3 wavelet; 4 băng con", "→ Chương 5"],
    ["Tổng kết", "26", "—", "—", "Bảng so sánh, bẫy chung", "→ Chương 5"],
]
write(4, "Các phép biến đổi", EX, stories, MAP)
