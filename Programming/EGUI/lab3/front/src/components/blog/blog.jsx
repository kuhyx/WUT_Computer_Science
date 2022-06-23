import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import { Link } from 'react-router-dom';
import React from "react";

export default function Blog({entry}) {
    const detailsString = `/blogEntry/` + entry._id;
    return (
<Card style={{ width: '40rem', height:'40rem', margin:'1rem'}}>
 
  <Card.Body>
  
    <Card.Title> {entry.title}</Card.Title>
    <Card.Text>
      Author: { entry.login }
      </Card.Text>
    <Card.Text>
      Created at: { new Date (entry.createdAt).toDateString() }
      </Card.Text>
    <Card.Text>
          
        {entry.description}
    </Card.Text>
    <Link to={detailsString}>Details</Link>

  </Card.Body>
</Card>
        )
}