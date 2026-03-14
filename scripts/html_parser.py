"""
HTML Parser Module - 修复版
解析HTML演示文稿，提取幻灯片数据用于PPTX生成
"""
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any, Optional


class HTMLParser:
    """HTML解析器，提取幻灯片结构和内容"""

    def __init__(self):
        self.css_variables = {}

    def parse(self, html_file: str) -> List[Dict[str, Any]]:
        """
        解析HTML文件，提取幻灯片数据

        Args:
            html_file: HTML文件路径

        Returns:
            幻灯片数据列表，每个元素代表一张幻灯片
        """
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取CSS变量
        self._extract_css_variables(soup)

        # 查找所有幻灯片
        slides = soup.find_all('section', class_='slide')

        slide_data = []

        for i, slide in enumerate(slides, 1):
            data = self._parse_slide(slide, i)
            slide_data.append(data)

        return slide_data

    def _extract_css_variables(self, soup: BeautifulSoup) -> None:
        """提取CSS自定义属性（变量）"""
        style_tags = soup.find_all('style')
        for style_tag in style_tags:
            css_text = style_tag.get_text()

            # 查找:root变量
            root_match = re.search(r':root\s*{([^}]+)}', css_text)
            if root_match:
                root_content = root_match.group(1)

                # 提取变量声明
                var_pattern = r'--([\w-]+)\s*:\s*([^;]+);'
                for match in re.finditer(var_pattern, root_content):
                    var_name = match.group(1)
                    var_value = match.group(2).strip()
                    self.css_variables[var_name] = var_value

    def _parse_slide(self, slide: BeautifulSoup, index: int) -> Dict[str, Any]:
        """
        解析单个幻灯片

        Args:
            slide: BeautifulSoup幻灯片元素
            index: 幻灯片索引

        Returns:
            幻灯片数据字典
        """
        data = {'index': index}

        # 获取标题
        h1 = slide.find('h1')
        h2 = slide.find('h2')
        if h1:
            data['title'] = h1.get_text(strip=True)
            data['title_level'] = 1
        elif h2:
            data['title'] = h2.get_text(strip=True)
            data['title_level'] = 2
        else:
            data['title'] = f"Slide {index}"
            data['title_level'] = 2

        # 获取副标题
        subtitle = slide.find(class_='subtitle')
        if subtitle:
            data['subtitle'] = subtitle.get_text(strip=True)

        # 检测内容类型
        # 优先判断是否为标题幻灯片（h1标题）
        if data.get('title_level') == 1:
            data['type'] = 'title'
        elif self._has_table(slide):
            data['type'] = 'table'
            data['table'] = self._parse_table(slide)
        elif self._has_color_cards(slide):
            data['type'] = 'colors'
            data['colors'] = self._parse_color_cards(slide)
        elif self._has_poems(slide):
            data['type'] = 'poems'
            data['poems'] = self._parse_poems(slide)
        elif self._has_two_column(slide):
            data['type'] = 'two_column'
            data['two_column'] = self._parse_two_column(slide)
        elif self._has_cards(slide):
            data['type'] = 'cards'
            data['cards'] = self._parse_cards(slide)
        elif self._has_list_items(slide):
            data['type'] = 'content'
            data['items'] = self._parse_list_items(slide)
        elif self._has_image(slide):
            data['type'] = 'image'
            data['image'] = self._parse_image(slide)
        else:
            data['type'] = 'content'
            data['items'] = []

        return data

    def _has_table(self, slide: BeautifulSoup) -> bool:
        """检查是否包含表格"""
        return slide.find('table') is not None

    def _has_color_cards(self, slide: BeautifulSoup) -> bool:
        """检查是否包含色彩卡片"""
        return len(slide.find_all('div', class_='color-card')) > 0

    def _has_poems(self, slide: BeautifulSoup) -> bool:
        """检查是否包含诗句"""
        return len(slide.find_all('div', class_='poem')) > 0

    def _has_cards(self, slide: BeautifulSoup) -> bool:
        """检查是否包含卡片"""
        return len(slide.find_all('div', class_='card')) > 0

    def _has_two_column(self, slide: BeautifulSoup) -> bool:
        """检查是否包含两列布局"""
        return slide.find('div', class_='two-column') is not None

    def _parse_two_column(self, slide: BeautifulSoup) -> Dict[str, Any]:
        """
        解析两列布局

        Returns:
            {'left': {'title': ..., 'items': [...]}, 'right': {'title': ..., 'items': [...]}}
        """
        two_column = slide.find('div', class_='two-column')
        if not two_column:
            return {'left': {'title': '', 'items': []}, 'right': {'title': '', 'items': []}}

        columns = two_column.find_all('div', recursive=False)
        result = {'left': {'title': '', 'items': []}, 'right': {'title': '', 'items': []}}

        for i, column in enumerate(columns):
            if i >= 2:
                break

            # 获取列标题（h3）
            h3 = column.find('h3')
            column_title = h3.get_text(strip=True) if h3 else ''

            # 获取列表项
            ul = column.find('ul')
            items = []
            if ul:
                for li in ul.find_all('li'):
                    item_text = li.get_text(strip=True)
                    if item_text:
                        items.append(item_text)

            if i == 0:
                result['left'] = {'title': column_title, 'items': items}
            else:
                result['right'] = {'title': column_title, 'items': items}

        return result

    def _has_list_items(self, slide: BeautifulSoup) -> bool:
        """检查是否包含列表项"""
        # 检查带class的列表项
        if len(slide.find_all('li', class_='list-item')) > 0:
            return True
        # 检查普通的li标签（在ul或ol中）
        if slide.find('ul') or slide.find('ol'):
            return True
        return False

    def _has_image(self, slide: BeautifulSoup) -> bool:
        """检查是否包含图片"""
        return slide.find('img', class_='slide-image') is not None

    def _parse_table(self, slide: BeautifulSoup) -> List[List[str]]:
        """
        解析表格

        Returns:
            [[row1_col1, row1_col2, ...], [row2_col1, row2_col2, ...], ...]
        """
        table = slide.find('table')
        if not table:
            return []

        rows = []
        for tr in table.find_all('tr'):
            row_data = []
            for cell in tr.find_all(['th', 'td']):
                cell_text = cell.get_text(strip=True)
                row_data.append(cell_text)
            if row_data:
                rows.append(row_data)

        return rows

    def _parse_color_cards(self, slide: BeautifulSoup) -> List[tuple]:
        """
        解析色彩卡片

        Returns:
            [(name, meaning, rgb), ...]
        """
        colors = []
        color_cards = slide.find_all('div', class_='color-card')

        for card in color_cards:
            name = card.find(class_='color-name')
            meaning = card.find(class_='color-meaning')
            circle = card.find(class_='color-circle')

            color_rgb = self._get_default_color()

            if circle and circle.get('style'):
                # 从内联样式提取颜色
                style = circle.get('style', '')
                color_hex = self._extract_color_from_style(style)
                if color_hex:
                    color_rgb = self._hex_to_rgb(color_hex)

            if name and meaning:
                color_name = name.get_text(strip=True)
                color_meaning = meaning.get_text(strip=True)

                # 根据名称匹配颜色（备用方案）
                if color_rgb == self._get_default_color():
                    color_rgb = self._match_color_by_name(color_name)

                colors.append((color_name, color_meaning, color_rgb))

        return colors

    def _parse_poems(self, slide: BeautifulSoup) -> List[tuple]:
        """
        解析诗句

        Returns:
            [(text, author), ...]
        """
        poems = []
        poem_divs = slide.find_all('div', class_='poem')

        for poem_div in poem_divs:
            text = poem_div.find(class_='poem-text')
            author = poem_div.find(class_='poem-author')

            if text and author:
                poem_text = text.get_text('\n', strip=True)
                poem_author = author.get_text(strip=True)
                poems.append((poem_text, poem_author))

        return poems

    def _parse_cards(self, slide: BeautifulSoup) -> List[Dict[str, str]]:
        """
        解析卡片

        Returns:
            [{'title': ..., 'content': ...}, ...]
        """
        cards = []
        card_divs = slide.find_all('div', class_='card')

        for card_div in card_divs:
            title = card_div.find('h3')
            # 获取所有段落内容
            paragraphs = card_div.find_all('p')
            content = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

            # 如果有标题或者有内容，就创建卡片
            if title or content:
                card_data = {
                    'title': title.get_text(strip=True) if title else '',
                    'content': content
                }
                cards.append(card_data)

        return cards

    def _parse_list_items(self, slide: BeautifulSoup) -> List[str]:
        """
        解析列表项

        Returns:
            [item1, item2, ...]
        """
        items = []
        # 首先查找带class的列表项
        list_items = slide.find_all('li', class_='list-item')

        # 如果没有找到，查找所有li标签
        if not list_items:
            list_items = slide.find_all('li')

        for item in list_items:
            item_text = item.get_text(strip=True)
            if item_text:
                items.append(item_text)

        return items

    def _parse_image(self, slide: BeautifulSoup) -> Dict[str, str]:
        """
        解析图片

        Returns:
            {'src': ..., 'alt': ..., 'caption': ...}
        """
        img = slide.find('img', class_='slide-image')
        caption = slide.find(class_='caption')

        image_data = {
            'src': img.get('src', '') if img else '',
            'alt': img.get('alt', '') if img else '',
            'caption': caption.get_text(strip=True) if caption else ''
        }

        return image_data

    def _extract_color_from_style(self, style: str) -> Optional[str]:
        """从CSS样式中提取颜色值"""
        # 查找background或color属性
        patterns = [
            r'background\s*:\s*#([0-9a-fA-F]{6})',
            r'background-color\s*:\s*#([0-9a-fA-F]{6})',
            r'color\s*:\s*#([0-9a-fA-F]{6})',
            r'background\s*:\s*rgb\((\d+),\s*(\d+),\s*(\d+)\)',
        ]

        for pattern in patterns:
            match = re.search(pattern, style)
            if match:
                if len(match.groups()) == 1:
                    # Hex color
                    return f"#{match.group(1)}"
                else:
                    # RGB color
                    r, g, b = match.groups()
                    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

        return None

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """将十六进制颜色转换为RGB元组"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _get_default_color(self) -> tuple:
        """获取默认颜色"""
        return (124, 179, 66)  # 默认绿色

    def _match_color_by_name(self, color_name: str) -> tuple:
        """根据颜色名称匹配RGB值"""
        color_map = {
            '嫩绿': (124, 179, 66),    # #7CB342
            '粉红': (244, 143, 177),   # #F48FB1
            '金黄': (255, 213, 79),    # #FFD54F
            '天蓝': (129, 212, 250),   # #81D4FA
            '深绿': (46, 125, 50),     # #2E7D32
            '棕色': (93, 64, 55),      # #5D4037
            '浅棕': (141, 110, 99),    # #8D6E63
        }

        for name, rgb in color_map.items():
            if name in color_name:
                return rgb

        return self._get_default_color()

    def get_css_variable(self, var_name: str, default: str = '') -> str:
        """获取CSS变量值"""
        return self.css_variables.get(var_name, default)

    def get_theme_colors(self) -> Dict[str, tuple]:
        """从CSS变量中提取主题颜色"""
        color_map = {
            'primary': '--color-primary',
            'secondary': '--color-secondary',
            'accent': '--color-accent',
            'sky': '--color-sky',
            'text_primary': '--text-primary',
            'text_secondary': '--text-secondary',
            'bg_light': '--bg-gradient-start',
            'bg_pink': '--bg-gradient-end',
        }

        colors = {}
        for key, var_name in color_map.items():
            hex_color = self.get_css_variable(var_name)
            if hex_color:
                colors[key] = self._hex_to_rgb(hex_color)
            else:
                colors[key] = self._get_default_color()

        return colors
