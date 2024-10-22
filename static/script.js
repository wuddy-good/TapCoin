// script.js

// Змінна для зберігання ID користувача
const userId = 1; // Заміна на реальний ID користувача
let timerInterval;

// Функція для отримання даних користувача
async function fetchUserData() {
    try {
        const response = await fetch(`/user?id=${userId}`);
        if (!response.ok) {
            throw new Error('Не вдалося отримати дані користувача');
        }
        const data = await response.json();
        document.getElementById('coinsCount').innerText = data.coins;
        startTimer(data.remaining_time || data.timer_duration); // Використовуйте значення з БД
    } catch (error) {
        console.error('Помилка:', error);
        alert('Не вдалося отримати дані користувача. Спробуйте ще раз.');
    }
}

// Функція для запуску таймера
function startTimer(duration) {
    let remainingTime = duration;
    document.getElementById('timer').innerText = remainingTime;

    clearInterval(timerInterval);
    document.getElementById('claimButton').disabled = true;

    timerInterval = setInterval(() => {
        remainingTime -= 1;
        document.getElementById('timer').innerText = remainingTime;

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            document.getElementById('claimButton').disabled = false;
            document.getElementById('timer').innerText = duration; // Скидання таймера на початкове значення
        }
    }, 1000);
}

// Обробник події для кнопки "Claim"
document.getElementById('claimButton').addEventListener('click', async () => {
    const response = await fetch('/claim', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: userId })
    });

    const result = await response.json();
    if (result.success) {
        document.getElementById('coinsCount').innerText = result.coins;
        startTimer(data.timer_duration || 60); // Використовуйте значення з БД або значення за замовчуванням
    } else {
        alert(result.message);
    }
});

// Отримання даних користувача при завантаженні сторінки
document.addEventListener('DOMContentLoaded', fetchUserData);
