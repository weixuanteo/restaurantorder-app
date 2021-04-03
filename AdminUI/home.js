// rmb to change the variable OID
axios.get('http://localhost/get_restaurants/1').then(responseAllRes => {
       //console.log(responseAllRes.data);
       var allRes = responseAllRes.data.data;
       console.log(allRes);

       var html_dis = ``;
       var status = "";

       //console.log(allRes);
       for (var res in allRes){
           console.log(allRes[res])
           var status = "";
           rest = allRes[res]
           console.log(rest.name)
           if (rest.is_open == true){
               status = "Open";
           }else{
               status = "Closed";
           }
           html_dis +=` 
                <div class="col-md-4">
                <div class="card">
                <div class="card"><img class="card-img-top w-100 d-block" src="assets/img/res5.jpg">
                        <h4 class="card-title" style="font-family: Bangers, cursive;color: rgb(0,0,0);">${rest.name}</h4>
                        <h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);">${rest.address}</h6>
                        <p class="card-text" style="color: rgb(0,0,0);">Hours: ${status}</p><button class="btn btn-primary" type="button" style="background: rgb(6,51,184);">Select</button>
                    </div>
                </div>
            </div>
        `;
        }
            document.getElementById("listOfRes").innerHTML = html_dis;
   })


{/* <div class="col-md-4">
   <div class="card">
   <div class="card"><img class="card-img-top w-100 d-block" src="assets/img/crispy-fried-chicken-plate-with-salad-carrot.jpg">
           <h4 class="card-title" style="font-family: Bangers, cursive;color: rgb(0,0,0);">${rest.name}</h4>
           <h6 class="text-muted card-subtitle mb-2" style="color: rgb(0,0,0);">${rest.address}</h6>
           <div class="simple-slider">
               <div class="swiper-container">
                   <div class="swiper-wrapper">
                       <div class="swiper-slide" style="background: url(&quot;https://cdn.bootstrapstudio.io/placeholders/1400x800.png&quot;) center center / cover no-repeat;"></div>
                       <div class="swiper-slide" style="background: url(&quot;https://cdn.bootstrapstudio.io/placeholders/1400x800.png&quot;) center center / cover no-repeat;"></div>
                       <div class="swiper-slide" style="background: url(&quot;https://cdn.bootstrapstudio.io/placeholders/1400x800.png&quot;) center center / cover no-repeat;"></div>
                   </div>
                   <div class="swiper-pagination"></div>
                   <div class="swiper-button-prev"></div>
                   <div class="swiper-button-next"></div>
               </div>
           </div>
           <p class="card-text" style="color: rgb(0,0,0);">${rest.is_open}</p><button class="btn btn-primary" type="button" style="background: rgb(6,51,184);">Select</button>
       </div>
   </div>
</div> */}