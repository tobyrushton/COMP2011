// sends a request to the server to like a post
const like = (id) => {
    $.ajax({
        url: `/like`,
        type: 'POST',
        data: JSON.stringify({ id }),
        contentType: "application/json; charset=utf-8",
        datatype: 'json',
        success: (response) => {
            // on completion of the request, the heart icon is updated to reflect the new state
            const heartIcon = $(`#post-${id}`).find("button").find("svg")
            if (response.operation == 'add') {
                heartIcon.addClass('liked')
            } else {
                heartIcon.removeClass('liked')
            }
        }
    })
}