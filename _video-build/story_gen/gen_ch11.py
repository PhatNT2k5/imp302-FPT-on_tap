import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from story_kit import P, S, intro, limit, pipeline, story, traps, write  # noqa: E402

CHAIN = ["IoU & mAP", "Cửa sổ trượt", "Họ R-CNN", "YOLO & SSD", "Anchor-free", "Transformer (DETR)"]
EX = "Camera của một chiếc xe tự lái: tìm người đi bộ, xe khác và biển báo trên đường phố"


def overlap_grid(label, rows, cols, truth, pred):
    """truth / pred: (x0, y0, x1, y1) in cells; returns a grid with T, D and ∩ cells."""
    cells, accent, warn = [], [], []
    for r in range(rows):
        row = []
        for c in range(cols):
            in_t = truth[0] <= c < truth[2] and truth[1] <= r < truth[3]
            in_p = pred[0] <= c < pred[2] and pred[1] <= r < pred[3]
            row.append("∩" if in_t and in_p else "T" if in_t else "D" if in_p else "")
            if in_t and in_p:
                accent.append([r, c])
            elif in_p:
                warn.append([r, c])
        cells.append(row)
    return {"label": label, "cells": cells, "accent": accent, "warn": warn}


stories = [
    intro("mo-dau", "Mở đầu: cái gì, và ở đâu?", "Xe tự lái nhìn đường phố", [
        P("Chào các bạn. Chương mười một là phát hiện đối tượng. Ví dụ của cả chương: camera trên một chiếc xe tự lái. "
          "Trong mỗi khung hình có người đi bộ, xe khác, biển báo.", "Ví dụ: camera xe tự lái"),
        P("Phân loại ảnh chỉ nói cả ảnh là gì. Định vị nói thêm vật ở đâu bằng một khung chữ nhật. "
          "Phát hiện đối tượng làm cả hai cho mọi vật: mỗi vật một nhãn và một khung, gọi là bounding box.", "Phát hiện = phân loại + định vị"),
        P("Thử nghĩ trước: nếu xe tự lái khoanh trúng người đi bộ nhưng khung lệch một chút, như vậy đã tính là đúng chưa?",
          "Khung lệch một chút có tính là đúng?", ask=True),
    ], CHAIN, [
        P("Ta bắt đầu bằng cách chấm điểm: IoU cho từng khung, mAP cho cả mô hình.", "Chấm điểm: IoU, mAP"),
        P("Rồi đi theo lịch sử: cửa sổ trượt truyền thống, họ R-CNN hai giai đoạn, YOLO và SSD một giai đoạn, "
          "nhóm không dùng anchor, và cuối cùng là Transformer.", "Cửa sổ trượt → R-CNN → YOLO/SSD → anchor-free → DETR"),
        P("Mỗi đời sinh ra để vá điểm yếu của đời trước, các bạn xem theo thứ tự nhé.", "Xem theo thứ tự"),
    ]),

    story("iou-map", "Chấm điểm bộ phát hiện: IoU và mAP", "method", [
        S("Vấn đề", "Khung lệch một chút có tính là đúng?", [
            P("Bộ phát hiện đưa ra rất nhiều khung. Ta cần một con số nói khung nào khớp với vật thật, và một con số chấm cả mô hình.",
              "Cần chấm từng khung và cả mô hình"),
        ]),
        S("Cách cũ", "Độ chính xác của phân loại", [
            P("Với phân loại ảnh, chấm điểm rất đơn giản: đoán đúng nhãn hay sai nhãn.", "Phân loại: đúng nhãn hay sai"),
            P("Nhưng phát hiện còn có vị trí. Đúng nhãn mà khung lệch hẳn sang bên cạnh thì vẫn vô dụng với xe tự lái.",
              "Không chấm được vị trí"),
        ]),
        S("Ý tưởng", "Hai khung chồng lên nhau bao nhiêu?", [
            P("Lấy khung thật do người gán nhãn vẽ, gọi là ground truth, và khung dự đoán. Phần hai khung chồng nhau càng lớn so với tổng vùng chúng phủ, dự đoán càng tốt.",
              "Chồng nhau càng nhiều càng tốt"),
            P("Đó là IoU, Intersection over Union: giao chia hợp.", "IoU = giao / hợp"),
        ]),
        S("Công thức", "IoU", [
            P("Tử số là diện tích phần chồng nhau. Mẫu số là diện tích vùng hai khung cùng phủ, phần chồng chỉ tính một lần.", "Giao trên, hợp dưới"),
            P("Không chạm nhau thì IoU bằng không, trùng khít thì bằng một. Càng gần một càng khớp.", "0 → không chạm · 1 → trùng khít"),
            P("Lưu ý: slide gốc in ngược phân số. Đúng theo tên gọi và theo ý nghĩa gần một là tốt, công thức phải là giao chia hợp.",
              "Slide in ngược: nhớ giao / hợp"),
        ], formula=r"IoU = \frac{\overbrace{\text{Area of intersection}}^{\text{phần chồng nhau}}}{\underbrace{\text{Area of union}}_{\text{phần cùng phủ, tính một lần}}}"),
        S("Cách làm", "Tính IoU bằng tay", [
            P("Khung thật là ô vuông bốn nhân bốn, diện tích mười sáu. Dự đoán thứ nhất lệch chéo hai ô. Phần giao, ký hiệu giao, là hai nhân hai bằng bốn ô.",
              "T = chỉ khung thật · D = chỉ dự đoán · ∩ = phần giao", reveal=1),
            P("Phần hợp: tổng hai khung trừ phần giao vì bị đếm hai lần, ba mươi hai trừ bốn bằng hai mươi tám. IoU là bốn phần hai mươi tám, khoảng không phẩy một bốn.",
              reveal=1),
            P("Thử đoán: dự đoán thứ hai chỉ lệch ngang một ô. IoU sẽ là bao nhiêu?", reveal=1, ask=True),
            P("Phần giao rộng ba, cao bốn, bằng mười hai. Hợp là ba mươi hai trừ mười hai bằng hai mươi. IoU bằng không phẩy sáu.", reveal=2),
            P("Thực tế người ta đặt ngưỡng, thường là không phẩy năm. Vượt ngưỡng thì tính là phát hiện đúng: dự đoán thứ hai đạt, dự đoán thứ nhất thì không.",
              reveal=2),
        ], grid=[overlap_grid("Lệch chéo: IoU = 4/28 ≈ 0,14", 6, 6, (0, 0, 4, 4), (2, 2, 6, 6)),
                 overlap_grid("Lệch ngang: IoU = 12/20 = 0,6", 4, 5, (0, 0, 4, 4), (1, 0, 5, 4))]),
        S("Cách làm", "Precision, recall và AP", [
            P("Để chấm cả mô hình, cần hai khái niệm. Precision: trong các khung mô hình đưa ra, bao nhiêu phần là đúng.", "Precision: khung đưa ra đúng bao nhiêu"),
            P("Recall: trong các vật có thật, mô hình tìm ra bao nhiêu phần. Đưa nhiều khung thì recall tăng nhưng precision giảm, hai đại lượng kéo nhau.",
              "Recall: vật thật tìm ra bao nhiêu"),
            P("Average Precision, AP, tóm tắt sự đánh đổi đó thành một con số cho một lớp, suy ra từ đường cong precision recall. mAP là trung bình AP trên K lớp, mAR là trung bình recall trung bình trên K lớp.",
              "AP từ đường cong P–R · mAP, mAR: trung bình trên K lớp"),
        ]),
        S("Cách làm", "Tính AP cho lớp người đi bộ", [
            P("Có bốn người đi bộ thật. Mô hình đưa ra năm khung, xếp theo độ tin cậy giảm dần. Khung một đúng: precision một, recall không phẩy hai lăm.", reveal=1),
            P("Khung hai sai: precision tụt còn không phẩy năm, recall giữ nguyên.", reveal=2),
            P("Khung ba đúng: precision khoảng không phẩy sáu bảy, recall không phẩy năm.", reveal=3),
            P("Khung bốn đúng: precision và recall đều là không phẩy bảy lăm.", reveal=4),
            P("Khung năm sai: precision còn không phẩy sáu, recall dừng ở không phẩy bảy lăm. Người đi bộ thứ tư không bao giờ được tìm thấy.", reveal=5),
            P("AP: recall tăng qua ba bậc, mỗi bậc rộng không phẩy hai lăm. Ở mỗi bậc lấy precision tốt nhất từ đó trở đi: một, không phẩy bảy lăm, không phẩy bảy lăm. "
              "Cộng lại, AP bằng không phẩy sáu hai lăm.", reveal=5),
        ], table={"headers": ["Khung (theo độ tin cậy)", "Đúng / Sai", "Precision", "Recall"],
                  "rows": [["1", "Đúng", "1/1 = 1,00", "1/4 = 0,25"], ["2", "Sai", "1/2 = 0,50", "0,25"], ["3", "Đúng", "2/3 ≈ 0,67", "2/4 = 0,50"],
                           ["4", "Đúng", "3/4 = 0,75", "3/4 = 0,75"], ["5", "Sai", "3/5 = 0,60", "0,75"]]}),
        S("So sánh", "IoU, AP và mAP", [
            P("IoU chấm một khung so với vật thật."),
            P("AP chấm một lớp, gộp cả precision lẫn recall."),
            P("mAP và mAR chấm cả mô hình trên mọi lớp."),
        ], table={"headers": ["Độ đo", "Chấm cái gì", "Tính từ"],
                  "rows": [["IoU", "Một khung", "Giao / hợp"], ["AP", "Một lớp", "Đường cong precision – recall"],
                           ["mAP / mAR", "Cả mô hình", "Trung bình AP / AR trên K lớp"]]}),
        S("Ứng dụng", "Chấm trên bộ dữ liệu chuẩn", [
            P("Muốn so các mô hình phải chấm trên cùng bộ dữ liệu. PASCAL VOC có khoảng mười nghìn ảnh, hai mươi lớp."),
            P("COCO có khoảng hai trăm nghìn ảnh, tám mươi lớp."),
            P("ImageNet của cuộc thi ILSVRC có khoảng mười bốn triệu ảnh, hai trăm lớp cho phát hiện."),
            P("Open Images có khoảng chín triệu ảnh, sáu trăm lớp. Các số lớp hai mươi, tám mươi, hai trăm, sáu trăm rất hay được hỏi."),
        ], table={"headers": ["Bộ dữ liệu", "Số ảnh (xấp xỉ)", "Số lớp"],
                  "rows": [["PASCAL VOC", "10 nghìn", "20"], ["COCO", "200 nghìn", "80"], ["ImageNet (ILSVRC)", "14 triệu", "200"], ["Open Images", "9 triệu", "600"]]}),
        limit("Biết chấm, nhưng khung từ đâu ra?", [
            P("Giờ ta biết chấm một bộ phát hiện. Câu hỏi tiếp: làm sao sinh ra các khung ứng viên ngay từ đầu?", "Khung ứng viên từ đâu ra?"),
            P("Cách đầu tiên người ta nghĩ đến: thử mọi vị trí. Đó là cửa sổ trượt.", "→ Cửa sổ trượt"),
        ], CHAIN, 2),
        traps([["IoU gần 1 nghĩa là gì?", "Khung dự đoán khớp rất sát khung thật"], ["mAP là trung bình của gì?", "AP trên K lớp; AP từ đường cong P–R"],
               ["COCO có bao nhiêu lớp?", "80 (VOC 20, ImageNet 200, Open Images 600)"]],
              ["Bẫy một: IoU gần một là khớp tốt, và công thức là giao chia hợp.",
               "Bẫy hai: mAP là trung bình AP trên các lớp, không phải trung bình precision.",
               "Bẫy ba: nhớ số lớp, VOC hai mươi, COCO tám mươi, ImageNet hai trăm, Open Images sáu trăm."]),
    ]),

    story("cua-so-truot", "Phương pháp truyền thống: cửa sổ trượt", "method", [
        S("Vấn đề", "Người đi bộ có thể ở bất kỳ đâu", [
            P("Người đi bộ có thể ở bất kỳ đâu trong khung hình, gần thì to, xa thì nhỏ, đứng thì cao, ngồi thì thấp.", "Vị trí, kích thước, tỉ lệ bất kỳ"),
        ]),
        S("Cách cũ", "Bộ phân loại chỉ nhìn cả ảnh", [
            P("Một bộ phân loại ảnh chỉ trả lời cả ảnh là gì. Nó không biết vật nằm ở đâu.", "Phân loại: không biết vị trí"),
        ]),
        S("Ý tưởng", "Soi từng ô bằng kính lúp", [
            P("Ý tưởng: trượt một cửa sổ qua khắp ảnh, như cầm kính lúp soi từng ô. Ở mỗi ô hỏi bộ phân loại: có người đi bộ ở đây không?",
              "Trượt cửa sổ, hỏi từng ô"),
            P("Pipeline truyền thống gồm ba bước: chọn vị trí có khả năng chứa thông tin, trích đặc trưng như SIFT, HOG, đường biên, rồi phân loại.",
              "Chọn vị trí → trích đặc trưng → phân loại"),
        ]),
        S("Cách làm", "Đếm số cửa sổ", [
            P("Ảnh sáu trăm bốn mươi nhân bốn trăm tám mươi, cửa sổ sáu mươi tư nhân sáu mươi tư, mỗi lần dịch tám pixel. Theo chiều ngang có bảy mươi ba vị trí.", reveal=1),
            P("Theo chiều dọc có năm mươi ba vị trí.", reveal=2),
            P("Thử đoán: riêng một kích thước cửa sổ đã có bao nhiêu cửa sổ?", reveal=2, ask=True),
            P("Ba nghìn tám trăm sáu mươi chín cửa sổ, cái nào cũng phải trích đặc trưng và chạy bộ phân loại.", reveal=3),
            P("Vật to nhỏ, cao dẹt khác nhau nên phải lặp với nhiều tỉ lệ và nhiều hình dạng. Lên tới hàng chục nghìn cửa sổ mỗi ảnh, gần như tất cả chỉ chứa nền.", reveal=4),
        ], table={"headers": ["Đại lượng", "Phép tính", "Kết quả"],
                  "rows": [["Vị trí ngang", "(640 − 64) / 8 + 1", "73"], ["Vị trí dọc", "(480 − 64) / 8 + 1", "53"], ["Một tỉ lệ", "73 × 53", "3 869"],
                           ["Nhiều tỉ lệ, hình dạng", "3 869 × số tỉ lệ × số hình dạng", "hàng chục nghìn"]]}),
        S("So sánh", "Ba mốc của phương pháp truyền thống", [
            P("Năm hai nghìn linh một, bộ phân loại nhị phân."),
            P("Năm hai nghìn linh năm, Histogram of Oriented Gradient, HOG."),
            P("Năm hai nghìn linh chín, Deformable Part Model. Cả ba đều dùng đặc trưng thủ công do con người thiết kế."),
        ], table={"headers": ["Năm", "Phương pháp", "Ghi nhớ"],
                  "rows": [["2001", "Bộ phân loại nhị phân", "Mốc đầu"], ["2005", "HOG", "Histogram hướng gradient"], ["2009", "Deformable Part Model", "Vật gồm nhiều phần"]]}),
        S("Ứng dụng", "Thời kỳ trước học sâu", [
            P("Các bộ phát hiện khuôn mặt và người đi bộ đời đầu trong máy ảnh và camera đều theo kiểu cửa sổ trượt với đặc trưng thủ công.",
              "Phát hiện khuôn mặt, người đi bộ đời đầu"),
        ]),
        limit("Quá nhiều cửa sổ vô ích", [
            P("Chi phí tính toán rất cao, và sinh ra rất nhiều ứng viên vô ích. Đặc trưng thủ công lại kém linh hoạt.", "Tốn kém, ứng viên vô ích, đặc trưng thủ công"),
            P("Học sâu giải cả hai: đề xuất ít vùng đáng xem hơn, và để mạng tự học đặc trưng. Đó là họ R-CNN.", "→ Họ R-CNN"),
        ], CHAIN, 3),
        traps([["Ba bước của pipeline truyền thống?", "Chọn vị trí, trích đặc trưng, phân loại"],
               ["Vì sao cửa sổ trượt tốn kém?", "Nhiều vị trí × nhiều tỉ lệ × nhiều hình dạng"],
               ["HOG ra đời năm nào?", "2005 (nhị phân 2001, DPM 2009)"]],
              ["Bẫy một: pipeline truyền thống là chọn vị trí, trích đặc trưng, rồi phân loại.",
               "Bẫy hai: chi phí đến từ việc quét nhiều vị trí, nhiều tỉ lệ, nhiều hình dạng.",
               "Bẫy ba: dòng thời gian là hai nghìn linh một, hai nghìn linh năm với HOG, và hai nghìn linh chín với Deformable Part Model."]),
    ]),

    story("r-cnn", "Anchor và họ R-CNN", "method", [
        S("Vấn đề", "Bớt cửa sổ vô ích, để máy tự học đặc trưng", [
            P("Xe tự lái không thể chờ hàng chục nghìn lần phân loại cho mỗi khung hình. Cần ít ứng viên hơn, và đặc trưng tốt hơn.",
              "Ít ứng viên hơn, đặc trưng tốt hơn"),
        ]),
        S("Cách cũ", "Cửa sổ trượt và đặc trưng thủ công", [
            P("Cửa sổ trượt thử mọi chỗ một cách mù quáng, và đặc trưng do con người thiết kế.", "Thử mù quáng, đặc trưng thủ công"),
        ]),
        S("Ý tưởng", "Khuôn có sẵn và hai giai đoạn", [
            P("Anchor box là một tập khung mẫu định nghĩa trước, nhiều kích thước và tỉ lệ, rải dày trên ảnh, như những khuôn có sẵn.",
              "Anchor: khuôn có sẵn nhiều cỡ"),
            P("Anchor khớp đủ tốt với vật thật, đo bằng IoU, là mẫu dương; chỉ chứa nền là mẫu âm. Mô hình chỉ cần dự đoán lớp và độ lệch để khớp khuôn với vật.",
              "Dương / âm theo IoU; dự đoán độ lệch"),
            P("Họ R-CNN làm theo hai giai đoạn, giống người đọc kỹ: lướt tìm chỗ đáng chú ý, rồi mới xem từng chỗ.", "Hai giai đoạn: đề xuất → phân loại"),
        ]),
        S("Cách làm", "Ba đời R-CNN", [
            P("R-CNN dùng selective search sinh rất nhiều khung ứng viên, mỗi khung qua mạng tích chập riêng để trích đặc trưng, rồi SVM phân loại và hồi quy tuyến tính chỉnh vị trí. Đơn giản nhưng chậm.",
              reveal=1),
            P("Fast R-CNN thêm RoI pooling đưa mọi vùng về kích thước cố định, nên mạng tích chập chỉ chạy một lần cho cả ảnh, cùng mô hình đa nhiệm. "
              "Theo slide, chính xác hơn mười một phẩy năm phần trăm và nhanh hơn hơn hai trăm lần.", reveal=2),
            P("Thử đoán: sau Fast R-CNN, khâu nào còn chậm nhất?", reveal=2, ask=True),
            P("Selective search. Faster R-CNN thay nó bằng mạng đề xuất vùng RPN, dùng chung đặc trưng với mạng phát hiện. Cả quy trình nằm trong một mạng, học từ đầu đến cuối.",
              reveal=3),
        ], table={"headers": ["Mô hình", "Sinh ứng viên", "Điểm mới", "Ghi nhớ"],
                  "rows": [["R-CNN", "Selective search", "CNN + SVM + hồi quy tuyến tính", "Đơn giản nhưng chậm"],
                           ["Fast R-CNN", "Selective search", "RoI pooling + đa nhiệm", "+11,5% chính xác, nhanh hơn 200 lần"],
                           ["Faster R-CNN", "RPN", "RPN chia sẻ đặc trưng", "Một mạng, end-to-end"]]}),
        S("Cách làm", "Đường đi của một ảnh qua Faster R-CNN", [
            P("Ảnh đi qua mạng tích chập xương sống đúng một lần, cho bản đồ đặc trưng.", "Backbone CNN: chạy một lần", reveal=1),
            P("Mạng đề xuất vùng chọn những anchor có khả năng chứa vật.", "RPN chọn anchor có vật", reveal=2),
            P("RoI pooling cắt phần tương ứng và đưa về kích thước cố định.", "RoI pooling: kích thước cố định", reveal=3),
            P("Hai nhánh song song: phân loại, và hồi quy tinh chỉnh khung.", "Phân loại + hồi quy khung", reveal=4),
        ], graph=pipeline(["Ảnh", "Backbone CNN", "RPN (anchor)", "RoI pooling", "Phân loại + hồi quy khung"], [0, 1, 2, 3, 4])),
        S("So sánh", "So với cửa sổ trượt", [
            P("Cửa sổ trượt thử hàng chục nghìn ô; R-CNN chỉ xem các vùng được đề xuất."),
            P("Đặc trưng thủ công được thay bằng đặc trưng do CNN tự học."),
            P("Faster R-CNN gộp mọi khâu vào một mạng, chính xác cao, nhưng vẫn chậm hơn các mô hình một giai đoạn."),
        ], table={"headers": ["", "Cửa sổ trượt", "Faster R-CNN"],
                  "rows": [["Ứng viên", "Mọi vị trí, mọi tỉ lệ", "Anchor được RPN chọn"], ["Đặc trưng", "Thủ công", "CNN tự học"],
                           ["Tốc độ", "Rất chậm", "Nhanh hơn nhiều, vẫn 2 giai đoạn"]]}),
        S("Ứng dụng", "Họ R-CNN ở đâu", [
            P("Faster R-CNN là mô hình nền của nhiều hệ thống cần độ chính xác cao. Mask R-CNN ở chương chín chính là Faster R-CNN thêm một nhánh vẽ mặt nạ cho phân đoạn thực thể.",
              "Mask R-CNN = Faster R-CNN + nhánh mặt nạ"),
        ]),
        limit("Hai giai đoạn vẫn chậm cho thời gian thực", [
            P("Hai giai đoạn nghĩa là mỗi ảnh phải đề xuất rồi mới xét từng vùng. Xe tự lái chạy ba mươi khung hình mỗi giây thì cần nhanh hơn nữa.",
              "Cần nhanh hơn cho thời gian thực"),
            P("Nếu bỏ hẳn giai đoạn đề xuất thì sao? Đó là YOLO và SSD.", "→ YOLO & SSD"),
        ], CHAIN, 4),
        traps([["Fast R-CNN nhanh nhờ đâu?", "RoI pooling + mô hình đa nhiệm"], ["Faster R-CNN thay selective search bằng gì?", "Region Proposal Network (RPN)"],
               ["Anchor dương / âm dựa vào gì?", "Độ khớp IoU với vật thật"]],
              ["Bẫy một: Fast R-CNN nhanh nhờ RoI pooling và mô hình đa nhiệm. Nhớ mười một phẩy năm phần trăm và hai trăm lần.",
               "Bẫy hai: Faster R-CNN thay selective search bằng mạng đề xuất vùng RPN chia sẻ đặc trưng.",
               "Bẫy ba: anchor được gán dương hay âm theo độ khớp IoU với vật thật."]),
    ]),

    story("yolo-ssd", "Một giai đoạn: YOLO và SSD", "method", [
        S("Vấn đề", "Ba mươi khung hình mỗi giây", [
            P("Xe đang chạy, mỗi giây ba mươi khung hình. Bộ phát hiện phải trả lời gần như tức thì.", "Cần gần thời gian thực"),
        ]),
        S("Cách cũ", "Đề xuất rồi mới xét", [
            P("Họ R-CNN đi hai bước: đề xuất vùng, rồi phân loại từng vùng. Bước nào cũng tốn thời gian.", "Hai giai đoạn: tốn thời gian"),
        ]),
        S("Ý tưởng", "Liếc một cái là xong", [
            P("Bộ phát hiện một giai đoạn giống người liếc một cái là thấy hết. YOLO, You Only Look Once, dự đoán trực tiếp khung và lớp trong một lần truyền qua mạng.",
              "YOLO: một lần nhìn, ra cả khung lẫn lớp"),
            P("Bỏ giai đoạn đề xuất giúp rất nhanh, gần thời gian thực. Đó là thứ YOLO đánh đổi để có.", "Đổi lấy tốc độ"),
        ]),
        S("Cách làm", "SSD: dự đoán ở nhiều tỉ lệ", [
            P("SSD, Single Shot Detector, cũng một giai đoạn. Nó dự đoán điểm số lớp và độ lệch khung cho một tập khung mặc định cố định, bằng các bộ lọc tích chập nhỏ trên bản đồ đặc trưng.",
              "Khung mặc định + bộ lọc tích chập nhỏ"),
            P("Thử đoán: một chiếc xe ở xa rất nhỏ, một chiếc ở gần rất to. Một bản đồ đặc trưng có đủ cho cả hai không?", "Thử đoán: một tỉ lệ có đủ?", ask=True),
            P("Không. SSD dự đoán trên nhiều bản đồ đặc trưng: bản đồ độ phân giải cao lo vật nhỏ, bản đồ độ phân giải thấp lo vật lớn. Nó cũng tách riêng dự đoán theo tỉ lệ khung hình.",
              "Phân giải cao → vật nhỏ · thấp → vật lớn"),
        ]),
        S("So sánh", "Hai giai đoạn so với một giai đoạn", [
            P("Hai giai đoạn như họ R-CNN: đề xuất vùng rồi phân loại, chính xác nhưng chậm hơn."),
            P("Một giai đoạn như YOLO, SSD: dự đoán thẳng trong một lượt, nhanh, gần thời gian thực."),
            P("Cả hai nhóm, theo slide, vẫn dựa trên anchor hoặc khung mặc định."),
        ], table={"headers": ["", "Hai giai đoạn", "Một giai đoạn"],
                  "rows": [["Đại diện", "R-CNN, Fast, Faster", "YOLO, SSD"], ["Cách làm", "Đề xuất → phân loại", "Dự đoán thẳng một lượt"],
                           ["Đánh đổi", "Chính xác hơn, chậm hơn", "Nhanh, gần thời gian thực"]]}),
        S("Ứng dụng", "Khi nào cần một giai đoạn", [
            P("Camera giám sát thời gian thực, robot, thiết bị di động, xe tự lái: những nơi cần trả lời ngay thường chọn họ YOLO hoặc SSD.",
              "Giám sát, robot, di động, xe tự lái"),
        ]),
        limit("Vẫn phải thiết kế anchor bằng tay", [
            P("Dù một hay hai giai đoạn, ta vẫn phải chọn kích thước và tỉ lệ anchor bằng tay, và phần lớn anchor chỉ chứa nền.", "Anchor: siêu tham số tay, đa số là nền"),
            P("Có cách nào bỏ hẳn anchor không? Video sau: anchor-free.", "→ Anchor-free"),
        ], CHAIN, 5),
        traps([["YOLO thuộc nhóm nào?", "Một giai đoạn (theo slide: dựa trên anchor)"], ["SSD chính xác nhờ đâu?", "Dự đoán ở nhiều tỉ lệ bản đồ đặc trưng"],
               ["YOLO đánh đổi gì?", "Lấy tốc độ, gần thời gian thực"]],
              ["Bẫy một: YOLO và SSD là một giai đoạn, và trong slide được xếp vào nhóm dựa trên anchor.",
               "Bẫy hai: SSD chính xác nhờ dự đoán trên nhiều bản đồ đặc trưng có độ phân giải khác nhau.",
               "Bẫy ba: YOLO bỏ giai đoạn đề xuất vùng để đổi lấy tốc độ."]),
    ]),

    story("anchor-free", "Không dùng anchor: CornerNet và FCOS", "method", [
        S("Vấn đề", "Khuôn chọn sai thì mô hình kém", [
            P("Biển báo nhỏ, xe buýt dài, người đi bộ cao gầy: chọn bộ anchor không hợp với dữ liệu thì hiệu năng giảm mạnh.", "Anchor không hợp dữ liệu"),
        ]),
        S("Cách cũ", "Ba vấn đề của anchor", [
            P("Một: kích thước và tỉ lệ anchor là siêu tham số con người chọn, mô hình khó tổng quát hóa.", "1. Siêu tham số tay"),
            P("Hai: phần lớn anchor chỉ chứa nền, mất cân bằng nghiêm trọng giữa mẫu âm và mẫu dương.", "2. Mất cân bằng âm / dương"),
            P("Ba: ngay cả anchor dương vẫn mơ hồ về vị trí và lẫn nhiễu nền.", "3. Mơ hồ vị trí, nhiễu nền"),
        ]),
        S("Ý tưởng", "Tìm điểm, không cần khuôn", [
            P("Thay vì so với khuôn có sẵn, hãy tìm thẳng những điểm đặc biệt của vật: các góc của khung, hoặc tâm của vật.", "Tìm góc hoặc điểm, không cần khuôn"),
        ]),
        S("Cách làm", "Hai nhánh không dùng anchor", [
            P("Nhánh dựa trên điểm khóa biểu diễn khung bằng các góc thưa. CornerNet giới thiệu corner pooling, một lớp pooling mới giúp mạng định vị góc của khung tốt hơn.",
              "Điểm khóa: CornerNet, corner pooling"),
            P("Nhánh dựa trên điểm neo có đại diện FCOS, bộ phát hiện một giai đoạn tích chập hoàn toàn. Nó dự đoán trực tiếp tại từng vị trí trên bản đồ đặc trưng, không cần anchor nào.",
              "Điểm neo: FCOS dự đoán tại từng vị trí"),
        ]),
        S("So sánh", "Anchor so với anchor-free", [
            P("Nhóm dựa trên anchor cần chọn trước kích thước và tỉ lệ khuôn."),
            P("Nhóm anchor-free bỏ được siêu tham số đó, và bớt mất cân bằng âm dương."),
            P("Đại diện anchor-free là CornerNet với các góc và FCOS với các điểm."),
        ], table={"headers": ["", "Dựa trên anchor", "Anchor-free"],
                  "rows": [["Đại diện", "Faster R-CNN, YOLO, SSD", "CornerNet, FCOS"], ["Siêu tham số khuôn", "Có", "Không"],
                           ["Biểu diễn khung", "Khuôn + độ lệch", "Góc, hoặc điểm + khoảng cách"]]}),
        S("Ứng dụng", "Anchor-free ở đâu", [
            P("Ý tưởng tìm điểm thay vì khuôn được dùng rộng rãi trong các bộ phát hiện hiện đại, nhất là khi vật có hình dạng rất đa dạng.",
              "Vật có hình dạng đa dạng"),
        ]),
        limit("CNN chỉ nhìn cục bộ", [
            P("Dù có anchor hay không, CNN vẫn trích đặc trưng bằng các cửa sổ tích chập nhỏ, mỗi cửa sổ chỉ thấy một vùng hẹp. Khó nắm thông tin toàn cục.",
              "CNN: cửa sổ cục bộ"),
            P("Video sau dùng Transformer để mọi vị trí nhìn thấy mọi vị trí khác.", "→ Transformer"),
        ], CHAIN, 6),
        traps([["Mô hình nào là anchor-free?", "CornerNet, FCOS (YOLO, SSD thì không)"], ["CornerNet có gì mới?", "Corner pooling"],
               ["Ba vấn đề của anchor?", "Siêu tham số tay, mất cân bằng âm/dương, mơ hồ vị trí"]],
              ["Bẫy một: anchor-free là CornerNet và FCOS. YOLO và SSD không thuộc nhóm này.",
               "Bẫy hai: điểm mới của CornerNet là corner pooling.",
               "Bẫy ba: ba vấn đề của anchor là siêu tham số tay, mất cân bằng âm dương, và mơ hồ vị trí."]),
    ]),

    story("transformer", "Phát hiện bằng Transformer: DETR", "method", [
        S("Vấn đề", "Hiểu cả khung cảnh", [
            P("Một người đứng cạnh vạch kẻ đường có khả năng sắp băng qua. Hiểu được điều đó cần nhìn quan hệ giữa các vùng xa nhau trong ảnh.",
              "Cần quan hệ giữa các vùng xa nhau"),
        ]),
        S("Cách cũ", "Cửa sổ tích chập độc lập", [
            P("CNN trích đặc trưng bằng các cửa sổ tích chập trượt độc lập, nên khó thu thông tin toàn cục một cách hiệu quả.", "CNN khó nắm toàn cục"),
        ]),
        S("Ý tưởng", "Mọi vị trí nhìn thấy mọi vị trí", [
            P("Transformer cho mọi vị trí chú ý đến mọi vị trí khác, nắm được phụ thuộc tầm xa và thông tin toàn cục.", "Attention: phụ thuộc tầm xa"),
            P("Trong DETR, mỗi object query giống một người đi hỏi: ở đây có vật nào không?", "Object query: người đi hỏi"),
        ]),
        S("Cách làm", "Kiến trúc DETR", [
            P("Một backbone CNN học biểu diễn hai chiều của ảnh.", "Backbone CNN", reveal=1),
            P("Biểu diễn được làm phẳng và cộng thêm mã hóa vị trí.", "Làm phẳng + mã hóa vị trí", reveal=2),
            P("Bộ mã hóa transformer xử lý toàn bộ chuỗi đặc trưng.", "Bộ mã hóa transformer", reveal=3),
            P("Bộ giải mã nhận một số nhỏ cố định các embedding vị trí đã học, gọi là object queries, chú ý đến đầu ra bộ mã hóa để trả về từng vật.",
              "Bộ giải mã + object queries", reveal=4),
        ], graph=pipeline(["Ảnh", "Backbone CNN", "Làm phẳng + mã hóa vị trí", "Bộ mã hóa transformer", "Bộ giải mã (object queries)", "Lớp + khung"],
                          [0, 1, 2, 3, 4, 4])),
        S("So sánh", "CNN so với Transformer", [
            P("CNN nhìn cục bộ qua các cửa sổ; Transformer nhìn toàn cục qua cơ chế chú ý."),
            P("DETR dùng object queries thay cho anchor và đề xuất vùng."),
            P("Ngoài DETR còn có ViT và ViT-FRCNN áp dụng transformer cho phát hiện."),
        ], table={"headers": ["", "CNN (R-CNN, YOLO…)", "Transformer (DETR)"],
                  "rows": [["Tầm nhìn", "Cục bộ, cửa sổ tích chập", "Toàn cục, attention"], ["Sinh dự đoán", "Anchor / đề xuất / điểm", "Object queries"],
                           ["Biến thể", "—", "ViT, ViT-FRCNN"]]}),
        S("Ứng dụng", "Transformer trong thị giác", [
            P("Transformer đang là xu hướng chính trong thị giác máy tính, từ phát hiện đến phân đoạn và phân loại.", "Xu hướng chính hiện nay"),
        ]),
        limit("Mọi bộ phát hiện đều có khâu phân loại", [
            P("Dù là R-CNN, YOLO hay DETR, cuối cùng đều có một khâu trả lời: vật này thuộc lớp nào?", "Khâu phân loại có ở mọi nơi"),
            P("Chương mười hai sẽ mổ xẻ chính khâu đó.", "→ Chương 12: phân loại"),
        ], CHAIN, 6),
        traps([["Vì sao dùng Transformer?", "Nắm phụ thuộc tầm xa, thông tin toàn cục"], ["Object queries là gì?", "Embedding vị trí đã học, số lượng nhỏ cố định"],
               ["DETR đưa gì vào bộ mã hóa?", "Đặc trưng CNN đã làm phẳng + mã hóa vị trí"]],
              ["Bẫy một: Transformer được dùng vì nắm được phụ thuộc tầm xa, điều CNN làm kém.",
               "Bẫy hai: object queries là một số nhỏ cố định các embedding vị trí đã học, ở bộ giải mã.",
               "Bẫy ba: bộ mã hóa nhận đặc trưng CNN đã làm phẳng và cộng mã hóa vị trí."]),
    ]),

    story("tong-ket", "Tổng kết chương 11", "summary", [
        S("Tổng kết", "Từ cửa sổ trượt đến Transformer", [
            P("Nhìn lại cả chương với chiếc xe tự lái. IoU chấm từng khung, mAP chấm cả mô hình."),
            P("Cửa sổ trượt thử mọi chỗ nên rất tốn kém. Họ R-CNN đề xuất vùng rồi phân loại, Faster R-CNN gộp tất cả vào một mạng."),
            P("YOLO và SSD bỏ giai đoạn đề xuất để nhanh, anchor-free bỏ khuôn có sẵn, và DETR dùng Transformer để nhìn toàn cục."),
        ], chain={"items": CHAIN, "current": len(CHAIN)}),
        S("Tổng kết", "Bốn nhóm phương pháp học sâu", [
            P("Anchor hai giai đoạn: họ R-CNN, chính xác nhưng chậm hơn.", reveal=[1]),
            P("Anchor một giai đoạn: YOLO, SSD, nhanh gần thời gian thực.", reveal=[2]),
            P("Anchor-free: CornerNet, FCOS. Transformer: DETR, ViT-FRCNN.", reveal=[3, 4]),
        ], table={"headers": ["Nhóm", "Đại diện", "Ý chính"],
                  "rows": [["Anchor, 2 giai đoạn", "R-CNN, Fast, Faster", "Đề xuất rồi phân loại + hồi quy"], ["Anchor, 1 giai đoạn", "YOLO, SSD", "Dự đoán thẳng một lượt"],
                           ["Anchor-free", "CornerNet, FCOS", "Góc hoặc điểm"], ["Transformer", "DETR, ViT-FRCNN", "Attention, object queries"]]}),
        S("Bẫy thi", "Năm bẫy chung", [
            P("Một: IoU là giao chia hợp, gần một là khớp."), P("Hai: mAP là trung bình AP trên các lớp."),
            P("Ba: Fast R-CNN nhanh nhờ RoI pooling và đa nhiệm."), P("Bốn: Faster R-CNN dùng RPN."),
            P("Năm: anchor-free là CornerNet và FCOS."),
        ], table={"headers": ["Câu hỏi", "Đáp án"],
                  "rows": [["IoU?", "Giao / hợp, gần 1 là khớp"], ["mAP?", "Trung bình AP trên K lớp"], ["Fast R-CNN nhanh nhờ?", "RoI pooling + đa nhiệm"],
                           ["Faster R-CNN thay selective search bằng?", "RPN"], ["Anchor-free?", "CornerNet, FCOS"]]}),
        S("Tổng kết", "Sang chương 12", [
            P("Chương cuối, chương mười hai, mổ xẻ khâu phân loại có trong mọi bộ phát hiện: từ khoảng cách tối thiểu, Bayes, đến perceptron và mạng nơ-ron.",
              "Chương 12: phân loại mẫu"),
        ]),
    ]),
]

