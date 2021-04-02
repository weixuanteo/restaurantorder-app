//Register Account
const createAccount = (account) => {
    axios.post('http://localhost/owner/registration', account)
        .then(response => {
            const addAccount = response.data;
            console.log(`POST: user is added`, addAccount);
            window.location.href = "login.html";
        })
        .catch(error => console.error(error));
};

const form = document.querySelector('form');

const formEvent = form.addEventListener('submit', event => {
    event.preventDefault();

    const name = document.querySelector('#name').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    const cfmPassword = document.querySelector('#cfmPassword').value;
    let hasErrors = false;

    if (name == "" || email == "" || password == "" || cfmPassword == "" || password != cfmPassword) {
        hasErrors = true;
    }

    if (hasErrors) {
        const alertBanner = document.querySelector('#errorMessage');
        alertBanner.classList.remove('hideElement');
        alertBanner.classList.add('showElement');
        hasErrors = false;
        return;
    }

    const account = { name, email , password};
    createAccount(account);
});