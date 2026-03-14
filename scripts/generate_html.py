#!/usr/bin/env python3
"""
Generate HTML Presentation
生成HTML演示文稿（简化版，专注于PPTX兼容性）

Usage:
    python generate_html.py --plan "Create a presentation about AI"
    python generate_html.py --generate
    python generate_html.py --generate --theme spring
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Dict, Any, List


def create_planning_md(prompt: str, output_file: str = "PLANNING.md"):
    """
    创建规划文档

    Args:
        prompt: 用户提示
        output_file: 输出文件路径
    """
    planning_content = f"""# Presentation Planning

**Task**: {prompt}
**Slide count**: 8-10
**Language**: Chinese
**Audience**: General audience
**Goals**:
- Present information clearly
- Engage the audience
- Provide actionable insights

**Style**: Professional, clean, modern
**Preset**: Spring

---

## Visual & Layout Guidelines

- **Overall tone**: Professional and approachable
- **Background**: Gradient from light green to light pink
- **Primary text**: Dark green (#2E7D32)
- **Accent (primary)**: Spring green (#7CB342)
- **Typography**: Microsoft YaHei for Chinese, Arial for English
- **Per-slide rule**: 1 key point + up to 5 supporting bullets
- **Animations**: Fade-in effects, 0.6s duration

---

## Slide-by-Slide Outline

**Slide 1 | Cover**
- Title: [Main Title]
- Subtitle: [Subtitle]
- Visual: Gradient background with decorative elements

**Slide 2 | Introduction**
- Title: Introduction
- Key point: [Main point]
- Supporting:
  - [Point 1]
  - [Point 2]
  - [Point 3]

**Slide 3 | Main Content 1**
- Title: [Section Title]
- Key point: [Main point]
- Supporting:
  - [Point 1]
  - [Point 2]
  - [Point 3]
  - [Point 4]

**Slide 4 | Main Content 2**
- Title: [Section Title]
- Key point: [Main point]
- Supporting:
  - [Point 1]
  - [Point 2]
  - [Point 3]

**Slide 5 | Details**
- Title: [Section Title]
- Key point: [Main point]
- Supporting:
  - [Point 1]
  - [Point 2]
  - [Point 3]
  - [Point 4]

**Slide 6 | Examples**
- Title: Examples
- Key point: [Main point]
- Supporting:
  - [Example 1]
  - [Example 2]
  - [Example 3]

**Slide 7 | Summary**
- Title: Summary
- Key point: [Main point]
- Supporting:
  - [Point 1]
  - [Point 2]
  - [Point 3]

**Slide 8 | Closing**
- Title: Thank You
- Subtitle: [Call to action or contact info]
- Visual: Consistent with cover slide

---

## Resources Used

- User prompt: {prompt}

---

## Images

- No images specified (will use CSS-generated elements)

---

## Deliverables

- Output: presentation.html (single-file, zero dependencies)
- Inline editing: Yes
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(planning_content)

    print(f"✅ Planning document created: {output_file}")
    print(f"\n📝 Please review and edit {output_file} to customize your presentation.")
    print(f"   Then run: python generate_html.py --generate")


def read_planning_md(planning_file: str = "PLANNING.md") -> Dict[str, Any]:
    """
    读取规划文档

    Args:
        planning_file: 规划文件路径

    Returns:
        规划数据字典
    """
    if not os.path.exists(planning_file):
        print(f"❌ Planning file not found: {planning_file}")
        print(f"   Run: python generate_html.py --plan \"Your topic\"")
        sys.exit(1)

    with open(planning_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 简化解析，实际应用中可以使用更复杂的解析逻辑
    planning_data = {
        'task': '',
        'slide_count': 8,
        'language': 'Chinese',
        'slides': []
    }

    # 提取任务
    if '**Task**:' in content:
        task_start = content.find('**Task**:') + len('**Task**:')
        task_end = content.find('\n', task_start)
        planning_data['task'] = content[task_start:task_end].strip()

    # 提取幻灯片数量
    if '**Slide count**:' in content:
        count_start = content.find('**Slide count**:') + len('**Slide count**:')
        count_end = content.find('\n', count_start)
        count_str = content[count_start:count_end].strip()
        try:
            planning_data['slide_count'] = int(count_str.split('-')[0].strip())
        except:
            pass

    print(f"✅ Planning document loaded: {planning_file}")
    print(f"   Task: {planning_data['task']}")
    print(f"   Slides: {planning_data['slide_count']}")

    return planning_data


def generate_html(planning_file: str = "PLANNING.md", output_file: str = "presentation.html", theme: str = "spring"):
    """
    生成HTML演示文稿

    Args:
        planning_file: 规划文件路径
        output_file: 输出HTML文件路径
        theme: 主题名称
    """
    planning_data = read_planning_md(planning_file)

    # 主题配置
    themes = {
        'spring': {
            'primary': '#7CB342',
            'secondary': '#F48FB1',
            'accent': '#FFD54F',
            'sky': '#81D4FA',
            'text_primary': '#2E7D32',
            'text_secondary': '#5D4037',
            'bg_start': '#E8F5E9',
            'bg_end': '#FCE4EC'
        },
        'business': {
            'primary': '#1E40AF',
            'secondary': '#3B82F6',
            'accent': '#F59E0B',
            'sky': '#60A5FA',
            'text_primary': '#1F2937',
            'text_secondary': '#4B5563',
            'bg_start': '#F9FAFB',
            'bg_end': '#F3F4F6'
        },
        'creative': {
            'primary': '#8B5CF6',
            'secondary': '#EC4899',
            'accent': '#FBBF24',
            'sky': '#06B6D4',
            'text_primary': '#111827',
            'text_secondary': '#374151',
            'bg_start': '#FEF3C7',
            'bg_end': '#FCE7F3'
        },
        'minimal': {
            'primary': '#374151',
            'secondary': '#6B7280',
            'accent': '#9CA3AF',
            'sky': '#D1D5DB',
            'text_primary': '#111827',
            'text_secondary': '#4B5563',
            'bg_start': '#FFFFFF',
            'bg_end': '#F9FAFB'
        }
    }

    theme_config = themes.get(theme, themes['spring'])

    # 生成HTML内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{planning_data['task']}</title>
    <style>
        /* CSS Variables - Theme: {theme} */
        :root {{
            --color-primary: {theme_config['primary']};
            --color-secondary: {theme_config['secondary']};
            --color-accent: {theme_config['accent']};
            --color-sky: {theme_config['sky']};
            --text-primary: {theme_config['text_primary']};
            --text-secondary: {theme_config['text_secondary']};
            --bg-gradient-start: {theme_config['bg_start']};
            --bg-gradient-end: {theme_config['bg_end']};
            --font-heading: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            --font-body: 'Microsoft YaHei', 'PingFang SC', sans-serif;
        }}

        /* Reset */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html, body {{
            height: 100%;
            overflow: hidden;
            font-family: var(--font-body);
            background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
        }}

        /* Presentation Container */
        .presentation {{
            width: 100vw;
            height: 100vh;
            position: relative;
            overflow: hidden;
        }}

        /* Slide */
        .slide {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 3rem;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.6s ease-in-out, visibility 0.6s ease-in-out;
        }}

        .slide.active {{
            opacity: 1;
            visibility: visible;
        }}

        /* Typography */
        h1 {{
            font-family: var(--font-heading);
            font-size: 3.5rem;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: 1rem;
        }}

        h2 {{
            font-family: var(--font-heading);
            font-size: 2.5rem;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: 2rem;
        }}

        .subtitle {{
            font-size: 1.5rem;
            color: var(--text-secondary);
            text-align: center;
        }}

        /* List */
        ul {{
            list-style: none;
            max-width: 800px;
        }}

        li {{
            font-size: 1.5rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            padding: 0.75rem 1rem;
            background: rgba(255, 255, 255, 0.4);
            border-left: 4px solid var(--color-primary);
            border-radius: 8px;
        }}

        /* Decorative Elements */
        .flower-decoration {{
            position: absolute;
            opacity: 0.15;
            pointer-events: none;
        }}

        .flower {{
            position: absolute;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--color-secondary) 0%, transparent 70%);
        }}

        /* Navigation */
        .nav-dots {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 0.5rem;
            z-index: 100;
        }}

        .nav-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(0, 0, 0, 0.2);
            cursor: pointer;
            transition: background 0.3s;
        }}

        .nav-dot.active {{
            background: var(--color-primary);
        }}

        /* Edit Button */
        .edit-button {{
            position: fixed;
            top: 1rem;
            left: 1rem;
            padding: 0.5rem 1rem;
            background: var(--color-primary);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.875rem;
            z-index: 100;
        }}

        .edit-button:hover {{
            background: var(--color-secondary);
        }}

        /* Editable */
        [contenteditable="true"] {{
            outline: 2px dashed var(--color-accent);
            outline-offset: 4px;
        }}
    </style>
