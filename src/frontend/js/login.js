
async function loginWithGitHub() {
    window.location.href = "http://yourhost.example/api/oauth/github-oauth/login";
}

async function getCurrentUser() {
    var userInfo = document.getElementById('user-info');
    const response1 = await fetch('http://yourhost.example/api/oauth/cookie/me', {
        method: 'POST',
        credentials: 'include'
    });
    if (response1.ok) {
            const userData = await response1.json();
            const user = userData[0];
            const { login, id, avatar_url } = user;

            var img = document.createElement('img');
            img.src = `${avatar_url}`;
            img.alt = 'Фото профиля';
            img.style.width = '100px';
            img.style.height = '100px';
            img.style.border = '2px solid #ccc';
            img.style.objectFit = 'cover';
            
            userInfo.innerText = `${login}`
            userInfo.appendChild(img)
        } 
    else {
        userInfo.innerText = 'User not logged in';
    }
    const response2 = await fetch('http://yourhost.example/api/scraper/user/me', {
        method: 'POST',
        credentials: 'include'
    });
}

async function logout() {
    var userInfo = document.getElementById('user-info');
    const me_response = await fetch('http://yourhost.example/api/oauth/cookie/me', {
        method: 'POST',
        credentials: 'include'
    });
    if (!me_response.ok) {
        userInfo.innerText = 'User not logged in!'
    } else {
        const response = await fetch('http://yourhost.example/api/oauth/cookie/logout', {
        method: 'POST',
        credentials: 'include'
    });
    if (response.ok) {
        userInfo.innerText = 'You have logged out!';
    }
    }
}

window.onload = getCurrentUser;