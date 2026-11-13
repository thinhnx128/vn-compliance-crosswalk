# Bộ công cụ bảo vệ dữ liệu cá nhân cho doanh nghiệp vừa và nhỏ

Bộ mẫu biểu và công cụ tiếng Việt, miễn phí, giúp doanh nghiệp **tự** rà soát và triển khai tuân thủ
Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Nghị định 356/2025/NĐ-CP (cùng có hiệu lực từ 01/01/2026).

> Mẫu tham khảo, là diễn giải chuyên môn của tác giả, **không phải tư vấn pháp lý**. Căn cứ theo bản đăng
> Công báo, đối chiếu ngày **13/11/2026**. Văn bản có thể được sửa đổi hoặc có hướng dẫn mới sau ngày này;
> hãy kiểm tra văn bản đang có hiệu lực trước khi dùng.

## Dùng ngay

| Công cụ | Dùng để | Truy cập |
|---|---|---|
| **Kiểm tra nhanh 10 câu** | Biết sơ bộ doanh nghiệp đang ở đâu trong 3 phút. Chạy trên trình duyệt, không gửi dữ liệu đi đâu | [Mở trang](https://thinhnx128.github.io/vn-compliance-crosswalk/kiem-tra-nhanh/) |
| **Bộ công cụ đầy đủ (Word, Excel)** | 2 sổ Excel và 10 tài liệu Word, tải về dùng ngay | [Bản phát hành mới nhất](https://github.com/thinhnx128/vn-compliance-crosswalk/releases/latest) |

## Bộ đầy đủ gồm gì

| File | Nội dung |
|---|---|
| `CHK-DP` Bộ tự kiểm tra (Excel) | Sheet **Sàng lọc**: 4 câu để biết doanh nghiệp có được miễn một số nghĩa vụ theo quy mô không (Luật Điều 38). Sheet **Tự kiểm tra**: 22 câu, mỗi câu có căn cứ điều, khoản và ghi rõ là luật định hay thực tiễn tốt. Sheet **Kết quả**: tự tính điểm theo 10 nhóm |
| `REG-DP` Sổ bảo vệ dữ liệu cá nhân (Excel) | Hoạt động xử lý; bên xử lý và chuyển xuyên biên giới; yêu cầu của chủ thể (hạn phản hồi 02 ngày làm việc và hạn thực hiện tự tính theo loại yêu cầu); vi phạm (hạn 72 giờ tự tính) |
| `DP-00` | Mẫu báo cáo chẩn đoán mức sẵn sàng |
| `DP-01` | Chính sách bảo vệ dữ liệu cá nhân |
| `DP-02` | Thông báo về xử lý dữ liệu cá nhân |
| `DP-03` | Đánh giá tác động xử lý và chuyển dữ liệu xuyên biên giới |
| `DP-04` | Quy trình giải quyết yêu cầu của chủ thể dữ liệu |
| `DP-05` | Quy trình xử lý vi phạm |
| `DP-06` | Mẫu thỏa thuận xử lý dữ liệu với bên xử lý |
| `DP-07` | Mẫu đồng ý và rút lại đồng ý |
| `SP-01`, `SP-02` | Hướng dẫn sử dụng; giấy phép và lưu ý |

## Những điểm doanh nghiệp nhỏ hay bỏ sót

- **Miễn trừ theo quy mô** (Luật Điều 38; NĐ 356 Điều 41): doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được chọn
  không lập hồ sơ đánh giá tác động và không chỉ định nhân sự bảo vệ dữ liệu trong 05 năm kể từ 01/01/2026; hộ
  kinh doanh, doanh nghiệp siêu nhỏ không phải thực hiện. **Không được miễn** nếu kinh doanh dịch vụ xử lý dữ
  liệu cá nhân, trực tiếp xử lý dữ liệu nhạy cảm, hoặc đã xử lý tích lũy từ 100 nghìn chủ thể trở lên. Các nghĩa
  vụ khác vẫn áp dụng.
- **Thời hạn trả lời chủ thể dữ liệu không phải một con số** (NĐ 356 Điều 5): phản hồi trong 02 ngày làm việc;
  thực hiện trong 10 ngày (xem, chỉnh sửa, cung cấp), 15 ngày (rút lại đồng ý, hạn chế, phản đối) hoặc 20 ngày
  (xóa); dài hơn khi cần bên xử lý, bên thứ ba.
- **Thông báo vi phạm** (Luật Điều 23): chậm nhất 72 giờ kể từ khi phát hiện, với vi phạm có thể gây tổn hại
  theo khoản 1; phải lập biên bản xác nhận.
- **Hồ sơ đánh giá tác động** (Luật Điều 21): gửi trong 60 ngày kể từ ngày đầu tiên xử lý.
- **Dùng dịch vụ đám mây của nhà cung cấp nước ngoài là chuyển dữ liệu xuyên biên giới** (NĐ 356 Điều 17), trừ
  các trường hợp được miễn, ví dụ lưu dữ liệu người lao động của chính tổ chức (Luật Điều 20 khoản 6).

## Mã nguồn của mẫu

- `mau/*.md`: nội dung các tài liệu ở dạng Markdown. `{{TEN_BIEN}}` là thông tin của tổ chức, `[● ...]` là chỗ
  người dùng tự điền.
- `cau-hoi.json`: 22 câu kiểm tra kèm căn cứ, dùng chung cho bộ tự kiểm tra và mẫu báo cáo.

Các file Word, Excel trong bản phát hành được sinh từ những nguồn này. Trình sinh tài liệu sẽ được công bố ở
một đợt sau.

## Góp ý, báo lỗi

Thấy chỗ sai, chỗ lỗi thời, hoặc cần một mẫu chưa có: mở [issue](https://github.com/thinhnx128/vn-compliance-crosswalk/issues).
Đặc biệt hoan nghênh phản hồi từ doanh nghiệp đã dùng thử: dùng được không, vướng ở đâu.

## Giấy phép

Nội dung trong `toolkits/` và các file phát hành kèm: [CC BY 4.0](../../LICENSE-DATA). Được dùng, sửa, chia sẻ cho
mọi mục đích, chỉ cần ghi nguồn.
