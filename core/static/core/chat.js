function resetFormElement(e) {
  e.wrap('<form>').closest('form').get(0).reset();
  e.unwrap();

  // Prevent form submission
  e.stopPropagation();
  e.preventDefault();
}

$(document).ready(function() {
    $(".chat").scrollTop($(".chat")[0].scrollHeight);
    var form = $(".input");

    $('#button_attach').change(function() {
        var file = $('#button_attach')[0].files[0];
        $(".attached_file_span").text("Выбран файл: " + file.name);
        $(".attached_file").css('display', 'block');
        $(".chat").css('height', 'calc(100% - 80px - 70px - 22px)');
        $(".chat").animate({ scrollTop: $(".chat")[0].scrollHeight}, 800);
    });

    form.on('submit', function (e) {
        e.preventDefault();
        $(".attached_file").css('display', 'none');
        $(".chat").css('height', 'calc(100% - 80px - 60px)');

        const formData = new FormData(this);

        if ($("#button_attach")[0].files[0] != undefined || $("#message_input").val() != "") {
            $.ajax({
                type: 'POST',
                url: '/message_create/',
                data: formData,
                processData: false,
                contentType: false,

                success: (result) => {
                    $('.chat').append(result['rendered_template']);
                    $('#message_input').val("");
                    resetFormElement($("#button_attach"))
                    $(".chat").animate({ scrollTop: $(".chat")[0].scrollHeight}, 800);
                }
            });
        }
        else {
            console.log($("#button_attach")[0].files[0] != undefined, $("#message_input").val())
        }


    });

    setInterval(function () {
        var lastId = $('.message').last().data("id");
        if (lastId == null){
            lastId = 0;
        }
        $.ajax({
            type: 'GET',
            url: '/messages/',
            data: {'last_id': lastId},


            success: (result) => {
                if (result.toString().indexOf('<title>') + 1) {
                    window.location.replace('../login');
                }
                else if (result !== ""){
                    $('.chat').append(result);
                    $(".chat").animate({ scrollTop: $(".chat")[0].scrollHeight}, 800);
                }
            }
        });
    }, 1000);
});
