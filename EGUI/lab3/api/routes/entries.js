const router = require("express").Router();
const Entry = require("../models/Entry");
const bcrypt = require('bcrypt');


//Create Entry
router.post("/", async(request, response)=>{
    const newEntry = new Entry(request.body);
    try{
        const savedEntry = newEntry.save();
        response.status(200).json(savedEntry);
        return;
    }catch(err){
        response.status(500).json(err);
        return;
    }
})

//Update Entry
router.put("/:id", async(request, response)=>{
    console.log("test");
    const newEntry = new Entry(request.body);
    try{
        const entry = await Entry.findById(request.params.id);
        if(entry.login === request.body.login){
            try{
                const updatedEntry = await Entry.findByIdAndUpdate(
                    request.params.id,
                    {
                        $set: request.body,
                    },
                    { new : true }
                );
                response.status(200).json(updatedEntry);
                return;
            }catch(err){
            response.status(500).json(err);
            return;
            }
        }else{
            response.status(401).json("You can not update entry that is not yours")
            return;
        }



        }catch(err){
        response.status(500).json(err);
        return;
    }
})

//Delete Entry
router.delete("/:id", async(request, response)=>{
    console.log("test");
    const newEntry = new Entry(request.body);
    try{
        const entry = await Entry.findById(request.params.id);
        if(entry.login === request.body.login){
            try{
                await entry.delete();
                response.status(200).json("Entry deleted");
                return;
            }catch(err){
            response.status(500).json(err);
            return;
            }
        }else{
            response.status(401).json("You can not delete entry that is not yours")
            return;
        }



        }catch(err){
        response.status(500).json(err);
        return;
    }
})
//Get Entry
router.get("/:id", async (request, response) => {
    try {
        const entry = await Entry.findById(request.params.id);
        response.status(200).json(entry);
        return;
    } catch (err) {
        response.status(500).json(err);
        return;
    }
})

//Get all entries
router.get("/", async (request, response) => {
    const login = request.query.login;
    try {
        let entries;
        if(login){
            entries = await Entry.find({login});
        } else {
            entries = await Entry.find();
        }
        response.status(200).json(entries);
        return;
    } catch (err) {
        response.status(500).json(err);
        return;
    }
})

module.exports = router;