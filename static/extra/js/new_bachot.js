$(function() { 
    $('#plus-ex').click(function(){  
        if($(this).hasClass('plus')){
            $(this).removeClass('plus')
            $(this).addClass('ex');
            $('#moment-buttons li').addClass('out');
        } else {
            $(this).removeClass('ex');
            $(this).addClass('plus');
            $('#moment-buttons li').removeClass('out');
        }
        return false;
    });
});
$(document).ready(function(){
    $('#bachTextModal form').submit(function(event){
        event.preventDefault();
        event.stopPropagation();
        var modal = $('#bachTextModal');
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            cache: false,
            type: 'post',
            beforeSend: function() {
                $('#bachTextModal .modal-body').html('<p class="text-center"><img src="/static/assets/img/ajax-loader.gif"></p>');
            },
            success: function(data){
                $(modal).modal('toggle');
                $('#bachTextModal textarea').val('');
                if ($('.timeline').length) {
                    $('.timeline').prepend(data);    
                }
                else {
                    $('.col-md-6').find('.nice-shadow').remove();
                    $('.col-md-6').append('<ul class="timeline"></ul>');
                    $('.timeline').prepend(data); 
                };
                
            },
            error: function(){
                alert('There is an error on submit.');
            }
        });
        return false;
    });
    $('#bachPictureModal form').ajaxForm({
        beforeSend: function() {
            $('#bachPictureModal .modal-body').html('<p class="text-center"><img src="/static/assets/img/ajax-loader.gif"></p>');
        },
        success: function(data){
            $('#bachPictureModal').modal('toggle');
            $('#bachPictureModal textarea').val('');
            if ($('.timeline').length) {
                $('.timeline').prepend(data);    
            }
            else {
                $('.col-md-6').find('.nice-shadow').remove();
                $('.col-md-6').append('<ul class="timeline"></ul>');
                $('.timeline').prepend(data); 
            };
        },
        error: function(){
            alert('There is an error on submit.');
        }
    }); 
    $('#bachLocationModal form').ajaxForm({
        beforeSend: function() {
            $('#bachLocationModal .modal-body').html('<p class="text-center"><img src="/static/assets/img/ajax-loader.gif"></p>');
        },
        success: function(data){
            $('#bachLocationModal').modal('toggle');
            $('#bachLocationModal textarea').val('');
            if ($('.timeline').length) {
                $('.timeline').prepend(data);    
            }
            else {
                $('.col-md-6').find('.nice-shadow').remove();
                $('.col-md-6').append('<ul class="timeline"></ul>');
                $('.timeline').prepend(data); 
            };
        },
        error: function(){
            alert('There is an error on submit.');
        }
    });
    $('#bachListeningModal form').submit(function(event){
        event.preventDefault();
        event.stopPropagation();
        var modal = $('#bachListeningModal');
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            cache: false,
            type: 'post',
            beforeSend: function() {
                $('#bachListeningModal .modal-body').html('<p class="text-center"><img src="/static/assets/img/ajax-loader.gif"></p>');
            },
            success: function(data){
                $(modal).modal('toggle');
                $('#bachListeningModal textarea').val('');
                if ($('.timeline').length) {
                    $('.timeline').prepend(data);    
                }
                else {
                    $('.col-md-6').find('.nice-shadow').remove();
                    $('.col-md-6').append('<ul class="timeline"></ul>');
                    $('.timeline').prepend(data); 
                };
                
            },
            error: function(){
                alert('There is an error on submit.');
            }
        });
        return false;
    });


    $('#bachTextModal').on('shown.bs.modal', function(event){
        $.ajax({
            url: '/bachot/bachot-form/',
            data: {'t': 'T'},
            cache: false,
            type: 'get',
            success: function(data){
                $('#bachTextModal').find('.modal-body').html(data);
            }
        });
    })

    $('#bachPictureModal').on('shown.bs.modal', function(event){
        $.ajax({
            url: '/bachot/bachot-form/',
            data: {'t': 'P'},
            cache: false,
            type: 'get',
            success: function(data){
                $('#bachPictureModal').find('.modal-body').html(data);
            }
        });
    })

    $('#bachLocationModal').on('shown.bs.modal', function(event){
        $.ajax({
            url: '/bachot/bachot-form/',
            data: {'t': 'L'},
            cache: false,
            type: 'get',
            success: function(data){
                $('#bachLocationModal').find('.modal-body').html(data);
            }
        });
    })

    $('#bachListeningModal').on('shown.bs.modal', function(event){
        $.ajax({
            url: '/bachot/bachot-form/',
            data: {'t': 'N'},
            cache: false,
            type: 'get',
            success: function(data){
                $('#bachListeningModal').find('.modal-body').html(data);
            }
        });
    })
});