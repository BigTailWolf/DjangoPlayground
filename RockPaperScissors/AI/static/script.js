function process() {
    console.log(this);
    fetch('/process/'+this.id)
        .then(data => data.json())
        .then(data => {
            console.log(data);
            $('#ai').attr('src', 'static/'+data.ai_choice+'.png');

            if (data.result == 'win') {
                console.log('Process Win')
                $('#win_score').text(data.win);
                $('#result').html('<h2>WIN</h2>');
                $('#result').css('background-color', 'darkgreen')
            }
            if (data.result == 'tie') {
                console.log('Process Tie')
                $('#tie_score').text(data.tie);
                $('#result').html('<h2>TIE</h2>');
                $('#result').css('background-color', 'goldenrod')
            }
            if (data.result == 'loss') {
                console.log('Process Loss')
                $('#loss_score').text(data.loss);
                $('#result').html('<h2>LOSS</h2>');
                $('#result').css('background-color', 'red')
            }
        })
}

$(document).ready(function(){

    console.log('Page loaded')

    $('#rock').click(process);
    $('#paper').click(process);
    $('#scissors').click(process);

    var modal = document.getElementById("myModal");

    $('#view_records').click(function() {
        modal.style.display = "block";
    });

    $('.close').click(function() {
        modal.style.display = "none";
    });
});
