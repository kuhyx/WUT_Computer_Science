import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button'
import { Context } from '../../../context/Context';
import Form from 'react-bootstrap/Form'
import React from "react";
import axios from 'axios';
import { useContext } from 'react';
import { useState } from 'react';

export default function CreateEntry() {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const {user} = useContext(Context);
 
    const handleSubmit = async (e) => {
        e.preventDefault();
        const newEntry = {
            login: user.login,
            title,
            description,
        };
    try{
        const response = await axios.post("http://localhost:5000/api/entries", newEntry);
        console.log(response.data);
        window.location.replace("blogEntry/" + response.data._id);
    }catch(err){
        console.log(err);
    }
};
    return (
        <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formText">
            <Form.Label>Entry Title</Form.Label>
            <Form.Control type="text" placeholder="Enter Entry Title" 
                onChange={e=>setTitle(e.target.value)}
            />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formText">
            <Form.Label>Entry</Form.Label>
            <Form.Control type="text" class="mh-100" placeholder="Enter Entry" 
                onChange={e=>setDescription(e.target.value)}
            />
        </Form.Group>

        <Button variant="primary" type="submit">
            Submit
        </Button>
        </Form>
        )
}