# Driving Safety Website

静态官网：行车记录仪与行车安全应用。

- 入口：`index.html`
- 相对路径链接，适合 GitHub Pages 子路径
- 页脚社交：抖音/微博/哔哩哔哩/小红书

## 无命令行部署到 GitHub Pages
1. 在 GitHub 新建仓库（例如 `driving-safety-site`）。
2. 打开仓库 → Add file → Upload files，把整个 `web` 文件夹内的所有文件（包含 `.nojekyll`）拖拽上传到仓库根目录并提交。
3. 仓库 → Settings → Pages：
   - Source 选择 “Deploy from a branch”
   - Branch 选择 `main`、Folder 选择 `/ (root)`，保存
4. 等待 1–3 分钟，访问 `https://<你的用户名>.github.io/driving-safety-site/`。

如需自定义域名，按 Pages 设置中的指引添加 `CNAME`。

