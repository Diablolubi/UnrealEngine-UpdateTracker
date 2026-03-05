# Unreal Engine 更新追踪器 (Unreal Engine Update Tracker)

[English version](README.en.md) | [日本語版](README.md)

本项目是一个自动化服务，定期监控 Unreal Engine 私有 GitHub 仓库的更新，使用 AI (Google Gemini) 总结重要变更（如新功能、规格变更），并将其作为报告发布到 GitHub Discussions。

<table><tr><td>
<img width="644" alt="image" src="https://github.com/pafuhana1213/Screenshot/blob/master/Report_sample_en.png" />
</td></tr></table>

注意：此图片为报告示例，所示内容完全为模拟数据。它并不代表 Unreal Engine 的实际更新。

## 🌟 主要功能

-   **自动更新检查：** 使用 GitHub Actions 按计划（每天 UTC 23:00 / 北京时间次日 07:00）或手动检查 UE 仓库中的最新提交。
-   **AI 驱动的总结：** Gemini API 分析提交内容，将其分类为“新功能”和“规格变更”等部分，并为每个部分提供摘要。
-   **发布到 Discussions：** 生成的报告将作为“Unreal Engine Daily Report”发布到仓库的 GitHub Discussions。
-   **Slack 通知：** 报告内容也可以同步发送到指定的 Slack 频道。
-   **Discord 通知：** 报告内容也可以同步发送到指定的 Discord 频道。

## 🚀 订阅最新报告

您可以直接订阅更新报告，而无需自己设置此工具。
在下面的仓库中，每天固定时间生成的报告会自动发布到 GitHub Discussions。

