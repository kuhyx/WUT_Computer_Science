import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import React from "react";

export default function BlogEntry() {
    return (
<Card>
        <Card.Title class="text-center display-1 m-5"> Entry Title </Card.Title>
  <Card.Header class="text-center "> Author: </Card.Header>
  <Card.Header class="text-center "> Created: </Card.Header>
  <Card.Body>
    
    <Card.Text >
      Entry content
    </Card.Text>
    <Button variant="primary p-4">Edit</Button>
    <Button variant="primary m-5 p-4">Remove</Button>
  </Card.Body>
</Card>
        )
}