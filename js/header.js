async function openModal() {
    const modal = document.getElementById("modal");
    modal.classList.add("active");
}

async function closeModal() {
    const modal = document.getElementById("modal");
    modal.classList.remove("active");
}

async function switchForm(formId) {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const recoveryForm = document.getElementById("recovery-form")

    if (formId === 'register-form') {
        loginForm.classList.remove("active");
        recoveryForm.classList.remove("active")
        registerForm.classList.add("active");
    } else {
        if (formId === 'recovery-form') {
            loginForm.classList.remove("active");
            registerForm.classList.remove("active")
            recoveryForm.classList.add("active");
        } else {
            recoveryForm.classList.remove("active")
            registerForm.classList.remove("active");
            loginForm.classList.add("active");
        }
    }
}

async function showProfileButton() {
    const profileIcon = document.getElementById('profile-icon');
    const logoutIcon = document.getElementById('logout-icon');
    const loginIcon = document.getElementById('login-icon');
    profileIcon.style.display = 'inline-block'; // Показываем кнопку
    logoutIcon.style.display = 'inline-block';
    loginIcon.style.display = 'none'
}

async function hideProfileButton() {
    const profileIcon = document.getElementById('profile-icon');
    const logoutIcon = document.getElementById('logout-icon');
    const loginIcon = document.getElementById('login-icon');
    profileIcon.style.display = 'none'; // Скрываем кнопку
    logoutIcon.style.display = 'none';
    loginIcon.style.display = 'inline-block';

}



async function checkStatus() {
    try {
        const response = await fetch('/auth/me/', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.ok) {
            await showProfileButton()
        } else {
            await hideProfileButton
        }
    } catch (error) {
        console.error('Ошибка при проверке авторизации:', error);
        await hideProfileButton();
    }
}

function displayErrors(errorData) {
    let message = 'Произошла ошибка';

    if (errorData && errorData.detail) {
        if (Array.isArray(errorData.detail)) {
            // Обработка массива ошибок
            message = errorData.detail.map(error => {
                if (error.type === 'string_too_short') {
                    return `Поле "${error.loc[1]}" должно содержать минимум ${error.ctx.min_length} символов.`;
                }
                return error.msg || 'Произошла ошибка';
            }).join('\n');
        } else {
            // Обработка одиночной ошибки
            message = errorData.detail || 'Произошла ошибка';
        }
    }

    // Отображение сообщения об ошибке
    alert(message);
}


async function loginFunction(event) {
    event.preventDefault(); // Останавливаем стандартное поведение формы

    // Сбор данных из формы
    const form = document.getElementById("login-form")
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        if (!response.ok) {
            const errorData = await response.json()
            displayErrors(errorData);
            return;
        }

        const result = await response.json();

        if (result.message) {
            await checkStatus()
            await closeModal()
        } else {
            alert(result.message || 'Неизвестная ошибка')
        }
    } catch (error) {
        console.error('Ошибка:', error)
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.')
    }
}

async function registerFunction(event) {
    event.preventDefault(); // Останавливаем стандартное поведение формы

    // Сбор данных из формы
    const form = document.getElementById("register-form")
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        if (!response.ok) {
            const errorData = await response.json()
            displayErrors(errorData);
            return;
        }

        const result = await response.json();

        if (result.message) {
            await switchForm("login-form")
        } else {
            alert(result.message || 'Неизвестная ошибка')
        }
    } catch (error) {
        console.error('Ошибка:', error)
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.')
    }
}

async function recoveryFunction(event) {
    return;
}

async function logout() {
    try {
        await fetch('/auth/logout/', {
            method: 'POST',
            credentials: 'include'
        })
        await hideProfileButton()
    } catch (error) {
        console.error('Ошибка при выходе из системы:', error);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
   await checkStatus()
});

document.getElementById('logout-icon').addEventListener('click', async function () {
    await logout()
})