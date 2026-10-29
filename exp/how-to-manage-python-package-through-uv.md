`uv` 提供了两种主要的包管理模式：项目级管理（推荐，类似 Poetry/PDM）和 pip 兼容模式（传统，类似 pip/venv）。你可以根据项目需求选择适合的方式。

以下是详细的管理指南：

1. 项目级管理（推荐）
这是 `uv` 的核心优势所在，它通过 `pyproject.toml` 和 `uv.lock`文件统一管理依赖、虚拟环境和 Python 版本，确保环境的一致性和可复现性。

核心工作流
*   初始化项目：
    ```bash
    uv init my-project
    cd my-project
    ```
    这会生成 `pyproject.toml` 和 `.python-version` 文件。

*   添加依赖：
    ```bash
    添加生产依赖
    uv add requests flask
    
    添加指定版本
    uv add "django>=4.2,<5.0"
    
    添加开发依赖（如测试工具）
    uv add --dev pytest black
    ```
    `uv add` 会自动更新 `pyproject.toml` 中的依赖列表，并生成/更新 `uv.lock` 锁文件。

*   同步环境：
    ```bash
    uv sync
    ```
    该命令会根据 `uv.lock` 文件精确安装所有依赖，并创建或更新虚拟环境（默认在 `.venv`）。如果锁文件不存在，它会先解析依赖并生成锁文件。

*   移除依赖：
    ```bash
    uv remove requests
    uv remove --dev pytest
    ```

*   运行代码：
    ```bash
    自动激活虚拟环境并运行脚本
    uv run python main.py
    
    直接运行命令行工具
    uv run flask run
    ```

优势
*   锁定机制：`uv.lock` 记录了所有传递依赖的确切版本和哈希值，确保在不同机器上构建完全一致的环境。
*   一体化：无需手动管理 `venv`，`uv` 会自动处理虚拟环境的创建和激活。
*   速度快：依赖解析和安装速度远超传统工具。

---

2. Pip 兼容模式
如果你习惯使用 `pip` 和 `requirements.txt`，或者需要与非 `uv` 项目兼容，可以使用 `uv pip` 子命令。它的语法与 `pip` 完全一致，但速度更快。

常用命令
*   安装包：
    ```bash
    安装单个包
    uv pip install requests
    
    从 requirements.txt 安装
    uv pip install -r requirements.txt
    
    可编辑安装（用于本地开发）
    uv pip install -e .
    ```

*   卸载包：
    ```bash
    uv pip uninstall requests
    ```

*   查看已安装包：
    ```bash
    uv pip list
    uv pip show requests
    ```

*   导出依赖：
    ```bash
    uv pip freeze > requirements.txt
    ```

*   升级包：
    ```bash
    uv pip install --upgrade requests
    ```

注意
*   在使用 `uv pip` 之前，你需要手动创建并激活虚拟环境（例如使用 `uv venv` 或 `python -m venv .venv`）。
*   `uv pip` 不会自动生成或维护 `uv.lock` 文件，依赖锁定需依靠 `requirements.txt` 或其他外部工具。

---

3. 虚拟环境管理
无论使用哪种模式，`uv` 都提供了极速的虚拟环境管理功能。

*   创建虚拟环境：
    ```bash
    默认创建 .venv
    uv venv
    
    指定 Python 版本（uv 会自动下载该版本如果本地没有）
    uv venv --python 3.12
    
    指定路径
    uv venv my-env
    ```

*   激活环境：
    *   Linux/macOS: `source .venv/bin/activate`
    *   Windows: `.venv\Scripts\activate`

*   删除环境：直接删除 `.venv` 目录即可。

---

4. 全局工具管理（类似 pipx）
对于不需要绑定到特定项目的命令行工具（如 `ruff`, `black`, `httpie`），可以使用 `uv tool` 进行全局安装，避免污染项目环境。

*   运行工具（无需安装）：
    ```bash
    uv tool run ruff check .
    或简写
    uvx ruff check .
    ```

*   全局安装工具：
    ```bash
    uv tool install ruff
    ```

*   列出/卸载全局工具：
    ```bash
    uv tool list
    uv tool uninstall ruff
    ```

---

总结：如何选择？

| 场景 | 推荐模式 | 关键命令 |
| :--- | :--- | :--- |
| 新项目开发 | 项目级管理 | `uv init`, `uv add`, `uv sync`, `uv run` |
| 现有 pip 项目迁移 | Pip 兼容模式 | `uv pip install -r requirements.txt` |
| 临时运行脚本/工具 | 全局工具管理 | `uvx <tool>` |
| 数据科学/Jupyter | Pip 兼容模式 | `uv venv`, `uv pip install ...` (便于与 Jupyter 内核集成) |

