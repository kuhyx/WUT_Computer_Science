import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useState } from 'react';

export default function Register() {
  const [login, setLogin] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [blogTitle, setBlogTitle] = useState("");


  const sendRegisterInfo = async (e) => {
    e.preventDefault();
    const response = await axios.post("auth/register", {
      login,
      email,
      password,
      blogTitle,
    });
  }
    return (
        <Form onSubmit={sendRegisterInfo}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email"
            onChange={e=>setEmail(e.target.value)}
              />
            </Form.Group>
            
            <Form.Group className="mb-3" controlId="formLogin">
            <Form.Label>Login</Form.Label>
            <Form.Control type="login" placeholder="Enter Login" 
            onChange={e=>setLogin(e.target.value)}
              />
            
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBlogTitle">
            <Form.Label>Blog Title</Form.Label>
            <Form.Control type="blogTitle" placeholder="Enter Blog Title" 
            onChange={e=>setBlogTitle(e.target.value)}
            />
            </Form.Group>
            
            <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter Password" 
            onChange={e=>setPassword(e.target.value)}
            />
        </Form.Group>
        <Button variant="primary" type="submit">
            Submit
        </Button>
    </Form>
    );
}