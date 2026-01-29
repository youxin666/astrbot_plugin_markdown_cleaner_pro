from astrbot import plugin
from astrbot.message import Message
import re

PLUGIN_META = {
    "id": "markdown_cleaner_pro",
    "name": "强化版Markdown清理插件",
    "version": "1.0.0",
    "description": "彻底移除回复中的**、##等Markdown格式",
    "author": "youxin666",
    "homepage": "https://github.com/youxin666/astrbot_plugin_markdown_cleaner_pro",
    "license": "MIT",
    "requirements": [],
    "config": []
}

class MarkdownCleanerProPlugin(plugin.Plugin):
    def __init__(self, config: dict):
        super().__init__(config)
        # 强化版过滤规则：覆盖所有**、##、列表、引用
        self.patterns = [
            (re.compile(r"\*\*+"), r""),  # 匹配1个及以上**，直接移除
            (re.compile(r"#{1,6}\s*"), r""),  # 匹配##/###等标题符号
            (re.compile(r"(\*|\-|\+)\s"), r""),  # 匹配列表符号（* - +）
            (re.compile(r">+\s"), r""),  # 匹配引用符号（>）
        ]

    @plugin.hook("on_reply_filter")
    def clean_markdown(self, msg: Message) -> Message:
        if msg.content:
            cleaned = msg.content
            # 依次应用所有过滤规则
            for pattern, replacement in self.patterns:
                cleaned = pattern.sub(replacement, cleaned)
            msg.content = cleaned
        return msg

def load_plugin(config: dict) -> plugin.Plugin:
    return MarkdownCleanerProPlugin(config)
