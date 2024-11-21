// Функции для управления загрузкой
function showLoading() {
    document.getElementById("loading").style.display = "block";  // Общий загрузчик страницы
}

function hideLoading() {
    document.getElementById("loading").style.display = "none";  // Скрыть общий загрузчик страницы
}

function showOrdersLoading() {
    document.getElementById("orders-loading").style.display = "block";  // Загрузчик для заказов
    document.getElementById("orders-content").style.display = "none";  // Скрыть заказы
}

function hideOrdersLoading() {
    document.getElementById("orders-loading").style.display = "none";  // Скрыть загрузчик для заказов
    document.getElementById("orders-content").style.display = "block";  // Показать заказы
}

// Функция для загрузки профиля
async function loadProfile() {
    try {
        showLoading();
        const response = await fetch('/auth/me/');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке данных');
        }
        const profile = await response.json();
        console.log('Профиль загружен:', profile);

        // Показать секцию для заполнения (если она скрыта)
        const userInfoSection = document.getElementById('userInfo');
        if (userInfoSection) {
            userInfoSection.style.display = 'block'; // Показать секцию
        }

        renderProfile(profile);

        // Скрыть секцию обратно, если нужно
        if (userInfoSection) {
            userInfoSection.style.display = 'none';
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        console.error('Ошибка:', error);
        document.getElementById('profile-content').innerHTML = '<p>Не удалось загрузить данные</p>';
    }
}

// Рендеринг данных профиля
function renderProfile(profile) {
    // Элементы профиля
    const name = document.getElementById('name');
    const lastName = document.getElementById('last_name');
    const patronymic = document.getElementById('patronymic');
    const email = document.getElementById('profile-email');
    const phone = document.getElementById('profile-phone');
    console.log(name);
    // Проверяем существование элементов перед записью значений
    name.value = profile.username || '';
    if (lastName) lastName.value = profile.last_name || 'Пусто';
    if (patronymic) patronymic.value = profile.patronymic || 'Пусто';
    if (email) email.textContent = `Email: ${profile.email || 'Не указан'}`;
    if (phone) phone.textContent = `Телефон: ${profile.phone_num || 'Не указан'}`;
}

// Функция для загрузки заказов
async function loadOrders() {
    try {
        showOrdersLoading();
        const response = await fetch('/auth/orders/');  // Путь для получения данных о заказах
        if (!response.ok) {
            throw new Error('Ошибка при загрузке заказов');
        }
        const orders = await response.json();
        console.log('Заказы загружены:', orders);

        renderOrders(orders);
        hideOrdersLoading();
    } catch (error) {
        hideOrdersLoading();
        console.error('Ошибка:', error);
        document.getElementById('orders-content').innerHTML = '<p>Не удалось загрузить заказы</p>';
    }
}

// Рендеринг данных заказов
function renderOrders(orders) {
    const ordersContainer = document.getElementById('orders-content');
    ordersContainer.innerHTML = ''; // Очистить текущие заказы перед рендерингом

    orders.forEach(order => {
        const orderItem = document.createElement('div');
        orderItem.classList.add('order-item');
        orderItem.innerHTML = `
            <img src="${order.imageUrl}" alt="${order.name}" class="order-image">
            <div class="order-info">
                <h3>${order.name}</h3>
                <p>Дата заказа: ${order.date}</p>
                <p>Статус: ${order.status}</p>
            </div>
        `;
        ordersContainer.appendChild(orderItem);
    });
}

// Функция для показа и скрытия секций
function showSection(sectionId) {
    // Скрыть все секции
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
        section.classList.remove('active');
    });

    // Показать выбранную секцию
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
        selectedSection.classList.add('active');
    }
}

// Инициализация на загрузке DOM
document.addEventListener('DOMContentLoaded', async () => {
    // Загрузка профиля при загрузке страницы
    await loadProfile();

    // Показать секцию информации о пользователе по умолчанию
    showSection('userInfo');

    // Обработчик нажатия на кнопку "Профиль"
    document.getElementById('profile-user-button').addEventListener('click', () => {
        showSection('userInfo');  // Показываем секцию профиля
    });

    // Обработчик нажатия на кнопку "Заказы"
    document.getElementById('order-info-button').addEventListener('click', async () => {
        showSection('profile-orders');  // Показываем секцию заказов
        await loadOrders();  // Загружаем данные заказов
    });
});
