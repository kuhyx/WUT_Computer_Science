import 'bootstrap/dist/css/bootstrap.min.css';

import Button from 'react-bootstrap/Button';
import { Context } from '../../../context/Context';
import Form from 'react-bootstrap/Form';
import { Link } from 'react-router-dom';
import axios from "axios";
import { useContext } from 'react';
import { useRef } from 'react';

export default function Login() {
    const passwordRef = useRef();
    const userRef = useRef();
    const { dispatch, isFetching } = useContext(Context);
    const handleSubmit = async (e)=>{
        e.preventDefault();
        dispatch({type:"LOGIN_START"});
        try{
            const response = await axios.post("/auth/login", {
                login: userRef.current.value,
                password: passwordRef.current.value,
            })
            dispatch({type:"LOGIN_SUCCESS", payload: response.data});
        }catch(err){
            dispatch({type:"LOGIN_FAILURE"});
        }
     }


    return (
        <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formLogin">
        <Form.Label>Login</Form.Label>
        <Form.Control type="login" placeholder="Enter Login"
            ref={userRef}
        />
        
        </Form.Group>
    
        <Form.Group className="mb-3" controlId="formPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Enter Password"
        ref={passwordRef} 
        />
    </Form.Group>
    <Button variant="primary" type="submit" disabled={isFetching}>
        Login
    </Button>
    </Form>

        );
}