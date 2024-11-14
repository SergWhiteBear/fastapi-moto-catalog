async function loadMotorcycles() {
    try {
        const response = await fetch('/moto/get_all_moto/'); // Укажите ваш URL API
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const motorcycles = await response.json();
        await renderMotorcycles(motorcycles);
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('content').innerHTML = '<p>Не удалось загрузить данные</p>';
    }
}



// Функция для рендеринга данных
async function renderMotorcycles(motorcycles) {
    const content = document.getElementById('content');
    content.innerHTML = ''; // Очистить содержимое перед добавлением новых данных
    motorcycles.forEach(motorcycle => {
        const motorcycleCard = document.createElement('div');
        motorcycleCard.className = 'motorcycle-card';

        motorcycleCard.innerHTML = `
            <div class="motorcycle-image">
                <img src="${motorcycle.image_url[0]}" alt="${motorcycle.name}">
            </div>
            <div class="motorcycle-info">
                <h2>${motorcycle.name}</h2>
                <p>Класс: ${motorcycle.moto_class}</p>
                <p>Цена: ${motorcycle.price.toLocaleString('ru-RU')} ₽</p>
                <p>Номер рамы: ${motorcycle.frame_num}</p>
                <p>Номер двигателя: ${motorcycle.engine_num}</p>
                <p>Комментарий: ${motorcycle.comments || 'Нет комментариев'}</p>
                <p>Дата обновления: ${new Date(motorcycle.updated_at).toLocaleDateString('ru-RU')}</p>
            </div>
        `;
        content.appendChild(motorcycleCard)
    });
}



// Запуск загрузки данных при загрузке страницы
document.addEventListener('DOMContentLoaded', loadMotorcycles);
document.getElementById('profile-icon').addEventListener('click', async function () {
    // Перенаправление на страницу профиля
    window.location.href = '/profile';
});