# 主日29 · 耶稣基督真实地临在圣餐中

2026-10-31 · v1.0.0 · GTser

| 公开入口 | 链接 |
| --- | --- |
| GitHub Pages | https://08-ser-gt-je-personal-20261003.github.io/lord-day29-real-presence-20261031-v1-GTser/ |
| Surge | https://lord-day29-real-presence-20261031-v1-gtser.surge.sh/ |
| 新建源码仓库 | https://github.com/08-Ser-GT-Je-Personal-20261003/lord-day29-real-presence-20261031-v1-GTser |

## 内容

独立的欧陆改革宗讲章网站，按“真实临在的性质、真实临在的益处”两点展开。含路22:1–30完整读经、历史与逐段释经、四条神学脉络、16组详细讨论答案、互动临在图解、动态救赎脉络、原创地图与插图、本机朗读和复习自测。六份认信原典完整保留，三经另有干净阅读／背诵页面。原主日28项目未修改。

## 运行与维护

安装Python依赖：`python -m pip install -r requirements.txt`。

- 离线构建：`python build.py`，读取仓库原文与已核验记录。
- 在线重核：`python build.py --verify-live`。发现词句变化会停止，需人工审阅，不静默替换译文。
- 本地预览：`python -m http.server 4189 -d dist`。
- 内容核验：`python qa/verify.py`。
- 发布目录：`dist/`。GitHub Actions自动发布Pages；Surge可手动发布同目录。

正文源文件：`content.html`；讨论／自测／图解数据：`learning.json`；六份认信快照：`confessions.json`；读经：`scripture.json`。UI在`dist/style.css`与`dist/app.js`，SVG在`dist/assets/`。无需构建框架，无数据库，无运行时第三方依赖。不要提交账号、密码、令牌、.netrc或Surge生成的CNAME到仓库。

## 文本与证据

认信全部采用CCI指定中文原文，不混入其他译本。完整快照日期2026-10-17；三经、问47–48／78–79、比利时19／33／35、多特第五项14另在2026-10-31在线核验，见`dist/source-verification.json`。其余原典不宣称全部当日重抓。全库232条，包括CCI所收多特59条正面教义及4组驳谬，不从别版补结语。

历史推断与经文明言分开；地图是非比例示意，未虚构最后晚餐房址。诗歌按给定编号，未猜歌词曲名。“21篇1–3节”按上下文理解为韵诗编号，实际分节按当地诗本。朗读依赖设备可用中文声音，网站不自带预录音频。

检查报告见`qa/`；公开部署记录见`deployment.json`。原创讲解与图示由本项目编写；第三方译文权利归相应权利人，不对其附加原创授权。
