//Register Account
const createAccount = (account) => {
    axios.post('http://localhost/owner/registration', account)
        .then(response => {
            const addAccount = response.data;
            console.log(`POST: user is added`, addAccount);
            
        })
        .catch(error => console.error(error));
};

const form = document.querySelector('form');

const formEvent = form.addEventListener('submit', event => {
    event.preventDefault();

    const name = document.querySelector('#name').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;

    const account = { name, email , password};
    createAccount(account);
});