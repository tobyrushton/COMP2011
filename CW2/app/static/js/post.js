$(document).ready(function(){
    // Set the CSRF token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetupso that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $('#post-btn').on("click", function(){
        const body = $('#post-content').val()

        if(body){
            $.ajax({
                url: '/post',
                type: 'POST',
                data: JSON.stringify({ body }),
                contentType: "application/json; charset=utf-8",
                datatype: 'json',
                success: () => {
                    $('#post-content').val('')
                }
            })
        }
    })
})