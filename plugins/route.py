from aiohttp import web

routes = web.RouteTableDef()

# Define the HTML content for the homepage
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASV Bot - Welcome</title>
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            color: #333;
            scroll-behavior: smooth;
        }
        .navbar {
            font-family: 'Slab Serif', Courier;
            background-color: #333;
            overflow: hidden;
            position: fixed;
            top: 0;
            left: 10%; /* 5% margin from the left */
            right: 10%; /* 5% margin from the right */
            padding: 14px 0; /* Adjust padding as needed */
            box-sizing: border-box;
            z-index: 1000;
            transition: background-color 0.3s;
            border-radius: 15px;
            display: flex;
            justify-content: space-evenly;
        }

        .navbar a {
            color: #f2f2f2;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            transition: background-color 0.3s, color 0.3s;
        }

        .navbar a:hover {
            background-color: #ddd;
            color: black;
            border-radius: 12px;
        }
        .hero-section, .content-section {
            width: 90%; /* Set the width of the sections */
            padding: 60px 20px; /* Padding inside the sections */
            box-sizing: border-box; /* Include padding and border in the element's total width and height */
            text-align: center; /* Center-align text */
            margin: 0 auto; /* Center the section horizontally with equal distance from left and right */
        }
        .hero-section {
            background: #fefdf2; /* Background color */
            padding-top: 100px; /* Top padding to avoid overlapping with navbar */
            border-bottom: 1px solid #ccc; /* Bottom border */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow */
        }
        .hero-section h1 {
            font-size: 4em; /* Font size for the heading */
        }
        .content-section {
            margin-top: 20px; /* Top margin */
            background: white; /* Background color */
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow */
        }
        .content-section h2 {
            margin-top: 0; /* Remove top margin for heading */
        }
        .footer {
            font-family: 'Slab Serif', Courier;
            background-color: #333;
            color: #f2f2f2;
            padding: 20px 0; /* Adjust padding as needed */
            text-align: center;
            border-radius: 15px;
            margin: 40px 5%; /* 5% margin from the left and right */
            box-sizing: border-box;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .footer a {
            color: #f2f2f2;
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer a:hover {
            color: #ddd;
        }
        
        .footer .telegram-link {
            color: #1DA1F2; /* Different font color */
            text-decoration: underline; /* Underline the text */
            transition: color 0.3s;
        }

        .footer .telegram-link:hover {
            color: #0d8bf2; /* Change color on hover */
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }

        .telegram-bot-link {
            color: #1DA1F2;
            text-decoration: none;
        }

        .telegram-bot-link:hover {
            color: #0d8bf2;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="#home">HOME</a>
        <a href="#about">ABOUT</a>
        <a href="#contact">CONTACT</a>
    </div>
    <div></div>

    <div id="home" class="hero-section">
        <div>
        <h1>Welcome to ASV Bot</h1>
        <p>Your gateway to seamless file sharing and management. ASV Bot provides you with advanced tools to efficiently organize, share, and manage your files across different platforms. Whether you're a business professional needing streamlined document management or a creative individual sharing multimedia content, ASV Bot is here to simplify your workflow.</p>
        <p>Experience the power of ASV Bot today and discover how easy file management can be. Join thousands of satisfied users who rely on ASV Bot for their everyday file sharing needs.</p>
        <p>For any inquiries or assistance, please contact us at <a href="https://t.me/DarkHumorHub_bot" target="_blank">@DarkHumorHub_bot</a>.</p>
    </div>
    </div>

    <div id="about" class="content-section">
    <h2>About ASV Bot</h2>
    <p>ASV Bot is your ultimate solution for seamless file management and sharing. Designed with user convenience in mind, ASV Bot simplifies the process of organizing and distributing files across various platforms. Whether you're a professional managing documents or a content creator sharing media files, ASV Bot offers robust features to enhance your productivity.</p>
    <p>Our mission is to provide you with a reliable tool that ensures effortless file management. Experience the efficiency and convenience of ASV Bot today and discover how it can streamline your workflow.</p>
    <p>If you encounter any challenges or have questions about using ASV Bot, our dedicated support team is here to assist you. Contact us via <a href="https://t.me/DarkHumorHub_bot" target="_blank">Telegram</a> for prompt assistance.</p>
</div>

    <div id="contact" class="content-section">
    <h2>Contact Us</h2>
    <p>For any inquiries or questions about ASV Bot, feel free to reach out to us via <a href="https://t.me/DarkHumorHub_bot" target="_blank">Telegram</a>. Our dedicated support team is ready to assist you with any issues or queries you may have. Whether you need help with using the bot or have suggestions for improvement, we're here to ensure your experience with ASV Bot is seamless and productive.</p>
</div>

    <div class="footer">
    <p>&copy; 2024 ASV Bot. All rights reserved.</p>
    <p>ASV Bot is dedicated to providing seamless file sharing and management solutions.</p>
    <p>For support or inquiries, please contact us via <a href="https://t.me/DarkHumorHub_bot" target="_blank" class="telegram-link">Telegram</a>.</p>
    <div class="telegram-bounce">
        <a href="
https://t.me/ASVanimeBot?start=" target="_blank" class="telegram-bot-link telegram-link">Start our Telegram bot</a>
    </div>
</div>
    
    <script>
        document.querySelectorAll('.navbar a').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
    
</body>
</html>
"""


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text=html_content, content_type='text/html')
