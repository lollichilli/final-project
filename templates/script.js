const BASE_URL = "https://banking-api-uy2e.onrender.com/api/v1/banking";

async function requestUserData(username) {
    return fetch(`${BASE_URL}/${username}`)
        .then(response => response.json())
        .catch(error => console.log(error));
}

function displayData(data, username) {
    const usernameElement = document.getElementById("username");
    const emailElement = document.getElementById("email");
    usernameElement.innerHTML = username;
    emailElement.innerText = data[username][2];
}

// Redirect user
function redirect(url) {
    window.location.href = url;
}

// Try to log the user in
// If successful save user in local storage
async function login() {
    let username = document.querySelector("input[name='username']").value;
    let password = document.querySelector("input[name='password']").value;

    let userData = await requestUserData(username);
    // If the user exists and the password is correct then continue
    if (userData && password == userData[username][3]) {
        sessionStorage.setItem('username', username);
        console.log('redirecting...')
        redirect("index.html");
    } else {
        pswdMsg = document.getElementById("msg");
        pswdMsg.innerText = "Incorrect Username/Password";
    }
}

// On page load, get the logged-in user's username and display user info
 window.onload = async function () {

    // Get the relative url
    var pathname = window.location.pathname;
    console.log(pathname);

    // Onload behavior is different depending on path
    switch(pathname) {
        case "/templates/index.html" :
            // Get the username from session
            let username = sessionStorage.getItem("username");
            username = username ? username : redirect("login.html");

            // Display the user info
            userData = await requestUserData(username);
            displayData(userData, username);
            break;

        case "/templates/login.html" :
            break;
    }
};