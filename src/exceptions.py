from fastapi import status, HTTPException

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден"
)

UserNotActiveException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пользователь не активирован"
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"
)

PasswordMismatchException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Пароли не совпадают"
)

EmailNotVerifiedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Почта не подтверждена"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек"
)

TokenNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен не найден"
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен не валидный"
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен не предоставлен"
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не найден ID пользователя"
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Недостаточно прав"
)

MotoNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Мотоцикл не найден"
)

MotoOutOfStockException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Мотоцикл отсутствует на складе"
)

MotoAlreadyInBasketException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Мотоцикл уже добавлен в корзину"
)

MotoNotInBasketException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Мотоцикл не найден в корзине"
)

BasketNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Корзина не найдена"
)

BasketEmptyException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Корзина пуста"
)

ItemAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Элемент уже добавлен в корзину"
)

ItemNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Элемент не найден в корзине"
)

OrderNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Заказ не найден"
)

OrderAlreadyProcessedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Заказ уже обработан"
)

OrderPaymentFailedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка оплаты заказа"
)

OrderCancellationException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Невозможно отменить заказ"
)

PaymentFailedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Оплата не прошла"
)

PaymentAlreadyProcessedException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Оплата уже обработана"
)

InvalidPaymentDataException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверные данные для оплаты"
)

DeliveryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Доставка не найдена"
)

DeliveryAlreadyProcessedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Доставка уже обработана"
)

InvalidDeliveryAddressException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверный адрес доставки"
)

DatabaseConnectionException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка подключения к базе данных"
)

InternalServerErrorException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Внутренняя ошибка сервера"
)

ValidationErrorException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка валидации данных"
)

InvalidRequestException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверный запрос"
)

# Ошибки, связанные с двигателями
EngineAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Двигатель с таким номером уже существует"
)

EngineNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Двигатель не найден"
)

# Ошибки, связанные с мотоциклами
MotoAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Мотоцикл с таким номером рамы уже существует"
)

# Ошибки, связанные с обновлением и удалением
NoRecordsFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Записи для обновления или удаления не найдены"
)

ImpossibleTransitionException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Текущий переход невозможен"
)
