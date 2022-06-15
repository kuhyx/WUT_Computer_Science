import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function Register() {
    return (
        <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email"
              />
            </Form.Group>
            
            <Form.Group className="mb-3" controlId="formLogin">
            <Form.Label>Login</Form.Label>
            <Form.Control type="login" placeholder="Enter Login" 
              />
            
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBlogTitle">
            <Form.Label>Blog Title</Form.Label>
            <Form.Control type="blogTitle" placeholder="Enter Blog Title" 
            />
            </Form.Group>
            
            <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter Password" 
            />
        </Form.Group>
        <Button variant="primary" type="submit">
            Submit
        </Button>
    </Form>
    );
}