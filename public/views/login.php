
<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://fonts.googleapis.com/css2?family=Carter+One&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,200..1000;1,200..1000&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css"/>
    <link rel="stylesheet" type="text/css" href="../css/login-styles.css">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
</head>
<body>
    <div class="container">
        <div class="left">
            <div class="logo-and-text">
                <h1>ZIUTKI<br>GYM</h1>
                <img class="logo" src="../img/logo.png" alt="Logo">
            </div>
            <img class="benchGuy" src="../img/cute-man-barbell.png" alt="bench">
        </div>

        <div class="right">
            <h1>Login</h1>
            <div class="meesages">
                <?php 
                    if (isset($messages)) {
                        foreach ($messages as $message) {
                            echo $message;
                        }
                    }
                ?>
            </div>
            <form action="login" method="POST">
                <input name="email" type="text" placeholder="✉️ Email" autocomplete="on" maxlength="25" minlength="3" required>
                <input name="password" type="password" placeholder="🔒 Password" autocomplete="off" maxlength="32" minlength="8" required>
                <button class="loginButton" type="submit">Login</button>
                <div class="forgotPasswordContainer">
                    <a class="forgotPassword" href="/reset-password">Forgot password?</a>
                </div>
                    
                <div class="separator">
                    <hr>
                    <span>OR</span>
                    <hr>
                </div>
                
                <div class="socialLogin">
                    <div class="facebook">
                        <button class="facebookLogin"><i class="fa-brands fa-facebook"></i>  Login with Facebook</button>
                    </div>
                    <div class="google">
                        <button class="googleLogin"><i class="fa-brands fa-google"></i>  Login with Google</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</body>
</html>