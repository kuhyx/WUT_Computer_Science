import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function Login() {
    return (
        <Form>
        <Form.Group className="mb-3" controlId="formLogin">
        <Form.Label>Login</Form.Label>
        <Form.Control type="login" placeholder="Enter Login"/>
        
        </Form.Group>
    
        <Form.Group className="mb-3" controlId="formPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Enter Password" 
        />
    </Form.Group>
    <Button variant="primary" type="submit" >
        Login
    </Button>
    </Form>

        );
}