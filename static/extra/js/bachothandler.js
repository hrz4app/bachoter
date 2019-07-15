$(document).on('submit', 'form.likes-dislikes', function(event){
    event.preventDefault();
    event.stopPropagation();
    var li = $(this).closest('li');
    var text = $(li).find('.bachot-text');
    var bachot_id = $(li).attr("bachot-id");
    $.ajax({
        url: $(this).attr('action'),
        data: $(this).serialize(),
        cache: false,
        type: 'post',
        success: function(data){
            $(text).next('.progress').remove();
            $(text).next('.btn-group-justified').remove();
            $(data).insertAfter(text);
        }
    });
    return false;
});
$(document).on('click', 'button.delete-bachot', function(){
    var li = $(this).closest('li');
    var bachot_id = $(li).attr('bachot-id');
    var csrf = $(li).attr('csrf');
    $.ajax({
        url: '/bachot/delete/',
        data: {
            'bachot_id': bachot_id,
            'csrfmiddlewaretoken': csrf
        },
        cache: false,
        type: 'post',
        success: function(data){
            $(li).fadeOut(400,function(){
                $(li).remove();
            });
        }
    });
    return false;
});
$(document).on('click', 'button.delete-comment', function(){
    var li = $(this).closest('li');
    var comment_id = $(li).attr('comment-id');
    var bachot_id = $(li).attr('bachot-id');
    var csrf = $(li).attr('csrf');
    var li_bachot = $('li.timeline-inverted[bachot-id="'+bachot_id+'"');
    var comment_count = $(li_bachot).find('.comment-count');
    var comment_count_data = parseInt($(li_bachot).find('.comment-count').html());
    $.ajax({
        url: '/bachot/delete-comment/',
        data: {
            'comment_id': comment_id,
            'csrfmiddlewaretoken': csrf
        },
        cache: false,
        type: 'post',
        success: function(data){
            $(li).prev($('hr')).remove();
            $(li).next($('hr')).remove();
            $(li).remove();
            if (data == 0){
                $('#bachCommentModal').find('ul.media-list').append('<h4 class="text-center">Nothing to show.</h4>');
            };
            $(comment_count).html(comment_count_data-1);
        }
    });
    return false;
});
$(document).ready(function(){
    $('[data-hover="tooltip"]').tooltip({
        trigger: 'hover'
    });
    $('#bachCommentModal').on('show.bs.modal', function(event){
        var btn = $(event.relatedTarget)
        var li = $(btn).closest('li');
        var bachot_id = $(li).attr('bachot-id');
        $(this).find('input[name="bachot_id"]').val('').val(bachot_id);
        $.ajax({
            url: '/bachot/get-comments/',
            data: {
                'b': bachot_id
            },
            cache: false,
            type: 'get',
            success: function(data){
                $('#bachCommentModal').find('.modal-body').html(data);
            }
        });
    });
    $('form#comments').submit(function(event){
        event.preventDefault();
        event.stopPropagation();
        var bachot_id = parseInt($(this).find('input[name="bachot_id"]').val());
        var li = $('li.timeline-inverted[bachot-id="'+bachot_id+'"');
        var comment_count = $(li).find('.comment-count');
        var comment_count_data = parseInt($(li).find('.comment-count').html());
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            cache: false,
            type: 'post',
            success: function(data){
                $('#bachCommentModal').find('textarea[name="text"]').val('');
                $('#bachCommentModal').find('textarea[name="text"]').focus();
                if ($('#bachCommentModal').find('ul.media-list').find('h4[class="text-center"]').length){
                    $('#bachCommentModal').find('ul.media-list').find('h4').remove();
                }
                else if ($('#bachCommentModal').find('ul.media-list').find('h4[class="text-center"]').length == 0){
                    $('#bachCommentModal').find('ul.media-list').append('<hr style="border-color:#d4d4d4;">');
                };
                $('#bachCommentModal').find('ul.media-list').append(data);
                $(comment_count).html(comment_count_data+1);
            }
        });
        return false;
    });
});