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
        rest_id:0,
        restaurantItems:null
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

        this.getRestaurantItems();
    },
    methods: {
        getRestaurantItems: async function(){
            const response = await axios.get('http://localhost/restaurant/'+this.rest_id+'/items');
            this.restaurantItems = response.data.data;
            console.log(this.restaurantItems)
        },
        addNewItem: function() {
            window.location.href = "UploadMenu.html?id=" + this.rest_id;
        },
        updateItem:function(item_id){
            window.location.href = "UpdateMenu.html?rest_id="+this.rest_id+"&id=" + item_id;
        },
        viewOrders: function() {
            window.location.href = "OrderList.html?id=" + this.rest_id;
        },
        viewStripeDashboard: function() {
            const ownerObj = getOwner();
            axios.get('http://localhost/payment/dashboard/' + ownerObj.stripe_account).then(response => {
                const dashboard_url = response.data.data.url;
                window.location.href = dashboard_url;
            })
        }
    }
})









