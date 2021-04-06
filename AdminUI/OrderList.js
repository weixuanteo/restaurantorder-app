window.onload = function() {
    const owner = getOwner();
    const owner_name = owner.name;
    document.getElementById("ownerName").innerHTML = owner_name;

    attachSignOut();
}

const url_string = window.location.href;
const url = new URL(url_string)
const rest_id = url.searchParams.get("id");

new Vue({
    el: "#app",
    data: {
        orders: null,
    },
    mounted: function() {
        axios.get("http://localhost/get_orders/" + rest_id).then(response => {
            this.orders = response.data.data;
            console.log(this.orders)

        }).catch(error => {
            console.log(error)
        })
    },
    methods: {
        checkInitialStatus: function(status) {
            if (status == 1) {
                return true;
            }
            return false;
        },
        checkPreparingStatus: function(status) {
            if (status == 2) {
                return true;
            }
            return false;
        },
        checkCompletedStatus: function(status) {
            if (status == 3) {
                return true;
            }
            return false;
        },
        updateStatus: function(order_id, status) {
            data = {"status": status}
            axios.put("http://localhost/order/status/" + order_id, json=data).then((response) => {
                if (response.data.status == "success") {
                    axios.get("http://localhost/get_orders/" + rest_id).then(response => {
                        this.orders = response.data.data;
                        console.log(this.orders)
            
                    }).catch(error => {
                        console.log(error)
                    })
                }
            }).catch((error) => {
                console.log(error)
            })
        }
    }
})


// axios.get('http://localhost/get_orders/' + rest_id).then(responseAllOrders => {
//     //console.log(responseAllRes.data);
//     var allOrder = responseAllOrders.data.data;
//     // console.log(allOrder);

//     var html_dis = ``;
//     //console.log(allRes);
//     for (var order in allOrder){
//         ord = allOrder[order];
//         var id = ord.order_id;
//         // console.log(ord.order_item);
//         var orderStatus = "";
//         item_list = "";

//         if (ord.order_status.status == 1) {
//             orderStatus = "Preparing";
//             for (var item in ord.order_item){
//                 item = ord.order_item[item];
//                 // console.log(item.item_id)
//                 item_list += `
//                     <p> <strong>${item.qty} X  ${item.name}</strong></p>
//                 `;
//             }
//                 html_dis +=` 
//                 <div class="col-md-4">
//                 <div class="card">
//                     <div class="card-body" style="box-shadow: 0px 0px 13px;">
//                         <h4 id='order_oid' class="card-title" style="color: rgb(0,0,0);">Order No: ${ord.order_id}</h4>
//                         <h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);">Table No: ${ord.table_no}</h6>
//                         ${item_list}
//                         <br><h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);" id="status">Order Status: ${orderStatus}</h6>
//                         <div class="popup" id='orderItem'  onclick="putOrderComplete()">
//                         <button class="btn btn-primary" id="orderCompleted" order_value='${ord.order_id}' type="button" style="background: rgb(6,51,184);margin-top: 10px;">Complete</button>
//                         </div>
//                     </div>
//                 </div>
//             </div>`;
//         } else if (ord.order_status.status == 2) {

//         } else {
//             // No need to display when order is completed
//             orderStatus = "Completed";
//         }
//     }
//             document.getElementById("ordersList").innerHTML = html_dis;
// })

// function putOrderPreparing() {

// }

// // update order status here 
// function putOrderComplete() {

//     var choseOrder_id = document.getElementById('orderCompleted').getAttribute('order_value');
//     console.log (choseOrder_id);

//     var popup;
//     if (confirm("Order is ready to serve?") == true) {
//         popup = "Data saved successfully!";   
//     } 
//     else {
//         popup = "Save Canceled!";
//     }

//     axios({
//         method:'put',
//         url:"http://localhost/order/updatestatus/"+choseOrder_id,
//         data:{
//             status: 3
//         }
//     })
//   }
//   document.getElementById('orderCompleted').addEventListener('click', putOrderComplete);
//   window.location.reload();
