
async function loginWithGitHub() {
    window.location.href = "http://localhost:80/api/oauth/github-oauth/login";
}

async function getCurrentUser() {
    var userInfo = document.getElementById('user-info');
    const response = await fetch('http://localhost:80/api/oauth/cookie/me/', {
        method: 'POST',
        credentials: 'include'
    });
    if (response.ok) {
            const userData = await response.json();
            const user = userData[0];
            const { login, id, avatar_url } = user;

            var img = document.createElement('img');
            img.src = `${avatar_url}`;
            img.alt = 'Фото профиля';
            
            userInfo.innerText = `${login}`
            userInfo.appendChild(img)
        } 
    else {
        userInfo.innerText = 'User not logged in';
    }
}

async function logout() {
    var userInfo = document.getElementById('user-info');
    const me_response = await fetch('http://localhost:80/api/oauth/cookie/me/', {
        method: 'POST',
        credentials: 'include'
    });
    if (!me_response.ok) {
        userInfo.innerText = 'User not logged in!'
    } else {
        const response = await fetch('http://localhost:80/api/oauth/cookie/logout/', {
        method: 'POST',
        credentials: 'include'
    });
    if (response.ok) {
        userInfo.innerText = 'You have logged out!';
    }
    }
}

window.onload = getCurrentUser;