// Globals.
var urlFormId = '#tt-url-form';
var urlFormInputId = '#tt-url-form-input';
var videoIFrameId = '#tt-video-iframe';
var labelsListId = '#tt-labels-list';
var initialVideoURL = 'https://www.youtube.com/watch?v=YbcxU1IK7s4';
var availableListId = '#tt-available-list'

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

function loadVideo(id) {
    var urlFormInput = $(urlFormInputId);
    urlFormInput.val('http://youtu.be/' + id);
    urlFormInput.submit();
}

$(document).ready(function() {

    var urlForm = $(urlFormId);
    var urlFormInput = $(urlFormInputId);
    var videoIFrame = $(videoIFrameId);
    var labelsList = $(labelsListId);
    var availableList = $(availableListId)

    // Ask for cached section stuff
    axios.get('/cached')
        .then(function (response) {
            var thumbs = response.data.map(function(id) {
               return '<div class="col-md-2"><a onclick="loadVideo(\'' + id + '\')"'
                 + 'href="javascript:void(0)"> '
                 + '<img src="http://img.youtube.com/vi/' + id + '/1.jpg" '
                 + 'height="90" width="120"> </a> </div>';
            }).join('');
            availableList.html(thumbs)
        });

    // Set up submit Handler
    urlForm.submit(function urlFormSubmit(event) {
        labelsList.html('<p>Loading</p>')

        // Don't reload the page.
        event.preventDefault();

        // Set the video URL
        // User gives: https://www.youtube.com/watch?v=YbcxU1IK7s4
        // Embed frame needs: https://www.youtube.com/embed/YbcxU1IK7s4
        var url = urlFormInput.val()
        var videoId = url.split("v=").length == 2 ? url.split("v=").pop() : url.split('/').pop()

        var embedURL = 'https://www.youtube.com/embed/' + videoId;
        videoIFrame.attr('src', embedURL);

        // Define the request
        var reqBody = {
            url: urlFormInput.val()
        };

        // Post the request
        axios.post('/video', reqBody)
            .then(function responseHandler(response) {
                var displayLabels;
                if (response.data.hasOwnProperty('sortedLabels')) {
                    displayLabels = response.data.sortedLabels.slice(0, 10); // {0 : "label"}
                }
                else {
                    alert("Response wasn't good");
                    console.log(response.data);
                }
                var listItems = [];
                var label;
                var info;
                for(var i in displayLabels) {
                    label = displayLabels[i];
                    info = response.data.labels[label];
                    // Create the links for each list item.
                    var timeLinks = info.times.map(function(time) {
                        var hms = secondsToHms(time);
                        return '<a class="" onclick="setVideoTime(' + time + ')" href="javascript:void(0)">' +
                            hms + '</a>';
                    });
                    // Capitalize the first letter.
                    label = _.upperFirst(label);
                    // Returns the list item.
                    var labelLink = '<a class="labelLink" target="_blank" href="http://imagenet.stanford.edu/synset?wnid=' + info.labelId + '">' + label + '</a>';
                    listItems.push('<li>' + labelLink + ': ' + timeLinks.join(', ') + '</li>');
                }

                // Insert the list items.
                labelsList.html(listItems);
            });

    });

    // Send an initial fake request.
    urlFormInput.val(initialVideoURL);
    urlForm.submit();
});
