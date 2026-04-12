const express = require('express');
const app = express();

require('dotenv').config()

// serve static files
app.use(express.static('public'));

// Routes: Auth
const authRoutes = require('./app/routes/Auth.routes.js');
app.use('/auth', authRoutes);

// Routes: Dashboard
const dashboardRoutes = require('./app/routes/Dashboard.routes.js');
app.use('/dashboard', dashboardRoutes);

app.listen(process.env.SERVER_PORT, process.env.SERVER_ADDRESS, () => {
    console.log('Server is now running...')
});