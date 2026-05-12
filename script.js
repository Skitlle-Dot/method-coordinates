// Данные о типах задач
const taskTypes = [
    { number: 1, name: 'Планиметрия', count: 20 },
    { number: 2, name: 'Векторы', count: 20 },
    { number: 3, name: 'Стереометрия', count: 20 },
    { number: 8, name: 'Производная', count: 20 },
    { number: 12, name: 'Экстремумы', count: 10 },
    { number: 14, name: 'Сложная стереометрия', count: 10 },
    { number: 15, name: 'Неравенства', count: 20 },
    { number: 16, name: 'Движение', count: 10 },
    { number: 17, name: 'Сложная планиметрия', count: 5 }
];

function renderTaskTypes() {
    const grid = document.getElementById('types-grid');
    if (!grid) return;

    taskTypes.forEach(type => {
        const card = document.createElement('a');
        card.href = `tasks/type${type.number}.html`;
        card.className = 'type-card';
        card.innerHTML = `
            <h3>Задание ${type.number}</h3>
            <p>${type.name}</p>
            <span class="count">${type.count} задач</span>
        `;
        grid.appendChild(card);
    });
}

function showAnswer() {
    const answer = document.getElementById('answer');
    const solution = document.getElementById('solution');
    if (answer) answer.classList.add('show');
    if (solution) solution.classList.remove('show');
}

function showSolution() {
    const answer = document.getElementById('answer');
    const solution = document.getElementById('solution');
    if (solution) solution.classList.add('show');
    if (answer) answer.classList.remove('show');
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(savedTheme);
    
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        toggleBtn.textContent = savedTheme === 'light' ? '🌙 Тёмная тема' : '☀️ Светлая тема';
        
        toggleBtn.addEventListener('click', () => {
            if (document.body.classList.contains('light')) {
                document.body.classList.remove('light');
                document.body.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                toggleBtn.textContent = '☀️ Светлая тема';
            } else {
                document.body.classList.remove('dark');
                document.body.classList.add('light');
                localStorage.setItem('theme', 'light');
                toggleBtn.textContent = '🌙 Тёмная тема';
            }
        });
    }
}

window.showAnswer = showAnswer;
window.showSolution = showSolution;

document.addEventListener('DOMContentLoaded', () => {
    renderTaskTypes();
    initTheme();
});