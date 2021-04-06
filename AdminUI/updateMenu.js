window.onload = function() {
    const owner = getOwner();
    const owner_name = owner.name;
    document.getElementById("ownerName").innerHTML = owner_name;

    attachSignOut();
}


const url_string = window.location.href;
const url = new URL(url_string)
const rest_id = url.searchParams.get("rest_id");
const item_id = url.searchParams.get("id");

console.log(rest_id)
console.log(item_id)

axios.get('http://localhost/restaurant/item/' + item_id).then(response => {
    var itemDetails = response.data.data;
    console.log(itemDetails);
    var html_list = ``;

    html_list =` 
    <section class="contact-clean">                       
    <h3 class="text-dark mb-1" style="text-align: center;font-family: Timmana, sans-serif;">Update Menu Here</h3>
    <form id="updateForm">
        <div class="form-group">Food Name<br><input class="form-control" type="text" id="foodname" name="name"  value="${itemDetails.name}"></div>
        <div class="form-group">Price <br><input type="text" class="form-control" id="foodprice" value="${itemDetails.price}"/></div>
        <div class="form-group">Category <br><input type="text" class="form-control" id="foodcategory" value="${itemDetails.category}"/></div>
        <div class="form-group">Description<br><input class="form-control" name="description" id= "description" value="${itemDetails.description}" rows="14"></textarea></div>
        <div class="container">
        <div class="form-group"><button onclick="location.href='individualRes.html?id=${rest_id}'" class="btn btn-primary" id="backBtn" style="background: rgb(6,51,184);">Back</button>
        <button class="btn btn-primary" style="background: rgb(6,51,184);display:inline-block; float:right;" id="updateBtn" >Update</button>
        </div>
    </form>
    </section>`;

    document.getElementById("itemDetails").innerHTML = html_list;

    const form = document.getElementById("updateForm")
    form.addEventListener('submit', function() {
        event.preventDefault();
    });

    const updateBtn =document.getElementById("updateBtn")
        updateBtn.addEventListener('click', function() {
        const name = document.querySelector('#foodname').value;
        const price = document.querySelector('#foodprice').value;
        const category = document.querySelector('#foodcategory').value;
        const description = document.querySelector('#description').value;
        const resInfo = {"name": name, "price": price, "category": category,"description":description};
        
        console.log(item_id);
        axios.put('http://localhost/restaurant/item/' + item_id, json=resInfo)
        .then(response => {
            const updatedRes = response.data;
            console.log(`PUT: Item is changed`, updatedRes);
            window.location.href = "individualRes.html?id="+rest_id;
        })
        .catch(error => console.error(error));

        console.log(resInfo)
})

})