MAP = [
    ["Mở đầu", "1–3", "Xe tự lái: cái gì, ở đâu", "—", "Phát hiện = phân loại + định vị", "→ IoU & mAP"],
    ["IoU & mAP", "4–11", "Chấm khung lệch một chút", "Độ chính xác phân loại: không chấm vị trí", "Giao/hợp; AP từ đường cong P–R; bộ dữ liệu chuẩn", "Khung từ đâu ra → cửa sổ trượt"],
    ["Cửa sổ trượt", "12–13", "Vật ở bất kỳ đâu, cỡ bất kỳ", "Phân loại cả ảnh", "Trượt cửa sổ: vị trí → đặc trưng → phân loại", "Hàng chục nghìn cửa sổ → R-CNN"],
    ["Họ R-CNN", "14–19", "Bớt ứng viên, học đặc trưng", "Thử mù quáng, đặc trưng tay", "Anchor; R-CNN → Fast (RoI pooling) → Faster (RPN)", "2 giai đoạn chậm → YOLO/SSD"],
    ["YOLO & SSD", "20–23", "30 khung/giây", "Đề xuất rồi mới xét", "Một lượt; SSD đa tỉ lệ", "Anchor chọn tay → anchor-free"],
    ["Anchor-free", "24–29", "Khuôn sai thì kém", "3 vấn đề của anchor", "Góc (CornerNet), điểm (FCOS)", "CNN cục bộ → Transformer"],
    ["Transformer", "30–33", "Hiểu cả khung cảnh", "Cửa sổ tích chập độc lập", "DETR: attention, object queries", "→ Chương 12"],
    ["Tổng kết", "—", "—", "—", "Bốn nhóm, bẫy chung", "→ Chương 12"],
]
write(11, "Phát hiện đối tượng", EX, stories, MAP)
