# Python File Server

這是一個簡單的 Python 文件伺服器，使用 Flask 框架建立。它能讓你上傳文件，查看已上傳的文件列表，並下載指定的文件。

## 部屬

先確保系統已安裝 poetry

```
poetry install
poetry run python server.py
```

## 使用方式
### 上傳文件

- **URL**
    - `/`
- **方法**
    - `POST`
- **資料參數**
    - **必要參數：**
      `file=[binary]`
- **成功回應範例：**
    - **程式碼：** 200
      **內容：** `File uploaded successfully!`
- **錯誤回應範例：**
    - **程式碼：** 400 BAD REQUEST
      **內容：** `No file part in the request.`

### 獲取所有文件列表

- **URL**
    - `/files`
- **方法**
    - `GET`
- **成功回應範例：**
    - **程式碼：** 200
      **內容：** `["file1.txt", "file2.png"]`
- **錯誤回應：**
    - 本 API 不會返回錯誤

### 下載指定文件

- **URL**
    - `/files/<filename>`
- **方法**
    - `GET`
- **URL 參數**
    - **必要參數：**
      `filename=[string]`
- **成功回應：**
    - **程式碼：** 200
      **內容：** 文件的二進制資料
- **錯誤回應範例：**
    - **程式碼：** 404 NOT FOUND
      **內容：** `File not found`


