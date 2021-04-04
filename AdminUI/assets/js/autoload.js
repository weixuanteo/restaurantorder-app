// Autoload.js - Javascript file that contains utility functions

const owner = localStorage.getItem("owner");
if (!owner) {
    window.location.href = "login.html";
}

function getOwner() {
    const owner = JSON.parse(localStorage.getItem("owner"));
    return owner;
}

function signOut() {
    localStorage.removeItem("owner");
    window.location.href = "login.html";
}

function attachSignOut() {
    const logoutBtn = document.getElementById("logoutBtn");
    logoutBtn.addEventListener("click", function() {
        signOut();
    })
}