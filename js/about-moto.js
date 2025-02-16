// Извлечение параметров из URL
function getUrlParams() {
    const path = window.location.pathname;
    const segments = path.split('/');
    return {
        id: segments[segments.length - 1]
    };
}


// Рендеринг минимальных данных
function renderMinimalDetails() {
    const {id} = getUrlParams();
    const pageContent = document.getElementById('page-content');
    pageContent.innerHTML = `
        <h1>${name}</h1>
    `;
    return id; // Вернуть id для подгрузки данных
}

// Загрузка полных данных о мотоцикле с сервера
async function fetchMotorcycleDetails(id) {
    const response = await fetch(`/moto/get_moto/${id}`);
    if (!response.ok) {
        throw new Error('Ошибка загрузки данных');
    }
    return response.json();
}

// Рендеринг полной информации
function renderFullDetails(details) {
    const pageContent = document.getElementById('page-content')


    pageContent.innerHTML = `
        <div class="slider-container">
          <div class="slider">
            <div class="slider-track"></div>
          </div>
            <div class="slider-controls">
                <button class="prev" disabled></button>
                <button class="next"></button>
            </div>
       </div>
       <div class="details-container">
        <div class="details">
            <!-- Данные о товаре будут здесь -->
        </div>
        <div class="shop-container">
            <!-- Данные о покупке -->
            <button class="add-cart" ></button>
        </div>
        </div>
        
    `

    const detailsContainer = pageContent.querySelector('.details-container');
    console.log(detailsContainer)
    if (!detailsContainer) {
        console.error("Элемент 'details-container' не найден в DOM");
        return;
    }

    detailsContainer.querySelector('.details').innerHTML = `
        <h1>${details.name}</h1>
        <p>Цена: ${details.price} ₽</p>
        <p>Класс: ${details.moto_class}</p>
        <p>Год выпуска: ${details.year}</p>
        <p>Объем двигателя: ${details.engine_capacity} см³</p>
        <p>Пробег: ${details.mileage} км</p>
        <p>Состояние: ${details.condition}</p>
        <p>Комментарии: ${details.comments}</p>
    `;

    const sliderTrack = pageContent.querySelector('.slider-track');
    const slider = pageContent.querySelector('.slider');
    const prev = pageContent.querySelector('.prev');
    const next = pageContent.querySelector('.next');

    if (!sliderTrack || !slider || !prev || !next) {
        console.error("Не все элементы слайдера были найдены в DOM");
        return;
    }

    sliderTrack.innerHTML = '';


    // Добавляем изображения в .slider-track
    details.image_url.forEach((url, index) => {
        const slideContainer = document.createElement('div');
        slideContainer.classList.add('slide');

        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('slide-img');

        slideContainer.appendChild(img);
        sliderTrack.appendChild(slideContainer);
    });

    // Добавляем информацию о детали


    // Вычисляем ширину одного слайда
    const slideWidth = slider.offsetWidth;

    // Событие прокрутки для управления кнопками
    slider.addEventListener('scroll', () => {
        const scrollLeft = slider.scrollLeft;
        const maxScrollLeft = slider.scrollWidth - slider.offsetWidth;

        prev.disabled = scrollLeft === 0;
        next.disabled = scrollLeft === maxScrollLeft;
    });

    // Управление кнопками
    next.addEventListener('click', () => {
        slider.scrollBy({ left: slideWidth, behavior: 'smooth' });
    });

    prev.addEventListener('click', () => {
        slider.scrollBy({ left: -slideWidth, behavior: 'smooth' });
    });

    // Обработка тач-скроллинга
    let startX = 0;
    let isDragging = false;

    slider.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
        slider.style.scrollSnapType = 'none'; // Отключаем snap, чтобы можно было плавно скролить
    });

    slider.addEventListener('touchmove', (e) => {
        if (!isDragging) return;

        const moveX = startX - e.touches[0].clientX;
        if (Math.abs(moveX) > slideWidth * 0.6) {
            if (moveX > 0) {
                slider.scrollBy({ left: slideWidth, behavior: 'smooth' }); // Сдвиг влево
            } else {
                slider.scrollBy({ left: -slideWidth, behavior: 'smooth' }); // Сдвиг вправо
            }
            startX = e.touches[0].clientX; // Обновляем начальную точку
        }
    });

    slider.addEventListener('touchend', () => {
        isDragging = false;
        slider.style.scrollSnapType = 'x mandatory'; // Включаем snap для нормальной прокрутки
    });

    // Устанавливаем начальное состояние кнопок
    prev.disabled = true;
    next.disabled = slider.scrollWidth <= slider.offsetWidth;
}



// Управление загрузкой данных
async function loadDetailsPage() {
    const id = renderMinimalDetails(); // Отрисовать минимальные данные
    document.getElementById('loading').style.display = 'block';
    try {
        const fullDetails = await fetchMotorcycleDetails(id);
        renderFullDetails(fullDetails);
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        document.getElementById('details-container').innerHTML += '<p>Не удалось загрузить дополнительные данные</p>';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}


// Запуск загрузки при загрузке страницы
document.addEventListener('DOMContentLoaded', loadDetailsPage);