</head>
<body>
    <div class="presentation">
        <!-- Slide 1: Cover -->
        <section class="slide active">
            <h1 contenteditable="false">{planning_data['task']}</h1>
            <p class="subtitle" contenteditable="false">Welcome to this presentation</p>
            <div class="flower-decoration">
                <div class="flower" style="top: 10%; left: 10%;"></div>
                <div class="flower" style="top: 20%; right: 15%;"></div>
                <div class="flower" style="bottom: 15%; left: 15%;"></div>
                <div class="flower" style="bottom: 25%; right: 10%;"></div>
            </div>
        </section>

        <!-- Slide 2: Introduction -->
        <section class="slide">
            <h2 contenteditable="false">Introduction</h2>
            <ul>
                <li contenteditable="false">Key point 1: Introduction to the topic</li>
                <li contenteditable="false">Key point 2: Why this matters</li>
                <li contenteditable="false">Key point 3: What we'll cover</li>
            </ul>
        </section>

        <!-- Slide 3: Main Content -->
        <section class="slide">
            <h2 contenteditable="false">Main Content</h2>
            <ul>
                <li contenteditable="false">Important point 1</li>
                <li contenteditable="false">Important point 2</li>
                <li contenteditable="false">Important point 3</li>
                <li contenteditable="false">Important point 4</li>
            </ul>
        </section>

        <!-- Slide 4: Details -->
        <section class="slide">
            <h2 contenteditable="false">Details</h2>
            <ul>
                <li contenteditable="false">Detail 1: More information</li>
                <li contenteditable="false">Detail 2: Additional context</li>
                <li contenteditable="false">Detail 3: Supporting evidence</li>
            </ul>
        </section>

        <!-- Slide 5: Examples -->
        <section class="slide">
            <h2 contenteditable="false">Examples</h2>
            <ul>
                <li contenteditable="false">Example 1: Real-world application</li>
                <li contenteditable="false">Example 2: Case study</li>
                <li contenteditable="false">Example 3: Best practices</li>
            </ul>
        </section>

        <!-- Slide 6: Summary -->
        <section class="slide">
            <h2 contenteditable="false">Summary</h2>
            <ul>
                <li contenteditable="false">Key takeaway 1</li>
                <li contenteditable="false">Key takeaway 2</li>
                <li contenteditable="false">Key takeaway 3</li>
            </ul>
        </section>

        <!-- Slide 7: Closing -->
        <section class="slide">
            <h1 contenteditable="false">Thank You</h1>
            <p class="subtitle" contenteditable="false">Questions & Discussion</p>
            <div class="flower-decoration">
                <div class="flower" style="top: 10%; left: 10%;"></div>
                <div class="flower" style="top: 20%; right: 15%;"></div>
                <div class="flower" style="bottom: 15%; left: 15%;"></div>
                <div class="flower" style="bottom: 25%; right: 10%;"></div>
            </div>
        </section>
    </div>

    <!-- Navigation Dots -->
    <div class="nav-dots"></div>

    <!-- Edit Button -->
    <button class="edit-button" onclick="toggleEdit()">Edit Mode</button>

    <script>
        // Slide Navigation
        const slides = document.querySelectorAll('.slide');
        const navDotsContainer = document.querySelector('.nav-dots');
        let currentSlide = 0;
        let isEditMode = false;

        // Create navigation dots
        slides.forEach((_, index) => {{
            const dot = document.createElement('div');
            dot.className = 'nav-dot' + (index === 0 ? ' active' : '');
            dot.addEventListener('click', () => goToSlide(index));
            navDotsContainer.appendChild(dot);
        }});

        const navDots = document.querySelectorAll('.nav-dot');

        function goToSlide(index) {{
            slides[currentSlide].classList.remove('active');
            navDots[currentSlide].classList.remove('active');
            currentSlide = index;
            slides[currentSlide].classList.add('active');
            navDots[currentSlide].classList.add('active');
        }}

        function nextSlide() {{
            const next = (currentSlide + 1) % slides.length;
            goToSlide(next);
        }}

        function prevSlide() {{
            const prev = (currentSlide - 1 + slides.length) % slides.length;
            goToSlide(prev);
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (isEditMode) return;
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                nextSlide();
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                prevSlide();
            }}
        }});

        // Touch/swipe navigation
        let touchStartX = 0;
        document.addEventListener('touchstart', (e) => {{
            touchStartX = e.touches[0].clientX;
        }});

        document.addEventListener('touchend', (e) => {{
            if (isEditMode) return;
            const touchEndX = e.changedTouches[0].clientX;
            const diff = touchStartX - touchEndX;
            if (Math.abs(diff) > 50) {{
                if (diff > 0) {{
                    nextSlide();
                }} else {{
                    prevSlide();
                }}
            }}
        }});

        // Edit mode toggle
        function toggleEdit() {{
            isEditMode = !isEditMode;
            const button = document.querySelector('.edit-button');
            const editableElements = document.querySelectorAll('[contenteditable]');

            if (isEditMode) {{
                button.textContent = 'Save';
                button.style.background = 'var(--color-accent)';
                editableElements.forEach(el => {{
                    el.setAttribute('contenteditable', 'true');
                }});
            }} else {{
                button.textContent = 'Edit Mode';
                button.style.background = 'var(--color-primary)';
                editableElements.forEach(el => {{
                    el.setAttribute('contenteditable', 'false');
                }});
                // Auto-save could be implemented here
            }}
        }}
    </script>
</body>
</html>
"""

    # 保存HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ HTML presentation generated: {output_file}")
    print(f"   Theme: {theme}")
    print(f"   Slides: 7")
    print(f"\n💡 To view: Open {output_file} in your browser")
    print(f"💡 To export to PPTX: python generate_editable_pptx.py {output_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Generate HTML presentation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--plan',
        metavar='PROMPT',
        help='Create planning document from prompt'
    )

    parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate HTML from planning document'
    )

    parser.add_argument(
        '--theme',
        default='spring',
        choices=['spring', 'business', 'creative', 'minimal'],
        help='Theme name (default: spring)'
    )

    parser.add_argument(
        '--output',
        help='Output file name'
    )

    args = parser.parse_args()

    if args.plan:
        output_file = args.output or "PLANNING.md"
        create_planning_md(args.plan, output_file)
    elif args.generate:
        planning_file = args.output or "PLANNING.md"
        html_output = args.output or "presentation.html"
        if args.output and args.output.endswith('.html'):
            html_output = args.output
            planning_file = "PLANNING.md"
        generate_html(planning_file, html_output, args.theme)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
