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
    },
    mounted: function() {
        const owner = getOwner();
        this.owner_id = owner.owner_id;
        console.log(this.owner_id);

        //Upload Restaurant 
        const createRes = (resInfo) => {
            // RMB to change the oid variable 
            axios.post('http://localhost/create_restaurant/'+this.owner_id, resInfo)
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
        const form = document.getElementById('uploadForm');

        const formEvent = form.addEventListener('submit', event => {
            event.preventDefault();
        });

        const submitBtn = document.getElementById("submitBtn");
        submitBtn.addEventListener('click', function() {
            const name = document.querySelector('#resName').value;
            const is_open = switchStatus
            const address = document.querySelector('#resAddress').value;
            console.log(is_open)

            const resInfo = {name: name, is_open: is_open , address: address};
            createRes(resInfo);
            console.log(resInfo)
            setTimeout(function() {
                window.location.href = "index.html";
            }, 2000)
        });


    }
})





