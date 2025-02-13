function showLoading() {
    document.getElementById("loading").style.display = "block";
}

// Функция для скрытия иконки загрузки
function hideLoading() {
    document.getElementById("loading").style.display = "none";
}


async function loadMotorcycles() {
    showLoading()
    try {

        const response = await fetch('/moto/get_all_moto/'); // Укажите ваш URL API
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const motorcycles = await response.json();
        await renderMotorcycles(motorcycles);
        hideLoading()
    } catch (error) {
        hideLoading()
        console.error('Ошибка:', error);
        document.getElementById('content').innerHTML = '<p>Не удалось загрузить данные</p>';
    }
}



// Функция для рендеринга данных
async function renderMotorcycles(motorcycles) {
    const tableBody = document.getElementById('table-body');

    // Очистка таблицы
    tableBody.innerHTML = '';

    motorcycles.forEach(motorcycle => {

        // Создание строки
        const tableRow = document.createElement('a');
        tableRow.className = 'table-row';

        // Создание ссылки с передачей минимальных данных через URL
        tableRow.href = `/moto/details/${motorcycle.id}`;
        // Внутри ссылки создаём HTML для содержимого строки
        tableRow.innerHTML = `
            <div class="image">
                <img src="${motorcycle.image_url[0]}" alt="${motorcycle.name}">
            </div>
            <div class="item-title">
                <span class="moto-name">${motorcycle.name}</span>
            </div>
            <div class="row-item">
                <span class="column-name">Класс:</span>
                <span class="row-value">${motorcycle.moto_class}</span>
            </div>
            <div class="row-item">
                <span class="column-name">Год, объем:</span>
                <span class="row-value"></span>
            </div>
            <div class="row-item">
                <span class="column-name">Пробег:</span>
                <span class="row-value"></span>
            </div>
            <div class="row-item">
                <span class="column-name">Состояние:</span>
                <span class="row-value">
            </div>
            <div class="row-item">
                <span class="column-name">Цена:</span>
                <span class="row-value">${motorcycle.price} ₽</span>
            </div>
        `;

        // Добавляем строку в тело таблицы
        tableBody.appendChild(tableRow);
    });
}


// Запуск загрузки данных при загрузке страницы
document.addEventListener('DOMContentLoaded', loadMotorcycles);
document.getElementById('profile-icon').addEventListener('click', async function () {
    // Перенаправление на страницу профиля
    window.location.href = '/profile';
});
