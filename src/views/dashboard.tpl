<!-- Updated dashboard.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap">
    <title>Your Dashboard - Stashlet Kit</title>
</head>
<body class="d-font-montserrat d-body bg-gray-100">
    <div class="dashboard-container">
        <!-- Sidebar -->
        <nav class="sidebar">
            <div class="sidebar-header">
                <h2 class="text-2xl font-bold text-white">Stashlet Kit</h2>
            </div>
            <ul class="sidebar-menu">
                <li><a href="#" class="active">Create Collection</a></li>
                <li><a href="#">View Collections</a></li>
                <li><a href="#">Delete Collection</a></li>
                <li><a href="#">Update Collection</a></li>
            </ul>
            <div class="settings-button">
                <a href="/auth/close-account">
                    <button class="settings-btn">Close</button>
                </a>
            </div>
            <div class="logout-button">
                <a href="/auth/logout">
                    <button class="settings-btn">Logout</button>
                </a>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Your content goes here -->
            <h1 class="text-3xl font-bold mb-4">Welcome to Your Dashboard</h1>
            <p class="text-gray-600">Start organizing your web resources efficiently.</p>
        </div>
    </div>
</body>
</html>
