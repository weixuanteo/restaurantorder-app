window.onload = function() {
    const owner = getOwner();
    const owner_name = owner.name;
    document.getElementById("ownerName").innerHTML = owner_name;

    attachSignOut();
}


var router = new VueRouter({
    mode:'history',
    routes: []
});


new Vue({
    router,
    el: '#app',
    data:{
        rest_id:0
    },
    created:function(){
        this.rest_id = this.$route.query.id
        console.log(this.rest_id);

        // display restaurant name 
        axios.get('http://localhost/restaurant/'+this.rest_id).then(responseRest =>{
            var rest_name = ``;
            var restaurant = responseRest.data.data;
            console.log(restaurant.name)
            rest_name = `
            <h3 id="restaurant_name" class="text-dark mb-0" style="color: rgb(4,4,4);font-size: 30px;">${restaurant.name}</h3>`;
            
            document.getElementById("restaurant_name").innerHTML = rest_name;
        })

        // display restaurant items 
        axios.get('http://localhost/restaurant/'+this.rest_id+'/items').then(responseAllResItems => {
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
    },
    methods: {
        addNewItem: function() {
            window.location.href = "UploadMenu.html?id=" + this.rest_id;
        },
        viewOrders: function() {
            window.location.href = "OrderList.html?id=" + this.rest_id;
        }
    }



})









