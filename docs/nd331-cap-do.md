# Tóm tắt tiêu chí xác định cấp độ HTTT theo Nghị định 331/2026/NĐ-CP

> Tóm tắt do tác giả tự diễn đạt từ Điều 8, 9 và 11–15 của Nghị định 331/2026/NĐ-CP ngày 19/8/2026,
> đối chiếu ngày 31/10/2026. Chỉ để tham khảo; việc xác định cấp độ phải căn cứ văn bản gốc, kết quả
> đánh giá rủi ro (Điều 10) và hướng dẫn của Bộ Công an.

## Nguyên tắc (Điều 8)

- Mỗi hệ thống thông tin chỉ có một chủ quản.
- Hệ thống đáp ứng tiêu chí của nhiều cấp độ thì lấy cấp độ cao nhất.
- Không được chia tách hay hợp nhất hệ thống một cách hình thức để hạ cấp độ.

## Phân loại đầu vào (Điều 9)

- **Loại thông tin:** công cộng; riêng; cá nhân; bí mật nhà nước (Mật, Tối mật, Tuyệt mật).
- **Loại hệ thống theo chức năng:** phục vụ nội bộ; phục vụ người dân, doanh nghiệp; cơ sở hạ tầng
  thông tin; điều khiển công nghiệp; hệ thống khác phục vụ nghiệp vụ chuyên ngành.

## Tiêu chí theo cấp độ (đáp ứng một trong các tiêu chí)

| Cấp độ | Tiêu chí chính |
|---|---|
| 1 (Điều 11) | Hệ thống nội bộ chỉ xử lý thông tin công cộng |
| 2 (Điều 12) | Hệ thống nội bộ xử lý thông tin riêng hoặc thông tin cá nhân (không có bí mật nhà nước); dịch vụ trực tuyến không thuộc ngành nghề kinh doanh có điều kiện; dịch vụ trực tuyến khác xử lý dữ liệu cá nhân dưới 100.000 chủ thể (cơ bản) hoặc dưới 10.000 chủ thể (nhạy cảm); hạ tầng thông tin phục vụ một cơ quan, tổ chức |
| 3 (Điều 13) | Xử lý bí mật nhà nước hoặc hệ thống quốc phòng, an ninh mà bị phá hoại sẽ tổn hại an ninh quốc gia; dịch vụ trực tuyến thuộc ngành nghề kinh doanh có điều kiện; hệ thống giải quyết thủ tục hành chính; dịch vụ trực tuyến xử lý dữ liệu cá nhân từ 100.000 chủ thể (cơ bản) hoặc từ 10.000 chủ thể (nhạy cảm); hạ tầng phục vụ một bộ, ngành, tỉnh hoặc một số tỉnh; hệ thống điều khiển công nghiệp của công trình cấp II, III, IV |
| 4 (Điều 14) | Bí mật nhà nước hoặc quốc phòng, an ninh mà bị phá hoại sẽ tổn hại nghiêm trọng an ninh quốc gia; hệ thống quốc gia phục vụ Chính phủ điện tử hoặc hạ tầng toàn quốc vận hành 24/7; điều khiển công nghiệp của công trình cấp I |
| 5 (Điều 15) | Hệ thống chiến lược về quốc phòng, an ninh mà bị phá hoại sẽ tổn hại đặc biệt nghiêm trọng; lưu trữ tập trung dữ liệu đặc biệt quan trọng của quốc gia; hạ tầng quốc gia kết nối quốc tế; điều khiển công nghiệp của công trình cấp đặc biệt hoặc liên quan an ninh quốc gia |

Mỗi cấp độ còn có tiêu chí "hệ thống khác do Thủ tướng quyết định hoặc được đánh giá theo Khung quản
lý rủi ro an ninh mạng".

## Thẩm quyền thẩm định, phê duyệt (Điều 18, 20)

| Cấp độ | Thẩm định | Phê duyệt |
|---|---|---|
| 1, 2 | Đơn vị chuyên trách về an ninh mạng | Đơn vị chuyên trách, báo cáo chủ quản |
| 3 | Đơn vị chuyên trách | Chủ quản |
| 4 | Bộ Công an chủ trì (Bộ Quốc phòng, Ban Cơ yếu với hệ thống chuyên ngành) | Chủ quản |
| 5 | Bộ Công an chủ trì | Thủ tướng phê duyệt Danh mục; chủ quản phê duyệt phương án |

Khi đơn vị chuyên trách đồng thời vận hành hệ thống, việc thẩm định giao cho đơn vị trực thuộc khác
hoặc Hội đồng thẩm định độc lập (Điều 18 khoản 4).

## Dùng với công cụ

```bash
vncc init nd331-2026 --level 2 -o hoso-cap-do-2.yaml   # chỉ sinh yêu cầu áp dụng cho cấp độ 2
vncc gap hoso-cap-do-2.yaml                              # báo cáo khoảng cách theo cấp độ trong hồ sơ
```
