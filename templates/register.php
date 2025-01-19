<!DOCTYPE html>
<html lang="en">

<head>
    <title>User Login</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="nav/pets.png" type="image/x-icon">

    <style>
        
        body {
            font-family: Arial, sans-serif;
        }

        .container {
            margin-top: 10%;
            margin-left: 18%;
            width: 30%;
        }

        input[type="text"],
        input[type="password"],
        input[type="submit"] {
            width: 35%;
            padding: 10px;
            margin: 0px 0;
            display: inline-block;
            border: 1px solid black;
            box-sizing: border-box;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }

        .picture {
            width: 50%;
            box-shadow: 5px 10px #888888;
            margin-top: -29%;
            margin-left: 50%;
        }
    </style>
</head>

<body>
    {% extends 'base.html' %}

    {% block title %}Home{% endblock %}

    {% block content %}


    <div class="container">
        <h2>Register</h2>
        <form method="POST">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
        <br>Already an User ? <br>

        <a href="login">Login Now</a><br>
    </div>
    <div class="picture">
        <img src="static\1.png" height="100%" width="100%">
    </div>
    {% endblock %}
</body>

</html>