import React, { useEffect, useState } from "react";

import Blogs from "../../blogs/Blogs";
import axios from "axios"

export default function Home() {
    const [blogEntries, setBlogEntires] = useState([]);

    useEffect(()=>{
        const fetchEntries = async () => {
            const response = await axios.get("/posts");
            console.log(response);
        }
        fetchEntries();
    },[])
    return (
        <div>

            <Blogs/>
        </div> 
        )
}