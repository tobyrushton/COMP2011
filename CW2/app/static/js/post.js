$(document).ready(function(){
    // on click for the post button sends a request to create post
    $('#post-btn').on("click", function(){
        const body = $('#post-content').val()

        // if the body is not empty, send a request to the server to create a post
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