function my_alert(massage){
    let div=document.createElement('div');
    div.setAttribute('id','msg');
    let span = document.createElement('span');
    span.innerHTML = massage;
    div.appendChild(span);
    document.body.appendChild(div);
    clearMsg();

}
function clearMsg(){
    let t = setTimeout(function(){
        document.getElementById('msg').remove();
    },2000)
};

