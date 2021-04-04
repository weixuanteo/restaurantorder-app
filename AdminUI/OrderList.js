// rmb to change the variable restid
axios.get('http://localhost/order/restaurant/1').then(responseAllOrders => {
    //console.log(responseAllRes.data);
    var allOrder = responseAllOrders.data.data;
    console.log(allOrder);

    var html_dis = ``;
    //console.log(allRes);
    for (var order in allOrder){
        ord = allOrder[order]
        console.log(ord.order_item);
        var orderStatus = "";
        item_list = "";

        if(ord.order_status.status == 1){
            orderStatus = "Received";
            for (var item in ord.order_item){
                item = ord.order_item[item];
                console.log(item.item_id)
                item_list += `
                <div class="form-check"><input class="form-check-input" type="checkbox" id="formCheck-1"><label class="form-check-label" for="formCheck-1"> ${item.qty} X  ${item.item_id}"need item name"</label></div>
                `;
            }
                html_dis +=` 
                <div class="col-md-4">
                <div class="card">
                    <div class="card-body" style="box-shadow: 0px 0px 13px;">
                        <h4 class="card-title" style="color: rgb(0,0,0);">Order No: ${ord.order_id}</h4>
                        <h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);">Table No:${ord.table_no}</h6>
                        ${item_list}
                        <br><h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);">Order Status: ${orderStatus}</h6>
                        <button id = 'completeButton' onClick="myFun()" class="btn btn-primary" type="button" style="background: rgb(6,51,184);margin-top: 10px;">Complete</button>
                    </div>
                </div>
            </div>`;
        }else{
            // No need to display when order is completed
            orderStatus = "Completed";
        }
        }
            document.getElementById("ordersList").innerHTML = html_dis;
   })


// update order status here 

// var updateOrderStatus = document.getElementById('name');

