function alert(massage){
    document.body.innerHTML+=("<div id='msg'><span>"+massage+"</span></div>");
    clearMsg();
}
function clearMsg(){
    let t = setTimeout(function(){
        document.getElementById('msg').remove();
    },2000)
};

