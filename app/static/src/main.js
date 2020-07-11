var intervalId;

function onAjaxFail() {
    alert("程序出错了...");
}

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
            let progressButton = $("#getProgress-" + task_id);
            progressButton.parent().prev().text(response);
            if (response === "识别完成"){
                clearInterval(intervalId);
                progressButton.hide();
                $("#getResult-" + task_id).removeClass("hidden");
            }
        },
        fail: function () {
            clearInterval(intervalId);
            onAjaxFail();
        }
    });
}

$(function () {
    var isIntervalStarted = false;
    $("[name='progress']").click(function() {
        var task_id = this.id.split('-').pop();
        if (!isIntervalStarted) {
            intervalId = setInterval(function(){getProgress(task_id)}, 1000 * 60 * 10);
            isIntervalStarted = true;
        }
        getProgress(task_id);
    });
    $("[name='result']").click(function () {
        var task_id = this.id.split('-').pop();
        let resultButton = $(this);
        let form = new FormData();
        form.append("task_id", task_id);
        $.ajax({
            "url": "/result",
            "type": "POST",
            "data": form,
            processData: false,
            contentType: false,
            success: function (response) {
                resultButton.parent().prev().text(response);
                if (response === "识别完成") {
                    $.ajax({
                        "url": "/word",
                        "type": "POST",
                        "data": form,
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            window.open("/file/" + response)
                        },
                        fail: onAjaxFail
                    })
                }
            },
            fail: onAjaxFail
        })
    })
});