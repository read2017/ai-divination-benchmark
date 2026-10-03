<div align="center">

# AI 命运工具公开测评

<p align="center">
  <img src="assets/hero.gif" alt="12 款开源命理工具 · 24 个普通人 · 46 件人生大事 的测评流程" width="100%"/>
</p>

> *12 款开源命理工具、16 种配置、24 个普通人的 46 件人生大事：工具组第一名，没有超过「四句好话」对照。*

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)
![scoring offline reproducible](https://img.shields.io/badge/scoring-offline%20reproducible-b34c2f)
![type retrospective backtest](https://img.shields.io/badge/type-retrospective%20backtest-6b7772)
[![Stars](https://img.shields.io/github/stars/read2017/ai-divination-benchmark?style=social)](https://github.com/read2017/ai-divination-benchmark/stargazers)

<br>

**藏起 24 个普通人的真实经历，只给出生资料和一段三年窗口，让 12 款开源命理工具自己判断事业、感情、学业、钱财会怎么变，再逐条对照公开记录。原始回答、评分规则、对照组和全部方法边界都在仓库里，评分不联网即可复算。**

<sub>八字 · 紫微斗数 · 印度占星 · 奇门 · 六爻 · 塔罗 ｜ 中文 ｜ 同一模型 gpt-6-luna</sub>

<br>

[从哪里开始](#从哪里开始) · [关键成绩](#关键成绩) · [被测项目](#被测项目) · [怎么测](#怎么测) · [复核成绩](#复核成绩) · [必须一起看的边界](#必须一起看的边界) · [目录与授权](#目录与授权) · [展示网页](docs/index.html)

<br>

</div>

---

这是一份探索性回测，不是未来准确率证明。24个普通人的公开案例、46件选定人生大事；统一使用 `gpt-6-luna` 解读。覆盖八字、紫微斗数、印度占星，以及模拟奇门、六爻、塔罗。本仓库发布测评结果、评分方法和已有回答，不提供付费占卜服务。

## 从哪里开始

- [通俗测评报告](reports/publication/人生变化命理测评-v6.md)：完整榜单、GitHub原链接及事业／感情／学业／钱财分项。
- [录屏展示网页](docs/index.html)：下载仓库后用浏览器打开；F全屏、R简洁模式、上下方向键切换章节。GitHub文件页只显示源代码，在线展示可手动配置Pages，见[发布说明](PUBLICATION.md)。
- [证据附件](reports/publication/人生变化命理测评-v6-证据附件.md)和[逐题明细CSV](reports/publication/人生变化测评-逐题明细.csv)。
- 口播稿与自媒体成稿留在本地，不随仓库发布；本仓库只放可复核的测评材料。

## 关键成绩

| 配置 | 准确分 /85 | 最终分 /100 | 同类大事命中 /46 | 方向说反 |
|---|---:|---:|---:|---:|
| 雪眠八字（出生资料组第一） | 10.61 | 16.74 | 4 | 4次 |
| 金辰八字 | 9.94 | 16.00 | 4 | 5次 |
| 命理大师 | 6.36 | 11.69 | 2 | 5次 |
| “全说好事”固定规则（对照，非Skill） | 32.05 | 40.26 | 19 | 9次 |

排名按准确分，最终分包含具体性、错输入对照、可观察易用性。类别命中不等于年份完全准确；未命中不全是猜错，也包括遗漏和未作答。普通AI对照没有给判断，零分不能用来证明命理工具有效。完整16项配置和两项对照见报告。

## 被测项目

本轮读取并实测了 12 个开源仓库、16 种配置。按体系分组，链接指向本轮实际读取的仓库（不是推荐，也不代表合作关系）：

**八字 BaZi**（6）
[雪眠八字 xuemian168/bazi-skill](https://github.com/xuemian168/bazi-skill) ·
[金辰八字 jinchenma94/bazi-skill](https://github.com/jinchenma94/bazi-skill) ·
[高鑫八字 gaoxin492/bazi-skill](https://github.com/gaoxin492/bazi-skill) ·
[Suangua Sudo-Biao/suangua](https://github.com/Sudo-Biao/suangua) ·
[命语 Brhiza/mingyu](https://github.com/Brhiza/mingyu) ·
[Horosa Horace-Maxwell/horosa-skill](https://github.com/Horace-Maxwell/horosa-skill)

**紫微斗数 Zi Wei Dou Shu**（2）
[Wolke/ziwei-doushu](https://github.com/Wolke/ziwei-doushu) ·
[命理大师 learnwithu/mingli-master](https://github.com/learnwithu/mingli-master)

**八字＋紫微 BaZi + Zi Wei**（1）
[AdrianBOM/bazi-ziwei-skill](https://github.com/AdrianBOM/bazi-ziwei-skill)

**印度占星 Vedic Astrology**（1）
[CNWU16/vedic-astro-skills](https://github.com/CNWU16/vedic-astro-skills)

**多体系：八字／紫微／奇门遁甲／六爻／塔罗**（1）
[太卜 hhszzzz/taibu](https://github.com/hhszzzz/taibu) —— 八字、紫微、奇门、六爻、塔罗各列一行单独计分

**塔罗 Tarot**（1）
[daman-ovo-0404/tarot-skill](https://github.com/daman-ovo-0404/tarot-skill)

对照组不是项目：**全说好事**（固定规则）、**普通 AI**（不加载任何 Skill）、**错生日**（把出生资料换成另一个人的）。未覆盖手相、风水、合婚，以及六爻、奇门的真实问事预测。

## 怎么测

隐藏姓名与经历，给出生资料及三年窗口；结果交出后对照公开来源。评分关注事情、方向、时间、套话、错输入和交付体验。问事组使用固定时刻／随机条件模拟咨询，单独列榜。

- [冻结评分规则](runs/v6-consumer-events/protocol.md)
- [预测指令](runs/v6-consumer-events/predictor-instructions.md)
- [原始回答](runs/v6-consumer-events/answers/)、[错输入对照](runs/v6-consumer-events/controls/)、[体验探针](runs/v6-consumer-events/probes/)
- [24题来源与目标](datasets/gold/v6-events.jsonl)、[输入](runs/v6-consumer-events/inputs/)
- [实际项目版本](runs/v6-consumer-events/metadata/source-versions.json)、[文字资格裁定](runs/v6-consumer-events/adjudications.json)
- [机器成绩](reports/v6-consumer-scores.json)

## 复核成绩

只需要Python 3.10或以上，评分不联网，不需要API密钥，也不需要安装被测Skill。

```bash
python3 scripts/verify_release.py
python3 scripts/reproduce_scores.py
```

第二条在临时目录复算，不覆盖已发布成绩，比较完整JSON与逐题CSV。此处可复现的是“给定原答的评分”，不是重新生成模型回答：没有附一键调用模型、安装所有排盘依赖的运行器。大型原生排盘文件、依赖和下载的第三方仓库留在本地；相应模式限制与纠错记录见证据附件。

## 必须一起看的边界

- 公开来源包含网站口述整理、作者命例转述和论坛自述，未独立核实；部分出生盘可能按经历校时。
- 三年窗口按已知事件与领域覆盖选择，不能估算一般人群未来预测能力。
- 隔离依赖指令，不是权限强制双盲；模型训练记忆风险无法排除。一次问事预测曾误查旧报告，已作废并重新生成，见证据附件。
- 全部是“Skill＋同一个Luna模型”的组合表现；换模型可能换名次。
- 错输入仅5个婚恋案例；易用性无真人满意度调查；文字裁定无独立人工评审。
- 出生资料用匿名编号，但出生时间和来源仍可关联原公开案例，不应把它们称为彻底匿名数据，禁止尝试重新识别当事人。

## 目录与授权

`docs/` 展示网页；`reports/` 最新报告及成绩；`datasets/` 选定目标；`runs/` v6回答与规则；`harness/` 原始评分程序；`scripts/` 复核入口；`provenance/` 公开文件散列。

本仓库没有为作者原创内容擅自设置开源授权。公开可读不等于任意再授权；第三方图片及案例材料的权利归原作者，详见[第三方声明](THIRD_PARTY_NOTICES.md)。

## 关于作者

这份测评和配套的口播内容发在「**沉思哲｜AI产品研发**」。

- 邮箱：read2016@qq.com
- 抖音：108799524 ｜ 小红书：26262268555

<!-- 二维码占位：把自己的抖音/小红书二维码分别存成 assets/douyin-qrcode.png 与 assets/xiaohongshu-qrcode.png，然后放开下面这段
<table><tr>
<td align="center"><img src="assets/douyin-qrcode.png" width="220"/><br><sub>抖音</sub></td>
<td align="center"><img src="assets/xiaohongshu-qrcode.png" width="220"/><br><sub>小红书</sub></td>
</tr></table>
-->

## 支持这个项目

如果这份测评对你有用，**[点个 Star](https://github.com/read2017/ai-divination-benchmark/stargazers) 让我知道这类实测值得继续做**；[点 Watch](https://github.com/read2017/ai-divination-benchmark/subscription) 会在有更新时收到通知。
