const router = require("express").Router();
const User = require("../models/User");
const bcrypt = require('bcrypt');

//REGISTERING
router.post("/register", async (request, response)=>{
    try{
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(request.body.password, salt);
        const newUser = new User({
            login: request.body.login,
            email: request.body.email,
            password: hashedPassword,
        });

        const user = await newUser.save();
        response.status(200).json(user);
    } catch(err){
        response.status(500).json(err);
    }
});


// login
router.post("/login", async (request, response) => {
    try {
        const user = await User.findOne({ login: request.body.login });
        if(!user) 
        {
            response.status(400).json("Wrong login!");
            return;
        }

        
        const validated = await bcrypt.compare(request.body.password, user.password);
        if(!validated) 
        {
            response.status(400).json("Wrong password!");
            return;
        }
        
        const {password, ...others} = user._doc;
        response.status(200).json(others);
        return;
    } catch (err) {
        response.status(500).json(err);
    }
})

module.exports = router; 