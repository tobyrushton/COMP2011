$(document).ready(function(){
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