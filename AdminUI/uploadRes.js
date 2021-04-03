//Upload Restaurant 
const createRes = (resInfo) => {
    // RMB to change the oid variable 
    axios.post('http://localhost/create_restaurant/1', resInfo)
        .then(response => {
            const addedRes = response.data;
            console.log(`POST: Restaurant is added`, addedRes);
        })
        .catch(error => console.error(error));
};

var switchStatus = false;
$("#isopen").on('change', function() {
    if ($(this).is(':checked')) {
        switchStatus = $(this).is(':checked');
        // alert(switchStatus);// To verify
    }
    else {
       switchStatus = $(this).is(':checked');
    //    alert(switchStatus);// To verify
    }
});
console.log(switchStatus)
const form = document.querySelectorAll('form')[1];

const formEvent = form.addEventListener('submit', event => {
    event.preventDefault();
    const name = document.querySelector('#resName').value;
    const is_open = switchStatus
    const address = document.querySelector('#resAddress').value;
    console.log(is_open)

    const resInfo = {name, is_open , address};
    createRes(resInfo);
    console.log(resInfo)
});


