import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import React from "react";

export default function Blog() {
    return (
<Card style={{ width: '40rem', height:'40rem', margin:'1rem'}}>
 
  <Card.Body>
    <Card.Title>Blog title</Card.Title>
    <Card.Text>
        Blog text
    </Card.Text>
    <Button variant="primary">Details</Button>
  </Card.Body>
</Card>
        )
}