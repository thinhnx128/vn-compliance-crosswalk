---
ma: DP-05
ten: Quy trình xử lý vi phạm dữ liệu cá nhân
dieu_khoan: "Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 Điều 23; Nghị định 356/2025/NĐ-CP Điều 28, 29; ISO/IEC 27001 A.5.24–5.28"
---

# 1. Thế nào là vi phạm dữ liệu cá nhân

Sự cố làm dữ liệu cá nhân bị truy cập, tiết lộ, thay đổi, mất, hủy trái phép hoặc ngoài ý muốn; dữ liệu bị xử lý sai mục đích, không đúng thỏa thuận với chủ thể; hoặc không bảo đảm quyền của chủ thể dữ liệu. Ví dụ: gửi nhầm email chứa danh sách khách hàng; mất máy tính có dữ liệu nhân sự; tài khoản bị chiếm và dữ liệu bị tải xuống; nhân viên tự ý chia sẻ dữ liệu ra ngoài; mã độc tống tiền mã hóa cơ sở dữ liệu khách hàng.

# 2. Thời hạn theo luật

| Việc | Thời hạn | Căn cứ |
|---|---|---|
| Thông báo cơ quan chuyên trách bảo vệ dữ liệu cá nhân, khi vi phạm có thể gây tổn hại đến quốc phòng, an ninh quốc gia, trật tự, an toàn xã hội hoặc xâm phạm tính mạng, sức khỏe, danh dự, nhân phẩm, tài sản của chủ thể | **Chậm nhất 72 giờ kể từ khi phát hiện** hành vi vi phạm | Luật Điều 23 khoản 1 |
| Vi phạm liên quan dữ liệu vị trí hoặc dữ liệu sinh trắc học: thông báo cho chủ thể dữ liệu bị ảnh hưởng | Không quá **72 giờ** kể từ thời điểm phát hiện | NĐ 356 Điều 29 khoản 1 điểm a |
| Bên xử lý phát hiện vi phạm: thông báo bên kiểm soát | "Kịp thời" theo luật; theo hợp đồng [● khuyến nghị không quá 24 giờ] | Luật Điều 23 khoản 1 |
| Lưu hồ sơ vi phạm liên quan dữ liệu vị trí, sinh trắc học | Tối thiểu 5 năm kể từ ngày khắc phục xong | NĐ 356 Điều 29 khoản 1 điểm c |

Ngoài trường hợp 72 giờ nêu trên, Luật Điều 23 khoản 3 quy định thông báo cho cơ quan chuyên trách khi: phát hiện hành vi vi phạm quy định về bảo vệ dữ liệu cá nhân; dữ liệu bị xử lý sai mục đích, không đúng thỏa thuận với chủ thể; không bảo đảm hoặc thực hiện không đúng quyền của chủ thể dữ liệu.

Thông báo gửi đến cơ quan chuyên trách bảo vệ dữ liệu cá nhân hoặc qua Cổng thông tin quốc gia về bảo vệ dữ liệu cá nhân, theo **Mẫu số 08** tại Phụ lục Nghị định 356/2025/NĐ-CP.

# 3. Các bước

| Bước | Nội dung | Phụ trách | Thời hạn |
|---|---|---|---|
| 1 | Báo ngay khi phát hiện qua [● kênh báo cáo] | Người phát hiện | Ngay |
| 2 | Ghi nhận **thời điểm phát hiện**: đây là mốc tính 72 giờ | {{DPO}} | Ngay |
| 3 | Ngăn chặn: thu hồi email, khóa tài khoản, cô lập hệ thống | CNTT | Càng sớm càng tốt |
| 4 | Đánh giá: loại dữ liệu, số chủ thể, khả năng gây tổn hại, nguyên nhân | {{DPO}} cùng CNTT | Trong [● 24] giờ |
| 5 | Lập **biên bản xác nhận** về việc xảy ra hành vi vi phạm | {{DPO}} | Trước khi thông báo |
| 6 | Quyết định thông báo; lãnh đạo phê duyệt nội dung | {{NGUOI_PHE_DUYET}} | Trong 72 giờ |
| 7 | Thông báo cơ quan chuyên trách theo Mẫu số 08 | {{DPO}} | Trong 72 giờ |
| 8 | Thông báo chủ thể dữ liệu bị ảnh hưởng; bắt buộc trong 72 giờ nếu là dữ liệu vị trí, sinh trắc học | {{DPO}} | Theo mục 2 |
| 9 | Khắc phục hậu quả; phối hợp với cơ quan chuyên trách | Đơn vị liên quan | Theo kế hoạch |
| 10 | Lưu hồ sơ vào sổ REG-DP (sheet Vi phạm) | {{DPO}} | — |

Nếu {{TEN_CONG_TY}} là **bên xử lý**: thông báo kịp thời cho bên kiểm soát theo hợp đồng (DP-06) và cung cấp thông tin để bên kiểm soát thực hiện nghĩa vụ thông báo.

# 4. Nội dung thông báo cơ quan chuyên trách (NĐ 356 Điều 28 khoản 1)

- Mô tả tính chất của vi phạm: thời gian, địa điểm, hành vi, tổ chức, cá nhân, các loại dữ liệu cá nhân và số lượng dữ liệu liên quan.
- Chi tiết liên lạc của bộ phận, nhân sự bảo vệ dữ liệu cá nhân hoặc tổ chức, cá nhân cung cấp dịch vụ bảo vệ dữ liệu cá nhân.
- Mô tả các hậu quả, thiệt hại có thể xảy ra.
- Mô tả biện pháp được đưa ra để giải quyết, giảm thiểu tác hại.

# 5. Nội dung thông báo cho chủ thể với dữ liệu vị trí, sinh trắc học (NĐ 356 Điều 29 khoản 2)

Thời điểm và hình thức phát hiện; loại dữ liệu bị ảnh hưởng; mức độ nghiêm trọng và rủi ro; biện pháp đã, đang và sẽ thực hiện; hướng dẫn chủ thể tự phòng ngừa; thông tin liên hệ. Nếu không thể thông báo cho tất cả trong 72 giờ vì lý do kỹ thuật hoặc khẩn cấp: thông báo công khai trên trang thông tin điện tử, ứng dụng của tổ chức, và gửi cho từng chủ thể ngay khi điều kiện cho phép (khoản 3).

# 6. Ma trận nội bộ để ưu tiên xử lý

Bảng này là công cụ nội bộ, không thay cho điều kiện thông báo ở mục 2.

| Mức | Ví dụ | Hành động |
|---|---|---|
| Thấp | Dữ liệu đã mã hóa mạnh, khóa không bị lộ; gửi nhầm nội bộ và đã xóa | Ghi nhận, đánh giá điều kiện thông báo |
| Trung bình | Lộ thông tin liên hệ của một nhóm nhỏ | Đánh giá điều kiện thông báo; cân nhắc báo cho chủ thể |
| Cao | Lộ dữ liệu nhạy cảm hoặc số lượng lớn | Thông báo cơ quan chuyên trách và chủ thể |

# 7. Sau vi phạm

Họp rút kinh nghiệm trong [● 10] ngày làm việc; cập nhật biện pháp bảo vệ; cập nhật hồ sơ đánh giá tác động nếu cần; theo dõi hành động khắc phục đến khi đóng.
