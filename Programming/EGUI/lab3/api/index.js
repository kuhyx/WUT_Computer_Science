const express = require("express");
const app = express();
const dotenv = require("dotenv");
const mongoose = require("mongoose");
const authRoute = require("./routes/authentication");
const userRoute = require("./routes/users");
const entryRoute = require("./routes/entries");

dotenv.config();
app.use(express.json());

mongoose.connect(process.env.MONGO_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(console.log("Connected to MONGODB")).catch(err=>console.log(err));


app.use("/api/auth", authRoute);
app.use("/api/users", userRoute);
app.use("/api/entries", entryRoute);

app.listen("5000", ()=>{
    console.log("Api is running.");
});