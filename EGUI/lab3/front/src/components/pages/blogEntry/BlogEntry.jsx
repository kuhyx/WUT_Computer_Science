import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useEffect } from "react";

import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { useState } from 'react';

export default function BlogEntry() {
  const location = useLocation();
  const id = location.pathname.split("/")[2];
  const [entry, setEntry] = useState({});

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
    <Button variant="primary p-4">Edit</Button>
    <Button variant="primary m-5 p-4">Remove</Button>
  </Card.Body>
</Card>
        )
}