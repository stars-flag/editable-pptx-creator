"""
Theme Manager Module
管理PPTX主题配置
"""
import json
import os
from typing import Dict, Any, List


class ThemeManager:
    """主题管理器，加载和应用主题配置"""

    def __init__(self, themes_dir: str = None):
        """
        初始化主题管理器

        Args:
            themes_dir: 主题配置文件目录
        """
        if themes_dir is None:
            # 默认使用skill目录下的themes文件夹
            current_dir = os.path.dirname(os.path.abspath(__file__))
            themes_dir = os.path.join(os.path.dirname(current_dir), 'themes')

        self.themes_dir = themes_dir
        self.themes = {}
        self._load_all_themes()

    def _load_all_themes(self) -> None:
        """加载所有主题配置"""
        if not os.path.exists(self.themes_dir):
            return

        for filename in os.listdir(self.themes_dir):
            if filename.endswith('.json'):
                theme_name = filename[:-5]  # 移除.json后缀
                theme_path = os.path.join(self.themes_dir, filename)
                try:
                    with open(theme_path, 'r', encoding='utf-8') as f:
                        self.themes[theme_name] = json.load(f)
                except Exception as e:
                    print(f"Warning: Failed to load theme {theme_name}: {e}")

    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """
        获取指定主题配置

        Args:
            theme_name: 主题名称

        Returns:
            主题配置字典
        """
        if theme_name not in self.themes:
            print(f"Warning: Theme '{theme_name}' not found, using 'spring' theme")
            theme_name = 'spring'

        return self.themes.get(theme_name, self._get_default_theme())

    def get_available_themes(self) -> List[str]:
        """
        获取可用主题列表

        Returns:
            主题名称列表
        """
        return list(self.themes.keys())

    def list_themes(self) -> None:
        """列出所有可用主题及其描述"""
        print("Available themes:")
        print("-" * 60)

        for theme_name, theme_config in self.themes.items():
            name = theme_config.get('name', theme_name)
            description = theme_config.get('description', 'No description')
            print(f"  {theme_name:15} - {description}")

        print("-" * 60)

    def _get_default_theme(self) -> Dict[str, Any]:
        """获取默认主题配置"""
        return {
            "name": "Spring",
            "description": "Warm, vibrant spring theme",
            "colors": {
                "primary": "#7CB342",
                "secondary": "#F48FB1",
                "accent": "#FFD54F",
                "sky": "#81D4FA",
                "text_primary": "#2E7D32",
                "text_secondary": "#5D4037",
                "text_light": "#8D6E63",
                "bg_light": "#E8F5E9",
                "bg_pink": "#FCE4EC"
            },
            "fonts": {
                "heading": "微软雅黑",
                "body": "微软雅黑",
                "poem": "楷体"
            },
            "layout": {
                "slide_padding": 1.0,
                "content_gap": 0.5,
                "card_radius": 0.2
            }
        }

    def create_custom_theme(self, theme_name: str, theme_config: Dict[str, Any]) -> None:
        """
        创建自定义主题

        Args:
            theme_name: 主题名称
            theme_config: 主题配置
        """
        self.themes[theme_name] = theme_config

        # 保存到文件
        theme_path = os.path.join(self.themes_dir, f"{theme_name}.json")
        os.makedirs(self.themes_dir, exist_ok=True)

        with open(theme_path, 'w', encoding='utf-8') as f:
            json.dump(theme_config, f, indent=2, ensure_ascii=False)

        print(f"Custom theme '{theme_name}' created and saved to {theme_path}")

    def validate_theme(self, theme_config: Dict[str, Any]) -> bool:
        """
        验证主题配置是否有效

        Args:
            theme_config: 主题配置

        Returns:
            是否有效
        """
        required_keys = ['colors', 'fonts', 'layout']

        for key in required_keys:
            if key not in theme_config:
                print(f"Error: Missing required key '{key}' in theme config")
                return False

        # 验证颜色格式
        colors = theme_config['colors']
        for color_name, color_value in colors.items():
            if not self._is_valid_color(color_value):
                print(f"Error: Invalid color format for '{color_name}': {color_value}")
                return False

        return True

    def _is_valid_color(self, color: str) -> bool:
        """验证颜色格式是否有效"""
        if not color.startswith('#'):
            return False

        hex_part = color[1:]
        if len(hex_part) not in [3, 6]:
            return False

        try:
            int(hex_part, 16)
            return True
        except ValueError:
            return False

    def get_theme_preview(self, theme_name: str) -> str:
        """
        获取主题预览文本

        Args:
            theme_name: 主题名称

        Returns:
            主题预览文本
        """
        theme = self.get_theme(theme_name)

        preview = f"""
Theme: {theme.get('name', theme_name)}
Description: {theme.get('description', 'No description')}

Colors:
  Primary:   {theme['colors'].get('primary', 'N/A')}
  Secondary: {theme['colors'].get('secondary', 'N/A')}
  Accent:    {theme['colors'].get('accent', 'N/A')}
  Text:      {theme['colors'].get('text_primary', 'N/A')}

Fonts:
  Heading: {theme['fonts'].get('heading', 'N/A')}
  Body:    {theme['fonts'].get('body', 'N/A')}
"""
        return preview
