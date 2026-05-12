import os
import re

# Создаём папку tasks, если её нет
os.makedirs('tasks', exist_ok=True)

# Читаем файл с задачами
with open('tasks.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Разбиваем по маркеру "### Задача"
blocks = re.split(r'### Задача\s+', content)[1:]

# Словарь для хранения задач по типам
tasks_by_type = {}

def convert_to_latex(text):
    """Конвертирует простые математические выражения в LaTeX для MathJax"""
    if not text:
        return text
    
    # Защищаем уже существующие LaTeX-выражения
    if '\\(' in text or '\\[' in text:
        return text
    
    # Заменяем стрелочки на векторы
    text = text.replace('\\overrightarrow', '\\vec')
    text = text.replace('→', '\\vec ')
    
    # Корни (√(x) → \sqrt{x})
    text = re.sub(r'√\(([^)]+)\)', r'\\sqrt{\1}', text)
    text = re.sub(r'√([0-9]+(?:[,.]?[0-9]+)?)', r'\\sqrt{\1}', text)
    
    # Дроби через / (но только если это не часть текста)
    # Осторожно, чтобы не сломать обычные слэши
    text = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', text)
    
    # Степени (x² → x^2, x³ → x^3)
    text = text.replace('²', '^2').replace('³', '^3')
    
    # Точка для умножения
    text = text.replace('·', '\\cdot ')
    
    # Фигурные скобки для векторов {x; y; z} → \{x; y; z\}
    text = re.sub(r'\{([^{}]+)\}', r'\\{\1\\}', text)
    
    # Греческие буквы
    greek_map = {
        'φ': '\\varphi',
        'π': '\\pi',
        'α': '\\alpha',
        'β': '\\beta',
        'γ': '\\gamma',
        'Δ': '\\Delta',
        'λ': '\\lambda',
        'μ': '\\mu',
        'σ': '\\sigma',
        'ω': '\\omega',
        'ε': '\\varepsilon',
    }
    for gr, latex_gr in greek_map.items():
        text = text.replace(gr, latex_gr)
    
    # Проверяем, есть ли математические символы
    math_patterns = ['sqrt', 'frac', 'cdot', '^', 'vec', '\\{', '\\}', 'varphi', 'pi', 'alpha', 'beta', 'gamma', 'Delta', 'lambda', 'mu', 'sigma', 'omega', 'varepsilon']
    has_math = any(p in text for p in math_patterns)
    
    # Обрабатываем куски текста с формулами
    if has_math and '\\(' not in text:
        # Разбиваем по пробелам и пунктуации, обрамляем только части с математикой
        result_parts = []
        
        # Регулярка для поиска потенциальных формул
        math_candidates = re.finditer(r'([-+]?\d*\.?\d*\s*[a-zA-Z]?\s*[\+\-\*\/\^=]?\s*[^\s]+)', text)
        
        # Простой подход: оборачиваем весь текст в \(...\) если есть математика
        # Но аккуратно с переносами строк
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if any(p in line for p in math_patterns):
                if not line.strip().startswith('\\('):
                    new_lines.append(f'\\({line}\\)')
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        text = '\n'.join(new_lines)
    
    return text

def format_with_line_breaks(text):
    """Сохраняет переносы строк и добавляет отступы"""
    if not text:
        return text
    
    # Заменяем переносы строк на <br> для HTML
    text = text.replace('\n', '<br>\n')
    return text

for block in blocks:
    try:
        number_match = re.match(r'(\d+)\.(\d+)', block.strip())
        if not number_match:
            continue
        
        task_type = number_match.group(1)
        task_index = number_match.group(2)
        
        condition_match = re.search(r'\*\*Условие:\*\*(.*?)\*\*Решение:\*\*', block, re.DOTALL)
        if not condition_match:
            continue
        task_text = condition_match.group(1).strip()
        
        solution_match = re.search(r'\*\*Решение:\*\*(.*?)\*\*Ответ:\*\*', block, re.DOTALL)
        if not solution_match:
            continue
        solution_text = solution_match.group(1).strip()
        
        answer_match = re.search(r'\*\*Ответ:\*\*(.*?)(?=\n---|\n###|\Z)', block, re.DOTALL)
        if not answer_match:
            continue
        answer_text = answer_match.group(1).strip()
        
        if task_type not in tasks_by_type:
            tasks_by_type[task_type] = []
        
        tasks_by_type[task_type].append({
            'index': task_index,
            'task_text': task_text,
            'solution': solution_text,
            'answer': answer_text
        })
        
        # Применяем конвертацию в LaTeX
        task_text_display = convert_to_latex(task_text)
        solution_display = convert_to_latex(solution_text)
        answer_display = convert_to_latex(answer_text)
        
        # Сохраняем переносы строк
        task_text_display = format_with_line_breaks(task_text_display)
        solution_display = format_with_line_breaks(solution_display)
        answer_display = format_with_line_breaks(answer_display)
        
        filename = f'tasks/task_{task_type}_{task_index}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Задание {task_type}.{task_index} - Метод координат</title>
    <link rel="stylesheet" href="../style.css?v=6">
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script" async></script>
</head>
<body class="light">
    <div class="container">
        <header>
            <h1>📝 Задание {task_type}.{task_index}</h1>
            <p class="subtitle">Задача по методу координат</p>
        </header>

        <nav>
            <ul>
                <li><a href="../index.html">Главная</a></li>
                <li><a href="../tasks.html">📝 Задачи</a></li>
                <li><a href="../theory.html">📚 Теория</a></li>
                <li><a href="../about.html">📖 О проекте</a></li>
            </ul>
        </nav>

        <button id="theme-toggle" class="theme-toggle">🌙 Тёмная тема</button>

        <main>
            <div class="task-page">
                <div class="task-condition">
                    <h3>📖 Условие</h3>
                    <div class="task-text" style="line-height: 1.8; white-space: normal;">{task_text_display}</div>
                </div>

                <div class="task-buttons">
                    <button class="task-button answer" onclick="showAnswer()">🔍 Ответ</button>
                    <button class="task-button solution" onclick="showSolution()">📚 Разбор</button>
                    <button class="task-button" onclick="window.history.back()">🔙 Назад</button>
                </div>

                <div id="answer" class="task-result">
                    <h3>✅ Ответ</h3>
                    <div class="task-result-content" style="line-height: 1.8;">{answer_display}</div>
                </div>

                <div id="solution" class="task-result">
                    <h3>📖 Подробный разбор</h3>
                    <div class="task-result-content" style="line-height: 1.8;">{solution_display}</div>
                </div>
            </div>
        </main>

        <footer>
            <div class="footer-content">
                <p>by <strong>Skitlle</strong> • 2026</p>
            </div>
        </footer>
    </div>

    <script src="../script.js"></script>
</body>
</html>''')
        
        print(f"✅ Обработана задача {task_type}.{task_index}")
        
    except Exception as e:
        print(f'❌ Ошибка при обработке блока: {e}')

print(f'\n📊 Всего задач обработано: {sum(len(tasks) for tasks in tasks_by_type.values())}')

# Создаём страницы для каждого типа задач
type_names = {
    '1': 'Планиметрия',
    '2': 'Векторы',
    '3': 'Стереометрия',
    '8': 'Производная',
    '12': 'Экстремумы',
    '14': 'Сложная стереометрия',
    '15': 'Неравенства',
    '16': 'Движение',
    '17': 'Сложная планиметрия'
}

for task_type, tasks in tasks_by_type.items():
    tasks_sorted = sorted(tasks, key=lambda x: int(x['index']))
    
    filename = f'tasks/type{task_type}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Задание {task_type} - Метод координат</title>
    <link rel="stylesheet" href="../style.css?v=6">
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script" async></script>
</head>
<body class="light">
    <div class="container">
        <header>
            <h1>📝 Задание {task_type}</h1>
            <p class="subtitle">{type_names.get(task_type, 'Задачи')}</p>
        </header>

        <nav>
            <ul>
                <li><a href="../index.html">Главная</a></li>
                <li><a href="../tasks.html" class="active">📝 Задачи</a></li>
                <li><a href="../theory.html">📚 Теория</a></li>
                <li><a href="../about.html">📖 О проекте</a></li>
            </ul>
        </nav>

        <button id="theme-toggle" class="theme-toggle">🌙 Тёмная тема</button>

        <main>
            <div class="task-types">
                <h2>Выберите задачу</h2>
                <div class="types-grid">''')

        for task in tasks_sorted:
            f.write(f'''
                    <a href="task_{task_type}_{task['index']}.html" class="type-card">
                        <h3>Задача {task_type}.{task['index']}</h3>
                        <p>📐 Подробное решение</p>
                    </a>''')

        f.write('''
                </div>
            </div>
        </main>

        <footer>
            <div class="footer-content">
                <p>by <strong>Skitlle</strong> • 2026</p>
            </div>
        </footer>
    </div>
    <script src="../script.js"></script>
</body>
</html>''')

print('\n✅ Страницы типов задач созданы!')
print('\n📌 Теперь запусти сервер: python -m http.server')