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


function displayMotoDetails(moto) {
    const motoDetailsContainer = document.getElementById('moto-details');

    // Создаем элемент img для изображения мотоцикла
    const img = document.createElement('img');
    img.src = moto.url_image || 'https://via.placeholder.com/300';  // Если URL изображения не указан
    img.alt = moto.name || 'Мотоцикл';
    img.classList.add('moto-detail-image');
    motoDetailsContainer.appendChild(img);

    // Создаем элемент h1 для названия мотоцикла
    const title = document.createElement('h1');
    title.textContent = moto.name || 'Название не указано';
    title.classList.add('moto-detail-title');
    motoDetailsContainer.appendChild(title);

    // Создаем элемент p для цены мотоцикла
    const price = document.createElement('p');
    price.textContent = moto.price ? `${moto.price} ₽` : 'Цена не указана';
    price.classList.add('moto-detail-price');
    motoDetailsContainer.appendChild(price);

    // Создаем контейнер для детальной информации о мотоцикле
    const infoContainer = document.createElement('div');
    infoContainer.classList.add('moto-detail-info');

    // Информация о классе мотоцикла
    const motoClass = document.createElement('p');
    motoClass.innerHTML = `<strong>Класс мотоцикла:</strong> ${moto.moto_class || 'Не указано'}`;
    infoContainer.appendChild(motoClass);

    // Информация о двигателе
    const engine = document.createElement('p');
    engine.innerHTML = `<strong>Двигатель:</strong> ${moto.engine || 'Не указано'}`;
    infoContainer.appendChild(engine);

    // Описание мотоцикла
    const description = document.createElement('p');
    description.innerHTML = `<strong>Описание:</strong> ${moto.comments || 'Описание отсутствует'}`;
    infoContainer.appendChild(description);

    motoDetailsContainer.appendChild(infoContainer);

    // Создаем кнопку для добавления мотоцикла в корзину
    const addButton = document.createElement('button');
    addButton.textContent = 'Добавить в корзину';
    addButton.classList.add('add-to-cart-button');
    addButton.addEventListener('click', () => {
        // Логика для добавления товара в корзину
        addToCart(moto);
    });
    motoDetailsContainer.appendChild(addButton);
}

displayMotoDetails(fetchMotos(1));


