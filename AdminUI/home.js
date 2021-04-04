window.onload = function() {
    const owner = getOwner();
    const owner_name = owner.name;
    document.getElementById("ownerName").innerHTML = owner_name;

    attachSignOut();
}


new Vue({
    el: "#app",
    data: {
        owner_id: 0,
        restaurants: null
    },
    mounted: function() {
        const owner = getOwner();
        this.owner_id = owner.owner_id;
        this.getRestaurants();
    },
    methods: {
        getRestaurants: async function() {
            const response = await axios.get('http://localhost/get_restaurants/' + this.owner_id);
            this.restaurants = response.data.data;
        },
        selectRestaurant: function(rest_id) {
            window.location.href = "http://localhost:5500/AdminUI/IndividualRes.html?id=" + rest_id;
        },
        editRestaurant: function(rest_id) {
            window.location.href = "http://localhost:5500/AdminUI/UpdateRes.html?id=" + rest_id;
        }
        
    }
})