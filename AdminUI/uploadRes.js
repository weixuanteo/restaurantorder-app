//Upload Res
const createRes = (resInfo) => {
    axios.post('http://localhost/restaurant', resInfo)
        .then(response => {
            const addedRes = response.data;
            console.log(`POST: Restaurant is added`, addedRes);
        })
        .catch(error => console.error(error));
};

const form = document.querySelectorAll('form')[1];

const formEvent = form.addEventListener('submit', event => {
    event.preventDefault();

    const name = document.querySelector('#resName').value;
    const is_open = document.querySelector('#isopen').value;
    const address = document.querySelector('#resAddress').value;

    const resInfo = { name, is_open , address};
    createRes(resInfo);
    console.log(resInfo)
});
