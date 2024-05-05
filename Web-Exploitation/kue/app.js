const jwt = require("jsonwebtoken");
const express = require("express");
const cookieParser = require("cookie-parser");
const fs = require("fs");

const app = express();
app.use(cookieParser());

const JWT_SECRET = "your_secret_key";

const verifyJWT = (req, res, next) => {
    const token = req.cookies.auth;
    jwt.verify(token, JWT_SECRET, (err, decoded) => {
        if (err) return res.sendStatus(403);
        if (!decoded.roles) return res.sendStatus(403);
        req.roles = decoded.roles;
        next();
    });
};

app.get("/", (req, res) => {
    // Check if the client sent a cookie named 'auth'
    if (req.cookies.auth) {
        try {
            const decoded = jwt.verify(req.cookies.auth, JWT_SECRET);
            res.send(
                `Welcome back! Your username is ${decoded.username} and your roles are ${decoded.roles}`
            );
        } catch (error) {
            res.send("Invalid token. Please refresh to get a new token.");
        }
    } else {
        // User visits for the first time, set a JWT cookie
        const token = jwt.sign(
            { username: "new_user", roles: "user" },
            JWT_SECRET,
            {
                expiresIn: "1d",
            }
        );
        res.cookie("auth", token, {
            httpOnly: true, // Cookie accessible only by web server
            maxAge: 86400000, // Cookie expires after 1 day
        });
        res.send(
            "Hello, first time visitor! We have set a secure cookie for you."
        );
    }
});

app.get("/flag", verifyJWT, (req, res) => {
    try {
        if (req.roles !== "admin") return res.sendStatus(403);
        res.send(fs.readFileSync("flag.txt", "utf8"));
    } catch (error) {
        res.sendStatus(403);
    }
});

// Start the server on port 6060
app.listen(6060, () => {
    console.log("Server is running on http://localhost:6060");
});
