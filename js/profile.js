async function loadProfile() {
    try {
        const response = await fetch('/auth/me/');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке данных');
        }
        const profile = await response.json();
        console.log(profile);
        await renderProfile(profile);
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('profile-content').innerHTML = '<p>Не удалось загрузить данные</p>';
    }
}

function renderProfile(profile) {
    console.log(profile)
    const name = document.getElementById('name');
    const lastName = document.getElementById('last_name');
    const patronymic = document.getElementById('patronymic');
    const email = document.getElementById('profile-email');
    const phone = document.getElementById('profile-phone');
    const ordersContainer = document.getElementById('profile-orders');

    // Заполнение полей input значениями по умолчанию
    name.value = profile.username || '';
    lastName.value = profile.last_name || 'Пусто';
    patronymic.value = profile.patronymic || 'Пусто';
    email.textContent = `Email: ${profile.email || 'Не указан'}`
    phone.textContent = `Телефон: ${profile.phone_num || 'Не указан'}`

}

function showSection(sectionId) {
    // Скрыть все секции
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Показать выбранную секцию
    const selectedSection = document.getElementById(sectionId);
    selectedSection.classList.add('active');
}

document.addEventListener('DOMContentLoaded', loadProfile)

function updateFunction() {
    alert("Обновление")
}

document.getElementById('profile-user-button').addEventListener('click', () => {
    showSection('userInfo')
})
document.getElementById('order-info-button').addEventListener('click', () => {
    showSection('profile-orders')
})

// Показать секцию информации о пользователе по умолчанию
document.addEventListener('DOMContentLoaded', () => {
    showSection('userInfo');
});


let currentIndex = 0;

function slideOrders(direction) {
    const slider = document.getElementById('orders-slider');
    const items = document.querySelectorAll('.order-item');
    const totalItems = items.length;

    // Обновление текущего индекса
    currentIndex += direction;
    if (currentIndex < 0) {
        currentIndex = totalItems - 1;
    } else if (currentIndex >= totalItems) {
        currentIndex = 0;
    }

    // Сдвиг контейнера
    slider.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Поддержка свайпов
let startX = 0;

document.getElementById('orders-slider').addEventListener('touchstart', (event) => {
    startX = event.touches[0].clientX;
});

document.getElementById('orders-slider').addEventListener('touchend', (event) => {
    const endX = event.changedTouches[0].clientX;
    const diffX = startX - endX;

    if (diffX > 50) {
        slideOrders(1); // Свайп влево
    } else if (diffX < -50) {
        slideOrders(-1); // Свайп вправо
    }
});
