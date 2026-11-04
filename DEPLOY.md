# Đưa trang lên Vercel

Trang là web tĩnh (HTML/JS/CSS + video + PDF), không cần build. Tổng ~155 MB (video 135 MB, slide PDF 20 MB).

## Vì sao nên dùng GitHub thay vì `vercel` CLI

Gói Hobby của Vercel giới hạn **100 MB** cho file upload bằng CLI, mà thư mục này nặng ~155 MB nên CLI sẽ báo lỗi.
Deploy qua GitHub không bị giới hạn đó (mỗi file < 100 MB là được, video lớn nhất ~14 MB).

## Các bước

1. Tạo repo mới trên GitHub (ví dụ `imp302-on`), để Private cũng được.
2. Trong thư mục này chạy:
   ```bash
   git init
   git add .
   git commit -m "feat: IMP302 study site"
   git branch -M main
   git remote add origin https://github.com/<ten-ban>/imp302-on.git
   git push -u origin main
   ```
   File `.gitignore` đã loại `_video-build/.venv` và `_video-build/cache` (gần 1 GB) nên không bị đẩy lên.
3. Vào https://vercel.com/new, chọn **Import** repo vừa tạo.
4. Cấu hình:
   - Framework Preset: **Other**
   - Build Command: để trống
   - Output Directory: để trống (hoặc `.`)
   - Root Directory: `./`
5. Bấm **Deploy**. Khoảng 1–2 phút là có link `https://<ten-project>.vercel.app`.

Mỗi lần sửa nội dung: `git add . && git commit -m "..." && git push`, Vercel tự deploy lại.

## Lưu ý

- `.vercelignore` đã loại `_video-build`, `serve.py`, `start.bat` khỏi bản deploy.
- Tiến độ học (localStorage) lưu theo từng địa chỉ web, nên trên link Vercel sẽ bắt đầu lại từ đầu.
- Link `.vercel.app` là công khai; ai có link đều xem được slide và video.
- Sau khi sửa file JS/CSS/dữ liệu, bản cũ có thể còn trong cache trình duyệt: nhấn Ctrl+F5.
