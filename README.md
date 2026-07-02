# 数据查询静态网站

这是一个单纯的静态网站托管项目，用 GitHub Pages 发布。站点不需要构建步骤，页面、样式、脚本和数据文件都会由 GitHub Actions 直接整理后发布到 Pages。

## 页面入口

- `index.html`：主页
- `size-charts.html`：浏览各店铺尺码表页面
- `size-chart.html`：按车型字段查询不同店铺的配对尺码
- `size-ref.html`：查询尺码参考数据

## 主要目录

```text
assets/
  fonts/                 字体文件

data/
  charts/                尺码表页面、站点 JS/CSS 和视图配置
    viewer.css
    viewer.js
    size-ref.js
    size-chart-view.yaml
    ALL/
    HNT/
    TM/
  generated/             从 Excel 导出的线上查询 JSON
  source/                Excel 源数据和车型尺寸数据

.github/workflows/
  static.yml             GitHub Pages 发布工作流
```

`bak/`、`.vscode/` 和本地辅助脚本不会被发布到 GitHub Pages。

## GitHub Pages 发布

发布工作流在 `.github/workflows/static.yml`。

触发方式：

- 推送到 `main` 分支时自动发布
- 也可以在 GitHub 仓库的 Actions 页面手动运行 `Deploy static site to Pages`

工作流会先读取 `data/source/车型数据尺码.xlsx`，按 `data/charts/size-chart-view.yaml` 里的工作表配置导出：

```text
data/generated/size-ref.json
data/generated/size-match.json
```

然后整理 `_site` 目录，只复制线上需要的内容：

```text
assets/
data/
index.html
size-chart.html
size-charts.html
size-ref.html
README.md
.nojekyll
```

然后使用 GitHub 官方 Pages Actions 上传并发布：

- `actions/configure-pages`
- `actions/upload-pages-artifact`
- `actions/deploy-pages`

仓库第一次启用时，需要在 GitHub 仓库设置里确认：

```text
Settings -> Pages -> Source -> GitHub Actions
```

## 更新数据或页面

常见更新位置：

- Excel 源数据：`data/source/车型数据尺码.xlsx`
- Excel 工作表配置：`data/charts/size-chart-view.yaml`
- 尺码表 HTML：`data/charts/<店铺>/<类型>/output_*.html`
- 尺码表样式：`data/charts/<店铺>/<类型>/size-chart.css`
- 尺码查询配置：`data/charts/size-chart-view.yaml`
- 页面入口目录配置：`size-charts.html` 和 `size-chart.html`

如果新增或删除 `output_*.html`，需要同步更新 `size-charts.html` 和 `size-chart.html` 里的 `directories` 列表。

尺码参考和尺码配对的数据源在 YAML 中指定：

```yaml
excel_source:
  path: data/source/车型数据尺码.xlsx
  match_data_path: data/generated/size-match.json
match_sources:
  - name: ALL
    sheet: ALL尺码匹配
  - name: TM
    sheet: TM尺码匹配
  - name: HNT
    sheet: HNT尺码匹配
size_reference:
  sheet: ALL尺码
  data_path: data/generated/size-ref.json
```

## 本地预览

在项目根目录启动一个静态服务器后访问主页即可：

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

然后打开：

```text
http://127.0.0.1:8765/
```

## 发布前检查

提交前建议确认这些文件路径都存在：

- `data/charts/viewer.css`
- `data/charts/viewer.js`
- `data/charts/size-ref.js`
- `data/source/车型数据尺码.xlsx`
- `data/generated/size-ref.json`
- `data/generated/size-match.json`
- `data/charts/TM/nonpick/output_001.html`
- `data/charts/TM/pick/output_001.html`
- `data/charts/HNT/nonpick/output_001.html`
- `data/charts/HNT/pick/output_001.html`
