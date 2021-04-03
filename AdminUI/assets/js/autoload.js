// Autoload.js - Javascript file that contains utility functions

const owner = localStorage.getItem("owner");
if (!owner) {
    window.location.href = "login.html";
}