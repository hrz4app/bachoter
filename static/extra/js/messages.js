$(document).ready(function(){
    $('#send').submit(function(){
        $.ajax({
            url: $('#send').attr('action'),
            data: $('#send').serialize(),
            cache: false,
            type: 'post',
            success: function(data){
                $('.send-message').after(data);
                $('input[name="message"]').val('');
                $('input[name="message"]').focus();
            }
        });
        return false;
    });
});