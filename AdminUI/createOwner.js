var username = document.getElementById('name');
var email = document.getElementById('email');
var password = document.getElementById('password');


//const getData = () =>{
//    axios.get('localhost/owner/registration').then(response=>{
//        console.log(response);
//    })
//};

//POST
function addOwner() {
    axios({
        method: 'post',
        url: 'localhost/owner/registration',
        data:{
            email: email,
            name: username,
            password: password
        }
    })
} 
document.getElementById('register').addEventListener('click', addOwner);