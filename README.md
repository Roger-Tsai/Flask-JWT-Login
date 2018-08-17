# Flask-JWT-Login

### 目標
透過 Flask 及其擴展來開發網頁後端登入功能，並以 JWT 來做驗證

### Flask 簡介 (Wikipedia 節錄)
Flask是一個使用Python編寫的輕量級Web應用框架，用extension增加其他功能。Flask並沒有預設使用的資料庫、表單驗證工具，而是利用Flask-extension加入這些功能：ORM、表單驗證工具、檔案上傳、各種開放式身分驗證技術。

### JWT (JSON Web Token)
簡單來說就是Json格式的 Web Token

可拆解成3個部份：
1. Header: 一個 Base64UrlEncode 過的 Json，包含 Hash 的演算法 (預設 HMAC SHA256)，以及 Token Type (JWT)
2. Payload: 一個 Base64UrlEncode 過的 Json，包含無機敏資料的個人資料(id, name 之類的)，以及 Token Expiration Time、Issuer等資訊。更詳細資訊可參考： https://tools.ietf.org/html/rfc7519#section-4.1
3. Signature: 簽名驗證

### 使用說明
- 本範例搭配的資料庫為 MySQL，因此用戶需先至 app/config.py 中將資料庫相關參數設定完畢，其他如 Host、Port 等參數也可一併在該處設定
- 設定完成後，執行: python run.py 即可
- 驗證 JWT 的部份在 app/auth/auths.py 中，並新增 Decorator login_required 

### API 說明
- 本範例使用 Blueprint 將 API 區分為各個模組
- 註冊：[POST] /user/register
- 登入：[POST] /user/login
- 取得用戶資料：[GET] /user/info

### 更新紀錄
## Version 1.0.0
- date： 2018-08-17
- desc： 撰寫以 JWT 為驗證基準的後台登入功能，支援註冊、登入、驗證等能力，未來再繼續擴充。
