const url_string = window.location.href;
const url = new URL(url_string)
const rest_id = url.searchParams.get("id");


axios.get('http://localhost/restaurant/' + rest_id).then(responseRestDetails => {
        var html_dis = ``;
        var RestDetails = responseRestDetails.data.data;
        console.log(RestDetails);
        console.log(RestDetails.name)
        switchStatus = RestDetails.is_open


        html_dis +=`
        <section class="contact-clean">
        <h3 class="text-dark mb-1" style="text-align: center;font-family: Timmana, sans-serif;">Upload Restaurant Details Here</h3>
        <form >
            <div class="form-group">Name <br><input class="form-control" type="text" id="resName" name="name" placeholder="${RestDetails.name}" value = "${RestDetails.name}"></div>
            <div class="form-group">Is Restaurant Open<label style="margin-left: 20px;" class="switch"><input type="checkbox" id="isopen" value="true" name="Is Open"><div class="slider round"></div></label></div>
            <div class="form-group"><label>Restaurant Image</label><input class="form-control-file" type="file"></div>
            <div class="form-group">Address <br><input class="form-control" id="resAddress" name="address" placeholder="${RestDetails.address}" rows="14" value = "${RestDetails.address}"></textarea></div>
            <div class="form-group"><button class="btn btn-primary" type="submit" style="background: rgb(6,51,184);">Update</button></div>
        </form>
        </section>`; 
        
            document.getElementById("restDetails").innerHTML = html_dis;
   })


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

const updateRes = (resInfo) => {
    // RMB to change the oid variable 
    axios.put('http://localhost/restaurant/1', resInfo)
        .then(response => {
            const updatedRes = response.data;
            console.log(`PUT: Restaurant is changed`, updatedRes);
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
    updateRes(resInfo);
    console.log(resInfo)
});
