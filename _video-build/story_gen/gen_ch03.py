import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, chain, limit, pipeline, story, traps, write  # noqa: E402

CHAIN = ["Mô hình nhiễu", "Bộ lọc trung bình", "Notch", "Hàm suy giảm", "Lọc nghịch đảo", "Wiener", "CLS", "Wavelet", "CT", "Đa kênh & video"]
EX = "Ảnh biển số xe từ camera giao thông ban đêm: vừa mờ vì xe chạy, vừa nhiễu vì thiếu sáng"


def hist(values, labels, **extra):
    return {"bars": [{"label": lab, "value": v} for lab, v in zip(labels, values)], **extra}


stories = [
    story("mo-dau", "Mở đầu: bài toán ngược", "intro", [
        S("Mở đầu", "Một biển số vừa mờ vừa nhiễu", [
            P("Chào các bạn. Chương ba là phục hồi ảnh, chương dài và nặng lý thuyết nhất, nhưng ý tưởng rất trực quan. "
              "Ví dụ cả chương: ảnh biển số xe từ camera giao thông ban đêm, vừa mờ vì xe chạy, vừa nhiễu vì thiếu sáng.", "Ví dụ: biển số mờ và nhiễu"),
            P("Khác tăng cường ảnh mang tính chủ quan, phục hồi dựa trên kiến thức tiên nghiệm về hiện tượng suy giảm, và cải thiện theo một tiêu chí khách quan.",
              "Phục hồi: dựa trên kiến thức về suy giảm"),
            P("Thử nghĩ: nếu biết chính xác ảnh bị làm mờ thế nào, ta có đảo ngược được hoàn toàn không?", "Biết cách làm mờ thì đảo ngược được không?", ask=True),
        ]),
        S("Mở đầu", "Mô hình suy giảm", [
            P("Ảnh gốc f đi qua hàm suy giảm h, là kênh truyền hay hệ thống thu nhận.", reveal=1),
            P("Cộng thêm nhiễu, ra ảnh quan sát g. Trong miền tần số: G bằng H nhân F cộng N.", reveal=2),
            P("Bài toán ngược: từ g, cùng hiểu biết về h và về nhiễu, ước lượng một ảnh gần f nhất.", reveal=3),
        ], graph=pipeline(["Ảnh gốc f", "Hàm suy giảm h", "+ nhiễu n", "Ảnh quan sát g", "Phục hồi → f̂"], [0, 1, 2, 2, 3]),
           formula=r"g = h * f + n \quad\Longleftrightarrow\quad G = H\,F + N"),
        S("Mở đầu", "Lộ trình của chương", [
            P("Trước hết hiểu nhiễu, rồi các bộ lọc khử nhiễu: trung bình, notch cho nhiễu tuần hoàn.", "Nhiễu → bộ lọc trung bình → notch"),
            P("Tiếp đến khử mờ: ước lượng hàm suy giảm, lọc nghịch đảo, Wiener, CLS. Rồi wavelet, tái tạo CT, và phục hồi đa kênh, video.",
              "Khử mờ: h → nghịch đảo → Wiener → CLS → wavelet → CT"),
        ], chain=chain(CHAIN, 0)),
    ]),

    story("mo-hinh-nhieu", "Các mô hình nhiễu", "method", [
        S("Vấn đề", "Muốn khử nhiễu phải biết nhiễu là gì", [
            P("Ảnh biển số ban đêm có hạt lấm tấm khắp nơi, đôi chỗ có điểm trắng đen lẻ tẻ. Bộ lọc tốt cho loại này có thể tệ cho loại kia.", "Mỗi loại nhiễu một bộ lọc"),
        ]),
        S("Cách cũ", "Một bộ lọc cho mọi ảnh", [
            P("Dùng một bộ lọc làm mượt cho mọi trường hợp: nhiễu giảm nhưng chi tiết như nét chữ biển số cũng mờ theo.", "Lọc chung: mất chi tiết"),
        ]),
        S("Ý tưởng", "Mô tả nhiễu bằng phân bố xác suất", [
            P("Nhiễu sinh ra khi thu nhận và truyền dẫn. Ta mô tả nó bằng hàm mật độ xác suất: giá trị nhiễu hay rơi vào đâu.", "Nhiễu → hàm mật độ xác suất"),
            P("Khi phổ Fourier của nhiễu là hằng số trên mọi tần số, ta gọi là nhiễu trắng. Nhiễu thường coi là độc lập tọa độ và không tương quan với ảnh.",
              "Nhiễu trắng: phổ hằng số"),
        ]),
        S("Cách làm", "Nhìn histogram của nhiễu", [
            P("Chụp một vùng phẳng, histogram cho thấy hình dạng nhiễu. Nhiễu Gauss có histogram hình chuông quanh giá trị thật.", reveal=1),
            P("Thử đoán: nhiễu muối tiêu có histogram trông thế nào?", reveal=1, ask=True),
            P("Hai cột lẻ ở hai đầu, cực đen và cực trắng: một số pixel ngẫu nhiên bị biến thành không hoặc hai trăm năm mươi lăm.", reveal=2),
        ], compare={"left": {"label": "Gauss: hình chuông", "histogram": hist([1, 4, 12, 25, 12, 4, 1], ["", "", "", "100", "", "", ""], top=40)},
                    "right": {"label": "Muối tiêu: hai cột ở hai đầu", "histogram": hist([6, 0, 0, 40, 0, 0, 6], ["0", "", "", "100", "", "", "255"], top=40)},
                    "arrow": "khác hình dạng"}),
        S("So sánh", "Các loại nhiễu thường gặp", [
            P("Gauss phổ biến nhất, đặc trưng bởi trung bình và độ lệch chuẩn.", reveal=[1]),
            P("Rayleigh, Erlang hay Gamma, hàm mũ và phân bố đều là các hàm mật độ khác.", reveal=[2, 3]),
            P("Muối tiêu là nhiễu xung, pixel thành cực đen hoặc cực trắng.", reveal=[4]),
        ], table={"headers": ["Loại nhiễu", "Đặc điểm"],
                  "rows": [["Gauss", "Phổ biến nhất; trung bình + độ lệch chuẩn"], ["Rayleigh, Erlang (Gamma)", "Phân bố lệch"],
                           ["Hàm mũ, phân bố đều", "Các dạng khác"], ["Muối tiêu (xung)", "Pixel thành 0 hoặc 255"]]}),
        S("Ứng dụng", "Biết nhiễu để chọn bộ lọc", [
            P("Cảm biến thiếu sáng cho nhiễu gần Gauss; đường truyền lỗi bit cho nhiễu muối tiêu. Biết nguồn gốc là đoán được loại nhiễu.", "Nguồn gốc → loại nhiễu"),
        ]),
        limit("Biết nhiễu, giờ chọn bộ lọc", [
            P("Mỗi loại nhiễu có đặc trưng thống kê riêng, quyết định bộ lọc phù hợp. Video sau: các bộ lọc trung bình.", "→ Bộ lọc trung bình"),
        ], CHAIN, 2),
        traps([["Nhiễu trắng là gì?", "Phổ Fourier hằng số trên mọi tần số"], ["Nhiễu muối tiêu là loại gì?", "Nhiễu xung: 0 hoặc 255"],
               ["Gauss đặc trưng bởi gì?", "Trung bình và độ lệch chuẩn"]],
              ["Bẫy một: nhiễu trắng có phổ Fourier là hằng số trên mọi tần số.",
               "Bẫy hai: muối tiêu là nhiễu xung, pixel thành cực đen hoặc cực trắng.",
               "Bẫy ba: nhiễu Gauss đặc trưng bởi trung bình và độ lệch chuẩn."]),
    ]),

    story("loc-trung-binh", "Các bộ lọc trung bình và thống kê thứ tự", "method", [
        S("Vấn đề", "Một điểm tiêu giữa vùng phẳng", [
            P("Trên nền biển số trắng đều, có một pixel bị nhiễu tiêu thành đen kịt. Bộ lọc nào xóa được mà không làm mờ?", "Xóa điểm đen lẻ"),
        ]),
        S("Cách cũ", "Trung bình cộng", [
            P("Arithmetic mean lấy trung bình cộng cửa sổ. Làm mượt nhưng làm mờ chi tiết, và điểm nhiễu chỉ bị pha loãng chứ không mất.", "Trung bình cộng: mờ, chỉ pha loãng"),
        ]),
        S("Ý tưởng", "Đổi cách lấy trung bình theo loại nhiễu", [
            P("Có nhiều cách lấy trung bình: nhân, điều hòa, contraharmonic với bậc Q. Mỗi cách nhạy khác nhau với giá trị cực đen hay cực trắng.", "Nhiều kiểu trung bình"),
            P("Hoặc thôi tính trung bình, chọn theo thứ tự: trung vị, lớn nhất, nhỏ nhất.", "Thống kê thứ tự: median, max, min"),
        ]),
        S("Cách làm", "Cửa sổ ba nhân ba có một điểm tiêu", [
            P("Tám pixel bằng một trăm, một pixel bằng không. Trung bình cộng khoảng tám mươi tám phẩy chín: điểm đen bị pha loãng, vẫn còn vết.", reveal=1),
            P("Trung bình nhân: tích có một số không nên ra không. Trung bình điều hòa: một chia không là vô cùng, kết quả cũng về không. Cả hai thất bại với nhiễu tiêu.",
              reveal=3),
            P("Thử đoán: contraharmonic với Q dương thì sao?", reveal=3, ask=True),
            P("Q bằng một: tổng bình phương chia tổng, được đúng một trăm. Q dương diệt tiêu. Trung vị và bộ lọc max cũng cho một trăm.", reveal=5),
        ], table={"headers": ["Bộ lọc", "Kết quả", "Nhận xét"],
                  "rows": [["Arithmetic mean", "≈ 88,9", "Pha loãng, còn vết"], ["Geometric mean", "0", "Thất bại với tiêu"],
                           ["Harmonic mean", "0", "Thất bại với tiêu"], ["Contraharmonic Q = 1", "100", "Q dương diệt tiêu"],
                           ["Median / max", "100", "Xóa sạch"]]}),
        S("Cách làm", "Nếu là điểm muối", [
            P("Đổi điểm nhiễu thành muối, hai trăm năm mươi lăm. Trung bình cộng khoảng một trăm mười bảy, vẫn còn vết sáng.", "Arithmetic ≈ 117,2"),
            P("Trung bình điều hòa khoảng một trăm lẻ bảy, gần một trăm hơn: điều hòa tốt với muối và Gauss, nhưng thất bại với tiêu.", "Harmonic ≈ 107,2: tốt với muối"),
            P("Contraharmonic với Q âm diệt muối. Bộ lọc min chọn giá trị nhỏ nhất, xóa sạch điểm trắng; trung vị cũng cho một trăm.", "Q âm diệt muối · min xóa muối"),
        ]),
        S("So sánh", "Bộ lọc nào cho nhiễu nào", [
            P("Arithmetic làm mượt nhưng mờ; geometric mượt tương đương mà giữ chi tiết tốt hơn.", reveal=[1, 2]),
            P("Harmonic tốt với muối và Gauss, thất bại với tiêu.", reveal=[3]),
            P("Contraharmonic: Q dương diệt tiêu, Q âm diệt muối, cùng một dấu không diệt được cả hai. Max diệt tiêu, min diệt muối.", reveal=[4, 5]),
        ], table={"headers": ["Bộ lọc", "Tốt với", "Kém với"],
                  "rows": [["Arithmetic", "Gauss (làm mượt)", "Làm mờ chi tiết"], ["Geometric", "Như arithmetic, giữ chi tiết hơn", "Tiêu (tích = 0)"],
                           ["Harmonic", "Muối, Gauss", "Tiêu"], ["Contraharmonic", "Q > 0: tiêu · Q < 0: muối", "Không diệt cả hai cùng lúc"],
                           ["Max / Min", "Max: tiêu · Min: muối", "Ngược lại"]]}),
        S("Ứng dụng", "Bộ lọc trung bình ở đâu", [
            P("Ảnh quét tài liệu, ảnh truyền qua kênh lỗi, ảnh y tế: chọn đúng bộ lọc theo loại nhiễu giúp giữ nét chữ và chi tiết.", "Tài liệu quét, ảnh truyền lỗi"),
        ]),
        limit("Nhiễu dạng sọc lặp lại", [
            P("Có loại nhiễu không ngẫu nhiên mà lặp lại đều đặn như sọc, do nhiễu điện. Lọc trung bình sẽ làm mờ cả ảnh mà sọc vẫn còn.", "Nhiễu tuần hoàn"),
            P("Video sau xử lý nó trong miền tần số: bộ lọc notch.", "→ Notch"),
        ], CHAIN, 3),
        traps([["Contraharmonic Q dương diệt gì?", "Nhiễu tiêu (pepper)"], ["Harmonic thất bại với gì?", "Nhiễu tiêu"], ["Max / min diệt gì?", "Max: tiêu · min: muối"]],
              ["Bẫy một: contraharmonic với Q dương diệt tiêu, Q âm diệt muối.",
               "Bẫy hai: trung bình điều hòa tốt với muối và Gauss nhưng thất bại với tiêu.",
               "Bẫy ba: bộ lọc max diệt tiêu, bộ lọc min diệt muối."]),
    ]),

    story("notch", "Nhiễu tuần hoàn và bộ lọc notch", "method", [
        S("Vấn đề", "Sọc nhiễu đều đặn", [
            P("Nhiễu điện từ đèn đường làm ảnh có những sọc mờ lặp lại đều khắp khung hình.", "Sọc lặp lại đều"),
        ]),
        S("Cách cũ", "Lọc trung bình trong miền không gian", [
            P("Lọc trung bình làm mờ cả ảnh mà vẫn không xóa sạch sọc, vì sọc trải khắp ảnh.", "Mờ cả ảnh, sọc vẫn còn"),
        ]),
        S("Ý tưởng", "Nhiễu tuần hoàn là vài đốm trong phổ", [
            P("Trong phổ Fourier, nhiễu tuần hoàn hiện thành các đốm năng lượng tập trung tại đúng tần số của nhiễu.", "Đốm sáng trong phổ"),
            P("Chỉ cần khoét đúng các đốm đó là xóa được sọc, phần còn lại của ảnh gần như không bị đụng tới.", "Khoét đúng các đốm"),
        ]),
        S("Cách làm", "Khoét đốm nhiễu trong phổ", [
            P("Phổ của ảnh cao nhất ở tần số không và giảm dần ra tần số cao, nhưng có hai đốm nhô lên bất thường.", reveal=0),
            P("Thử đoán: hai đốm đó là gì?", reveal=0, ask=True),
            P("Là tần số của sọc nhiễu, đối xứng hai bên. Bộ lọc notch reject đặt vùng chặn đúng tại hai đốm đó.", reveal=1),
        ], histogram=hist([2, 3, 26, 6, 10, 40, 10, 6, 26, 3, 2], ["", "", "−u₀", "", "", "0", "", "", "u₀", "", ""],
                          bands=[{"start": 2, "end": 3, "step": 1, "marks": [{"step": 1, "style": "warn"}]},
                                 {"start": 8, "end": 9, "label": "vùng chặn notch", "step": 1, "marks": [{"step": 1, "style": "warn"}]}],
                          caption="Phổ minh họa (đối xứng); hai đốm ±u₀ là nhiễu tuần hoàn")),
        S("Công thức", "Notch reject và notch pass", [
            P("Notch reject là tích các bộ lọc thông cao có tâm dời tới vị trí các đốm nhiễu, theo từng cặp đối xứng.", "Tích các bộ lọc thông cao dời tâm"),
            P("Notch pass là phần bù: một trừ notch reject. Nó giữ lại đúng nhiễu, dùng để quan sát hình dạng nhiễu.", "Notch pass = 1 − notch reject"),
        ], formula=r"H_{NR}(u,v) = \prod_{k=1}^{Q} \underbrace{H_k(u,v)\, H_{-k}(u,v)}_{\text{thông cao dời tâm tới đốm } \pm k} \qquad H_{NP} = 1 - H_{NR}"),
        S("So sánh", "Lọc không gian so với notch", [
            P("Lọc trung bình đụng tới mọi tần số, làm mờ cả ảnh.", reveal=[1]), P("Notch chỉ chặn vài tần số nhiễu, giữ nguyên phần còn lại.", reveal=[2]),
        ], table={"headers": ["", "Lọc trung bình", "Notch reject"],
                  "rows": [["Tác động", "Mọi tần số", "Chỉ tần số nhiễu"], ["Ảnh sau lọc", "Mờ, sọc còn", "Hết sọc, giữ chi tiết"]]}),
        S("Ứng dụng", "Notch ở đâu", [
            P("Khử nhiễu điện lưới, sọc do máy quét, nhiễu tuần hoàn trong ảnh vệ tinh và ảnh y tế.", "Nhiễu điện, sọc máy quét"),
        ]),
        limit("Ảnh còn mờ", [
            P("Khử nhiễu xong, biển số vẫn mờ vì xe chạy. Muốn khử mờ, trước hết phải biết ảnh bị làm mờ thế nào.", "Còn mờ → cần biết h"),
        ], CHAIN, 4),
        traps([["Vì sao nhiễu tuần hoàn hợp lọc tần số?", "Hiện thành đốm tập trung trong phổ"], ["Notch reject xây thế nào?", "Tích các bộ lọc thông cao dời tâm"],
               ["Notch pass?", "1 − notch reject"]],
              ["Bẫy một: nhiễu tuần hoàn hiện thành các đốm năng lượng tập trung trong phổ Fourier.",
               "Bẫy hai: notch reject là tích các bộ lọc thông cao có tâm dời tới các đốm nhiễu.",
               "Bẫy ba: notch pass là phần bù, bằng một trừ notch reject."]),
    ]),

    story("ham-suy-giam", "Hàm suy giảm và cách ước lượng", "extra", [
        S("Vấn đề", "Ảnh bị làm mờ thế nào?", [
            P("Muốn đảo ngược sự mờ, phải biết hàm suy giảm h: chuyển động của xe, độ lệch tiêu cự, hay nhiễu loạn không khí.", "Cần biết h"),
        ]),
        S("Ý tưởng", "Suy giảm tuyến tính, bất biến vị trí", [
            P("Với suy giảm tuyến tính và bất biến vị trí, h thỏa tính cộng, tính đồng nhất và bất biến không gian.", "Cộng tính, đồng nhất, bất biến vị trí"),
            P("Ảnh không nhiễu là tích chập ảnh gốc với đáp ứng xung của h, biểu diễn qua tích phân Fredholm loại một. Có nhiễu thì cộng N: G bằng H F cộng N.",
              "Tích chập, Fredholm loại một"),
        ]),
        S("Cách làm", "Ba cách ước lượng h", [
            P("Quan sát: nhìn một chi tiết sắc nét trong ảnh, như một điểm đèn nhỏ, xem nó bị nhòe ra sao.", reveal=1),
            P("Thực nghiệm: chụp một xung sáng cường độ A đã biết bằng chính thiết bị đó để đo đáp ứng.", reveal=2),
            P("Mô hình hóa: dùng toán học, ví dụ nhiễu loạn khí quyển gần giống bộ lọc thông thấp Gauss. Phục hồi khi phải ước lượng h như vậy gọi là giải chập mù.",
              reveal=3),
        ], table={"headers": ["Cách", "Làm thế nào"],
                  "rows": [["Quan sát", "Xem chi tiết sắc nét bị nhòe trong ảnh"], ["Thực nghiệm", "Chụp xung cường độ A đã biết"],
                           ["Mô hình hóa", "Công thức toán, vd khí quyển ≈ thông thấp Gauss"]]}),
        traps([["Ba cách ước lượng h?", "Quan sát, thực nghiệm, mô hình hóa"], ["Phục hồi khi phải ước lượng h gọi là?", "Giải chập mù (blind deconvolution)"]],
              ["Bẫy một: ba cách ước lượng hàm suy giảm là quan sát, thực nghiệm và mô hình hóa.",
               "Bẫy hai: phục hồi khi phải ước lượng hàm suy giảm gọi là giải chập mù."]),
    ]),

    story("loc-nghich-dao", "Lọc nghịch đảo", "method", [
        S("Vấn đề", "Biết h rồi, đảo ngược thế nào?", [
            P("Đã biết H, ta muốn lấy lại F từ ảnh quan sát G.", "Lấy F từ G"),
        ]),
        S("Cách cũ", "Lọc trung bình chỉ làm mượt", [
            P("Các bộ lọc khử nhiễu chỉ làm mượt, không đảo ngược được sự mờ.", "Làm mượt ≠ khử mờ"),
        ]),
        S("Ý tưởng", "Chia lại cho H", [
            P("G bằng H nhân F, vậy chia G cho H là ra F. Đơn giản như đảo ngược một phép nhân.", "F̂ = G / H"),
        ]),
        S("Cách làm", "Ba tần số, cùng một chút nhiễu", [
            P("Giả sử tại ba tần số, F đều bằng mười, nhiễu bằng không phẩy năm, còn H là một, không phẩy năm, và không phẩy không một.", reveal=1),
            P("Tần số thứ nhất: G bằng mười phẩy năm, chia cho một được mười phẩy năm, sai không phẩy năm.", reveal=1),
            P("Tần số thứ hai: G năm phẩy năm, chia không phẩy năm được mười một, sai một.", reveal=2),
            P("Thử đoán: tần số mà H chỉ bằng không phẩy không một thì sao?", reveal=2, ask=True),
            P("G chỉ là không phẩy sáu, chia cho không phẩy không một được sáu mươi. Sai năm mươi! Nhiễu nhỏ xíu bị khuếch đại một trăm lần.", reveal=3),
        ], table={"headers": ["H", "G = 10·H + 0,5", "Nghịch đảo G/H", "Sai so với F = 10"],
                  "rows": [["1", "10,5", "10,5", "0,5"], ["0,5", "5,5", "11", "1"], ["0,01", "0,6", "60", "50 ✗"]]}),
        S("Công thức", "Vì sao nhiễu bùng nổ", [
            P("Chia G cho H được F cộng N chia H. Khi H gần không, số hạng N chia H khổng lồ.", "F̂ = F + N/H"),
        ], formula=r"\hat{F} = \frac{G}{H} = F + \underbrace{\frac{N}{H}}_{\text{bùng nổ khi } H \to 0}"),
        S("So sánh", "Không nhiễu và có nhiễu", [
            P("Không nhiễu, lọc nghịch đảo phục hồi hoàn hảo.", reveal=[1]), P("Có nhiễu, tần số nào H gần không thì nhiễu bị khuếch đại không kiểm soát.", reveal=[2]),
        ], table={"headers": ["Điều kiện", "Lọc nghịch đảo"],
                  "rows": [["Không nhiễu", "Phục hồi hoàn hảo"], ["Có nhiễu, H gần 0", "Nhiễu bị khuếch đại cực lớn"]]}),
        S("Ứng dụng", "Khi nào dùng được", [
            P("Lọc nghịch đảo chỉ dùng được khi nhiễu rất nhỏ và H không có giá trị gần không, hoặc khi ta chỉ phục hồi một dải tần số an toàn.", "Nhiễu nhỏ, H không gần 0"),
        ]),
        limit("Cần biết lúc nào nên dừng", [
            P("Ta cần bộ lọc biết tự kiềm chế ở những tần số mà nhiễu lấn át tín hiệu. Đó là bộ lọc Wiener.", "→ Wiener"),
        ], CHAIN, 6),
        traps([["Lọc nghịch đảo yếu ở đâu?", "Rất nhạy nhiễu khi H gần 0"], ["Không nhiễu thì sao?", "Phục hồi hoàn hảo"]],
              ["Bẫy một: lọc nghịch đảo rất nhạy nhiễu tại các tần số H gần không.",
               "Bẫy hai: nếu không có nhiễu, lọc nghịch đảo phục hồi hoàn hảo."]),
    ]),

    story("wiener", "Bộ lọc Wiener (MMSE)", "method", [
        S("Vấn đề", "Phục hồi mà không khuếch đại nhiễu", [
            P("Ta muốn ước lượng gần ảnh gốc nhất, tức sai số bình phương trung bình nhỏ nhất, mà không để nhiễu bùng nổ.", "Sai số bình phương trung bình nhỏ nhất"),
        ]),
        S("Cách cũ", "Lọc nghịch đảo", [
            P("Lọc nghịch đảo chia thẳng cho H, khuếch đại nhiễu tại các tần số H nhỏ.", "Chia thẳng → nhiễu bùng nổ"),
        ]),
        S("Ý tưởng", "Biết khi nào nên tin tín hiệu", [
            P("Wiener đưa thêm tỉ lệ công suất nhiễu trên tín hiệu. Tần số nào tín hiệu mạnh thì phục hồi mạnh; tần số nào nhiễu lấn át thì kiềm chế.",
              "Thêm tỉ lệ nhiễu / tín hiệu"),
            P("Giả định: nhiễu và ảnh không tương quan, đều có trung bình không, và ước lượng là hàm tuyến tính của ảnh suy giảm.", "Giả định: không tương quan, trung bình 0"),
        ]),
        S("Công thức", "Bộ lọc Wiener", [
            P("Tử số giống lọc nghịch đảo. Mẫu số cộng thêm K, tỉ lệ công suất nhiễu trên tín hiệu.", "Mẫu số + K"),
            P("Khi K bằng không, tức không nhiễu, Wiener trở về đúng lọc nghịch đảo. Khi H rất nhỏ so với K, hệ số tiến về không thay vì vô cùng.",
              "K = 0 → nghịch đảo · H nhỏ → hệ số về 0"),
        ], formula=r"\hat{F} = \left[ \frac{H^{*}}{|H|^2 + \underbrace{K}_{S_n / S_f}} \right] G"),
        S("Cách làm", "Cùng ba tần số, K bằng không phẩy không một", [
            P("H bằng một: Wiener cho mười phẩy bốn, gần như lọc nghịch đảo.", reveal=1),
            P("H bằng không phẩy năm: mười phẩy năm tám.", reveal=2),
            P("Thử đoán: tại H bằng không phẩy không một, Wiener cho bao nhiêu?", reveal=2, ask=True),
            P("Chỉ khoảng không phẩy năm chín, thay vì sáu mươi. Wiener chấp nhận bỏ tần số đó vì nhiễu lấn át, nhưng không để nhiễu bùng nổ.", reveal=3),
        ], table={"headers": ["H", "G", "Nghịch đảo", "Wiener (K = 0,01)"],
                  "rows": [["1", "10,5", "10,5", "≈ 10,40"], ["0,5", "5,5", "11", "≈ 10,58"], ["0,01", "0,6", "60 ✗", "≈ 0,59"]]}),
        S("So sánh", "Nghịch đảo so với Wiener", [
            P("Nghịch đảo không dùng thông tin nhiễu; Wiener dùng tỉ lệ nhiễu trên tín hiệu.", reveal=[1]),
            P("Wiener tối ưu theo sai số bình phương trung bình, nhưng cần biết phổ công suất ảnh gốc.", reveal=[2, 3]),
        ], table={"headers": ["", "Lọc nghịch đảo", "Wiener (MMSE)"],
                  "rows": [["Thông tin nhiễu", "Không dùng", "Tỉ lệ Sn/Sf"], ["H gần 0", "Nhiễu bùng nổ", "Kiềm chế, không bùng nổ"],
                           ["Cần biết", "H", "H và phổ công suất ảnh gốc"]]}),
        S("Ứng dụng", "Wiener ở đâu", [
            P("Khử mờ ảnh thiên văn, ảnh y tế, ảnh camera. Hiệu năng phục hồi thường được đo bằng SNR và sai số bình phương trung bình.", "Thiên văn, y tế · đo bằng SNR, MSE"),
        ]),
        limit("Phải biết phổ ảnh gốc", [
            P("Wiener cần phổ công suất của ảnh gốc, thứ ta đang đi tìm. Và nó chỉ tối ưu theo trung bình thống kê, không tối ưu cho từng ảnh cụ thể.",
              "Cần phổ ảnh gốc; chỉ tối ưu trung bình"),
            P("Video sau: bình phương tối thiểu có ràng buộc.", "→ CLS"),
        ], CHAIN, 7),
        traps([["Wiener còn gọi là gì?", "Bộ lọc bình phương trung bình tối thiểu (MMSE)"], ["K = 0 thì Wiener thành gì?", "Lọc nghịch đảo"],
               ["Khó khăn của Wiener?", "Cần phổ công suất ảnh gốc; chỉ tối ưu trung bình"]],
              ["Bẫy một: Wiener là bộ lọc bình phương trung bình tối thiểu.",
               "Bẫy hai: khi không có nhiễu, Wiener trở về lọc nghịch đảo.",
               "Bẫy ba: Wiener cần phổ công suất ảnh gốc và chỉ tối ưu theo trung bình thống kê."]),
    ]),

    story("cls", "Lọc bình phương tối thiểu có ràng buộc", "method", [
        S("Vấn đề", "Không biết phổ ảnh gốc", [
            P("Ta không có ảnh biển số gốc, nên không biết phổ công suất của nó. Vẫn muốn phục hồi tốt cho đúng ảnh này.", "Không có phổ ảnh gốc"),
        ]),
        S("Cách cũ", "Wiener", [
            P("Wiener cần phổ công suất ảnh gốc và chỉ tối ưu theo trung bình thống kê.", "Cần phổ gốc"),
        ]),
        S("Ý tưởng", "Ảnh tốt là ảnh mượt, khớp với quan sát", [
            P("Chọn ảnh mượt nhất, đo bằng toán tử Laplacian, trong số các ảnh khớp với quan sát đến mức sai số cho phép.", "Mượt nhất (Laplacian) + khớp quan sát"),
            P("Laplacian lớn ở chỗ thay đổi đột ngột, nên tối thiểu nó giúp giảm độ nhạy với nhiễu.", "Laplacian → giảm nhạy nhiễu"),
        ]),
        S("Công thức", "Lời giải CLS", [
            P("Lời giải trong miền tần số giống Wiener, nhưng thay tỉ lệ nhiễu trên tín hiệu bằng gamma nhân phổ của Laplacian P.", "γ·|P|² thay cho K"),
            P("Chỉ cần biết trung bình và phương sai của nhiễu, không cần phổ ảnh gốc.", "Chỉ cần thống kê nhiễu"),
        ], formula=r"\hat{F} = \left[ \frac{H^{*}}{|H|^2 + \gamma\, \underbrace{|P|^2}_{\text{phổ Laplacian}}} \right] G"),
        S("Cách làm", "Điều chỉnh gamma", [
            P("Chọn một gamma ban đầu.", reveal=[1]),
            P("Tính ảnh phục hồi, rồi tính sai số khôi phục so với ảnh quan sát.", reveal=[2, 3]),
            P("Thử đoán: sai số còn lớn hơn mức cho phép thì nên tăng hay giảm gamma?", reveal=[3], ask=True),
            P("Giảm gamma để bớt làm mượt, khớp quan sát hơn; sai số quá nhỏ thì tăng gamma. Lặp đến khi thỏa ràng buộc.", reveal=[4, 5]),
        ], code={"lines": ["γ ← giá trị ban đầu", "F̂ ← H*·G / (|H|² + γ·|P|²)", "r ← G − H·F̂;  so ‖r‖² với ‖η‖² (từ thống kê nhiễu)",
                           "if ‖r‖² quá lớn: giảm γ;  if quá nhỏ: tăng γ", "lặp đến khi ‖r‖² ≈ ‖η‖² ± sai số cho phép"]}),
        S("So sánh", "Wiener so với CLS", [
            P("Wiener cần phổ công suất ảnh gốc và nhiễu, tối ưu trung bình.", reveal=[1]),
            P("CLS chỉ cần trung bình và phương sai nhiễu, tối ưu cho từng ảnh, đổi lại phải lặp chọn gamma.", reveal=[2, 3]),
        ], table={"headers": ["", "Wiener", "CLS"],
                  "rows": [["Cần biết", "Phổ ảnh gốc, phổ nhiễu", "Trung bình, phương sai nhiễu"], ["Tối ưu", "Trung bình thống kê", "Cho từng ảnh"],
                           ["Tham số", "K", "γ, điều chỉnh lặp"]]}),
        S("Ứng dụng", "CLS ở đâu", [
            P("Phục hồi ảnh khi không có mô hình thống kê của ảnh gốc, như ảnh pháp y hay ảnh khoa học chỉ có một bản.", "Ảnh chỉ có một bản, không có thống kê gốc"),
        ]),
        limit("Mọi tần số đều bị đối xử như nhau", [
            P("Các bộ lọc tần số xử lý cả ảnh một kiểu. Nhiễu ở vùng phẳng và chi tiết ở vùng nét chữ lại cần cách xử lý khác nhau theo vị trí và tỉ lệ.",
              "Cần xử lý theo vị trí và tỉ lệ"),
            P("Video sau: khử nhiễu bằng wavelet.", "→ Wavelet"),
        ], CHAIN, 8),
        traps([["CLS tối thiểu gì?", "Hàm tiêu chí dựa trên Laplacian, có ràng buộc"], ["γ chọn thế nào?", "Điều chỉnh lặp đến khi thỏa ràng buộc"],
               ["CLS cần biết gì về ảnh gốc?", "Không cần phổ ảnh gốc"]],
              ["Bẫy một: CLS tối thiểu một hàm tiêu chí dựa trên Laplacian, kèm ràng buộc sai số khôi phục.",
               "Bẫy hai: gamma được điều chỉnh lặp đến khi thỏa ràng buộc.",
               "Bẫy ba: CLS không cần phổ công suất ảnh gốc."]),
    ]),

    story("wavelet", "Khử nhiễu bằng wavelet", "method", [
        S("Vấn đề", "Khử nhiễu mà giữ nét chữ", [
            P("Ta muốn xóa hạt nhiễu trên nền phẳng nhưng giữ nguyên các cạnh sắc của chữ trên biển số.", "Xóa nhiễu, giữ cạnh"),
        ]),
        S("Cách cũ", "Lọc trung bình và lọc tần số", [
            P("Lọc trung bình làm mờ cạnh. Lọc tần số đối xử mọi vị trí như nhau.", "Mờ cạnh; không phân biệt vị trí"),
        ]),
        S("Ý tưởng", "Nhiễu là nhiều hệ số nhỏ, cạnh là vài hệ số lớn", [
            P("Biến đổi wavelet là biểu diễn đa phân giải, cài bằng bộ lọc băng con hai kênh lặp. Cạnh thật cho vài hệ số chi tiết lớn; nhiễu rải ra rất nhiều hệ số nhỏ.",
              "Cạnh: hệ số lớn · nhiễu: hệ số nhỏ"),
            P("Vậy đặt một ngưỡng: hệ số nhỏ hơn ngưỡng coi như nhiễu, bỏ đi.", "Ngưỡng hóa hệ số"),
        ]),
        S("Cách làm", "Ba bước và hai kiểu ngưỡng", [
            P("Bước một, phân rã ảnh thành hệ số xấp xỉ tần số thấp và hệ số chi tiết tần số cao ở nhiều mức. Lấy năm hệ số chi tiết: không phẩy ba, âm không phẩy tám, hai phẩy năm, âm bốn, không phẩy một.",
              reveal=1),
            P("Bước hai, ngưỡng hóa với ngưỡng bằng một. Ngưỡng cứng chỉ xóa hệ số nhỏ hơn ngưỡng, giữ nguyên phần còn lại: hai phẩy năm và âm bốn.", reveal=2),
            P("Thử đoán: ngưỡng mềm khác ngưỡng cứng ở đâu?", reveal=2, ask=True),
            P("Ngưỡng mềm còn kéo các hệ số giữ lại về phía không một lượng bằng ngưỡng: một phẩy năm và âm ba.", reveal=3),
            P("Bước ba, biến đổi wavelet ngược để tái tạo ảnh đã khử nhiễu.", reveal=3),
        ], table={"headers": ["Hệ số chi tiết", "0,3", "−0,8", "2,5", "−4,0", "0,1"],
                  "rows": [["Gốc", "0,3", "−0,8", "2,5", "−4,0", "0,1"], ["Ngưỡng cứng (T = 1)", "0", "0", "2,5", "−4,0", "0"],
                           ["Ngưỡng mềm (T = 1)", "0", "0", "1,5", "−3,0", "0"]]}),
        S("So sánh", "Ngưỡng cứng so với ngưỡng mềm", [
            P("Ngưỡng cứng chỉ đưa hệ số nhỏ về không, giữ nguyên hệ số lớn.", reveal=[1]),
            P("Ngưỡng mềm giảm đều mọi hệ số theo ngưỡng, kết quả mượt hơn.", reveal=[2]),
        ], table={"headers": ["", "Ngưỡng cứng", "Ngưỡng mềm"],
                  "rows": [["Hệ số < T", "Về 0", "Về 0"], ["Hệ số ≥ T", "Giữ nguyên", "Co về 0 một lượng T"]]}),
        S("Ứng dụng", "Wavelet khử nhiễu ở đâu", [
            P("Ảnh y tế, ảnh thiên văn, tín hiệu âm thanh: khử nhiễu mà vẫn giữ cạnh và chi tiết đột ngột.", "Y tế, thiên văn, âm thanh"),
        ]),
        limit("Không chụp được bên trong vật", [
            P("Đến giờ ta phục hồi ảnh đã chụp. Có bài toán khác hẳn: tái tạo ảnh bên trong một vật mà camera không nhìn thấy, như lát cắt cơ thể.",
              "Tái tạo bên trong vật"),
            P("Video sau: tái tạo ảnh từ phép chiếu, nền tảng của CT.", "→ CT"),
        ], CHAIN, 9),
        traps([["Ba bước khử nhiễu wavelet?", "Phân rã → ngưỡng hóa → biến đổi ngược"], ["Ngưỡng mềm khác cứng?", "Mềm co cả hệ số lớn; cứng chỉ xóa hệ số nhỏ"]],
              ["Bẫy một: ba bước là phân rã, ngưỡng hóa, rồi biến đổi wavelet ngược.",
               "Bẫy hai: ngưỡng cứng chỉ xóa hệ số nhỏ; ngưỡng mềm giảm đều mọi hệ số theo ngưỡng."]),
    ]),

    story("ct", "Tái tạo ảnh từ phép chiếu (CT)", "method", [
        S("Vấn đề", "Nhìn vào bên trong cơ thể", [
            P("Tia X chụp thẳng chỉ cho một bóng chồng lên nhau của mọi thứ trên đường đi. Ta muốn thấy từng lát cắt bên trong.", "Muốn thấy lát cắt bên trong"),
        ]),
        S("Cách cũ", "Một tấm X quang", [
            P("Một tấm X quang thường là tổng hấp thụ dọc mỗi tia, mọi lớp chồng lên nhau, không biết cái gì nằm trước, cái gì nằm sau.", "Mọi lớp chồng lên nhau"),
        ]),
        S("Ý tưởng", "Chiếu từ nhiều góc rồi chiếu ngược", [
            P("Chiếu tia X qua vật theo nhiều hướng, mỗi hướng cho một profile hấp thụ một chiều.", "Nhiều góc chiếu"),
            P("Chiếu ngược, backprojection: rải đều mỗi giá trị đo ngược lại dọc theo tia của nó, rồi cộng tất cả các hướng. Chỗ nào nhiều tia cùng nói là đặc thì sáng lên.",
              "Rải ngược dọc tia, cộng các hướng"),
        ]),
        S("Cách làm", "Chiếu ngược một ảnh hai nhân hai", [
            P("Vật hai nhân hai: góc trên trái bằng hai, góc dưới phải bằng một, còn lại không.", reveal=1),
            P("Chiếu ngang được tổng hai hàng: hai và một. Chiếu dọc được tổng hai cột: hai và một.", reveal=1),
            P("Thử đoán: rải ngược rồi cộng hai hướng, điểm nào sáng nhất?", reveal=1, ask=True),
            P("Mỗi pixel nhận một nửa tổng hàng cộng một nửa tổng cột: hai, một phẩy năm, một phẩy năm, một. Góc trên trái sáng nhất, đúng vị trí vật, nhưng có vết nhòe. Thêm nhiều góc chiếu thì vết nhòe giảm.",
              reveal=2),
        ], grid=[{"label": "Vật thật", "cells": [[2, 0], [0, 1]], "accent": [[0, 0]]},
                 {"label": "Chiếu ngược 2 hướng", "cells": ["2 1,5".split(), "1,5 1".split()], "accent": [[0, 0]]}]),
        S("So sánh", "Ít góc so với nhiều góc", [
            P("Một góc chiếu chỉ cho một dải nhòe.", reveal=[1]),
            P("Slide minh họa với một, hai, ba, bốn và ba mươi hai phép chiếu ngược: càng nhiều góc, ảnh càng chính xác.", reveal=[2, 3]),
        ], table={"headers": ["Số góc chiếu", "Ảnh tái tạo"],
                  "rows": [["1", "Một dải nhòe"], ["2–4", "Thấy vị trí, còn vết nhòe"], ["32", "Gần đúng hình vật"]]}),
        S("Ứng dụng", "CT ở đâu", [
            P("Chụp cắt lớp vi tính trong bệnh viện thu các lát cắt, rồi chồng lại tạo biểu diễn ba chiều của cơ thể.", "Chụp cắt lớp, dựng 3D"),
        ]),
        limit("Ảnh nhiều kênh và video", [
            P("Ảnh màu, ảnh đa phổ và video có nhiều kênh liên quan nhau. Phục hồi từng kênh riêng là bỏ phí thông tin. Video cuối chương.", "→ Đa kênh & video"),
        ], CHAIN, 10),
        traps([["CT tái tạo bằng kỹ thuật gì?", "Chiếu ngược (backprojection)"], ["Nhiều góc chiếu thì sao?", "Ảnh càng chính xác"]],
              ["Bẫy một: CT tái tạo ảnh bằng chiếu ngược từ các profile hấp thụ một chiều.",
               "Bẫy hai: càng nhiều góc chiếu ngược, ảnh tái tạo càng chính xác."]),
    ]),

    story("da-kenh-video", "Phục hồi đa kênh và video", "extra", [
        S("Vấn đề", "Nhiều kênh, nhiều khung", [
            P("Ảnh màu có ba kênh, ảnh vệ tinh có nhiều băng, video có nhiều khung. Các kênh và khung liên quan chặt với nhau.", "Kênh, băng, khung liên quan nhau"),
        ]),
        S("Ý tưởng", "Khai thác tương quan giữa các kênh", [
            P("Ngoài tương quan trong từng kênh, khai thác thêm tương quan giữa các kênh, nên phục hồi tốt hơn xử lý riêng lẻ.", "Thêm tương quan giữa kênh"),
            P("Hai phương pháp: LMMSE dựa trên ma trận hiệp phương sai của nhiễu và ảnh; RWLS có thêm tham số điều chỉnh.", "LMMSE, RWLS"),
        ]),
        S("Cách làm", "Chuyển động trong video", [
            P("Phát hiện chuyển động xác định vùng chuyển động giữa hai thời điểm, chủ yếu cho camera tĩnh. Vì cường độ đổi cả do nhiễu và ánh sáng, dùng kiểm định giả thuyết với ngưỡng cố định hoặc thích ứng.",
              "Phát hiện: kiểm định giả thuyết với ngưỡng"),
            P("Ước lượng chuyển động cần ba yếu tố: mô hình chuyển động, tiêu chí ước lượng trong miền pixel hoặc tần số, và chiến lược tìm kiếm.",
              "Ước lượng: mô hình, tiêu chí, tìm kiếm"),
            P("Video có dữ liệu rất lớn, nên phương pháp phục hồi phải đủ nhẹ. Ứng dụng: thiên văn, pháp y, ảnh y tế.", "Video: phương pháp phải nhẹ"),
        ]),
        traps([["Vì sao phục hồi đa kênh tốt hơn?", "Khai thác tương quan giữa các kênh"], ["Ba yếu tố của ước lượng chuyển động?", "Mô hình, tiêu chí, chiến lược tìm kiếm"]],
              ["Bẫy một: phục hồi đa kênh tốt hơn vì khai thác thêm tương quan giữa các kênh.",
               "Bẫy hai: ước lượng chuyển động cần mô hình chuyển động, tiêu chí ước lượng và chiến lược tìm kiếm."]),
    ]),

    story("tong-ket", "Tổng kết chương 3", "summary", [
        S("Tổng kết", "Phục hồi ảnh trong một mạch", [
            P("Nhìn lại biển số ban đêm. Mô hình g bằng h tích chập f cộng nhiễu; mỗi loại nhiễu có hàm mật độ riêng."),
            P("Bộ lọc trung bình chọn theo loại nhiễu, notch xóa nhiễu tuần hoàn. Lọc nghịch đảo nhạy nhiễu, Wiener kiềm chế bằng tỉ lệ nhiễu trên tín hiệu, CLS bỏ được yêu cầu phổ ảnh gốc."),
            P("Wavelet khử nhiễu mà giữ cạnh, CT tái tạo bằng chiếu ngược, và phục hồi đa kênh khai thác tương quan giữa các kênh."),
        ], chain=chain(CHAIN, len(CHAIN))),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: contraharmonic Q dương diệt tiêu, Q âm diệt muối."), P("Hai: harmonic thất bại với tiêu."), P("Ba: notch reject là tích thông cao dời tâm."),
            P("Bốn: Wiener với K bằng không là lọc nghịch đảo."), P("Năm: CLS chỉnh gamma lặp, không cần phổ ảnh gốc."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["Contraharmonic Q?", "Q > 0 diệt tiêu, Q < 0 diệt muối"], ["Harmonic?", "Thất bại với tiêu"], ["Notch reject?", "Tích thông cao dời tâm"],
                           ["Wiener K = 0?", "Lọc nghịch đảo"], ["CLS?", "γ lặp, không cần phổ gốc"]]}),
        S("Tổng kết", "Sang chương 4", [
            P("Chương bốn đi sâu vào các phép biến đổi ảnh, như DCT và wavelet, mà ta đã dùng ở đây và sẽ dùng lại khi nén ảnh.", "Chương 4: các phép biến đổi"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–5", "Biển số mờ và nhiễu", "—", "g = h*f + n; bài toán ngược", "→ Mô hình nhiễu"],
    ["Mô hình nhiễu", "6–12", "Biết nhiễu để chọn lọc", "Một bộ lọc cho mọi ảnh", "PDF: Gauss, Rayleigh, Erlang, mũ, đều, muối tiêu", "→ Bộ lọc trung bình"],
    ["Bộ lọc trung bình", "13–17", "Điểm tiêu giữa vùng phẳng", "Trung bình cộng", "Geometric, harmonic, contraharmonic Q; median/max/min", "Nhiễu tuần hoàn → notch"],
    ["Notch", "18–24", "Sọc nhiễu đều", "Lọc không gian", "Đốm trong phổ; tích thông cao dời tâm", "Còn mờ → hàm suy giảm"],
    ["Hàm suy giảm", "25–30", "Ảnh mờ thế nào", "—", "Quan sát, thực nghiệm, mô hình; giải chập mù", "→ Nghịch đảo"],
    ["Lọc nghịch đảo", "33", "Đảo ngược H", "Chỉ làm mượt", "G/H; nhiễu bùng nổ khi H→0", "→ Wiener"],
    ["Wiener", "32–34", "Không khuếch đại nhiễu", "Nghịch đảo", "Thêm K = Sn/Sf; MMSE", "Cần phổ gốc → CLS"],
    ["CLS", "35–37", "Không có phổ gốc", "Wiener", "Laplacian + ràng buộc; γ lặp", "Không theo vị trí → wavelet"],
    ["Wavelet", "31", "Khử nhiễu giữ cạnh", "Lọc trung bình, tần số", "Phân rã → ngưỡng mềm/cứng → ngược", "Bên trong vật → CT"],
    ["CT", "38–44", "Lát cắt bên trong", "X quang chồng lớp", "Backprojection nhiều góc", "→ Đa kênh"],
    ["Đa kênh & video", "45–55", "Nhiều kênh, khung", "—", "LMMSE, RWLS; phát hiện, ước lượng chuyển động", "→ Tổng kết"],
    ["Tổng kết", "—", "—", "—", "Bẫy chung", "→ Chương 4"],
]
write(3, "Phục hồi ảnh", EX, stories, MAP)
