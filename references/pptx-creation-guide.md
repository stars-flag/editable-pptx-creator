# PPTX Creation Guide

This guide explains how to create editable PowerPoint presentations using python-pptx.

## Overview

The PPTX builder creates native PowerPoint objects (text boxes, shapes, colors) from parsed HTML data. Unlike screenshot-based approaches, all elements are fully editable in PowerPoint.

## Core Concepts

### 1. Presentation Setup

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Create presentation
prs = Presentation()

# Set slide size (16:9 aspect ratio)
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)
```

### 2. Color Management

```python
# Define color palette
colors = {
    'primary': RGBColor(124, 179, 66),      # #7CB342
    'secondary': RGBColor(244, 143, 177),   # #F48FB1
    'accent': RGBColor(255, 213, 79),       # #FFD54F
    'text_primary': RGBColor(46, 125, 50),  # #2E7D32
    'text_secondary': RGBColor(93, 64, 55), # #5D4037
    'bg_light': RGBColor(232, 245, 233),    # #E8F5E9
}
```

### 3. Font Management

```python
# Set font properties
para.font.name = '微软雅黑'  # For Chinese
para.font.name = 'Arial'     # For English
para.font.size = Pt(24)
para.font.bold = True
para.font.italic = True
```

## Slide Types

### 1. Title Slide

```python
def add_title_slide(self, title, subtitle):
    """Add title slide with main title and subtitle"""
    slide_layout = self.prs.slide_layouts[6]  # Blank layout
    slide = self.prs.slides.add_slide(slide_layout)

    # Add background
    self.add_background(slide)

    # Add main title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(2.5), Inches(8), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.alignment = PP_ALIGN.CENTER
    title_para.font.size = Pt(54)
    title_para.font.bold = True
    title_para.font.color.rgb = self.colors['text_primary']
    title_para.font.name = '微软雅黑'

    # Add subtitle
    if subtitle:
        subtitle_box = slide.shapes.add_textbox(
            Inches(1), Inches(4), Inches(8), Inches(1)
        )
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.text = subtitle
        subtitle_para = subtitle_frame.paragraphs[0]
        subtitle_para.alignment = PP_ALIGN.CENTER
        subtitle_para.font.size = Pt(28)
        subtitle_para.font.color.rgb = self.colors['text_secondary']
        subtitle_para.font.name = '微软雅黑'

    # Add decorations
    self.add_flower_decoration(slide)

    return slide
```

### 2. Content Slide (List)

```python
def add_content_slide(self, title, items):
    """Add content slide with bullet list"""
    slide_layout = self.prs.slide_layouts[6]
    slide = self.prs.slides.add_slide(slide_layout)

    # Add background
    self.add_background(slide)

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(0.8), Inches(8), Inches(1)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.alignment = PP_ALIGN.CENTER
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.font.color.rgb = self.colors['text_primary']
    title_para.font.name = '微软雅黑'

    # Add list items
    start_y = 2.2
    for i, item in enumerate(items):
        # Create item background box
        item_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1.5), Inches(start_y),
            Inches(7), Inches(0.7)
        )
        item_box.fill.solid()
        item_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
        item_box.fill.fore_color.brightness = 0.4  # Semi-transparent white
        item_box.line.color.rgb = self.colors['primary']
        item_box.line.width = Pt(2)

        # Add item text
        text_box = slide.shapes.add_textbox(
            Inches(1.7), Inches(start_y + 0.1),
            Inches(6.6), Inches(0.5)
        )
        text_frame = text_box.text_frame
        text_frame.text = f"• {item}"
        text_frame.word_wrap = True
        para = text_frame.paragraphs[0]
        para.font.size = Pt(24)
        para.font.color.rgb = self.colors['text_secondary']
        para.font.name = '微软雅黑'

        start_y += 0.9

    # Add decorations
    self.add_flower_decoration(slide)

    return slide
