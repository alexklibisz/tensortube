
// Shitty globals.
var urlFormId = '#tt-url-form';
var urlFormInputId = '#tt-url-form-input';
var videoIFrameId = '#tt-video-iframe';
var labelsListId = '#tt-labels-list';
var initialVideoURL = 'https://www.youtube.com/embed/YbcxU1IK7s4';

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

$( document ).ready(function() {

    var urlForm = $("#tt-url-form");
    var urlFormInput = $('#tt-url-form-input');
    var videoIFrame = $('#tt-video-iframe');
    var labelsList = $('#tt-labels-list');

    // Set up submit Handler
    urlForm.submit(function urlFormSubmit( event ) {

      // Don't reload the page.
      event.preventDefault();

      // Define the request
      var reqBody = { url: urlFormInput.val() };

      // Set the video.
      videoIFrame.attr('src', reqBody.url);

      // Post the request

      // What we get back from the server.
      var resBody = {
        labels: [
          {
            name: 'cat',
            times: ['30', '60', '90']
          },
          {
            name: 'dog',
            times: ['40', '80', '120']
          }
        ]
      };

      // Create the string for each list item.
      var listItems = resBody.labels.map(function(label) {
        var timeLinks = label.times.map(function(time) {
          var hms = secondsToHms(time);
          return '<a onclick="setVideoTime(' + time + ')" href="javascript:void(0)">'
            + hms + '</a>';
        });
        // Capitalize the first letter.
        label.name = _.upperFirst(label.name);
        // Returns the list item.
        return '<li>' + label.name + ': ' + timeLinks.join(', ') + '</li>';
      });

      // Insert the list items.
      labelsList.html(listItems);

    });

    // Send an initial fake request.
    urlFormInput.val(initialVideoURL);
    urlForm.submit();
});