最佳实践建议：对于大多数现代 Python 项目，推荐使用 项目级管理（`uv add`/`uv sync`），因为它提供了更好的依赖锁定、更快的解析速度和更简洁的工作流。<br>参考资料<br>[1] [uv pip 包管理详解：安装、可编辑安装、文件来源与卸载的完整实践-CSDN博客 - CSDN博客](https://blog.csdn.net/gitblog_00686/article/details/155088202)<br>[2] [Python 统一大业：uv 如何整合 Pip、Pyenv 和 Venv？-腾讯云开发者社区-腾讯云 - 腾讯云](https://cloud.tencent.com/developer/article/2671755)<br>[3] [Python包管理工具之uv的使用详细指南_python_脚本之家 - 脚本之家](https://www.jb51.net/python/3564051y2.htm)<br>[4] [uv：Python包管理的工业革命——从pip的3分钟到18秒的… - 程序员茄子 - chenxutan.com](https://chenxutan.com/d/1663.html)<br>[5] [ComfyUI-Manager终极依赖管理指南：5分钟实现pip与uv完美切换-CSDN博客 - CSDN博客](https://blog.csdn.net/gitblog_01043/article/details/160129798)<br>[6] [uv 包管理工具实战：从 pip 困境到依赖与环境的统一管理-CSDN博客 - CSDN博客](https://blog.csdn.net/weixin_26833139/article/details/166655695)<br>[7] [uv 精简使用教程一、安装 uv 验证安装： 二、包管理（对标 pip） 安装包 安装指定版本 批量安装依赖 卸载包 查 - 掘金 - 掘金开发者社区](https://juejin.cn/post/7621084209155194932)<br>[8] [uv包管理 - uv入门教程 - 从入门到精通 - www.baiyingyong.com](https://www.baiyingyong.com/python/uv/uv-packages.html)<br>[9] [UV 全命令速查手册-阿里云开发者社区 - 阿里云开发者社区](https://developer.aliyun.com/article/1711290)<br>[10] [Python 包管理工具 uv 命令大全（附核心注意事项）_python uv包管理-CSDN博客 - CSDN博客](https://blog.csdn.net/qq_44924694/article/details/159207966)<br>[11] [一文详细解析Python包管理工具uv的核心命令使用_阿里西西 - www.alixixi.com](https://www.alixixi.com/wz/643460.html)<br>[12] [一文详解Python包管理工具uv的核心命令使用_python_脚本之家 - 脚本之家](https://www.jb51.net/python/358265pl6.htm)<br>[13] [Python开发者必看！UV包管理器从0到1保姆级教程，彻底告别pip龟速和依赖地狱_uv拉取的包默认放在哪里?-CSDN博客 - CSDN博客](https://blog.csdn.net/lrh122800/article/details/160055007)<br>[14] [python包管理器uv工具的使用-腾讯云开发者社区-腾讯云 - 腾讯云](https://cloud.tencent.com/developer/article/2593276)<br>[15] [Python包管理新选择：uv工具全面解析与迁移指南-CSDN博客 - CSDN博客](https://blog.csdn.net/weixin_32288959/article/details/168808688)<br>[16] [再见pip！Rust 写的 uv 正在把 Python 包管理按在地上摩擦-腾讯云开发者社区-腾讯云 - 腾讯云](https://cloud.tencent.com/developer/article/2670620)<br>[17] [UV 包管理工具深度解析：对比 Conda 与 pip，实战掌握高效 Python 依赖管理方案-腾讯云开发者社区-腾讯云 - 腾讯云](https://cloud.tencent.com/developer/article/2522992)<br>[18] [uv实战：5分钟掌握Python包管理 - 知乎 - 知乎](https://zhuanlan.zhihu.com/p/1905925258747289612)<br>[19] [uv 极速 Python 包管理器完全指南 - 知乎 - 知乎](https://zhuanlan.zhihu.com/p/1994004726371611562)<br>[20] [uv pip install：Python包管理的超高速Rust替代方案-CSDN博客 - CSDN博客](https://blog.csdn.net/weixin_30225755/article/details/166086906)<br>[21] [【Python神器】UV 使用教程：命令示例 - 腾讯云开发者社区-腾讯云 - 腾讯云](https://cloud.tencent.com/developer/news/2617438)<br>[22] [Python包管理工具uv的命令大全(附核心注意事项)_python_脚本之家 - 脚本之家](https://www.jb51.net/python/361226lnr.htm)<br>[23] [Python 包管理工具 uv 使用教程 - 知乎 - 知乎](https://zhuanlan.zhihu.com/p/1888904532131575259)<br>[24] [pip配环境太慢、冲突太多？uv 可能是你今年最值得换的工具-腾讯云开发者社区-腾讯云 - 腾讯云](https://cloud.tencent.com/developer/article/2621128)<br>[25] [最新推出——Python包管理工具之uv_uv包管理工具-CSDN博客 - CSDN博客](https://blog.csdn.net/weixin_49095243/article/details/155847864)<br>[26] [uv 使用笔记：从 pip 到 Rust 级包管理器的实践迁移-CSDN博客 - CSDN博客](https://blog.csdn.net/weixin_30423065/article/details/165470727)<br><br>百度AI生成，内容仅供参考