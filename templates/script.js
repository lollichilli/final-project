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

async function requestBalance(username) {
    return fetch(`${BASE_URL}/banking/${username}/balance`)
        .then((response) => response.json())
        .then((data) => displayBalance(data))
        .catch((error) => console.log(error));
}

function displayBalance(data) {
    const balanceElement = document.getElementById("balance");
    balanceElement.innerText = `$${data["Balance"]}`;
}

async function requestTransactionsTo(username) {
    return fetch(`${BASE_URL}/banking/${username}/transactionst`)
        .then((response) => response.json())
        .then((data) => displayTransTo(data["Transactions_t"]))
        .catch((error) => console.log(error));
}

function displayTransTo(data) {
    const transDate = document.getElementById("trans-to-date");
    transDate.innerText = data[0][1];
    const transFrom = document.getElementById("trans-to-from");
    transFrom.innerText = data[0][2];
    const transAmount = document.getElementById("trans-to-amount");
    transAmount.innerText = data[0][4];
}
async function requestTransactionsFrom(username) {
    return fetch(`${BASE_URL}/banking/${username}/transactionsf`)
        .then((response) => response.json())
        .then((data) => displayTransFrom(data["Transactions_f"]))
        .catch((error) => console.log(error));
}

function displayTransFrom(data) {
    const transDate = document.getElementById("trans-from-date");
    transDate.innerText = data[0][1];
    const transTo = document.getElementById("trans-from-to");
    transTo.innerText = data[0][3];
    const transAmount = document.getElementById("trans-from-amount");
    transAmount.innerText = data[0][4];
}

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
}
