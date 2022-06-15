import React, { useEffect, useState } from "react";

import Blogs from "../../blogs/Blogs";
import axios from "axios"

export default function Home() {
    const [blogEntries, setBlogEntires] = useState([]);
    
    useEffect(()=>{
        const fetchEntries = async () => {
            console.log("Fetching: ");
            const response = await axios.get("/entries");
            setBlogEntires(response.data);
        }
        fetchEntries();
    },[])
    return (
        <div>

             <Blogs entries={blogEntries} /> 
        </div> 
        )
}