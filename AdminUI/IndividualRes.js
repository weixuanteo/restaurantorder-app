window.onload = function() {
    const owner = getOwner();
    const owner_name = owner.name;
    document.getElementById("ownerName").innerHTML = owner_name;

    attachSignOut();
}

const url_string = window.location.href;
const url = new URL(url_string)
const rest_id = url.searchParams.get("id");


axios.get('http://localhost/restaurant/' + rest_id  + '/items').then(responseAllResItems => {
        var html_dis = ``;
        var allRestItems = responseAllResItems.data.data;
        console.log(allRestItems);
        for(var restItem in allRestItems){
            // console.log(restItem)
            console.log(allRestItems[restItem])
            item_detail = allRestItems[restItem]

            html_dis +=`
            <div class="card"><img class="card-img-top w-100 d-block" src="${item_detail.img_url}">
                <div class="card-body">
                    <h4 class="card-title" style="color: rgb(0,0,0);">${item_detail.name}</h4>
                    <p class="card-text" style="color: rgb(0,0,0);">Description: ${item_detail.description}</p>
                    <p class="card-text" style="color: rgb(0,0,0);">Price: $ ${item_detail.price.toFixed(2)}</p><button class="btn btn-primary" type="button" style="background: rgb(6,51,184);">Delete</button><button class="btn btn-primary" type="button" style="float: right;background: rgb(6,51,184);">Edit</button>
                </div>
            </div>`; 
        }
            document.getElementById("listOfItemsbyRes").innerHTML = html_dis;
   })

