// Globals.
var urlFormId = '#tt-url-form';
var urlFormInputId = '#tt-url-form-input';
var videoIFrameId = '#tt-video-iframe';
var labelsListId = '#tt-labels-list';
var initialVideoURL = 'https://www.youtube.com/watch?v=YbcxU1IK7s4';

function setVideoTime(seconds) {
    var iframe = $(videoIFrameId);
    var currentSrc = iframe.attr('src');
    var newSrc = currentSrc.split('?').shift();
    newSrc += "?start=" + seconds + "&autoplay=1";
    iframe.attr('src', newSrc);
    iframe.contentWindow.location.reload();
    return false; // Prevents page reload
}

function secondsToHms(d) {
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);
    return ((h > 0 ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (s < 10 ? "0" : "") + s);
}

$(document).ready(function() {

    var urlForm = $("#tt-url-form");
    var urlFormInput = $('#tt-url-form-input');
    var videoIFrame = $('#tt-video-iframe');
    var labelsList = $('#tt-labels-list');

    // Set up submit Handler
    urlForm.submit(function urlFormSubmit(event) {

        // Don't reload the page.
        event.preventDefault();

        // Set the video URL
        // User gives: https://www.youtube.com/watch?v=YbcxU1IK7s4
        // Embed frame needs: https://www.youtube.com/embed/YbcxU1IK7s4
        var videoId = urlFormInput.val().split('=').pop();
        var embedURL = 'https://www.youtube.com/embed/' + videoId;
        videoIFrame.attr('src', embedURL);

        // Define the request
        var reqBody = {
            url: urlFormInput.val()
        };

        // Post the request
        axios.post('/video', reqBody)
            .then(function responseHandler(response) {
                var labels = response.data.labels;
                var listItems = [];
                for(var key in labels) {
                    // Create the links for each list item.
                    var timeLinks = labels[key].times.map(function(time) {
                        var hms = secondsToHms(time);
                        return '<a onclick="setVideoTime(' + time + ')" href="javascript:void(0)">' +
                            hms + '</a>';
                    });
                    // Capitalize the first letter.
                    key = _.upperFirst(key);
                    // Returns the list item.
                    listItems.push('<li>' + key + ': ' + timeLinks.join(', ') + '</li>');
                }

                // Insert the list items.
                labelsList.html(listItems);
            });

    });

    // Send an initial fake request.
    urlFormInput.val(initialVideoURL);
    urlForm.submit();
});
