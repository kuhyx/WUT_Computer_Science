import 'bootstrap/dist/css/bootstrap.min.css';

import Container from 'react-bootstrap/Container'
import { Context } from '../../context/Context';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar'
import { useContext } from 'react';

export default function TopBar() {
  const {user, dispatch} = useContext(Context);

  const handleLogout = () => {
    dispatch({type: "LOGOUT"});
  }
    return (
<Navbar bg="light" expand="lg">
  <Container>
    <Navbar.Brand href="">Lab 3 Blog, user: {user.login}</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="me-auto">
        <Nav.Link href="/">Home</Nav.Link>
        <Nav.Link href="/login">{user ? "" : "Login"}</Nav.Link>
        <Nav.Link href="/register">{user ? "" : "Register"}</Nav.Link>
        {user ?  <Nav.Link onClick={handleLogout}> Logout </Nav.Link> : "" }
        <Nav.Link href="/createEntry"> {user ? "Create entry" : ""}
        
</Nav.Link>
        </Nav>
    </Navbar.Collapse>
  </Container>
</Navbar>
    )
}
