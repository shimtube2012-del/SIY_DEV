import webbrowser

def show_popup():
    popup_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>생일 축하합니다.</title>
        <script>
            function playSound() {
                var audio = new Audio('https://example.com/bapbapre.mp3'); // 음성 효과 파일 URL
                audio.play();
            }
            window.onload = function() {
                alert('생일 축하합니다!');
                playSound();
            };
        </script>
    </head>
    <body>
        <h1>생일 축하합니다!</h1>
    </body>
    </html>
    """
    
    webbrowser.open_new_tab('data:text/html;charset=utf-8,' + popup_html)

if __name__ == '__main__':
    show_popup()
