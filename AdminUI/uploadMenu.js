//Upload Res
const createMenu = (menuInfo) => {
    axios.post('http://localhost/restaurant/1/item', menuInfo)
        .then(response => {
            const addedMenu = response.data;
            console.log(`POST: Menu is added`, addedMenu);
        })
        .catch(error => console.error(error));
};

const form = document.querySelectorAll('form')[1];

const formEvent = form.addEventListener('submit', event => {
    event.preventDefault();
    const itemname = document.querySelector('#foodname').value;
    const foodprice = document.querySelector('#foodprice').value;
    const foodcategory = document.querySelector('#foodcategory').value;
    const description = document.querySelector('#description').value;
    const img_url = "fake";


    const menuInfo = {"name" : itemname, "price" : foodprice, "description":description,"category":foodcategory,"img_url":img_url};
    createMenu(menuInfo);
    console.log(menuInfo)
});
