$(document).ready(function()
{

    $('.updateButton').on('click', function(){

        var likes = $(this).attr('likesTotsl');

        var new_likes = int(likes) + 1

        req = $.ajax({
            url: '/feed/',
            type:'POST',
            data: {new_likes: new_likes}

        });
        req.done(function(){

     
$('#likesTotsl').fadeout(500).fadeIn(500);
$('likesT').text(new_likes);
        });
    });
});


function funct(a){
    event.preventDefault()
}