[**订阅 UnrealEngine-UpdateTrackerReport 仓库**](https://github.com/pafuhana1213/UnrealEngine-UpdateTrackerReport)

**注意：** 此报告仓库是私有的，需要拥有[访问 Unreal Engine 源码仓库权限的 GitHub 账号](https://www.unrealengine.com/zh-CN/ue-on-github)才能查看。

## ✨ 请考虑支持！

我希望这个工具能帮助您完成日常的 UE 信息获取。

此工具由个人开发和维护，咖啡和 API 费用等成本均由个人承担，这是一个充满热情的项目。☕
如果您觉得这个工具有用，请考虑通过 GitHub Sponsors 支持其开发。您的支持将是极大的鼓励，也是保持项目持续运行的巨大动力！

[💖 **在 GitHub Sponsors 上支持开发者**](https://github.com/sponsors/pafuhana1213)

---

**以下文档适用于想要自行 Fork 并自定义此工具的用户。**

## 🛠️ 设置说明

1.  **Fork 此仓库：**
    点击右上角的 **Fork** 按钮，将此仓库复制到您自己的 GitHub 账号下。

2.  **设置基础 Secrets：**
    首先，在仓库的 `Settings` > `Secrets and variables` > `Actions` 中注册以下对工具运行至关重要的 Secrets。
    -   `UE_REPO_PAT`：一个具有私有 Unreal Engine 仓库 (`EpicGames/UnrealEngine`) 读取权限的 [个人访问令牌 (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)。
    -   `GEMINI_API_KEY`：从 [Google AI Studio](https://aistudio.google.com/app/apikey) 获取的 API 密钥。

3.  **配置通知目标（至少需要一个）：**
    接下来，选择并配置您希望接收报告的位置。您可以设置 **GitHub Discussions**、**Slack**、**Discord**、**飞书 (Feishu)** 或其中的任何组合。

    #### A) 发布到 GitHub Discussions
    适用于团队讨论和永久记录。
    1.  **启用 Discussions：** 在目标仓库的 `Settings` > `General` > `Features` 中启用 `Discussions`。
    2.  **创建类别：** 在 Discussions 选项卡中创建一个类别（例如 `Announcements`）。
    3.  **添加 Secrets：** 注册以下 Secrets。
        -   `DISCUSSION_REPO`：用于发布报告的**私有**仓库名称（例如 `MyOrg/MyTeamRepo`）。
        -   `DISCUSSION_REPO_PAT`：具有在 `DISCUSSION_REPO` 中写入 Discussions 权限的 PAT。

    #### B) 发布到 Slack
    适用于实时通知和快速信息共享。
    1.  **创建 Incoming Webhook：** 按照 [Slack 文档](https://slack.com/help/articles/115005265063-Using-Incoming-Webhooks-in-Slack) 为您所需的频道发布 Webhook URL。
    2.  **添加 Secrets：** 注册以下 Secrets。
        -   `SLACK_WEBHOOK_URL`：上面发布的 Incoming Webhook URL。
        -   `SLACK_CHANNEL`：要发布到的 Slack 频道名称（例如 `#ue-updates`）。

    #### C) 发布到 Discord
    同样适用于实时通知。
    1.  **创建 Webhook：** 按照 [Discord 文档](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) 为您**所需的频道**创建 Webhook URL。在 Discord 中，URL 本身决定了目标频道，因此您不需要像 Slack 那样单独指定频道名称。
    2.  **添加 Secret：** 注册以下 Secret。
        -   `DISCORD_WEBHOOK_URL`：上面创建的 Webhook URL。

    #### D) 发布到飞书 (Feishu)
    适用于使用飞书办公的团队。
    1.  **创建自定义机器人：** 在飞书群组的“设置” -> “群机器人”中添加“自定义机器人”，并复制它的 Webhook URL。
    2.  **添加 Secret：** 注册以下 Secret。
        -   `FEISHU_WEBHOOK_URL`：上面复制的 Webhook URL。

  **⚠️ 重要：安全操作建议**
  Unreal Engine 的更新历史是机密信息，仅根据 Epic Games 许可协议向授权帐户开放。为防止意外的信息泄露，如果未配置至少一个通知目标，该工具将**停止运行**。

**建议设置：**
强烈建议将 `DISCUSSION_REPO` 设置为 **Unreal Engine 源码仓库的 Fork 仓库，或者是另一个仅由具有等同访问权限的成员组成的私有仓库。** 这可确保遵守许可协议并允许安全的信息共享。

## 🏃‍♀️ 如何运行

-   **自动运行：** 工作流根据配置的计划自动运行（默认每天 UTC 23:00 / 北京时间次日 07:00）。
-   **手动运行：** 您也可以通过访问仓库的 `Actions` 选项卡，选择 `Unreal Engine Update Tracker` 工作流，然后点击 `Run workflow` 按钮来手动运行。**注意：手动运行受限于仓库管理员。**
    -   **Report Language：** 输入报告的语言（例如 `Chinese`, `English`, `Japanese`）。默认值：`Japanese`。
    -   **Commit Scan Limit：** 指定手动运行要扫描的最近提交数量（默认：过去 24 小时内的提交）。
    -   **Discussion Category：** 发布报告的 Discussion 类别名称。默认值：`Daily Reports`。
    -   **Gemini Model：** 用于分析的 AI 模型名称。默认值：`gemini-2.5-pro`。
    -   **Slack Webhook URL：** 要使用的临时 Slack Webhook URL，将覆盖 Secret。
    -   **Slack Channel：** 要使用的临时 Slack 频道名称，将覆盖 Secret。
    -   **Discord Webhook URL：** 要使用的临时 Discord Webhook URL，将覆盖 Secret。
    -   **Feishu Webhook URL：** 要使用的临时飞书 Webhook URL，将覆盖 Secret。

-   **更改默认值：**
    您可以通过设置仓库的 **Variables** 来更改计划运行和手动运行的默认值。转到 `Settings` > `Secrets and variables` > `Actions`，在 `Variables` 选项卡中设置以下内容：
    -   `REPORT_LANGUAGE`：默认报告语言（例如 `Chinese`）。
    -   `DISCUSSION_CATEGORY`：默认发布类别（例如 `Daily Reports`）。
    -   `GEMINI_MODEL`：默认使用的 AI 模型（例如 `gemini-2.5-pro`）。
    -   `UE_BRANCH`：要监控的分支名称（例如 `release`）。默认值为 `ue5-main`。

## 🎨 自定义

### 更改报告格式

输出格式（包括报告的类别、总结样式和整体结构）由提供给 AI 的指令（Prompt）决定。

如果您想更改格式，例如要求更详细的报告或强调特定信息，可以直接编辑仓库根目录下的 `prompts/report_prompt.md` 文件。通过修改此文件，您可以自定义 AI 的行为，而无需修改任何 Python 代码。

## 📝 许可和重要注意事项

**在使用此工具之前，请仔细阅读以下内容。**

-   **用户责任：** 虽然此工具经过精心设计以符合 Unreal Engine 许可协议，但最终的操作责任在于用户。具体而言，您必须**始终指定一个访问受限的私有仓库**作为报告的目标位置 (`DISCUSSION_REPO`)。发布到公共仓库可能会构成违反许可协议。

-   **API 密钥和计费：**
    *   此工具使用 Google Gemini API，可能会根据使用情况产生费用。
    *   如果您 Fork 并使用此仓库，**Fork 仓库的所有者承担其 API 密钥的所有计费责任。**
    *   为了确保严格遵守 Unreal Engine 的条款，**强烈建议使用提交的数据不用于 AI 训练的许可方案下的 API 密钥。**

-   **设计上的安全性：**
    *   为了将违反许可的风险降至最低，此工具在向 AI 提供信息时**不会发送任何 Unreal Engine 源代码或代码差分 (diff)**。分析仅基于提交消息和更改的文件路径。

-   **运行注意事项：**
    *   此脚本实际上会根据其配置发布到 GitHub Discussions。请在测试运行期间保持谨慎。
    *   各种 API 都有使用限制（频率限制）。

---
