# 导入必要模块（包含yaml和os，用于读取配置文件）
from astrbot import plugin
from astrbot.message import Message
import re
import yaml
import os

# 插件元信息（和plugin.json保持一致）
PLUGIN_META = {
    "id": "markdown_cleaner_pro",
    "name": "强化版Markdown清理插件",
    "version": "1.0.0",
    "description": "彻底移除回复中的**、##等Markdown格式，支持自定义开关",
    "author": "youxin666",
    "homepage": "https://github.com/youxin666/astrbot_plugin_markdown_cleaner_pro",
    "license": "MIT",
    "requirements": [],
    "config": []
}

class MarkdownCleanerProPlugin(plugin.Plugin):
    def __init__(self, config: dict):
        super().__init__(config)
        # ========== 新增：读取config.yaml配置文件 ==========
        # 获取插件文件夹路径，拼接config.yaml的绝对路径
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(plugin_dir, "config.yaml")
        
        # 初始化默认配置（如果config.yaml不存在，用默认值）
        default_config = {
            "remove_bold": True,    # 移除**
            "remove_heading": True, # 移除##/###等标题符号
            "remove_list": True,    # 移除* / - / + 列表符号
            "remove_quote": True    # 移除> 引用符号
        }
        
        # 读取配置文件（如果文件存在则覆盖默认配置）
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    self.plugin_config = yaml.safe_load(f)
                # 合并默认配置（防止用户删了配置项导致报错）
                for key in default_config:
                    if key not in self.plugin_config:
                        self.plugin_config[key] = default_config[key]
            except Exception as e:
                # 配置文件读取失败，用默认配置
                self.plugin_config = default_config
        else:
            # 没有config.yaml，直接用默认配置
            self.plugin_config = default_config

        # ========== 根据配置生成过滤规则 ==========
        self.patterns = []
        # 1. 移除**（加粗）
        if self.plugin_config.get("remove_bold", True):
            self.patterns.append((re.compile(r"\*\*+"), r""))
        # 2. 移除##/###等标题符号
        if self.plugin_config.get("remove_heading", True):
            self.patterns.append((re.compile(r"#{1,6}\s*"), r""))
        # 3. 移除* / - / + 列表符号
        if self.plugin_config.get("remove_list", True):
            self.patterns.append((re.compile(r"(\*|\-|\+)\s"), r""))
        # 4. 移除> 引用符号
        if self.plugin_config.get("remove_quote", True):
            self.patterns.append((re.compile(r">+\s"), r""))

    # 回复过滤钩子：处理所有机器人回复
    @plugin.hook("on_reply_filter")
    def clean_markdown(self, msg: Message) -> Message:
        if msg.content:  # 仅当回复有内容时处理
            cleaned_content = msg.content
            # 依次应用所有过滤规则
            for pattern, replacement in self.patterns:
                cleaned_content = pattern.sub(replacement, cleaned_content)
            # 替换后的内容赋值回消息对象
            msg.content = cleaned_content
        return msg

# 插件加载入口（AstrBot必须的函数）
def load_plugin(config: dict) -> plugin.Plugin:
    return MarkdownCleanerProPlugin(config)
