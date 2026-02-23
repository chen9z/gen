# Extension UI 迁移指南（Textual -> PTK+Rich）

本版本对扩展 UI 做了 **breaking change**：交互式模式已从 Textual 迁移为 `prompt_toolkit + Rich`，UI 协议收敛为纯文本终端语义。

## 1. 关键变更

- 保留：
  - `select/confirm/input/editor`
  - `notify`
  - `set_status`
  - `set_widget(key, content, placement)`
  - `set_header(content)`
  - `set_footer(content)`
  - `set_title`
  - `get_editor_text/set_editor_text`
  - `set_editor_component`
- 移除：
  - 组件工厂（callable）
  - 组件实例生命周期（`dispose`）
  - 任意 UI 组件对象注入

## 2. 参数约束（新增严格校验）

- `set_widget/set_header/set_footer`：仅支持 `str | list[str] | None`
- `set_editor_component`：仅支持 `CustomEditorComponent | None`
- 非法类型会直接抛 `TypeError`（不再静默忽略）

## 3. 典型迁移

旧写法（不再支持）：

```python
session.ui.set_widget("summary", lambda app: MyWidget(app))
session.ui.set_header(lambda app: HeaderComp())
session.ui.set_editor_component(lambda app: EditorComp())
```

新写法（纯文本）：

```python
session.ui.set_widget("summary", ["Line 1", "Line 2"], placement="above_editor")
session.ui.set_header("Build started")
session.ui.set_footer(["press Ctrl+R to resume", "press Ctrl+T to switch tree"])
session.ui.set_editor_component(CustomEditorComponent(placeholder="Type message", title="default"))
```

## 4. placement 约定

- 支持：`above_editor` / `below_editor`
- 兼容别名：`aboveEditor` / `belowEditor`

## 5. RPC 影响

RPC 仍使用 `extension_ui_request/extension_ui_response`，但 payload 仅传文本字段，不再包含组件工厂语义。
