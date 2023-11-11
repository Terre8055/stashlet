<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap">
    <title>Stashlet- Close Account</title>
</head>
<body class="font-montserrat bg-gray-100">
    <div class="container mx-auto flex items-center justify-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h2 class="text-2xl font-bold mb-6 text-center">Delete and Remove User STORE</h2>
            
            <!-- Login Form -->
            <form action="/auth/close-account" method="post" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-600">Enter Secure User String</label>
                    <input type="text" id="username" name="sus" class="mt-1 p-2 w-full border rounded-md">
                </div>
                              
                <button type="submit" class="bg-blue-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full w-full">
                    Delete Account
                </button>
            </form>
            
            <p class="text-center mt-4 text-gray-600">
                Cancel? <a href="/auth/login" class="text-blue-600">Go back</a>.
            </p>
        </div>
    </div>
</body>
</html>
