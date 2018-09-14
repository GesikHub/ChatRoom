function sendMessage(user_id, chat_id) {
    let textMessage = document.getElementById('textMessage');
    if(!!$.trim(textMessage.value)) {
        $.post('/set_message', {
            text: textMessage.value.toString(),
            sender: user_id,
            chat_room: chat_id,
        }).done(function (response) {
            if (response['message'] == '200') {
                $("#messages").append('<div class="message right">\n' +
                    '<div class="message-text">' + textMessage.value.toString() + '</div>\n' +
                    '</div>');
                textMessage.value = '';
            }
        }).fail(function () {
            alert('Error: Could not contact server.');
        });
    }
}