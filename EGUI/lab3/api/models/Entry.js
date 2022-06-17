const mongoose = require("mongoose");

const EntrySchema = new mongoose.Schema({
    title:{
        type:String,
        required: true
    },
    description:{
        type:String,
        required:true,
    },
    login:{
        type:String,
        required:true,
    }
    
},
{ timestamps: true }
);

module.exports = mongoose.model("Entry", EntrySchema);