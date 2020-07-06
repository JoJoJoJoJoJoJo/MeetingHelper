var intervalId;

function getProgress(task_id) {
    let form = new FormData();
    form.append("task_id", task_id);
    $.ajax({
        "url": "/progress",
        "type": "POST",
        "data": form,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response == 'success'){
                clearInterval(intervalId);
            }
        }
    });
}

$(function () {
    var isIntervalStarted = false;
    $("[name='progress']").click(function() {
        var task_id = this.id.split('-').pop();
        if (!isIntervalStarted) {
            intervalId = setInterval(function(){getProgress(task_id)}, 6000);
        }
    })
})