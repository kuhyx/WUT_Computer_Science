const router = require("express").Router();
const User = require("../models/User");
const bcrypt = require('bcrypt');


//GET USER
router.get("/:id", async(request, response)=>{
    try{
        const user = await User.findById(request.params.id);
        const {password, ...others} = user._doc;
        response.status(200).json(others);
        return;
    }catch(err){
        response.status(500).json(err);
        return;
    }
})

module.exports = router;