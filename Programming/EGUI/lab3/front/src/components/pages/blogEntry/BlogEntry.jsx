import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useEffect } from "react";

import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Context } from '../../../context/Context';
import Form from 'react-bootstrap/Form'
import axios from 'axios';
import { useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { useState } from 'react';

export default function BlogEntry() {

  const location = useLocation();
  const id = location.pathname.split("/")[2];
  const [entry, setEntry] = useState({});
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [updateMode, setUpdateMode] = useState(false);
  const { user } = useContext(Context);

  const handleRemove = async() => {
    try{
    await axios.delete(`http://localhost:5000/api/entries/${entry._id}`, {
      data: {login:user.login} });
    window.location.replace("/");
    }catch(err)
    {
      console.log(err);
    }
  }

  const saveEdit = async() => {
    setUpdateMode(false);
    try{
      await axios.put(`http://localhost:5000/api/entries/${entry._id}`, {
          login:user.login,
        title:title,
      description:description});
      }catch(err)
      {
        console.log(err);
      }
  }

  const handleEdit = async() => {
    setUpdateMode(true);
    try{
    await axios.delete("posts/" + id, {login:user.login});
    }catch(err)
    {
      console.log(err);
    }
  }

  useEffect(()=>{
    const getEntry = async () =>{
      const response = await axios.get("/entries/" + id);
      setEntry(response.data);
    };
    getEntry();
  })
    return (
<Card>
        {updateMode ?         <Form.Group className="mb-3" controlId="formText">
            <Form.Label>Entry Title</Form.Label>
            <Form.Control type="text" placeholder="Enter Entry Title" 
                onChange={e=>setTitle(e.target.value)}
            />
        </Form.Group> : <Card.Title class="text-center display-1 m-5"> { entry.title } </Card.Title> }
  <Card.Header class="text-center "> { entry.login } </Card.Header>
  <Card.Header class="text-center "> Created at: { new Date (entry.createdAt).toDateString() } </Card.Header>
  <Card.Body>
  {updateMode ?         <Form.Group className="mb-3" controlId="formText">
            <Form.Label>Entry</Form.Label>
            <Form.Control type="text" class="mh-100" placeholder="Enter Entry" 
                onChange={e=>setDescription(e.target.value)}
            />
        </Form.Group> : 
    <Card.Text >
      { entry.description }
    </Card.Text> }
    {user.login === entry.login ? updateMode ?  <Button variant="primary p-4 " onClick={saveEdit}>Save edit</Button> : <Button variant="primary p-4 " onClick={handleEdit}>Edit</Button> : ""}
    {user.login === entry.login ? <Button variant="primary m-5 p-4" onClick={handleRemove }>Remove</Button> : ""}
  </Card.Body>
</Card>
        )
}