# 澳門即時天氣

此網站顯示澳門氣象局的天氣簡報、紫外線及一般性空氣質量預報。GitHub
Actions 每小時第 2 分鐘讀取官方 XML 並部署更新，避免瀏覽器跨網域限制。

## 部署到 GitHub Pages

1. 在 GitHub repository 的 **Settings → Pages → Build and deployment** 中，將
   **Source** 設為 **GitHub Actions**。
2. 推送到 `main` 分支，或在 **Actions → Deploy GitHub Pages** 手動執行工作流程。
3. 部署完成後，在 Pages 設定頁開啟網站網址。

工作流程亦會每小時第 25 分鐘更新天氣資料。首次推送或手動執行即可觸發首次部署。
