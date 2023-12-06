const BASE_URL = "https://banking-api-uy2e.onrender.com/api/v1";

async function requestData(username) {
    return fetch(`${BASE_URL}/banking/${username}`)
        .then((response) => response.json())
        .then((data) => displayData(data[username]))
        .catch((error) => console.log(error));
}

function displayData(data) {
    const usernameElement = document.getElementById("username");
    const emailElement = document.getElementById("email");
    usernameElement.innerText = data[1];
    emailElement.innerText = data[2];
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


// On page load, get the logged-in user's username and display user info
window.onload = function () {
    // Replace 'username' with the actual username of the logged-in user
    const loggedInUsername = 'larske07';
    requestData(loggedInUsername);
    requestBalance(loggedInUsername);
    requestTransactionsTo(loggedInUsername);
    requestTransactionsFrom(loggedInUsername);
};
