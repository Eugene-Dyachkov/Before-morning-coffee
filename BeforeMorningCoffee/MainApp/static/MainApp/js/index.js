
document.addEventListener('DOMContentLoaded',function(){
    var connection = new WebSocket('ws://192.168.1.107:8855/');

    connection.onopen = () =>{
        console.log("its OK");
    }


}, false);
