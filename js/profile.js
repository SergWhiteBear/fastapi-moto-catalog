async function loadProfile() {
    try {
        const response = await fetch('/auth/me/')
        if (!response.ok) {
            throw new Error('Error')
        }
        const profile = await response.json()
        console.log(profile)
        await renderProfile(profile)
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('content').innerHTML = '<p>Не удалось загрузить данные</p>';
    }
}

async function renderProfile(profile) {
    const content = document.getElementById('profile-content')
    const profileCard = document.createElement('div')
    profileCard.className = 'profile-card'
    profileCard.innerHTML = `
    <div class="profile-info">
        <img src="https://via.placeholder.com/150" alt="Аватар" class="profile-avatar">
        <div class="profile-name"> ${profile.username}</div>
        <div class="profile-email">Email: ${profile.email}</div>
        <div class="profile-phone">Номер: ${profile.phone_num}</div>
    </div>
    `;
    content.appendChild(profileCard)
}

document.addEventListener('DOMContentLoaded', loadProfile)