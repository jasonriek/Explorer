const videoStream = document.getElementById('video-stream');
        const socket = new WebSocket('wss://' + window.location.host);

        socket.binaryType = 'blob';  // Receive binary data
        let buffer = []; // To accumulate chunks of data
        let isCollecting = false;
        
        let lastFrameTime = 0;
        const minFrameInterval = 100;  // Render frames every 100ms (~10 FPS)
        
        socket.onmessage = function (event) {
            try {
                const now = Date.now();
                if (now - lastFrameTime > minFrameInterval) {
                    const blob = new Blob([event.data], { type: 'image/jpeg' });
                    const url = URL.createObjectURL(blob);
                    videoStream.src = url;
            
                    videoStream.onload = function () {
                        URL.revokeObjectURL(url);  // Release the previous object URL
                    };
            
                    lastFrameTime = now;
                }
            }
            catch(error) {
                console.log(error);
            }

        };
        