```

### 3. Card Grid Slide

```python
def add_color_cards_slide(self, title, colors):
    """Add color card grid slide (2x2 layout)"""
    slide_layout = self.prs.slide_layouts[6]
    slide = self.prs.slides.add_slide(slide_layout)

    # Add background
    self.add_background(slide)

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(0.5), Inches(8), Inches(1)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.alignment = PP_ALIGN.CENTER
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.font.color.rgb = self.colors['text_primary']
    title_para.font.name = '微软雅黑'

    # Add color cards (2x2 grid)
    positions = [
        (1.5, 1.8), (5.5, 1.8),
        (1.5, 4.2), (5.5, 4.2)
    ]

    for i, (color_name, color_meaning, color_rgb) in enumerate(colors):
        x, y = positions[i]

        # Card background
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y),
            Inches(3), Inches(2)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.fill.fore_color.brightness = 0.2
        card.line.color.rgb = self.colors['primary']
        card.line.width = Pt(1)

        # Color circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(x + 1), Inches(y + 0.3),
            Inches(1), Inches(1)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color_rgb
        circle.line.color.rgb = RGBColor(0, 0, 0)
        circle.line.width = Pt(1)

        # Color name
        name_box = slide.shapes.add_textbox(
            Inches(x), Inches(y + 1.4),
            Inches(3), Inches(0.3)
        )
        name_frame = name_box.text_frame
        name_frame.text = color_name
        name_para = name_frame.paragraphs[0]
        name_para.alignment = PP_ALIGN.CENTER
        name_para.font.size = Pt(18)
        name_para.font.bold = True
        name_para.font.color.rgb = self.colors['text_primary']
        name_para.font.name = '微软雅黑'

        # Color meaning
        meaning_box = slide.shapes.add_textbox(
            Inches(x), Inches(y + 1.7),
            Inches(3), Inches(0.25)
        )
        meaning_frame = meaning_box.text_frame
        meaning_frame.text = color_meaning
        meaning_para = meaning_frame.paragraphs[0]
        meaning_para.alignment = PP_ALIGN.CENTER
        meaning_para.font.size = Pt(14)
        meaning_para.font.color.rgb = self.colors['text_light']
        meaning_para.font.name = '微软雅黑'

    return slide
```

### 4. Poem Slide

```python
def add_poems_slide(self, title, poems):
    """Add poem slide with poem cards"""
    slide_layout = self.prs.slide_layouts[6]
    slide = self.prs.slides.add_slide(slide_layout)

    # Add background
    self.add_background(slide)

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(0.3), Inches(8), Inches(0.8)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.alignment = PP_ALIGN.CENTER
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = self.colors['text_primary']
    title_para.font.name = '微软雅黑'

    # Add poem cards
    start_y = 1.3
    for poem_text, poem_author in poems:
        # Poem card background
        poem_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1.5), Inches(start_y),
            Inches(7), Inches(1.5)
        )
        poem_card.fill.solid()
        poem_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        poem_card.fill.fore_color.brightness = 0.3
        poem_card.line.color.rgb = self.colors['primary']
        poem_card.line.width = Pt(2)

        # Poem text
        poem_box = slide.shapes.add_textbox(
            Inches(1.7), Inches(start_y + 0.3),
            Inches(6.6), Inches(0.8)
        )
        poem_frame = poem_box.text_frame
        poem_frame.text = poem_text
        poem_frame.word_wrap = True
        poem_para = poem_frame.paragraphs[0]
        poem_para.alignment = PP_ALIGN.CENTER
        poem_para.font.size = Pt(22)
        poem_para.font.color.rgb = self.colors['text_primary']
        poem_para.font.name = '楷体'

        # Author
        author_box = slide.shapes.add_textbox(
            Inches(1.7), Inches(start_y + 1.1),
            Inches(6.6), Inches(0.3)
        )
        author_frame = author_box.text_frame
        author_frame.text = poem_author
        author_para = author_frame.paragraphs[0]
        author_para.alignment = PP_ALIGN.CENTER
        author_para.font.size = Pt(14)
        author_para.italic = True
        author_para.font.color.rgb = self.colors['text_light']
        author_para.font.name = '微软雅黑'

        start_y += 1.7

    return slide
