import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useEffect } from "react";

import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Context } from '../../../context/Context';
import axios from 'axios';
import { useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { useState } from 'react';

export default function BlogEntry() {

  const location = useLocation();
  const id = location.pathname.split("/")[2];
  const [entry, setEntry] = useState({});
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

  const handleEdit = async() => {
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
        <Card.Title class="text-center display-1 m-5"> { entry.title } </Card.Title>
  <Card.Header class="text-center "> { entry.login } </Card.Header>
  <Card.Header class="text-center "> Created at: { new Date (entry.createdAt).toDateString() } </Card.Header>
  <Card.Body>
    
    <Card.Text >
      { entry.description }
    </Card.Text>
    <Button variant="primary p-4 " onClick={handleEdit}>Edit</Button>
    <Button variant="primary m-5 p-4" onClick={handleRemove }>Remove</Button>
  </Card.Body>
</Card>
        )
}