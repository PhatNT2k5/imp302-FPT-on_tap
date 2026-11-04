export const lessonMedia = {
  "1": [
    {
      "kind": "image",
      "anchor": "Histogram ảnh",
      "title": "Ảnh và histogram",
      "caption": "Trục ngang là mức xám, trục dọc là số pixel. Histogram đếm độ sáng, không lưu vị trí pixel.",
      "src": "media/c01-slide-04.webp",
      "alt": "Ảnh và histogram — slide chương 1, trang PDF 4",
      "source": "references/01-1.-Basic-Gray-Level-Image-Processing.pdf#page=4",
      "page": 4,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "Ngưỡng hóa ảnh",
      "title": "Đổi ngưỡng, đổi vùng giữ lại",
      "caption": "Quan sát các ảnh nhị phân: thay T sẽ thay đổi phần vật thể được giữ lại.",
      "src": "media/c01-slide-20.webp",
      "alt": "Đổi ngưỡng, đổi vùng giữ lại — slide chương 1, trang PDF 20",
      "source": "references/01-1.-Basic-Gray-Level-Image-Processing.pdf#page=20",
      "page": 20,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "Ngưỡng hóa ảnh",
      "title": "Đổi ngưỡng T: pixel nào thành trắng?",
      "caption": "Ngưỡng tăng làm vùng trắng thu hẹp. Quy ước trong clip: trắng khi f(x,y) > T.",
      "src": "media/c01-threshold.mp4",
      "poster": "media/c01-threshold.webp",
      "track": "media/c01-threshold.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Histogram ảnh",
      "id": "c01-histogram",
      "title": "Histogram và kéo giãn tương phản",
      "goal": "Hiểu histogram thay đổi thế nào khi mở rộng dải mức xám.",
      "caption": "Histogram mô tả phân bố độ sáng; kéo giãn mở rộng dải giá trị đang có.",
      "src": "media/detailed/c01-histogram.mp4",
      "poster": "media/detailed/c01-histogram.webp",
      "track": "media/detailed/c01-histogram.vtt",
      "duration": 40,
      "source": "references/01-1.-Basic-Gray-Level-Image-Processing.pdf#page=9",
      "steps": [
        {
          "start": 0,
          "title": "Ảnh tương phản thấp",
          "text": "Ảnh thử chỉ dùng mức xám 80–160 nên các vùng sáng tối khó phân biệt.",
          "formula": "Đầu vào: f ∈ [80,160]"
        },
        {
          "start": 8,
          "title": "Đếm số pixel",
          "text": "Gom các pixel có cùng độ sáng vào từng cột. Histogram không lưu vị trí của pixel.",
          "formula": "H(k) = số pixel có mức xám k"
        },
        {
          "start": 16,
          "title": "Tính ánh xạ tuyến tính",
          "text": "Đưa 80 về 0 và 160 về 255. Mức xám ở giữa được ánh xạ theo cùng một đường thẳng.",
          "formula": "g = (f − 80) × 255 / 80"
        },
        {
          "start": 24,
          "title": "Áp dụng lên toàn ảnh",
          "text": "Pixel 120 trở thành khoảng 128. Dải sáng rộng hơn giúp nhìn cấu trúc rõ hơn.",
          "formula": "80 → 0; 120 → 128; 160 → 255"
        },
        {
          "start": 32,
          "title": "So sánh trước và sau",
          "text": "Kéo giãn làm tăng tương phản nhưng không tạo chi tiết mới hay sửa được mọi loại nhiễu.",
          "formula": "Tăng tương phản ≠ phục hồi thông tin"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Ngưỡng hóa ảnh",
      "id": "c01-otsu",
      "title": "Otsu: từ histogram đến ngưỡng tự động",
      "goal": "Theo dõi cách thử nhiều ngưỡng để tách nền và vật thể.",
      "caption": "Otsu tối đa hóa phương sai giữa hai lớp; hiệu quả phụ thuộc phân bố cường độ.",
      "src": "media/detailed/c01-otsu.mp4",
      "poster": "media/detailed/c01-otsu.webp",
      "track": "media/detailed/c01-otsu.vtt",
      "duration": 40,
      "source": "references/01-1.-Basic-Gray-Level-Image-Processing.pdf#page=21",
      "steps": [
        {
          "start": 0,
          "title": "Hai nhóm độ sáng",
          "text": "Ảnh thử gồm nền tối và vật thể sáng. Histogram xuất hiện hai nhóm chính.",
          "formula": "Mục tiêu: chia pixel thành 2 lớp"
        },
        {
          "start": 8,
          "title": "Thử một ngưỡng thấp",
          "text": "Với T thấp, nhiều pixel nền vẫn bị gán thành vật thể. Chia lớp chưa tốt.",
          "formula": "Trắng nếu f > T; đen nếu f ≤ T"
        },
        {
          "start": 16,
          "title": "Tính độ tách lớp",
          "text": "Với mỗi T, tính trọng số và trung bình hai lớp, rồi đo khoảng cách giữa chúng.",
          "formula": "σ²B = w0 × w1 × (μ0 − μ1)²"
        },
        {
          "start": 24,
          "title": "Chọn ngưỡng tối ưu",
          "text": "Quét T từ 0 đến 255, chọn T làm phương sai giữa hai lớp lớn nhất.",
          "formula": "T* = arg max σ²B(T)"
        },
        {
          "start": 32,
          "title": "Đọc kết quả đúng cách",
          "text": "Otsu tách theo cường độ, không hiểu vật thể. Ánh sáng không đều có thể làm kết quả kém.",
          "formula": "Tự động chọn T ≠ luôn đúng ngữ nghĩa"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Hình thái học ảnh nhị phân",
      "id": "c01-morphology",
      "title": "Erosion, dilation, opening và closing",
      "goal": "Phân biệt thứ tự hai phép toán hình thái học trên ảnh nhị phân.",
      "caption": "Opening thường loại vật thể nhỏ; closing thường lấp lỗ nhỏ. Kết quả phụ thuộc phần tử cấu trúc.",
      "src": "media/detailed/c01-morphology.mp4",
      "poster": "media/detailed/c01-morphology.webp",
      "track": "media/detailed/c01-morphology.vtt",
      "duration": 40,
      "source": "references/01-1.-Basic-Gray-Level-Image-Processing.pdf#page=28",
      "steps": [
        {
          "start": 0,
          "title": "Ảnh và phần tử cấu trúc",
          "text": "Ảnh nhị phân có khối chính, chấm nhiễu và lỗ nhỏ. Dùng cửa sổ vuông 3×3.",
          "formula": "Vật thể = 1; nền = 0"
        },
        {
          "start": 8,
          "title": "Erosion: co vật thể",
          "text": "Pixel chỉ còn trắng khi toàn bộ cửa sổ thuộc vật thể. Biên lùi vào, chấm nhỏ biến mất.",
          "formula": "Erosion với phần tử 3×3"
        },
        {
          "start": 16,
          "title": "Dilation: giãn vật thể",
          "text": "Pixel thành trắng nếu cửa sổ chạm vật thể. Biên mở rộng; lỗ nhỏ có thể bị lấp.",
          "formula": "Dilation với phần tử 3×3"
        },
        {
          "start": 24,
          "title": "Opening: co rồi giãn",
          "text": "Co trước loại chấm nhỏ; giãn sau phục hồi phần lớn kích thước khối còn lại.",
          "formula": "Opening = erosion → dilation"
        },
        {
          "start": 32,
          "title": "Closing: giãn rồi co",
          "text": "Giãn trước nối khe hoặc lấp lỗ nhỏ; co sau thu biên về gần ban đầu.",
          "formula": "Closing = dilation → erosion"
        }
      ]
    }
  ],
  "2": [
    {
      "kind": "image",
      "anchor": "2.1",
      "title": "Bộ lọc Gaussian",
      "caption": "So sánh f(m,n) và g(m,n): lọc thông thấp làm mượt ảnh, đồng thời có thể làm mờ chi tiết.",
      "src": "media/c02-slide-09.webp",
      "alt": "Bộ lọc Gaussian — slide chương 2, trang PDF 9",
      "source": "references/02-2.-Image-and-Video-Processing.pdf#page=9",
      "page": 9,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "2.4",
      "title": "Unsharp masking: làm nét từ ảnh mờ",
      "caption": "Lấy ảnh gốc trừ ảnh làm mờ để tạo mặt nạ chi tiết, rồi cộng mặt nạ vào ảnh gốc.",
      "src": "media/c02-slide-37.webp",
      "alt": "Unsharp masking: làm nét từ ảnh mờ — slide chương 2, trang PDF 37",
      "source": "references/02-2.-Image-and-Video-Processing.pdf#page=37",
      "page": 37,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "2.1",
      "title": "Gaussian: mượt hơn, mất bớt chi tiết",
      "caption": "So sánh ảnh gốc bên trái với ảnh lọc bên phải; Gaussian làm mượt, không tự phục hồi chi tiết đã mất.",
      "src": "media/c02-gaussian.mp4",
      "poster": "media/c02-gaussian.webp",
      "track": "media/c02-gaussian.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "2.4",
      "id": "c02-convolution",
      "title": "Cửa sổ lọc trượt: nhân rồi cộng",
      "goal": "Tính một pixel đầu ra của lọc trung bình 3×3.",
      "caption": "Lọc tuyến tính lấy tổng có trọng số. Convolution tổng quát cần lật kernel trước khi trượt.",
      "src": "media/detailed/c02-convolution.mp4",
      "poster": "media/detailed/c02-convolution.webp",
      "track": "media/detailed/c02-convolution.vtt",
      "duration": 40,
      "source": "references/02-2.-Image-and-Video-Processing.pdf#page=28",
      "steps": [
        {
          "start": 0,
          "title": "Chọn vùng lân cận",
          "text": "Cửa sổ 3×3 lấy chín giá trị quanh pixel đang xét. Đây là xử lý theo lân cận.",
          "formula": "Một pixel đầu ra ← một cửa sổ"
        },
        {
          "start": 8,
          "title": "Đặt kernel",
          "text": "Bộ lọc trung bình dùng chín hệ số bằng 1/9. Tổng hệ số bằng 1 nên giữ vùng sáng đều.",
          "formula": "Kernel 3×3: mỗi phần tử = 1/9"
        },
        {
          "start": 16,
          "title": "Nhân từng cặp",
          "text": "Nhân mỗi giá trị pixel với hệ số tương ứng trong kernel.",
          "formula": "Tích tại ô i: pixel_i / 9"
        },
        {
          "start": 24,
          "title": "Cộng các tích",
          "text": "Tổng chín tích là giá trị mới tại tâm. Trong ví dụ, tổng cửa sổ là 450.",
          "formula": "g = 450 / 9 = 50"
        },
        {
          "start": 32,
          "title": "Trượt và lặp",
          "text": "Lặp cho các vị trí còn lại. Với kernel đối xứng này, correlation và convolution trùng nhau.",
          "formula": "Ảnh mượt hơn, cạnh có thể mờ"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "2.2",
      "id": "c02-median-detail",
      "title": "Median: vì sao chống nhiễu muối tiêu?",
      "goal": "So sánh trung bình và trung vị trên cùng một cửa sổ có ngoại lai.",
      "caption": "Trung vị là giá trị ở giữa sau sắp xếp, không phải trung bình cộng.",
      "src": "media/detailed/c02-median-detail.mp4",
      "poster": "media/detailed/c02-median-detail.webp",
      "track": "media/detailed/c02-median-detail.vtt",
      "duration": 40,
      "source": "references/02-2.-Image-and-Video-Processing.pdf#page=11",
      "steps": [
        {
          "start": 0,
          "title": "Một điểm nhiễu cực sáng",
          "text": "Tám giá trị quanh 40–60, nhưng một pixel bị đẩy lên 255.",
          "formula": "Cửa sổ: 40,45,45,50,50,50,55,60,255"
        },
        {
          "start": 8,
          "title": "Lọc trung bình",
          "text": "Tổng chín số chia 9 bị giá trị 255 kéo lên. Điểm đầu ra sáng hơn vùng lân cận.",
          "formula": "Mean = 650 / 9 ≈ 72,2"
        },
        {
          "start": 16,
          "title": "Sắp xếp cửa sổ",
          "text": "Median xét thứ tự giá trị thay vì khoảng cách tới trung bình.",
          "formula": "40 ≤ 45 ≤ 45 ≤ 50 ≤ 50 ≤ 50 ≤ 55 ≤ 60 ≤ 255"
        },
        {
          "start": 24,
          "title": "Lấy phần tử giữa",
          "text": "Cửa sổ có 9 giá trị nên chọn phần tử thứ 5. Giá trị ngoại lai không kéo lệch trung vị.",
          "formula": "Median = 50"
        },
        {
          "start": 32,
          "title": "Quan sát trên ảnh",
          "text": "Trung vị loại nhiều chấm nhiễu xung. Cửa sổ quá lớn vẫn có thể xóa chi tiết nhỏ.",
          "formula": "Median phù hợp với nhiễu xung"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "2.5",
      "id": "c02-fourier-filter",
      "title": "Lọc thông thấp trong miền Fourier",
      "goal": "Theo chuỗi ảnh → phổ → mặt nạ → biến đổi ngược.",
      "caption": "Tích chập không gian tương ứng với phép nhân phổ. Clip dùng mô hình tuần hoàn, chưa xử lý biên bằng padding.",
      "src": "media/detailed/c02-fourier-filter.mp4",
      "poster": "media/detailed/c02-fourier-filter.webp",
      "track": "media/detailed/c02-fourier-filter.vtt",
      "duration": 40,
      "source": "references/02-2.-Image-and-Video-Processing.pdf#page=42",
      "steps": [
        {
          "start": 0,
          "title": "Ảnh có chi tiết nhanh",
          "text": "Vạch mảnh và biên sắc tương ứng với biến thiên cường độ nhanh trong không gian.",
          "formula": "Chi tiết nhỏ thường cần tần số cao"
        },
        {
          "start": 8,
          "title": "Biến đổi Fourier",
          "text": "FFT chuyển ảnh sang hệ số tần số. Phổ được dịch tâm để dễ nhìn vùng tần số thấp.",
          "formula": "F = FFT2(f); hình phổ dùng log(1+"
        },
        {
          "start": 16,
          "title": "Tạo mặt nạ thông thấp",
          "text": "Mặt nạ Gaussian giữ gần tâm mạnh hơn, giảm dần các tần số xa tâm.",
          "formula": "H(u,v) = exp(−D² / (2D0²))"
        },
        {
          "start": 24,
          "title": "Nhân rồi biến đổi ngược",
          "text": "Nhân từng hệ số với H và dùng IFFT để trở về miền ảnh.",
          "formula": "g = IFFT2(H × F)"
        },
        {
          "start": 32,
          "title": "Thay đổi tần số cắt",
          "text": "D0 nhỏ làm ảnh mượt mạnh hơn nhưng mất nhiều chi tiết hơn. Không phải mọi thông thấp đều khử mọi nhiễu.",
          "formula": "D0 giảm → lọc mạnh hơn"
        }
      ]
    }
  ],
  "3": [
    {
      "kind": "image",
      "anchor": "3.1",
      "title": "Mô hình suy giảm và phục hồi",
      "caption": "Theo các mũi tên: ảnh gốc đi qua hàm suy giảm và nhiễu; bước phục hồi ước lượng lại ảnh gốc.",
      "src": "media/c03-slide-05.webp",
      "alt": "Mô hình suy giảm và phục hồi — slide chương 3, trang PDF 5",
      "source": "references/03-3.-Image-Degradation-Restoration-and-Resconstruction.pdf#page=5",
      "page": 5,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "3.3",
      "title": "Nhiễu tuần hoàn và lọc notch",
      "caption": "Tìm các đỉnh nhiễu trong phổ; chặn chúng bằng notch rồi biến đổi ngược về ảnh.",
      "src": "media/c03-slide-22.webp",
      "alt": "Nhiễu tuần hoàn và lọc notch — slide chương 3, trang PDF 22",
      "source": "references/03-3.-Image-Degradation-Restoration-and-Resconstruction.pdf#page=22",
      "page": 22,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "3.3",
      "title": "Median và nhiễu muối tiêu",
      "caption": "Bộ lọc trung vị loại nhiều điểm nhiễu xung, nhưng cửa sổ quá lớn cũng làm mất chi tiết.",
      "src": "media/c03-median.mp4",
      "poster": "media/c03-median.webp",
      "track": "media/c03-median.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "3.2",
      "id": "c03-noise-models",
      "title": "Nhiễu Gaussian và nhiễu muối tiêu",
      "goal": "Nhận ra hai kiểu nhiễu và cách chọn bộ lọc phù hợp.",
      "caption": "Nhiễu Gaussian là nhiễu cộng trong ví dụ; muối tiêu thay một số pixel bằng giá trị cực trị.",
      "src": "media/detailed/c03-noise-models.mp4",
      "poster": "media/detailed/c03-noise-models.webp",
      "track": "media/detailed/c03-noise-models.vtt",
      "duration": 40,
      "source": "references/03-3.-Image-Degradation-Restoration-and-Resconstruction.pdf#page=12",
      "steps": [
        {
          "start": 0,
          "title": "Ảnh sạch làm tham chiếu",
          "text": "Dùng một ảnh thử có vùng phẳng, cạnh và vạch mảnh để quan sát nhiễu.",
          "formula": "Ảnh tham chiếu f"
        },
        {
          "start": 8,
          "title": "Thêm nhiễu Gaussian",
          "text": "Nhiễu cộng tạo dao động nhỏ trên nhiều pixel. Clip dùng trung bình 0, độ lệch chuẩn 20.",
          "formula": "g = clip(f + N(0,20²))"
        },
        {
          "start": 16,
          "title": "Thêm nhiễu xung",
          "text": "Một số pixel bị thay bằng 0 hoặc 255, tạo chấm đen trắng rõ rệt.",
          "formula": "Muối tiêu: thay giá trị tại một số vị trí"
        },
        {
          "start": 24,
          "title": "Lọc theo loại nhiễu",
          "text": "Làm mượt có thể giảm dao động Gaussian; median thường xử lý tốt chấm nhiễu xung.",
          "formula": "Chọn bộ lọc theo mô hình nhiễu"
        },
        {
          "start": 32,
          "title": "Kiểm tra phần đánh đổi",
          "text": "Khử nhiễu và giữ cạnh thường đánh đổi với nhau. So sánh cả vùng phẳng lẫn chi tiết.",
          "formula": "Ảnh ít nhiễu chưa chắc giữ đủ chi tiết"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "3.6",
      "id": "c03-wiener",
      "title": "Wiener: phục hồi mờ có xét nhiễu",
      "goal": "Hiểu vì sao chia ngược trực tiếp dễ khuếch đại nhiễu.",
      "caption": "Wiener cân bằng khôi phục tín hiệu và hạn chế khuếch đại nhiễu; ví dụ dùng K hằng xấp xỉ.",
      "src": "media/detailed/c03-wiener.mp4",
      "poster": "media/detailed/c03-wiener.webp",
      "track": "media/detailed/c03-wiener.vtt",
      "duration": 40,
      "source": "references/03-3.-Image-Degradation-Restoration-and-Resconstruction.pdf#page=33",
      "steps": [
        {
          "start": 0,
          "title": "Tạo ảnh bị suy giảm",
          "text": "Làm mờ ảnh bằng hàm H rồi cộng nhiễu nhỏ. Trong clip, H được biết trước.",
          "formula": "G = H × F + N"
        },
        {
          "start": 8,
          "title": "Nguy cơ của lọc ngược",
          "text": "Chia cho H rất nhỏ có thể phóng đại thành phần nhiễu và gây kết quả dao động mạnh.",
          "formula": "F̂ = G / H nhạy khi "
        },
        {
          "start": 16,
          "title": "Thêm điều chuẩn",
          "text": "Wiener dùng hệ số giảm khuếch đại nơi tín hiệu kém tin cậy. Clip dùng K hằng để minh họa.",
          "formula": "F̂ = H*G / ("
        },
        {
          "start": 24,
          "title": "Thử nhiều giá trị K",
          "text": "K nhỏ dễ còn nhiễu; K lớn làm mượt mạnh hơn. Quan sát độ rõ và độ hạt cùng lúc.",
          "formula": "K mô phỏng tỉ lệ công suất nhiễu/tín hiệu"
        },
        {
          "start": 32,
          "title": "Đọc giới hạn ví dụ",
          "text": "Ảnh gốc chỉ dùng để so sánh. Thực tế phải ước lượng H và phổ nhiễu, không luôn biết sẵn.",
          "formula": "Không bảo đảm lấy lại mọi chi tiết"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "3.3",
      "id": "c03-notch",
      "title": "Notch: bỏ sọc nhiễu bằng cách chặn đỉnh phổ",
      "goal": "Theo dõi cặp đỉnh gây nhiễu tuần hoàn trong Fourier.",
      "caption": "Với ảnh thực, cần xử lý cặp đỉnh đối xứng để duy trì tính đối xứng liên hợp của phổ.",
      "src": "media/detailed/c03-notch.mp4",
      "poster": "media/detailed/c03-notch.webp",
      "track": "media/detailed/c03-notch.vtt",
      "duration": 40,
      "source": "references/03-3.-Image-Degradation-Restoration-and-Resconstruction.pdf#page=22",
      "steps": [
        {
          "start": 0,
          "title": "Thêm một sóng gây sọc",
          "text": "Cộng sóng sin có chu kỳ xác định vào ảnh. Sọc lặp đều là dấu hiệu nhiễu tuần hoàn.",
          "formula": "n(x,y) = A sin(2πkx/N)"
        },
        {
          "start": 8,
          "title": "Nhìn vào phổ Fourier",
          "text": "Sóng sin tạo một cặp đỉnh đối xứng quanh tâm phổ của ảnh thực.",
          "formula": "Đỉnh tại +k và −k"
        },
        {
          "start": 16,
          "title": "Chặn đúng cặp đỉnh",
          "text": "Mặt nạ notch đặt gần 0 quanh hai vị trí nhiễu, giữ phần lớn hệ số khác.",
          "formula": "Không cần xóa toàn bộ tần số cao"
        },
        {
          "start": 24,
          "title": "Biến đổi ngược",
          "text": "Áp dụng mặt nạ vào phổ rồi dùng IFFT. Các sọc giảm rõ trong ảnh tái tạo.",
          "formula": "g_lọc = IFFT2(H_notch × G)"
        },
        {
          "start": 32,
          "title": "Kiểm tra chi tiết bị mất",
          "text": "Nếu tín hiệu thật trùng tần số bị chặn, nó cũng bị ảnh hưởng. Notch rộng quá gây mất chi tiết.",
          "formula": "Chặn có chọn lọc, không phải xóa tùy ý"
        }
      ]
    }
  ],
  "4": [
    {
      "kind": "image",
      "anchor": "4.3",
      "title": "64 mẫu cơ sở của DCT 8 × 8",
      "caption": "Ô góc trên trái là thành phần DC. Đi sang phải tăng tần số theo x; đi xuống tăng tần số theo y. Đây là các mẫu cơ sở, không phải phổ DCT của một ảnh cụ thể.",
      "src": "media/c04-diagram.webp",
      "alt": "64 mẫu cơ sở của DCT 8 × 8 — sơ đồ minh họa theo kiến thức slide",
      "source": "references/04-4.-Image-and-Video-Analysis.pdf#page=7",
      "page": 9,
      "width": 1600,
      "height": 950,
      "derived": true
    },
    {
      "kind": "image",
      "anchor": "4.5",
      "title": "Phân rã ảnh bằng wavelet",
      "caption": "Quan sát ảnh xấp xỉ và các băng chi tiết: wavelet biểu diễn ảnh ở nhiều hướng và nhiều thang đo.",
      "src": "media/c04-slide-25.webp",
      "alt": "Phân rã ảnh bằng wavelet — slide chương 4, trang PDF 25",
      "source": "references/04-4.-Image-and-Video-Analysis.pdf#page=25",
      "page": 25,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "4.3",
      "id": "c04-dct",
      "title": "DCT: giữ ít hệ số thì ảnh thay đổi ra sao?",
      "goal": "Liên hệ 64 hệ số DCT với khả năng tái tạo khối ảnh 8×8.",
      "caption": "Biến đổi DCT tự nó không gây mất dữ liệu; bỏ hoặc lượng tử hóa hệ số mới tạo sai lệch.",
      "src": "media/detailed/c04-dct.mp4",
      "poster": "media/detailed/c04-dct.webp",
      "track": "media/detailed/c04-dct.vtt",
      "duration": 40,
      "source": "references/04-4.-Image-and-Video-Analysis.pdf#page=7",
      "steps": [
        {
          "start": 0,
          "title": "Chọn khối ảnh 8×8",
          "text": "Một khối có 64 pixel được biểu diễn bằng tổ hợp của 64 mẫu cosine cơ sở.",
          "formula": "64 pixel ↔ 64 hệ số DCT"
        },
        {
          "start": 8,
          "title": "Biến đổi sang hệ số",
          "text": "DCT trực chuẩn thay đổi cách biểu diễn, chưa tự làm mất thông tin.",
          "formula": "C = A × f × Aᵀ"
        },
        {
          "start": 16,
          "title": "Chỉ giữ DC",
          "text": "Giữ hệ số góc trên trái, đặt phần còn lại bằng 0. Khối tái tạo trở thành gần như một màu.",
          "formula": "DC biểu diễn độ sáng trung bình"
        },
        {
          "start": 24,
          "title": "Thêm tần số thấp",
          "text": "Giữ một miền nhỏ ở góc trên trái cho hình dạng thô; thêm hệ số giúp tái tạo chi tiết.",
          "formula": "Giữ 2×2 rồi 4×4 hệ số"
        },
        {
          "start": 32,
          "title": "Giữ đủ hệ số",
          "text": "Dùng đủ 8×8 hệ số khôi phục khối ban đầu, sai số chỉ do tính toán số học.",
          "formula": "f = Aᵀ × C × A"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "4.5",
      "id": "c04-haar",
      "title": "Wavelet Haar: tách xấp xỉ và chi tiết",
      "goal": "Xem cách lấy trung bình và sai khác theo hàng rồi theo cột.",
      "caption": "Haar là một ví dụ wavelet. Tên LH/HL có thể đổi theo quy ước; hãy xem hướng biến đổi hàng/cột.",
      "src": "media/detailed/c04-haar.mp4",
      "poster": "media/detailed/c04-haar.webp",
      "track": "media/detailed/c04-haar.vtt",
      "duration": 40,
      "source": "references/04-4.-Image-and-Video-Analysis.pdf#page=23",
      "steps": [
        {
          "start": 0,
          "title": "Ghép cặp hai mẫu",
          "text": "Với cặp (a,b), lấy tổng và hiệu có chuẩn hóa. Ví dụ (10,14) cho tổng lớn, hiệu nhỏ.",
          "formula": "L=(a+b)/√2; H=(a−b)/√2"
        },
        {
          "start": 8,
          "title": "Xử lý theo hàng",
          "text": "Mỗi hàng được tách thành thành phần mượt và thành phần thay đổi theo chiều ngang.",
          "formula": "Theo hàng: [L "
        },
        {
          "start": 16,
          "title": "Xử lý tiếp theo cột",
          "text": "Tách theo cột tạo bốn băng: xấp xỉ và ba nhóm chi tiết định hướng.",
          "formula": "LL, LH, HL, HH"
        },
        {
          "start": 24,
          "title": "Phân rã đa tỉ lệ",
          "text": "Tiếp tục phân rã riêng băng LL. Chi tiết thô và chi tiết nhỏ nằm ở các mức khác nhau.",
          "formula": "Level 2 = phân rã LL của level 1"
        },
        {
          "start": 32,
          "title": "Tái tạo bằng phép ngược",
          "text": "Nếu giữ tất cả hệ số, cộng/trừ ngược sẽ khôi phục ảnh ban đầu.",
          "formula": "a=(L+H)/√2; b=(L−H)/√2"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "4.4",
      "id": "c04-hadamard",
      "title": "Walsh–Hadamard: biến đổi bằng cộng và trừ",
      "goal": "Theo dõi phép biến đổi và phép ngược trên bốn mẫu.",
      "caption": "Clip dùng Hadamard thứ tự Sylvester, không sắp lại theo sequency; phép ngược cần hệ số chuẩn hóa.",
      "src": "media/detailed/c04-hadamard.mp4",
      "poster": "media/detailed/c04-hadamard.webp",
      "track": "media/detailed/c04-hadamard.vtt",
      "duration": 40,
      "source": "references/04-4.-Image-and-Video-Analysis.pdf#page=13",
      "steps": [
        {
          "start": 0,
          "title": "Bốn mẫu đầu vào",
          "text": "Dùng vector x = [4,2,0,2]. Ma trận Hadamard chỉ gồm +1 và −1.",
          "formula": "x = [4,2,0,2]ᵀ"
        },
        {
          "start": 8,
          "title": "Nhân với các mẫu dấu",
          "text": "Mỗi hàng của H cộng hoặc trừ các phần tử đầu vào theo một mẫu dấu.",
          "formula": "y = Hx"
        },
        {
          "start": 16,
          "title": "Thu các hệ số",
          "text": "Mẫu toàn dấu cộng lấy tổng 8. Các mẫu đổi dấu đo những kiểu biến thiên khác nhau.",
          "formula": "y = [8,0,4,4]ᵀ"
        },
        {
          "start": 24,
          "title": "Đổi ngược",
          "text": "Vì HᵀH = 4I, nhân lại Hᵀ rồi chia 4 sẽ lấy lại vector x.",
          "formula": "x = Hᵀy / 4"
        },
        {
          "start": 32,
          "title": "Phân biệt với DCT",
          "text": "Hadamard dùng mẫu vuông ±1; DCT dùng cosine. Cả hai đều có thể là biểu diễn khả nghịch.",
          "formula": "Không tự gây mất dữ liệu"
        }
      ]
    }
  ],
  "5": [
    {
      "kind": "image",
      "anchor": "5.4",
      "title": "Các bước tạo mã Huffman",
      "caption": "Theo dõi việc ghép các xác suất nhỏ nhất và gán bit: ký hiệu xuất hiện thường xuyên thường nhận từ mã ngắn hơn.",
      "src": "media/c05-slide-24.webp",
      "alt": "Cây mã Huffman — slide chương 5, trang PDF 24",
      "source": "references/05-5.-Image-compression.pdf#page=24",
      "page": 24,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "5.7",
      "title": "Quy trình mã hóa JPEG",
      "caption": "Theo dõi các khối biến đổi, lượng tử hóa và mã hóa. Lượng tử hóa là bước gây mất thông tin trong JPEG có mất dữ liệu.",
      "src": "media/c05-slide-40.webp",
      "alt": "Quy trình mã hóa JPEG — slide chương 5, trang PDF 40",
      "source": "references/05-5.-Image-compression.pdf#page=40",
      "page": 40,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "5.7",
      "title": "JPEG: chất lượng và dung lượng",
      "caption": "Quan sát số byte thực của từng ảnh JPEG và vùng biên. Đây là một ảnh ví dụ, không phải quan hệ dung lượng cố định cho mọi ảnh.",
      "src": "media/c05-jpeg.mp4",
      "poster": "media/c05-jpeg.webp",
      "track": "media/c05-jpeg.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "5.4",
      "id": "c05-huffman",
      "title": "Huffman: ghép xác suất để tạo mã ngắn",
      "goal": "Tính độ dài mã trung bình cho bốn ký hiệu.",
      "caption": "Đảo nhãn 0/1 hoặc xử lý hòa khác có thể cho bộ mã khác nhưng cùng độ dài trung bình tối ưu.",
      "src": "media/detailed/c05-huffman.mp4",
      "poster": "media/detailed/c05-huffman.webp",
      "track": "media/detailed/c05-huffman.vtt",
      "duration": 40,
      "source": "references/05-5.-Image-compression.pdf#page=24",
      "steps": [
        {
          "start": 0,
          "title": "Đọc xác suất ký hiệu",
          "text": "Nguồn có A:0,4; B:0,3; C:0,2; D:0,1. Mã cố định cho 4 ký hiệu cần 2 bit.",
          "formula": "Tổng xác suất = 1"
        },
        {
          "start": 8,
          "title": "Ghép hai xác suất nhỏ nhất",
          "text": "Ghép C và D thành một nút có trọng số 0,3. Lặp với các nút còn lại.",
          "formula": "0,1 + 0,2 = 0,3"
        },
        {
          "start": 16,
          "title": "Hoàn thành cây nhị phân",
          "text": "Ghép hai nút trọng số 0,3 thành 0,6; ghép tiếp với A có trọng số 0,4.",
          "formula": "0,3+0,3=0,6; 0,6+0,4=1"
        },
        {
          "start": 24,
          "title": "Gán bit trên nhánh",
          "text": "Một cách gán hợp lệ: A=0, B=10, C=110, D=111. Không mã nào là tiền tố của mã khác.",
          "formula": "Độ dài: 1, 2, 3, 3 bit"
        },
        {
          "start": 32,
          "title": "Tính độ dài trung bình",
          "text": "Ký hiệu hay gặp được mã ngắn hơn. Trung bình 1,9 bit/ký hiệu, chưa tính chi phí lưu bảng mã.",
          "formula": "0,4×1+0,3×2+0,2×3+0,1×3 = 1,9"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "5.6",
      "id": "c05-arithmetic",
      "title": "Arithmetic coding: thu hẹp khoảng cho chuỗi BAC",
      "goal": "Theo dõi ba lần cập nhật khoảng và chọn một số đại diện.",
      "caption": "Clip minh họa bằng số thực thập phân; triển khai thực tế cần biểu diễn hữu hạn và cơ chế chuẩn hóa.",
      "src": "media/detailed/c05-arithmetic.mp4",
      "poster": "media/detailed/c05-arithmetic.webp",
      "track": "media/detailed/c05-arithmetic.vtt",
      "duration": 40,
      "source": "references/05-5.-Image-compression.pdf#page=34",
      "steps": [
        {
          "start": 0,
          "title": "Chia khoảng ban đầu",
          "text": "A chiếm [0;0,5), B chiếm [0,5;0,8), C chiếm [0,8;1). Dùng cùng mô hình khi giải mã.",
          "formula": "P(A)=0,5; P(B)=0,3; P(C)=0,2"
        },
        {
          "start": 8,
          "title": "Đọc ký hiệu B",
          "text": "Chọn đoạn của B trong khoảng hiện tại [0;1). Khoảng mới là [0,5;0,8).",
          "formula": "low=0,5; high=0,8"
        },
        {
          "start": 16,
          "title": "Đọc tiếp A",
          "text": "Lấy nửa đầu của khoảng rộng 0,3. Khoảng BA là [0,5;0,65).",
          "formula": "high = 0,5 + 0,3×0,5 = 0,65"
        },
        {
          "start": 24,
          "title": "Đọc tiếp C",
          "text": "Lấy phần từ 0,8 đến 1 của khoảng BA. Thu được [0,62;0,65).",
          "formula": "low = 0,5 + 0,15×0,8 = 0,62"
        },
        {
          "start": 32,
          "title": "Chọn số đại diện",
          "text": "0,63 nằm trong khoảng cuối. Giải mã cần cùng xác suất và biết độ dài chuỗi hoặc ký hiệu kết thúc.",
          "formula": "0,62 ≤ 0,63 < 0,65"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "5.7",
      "id": "c05-jpeg-steps",
      "title": "JPEG: DCT → lượng tử → tái tạo",
      "goal": "Nhìn trực tiếp sai số xuất hiện tại bước lượng tử hóa khối 8×8.",
      "caption": "Ví dụ chỉ minh họa nhánh khối xám và lượng tử hóa; JPEG màu còn có đổi không gian màu và có thể giảm mẫu chroma.",
      "src": "media/detailed/c05-jpeg-steps.mp4",
      "poster": "media/detailed/c05-jpeg-steps.webp",
      "track": "media/detailed/c05-jpeg-steps.vtt",
      "duration": 40,
      "source": "references/05-5.-Image-compression.pdf#page=40",
      "steps": [
        {
          "start": 0,
          "title": "Chọn khối và dịch mức",
          "text": "Lấy khối ảnh xám 8×8, trừ 128 để đưa các giá trị quanh 0.",
          "formula": "f_dịch = f − 128"
        },
        {
          "start": 8,
          "title": "Tính DCT",
          "text": "Biểu diễn khối bằng các hệ số tần số. Chưa bỏ hệ số ở bước này.",
          "formula": "C = DCT2(f_dịch)"
        },
        {
          "start": 16,
          "title": "Lượng tử hóa",
          "text": "Chia hệ số cho bảng lượng tử và làm tròn. Nhiều hệ số nhỏ trở thành 0.",
          "formula": "Cq = round(C / Q)"
        },
        {
          "start": 24,
          "title": "Mã hóa chuỗi hệ số",
          "text": "Zigzag và mã entropy khai thác các số 0. Mã entropy không tạo thêm sai số lượng tử.",
          "formula": "DCT → lượng tử → zigzag → mã entropy"
        },
        {
          "start": 32,
          "title": "Giải lượng tử và IDCT",
          "text": "Nhân lại Q rồi IDCT, cộng 128. Sai lệch so với ảnh gốc vẫn còn vì đã làm tròn.",
          "formula": "f̂ = IDCT2(Cq × Q) + 128"
        }
      ]
    }
  ],
  "6": [
    {
      "kind": "image",
      "anchor": "6.1",
      "title": "Bộ nhớ khung và dự đoán chuyển động",
      "caption": "Khung tham chiếu được giữ lại để ước lượng và bù chuyển động, giúp giảm thông tin phải mã hóa.",
      "src": "media/c06-slide-09.webp",
      "alt": "Bộ nhớ khung và dự đoán chuyển động — slide chương 6, trang PDF 9",
      "source": "references/06-6.-Video-compression.pdf#page=9",
      "page": 9,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "6.4",
      "title": "Dự đoán hai chiều trong MPEG",
      "caption": "Quan sát hướng tham chiếu giữa các khung; khung B có thể dự đoán từ cả khung trước và khung sau.",
      "src": "media/c06-slide-24.webp",
      "alt": "Dự đoán hai chiều trong MPEG — slide chương 6, trang PDF 24",
      "source": "references/06-6.-Video-compression.pdf#page=24",
      "page": 24,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "6.1",
      "title": "Dự đoán chuyển động và phần dư",
      "caption": "Ví dụ tổng hợp: một vật thể chỉ tịnh tiến. Phần dư bằng trị tuyệt đối của khung hiện tại trừ khung dự đoán.",
      "src": "media/c06-motion.mp4",
      "poster": "media/c06-motion.webp",
      "track": "media/c06-motion.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "6.1",
      "id": "c06-block-match",
      "title": "Block matching: tìm vector chuyển động",
      "goal": "So sánh các vị trí dự đoán bằng tổng sai khác tuyệt đối.",
      "caption": "Chuyển động phức tạp không luôn được mô tả đủ bằng một vector tịnh tiến cho mỗi khối.",
      "src": "media/detailed/c06-block-match.mp4",
      "poster": "media/detailed/c06-block-match.webp",
      "track": "media/detailed/c06-block-match.vtt",
      "duration": 40,
      "source": "references/06-6.-Video-compression.pdf#page=9",
      "steps": [
        {
          "start": 0,
          "title": "Hai khung liên tiếp",
          "text": "Một khối sáng dịch ngang trên nền tối. Chọn khung trước làm tham chiếu.",
          "formula": "Vector thật trong ví dụ: (+24,0) px"
        },
        {
          "start": 8,
          "title": "Thử một vị trí",
          "text": "Dịch khối tham chiếu theo một vector ứng viên rồi so với khối hiện tại.",
          "formula": "SAD = Σ "
        },
        {
          "start": 16,
          "title": "Tìm ứng viên tốt nhất",
          "text": "Quét các độ dịch trong vùng tìm kiếm; giữ vector làm SAD nhỏ nhất.",
          "formula": "v* = arg min SAD(v)"
        },
        {
          "start": 24,
          "title": "Bù chuyển động",
          "text": "Dùng vector tìm được tạo khung dự đoán. Ví dụ chỉ có tịnh tiến nên có thể khớp hoàn toàn.",
          "formula": "Khung dự đoán từ khung tham chiếu"
        },
        {
          "start": 32,
          "title": "Mã hóa phần dư",
          "text": "Encoder còn cần gửi vector và phần dư. Che khuất hoặc đổi sáng thường làm phần dư khác 0.",
          "formula": "Hiện tại = dự đoán + phần dư"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "6.4",
      "id": "c06-ipb",
      "title": "Khung I, P, B và thứ tự giải mã",
      "goal": "Phân biệt thứ tự hiển thị với thứ tự cần có khung tham chiếu.",
      "caption": "I/P/B mô tả kiểu dự đoán, không phải ba mức chất lượng cố định. Clip là GOP minh họa đơn giản.",
      "src": "media/detailed/c06-ipb.mp4",
      "poster": "media/detailed/c06-ipb.webp",
      "track": "media/detailed/c06-ipb.vtt",
      "duration": 40,
      "source": "references/06-6.-Video-compression.pdf#page=27",
      "steps": [
        {
          "start": 0,
          "title": "Thứ tự cần hiển thị",
          "text": "Ví dụ đơn giản gồm I0, B1, B2, P3. Đây là vị trí các khung khi xem video.",
          "formula": "Thứ tự hiển thị: I0 → B1 → B2 → P3"
        },
        {
          "start": 8,
          "title": "Khung I độc lập",
          "text": "I0 dùng dự đoán trong khung, không cần khung trước hoặc sau để tái tạo trong ví dụ.",
          "formula": "I: điểm bắt đầu tham chiếu"
        },
        {
          "start": 16,
          "title": "Khung P tham chiếu quá khứ",
          "text": "P3 dùng I0 làm tham chiếu trong sơ đồ đơn giản. Giải mã P3 trước khi dựng các B giữa chúng.",
          "formula": "P3 cần I0"
        },
        {
          "start": 24,
          "title": "Khung B dùng hai phía",
          "text": "B1 và B2 có thể dự đoán từ I0 và P3. Vì thế P3 cần sẵn dù được hiển thị sau.",
          "formula": "B1,B2 dùng I0 và P3"
        },
        {
          "start": 32,
          "title": "Thứ tự giải mã có thể khác",
          "text": "Một thứ tự hợp lệ cho ví dụ là I0, P3, B1, B2. Cấu trúc codec thực có thể phức tạp hơn.",
          "formula": "Giải mã: I0 → P3 → B1 → B2"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "6.3",
      "id": "c06-transcoding",
      "title": "Chuyển mã: giảm bitrate và sai số tích lũy",
      "goal": "Hiểu chuỗi giải mã rồi mã hóa lại khi thay mức lượng tử.",
      "caption": "Giảm độ phân giải, giảm frame rate và tăng lượng tử là các cách khác nhau; không thể suy bitrate chỉ từ kích thước pixel.",
      "src": "media/detailed/c06-transcoding.mp4",
      "poster": "media/detailed/c06-transcoding.webp",
      "track": "media/detailed/c06-transcoding.vtt",
      "duration": 40,
      "source": "references/06-6.-Video-compression.pdf#page=18",
      "steps": [
        {
          "start": 0,
          "title": "Bitstream đầu vào",
          "text": "Ảnh trong video đã qua lượng tử hóa. Giải mã không tự lấy lại phần chi tiết đã mất.",
          "formula": "Mã hóa lần 1 → dữ liệu nén"
        },
        {
          "start": 8,
          "title": "Giải mã để xử lý",
          "text": "Bộ chuyển mã miền pixel dựng lại khung trước khi đổi độ phân giải hoặc tham số mã hóa.",
          "formula": "Giải mã → khung tái tạo"
        },
        {
          "start": 16,
          "title": "Mã hóa lại với lượng tử mạnh",
          "text": "Bước lượng tử lớn hơn thường làm hệ số dễ mã hóa hơn nhưng tạo thêm sai số.",
          "formula": "q tăng → nhiều hệ số bị làm tròn"
        },
        {
          "start": 24,
          "title": "So với mã hóa trực tiếp",
          "text": "So sánh tái lượng tử hóa hai lần với lượng tử hóa trực tiếp từ ảnh gốc. Hai đường có thể khác.",
          "formula": "Q2(Q1(f)) không luôn bằng Q2(f)"
        },
        {
          "start": 32,
          "title": "Rút ra lựa chọn",
          "text": "Giảm bitrate cần đánh đổi chất lượng. Clip minh họa lượng tử vô hướng, không đo bitrate codec hoàn chỉnh.",
          "formula": "Tránh mã hóa có mất dữ liệu nhiều lần"
        }
      ]
    }
  ],
  "7": [
    {
      "kind": "image",
      "anchor": "Chuyển đổi tốc độ lấy mẫu",
      "title": "Giảm mẫu và phổ tần số",
      "caption": "Quan sát phổ trước và sau khi giảm mẫu. Lọc thông thấp trước khi lấy thưa mẫu giúp hạn chế chồng lấn phổ (aliasing).",
      "src": "media/c07-slide-11.webp",
      "alt": "Downsampling và aliasing — slide chương 7, trang PDF 11",
      "source": "references/07-7.-Image-and-Video-Acquisition.pdf#page=11",
      "page": 11,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "Các phương pháp nội suy",
      "title": "Phóng to ảnh bằng nội suy",
      "caption": "Nearest neighbor giữ dạng khối; nội suy tuyến tính dùng các mẫu lân cận để tạo chuyển tiếp mượt hơn.",
      "src": "media/c07-slide-18.webp",
      "alt": "Phóng to ảnh bằng nội suy — slide chương 7, trang PDF 18",
      "source": "references/07-7.-Image-and-Video-Acquisition.pdf#page=18",
      "page": 18,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "Các phương pháp nội suy",
      "title": "Cùng ảnh nhỏ, hai cách phóng to",
      "caption": "So sánh nearest neighbor với bilinear trên cùng ảnh đã giảm mẫu. Hai ảnh được hiển thị cùng kích thước để thấy khác biệt.",
      "src": "media/c07-sampling.mp4",
      "poster": "media/c07-sampling.webp",
      "track": "media/c07-sampling.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Chuyển đổi tốc độ lấy mẫu",
      "id": "c07-aliasing",
      "title": "Aliasing: vì sao phải lọc trước khi giảm mẫu?",
      "goal": "So sánh lấy thưa mẫu trực tiếp với lọc thông thấp rồi lấy mẫu.",
      "caption": "Lọc trước giảm chồng lấn phổ; lọc sau không thể bảo đảm đảo ngược aliasing đã xảy ra.",
      "src": "media/detailed/c07-aliasing.mp4",
      "poster": "media/detailed/c07-aliasing.webp",
      "track": "media/detailed/c07-aliasing.vtt",
      "duration": 40,
      "source": "references/07-7.-Image-and-Video-Acquisition.pdf#page=9",
      "steps": [
        {
          "start": 0,
          "title": "Ảnh có vạch rất mảnh",
          "text": "Nhiều vạch sáng tối lặp nhanh tạo năng lượng tần số cao. Lưới mẫu thưa có thể không đủ để ghi nhận.",
          "formula": "Tín hiệu cần thỏa Nyquist của lưới mới"
        },
        {
          "start": 8,
          "title": "Lấy thưa trực tiếp",
          "text": "Chỉ giữ một pixel mỗi bốn pixel theo từng chiều. Vạch có thể biến thành họa tiết sai.",
          "formula": "Downsample ×4: giữ mỗi mẫu thứ 4"
        },
        {
          "start": 16,
          "title": "Lọc thông thấp trước",
          "text": "Giảm các biến thiên quá nhanh trước khi bỏ mẫu, thay vì đợi lấy mẫu xong mới làm mượt.",
          "formula": "Prefilter → decimation"
        },
        {
          "start": 24,
          "title": "So sánh cùng kích thước",
          "text": "Phóng lại hai kết quả chỉ để nhìn rõ. Nhánh lọc trước ít họa tiết giả hơn nhưng mất chi tiết nhỏ.",
          "formula": "Phóng hiển thị không khôi phục chi tiết"
        },
        {
          "start": 32,
          "title": "Phân biệt độ nét và đúng mẫu",
          "text": "Ảnh có vẻ sắc không đồng nghĩa phản ánh đúng các vạch gốc; aliasing có thể tạo chi tiết giả.",
          "formula": "Giảm aliasing thường cần đánh đổi độ nét"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Các phương pháp nội suy",
      "id": "c07-bilinear",
      "title": "Bilinear: tính một pixel mới từ bốn pixel",
      "goal": "Thực hiện hai lần nội suy tuyến tính bằng số cụ thể.",
      "caption": "Bilinear là trung bình có trọng số theo khoảng cách trên hai chiều, không phải luôn lấy trung bình đều bốn góc.",
      "src": "media/detailed/c07-bilinear.mp4",
      "poster": "media/detailed/c07-bilinear.webp",
      "track": "media/detailed/c07-bilinear.vtt",
      "duration": 40,
      "source": "references/07-7.-Image-and-Video-Acquisition.pdf#page=18",
      "steps": [
        {
          "start": 0,
          "title": "Bốn điểm quanh vị trí mới",
          "text": "Các góc có giá trị 20, 100, 60, 180. Cần tính tại x=0,25 và y=0,75 trong ô.",
          "formula": "Trên: 20,100; dưới: 60,180"
        },
        {
          "start": 8,
          "title": "Nội suy hàng trên",
          "text": "Đi một phần tư từ 20 đến 100: giá trị trung gian là 40.",
          "formula": "Trên = 0,75×20 + 0,25×100 = 40"
        },
        {
          "start": 16,
          "title": "Nội suy hàng dưới",
          "text": "Đi một phần tư từ 60 đến 180: giá trị trung gian là 90.",
          "formula": "Dưới = 0,75×60 + 0,25×180 = 90"
        },
        {
          "start": 24,
          "title": "Nội suy theo chiều dọc",
          "text": "Đi ba phần tư từ hàng trên tới hàng dưới: kết quả 77,5.",
          "formula": "g = 0,25×40 + 0,75×90 = 77,5"
        },
        {
          "start": 32,
          "title": "So với nearest neighbor",
          "text": "Nearest chọn góc gần nhất là 60 trong ví dụ. Bilinear kết hợp bốn góc nên chuyển tiếp mượt hơn.",
          "formula": "Nearest: 60; bilinear: 77,5"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Chuyển đổi tốc độ khung hình",
      "id": "c07-temporal",
      "title": "Nội suy khung hình: bóng mờ và bù chuyển động",
      "goal": "So sánh trộn hai khung với đưa vật thể về vị trí giữa.",
      "caption": "Tăng frame rate bằng nội suy tạo khung ước lượng; nó không tương đương quay thêm khung thật.",
      "src": "media/detailed/c07-temporal.mp4",
      "poster": "media/detailed/c07-temporal.webp",
      "track": "media/detailed/c07-temporal.vtt",
      "duration": 40,
      "source": "references/07-7.-Image-and-Video-Acquisition.pdf#page=30",
      "steps": [
        {
          "start": 0,
          "title": "Hai khung đầu cuối",
          "text": "Một vật thể dịch ngang từ trái sang phải. Ta muốn tạo khung giữa tại thời điểm t=0,5.",
          "formula": "Có F0 và F1; cần F0,5"
        },
        {
          "start": 8,
          "title": "Trộn pixel theo thời gian",
          "text": "Lấy trung bình hai khung tạo hai bóng nửa sáng, thay vì một vật thể ở vị trí giữa.",
          "formula": "F0,5 = 0,5F0 + 0,5F1"
        },
        {
          "start": 16,
          "title": "Ước lượng độ dịch",
          "text": "Trong ví dụ, vật thể chỉ tịnh tiến và độ dịch được biết. Clip chưa chạy optical flow.",
          "formula": "Vector từ F0 đến F1: (+80,0)"
        },
        {
          "start": 24,
          "title": "Bù nửa chuyển động",
          "text": "Dịch vật thể 40 px để tạo khung giữa. Một vật thể rõ thay cho hai bóng mờ.",
          "formula": "v_giữa = 0,5 × v"
        },
        {
          "start": 32,
          "title": "Nhìn vào trường hợp khó",
          "text": "Bù chuyển động phụ thuộc ước lượng đúng; che khuất hay vật thể mới xuất hiện vẫn gây lỗi.",
          "formula": "Không có đủ thông tin để đoán mọi khung"
        }
      ]
    }
  ],
  "8": [
    {
      "kind": "image",
      "anchor": "8.1",
      "title": "Ordered dithering",
      "caption": "Các chấm đen trắng tạo cảm giác nhiều mức xám khi nhìn từ xa, dù mỗi điểm chỉ có hai trạng thái.",
      "src": "media/c08-slide-05.webp",
      "alt": "Ordered dithering — slide chương 8, trang PDF 5",
      "source": "references/08-8.-Image-and-Video-Rendering-and-Assessment-1-.pdf#page=5",
      "page": 5,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "8.3",
      "title": "SSIM: so sánh cấu trúc ảnh",
      "caption": "SSIM kết hợp so sánh độ sáng, tương phản và cấu trúc giữa ảnh tham chiếu và ảnh cần đánh giá.",
      "src": "media/c08-slide-20.webp",
      "alt": "SSIM: so sánh cấu trúc ảnh — slide chương 8, trang PDF 20",
      "source": "references/08-8.-Image-and-Video-Rendering-and-Assessment-1-.pdf#page=20",
      "page": 20,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "anchor": "8.1",
      "title": "Lượng tử hóa: ít mức xám hơn",
      "caption": "Số mức xám giảm từ 256 đến 2. Clip minh họa lượng tử hóa cường độ đồng đều, không phải thuật toán chọn bảng màu.",
      "src": "media/c08-quantize.mp4",
      "poster": "media/c08-quantize.webp",
      "track": "media/c08-quantize.vtt",
      "duration": 10
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "8.1",
      "id": "c08-dithering",
      "title": "Halftoning: hai màu nhưng nhìn như nhiều mức xám",
      "goal": "So sánh ngưỡng cố định với ordered dithering trên dải gradient.",
      "caption": "Dithering đổi cách phân bố các chấm nhị phân để mô phỏng sắc độ khi quan sát ở khoảng cách phù hợp.",
      "src": "media/detailed/c08-dithering.mp4",
      "poster": "media/detailed/c08-dithering.webp",
      "track": "media/detailed/c08-dithering.vtt",
      "duration": 40,
      "source": "references/08-8.-Image-and-Video-Rendering-and-Assessment-1-.pdf#page=5",
      "steps": [
        {
          "start": 0,
          "title": "Gradient nhiều mức xám",
          "text": "Ảnh gốc biến thiên mượt từ đen tới trắng. Thiết bị chỉ cho phép bật hoặc tắt điểm ảnh.",
          "formula": "Đầu ra chỉ có 0 hoặc 255"
        },
        {
          "start": 8,
          "title": "Ngưỡng cố định",
          "text": "So với cùng một T làm gradient bị chia thành hai vùng lớn, mất cảm giác chuyển sắc.",
          "formula": "Trắng nếu f > 128"
        },
        {
          "start": 16,
          "title": "Dùng ma trận ngưỡng",
          "text": "Ordered dithering lặp một mẫu Bayer 4×4; mỗi vị trí dùng một ngưỡng khác nhau.",
          "formula": "T(x,y) = 255 × (B+0,5) / 16"
        },
        {
          "start": 24,
          "title": "Quan sát mật độ chấm",
          "text": "Vùng sáng có nhiều chấm trắng hơn; vùng tối ít chấm trắng hơn. Mỗi pixel vẫn chỉ có hai mức.",
          "formula": "Mức xám được gợi bằng mật độ chấm"
        },
        {
          "start": 32,
          "title": "Nhìn ở hai tỉ lệ",
          "text": "Phóng to thấy mẫu chấm; thu nhỏ mắt tích hợp các điểm thành cảm giác sắc độ.",
          "formula": "Không tạo thêm mức tại từng pixel"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "8.3",
      "id": "c08-psnr",
      "title": "MSE và PSNR: tính từ sai số pixel",
      "goal": "Tính chỉ số bằng ví dụ rồi thấy giới hạn khi đánh giá cảm nhận.",
      "caption": "PSNR lớn thường nghĩa là sai số pixel nhỏ hơn với cùng thang giá trị; không bảo đảm ảnh đẹp hơn trong mọi tình huống.",
      "src": "media/detailed/c08-psnr.mp4",
      "poster": "media/detailed/c08-psnr.webp",
      "track": "media/detailed/c08-psnr.vtt",
      "duration": 40,
      "source": "references/08-8.-Image-and-Video-Rendering-and-Assessment-1-.pdf#page=17",
      "steps": [
        {
          "start": 0,
          "title": "Lấy ảnh chuẩn và ảnh lỗi",
          "text": "Ảnh x và y phải cùng kích thước, cùng thang giá trị trước khi so sánh.",
          "formula": "Ví dụ dùng ảnh xám 8 bit: MAX=255"
        },
        {
          "start": 8,
          "title": "Bình phương sai số",
          "text": "Với mỗi pixel, lấy x−y rồi bình phương; sai số âm và dương đều đóng góp.",
          "formula": "e_i² = (x_i − y_i)²"
        },
        {
          "start": 16,
          "title": "Lấy trung bình",
          "text": "Cộng sai số bình phương rồi chia số pixel để được MSE.",
          "formula": "MSE = Σ(x_i−y_i)² / N"
        },
        {
          "start": 24,
          "title": "Đổi sang PSNR",
          "text": "Ví dụ sai lệch +10 trên mọi pixel không clipping cho MSE=100 và PSNR≈28,13 dB.",
          "formula": "PSNR = 10 log10(255² / MSE)"
        },
        {
          "start": 32,
          "title": "Nhận ra giới hạn",
          "text": "Chỉ số tổng hợp không hiểu nội dung. Cùng mức sai số có thể gây cảm nhận khác nhau.",
          "formula": "MSE=0 → PSNR vô hạn theo định nghĩa"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "8.3",
      "id": "c08-ssim",
      "title": "SSIM: độ sáng, tương phản và cấu trúc",
      "goal": "Tách ba khía cạnh thay vì chỉ cộng sai số pixel.",
      "caption": "Clip dùng một cửa sổ toàn ảnh để minh họa công thức, không thay cho bản đồ SSIM cục bộ trong đánh giá thực tế.",
      "src": "media/detailed/c08-ssim.mp4",
      "poster": "media/detailed/c08-ssim.webp",
      "track": "media/detailed/c08-ssim.vtt",
      "duration": 40,
      "source": "references/08-8.-Image-and-Video-Rendering-and-Assessment-1-.pdf#page=18",
      "steps": [
        {
          "start": 0,
          "title": "Chọn hai ảnh để so sánh",
          "text": "Dùng ảnh tham chiếu và các phiên bản đổi sáng, đổi tương phản hoặc xáo pixel.",
          "formula": "So sánh trên cùng cửa sổ ảnh"
        },
        {
          "start": 8,
          "title": "Thành phần độ sáng",
          "text": "So sánh trung bình cường độ. Dịch toàn bộ mức sáng làm trung bình thay đổi.",
          "formula": "l(x,y) dùng μx và μy"
        },
        {
          "start": 16,
          "title": "Thành phần tương phản",
          "text": "So sánh độ lệch chuẩn. Dải sáng tối co lại làm độ lệch chuẩn giảm.",
          "formula": "c(x,y) dùng σx và σy"
        },
        {
          "start": 24,
          "title": "Thành phần cấu trúc",
          "text": "Hiệp phương sai cho biết các biến thiên có cùng vị trí và hướng hay không.",
          "formula": "s(x,y) dùng σxy"
        },
        {
          "start": 32,
          "title": "Kết hợp và đọc kết quả",
          "text": "Clip tính SSIM toàn ảnh với trọng số 1; triển khai thường tính theo các cửa sổ cục bộ.",
          "formula": "SSIM = l × c × s"
        }
      ]
    }
  ],
  "9": [
    {
      "kind": "image",
      "anchor": "9.1",
      "title": "Từ pixel đến superpixel",
      "caption": "Các vùng nhỏ gom pixel gần nhau có đặc trưng tương tự; xử lý trên vùng giúp giảm số phần tử.",
      "src": "media/c09-slide-08.webp",
      "alt": "Từ pixel đến superpixel — slide chương 9, trang PDF 8",
      "source": "references/10-9.-Image-and-Video-segmentation.pdf#page=8",
      "page": 8,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "9.2",
      "title": "Graph cut: chia đồ thị thành vùng",
      "caption": "Pixel là nút; liên kết thể hiện quan hệ giữa chúng. Source và sink biểu diễn hai phía của bài toán phân vùng.",
      "src": "media/c09-slide-18.webp",
      "alt": "Graph cut: chia đồ thị thành vùng — slide chương 9, trang PDF 18",
      "source": "references/10-9.-Image-and-Video-segmentation.pdf#page=18",
      "page": 18,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "9.1",
      "id": "c09-kmeans",
      "title": "K-means: gán cụm rồi cập nhật tâm",
      "goal": "Xem tâm cụm di chuyển trên dữ liệu 2D được tạo sẵn.",
      "caption": "K-means cần chọn K; SLIC còn dùng tọa độ và giới hạn vùng tìm kiếm, không chỉ đổi tên K-means.",
      "src": "media/detailed/c09-kmeans.mp4",
      "poster": "media/detailed/c09-kmeans.webp",
      "track": "media/detailed/c09-kmeans.vtt",
      "duration": 40,
      "source": "references/10-9.-Image-and-Video-segmentation.pdf#page=6",
      "steps": [
        {
          "start": 0,
          "title": "Biểu diễn pixel bằng đặc trưng",
          "text": "Mỗi điểm có hai đặc trưng mô phỏng. K-means không biết nhãn đúng; ta đặt K=3.",
          "formula": "Chọn K và các tâm ban đầu"
        },
        {
          "start": 8,
          "title": "Gán điểm vào tâm gần nhất",
          "text": "Tính khoảng cách Euclid từ mỗi điểm tới ba tâm, tô màu theo tâm gần nhất.",
          "formula": "label_i = arg min "
        },
        {
          "start": 16,
          "title": "Cập nhật các tâm",
          "text": "Thay mỗi tâm bằng trung bình những điểm đang thuộc cụm đó.",
          "formula": "μ_k = trung bình điểm trong cụm k"
        },
        {
          "start": 24,
          "title": "Lặp gán và cập nhật",
          "text": "Hai bước lặp làm các tâm ổn định dần. Khởi tạo khác có thể đưa tới nghiệm khác.",
          "formula": "Tối thiểu hóa tổng bình phương nội cụm"
        },
        {
          "start": 32,
          "title": "Liên hệ phân đoạn ảnh",
          "text": "Đặc trưng có thể là màu hoặc màu+khoảng cách. Cụm màu không tự bằng đối tượng ngữ nghĩa.",
          "formula": "K-means toàn cục ≠ SLIC cục bộ"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "9.2",
      "id": "c09-graphcut",
      "title": "Graph cut: cân bằng dữ liệu và ranh giới",
      "goal": "Xem một bài toán nhị phân nhỏ có thể kiểm tra mọi cách chia.",
      "caption": "Đây là minh họa năng lượng có thể giải bằng s-t min-cut; vét cạn chỉ phù hợp lưới rất nhỏ.",
      "src": "media/detailed/c09-graphcut.mp4",
      "poster": "media/detailed/c09-graphcut.webp",
      "track": "media/detailed/c09-graphcut.vtt",
      "duration": 40,
      "source": "references/10-9.-Image-and-Video-segmentation.pdf#page=18",
      "steps": [
        {
          "start": 0,
          "title": "Lưới 3×3 thành đồ thị",
          "text": "Mỗi pixel là nút. Cạnh nối các láng giềng ngang dọc; hai nhãn là nền và vật thể.",
          "formula": "9 nút → 2⁹ = 512 cách gán nhãn"
        },
        {
          "start": 8,
          "title": "Chi phí dữ liệu",
          "text": "Pixel sáng được ưu tiên làm vật thể, pixel tối ưu tiên làm nền. Chọn nhãn trái ưu tiên có chi phí.",
          "formula": "D_i(0)=I_i; D_i(1)=1−I_i"
        },
        {
          "start": 16,
          "title": "Chi phí ranh giới",
          "text": "Phạt hai pixel láng giềng khác nhãn, nhất là khi độ sáng của chúng giống nhau.",
          "formula": "E = ΣD_i + Σw_ij [l_i ≠ l_j]"
        },
        {
          "start": 24,
          "title": "Tìm cách chia nhỏ nhất",
          "text": "Clip duyệt đủ 512 cách gán để kiểm tra nghiệm tối ưu của ví dụ, thay vì triển khai thuật toán max-flow.",
          "formula": "Chọn nhãn có E nhỏ nhất"
        },
        {
          "start": 32,
          "title": "Phân biệt với normalized cut",
          "text": "Năng lượng nhị phân có source/sink trong clip khác tiêu chí Ncut và lời giải trị riêng.",
          "formula": "Graph cut nhị phân ≠ normalized cut"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "9.5",
      "id": "c09-frame-difference",
      "title": "Phân đoạn chuyển động bằng sai khác khung",
      "goal": "Nhìn vùng thay đổi được tạo và ngưỡng hóa như thế nào.",
      "caption": "Sai khác khung là phát hiện thay đổi. Nó không tự phân biệt chuyển động vật thể với chuyển động camera.",
      "src": "media/detailed/c09-frame-difference.mp4",
      "poster": "media/detailed/c09-frame-difference.webp",
      "track": "media/detailed/c09-frame-difference.vtt",
      "duration": 40,
      "source": "references/10-9.-Image-and-Video-segmentation.pdf#page=37",
      "steps": [
        {
          "start": 0,
          "title": "Chụp hai khung liên tiếp",
          "text": "Nền đứng yên, một khối sáng di chuyển. Camera cố định trong ví dụ này.",
          "formula": "Khung F(t−1) và F(t)"
        },
        {
          "start": 8,
          "title": "Trừ hai khung",
          "text": "Lấy trị tuyệt đối của hiệu để ghi nhận cả vùng vật thể rời đi và vùng mới tới.",
          "formula": "D = "
        },
        {
          "start": 16,
          "title": "Ngưỡng hóa ảnh sai khác",
          "text": "Giữ pixel có thay đổi lớn hơn T. Sai khác nhỏ bị coi là không chuyển động.",
          "formula": "Mask = D > T"
        },
        {
          "start": 24,
          "title": "Làm sạch mặt nạ",
          "text": "Opening có thể loại các chấm nhiễu nhỏ; phải kiểm tra không xóa vật thể nhỏ cần giữ.",
          "formula": "Làm sạch ≠ hiểu ngữ nghĩa"
        },
        {
          "start": 32,
          "title": "Đọc đúng vùng phát hiện",
          "text": "Mask thường chứa cả vị trí cũ lẫn mới. Camera rung hay đổi sáng cũng tạo sai khác.",
          "formula": "Vùng thay đổi không luôn là toàn vật thể"
        }
      ]
    }
  ],
  "10": [
    {
      "kind": "image",
      "anchor": "10.1",
      "title": "Trục chính, trục phụ và hộp bao",
      "caption": "Trục chính đi theo hướng dài nhất; trục phụ vuông góc với trục chính. Hộp bao và tỉ lệ hai trục giúp mô tả hình dạng. Ví dụ dùng một elip nằm ngang để dễ quan sát.",
      "src": "media/c10-diagram.webp",
      "alt": "Trục chính, trục phụ và hộp bao — sơ đồ minh họa theo kiến thức slide",
      "source": "references/11-10.-Feature-extraction.pdf#page=4",
      "page": 4,
      "width": 1600,
      "height": 950,
      "derived": true
    },
    {
      "kind": "image",
      "anchor": "10.5",
      "title": "Đặc trưng từ mạng CNN",
      "caption": "Ảnh đi qua mạng để tạo feature map; các lớp học những biểu diễn hữu ích cho bước nhận dạng phía sau.",
      "src": "media/c10-slide-29.webp",
      "alt": "Đặc trưng từ mạng CNN — slide chương 10, trang PDF 29",
      "source": "references/11-10.-Feature-extraction.pdf#page=29",
      "page": 29,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "10.2",
      "id": "c10-shape",
      "title": "Đặc trưng hình dạng: diện tích, hộp bao và trục",
      "goal": "Theo dõi đặc trưng nào thay đổi khi xoay cùng một hình.",
      "caption": "Bất biến hình học là phát biểu lý tưởng; lấy mẫu pixel, cắt biên và nội suy có thể tạo sai số nhỏ.",
      "src": "media/detailed/c10-shape.mp4",
      "poster": "media/detailed/c10-shape.webp",
      "track": "media/detailed/c10-shape.vtt",
      "duration": 40,
      "source": "references/11-10.-Feature-extraction.pdf#page=10",
      "steps": [
        {
          "start": 0,
          "title": "Một vùng nhị phân",
          "text": "Xét hình elip mẫu. Diện tích xấp xỉ bằng số pixel thuộc vật thể.",
          "formula": "Area = số pixel có nhãn 1"
        },
        {
          "start": 8,
          "title": "Tìm hộp bao theo trục ảnh",
          "text": "Lấy min/max tọa độ x,y. Hộp bao trục ảnh thay đổi khi xoay vật thể.",
          "formula": "Box = [xmin,ymin,xmax,ymax]"
        },
        {
          "start": 16,
          "title": "Tìm hai trục chính",
          "text": "Hiệp phương sai tọa độ vùng cho các hướng riêng; hướng phương sai lớn là trục chính.",
          "formula": "Eigenvector lớn → hướng trải rộng nhất"
        },
        {
          "start": 24,
          "title": "Xoay hình mẫu",
          "text": "Xoay làm hộp bao trục ảnh đổi, nhưng diện tích và độ dài hai trục chính lý tưởng giữ nguyên.",
          "formula": "Bất biến lý tưởng; raster có sai số"
        },
        {
          "start": 32,
          "title": "Chọn đặc trưng phù hợp",
          "text": "Diện tích và tỉ lệ trục mô tả hình dạng; hộp bao bổ sung vị trí và phạm vi.",
          "formula": "Không dùng một đặc trưng cho mọi bài toán"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "10.3",
      "id": "c10-pca",
      "title": "PCA: tìm hướng biến thiên lớn nhất",
      "goal": "Xem dữ liệu 2D được tâm hóa rồi chiếu xuống một chiều.",
      "caption": "PCA tối đa hóa phương sai giữ lại khi chiếu tuyến tính trực giao; nó không sử dụng nhãn lớp.",
      "src": "media/detailed/c10-pca.mp4",
      "poster": "media/detailed/c10-pca.webp",
      "track": "media/detailed/c10-pca.vtt",
      "duration": 40,
      "source": "references/11-10.-Feature-extraction.pdf#page=24",
      "steps": [
        {
          "start": 0,
          "title": "Đám mây dữ liệu 2D",
          "text": "Các điểm tạo thành đám mây kéo dài theo một hướng. Ta muốn giữ thông tin bằng ít tọa độ hơn.",
          "formula": "Đầu vào: vector x=(x1,x2)"
        },
        {
          "start": 8,
          "title": "Trừ trung bình",
          "text": "Đưa tâm dữ liệu về gốc trước khi tính hiệp phương sai.",
          "formula": "Xc = X − mean(X)"
        },
        {
          "start": 16,
          "title": "Tìm hướng riêng lớn nhất",
          "text": "Vector riêng có trị riêng lớn nhất là hướng phương sai lớn nhất của dữ liệu.",
          "formula": "C v1 = λ1 v1; λ1 lớn nhất"
        },
        {
          "start": 24,
          "title": "Chiếu lên trục đầu tiên",
          "text": "Mỗi điểm được thay bằng tọa độ vô hướng trên v1. Một phần biến thiên ở trục còn lại bị mất.",
          "formula": "z = Xc × v1"
        },
        {
          "start": 32,
          "title": "Tái tạo xấp xỉ",
          "text": "Chiếu ngược cho điểm nằm trên trục chính. Clip hiển thị phần trăm phương sai giữ lại.",
          "formula": "X̂ = z v1ᵀ + mean(X)"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "10.2",
      "id": "c10-glcm",
      "title": "GLCM: từ cặp láng giềng đến đặc trưng texture",
      "goal": "Đếm cặp pixel bên phải và tính tương phản kết cấu.",
      "caption": "GLCM phụ thuộc lượng tử hóa mức xám, hướng và khoảng cách láng giềng; clip đếm có hướng, chưa đối xứng hóa.",
      "src": "media/detailed/c10-glcm.mp4",
      "poster": "media/detailed/c10-glcm.webp",
      "track": "media/detailed/c10-glcm.vtt",
      "duration": 40,
      "source": "references/11-10.-Feature-extraction.pdf#page=16",
      "steps": [
        {
          "start": 0,
          "title": "Hai kiểu kết cấu",
          "text": "Một ảnh gồm các dải lớn, ảnh kia gồm ô xen kẽ. Dùng hai mức xám 0 và 1.",
          "formula": "Cùng giá trị nhưng khác bố trí"
        },
        {
          "start": 8,
          "title": "Chọn quan hệ láng giềng",
          "text": "Với mỗi pixel, xét pixel ngay bên phải; không đếm vòng từ cuối hàng về đầu hàng.",
          "formula": "Offset: (dx,dy) = (1,0)"
        },
        {
          "start": 16,
          "title": "Đếm cặp vào ma trận",
          "text": "Cặp (0,1) tăng ô hàng 0 cột 1. Tương tự cho (0,0), (1,0), (1,1).",
          "formula": "GLCM(i,j) = số cặp i → j"
        },
        {
          "start": 24,
          "title": "Chuẩn hóa và tính tương phản",
          "text": "Chia mỗi ô cho tổng số cặp, rồi nhân với bình phương chênh mức xám.",
          "formula": "Contrast = Σ(i−j)² P(i,j)"
        },
        {
          "start": 32,
          "title": "So sánh hai texture",
          "text": "Ô xen kẽ có nhiều cặp khác mức nên contrast lớn hơn ở offset đang chọn.",
          "formula": "Texture phụ thuộc hướng và khoảng cách"
        }
      ]
    }
  ],
  "11": [
    {
      "kind": "image",
      "anchor": "Các độ đo",
      "title": "IoU: nhìn phần giao và phần hợp",
      "caption": "Ba ví dụ dùng hai hộp vuông cùng kích thước. Hộp cam luôn lệch dọc 70 px; giảm lệch ngang từ trái sang phải làm phần giao và IoU tăng lên.",
      "src": "media/c11-diagram.webp",
      "alt": "IoU: nhìn phần giao và phần hợp — sơ đồ minh họa theo kiến thức slide",
      "source": "references/12-11.-Object-detection.pdf#page=5",
      "page": 5,
      "width": 1600,
      "height": 950,
      "derived": true
    },
    {
      "kind": "image",
      "anchor": "Phương pháp dựa trên anchor",
      "title": "Phát hiện đối tượng bằng YOLO",
      "caption": "Phân biệt hai đầu ra: vị trí bounding box và nhãn lớp. Phát hiện cần cả định vị lẫn phân loại.",
      "src": "media/c11-slide-20.webp",
      "alt": "Phát hiện đối tượng bằng YOLO — slide chương 11, trang PDF 20",
      "source": "references/12-11.-Object-detection.pdf#page=20",
      "page": 20,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Các độ đo",
      "id": "c11-iou",
      "title": "IoU: tính diện tích giao và hợp của hai hộp",
      "goal": "Tính số cụ thể rồi di chuyển hộp để xem IoU thay đổi.",
      "caption": "IoU đo độ khớp vị trí. Confidence là điểm tin cậy của mô hình và là một đại lượng khác.",
      "src": "media/detailed/c11-iou.mp4",
      "poster": "media/detailed/c11-iou.webp",
      "track": "media/detailed/c11-iou.vtt",
      "duration": 40,
      "source": "references/12-11.-Object-detection.pdf#page=5",
      "steps": [
        {
          "start": 0,
          "title": "Hai hộp 100×100",
          "text": "Hộp thật và hộp dự đoán có cùng kích thước; bắt đầu không chồng lấn.",
          "formula": "Mỗi hộp có diện tích 10.000"
        },
        {
          "start": 8,
          "title": "Tìm vùng giao",
          "text": "Khi hộp dự đoán lệch ngang 50, phần giao rộng 50 và cao 100.",
          "formula": "Intersection = 50×100 = 5.000"
        },
        {
          "start": 16,
          "title": "Tính vùng hợp",
          "text": "Cộng diện tích hai hộp rồi trừ phần giao để không đếm hai lần.",
          "formula": "Union = 10.000+10.000−5.000 = 15.000"
        },
        {
          "start": 24,
          "title": "Chia giao cho hợp",
          "text": "Tỉ lệ trong ví dụ là 1/3. IoU không phải phần trăm diện tích chỉ của hộp thật.",
          "formula": "IoU = 5.000 / 15.000 ≈ 0,333"
        },
        {
          "start": 32,
          "title": "Đưa hai hộp trùng nhau",
          "text": "Khi giao bằng hợp, IoU=1. Hộp không chạm có IoU=0.",
          "formula": "0 ≤ IoU ≤ 1"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "Phương pháp dựa trên anchor",
      "id": "c11-nms",
      "title": "NMS: bỏ các hộp dự đoán trùng lặp",
      "goal": "Xem cách giữ hộp điểm cao và loại hộp chồng lấn cùng lớp.",
      "caption": "Clip minh họa hard NMS trong một lớp; NMS không thay cho bước dự đoán và không phải mọi detector đều dùng nó.",
      "src": "media/detailed/c11-nms.mp4",
      "poster": "media/detailed/c11-nms.webp",
      "track": "media/detailed/c11-nms.vtt",
      "duration": 40,
      "source": "references/12-11.-Object-detection.pdf#page=20",
      "steps": [
        {
          "start": 0,
          "title": "Nhiều hộp cho cùng đối tượng",
          "text": "Mô hình có thể đề xuất nhiều hộp gần nhau. Clip dùng hộp và confidence tạo sẵn.",
          "formula": "Ví dụ minh họa, không chạy YOLO"
        },
        {
          "start": 8,
          "title": "Sắp theo confidence",
          "text": "Chọn hộp A có điểm 0,95 trước. Điểm cao nhất được giữ lại trong vòng này.",
          "formula": "A:0,95; B:0,85; C:0,75"
        },
        {
          "start": 16,
          "title": "Tính IoU với hộp đang giữ",
          "text": "B chồng mạnh với A, còn C nằm ở vùng khác. So sánh với ngưỡng NMS 0,5.",
          "formula": "Nếu IoU(A,B)>0,5 → loại B"
        },
        {
          "start": 24,
          "title": "Lặp với hộp còn lại",
          "text": "Giữ C vì ít chồng lấn với A. Kết quả còn hai hộp thay vì ba.",
          "formula": "Giữ A và C"
        },
        {
          "start": 32,
          "title": "Nhận ra giới hạn",
          "text": "NMS cứng có thể loại nhầm hộp của hai vật thể cùng lớp đứng sát nhau.",
          "formula": "Ngưỡng ảnh hưởng số hộp được giữ"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "11.2",
      "id": "c11-detector-pipeline",
      "title": "One-stage và two-stage: khác ở đâu?",
      "goal": "Đọc dòng dữ liệu của hai họ bộ phát hiện đối tượng.",
      "caption": "Đây là sơ đồ nguyên lý; không thực thi mô hình hay báo kết quả benchmark của một phiên bản detector cụ thể.",
      "src": "media/detailed/c11-detector-pipeline.mp4",
      "poster": "media/detailed/c11-detector-pipeline.webp",
      "track": "media/detailed/c11-detector-pipeline.vtt",
      "duration": 40,
      "source": "references/12-11.-Object-detection.pdf#page=18",
      "steps": [
        {
          "start": 0,
          "title": "Đầu vào và hai loại đầu ra",
          "text": "Object detection dự đoán cả vị trí hộp và lớp. Chỉ nói có vật thể gì chưa đủ.",
          "formula": "Đầu ra: bounding box + nhãn lớp"
        },
        {
          "start": 8,
          "title": "Two-stage: sinh đề xuất vùng",
          "text": "Một nhánh đề xuất các vùng có khả năng chứa vật thể từ đặc trưng ảnh.",
          "formula": "Ảnh → backbone → region proposals"
        },
        {
          "start": 16,
          "title": "Two-stage: xử lý từng vùng",
          "text": "Đặc trưng vùng được dùng để phân loại và tinh chỉnh tọa độ hộp.",
          "formula": "RoI features → lớp và box"
        },
        {
          "start": 24,
          "title": "One-stage: dự đoán trực tiếp",
          "text": "Họ one-stage dự đoán hộp và lớp trực tiếp từ các feature map mà không có pha RoI riêng.",
          "formula": "Backbone → heads dự đoán"
        },
        {
          "start": 32,
          "title": "So sánh theo mục tiêu",
          "text": "Không có kết luận mọi one-stage luôn nhanh hoặc mọi two-stage luôn chính xác hơn. Cần đo trên cùng điều kiện.",
          "formula": "Kiến trúc + dữ liệu + cấu hình đều quan trọng"
        }
      ]
    }
  ],
  "12": [
    {
      "kind": "image",
      "anchor": "Các khái niệm",
      "title": "Từ ảnh đến nhãn lớp",
      "caption": "Theo chiều pipeline: ảnh → đặc trưng → bộ phân loại → nhãn. Vector đặc trưng là cầu nối giữa ảnh và quyết định.",
      "src": "media/c12-slide-05.webp",
      "alt": "Từ ảnh đến nhãn lớp — slide chương 12, trang PDF 5",
      "source": "references/13-12.-Image-pattern-classification.pdf#page=5",
      "page": 5,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "image",
      "anchor": "12.5",
      "title": "Kiến trúc LeNet-5",
      "caption": "Các khối convolution và pooling trích đặc trưng; các lớp cuối dùng đặc trưng để dự đoán lớp.",
      "src": "media/c12-slide-29.webp",
      "alt": "Kiến trúc LeNet-5 — slide chương 12, trang PDF 29",
      "source": "references/13-12.-Image-pattern-classification.pdf#page=29",
      "page": 29,
      "width": 1600,
      "height": 900
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "12.2",
      "id": "c12-prototype",
      "title": "Phân loại bằng khoảng cách tới nguyên mẫu",
      "goal": "Tính hai khoảng cách Euclid rồi chọn lớp gần nhất.",
      "caption": "Bộ phân loại nguyên mẫu không đồng nghĩa K-means: nguyên mẫu có thể được tính từ dữ liệu đã có nhãn.",
      "src": "media/detailed/c12-prototype.mp4",
      "poster": "media/detailed/c12-prototype.webp",
      "track": "media/detailed/c12-prototype.vtt",
      "duration": 40,
      "source": "references/13-12.-Image-pattern-classification.pdf#page=10",
      "steps": [
        {
          "start": 0,
          "title": "Đặc trưng và nguyên mẫu",
          "text": "Hai lớp có nguyên mẫu μA=(2,2), μB=(7,6). Mẫu cần gán nhãn là x=(3,4).",
          "formula": "Mỗi nguyên mẫu thường là trung bình lớp"
        },
        {
          "start": 8,
          "title": "Tính khoảng cách tới A",
          "text": "Chênh tọa độ là (1,2). Tổng bình phương bằng 5.",
          "formula": "dA = √((3−2)²+(4−2)²) = √5"
        },
        {
          "start": 16,
          "title": "Tính khoảng cách tới B",
          "text": "Chênh tọa độ là (−4,−2). Tổng bình phương bằng 20.",
          "formula": "dB = √((3−7)²+(4−6)²) = √20"
        },
        {
          "start": 24,
          "title": "Chọn lớp gần hơn",
          "text": "Vì √5 < √20, mẫu được gán vào A. Có thể so sánh trực tiếp bình phương khoảng cách.",
          "formula": "dA≈2,24 < dB≈4,47 → A"
        },
        {
          "start": 32,
          "title": "Kiểm tra thang đặc trưng",
          "text": "Một đặc trưng có thang số quá lớn có thể chi phối Euclid. Cần cân nhắc chuẩn hóa phù hợp.",
          "formula": "Khoảng cách phụ thuộc biểu diễn"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "12.3",
      "id": "c12-bayes",
      "title": "Bayes: bằng chứng và xác suất tiên nghiệm",
      "goal": "Thấy quyết định thay đổi khi đổi prior với cùng một quan sát.",
      "caption": "Likelihood, prior và posterior là ba khái niệm khác nhau. Quy tắc quyết định còn phụ thuộc chi phí sai.",
      "src": "media/detailed/c12-bayes.mp4",
      "poster": "media/detailed/c12-bayes.webp",
      "track": "media/detailed/c12-bayes.vtt",
      "duration": 40,
      "source": "references/13-12.-Image-pattern-classification.pdf#page=15",
      "steps": [
        {
          "start": 0,
          "title": "Hai lớp Gaussian",
          "text": "Hai phân bố có trung bình −1 và +1, cùng độ lệch chuẩn 1. Quan sát x=0,2.",
          "formula": "p(x"
        },
        {
          "start": 8,
          "title": "Tiên nghiệm bằng nhau",
          "text": "Với P(A)=P(B)=0,5, B có likelihood lớn hơn tại x=0,2 nên được ưu tiên.",
          "formula": "Score_k = p(x"
        },
        {
          "start": 16,
          "title": "Đổi xác suất tiên nghiệm",
          "text": "Nếu A phổ biến hơn, đặt P(A)=0,8 và P(B)=0,2. Likelihood của x không đổi.",
          "formula": "Prior khác → trọng số khác"
        },
        {
          "start": 24,
          "title": "Chuẩn hóa thành hậu nghiệm",
          "text": "Chia các score cho tổng để được P(A",
          "formula": "x), P(B"
        },
        {
          "start": 32,
          "title": "Gắn với hàm mất mát",
          "text": "Chọn hậu nghiệm lớn nhất ứng với mất mát 0–1. Nếu chi phí sai khác nhau, phải tối thiểu hóa rủi ro.",
          "formula": "MAP cho loss 0–1; risk cho loss tổng quát"
        }
      ]
    },
    {
      "kind": "video",
      "detailed": true,
      "anchor": "12.5",
      "id": "c12-cnn",
      "title": "CNN: convolution → ReLU → pooling",
      "goal": "Theo một ví dụ số qua ba lớp cơ bản của mạng tích chập.",
      "caption": "CNN học kernel trong quá trình huấn luyện. Kernel đặt tay ở clip chỉ giúp hiểu các phép tính forward pass.",
      "src": "media/detailed/c12-cnn.mp4",
      "poster": "media/detailed/c12-cnn.webp",
      "track": "media/detailed/c12-cnn.vtt",
      "duration": 40,
      "source": "references/13-12.-Image-pattern-classification.pdf#page=29",
      "steps": [
        {
          "start": 0,
          "title": "Ảnh đầu vào và kernel",
          "text": "Dùng ma trận nhỏ và một kernel phát hiện biến thiên dọc. Trọng số được đặt tay để minh họa.",
          "formula": "Không huấn luyện hay nhận dạng thật"
        },
        {
          "start": 8,
          "title": "Tạo feature map",
          "text": "Kernel trượt trên ảnh, lấy tổng tích tại từng vị trí. Dùng valid nên kích thước nhỏ đi.",
          "formula": "6×6 với kernel 3×3 → map 4×4"
        },
        {
          "start": 16,
          "title": "Áp dụng ReLU",
          "text": "Giữ số dương và thay số âm bằng 0. Đây là phép phi tuyến sau convolution.",
          "formula": "ReLU(z) = max(0,z)"
        },
        {
          "start": 24,
          "title": "Max pooling 2×2",
          "text": "Mỗi ô 2×2 giữ giá trị lớn nhất với stride 2. Map 4×4 trở thành 2×2.",
          "formula": "4×4 → 2×2"
        },
        {
          "start": 32,
          "title": "Từ đặc trưng tới nhãn",
          "text": "Mạng hoàn chỉnh cần thêm các lớp và trọng số học từ dữ liệu. Clip dừng ở đặc trưng, chưa tạo nhãn dự đoán.",
          "formula": "Feature map ≠ kết quả phân loại cuối"
        }
      ]
    }
  ]
};
