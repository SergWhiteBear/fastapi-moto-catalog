const tg = window.Telegram.WebApp;
tg.expand();

// Переменная для хранения количества товаров в корзине
let cartCount = 0;

// Функция для обновления количества товаров в корзине
function updateCartCount() {
    const cartBadge = document.getElementById('cart-count');
    if (cartCount > 0) {
        cartBadge.textContent = cartCount;
        cartBadge.style.display = 'block'; // Показываем кружок, если количество больше 0
    } else {
        cartBadge.style.display = 'none'; // Скрываем кружок, если товаров нет
    }
}

// Функция для добавления товара в корзину
function addToCart() {
    cartCount++;
    updateCartCount();
}

function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' ₽';
}

// Функция для получения данных с сервера
function fetchMotos() {
    fetch("http://localhost:8000/moto/get_all")
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            displayMotos(data);
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных:', error);
        });
}

// Функция для отображения мотоциклов
function displayMotos(motos) {
    const catalog = document.getElementById('catalog');

    if (motos.length === 0) {
        catalog.innerHTML = '<p>Мотоциклы не найдены.</p>';
        return;
    }

    motos.forEach(moto => {
        const motoCard = document.createElement('div');
        motoCard.classList.add('moto-card');

        // Создаем контейнер для изображения
        const imageContainer = document.createElement('div');
        imageContainer.classList.add('image-container'); // Добавляем класс для контейнера

        const img = document.createElement('img');
        img.src = moto.url_image || 'https://via.placeholder.com/300'; // Если URL отсутствует
        img.alt = moto.name || 'Мотоцикл';
        img.classList.add('moto-image');

        imageContainer.appendChild(img);
        motoCard.appendChild(imageContainer);

        const title = document.createElement('h2');
        title.textContent = moto.name || 'Название не указано';
        title.classList.add('moto-title');
        motoCard.appendChild(title);

        const description = document.createElement('p');
        description.textContent = moto.comments || 'Описание отсутствует';
        description.classList.add('moto-description');
        motoCard.appendChild(description);

        const price = document.createElement('p');
        price.textContent = moto.price ? `Цена: ${formatPrice(moto.price)}` : 'Цена не указана';
        price.classList.add('moto-price');
        motoCard.appendChild(price);

        const motoClass = document.createElement('p');
        motoClass.textContent = `Класс: ${moto.moto_class}`;
        motoClass.classList.add('moto-class');
        motoCard.appendChild(motoClass);

        const engine = document.createElement('p');
        engine.textContent = `Двигатель: ${moto.engine}`;
        engine.classList.add('moto-engine');
        motoCard.appendChild(engine);

        const addButton = document.createElement('button');
        addButton.textContent = 'Добавить в корзину';
        addButton.classList.add('add-to-cart-button');
        addButton.addEventListener('click', addToCart);
        motoCard.appendChild(addButton);

        // Добавляем событие клика на всю карточку
        motoCard.addEventListener('click', () => {
            window.location.href = `/about/${moto.id}`; // Перенаправляем на страницу с описанием
        });

        catalog.appendChild(motoCard);
    });
}

// Вызов функции для получения данных при загрузке страницы
document.addEventListener('DOMContentLoaded', fetchMotos);
