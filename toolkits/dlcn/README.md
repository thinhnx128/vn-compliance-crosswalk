# Bộ công cụ bảo vệ dữ liệu cá nhân cho doanh nghiệp vừa và nhỏ

*Personal data protection toolkit for Vietnamese SMEs. [English version below](#english).*

Bộ mẫu biểu và công cụ tiếng Việt, miễn phí, mã nguồn mở, giúp doanh nghiệp **tự** rà soát và chuẩn bị hồ sơ theo
Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Nghị định 356/2025/NĐ-CP (cùng có hiệu lực từ 01/01/2026 theo
Điều 38 của Luật và Điều 42 của Nghị định).

> **Lưu ý.** Đây là mẫu tham khảo và là diễn giải chuyên môn của tác giả, **không phải tư vấn pháp lý**. Việc dùng
> bộ công cụ không bảo đảm doanh nghiệp đã tuân thủ. Căn cứ theo bản đăng Công báo, đối chiếu ngày
> **13/11/2026**. Văn bản có thể được sửa đổi hoặc có hướng dẫn mới sau ngày này; hãy kiểm tra văn bản đang có
> hiệu lực trước khi dùng.

## Bắt đầu

| Công cụ | Mục đích | Truy cập |
|---|---|---|
| **Kiểm tra nhanh 10 câu** | Hình dung ban đầu về mức sẵn sàng. Kết quả tính ngay trên trình duyệt; trang không gửi câu trả lời về máy chủ nào | [Mở trang](https://thinhnx128.github.io/vn-compliance-crosswalk/kiem-tra-nhanh/) |
| **Bộ công cụ đầy đủ** | 2 sổ Excel và 10 tài liệu Word, sửa được | [Tải gói zip](https://github.com/thinhnx128/vn-compliance-crosswalk/raw/main/toolkits/dlcn/phat-hanh/bo-cong-cu-bao-ve-du-lieu-ca-nhan.zip) |

Gói zip nằm trong kho tại [`phat-hanh/`](phat-hanh/) và được đính kèm vào các
[bản phát hành](https://github.com/thinhnx128/vn-compliance-crosswalk/releases) từ v0.5.1 (bản v0.5.0 không có
gói này). Mã băm SHA-256 của gói, cũng ghi ở `phat-hanh/SHA256SUMS`:
`770bc24a0de64ce86d8e4ee80c0b151a6d008b8586b686e4bf4b6a283d8a1fba`

## Thành phần

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

## Năm điểm doanh nghiệp nhỏ hay bỏ sót

1. **Miễn trừ theo quy mô** (Luật Điều 38 khoản 2, 3; NĐ 356 Điều 41). Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp
   được quyền chọn thực hiện hoặc không thực hiện Điều 21, 22 (hồ sơ đánh giá tác động và việc cập nhật) và
   khoản 2 Điều 33 (chỉ định bộ phận, nhân sự bảo vệ dữ liệu cá nhân) trong 05 năm kể từ 01/01/2026; hộ kinh
   doanh, doanh nghiệp siêu nhỏ không phải thực hiện các quy định đó. **Không áp dụng miễn trừ** với đơn vị kinh
   doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm, hoặc kể từ khi đạt quy mô từ
   100 nghìn chủ thể dữ liệu trở lên (tính trên tổng lượng dữ liệu cá nhân đã xử lý). Các nghĩa vụ khác của Luật
   vẫn áp dụng.
2. **Thời hạn trả lời chủ thể dữ liệu không phải một con số** (NĐ 356 Điều 5). Phản hồi trong 02 ngày làm việc;
   thực hiện trong 10 ngày (xem, chỉnh sửa, cung cấp), 15 ngày (rút lại đồng ý, hạn chế, phản đối) hoặc 20 ngày
   (xóa). Khi cần bên xử lý, bên thứ ba thực hiện thì có thời hạn riêng (15, 20 hoặc 30 ngày tùy trường hợp);
   yêu cầu phức tạp được gia hạn một lần và phải thông báo lý do. Bảng đầy đủ ở mẫu `DP-04`.
3. **Thông báo vi phạm** (Luật Điều 23). Không phải mọi sự cố đều phải thông báo trong 72 giờ. Thời hạn chậm nhất
   72 giờ kể từ khi phát hiện áp dụng với vi phạm có thể gây tổn hại nêu tại khoản 1. Bên kiểm soát phải lập biên
   bản xác nhận việc xảy ra vi phạm (khoản 2). Bên xử lý phát hiện vi phạm thì thông báo kịp thời cho bên kiểm soát.
4. **Hồ sơ đánh giá tác động** (Luật Điều 21). Bên kiểm soát, bên kiểm soát và xử lý dữ liệu lập, lưu hồ sơ và
   gửi 01 bản chính cho cơ quan chuyên trách trong 60 ngày kể từ ngày đầu tiên xử lý, trừ trường hợp được miễn.
5. **Dịch vụ đám mây của nhà cung cấp nước ngoài** (NĐ 356 Điều 17 khoản 1). Lưu dữ liệu trên dịch vụ này là một
   trường hợp chuyển dữ liệu xuyên biên giới. Một số trường hợp không phải lập hồ sơ đánh giá tác động chuyển
   dữ liệu xuyên biên giới, ví dụ lưu dữ liệu người lao động của chính tổ chức trên dịch vụ đám mây (Luật Điều 20
   khoản 6); hoạt động đó vẫn là chuyển dữ liệu xuyên biên giới.

## Mã nguồn của mẫu

- `mau/*.md`: nội dung các tài liệu ở dạng Markdown. `{{TEN_BIEN}}` là thông tin của tổ chức, `[● ...]` là chỗ
  người dùng tự điền.
- `cau-hoi.json`: 22 câu kiểm tra kèm căn cứ, dùng chung cho bộ tự kiểm tra và mẫu báo cáo.

Các file Word, Excel trong gói zip được sinh từ những nguồn này. Trình sinh tài liệu sẽ được công bố ở một đợt sau.

## Cần hỗ trợ?

Tổ chức đang áp dụng và cần hỗ trợ (cách dùng, chỉnh mẫu, mẫu còn thiếu): mở issue theo mẫu
[**Yêu cầu hỗ trợ**](https://github.com/thinhnx128/vn-compliance-crosswalk/issues/new/choose) hoặc hỏi ở
[Discussions](https://github.com/thinhnx128/vn-compliance-crosswalk/discussions). Hỗ trợ miễn phí, trong khả năng
thời gian của tác giả. Issue và Discussions là công khai: đừng đưa dữ liệu thật hay thông tin nội bộ lên đó.
Nội dung không phù hợp để đăng công khai: me@nguyenxuanthinh.com (email không phải kênh bảo mật; chỉ gửi thông tin tối
thiểu, chưa gửi dữ liệu thật khi hai bên chưa thống nhất cách xử lý).

## Góp ý, báo lỗi

Nếu thấy chỗ sai hoặc chỗ đã lỗi thời, xin mở
[issue](https://github.com/thinhnx128/vn-compliance-crosswalk/issues/new/choose) theo mẫu **Báo lỗi, góp ý**. Phản hồi từ doanh nghiệp đã dùng thử
(dùng được không, vướng ở đâu) đặc biệt có giá trị với dự án.

## Giấy phép

Nội dung trong `toolkits/` và các file phát hành kèm: [CC BY 4.0](../../LICENSE-DATA). Được dùng, sửa, chia sẻ cho
mọi mục đích, chỉ cần ghi nguồn.

---

## English

**Personal data protection toolkit for small and medium-sized enterprises in Vietnam.** A free, open-source set of Vietnamese-language templates and tools that helps organisations review their own
practices and prepare documentation under Vietnam's Law on Personal Data Protection No. 91/2025/QH15 and
Decree No. 356/2025/ND-CP (both in force from 1 January 2026, per Article 38 of the Law and Article 42 of the
Decree). The templates and the quick check are in Vietnamese; this section summarises them for English readers.

> **Notice.** These are reference templates reflecting the author's professional interpretation. They are
> **not legal advice**, and using the toolkit does not guarantee compliance. References follow the texts published
> in the Official Gazette, checked on **13 November 2026**. The texts may be amended or supplemented by new
> guidance after that date; verify the provisions currently in force before relying on them. Where this summary
> and the Vietnamese section differ, the Vietnamese section prevails.

### Getting started

| Tool | Purpose | Access |
|---|---|---|
| **10-question quick check** | A first view of readiness. The result is calculated in the browser; the page sends no answers to any server | [Open](https://thinhnx128.github.io/vn-compliance-crosswalk/kiem-tra-nhanh/) |
| **Full toolkit** | 2 Excel workbooks and 10 editable Word documents | [Download zip](https://github.com/thinhnx128/vn-compliance-crosswalk/raw/main/toolkits/dlcn/phat-hanh/bo-cong-cu-bao-ve-du-lieu-ca-nhan.zip) |

The zip is stored in the repository under [`phat-hanh/`](phat-hanh/) and attached to every
[release](https://github.com/thinhnx128/vn-compliance-crosswalk/releases) from v0.5.1 onwards (v0.5.0 does not
include it). Its SHA-256 checksum is given above and in `phat-hanh/SHA256SUMS`.

### Contents

| File | Content |
|---|---|
| `CHK-DP` Self-assessment (Excel) | **Screening** sheet: 4 questions on whether size-based exemptions apply (Law, Article 38). **Self-assessment** sheet: 22 questions, each citing its article and clause and marked as a legal requirement or good practice. **Results** sheet: automatic scoring across 10 groups |
| `REG-DP` Personal data protection register (Excel) | Processing activities; processors and cross-border transfers; data subject requests (2-working-day response deadline and fulfilment deadline calculated by request type); breaches (72-hour deadline calculated) |
| `DP-00` | Readiness assessment report template |
| `DP-01` | Personal data protection policy |
| `DP-02` | Personal data processing notice |
| `DP-03` | Impact assessment for processing and for cross-border transfer |
| `DP-04` | Procedure for handling data subject requests |
| `DP-05` | Breach handling procedure |
| `DP-06` | Data processing agreement template |
| `DP-07` | Consent and withdrawal-of-consent form |
| `SP-01`, `SP-02` | User guide; licence and notices |

### Five points small businesses often miss

1. **Size-based exemptions** (Law, Article 38(2)–(3); Decree 356, Article 41). Small enterprises and startups may
   choose whether to apply Articles 21 and 22 (impact assessment dossier and its updates) and Article 33(2)
   (designating a personal data protection unit or officer) for 5 years from 1 January 2026; household businesses
   and micro-enterprises are not required to apply them. **The exemption does not apply** to entities that provide
   personal data processing services, directly process sensitive personal data, or have reached 100,000 data
   subjects or more (based on the cumulative total of personal data processed). All other obligations under the Law
   still apply.
2. **There is no single deadline for data subject requests** (Decree 356, Article 5). Respond within 2 working
   days; fulfil within 10 days (access, rectification, provision), 15 days (withdrawal of consent, restriction,
   objection) or 20 days (erasure). Separate deadlines apply when a processor or third party must act (15, 20 or
   30 days depending on the case); complex requests may be extended once, with reasons notified. The full table
   is in template `DP-04`.
3. **Breach notification** (Law, Article 23). Not every incident must be notified within 72 hours. The deadline
   of no later than 72 hours from discovery applies to breaches likely to cause the harm described in
   paragraph 1. The controller must make a written record confirming the breach (paragraph 2). A processor that
   discovers a breach must promptly notify the controller.
4. **Impact assessment dossier** (Law, Article 21). A controller or a controller-processor prepares and keeps
   the dossier and sends one original to the specialised personal data protection authority within 60 days
   from the first day of processing, unless exempt.
5. **Cloud services of foreign providers** (Decree 356, Article 17(1)). Storing data on such a service is a case
   of cross-border data transfer. Some cases do not require a cross-border transfer impact assessment, for
   example an organisation storing its own employees' data on a cloud service (Law, Article 20(6)); the activity
   remains a cross-border transfer.

### Template sources

- `mau/*.md`: document content in Markdown. `{{TEN_BIEN}}` marks organisation details; `[● ...]` marks fields the
  user fills in.
- `cau-hoi.json`: the 22 assessment questions with their legal references, shared by the self-assessment and the
  report template.

The Word and Excel files in the zip are generated from these sources. The document generator will be published
in a later release.

### Need help?

If your organisation is applying the toolkit and needs help (usage, adapting a template, a missing template),
open a
[**Support request**](https://github.com/thinhnx128/vn-compliance-crosswalk/issues/new/choose) or ask in
[Discussions](https://github.com/thinhnx128/vn-compliance-crosswalk/discussions). Support is free and best-effort.
Issues and Discussions are public: do not post real data or internal information. For matters unsuitable for
public posting: me@nguyenxuanthinh.com (email is not a secure channel; send only the minimum, and no real data before
we have agreed how to handle it).

### Feedback

If you find an error or an outdated reference, please open an
[issue](https://github.com/thinhnx128/vn-compliance-crosswalk/issues/new/choose) using the **Error report, feedback** form. Feedback from organisations that have
tried the toolkit is especially valuable.

### Licence

Content under `toolkits/` and the accompanying release files: [CC BY 4.0](../../LICENSE-DATA). You may use,
adapt and share it for any purpose, with attribution.
