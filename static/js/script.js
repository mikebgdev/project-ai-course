function startVideo() {
    const videoSource = document.querySelector('input[name="video-source"]:checked').value;
    let videoUrl = '';

    if (videoSource === 'webcam') {
        videoUrl = '0';
    } else if (videoSource === 'url') {
        videoUrl = document.getElementById('url-input').value;
    } else if (videoSource === 'youtube') {
        videoUrl = document.getElementById('youtube-input').value;
    }

    fetch('/start_video', {
        method: 'POST',
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({type: videoSource, video_url: videoUrl})
    })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => {
            console.error('Error starting video:', error);
        });
}

