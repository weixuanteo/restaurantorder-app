// rmb to change the variable restid
axios.get('http://localhost/get_orders/1').then(responseAllOrders => {
    //console.log(responseAllRes.data);
    var allOrder = responseAllOrders.data.data;
    // console.log(allOrder);

    var html_dis = ``;
    //console.log(allRes);
    for (var order in allOrder){
        ord = allOrder[order];
        var id = ord.order_id;
        // console.log(ord.order_item);
        var orderStatus = "";
        item_list = "";

        if(ord.order_status.status == 1){
            orderStatus = "Preparing";
            for (var item in ord.order_item){
                item = ord.order_item[item];
                // console.log(item.item_id)
                item_list += `
                <div class="form-check"><input class="form-check-input" type="checkbox" id="formCheck-1"><label class="form-check-label" for="formCheck-1"> ${item.qty} X  ${item.name}</label></div>
                `;
            }
                html_dis +=` 
                <div class="col-md-4">
                <div class="card">
                    <div class="card-body" style="box-shadow: 0px 0px 13px;">
                        <h4 id='order_oid' class="card-title" style="color: rgb(0,0,0);">Order No: ${ord.order_id}</h4>
                        <h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);">Table No: ${ord.table_no}</h6>
                        ${item_list}
                        <br><h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);" id="status">Order Status: ${orderStatus}</h6>
                        <br><h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);" id="status">Price: $${ord.price.toFixed(2)}</h6>
                        <div class="popup" id='orderItem'  onclick="putOrderComplete()">
                        <button class="btn btn-primary" id="orderCompleted" order_value='${ord.order_id}' type="button" style="background: rgb(6,51,184);margin-top: 10px;">Complete</button>
                        </div>
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
function putOrderComplete() {

    var choseOrder_id = document.getElementById('orderCompleted').getAttribute('order_value');
    console.log (choseOrder_id);

    var popup;
    if (confirm("Order is ready to serve?") == true) {
        popup = "Data saved successfully!";   
    } 
    else {
        popup = "Save Canceled!";
    }

    axios({
        method:'put',
        url:"http://localhost/order/updatestatus/"+choseOrder_id,
        data:{
            status: 2
        }
    })
  }
  document.getElementById('orderCompleted').addEventListener('click', putOrderComplete);
  window.location.reload();
