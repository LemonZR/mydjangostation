
$(function(){
    //music is over
    $(`#mp3Btn`).on('ended', function() {
        console.log("音频已播放完成");
        $('.btn-audio').css({'background':'url(/static/images/b1.png) no-repeat center bottom','background-size':'cover'});
    })
    //player control
    var audio = document.getElementById('mp3Btn');
    audio.volume = .3;
    $('.btn-audio').click(function() {
        event.stopPropagation();//Prevent blistering
        if(audio.paused){ //If the current state is suspended
            $('.btn-audio').css({'background':'url(/static/images/b1.png) no-repeat center bottom','background-size':'cover'});
            audio.play(); //play
            return;
        }else{//It is currently playing
            $('.btn-audio').css({'background':'url(/static/images/b2.png) no-repeat center bottom','background-size':'cover'});
            audio.pause(); //pause
        }
    });
})
