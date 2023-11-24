<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/styles.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap">
    <title>Stashlet - Forgot Strings</title>
</head>
<body class="font-montserrat bg-gray-100">
    <div class="container mx-auto flex items-center justify-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h2 class="text-2xl font-bold mb-6 text-center">Verify User ID and Secured User String to recover account</h2>
            
            <!-- Login Form -->
            <form action="/auth/forgot-password" method="post" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-600">Enter User ID</label>
                    <input type="text" id="username" name="user_id" class="mt-1 p-2 w-full border rounded-md">
                </div>
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-600">Enter Secured User String</label>
                    <input type="text" id="username" name="sus" class="mt-1 p-2 w-full border rounded-md">
                </div>
                              
                <button type="submit" class="login-button">
                    Verify
                </button>
            </form>
            
            <p class="text-center mt-4 text-gray-600">
                Remembered Strings? <a href="/auth/login" class="text-link">Abort Verification</a>.
            </p>
        </div>
    </div>
</body>
</html>
