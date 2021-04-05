const url_string = window.location.href;
const url = new URL(url_string)
const rest_id = url.searchParams.get("id");

const createMenu = (menuInfo) => {
    axios.post('http://localhost/restaurant/' + rest_id + '/item', menuInfo)
        .then(response => {
            const addedMenu = response.data;
            console.log(`POST: Menu is added`, addedMenu);
            window.location.href = "IndividualRes.html?id=" + rest_id;
        })
        .catch(error => console.error(error));
};

const form = document.getElementById('menuForm');

const formEvent = form.addEventListener('submit', event => {
    event.preventDefault();
});

const uploadBtn = document.getElementById('uploadBtn');
uploadBtn.addEventListener('click', function() {
    const itemname = document.querySelector('#foodname').value;
    const foodprice = document.querySelector('#foodprice').value;
    const foodcategory = document.querySelector('#foodcategory').value;
    const description = document.querySelector('#description').value;
    const img_url = "fake";


    const menuInfo = {name: itemname, price: foodprice, description: description, category: foodcategory, img_url: img_url};
    createMenu(menuInfo);
    console.log(menuInfo)

    setTimeout(function() {
        window.location.href = "IndividualRes.html?id" + rest_id
    }, 1000)
});