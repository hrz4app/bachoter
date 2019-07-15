$(document).ready(function(){

    var buddyClick = function(event) {

        event.preventDefault();
        event.stopPropagation();

        var $form = $(this);
        var url = $form.attr('action');

        $.post(url, $form.serialize()).done(function(data) {
            if (data == 'buddy') {
                $('#buddy-click').hide();
                $('#pending-click').show();
            }
            else if (data == 'accept') {
                $('#accept-click').hide();
                $('#unbuddy-click').show();
                setTimeout(function(){
                    location.reload();
                }, 1000);
            }
            else if (data == 'delete') {
                $('#pending-click').hide();
                $('#unbuddy-click').hide();
                $('#buddy-click').show();
            }
        });
    };

    $('#buddy-click').submit(buddyClick);
    $('#unbuddy-click').submit(buddyClick);
    $('#accept-click').submit(buddyClick);
    $('#pending-click').submit(buddyClick);

    $('.btn-accept').mouseover(function() {
        $('.btn-accept').removeClass('btn-default').addClass('btn-success');
    });
    $('.btn-accept').mouseout(function() {
        $('.btn-accept').removeClass('btn-success').addClass('btn-default');
    });

    $('.btn-pending').mouseover(function() {
        $('.btn-pending').html('Cancel...');
    });
    $('.btn-pending').mouseout(function() {
        $('.btn-pending').html('Pending...');
    });

    $('.btn-buddy').mouseover(function() {
        $('.btn-buddy').removeClass('btn-default').addClass('btn-success');
    });
    $('.btn-buddy').mouseout(function() {
        $('.btn-buddy').removeClass('btn-success').addClass('btn-default');
    });

    $('.btn-buddying').mouseover(function() {
        $('.btn-buddying').html('UNBUDDY').removeClass('btn-success').addClass('btn-danger');
    });
    $('.btn-buddying').mouseout(function() {
        $('.btn-buddying').html('BUDDYING').removeClass('btn-danger').addClass('btn-success');
    });
});