function persons_feed() {
    $.ajax({
        url: '/persons_feed',
        type: 'GET',
        success: function (data) {
            $('#results').html(data);
        },
        error: function (xhr, status, error) {
            console.error('Error to load results:', error);
        },
        complete: function () {
            setTimeout(persons_feed, 3000);
        }
    });
}

persons_feed();
