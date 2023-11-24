<!-- Updated HTML for Login Page -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/styles.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap">
    <title>Login to Your Stashlet Kit</title>
</head>
<body class="font-montserrat bg-gray-100">
    <div class="login-container mx-auto flex items-center justify-center h-screen">
        <div class="login-form bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h2 class="text-2xl font-bold mb-6 text-center">Login to Your Stashlet Kit</h2>
            
            <!-- Login Form -->
            <form action="/auth/login" method="post" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-600">Enter User String</label>
                    <input type="text" id="username" name="request_string" class="input-field">
                </div>
                              
                <button type="submit" class="login-button">
                    Login
                </button>
            </form>
            
            <p class="text-center mt-4 text-gray-600">
                Don't have an account? <a href="/auth/register" class="text-link">Register here</a>.
            </p>
            <p class="text-center mt-2 text-gray-600">
                Forgot strings? <a href="/auth/forgot-password" class="text-link">Retrieve strings here</a>.
            </p>
        </div>
    </div>
</body>
</html>
