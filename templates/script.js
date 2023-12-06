const BASE_URL = "https://banking-api-uy2e.onrender.com/api/v1";

async function requestData(username) {
    return fetch(`${BASE_URL}/banking/${username}`)
        .then((response) => response.json())
        .then((data) => displayData(data[username]))
        .catch((error) => console.log(error));
}

function displayData(data) {
    // const usernameElement = document.getElementById("username")
    console.log(data);
    const emailElement = document.getElementById("email");
    const passwordElement = document.getElementById("password");
    // usernameElement = data[1];
    emailElement.innerText = data[2];
    passwordElement.innerText = data[3];
}

// On page load, get the logged-in user's username and display user info
window.onload = function () {
    // Replace 'username' with the actual username of the logged-in user
    const loggedInUsername = 'larske07';
    requestData(loggedInUsername);
};