# VPJ — Vĩnh Phúc Jobs

Website tìm việc responsive. Giao diện sử dụng Be Vietnam Pro tự lưu trong dự án, bảng màu xanh navy / xanh dương / cam, ảnh đại diện doanh nghiệp và thẻ tin dễ đọc.

## Mở trong VS Code
1. Giải nén và mở thư mục bằng File > Open Folder.
2. Cài extension Live Server.
3. Nhấn chuột phải dist/index.html > Open with Live Server.

Hoặc chạy `python -m http.server 5500 --directory dist`, rồi mở http://localhost:5500. Cần chạy qua HTTP để tải JSON; không mở trực tiếp file HTML bằng double-click.

## Dữ liệu
- Bản nhập công khai ngày 11/10/2026 từ https://vinhphuc.work/wp-json/wp/v2/posts.
- Đã đọc đủ 93 trang API và 9.212 bản ghi ở thời điểm nhập. Kiểm tra số lượng tại dist/data/import-status.json.
- Lưu tiêu đề, ngày đăng, liên kết nguồn, nhóm ngành/địa điểm lấy từ taxonomy, ảnh tại nguồn và thông tin công ty. Không nhập hồ sơ ứng viên, tài khoản hoặc dữ liệu riêng tư.
- Ảnh đại diện công ty lấy từ trang công ty cho nhóm tin gần đây; những tin khác dùng hình từ bài đăng hoặc avatar chữ khi không có ảnh.
- Lương và hạn tuyển chỉ hiển thị khi lấy được từ trang danh sách. Các trường chưa có được ghi “Xem tại nguồn”; không suy đoán lương hay yêu cầu.
- Toàn bộ nội dung mô tả, vị trí, quyền lợi và liên hệ ứng tuyển mở tại tin gốc. Chưa tự đồng bộ khi nguồn cập nhật.
- Mặc định xem tin đăng trong 60 ngày. Chọn “Toàn bộ kho tin” để tra cứu tin cũ. Ngày đăng không bảo đảm công ty còn tuyển.

## Bản nâng cấp VPJ 6
- Sửa lựa chọn địa điểm, nối lại bộ lọc để thay đổi lựa chọn thực sự cập nhật danh sách.
- 9.212 tin nguồn; 7.849 tin có tiêu đề vị trí tách được, 2.743 tin có số liệu lương, 5.060 tin có từ khóa kinh nghiệm. Việc tách tự động không bảo đảm đầy đủ; luôn kiểm tra bài gốc.
- 71 tệp chi tiết tải theo nhu cầu, chứa tên vị trí, công cụ/kỹ năng, trình độ, câu nêu lương và ảnh tại nguồn. Không sao chép toàn bộ bài gốc.
- Gợi ý vị trí/công ty khi tìm, lịch sử tìm kiếm, thẻ bộ lọc, hai cách xem tin, nhóm Có thông tin lương / Chưa qua hạn / Có ảnh công ty.
- Danh bạ toàn bộ công ty/nhóm tin với tìm kiếm, lọc khu vực, phân trang 24 đơn vị và hồ sơ công ty.
- Theo dõi công ty, tin gợi ý khớp tìm kiếm đã lưu qua chuông trong trang; không có email, SMS hoặc push.
- Theo dõi ứng tuyển, ghi chú, 5 trạng thái, xuất CSV; đây là nhật ký cá nhân, không tự gửi CV hay xác nhận trạng thái với doanh nghiệp.
- Tin vừa xem, chia sẻ liên kết mở đúng tin, gợi ý theo kỹ năng trong hồ sơ, 8 bài hướng dẫn và FAQ.
- Banner nổi, chuyển động nhẹ, hiệu ứng thẻ, hộp thoại và tải dữ liệu; hỗ trợ prefers-reduced-motion.

## Chức năng
Tìm tiếng Việt không dấu; lọc theo khu vực, ngành, thời gian, lương khi biết; sắp xếp; tải thêm mỗi lần 24 tin; lưu và so sánh; mở thông tin và ứng tuyển tại nguồn. Hồ sơ, CV PDF và tin tuyển dụng thử được lưu trên thiết bị.

Đăng nhập Google, Facebook, Zalo và số điện thoại hiện là giao diện thử nghiệm. Chưa có OAuth thật, SMS, máy chủ tài khoản hoặc gửi hồ sơ cho doanh nghiệp. Bản web có thể thêm vào màn hình chính; chưa có bản trên App Store/Google Play. Các doanh nghiệp hiển thị không mặc nhiên là đối tác của VPJ.

## Mã nguồn
- dist/index.html: bố cục và chức năng cơ bản.
- dist/app.css, fonts.css: stylesheet cuối cùng và font tiếng Việt.
- dist/pro.js, portal.js: hồ sơ, CV, nhà tuyển dụng và trang chủ.
- dist/real-data.js: dữ liệu nguồn, phân trang và ảnh đại diện.
- dist/experience.js, experience.css: trang chi tiết, khám phá, theo dõi, thông báo, công ty và hiệu ứng.
- dist/data/details/: các tệp thông tin vị trí, tải khi mở tin.
- dist/data/: bản dữ liệu công khai và thông tin lần nhập.
- dist/assets/: logo VPJ, font và ảnh doanh nghiệp.
- scripts/import_public_jobs.py, enrich_public_jobs.py: công cụ nhập dữ liệu công khai. Cần Python với lxml và Pillow. structure_job_content.py tách thông tin từ bộ nhớ đệm công khai sau khi nhập. Chạy import trước, enrich sau; các bước này ghi đè bản snapshot.

## Kiểm tra
Chạy `node checks/smoke.cjs` từ thư mục dự án. Kiểm tra số lượng bản ghi, ID duy nhất, tìm kiếm/lọc, phân trang giới hạn, lưu tin, liên kết nguồn và tài nguyên font. Đã kiểm tra đầy đủ bộ lọc, phân trang, danh bạ công ty, theo dõi, thông báo, khôi phục tìm kiếm, trạng thái ứng tuyển và chi tiết tin. Bộ kiểm tra này không thay thế kiểm tra hình ảnh giao diện trên trình duyệt.
