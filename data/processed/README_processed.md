# README_processed

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra dữ liệu hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.

## Nhiệm Vụ Của Thư Mục

Thư mục `data/processed` chứa các file JSON đã được tách theo từng bảng từ file dữ liệu gốc.

Các file này là kết quả hiện tại của `ingestion/load_data.py`.

## Các File Hiện Có

### `README_processed.md`

File này mô tả nhiệm vụ của thư mục `data/processed` và nhiệm vụ hiện tại của từng file JSON đã xử lý trong thư mục.

### `architectureTypes.json`

File này có 15 bản ghi.

Các field quan sát được:

- `id`
- `name`
- `slug`
- `description`
- `imageUrl`
- `order`
- `isActive`
- `seoTitle`
- `seoDescription`
- `imageAlt`
- `createdAt`
- `updatedAt`

File này đang được đọc bởi `ingestion/chunking/architectureTypes.py`.

### `companyInfo.json`

File này có 1 bản ghi.

Các field quan sát được:

- `companyName`
- `companySlogan`
- `companyDescription`
- `hotlines`
- `emails`
- `mainAddress`
- `secondaryAddress`
- `workingHours`
- `website`
- `socialLinks`
- `totalEmployees`
- `totalEngineers`
- `totalArchitects`
- `totalProjects`
- `thumbnailUrl`
- `thumbnailAlt`
- `thumbnailTitle`
- `seoTitle`
- `seoDescription`
- `structuredData`
- `createdAt`
- `updatedAt`

### `heroSlides.json`

File này có 10 bản ghi.

Các field quan sát được:

- `id`
- `title`
- `subtitle`
- `description`
- `imageUrl`
- `videoUrl`
- `page`
- `order`
- `isActive`
- `imageAlt`
- `videoTitle`
- `createdAt`
- `updatedAt`

### `interiorStyles.json`

File này có 10 bản ghi.

Các field quan sát được:

- `id`
- `name`
- `slug`
- `description`
- `imageUrl`
- `order`
- `isActive`
- `seoTitle`
- `seoDescription`
- `imageAlt`
- `createdAt`
- `updatedAt`

### `news.json`

File này có 17 bản ghi.

Các field quan sát được:

- `id`
- `title`
- `slug`
- `excerpt`
- `content`
- `author`
- `categoryId`
- `category`
- `projectId`
- `status`
- `isFeatured`
- `publishedAt`
- `readingTime`
- `viewCount`
- `thumbnailUrl`
- `thumbnailAlt`
- `seoTitle`
- `seoDescription`
- `structuredData`
- `createdAt`
- `updatedAt`

### `newsCategories.json`

File này có 4 bản ghi.

Các field quan sát được:

- `id`
- `name`
- `slug`
- `description`
- `order`
- `isActive`
- `seoTitle`
- `seoDescription`
- `createdAt`
- `updatedAt`

### `projectCategories.json`

File này có 12 bản ghi.

Các field quan sát được:

- `id`
- `name`
- `slug`
- `description`
- `icon`
- `order`
- `isActive`
- `seoTitle`
- `seoDescription`
- `createdAt`
- `updatedAt`

### `projects.json`

File này có 49 bản ghi.

Các field quan sát được:

- `id`
- `title`
- `slug`
- `description`
- `content`
- `categoryId`
- `category`
- `architectureTypeId`
- `architectureType`
- `interiorStyleId`
- `interiorStyle`
- `investor`
- `location`
- `area`
- `completedDate`
- `status`
- `isFeatured`
- `publishedAt`
- `viewCount`
- `thumbnailUrl`
- `thumbnailAlt`
- `seoTitle`
- `seoDescription`
- `structuredData`
- `createdAt`
- `updatedAt`

## Cách Hoạt Động Hiện Tại

Các file trong thư mục này được tạo bởi `ingestion/load_data.py`.

Khi chạy, mã nguồn đọc file JSON gốc, duyệt qua các bảng trong object `tables`, bỏ qua bảng rỗng và ghi bảng có dữ liệu ra file JSON riêng.

JSON được ghi với:

- `ensure_ascii=False`
- `indent=4`
- `encoding="utf-8"`

## Ghi Chú Kỹ Thuật

Đây là thư mục chứa dữ liệu sinh ra sau bước xử lý, không chứa mã nguồn Python.

Tính tới thời điểm hiện tại, chỉ `architectureTypes.json` đã có file chunking tương ứng trong mã nguồn.
