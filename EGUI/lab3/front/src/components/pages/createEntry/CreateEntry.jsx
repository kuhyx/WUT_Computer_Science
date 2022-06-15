import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import React from "react";

export default function CreateEntry() {
    return (
        <Form>
        <Form.Group className="mb-3" controlId="formText">
            <Form.Label>Entry Title</Form.Label>
            <Form.Control type="text" placeholder="Enter Entry Title" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formText">
            <Form.Label>Entry</Form.Label>
            <Form.Control type="text" class="mh-100" placeholder="Enter Entry" />
        </Form.Group>

        <Button variant="primary" type="submit">
            Submit
        </Button>
        </Form>
        )
}