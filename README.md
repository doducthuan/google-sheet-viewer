# Hướng dẫn cài đặt và chạy ứng dụng

## 1. Cài đặt Python và các thư viện cần thiết

- Đảm bảo đã cài đặt **Python** (phiên bản **3.6 trở lên**).
- Mở **Command Prompt** hoặc **PowerShell**.
- Chạy lệnh sau để cài đặt các thư viện cần thiết:
- Tạo môi trường ảo : python -m venv google_sheet_viewer ( để tránh xung đột với các thư viện khác khi cài đặt )
- Kích hoạt môi trường ảo : google_sheet_viewer\Scripts\activate
- Sau đó chạy các lệnh bên dưới
```bash
pip install -r requirements.txt
```

## 2. Tạo Google Cloud Project và lấy credentials

### Bật Google Sheets API:
- Truy cập [Google Cloud Console](https://console.cloud.google.com/)
- Tạo một **Project mới**
- Bật **Google Sheets API**

### Tạo Service Account:
- Truy cập `IAM & Admin` > `Service Accounts`
- Click **"Create Service Account"**
- Đặt tên và tạo
- Tạo **key** dưới dạng **JSON** và **tải về**
- Đổi tên file JSON vừa tải về thành `credentials.json`
- Đặt file `credentials.json` vào cùng thư mục với `app.py`

## 3. Chia sẻ Google Sheet với Service Account

- Mở **Google Sheet** của 
- Click nút **"Share" (Chia sẻ)**
- Thêm email của Service Account *(có thể tìm thấy trong file `credentials.json`)*
- Cấp quyền **"Viewer" (Người xem)**

## 4. Chạy ứng dụng

- Mở **Command Prompt** hoặc **PowerShell**
- Di chuyển đến thư mục chứa file `app.py`

```bash
python app.py
```

## 5. Truy cập ứng dụng

- Mở **trình duyệt web**
- Truy cập địa chỉ: [http://localhost:5000](http://localhost:5000)