```

## Background and Decorations

### Gradient Background

```python
def add_background(self, slide):
    """Add gradient background"""
    background = slide.background
    fill = background.fill
    fill.gradient()
    fill.gradient_angle = 135
    fill.gradient_stops[0].color.rgb = self.colors['bg_light']
    fill.gradient_stops[1].color.rgb = self.colors['bg_pink']
```

### Decorative Elements

```python
def add_flower_decoration(self, slide):
    """Add decorative flower elements"""
    positions = [
        (0.3, 0.3, 0.3), (8.7, 0.5, 0.25),
        (0.5, 6.5, 0.25), (8.5, 6.3, 0.3)
    ]

    for x, y, size in positions:
        flower = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(x), Inches(y),
            Inches(size), Inches(size)
        )
        flower.fill.solid()
        flower.fill.fore_color.rgb = self.colors['secondary']
        flower.fill.fore_color.brightness = 0.3
        flower.line.fill.background()
```

## Text Formatting

### Alignment

```python
from pptx.enum.text import PP_ALIGN

para.alignment = PP_ALIGN.LEFT    # Left align
para.alignment = PP_ALIGN.CENTER  # Center align
para.alignment = PP_ALIGN.RIGHT   # Right align
para.alignment = PP_ALIGN.JUSTIFY # Justify
```

### Font Properties

```python
para.font.size = Pt(24)
para.font.bold = True
para.font.italic = True
para.font.underline = True
para.font.color.rgb = RGBColor(46, 125, 50)
para.font.name = '微软雅黑'
```

### Text Frame Properties

```python
text_frame.word_wrap = True  # Enable word wrap
text_frame.margin_left = Pt(10)
text_frame.margin_right = Pt(10)
text_frame.margin_top = Pt(10)
text_frame.margin_bottom = Pt(10)
```

## Shape Properties

### Fill

```python
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(124, 179, 66)
shape.fill.fore_color.brightness = 0.2  # Lighter
shape.fill.fore_color.brightness = -0.2 # Darker
```

### Line/Border

```python
shape.line.color.rgb = RGBColor(46, 125, 50)
shape.line.width = Pt(2)
shape.line.fill.background()  # No line
```

### Shape Types

```python
from pptx.enum.shapes import MSO_SHAPE

MSO_SHAPE.ROUNDED_RECTANGLE  # Rounded rectangle
MSO_SHAPE.OVAL               # Oval/circle
MSO_SHAPE.RECTANGLE          # Rectangle
MSO_SHAPE.DIAMOND            # Diamond
MSO_SHAPE.HEXAGON            # Hexagon
```

## Best Practices

1. **Use native objects**: Always create text boxes and shapes, never use screenshots
2. **Maintain consistency**: Use the same fonts, colors, and spacing across slides
3. **Test editability**: Verify that all elements can be edited in PowerPoint
4. **Handle overflow**: If content doesn't fit, split across multiple slides
5. **Use proper fonts**: Use Microsoft YaHei for Chinese, Arial for English
6. **Set appropriate sizes**: Use `Inches()` for positioning and sizing
7. **Add decorations**: Use subtle decorative elements to enhance visual appeal

## Verification

```python
def verify_editability(self):
    """Verify that all elements are editable"""
    stats = {
        'text_boxes': 0,
        'shapes': 0,
        'images': 0,
        'screenshots': 0
    }

    for slide in self.prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                stats['text_boxes'] += 1
            stats['shapes'] += 1
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                stats['images'] += 1

    return stats
```

## Example Usage

```python
builder = PPTXBuilder(theme='spring')

# Build from parsed data
builder.build(slide_data)

# Verify editability
stats = builder.verify_editability()
print(f"Text boxes: {stats['text_boxes']}")
print(f"Shapes: {stats['shapes']}")

# Save
builder.save('presentation.pptx')
```

## Common Issues

### Issue: Text not visible
**Solution**: Check font color contrast with background

### Issue: Text overflow
**Solution**: Increase text box height or split content

### Issue: Shapes not aligned
**Solution**: Use consistent positioning with `Inches()`

### Issue: Colors not matching
**Solution**: Ensure RGB values are correct

### Issue: Fonts not displaying
**Solution**: Use standard fonts (Arial, Microsoft YaHei)
