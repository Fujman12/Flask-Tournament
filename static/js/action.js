/**
 * Created by narekmartikian on 01.09.17.
 */
$(function () {
    $('js-signup-form').on('submit', function () {
        var form = $(this)
        $.ajax({
            url:form.attr('action'),
            type:'post',
            data: form.serialize(),
            dataType:'json',
            success: function(data){
                alert(data)
            }
        })
    })
})