window.onload = function() {
    const owner = getOwner();
    const owner_name = owner.name;
    document.getElementById("ownerName").innerHTML = owner_name;

    attachSignOut();
}

const url_string = window.location.href;
const url = new URL(url_string)
const rest_id = url.searchParams.get("id");


axios.get('http://localhost/restaurant/' + rest_id).then(responseRestDetails => {
        var html_dis = ``;
        var RestDetails = responseRestDetails.data.data;
        console.log(RestDetails);
        console.log(RestDetails.name)
        console.log(RestDetails.is_open)
        var switchStatus = RestDetails.is_open

        var toggleSwitch = `<input type="checkbox" id="isopen" value="true" name="Is Open">`;
        if (switchStatus == true){
            toggleSwitch = `<input type="checkbox" id="isopen" value="true" name="Is Open" checked>`;
        }
        html_dis +=`
        <section class="contact-clean">
        <h3 class="text-dark mb-1" style="text-align: center;font-family: Timmana, sans-serif;">Update Restaurant Details Here</h3>
        <form id="updateForm">
            <div class="form-group">Name <br><input class="form-control" type="text" id="resName" name="name" placeholder="${RestDetails.name}" value = "${RestDetails.name}"></div>
            <div class="form-group">Is Restaurant Open<label style="margin-left: 20px;" class="switch">${toggleSwitch}<div class="slider round"></div></label></div>
            <div class="form-group">Address <br>
            <input class="form-control" id="resAddress" name="address" placeholder="${RestDetails.address}" rows="14" value = "${RestDetails.address}"></div>
            <div class="container">
            <div class="form-group"><button onclick="location.href='Home.html'" class="btn btn-primary" id="backBtn" style="background: rgb(6,51,184);">Back</button>
            <button class="btn btn-primary" style="background: rgb(6,51,184);display:inline-block; float:right;" id="updateBtn" >Update</button>
            </div>
        </form>
        </section>`; 
        
        document.getElementById("restDetails").innerHTML = html_dis;

        const form = document.getElementById("updateForm")
        form.addEventListener('submit', function() {
            event.preventDefault();
        });

        var switchStatus = RestDetails.is_open;
        $("#isopen").on('change', function() {
            if ($(this).is(':checked')) {
                switchStatus = $(this).is(':checked');
            }
            else {
               switchStatus = $(this).is(':checked');
            }
        });
        console.log(switchStatus)

        const updateBtn =document.getElementById("updateBtn")
            updateBtn.addEventListener('click', function() {
            const name = document.querySelector('#resName').value;
            const is_open = switchStatus
            const address = document.querySelector('#resAddress').value;
            console.log(is_open)

            const resInfo = {"name": name, "is_open": is_open, "address": address};
            
            console.log(rest_id);
            axios.put('http://localhost/restaurant/' + rest_id, json=resInfo)
            .then(response => {
                const updatedRes = response.data;
                console.log(`PUT: Restaurant is changed`, updatedRes);
                window.location.href = "home.html";
            })
            .catch(error => console.error(error));

            console.log(resInfo)
    })
   })
