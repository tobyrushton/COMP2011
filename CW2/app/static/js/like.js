const like = (id) => {
    $.ajax({
        url: `/like`,
        type: 'POST',
        data: JSON.stringify({ id }),
        contentType: "application/json; charset=utf-8",
        datatype: 'json',
        success: (response) => {
            const heartIcon = $(`#post-${id}`).find("button").find("svg")
            if (response.operation == 'add') {
                heartIcon.addClass('liked')
            } else {
                heartIcon.removeClass('liked')
            }
        }
    })
}